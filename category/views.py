from django.shortcuts import render
from .models import Mentor
from myprofile.models import Skill, SkillCategory, PersonalityTag, ClassType

# Create your views here.
def category(request):
    # Get all mentors initially
    mentors = Mentor.objects.all()
    
    # Get filter parameters from request
    category_filter = request.GET.get('category', 'all')
    personality_filter = request.GET.get('personality', 'all')
    mode_filter = request.GET.get('willingness', 'all')
    
    # Apply filters
    if category_filter != 'all':
        # Filter by skill category
        mentors = mentors.filter(user_profile__can_teach__category__name=category_filter)
    
    if personality_filter != 'all':
        # Filter by personality tag
        mentors = mentors.filter(user_profile__personality__name=personality_filter)
    
    if mode_filter != 'all':
        # Filter by class type
        mentors = mentors.filter(user_profile__class_type__name=mode_filter)
    
    # Get all categories and personality tags for the filter dropdowns
    categories = SkillCategory.objects.all()
    personality_tags = PersonalityTag.objects.all()
    class_types = ClassType.objects.all()
    
    context = {
        'mentors': mentors,
        'categories': categories,
        'personality_tags': personality_tags,
        'class_types': class_types,
    }
    return render(request, 'category/Category.html', context)