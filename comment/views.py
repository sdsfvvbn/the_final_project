from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Review

User = get_user_model()

class SubmitReviewView(LoginRequiredMixin, View):
    def post(self, request):
        rated_user_id = request.POST.get('rated_user')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        try:
            rated_user = User.objects.get(id=rated_user_id)
            review, created = Review.objects.get_or_create(
                reviewer=request.user,
                rated_user=rated_user,
                defaults={
                    'rating': rating,
                    'comment': comment,
                    'is_completed': True
                }
            )
            if not created:
                # 更新已存在的評價
                review.rating = rating
                review.comment = comment
                review.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

class GetUsersToReviewView(LoginRequiredMixin, View):
    def get(self, request):
        # 取得可以評價的用戶（排除自己和已評價過的）
        reviewed_users = Review.objects.filter(reviewer=request.user).values_list('rated_user_id', flat=True)
        users_to_review = User.objects.exclude(id=request.user.id).exclude(id__in=reviewed_users)
        
        users_data = [{'id': user.id, 'username': user.username} for user in users_to_review]
        return JsonResponse({'users': users_data})