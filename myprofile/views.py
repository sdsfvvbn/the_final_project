from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from myprofile.models import UserProfile

@login_required
def profile_view(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        return redirect("create_profile")  # 如果沒有 UserProfile，重定向到創建頁面

    # 根據學生的需求篩選推薦老師
    skills_to_learn = profile.want_to_learn.all()
    suggested_teachers = UserProfile.objects.filter(
        can_teach__in=skills_to_learn
    ).exclude(id=profile.id).distinct()

    return render(request, "profile.html", {
        "profile": profile,  # 當前學生的資料
        "suggested_teachers": suggested_teachers  # 推薦老師的資料
    })