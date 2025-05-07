from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth import get_user_model

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '註冊成功！')
            return redirect('home')
        else:
            # 顯示表單驗證錯誤
            for field in form:
                for error in field.errors:
                    messages.error(request, f'{field.label}: {error}')
            if form.non_field_errors():
                for error in form.non_field_errors():
                    messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'歡迎回來，{username}！')
            return redirect('home')
        else:
            # 檢查使用者是否存在
            User = get_user_model()
            if User.objects.filter(username=username).exists():
                messages.error(request, '密碼錯誤，請重試。')
            else:
                messages.error(request, '查無此帳號，請確認使用者名稱是否正確。')
                return render(request, 'registration/login.html', {
                    'username': username,  # 保留使用者輸入的帳號
                    'show_register': True
                })
    return render(request, 'registration/login.html')

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, '您已成功登出。')
    return redirect('home')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # 先登出
        user.delete()    # 刪除帳號
        messages.success(request, '您的帳號已成功註銷。')
        return redirect('home')
    return render(request, 'registration/delete_account.html')
