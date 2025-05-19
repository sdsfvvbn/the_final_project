from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from myprofile.models import UserProfile, Skill, PersonalityTag

# ==========================
# 建立用戶個人資料（初次填寫）
# ==========================
@login_required
def create_profile(request):
    # 若使用者已經建立過 UserProfile，則直接導向 profile 頁面
    if hasattr(request.user, 'userprofile'):
        return redirect('profile_view')

    if request.method == 'POST':
        # 從表單取得使用者提交的資料
        avatar = request.FILES.get('avatar')
        instagram = request.POST.get('instagram')
        city = request.POST.get('city')
        skills_to_learn = request.POST.getlist('want_to_learn')
        skills_to_teach = request.POST.getlist('can_teach')
        personalities = request.POST.getlist('personality') # 多選：ManyToMany
        class_type = request.POST.get('class_type')
        self_intro = request.POST.get('self_intro') 

        # 建立 UserProfile 物件（不包含多對多欄位）
        profile = UserProfile.objects.create(
            user=request.user,
            avatar=avatar,
            instagram=instagram,
            city=city,
            class_type=class_type,
            self_intro=self_intro
        )

        # 設定多對多欄位（技能、個性）
        profile.want_to_learn.set(skills)
        profile.can_teach.set(skills)
        profile.personality.set(personalities)

        # 儲存後導向 profile 頁面
        return redirect('profile_view')

    # GET 請求：顯示表單
    skills = Skill.objects.all()
    tags = PersonalityTag.objects.all()  
    categories = ["language", "art", "music", "sports", "cooking"]

    return render(request, 'create_profile.html', {
        'skills': skills,
        'tags': tags,
        'categories': categories 
    })



# ================================================
# 編輯個人資料（用 get_object_or_404 取得 profile）
# ================================================
@login_required
def edit_profile(request):
    # 嘗試取得目前登入使用者的 UserProfile，找不到就自動回傳 404
    profile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        # 依表單資料更新 profile
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
    # GET 請求，顯示表單
    skills = Skill.objects.all()
    tags = PersonalityTag.objects.all()
    # ... 其他 context
    return render(request, 'edit_profile.html', {
        'profile': profile,
        'skills': skills,
        'tags': tags,
        # ... 其他 context
    })


# ==========================
# 顯示個人資料（含推薦教師）
# ==========================
@login_required
def profile_view(request):
    try:
        # 嘗試取得目前登入使用者的 UserProfile
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # 若尚未建立 UserProfile，導向建立頁面
        return redirect('create_profile')

    # 取得使用者想學的技能
    skills_to_learn = profile.want_to_learn.all()
    # 根據這些技能找出能教的人（排除自己）
    suggested_teachers = UserProfile.objects.filter(
        can_teach__in=skills_to_learn
    ).exclude(id=profile.id).distinct()

    return render(request, 'myprofile/profile.html', {
        'profile': profile,
        'suggested_teachers': suggested_teachers
    })