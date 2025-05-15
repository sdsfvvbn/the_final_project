from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from myprofile.models import UserProfile, Skill, Tag

@login_required
def create_profile(request):
    # 檢查是否已經有 UserProfile
    if hasattr(request.user, 'userprofile'):
        return redirect('profile_view')  # 如果已經有 UserProfile，重定向到 profile_view

    if request.method == 'POST':
        # 獲取表單數據
        avatar = request.FILES.get('avatar')
        instagram = request.POST.get('instagram')
        skills = request.POST.getlist('skills')
        personality = request.POST.getlist('personality')
        self_intro = request.POST.get('self_intro')
        city = request.POST.get('city')

        # 創建 UserProfile 對象
        profile = UserProfile.objects.create(
            user=request.user,
            avatar=avatar,
            instagram=instagram,
            self_intro=self_intro,
            city=city
        )

        # 添加技能和個性標籤
        profile.want_to_learn.set(skills)
        profile.personality.set(personality)

        # 重定向到 profile_view
        return redirect('profile_view')

    # 如果是 GET 請求，渲染表單頁面
    skills = Skill.objects.all()  # 獲取所有技能
    tags = Tag.objects.all()  # 獲取所有標籤
    return render(request, 'myprofile/create_profile.html', {
        'skills': skills,
        'tags': tags
    })

def profile_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect('create_profile')  # 如果沒有 UserProfile，重定向到 create_profile

    return render(request, 'myprofile/profile.html', {
        'profile': profile,
    })