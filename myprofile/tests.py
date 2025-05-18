from myprofile.models import Skill, Tag, UserProfile
from django.contrib.auth.models import User

# 創建技能
skill1 = Skill.objects.create(name="Public Speaking")
skill2 = Skill.objects.create(name="Python Programming")
skill3 = Skill.objects.create(name="Painting")

# 創建個性標籤
tag1 = Tag.objects.create(name="Patient")
tag2 = Tag.objects.create(name="Creative")
tag3 = Tag.objects.create(name="Calm")

# 創建使用者(學生)
user1 = User.objects.create(username="student1", first_name="Emma", last_name="Liu")
profile1 = UserProfile.objects.create(
    user=user1, 
    self_intro="I love learning new things!",
    instagram="@emmatalks",
    city="Tainan City, Taiwan"
)
profile1.want_to_learn.add(skill1, skill2)
profile1.can_teach.add(skill3)
profile1.personality.add(tag1,tag3)

#創建使用者(老師)
user2 = User.objects.create(username="teacher1", first_name="Kevin", last_name="Chen")
profile2 = UserProfile.objects.create(user=user2)
profile2.can_teach.add(skill1)

user3 = User.objects.create(username="teacher2", first_name="Irene", last_name="Lin")
profile3 = UserProfile.objects.create(user=user3)
profile3.can_teach.add(skill2, skill3)