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

class Review(models.Model):
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_given')
    rated_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews_received')
    is_completed = models.BooleanField(default=False)  # 標記交換是否完成
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5星評分
    comment = models.TextField(blank=True, null=True)  # 評論內容
    created_at = models.DateTimeField(auto_now_add=True)  # 評價時間

    class Meta:
        unique_together = ('reviewer', 'rated_user')  # 確保每個用戶只能對另一個用戶評價一次
        ordering = ['-created_at']  # 按時間倒序排列

    def __str__(self):
        return f"{self.reviewer.username}'s review for {self.rated_user.username}"