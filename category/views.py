from django.shortcuts import render
from category.models import Mentor

# Create your views here.
def category(request):
    mentors = Mentor.objects.all()
    return render(request, 'category/Category.html', {'mentors': mentors})