from django.contrib import admin
from myprofile.models import UserProfile

# 我們不需要註冊任何模型，因為我們直接使用 UserProfile
# UserProfile 已經在 myprofile/admin.py 中註冊了

@admin.register(UserProfile)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'get_teaching_skills', 'get_personality', 'get_class_type')
    list_filter = ('city', 'can_teach__category', 'personality', 'class_type')
    search_fields = ('user__username', 'city', 'can_teach__name')
    filter_horizontal = ('can_teach', 'personality', 'class_type')
    
    def get_teaching_skills(self, obj):
        return ", ".join([skill.name for skill in obj.can_teach.all()])
    get_teaching_skills.short_description = '教學技能'
    
    def get_personality(self, obj):
        return ", ".join([tag.name for tag in obj.personality.all()])
    get_personality.short_description = '個性標籤'
    
    def get_class_type(self, obj):
        return ", ".join([type.name for type in obj.class_type.all()])
    get_class_type.short_description = '上課方式'
    
    class Meta:
        verbose_name = '導師資料'
        verbose_name_plural = '導師資料'
