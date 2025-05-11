from myprofile.models import Skill, Tag, UserProfile
from django.contrib.auth.models import User

# 創建技能
skill1 = Skill.objects.create(name="Public Speaking")
skill2 = Skill.objects.create(name="Python Programming")
skill3 = Skill.objects.create(name="Painting")

# 創建個性標籤
tag1 = Tag.objects.create(name="Patient")
tag2 = Tag.objects.create(name="Creative")

# 創建使用者
user1 = User.objects.create(username="student1", first_name="Emma", last_name="Liu")
profile1 = UserProfile.objects.create(user=user1, self_intro="I love learning new things!")
profile1.want_to_learn.add(skill1, skill2)
profile1.personality.add(tag1)

user2 = User.objects.create(username="teacher1", first_name="Kevin", last_name="Chen")
profile2 = UserProfile.objects.create(user=user2, self_intro="I enjoy teaching public speaking.")
profile2.can_teach.add(skill1)
profile2.personality.add(tag2)

user3 = User.objects.create(username="teacher2", first_name="Irene", last_name="Lin")
profile3 = UserProfile.objects.create(user=user3, self_intro="Python is my passion!")
profile3.can_teach.add(skill2, skill3)
profile3.personality.add(tag1, tag2)