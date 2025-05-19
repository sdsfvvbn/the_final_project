from django.shortcuts import render
from django.db.models import Q
from .models import Mentor
from myprofile.models import Skill, SkillCategory, PersonalityTag, ClassType

# Create your views here.
def category(request):
    # Start with all available mentors
    mentors = Mentor.objects.filter(is_available=True)
    
    # Get filter parameters from request
    category_filter = request.GET.get('category', '')
    personality_filter = request.GET.get('personality', '')
    mode_filter = request.GET.get('mode', '')
    search_query = request.GET.get('search', '')
    
    # Apply filters only if they are provided
    # If no filter is provided, all available mentors will be shown
    if category_filter:
        # Filter by skill category
        mentors = mentors.filter(user_profile__can_teach__category__name=category_filter)
    
    if personality_filter:
        # Filter by personality tag
        mentors = mentors.filter(user_profile__personality__name=personality_filter)
    
    if mode_filter:
        # Filter by teaching mode (Online/Physical)
        mentors = mentors.filter(mode=mode_filter)
    
    # Apply search if provided
    if search_query:
        mentors = mentors.filter(
            Q(user_profile__user__username__icontains=search_query) |
            Q(user_profile__city__icontains=search_query) |
            Q(user_profile__can_teach__name__icontains=search_query)
        ).distinct()
    
    # Get all categories and personality tags for the filter dropdowns
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
