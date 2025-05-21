from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from myprofile.models import UserProfile, Skill, PersonalityTag, ClassType, SkillCategory
from .forms import CreateProfileForm, ProfileAvatarForm
from django.contrib import messages
from django.http import JsonResponse

# ==========================
# 建立用戶個人資料（初次填寫）
# ==========================
@login_required
def create_profile(request):
    # 若使用者已經建立過 UserProfile，則直接導向 profile 頁面
    if hasattr(request.user, 'userprofile'):
        return redirect('profile_view')

    if request.method == 'POST':
        form = CreateProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # 建立 UserProfile 物件
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()

            # 設定多對多欄位
            profile.want_to_learn.set(request.POST.getlist('want_to_learn'))
            profile.can_teach.set(request.POST.getlist('can_teach'))
            profile.personality.set(request.POST.getlist('personality'))
            profile.class_type.set(request.POST.getlist('class_type'))

            messages.success(request, '個人資料已成功建立！')
            return redirect('profile_view')
    else:
        form = CreateProfileForm()

    # GET 請求：顯示表單
    skills = Skill.objects.all()
    tags = PersonalityTag.objects.all()
    class_types = ClassType.objects.all()
    categories = SkillCategory.objects.values_list('name', flat=True).distinct()

    return render(request, 'myprofile/create_profile.html', {
        'form': form,
        'skills': skills,
        'tags': tags,
        'categories': categories,
        'class_types': class_types,
    })


# ================================================
# 編輯個人資料（用 get_object_or_404 取得 profile）
# ================================================
@login_required
def edit_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        if request.FILES.get('avatar'):
            profile.avatar = request.FILES['avatar']
        profile.instagram = request.POST.get('instagram')
        profile.city = request.POST.get('city')
        profile.self_intro = request.POST.get('self_intro')
        profile.available_time = request.POST.get('available_time')
        profile.want_to_learn.set(request.POST.getlist('want_to_learn'))
        profile.can_teach.set(request.POST.getlist('can_teach'))
        profile.personality.set(request.POST.getlist('personality'))
        profile.class_type.set(request.POST.getlist('class_type'))
        profile.save()
        return redirect('profile_view')

    skill_categories = SkillCategory.objects.prefetch_related('skills').all()
    tags = PersonalityTag.objects.all()
    class_types = ClassType.objects.all()

    return render(request, 'myprofile/edit_profile.html', {
        'profile': profile,
        'skill_categories': skill_categories,
        'tags': tags,
        'class_types': class_types,
    })



# ==========================
# 顯示個人資料（含推薦教師）
# ==========================
@login_required
def profile_view(request):
    # 獲取要查看的用戶名
    username = request.GET.get('username')

    if username:
        # 如果提供了用戶名，顯示該用戶的資料
        try:
            profile = UserProfile.objects.get(user__username=username)
            # 檢查該用戶是否已發布個人資料
            if not profile.is_published and profile.user != request.user:
                messages.warning(request, '該用戶的個人資料尚未發布')
                return redirect('category')
        except UserProfile.DoesNotExist:
            messages.error(request, '找不到該用戶的個人資料')
            return redirect('category')
    else:
        # 否則顯示當前登入用戶的資料
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            # 若尚未建立 UserProfile，導向建立頁面
            return redirect('create_profile')

    # 取得使用者想學的技能
    skills_to_learn = profile.want_to_learn.all()
    # 根據這些技能找出能教的人（排除自己）
    suggested_teachers = UserProfile.objects.filter(
        can_teach__in=skills_to_learn,
        is_published=True  # 只顯示已發布的教師
    ).exclude(id=profile.id).distinct()

    return render(request, 'myprofile/profile.html', {
        'profile': profile,
        'suggested_teachers': suggested_teachers,
        'is_own_profile': profile.user == request.user,
        'class_types': ClassType.objects.all()  # 添加 class_types 到上下文
    })

@login_required
def update_avatar(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        form = ProfileAvatarForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Avatar has been updated successfully!')
            return redirect('profile_view')
    else:
        form = ProfileAvatarForm(instance=profile)

    return render(request, 'myprofile/update_avatar.html', {
        'form': form,
        'profile': profile
    })

@login_required
def toggle_publish(request):
    if request.method == 'POST':
        profile = get_object_or_404(UserProfile, user=request.user)
        profile.is_published = not profile.is_published
        profile.save()

        messages.success(request,
            '您的個人資料已{}'.format('發布' if profile.is_published else '隱藏'))
        return redirect('profile_view')
    return redirect('profile_view')