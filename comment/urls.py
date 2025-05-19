from django.urls import path
from . import views

app_name = 'comment'
urlpatterns = [
    path('submit-review/', views.SubmitReviewView.as_view(), name='submit_review'),
    path('get-users-to-review/', views.GetUsersToReviewView.as_view(), name='get_users_to_review'),
    path('get-reviews/', views.GetReviewsView.as_view(), name='get_reviews'),
    path('update-review/', views.UpdateReviewView.as_view(), name='update_review'),
    path('delete-review/', views.DeleteReviewView.as_view(), name='delete_review'),
]