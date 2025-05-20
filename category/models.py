from django.db import models
from myprofile.models import UserProfile

# 我們不需要額外的模型，直接使用 UserProfile
# 因為 UserProfile 已經包含了所有我們需要的資訊：
# - can_teach (技能)
# - personality (個性標籤)
# - class_type (上課方式)
# - city (地點)
# - avatar (頭像)
# - self_intro (自我介紹)