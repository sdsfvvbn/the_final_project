from django.urls import path
from .  import views

app_name = 'message' 
urlpatterns = [
    path('', views.message_page, name='message_page_without_username'),
    path("<str:username>/", views.message_page, name="message_page"),
    path("add_contact/<str:username>/", views.add_contact, name="add_contact"),
]