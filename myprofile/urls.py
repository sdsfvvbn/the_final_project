from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', views.create_profile, name='create_profile'),  # 建立個人資料
    path('edit/', views.edit_profile, name='edit_profile'),        # 編輯個人資料
    path('', views.profile_view, name='profile_view'),             # 個人資料主頁
    path('update-avatar/', views.update_avatar, name='update_avatar'),
]