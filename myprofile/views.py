from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import UserProfile

@login_required
def profile_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # 如果沒有 UserProfile，重定向到創建頁面
        return redirect("create_profile")  # 假設有一個名為 create_profile 的 URL

    # 根據使用者的需求篩選符合條件的老師
    skills_to_learn = profile.want_to_learn.all()
    suggested_teachers = UserProfile.objects.filter(
        can_teach__in=skills_to_learn
    ).exclude(id=profile.id).distinct()

    # 將老師的數據傳遞到模板
    return render(request, "profile.html", {
        "profile": profile,
        "suggested_teachers": suggested_teachers
    })