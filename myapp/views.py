from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, PasswordResetRequestForm
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.conf import settings
import logging
import random
import string
from django.contrib.auth.hashers import make_password

logger = logging.getLogger(__name__)

# Create your views here.
def home(request):
    return render(request, 'homepage/TalentSwap.html')

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '註冊成功！')
            return redirect('homepage')
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
            return redirect('homepage')
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
    return redirect('homepage')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        logout(request)  # 先登出
        user.delete()    # 刪除帳號
        messages.success(request, '您的帳號已成功註銷。')
        return redirect('homepage')
    return render(request, 'registration/delete_account.html')

def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            User = get_user_model()
            try:
                user = User.objects.get(email=email)
                # 生成重設密碼的 token
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))

                # 添加調試日誌
                logger.info(f'User ID: {user.pk}')
                logger.info(f'Generated uid: {uid}')
                logger.info(f'Generated token: {token}')

                # 建立重設密碼的連結
                try:
                    # 確保 uid 是字符串
                    uid_str = uid.decode('utf-8')
                    logger.info(f'Decoded uid: {uid_str}')

                    reset_url = request.build_absolute_uri(
                        reverse('password_reset_confirm', kwargs={'uidb64': uid_str, 'token': token})
                    )
                    logger.info(f'Generated reset URL: {reset_url}')
                except Exception as e:
                    logger.error(f'Error generating reset URL: {str(e)}')
                    logger.error(f'Error type: {type(e)}')
                    logger.error(f'Error args: {e.args}')
                    messages.error(request, f'生成重設密碼連結時發生錯誤：{str(e)}')
                    return redirect('myapp:login')

                # 發送電子郵件
                subject = '重設您的密碼'
                message = render_to_string('registration/password_reset_email.html', {
                    'user': user,
                    'reset_url': reset_url,
                })

                try:
                    # 檢查郵件設定
                    if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
                        raise ValueError('郵件設定不完整')

                    # 發送郵件
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [email],
                        fail_silently=False,
                        html_message=message
                    )
                    logger.info(f'密碼重設郵件已發送到 {email}')
                    messages.success(request, '重設密碼的連結已發送到您的電子郵件。')
                    return redirect('password_reset_done')
                except ValueError as ve:
                    logger.error(f'郵件設定錯誤：{str(ve)}')
                    messages.error(request, '郵件設定錯誤，請聯繫管理員。')
                except Exception as e:
                    logger.error(f'發送密碼重設郵件時發生錯誤：{str(e)}')
                    messages.error(request, '發送郵件時發生錯誤，請稍後再試。')

                return redirect('myapp:login')
            except User.DoesNotExist:
                logger.warning(f'嘗試重設密碼的電子郵件不存在：{email}')
                messages.error(request, '找不到使用此電子郵件的帳號。')
    else:
        form = PasswordResetRequestForm()

    return render(request, 'registration/password_reset_request.html', {'form': form})

def password_reset_confirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
        logger.warning(f'無效的密碼重設連結：uidb64={uidb64}, token={token}')

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')

            if password and password == password_confirm:
                try:
                    user.set_password(password)
                    user.save()
                    logger.info(f'使用者 {user.username} 的密碼已成功重設')
                    messages.success(request, '您的密碼已成功重設。請使用新密碼登入。')
                    return redirect('myapp:password_reset_complete')
                except Exception as e:
                    logger.error(f'重設密碼時發生錯誤：{str(e)}')
                    messages.error(request, '重設密碼時發生錯誤，請稍後再試。')
            else:
                messages.error(request, '密碼不符合或為空。')

        return render(request, 'registration/password_reset_confirm.html')
    else:
        messages.error(request, '重設密碼的連結無效或已過期。')
        return redirect('myapp:password_reset_request')
