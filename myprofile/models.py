from django.db import models
from django.contrib.auth.models import User
from your_app_name.models import Skill, Tag  # 替換 your_app_name 為實際應用名稱

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    want_to_learn = models.ManyToManyField(Skill, related_name='learners')
    can_teach = models.ManyToManyField(Skill, related_name='teachers')
    personality = models.ManyToManyField(Tag, blank=True)  # 例如 Calm, Patient
    available_time = models.TextField(blank=True, null=True)  # 自由填寫的時間描述
    self_intro = models.TextField(blank=True, null=True)  # 自由填寫的自我介紹

    def __str__(self):
        return self.user.username