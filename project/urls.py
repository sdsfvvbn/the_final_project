"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from homepage import views as homepage_views
from category import views as category_views
from django.urls import path
from django.urls import include

import message
from homepage import views
urlpatterns = [
    path('', homepage_views.home, name='homepage'),
    path('admin/', admin.site.urls),
    path('message/', include('message.urls', namespace='message')),
    path('myapp/', include('myapp.urls', namespace='myapp')),
    path('', views.home, name='homepage'),
    path('profile/', include('myprofile.urls')),
    path('comment/', include('comment.urls')),
    path('', homepage_views.home, name='homepage'),
    path('category/', category_views.category, name='category')
]
