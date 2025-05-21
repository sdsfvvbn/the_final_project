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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', homepage_views.home, name='homepage'),  # 首頁
    path('admin/', admin.site.urls),
    path('message/', include('message.urls', namespace='message')),
    path('myapp/', include('myapp.urls', namespace='myapp')),
    path('profile/', include('myprofile.urls')),      # 包含 myprofile 的所有路由（包含 update_avatar）
    path('comment/', include('comment.urls')),
    path('category/', category_views.category, name='category'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)