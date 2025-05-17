from django.urls import path
from . import views

app_name = 'comment'
urlpatterns = [
    path('submit-review/', views.SubmitReviewView.as_view(), name='submit_review'),
    path('get-users-to-review/', views.GetUsersToReviewView.as_view(), name='get_users_to_review'),
]