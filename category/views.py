from django.shortcuts import render
from django.db.models import Q
from myprofile.models import UserProfile, Skill, SkillCategory, PersonalityTag, ClassType

# Create your views here.
def category(request):
    # 獲取所有有教學技能的用戶
    mentors = UserProfile.objects.filter(can_teach__isnull=False).distinct()
    
    # 獲取過濾參數
    category_filter = request.GET.get('category', '')
    personality_filter = request.GET.get('personality', '')
    mode_filter = request.GET.get('mode', '')
    search_query = request.GET.get('search', '')
    
    # 應用過濾器
    if category_filter:
        mentors = mentors.filter(can_teach__category__name=category_filter)
    
    if personality_filter:
        mentors = mentors.filter(personality__name=personality_filter)
    
    if mode_filter:
        mentors = mentors.filter(class_type__name=mode_filter)
    
    # 應用搜尋
    if search_query:
        mentors = mentors.filter(
            Q(user__username__icontains=search_query) |
            Q(city__icontains=search_query) |
            Q(can_teach__name__icontains=search_query)
        ).distinct()
    
    # 獲取所有分類和個性標籤用於過濾下拉選單
    categories = SkillCategory.objects.all()
    personality_tags = PersonalityTag.objects.all()
    class_types = ClassType.objects.all()
    
    context = {
        'mentors': mentors,
        'categories': categories,
        'personality_tags': personality_tags,
        'class_types': class_types,
        'current_category': category_filter,
        'current_personality': personality_filter,
        'current_mode': mode_filter,
        'search_query': search_query,
    }
    return render(request, 'category/Category.html', context)
