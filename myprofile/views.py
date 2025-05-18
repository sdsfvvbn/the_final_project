from django.shortcuts import render, redirect
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
        self_intro = request.POST.get('self_intro')
        skills_to_learn = request.POST.getlist('want_to_learn')
        skills_to_teach = request.POST.getlist('can_teach')
        personalities = request.POST.getlist('personality')  # 多選：ManyToMany

        # 建立 UserProfile 物件（尚未加入多對多欄位）
        profile = UserProfile.objects.create(
            user=request.user,
            avatar=avatar,
            instagram=instagram,
            city=city,
            self_intro=self_intro
        )

        # 設定多對多欄位（技能、個性）
        profile.want_to_learn.set(skills)
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
