from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_profile, name='create_profile'),  # 定義 create_profile 路由
    path('', views.profile_view, name='profile_view'),  # 定義 profile_view 路由
]