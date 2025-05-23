from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('myapp/', include('myapp.urls')),
    path('ai_agent/', include('ai_agent.urls')),
]