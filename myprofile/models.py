from django.db import models
from django.conf import settings

# 定義技能模型
class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 技能名稱，必須唯一
    tags = models.ManyToManyField('Tag', blank=True, related_name='skills')  # 與標籤的多對多關係
    
    def __str__(self):
        return self.name  # 返回技能名稱作為字符串表示

# 定義標籤模型
class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)  # 標籤名稱，必須唯一

    def __str__(self):
        return self.name  # 返回標籤名稱作為字符串表示

# 定義用戶資料模型
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 與內建 User 模型一對一關聯
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')  # 頭像圖片
    instagram = models.CharField(max_length=100, blank=True, null=True)  # Instagram 帳號
    city = models.CharField(max_length=100, blank=True, null=True)  # 居住城市
    want_to_learn = models.ManyToManyField(Skill, related_name='learners')  # 想學習的技能（多對多關係）
    can_teach = models.ManyToManyField(Skill, related_name='teachers')  # 能教授的技能（多對多關係）
    personality = models.ManyToManyField(Tag, blank=True)  # 個性標籤（多對多關係）
    available_time = models.TextField(blank=True, null=True)  # 可用時間（自由文本）
    self_intro = models.TextField(blank=True, null=True)  # 自我介紹（自由文本）

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
        return self.user.username  # 返回用戶名作為字符串表示