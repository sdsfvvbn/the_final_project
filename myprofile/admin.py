from django.contrib import admin
from .models import UserProfile, SkillCategory, Skill, PersonalityTag, ClassType
from django.utils.html import format_html

# ============================================
# UserProfile 模型的後台管理設定
# ============================================
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # 在 admin 列表中顯示的欄位
    list_display = ('user', 'avatar_tag', 'instagram', 'city', 'get_teaching_skills', 'get_personality', 'get_class_type')

    # 提供搜尋功能，支援模糊查詢 username、IG、城市
    search_fields = ('user__username', 'instagram', 'city', 'can_teach__name')

    # 支援直欄式多選介面（適用 ManyToMany 欄位）
    filter_horizontal = ('want_to_learn', 'can_teach', 'personality', 'class_type')

    # 可過濾的欄位
    list_filter = ('city', 'can_teach__category', 'personality', 'class_type')

    def get_teaching_skills(self, obj):
        return ", ".join([skill.name for skill in obj.can_teach.all()])
    get_teaching_skills.short_description = '教學技能'

    def get_personality(self, obj):
        return ", ".join([tag.name for tag in obj.personality.all()])
    get_personality.short_description = '個性標籤'

    def get_class_type(self, obj):
        return ", ".join([type.name for type in obj.class_type.all()])
    get_class_type.short_description = '上課方式'

    def avatar_tag(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="width:40px;height:40px;border-radius:50%;object-fit:cover;" />', obj.avatar.url)
        return "-"
    avatar_tag.short_description = 'Avatar'

# ============================================
# SkillCategory 模型的後台管理設定
# ============================================
@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    # 僅顯示名稱欄位，無需分類欄位（因為你的 model 中沒有 category）
    list_display = ('name',)

    # 提供分類搜尋欄（模糊搜尋名稱）
    search_fields = ('name',)

# ============================================
# Skill 模型的後台管理設定
# ============================================
@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    # 顯示技能名稱與所屬分類（ForeignKey）
    list_display = ('name', 'category')

    # 可用分類篩選技能（右側 filter）
    list_filter = ('category',)

    # 提供技能名稱模糊搜尋
    search_fields = ('name',)

# ============================================
# PersonalityTag 模型的後台管理設定
# ============================================
@admin.register(PersonalityTag)
class PersonalityTagAdmin(admin.ModelAdmin):
    # 僅顯示標籤名稱
    list_display = ('name',)

    # 可搜尋個性標籤名稱（模糊）
    search_fields = ('name',)

# ============================================
# ClassType 模型的後台管理設定
# ============================================
@admin.register(ClassType)
class ClassTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)