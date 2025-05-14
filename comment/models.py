from django.conf import settings
from django.db import models

# Create your models here.

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