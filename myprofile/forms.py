from django import forms
from .models import UserProfile, Skill, PersonalityTag, ClassType

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar', 'instagram', 'city', 'self_intro']
        widgets = {
            'avatar': forms.FileInput(attrs={'class': 'form-control'}),
            'instagram': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'self_intro': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['avatar']