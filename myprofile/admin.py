from django.contrib import admin
from .models import UserProfile, SkillCategory, Skill, PersonalityTag

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'instagram', 'city')

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category',)
    search_fields = ('name',)

@admin.register(PersonalityTag)
class PersonalityTagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)