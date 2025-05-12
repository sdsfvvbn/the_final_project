from django.db import models
from django.conf import settings

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    want_to_learn = models.ManyToManyField(Skill, related_name='learners')
    can_teach = models.ManyToManyField(Skill, related_name='teachers')
    personality = models.ManyToManyField(Tag, blank=True)  # 例如 Calm, Patient
    available_time = models.TextField(blank=True, null=True)  # 自由填寫的時間描述
    self_intro = models.TextField(blank=True, null=True)  # 自由填寫的自我介紹

    def __str__(self):
        return self.user.username