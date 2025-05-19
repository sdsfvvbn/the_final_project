from django.db import models
from django.conf import settings
from myprofile.models import UserProfile, Skill, PersonalityTag

# Create your models here.
class Mentor(models.Model):
    user_profile = models.OneToOneField(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='mentor_profile'
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    mode = models.CharField(max_length=50, default='Online')  # 'Online' or 'Physical'
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.user_profile.user.username

    @property
    def name(self):
        return self.user_profile.user.username

    @property
    def avatar(self):
        return self.user_profile.avatar

    @property
    def title(self):
        return ", ".join([skill.name for skill in self.user_profile.can_teach.all()])

    @property
    def location(self):
        return self.user_profile.city or "Not specified"

    @property
    def personality(self):
        return self.user_profile.personality.all()

    @property
    def skills(self):
        return self.user_profile.can_teach.all()