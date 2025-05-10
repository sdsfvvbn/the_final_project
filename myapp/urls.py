from django.urls import path
from myapp import views
from django.contrib.auth import views as auth_views
app_name = 'myapp'
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('delete-account/', views.delete_account, name='delete_account'),
    # path(r'^admin/', admin.site.urls),
    # path(r'^$', sayhello),
]