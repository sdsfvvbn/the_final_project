from django.db import models
from django.conf import settings
import uuid
import os

# ========================
# 技能分類模型（Skill 類別）
# ========================
class SkillCategory(models.Model):
    name = models.CharField(max_length=50)  # 分類名稱，例如 Language, Art

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"  # admin 中顯示複數名稱


# ========================
# 技能項目模型（具體技能）
# ========================
class Skill(models.Model):
    name = models.CharField(max_length=100)  # 技能名稱，例如 English, Baking
    category = models.ForeignKey(
        SkillCategory,
        on_delete=models.CASCADE,
        related_name='skills'  # 讓你可以用 category.skills.all() 反向查詢
    )

    def __str__(self):
        return f"{self.name} ({self.category.name})"


# ========================
# 個性標籤模型（可套用於用戶）
# ========================
class PersonalityTag(models.Model):
    name = models.CharField(max_length=50, unique=True)  # 標籤名稱，例如 patient、creative

    def __str__(self):
        return self.name

# ========================
# 上課型態模型（如實體、線上）
# ========================
class ClassType(models.Model):
    name = models.CharField(max_length=20, unique=True)  # 例如 Physical, Online

    def __str__(self):
        return self.name

def user_avatar_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join('avatars', filename)

# ========================
# 使用者個人資料擴充（UserProfile）
# ========================
class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )  # 與內建 User 模型一對一關聯

    avatar = models.ImageField(
        upload_to=user_avatar_path,
        default='avatars/default.png'
    )  # 上傳頭像圖片，預設圖也可用

    instagram = models.CharField(
        max_length=100,
        blank=True, null=True
    )  # IG 帳號，可留空

    city = models.CharField(
        max_length=100,
        blank=True, null=True
    )  # 居住城市，可留空

    # 想學習的技能（多對多）
    want_to_learn = models.ManyToManyField(
        Skill,
        related_name='interested_users',
        blank=True
    )

    # 可以教授的技能（多對多）
    can_teach = models.ManyToManyField(
        Skill,
        related_name='teaching_users',
        blank=True
    )

    # 個性標籤（多對多）
    personality = models.ManyToManyField(
        PersonalityTag,
        blank=True
    )

    # 上課型態欄位（可複選）
    class_type = models.ManyToManyField(
        ClassType,
        blank=True,
        help_text="可複選你偏好的上課型態"
    )

    # 可上課時間
    available_time = models.TextField(
        blank=True, null=True,
        help_text="請輸入你方便上課的時間，例如：Mon-Fri evenings, Sat morning"
    )

    # 自我介紹
    self_intro = models.TextField(
        blank=True, null=True,
        help_text="請簡單介紹你自己 :)"
    )

    def __str__(self):
        return self.user.username