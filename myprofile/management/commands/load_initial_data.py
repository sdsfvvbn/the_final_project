from django.core.management.base import BaseCommand
from myprofile.models import SkillCategory, Skill, PersonalityTag, ClassType

class Command(BaseCommand):
    help = 'Load initial data for the application'

    def handle(self, *args, **kwargs):
        # 創建技能類別
        categories = [
            'Language',
            'Music',
            'Art',
            'Sports',
            'Cooking'
        ]

        for category_name in categories:
            SkillCategory.objects.get_or_create(name=category_name)
            self.stdout.write(f'Created category: {category_name}')

        # 創建技能
        skills_data = {
            'Language': ['English', 'Chinese', 'Japanese', 'Korean', 'Spanish', 'French'],
            'Music': ['Piano', 'Guitar', 'Violin', 'Singing', 'Drum', 'Bass'],
            'Art': ['Drawing', 'Painting', 'Digital Art', 'Calligraphy', 'Photography'],
            'Sports': ['Basketball', 'Swimming', 'Tennis', 'Yoga', 'Dancing'],
            'Cooking': ['Baking', 'Chinese Cuisine', 'Italian Cuisine', 'Japanese Cuisine', 'Pastry']
        }

        for category_name, skills in skills_data.items():
            category = SkillCategory.objects.get(name=category_name)
            for skill_name in skills:
                Skill.objects.get_or_create(name=skill_name, category=category)
                self.stdout.write(f'Created skill: {skill_name} in {category_name}')

        # 創建個性標籤
        personality_tags = [
            'Creative', 'Organized', 'Calm', 'Patient', 'Thoughtful',
            'Extrovert', 'Cheerful', 'Serious', 'Funny', 'Knowledgeable',
            'Goal-Oriented', 'Good Communicator', 'Supportive', 'Inspiring', 'Friendly'
        ]

        for tag_name in personality_tags:
            PersonalityTag.objects.get_or_create(name=tag_name)
            self.stdout.write(f'Created personality tag: {tag_name}')

        # 創建課程類型
        class_types = ['Online', 'Physical']

        for type_name in class_types:
            ClassType.objects.get_or_create(name=type_name)
            self.stdout.write(f'Created class type: {type_name}')

        self.stdout.write(self.style.SUCCESS('Successfully loaded initial data'))