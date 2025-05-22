from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label='電子郵件',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '請輸入您的電子郵件'})
    )

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 自定義其他欄位的樣式
        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': '請輸入名字'})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': '請輸入姓'})
        self.fields['username'].widget.attrs.update({'class': 'form-control', 'placeholder': '請輸入使用者名稱'})
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': '請輸入密碼'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': '請再次輸入密碼'})

        # 自定義欄位標籤
        self.fields['first_name'].label = '名字'
        self.fields['last_name'].label = '姓'
        self.fields['username'].label = '使用者名稱'
        self.fields['password1'].label = '密碼'
        self.fields['password2'].label = '確認密碼'

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('此電子郵件已被註冊。')
        return email

class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(
        label='電子郵件',
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': '請輸入您的電子郵件'})
    )