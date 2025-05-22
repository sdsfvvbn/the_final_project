from django.http import JsonResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from .models import Review
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator

User = get_user_model()

class SubmitReviewView(LoginRequiredMixin, View):
    def post(self, request):
        review_id = request.POST.get('review_id')  # 檢查是否是編輯模式
        rated_user_id = request.POST.get('rated_user')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')

        # 如果是編輯模式，使用 UpdateReviewView 的邏輯
        if review_id:
            try:
                review = Review.objects.get(id=review_id, reviewer=request.user)
                review.rating = rating
                review.comment = comment
                review.save()
                return JsonResponse({'success': True})
            except Review.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Review not found'})
            except Exception as e:
                return JsonResponse({'success': False, 'message': str(e)})

        # 如果是新增評價，使用原有的邏輯
        if not rated_user_id:
            return JsonResponse({'success': False, 'message': 'Please select a user to review'})

        try:
            rated_user = User.objects.get(id=rated_user_id)
            if rated_user == request.user:
                return JsonResponse({'success': False, 'message': 'You cannot review yourself'})

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
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Selected user does not exist'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

class GetUsersToReviewView(LoginRequiredMixin, View):
    def get(self, request):
        # 取得可以評價的用戶（排除自己和已評價過的）
        reviewed_users = Review.objects.filter(reviewer=request.user).values_list('rated_user_id', flat=True)
        users_to_review = User.objects.exclude(id=request.user.id).exclude(id__in=reviewed_users)

        users_data = [{'id': user.id, 'username': user.username} for user in users_to_review]
        return JsonResponse({'users': users_data})

class GetReviewsView(LoginRequiredMixin, View):
    def get(self, request):
        # 新增：允許用 ?username=xxx 查詢特定用戶的評論
        username = request.GET.get('username')
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)
        else:
            user = request.user

        # 查詢該用戶收到的評論
        received_reviews = Review.objects.filter(rated_user=user)
        received_data = []
        for review in received_reviews:
            # 取得 reviewer 的頭像
            avatar_url = review.reviewer.userprofile.avatar.url if hasattr(review.reviewer, 'userprofile') and review.reviewer.userprofile.avatar else '/media/avatars/default.png'
            received_data.append({
                'id': review.id,
                'reviewer': review.reviewer.username,
                'reviewer_avatar': avatar_url,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        # 查詢該用戶發出的評論（可選）
        given_reviews = Review.objects.filter(reviewer=user)
        given_data = []
        for review in given_reviews:
            given_data.append({
                'id': review.id,
                'rated_user': review.rated_user.username,
                'rated_user_id': review.rated_user.id,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        return JsonResponse({
            'received_reviews': received_data,
            'given_reviews': given_data
        })

@method_decorator(require_http_methods(["POST"]), name='dispatch')
class UpdateReviewView(LoginRequiredMixin, View):
    def post(self, request):
        review_id = request.POST.get('review_id')
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')

        try:
            review = Review.objects.get(id=review_id, reviewer=request.user)
            review.rating = rating
            review.comment = comment
            review.save()
            return JsonResponse({'success': True})
        except Review.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Review not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

@method_decorator(require_http_methods(["POST"]), name='dispatch')
class DeleteReviewView(LoginRequiredMixin, View):
    def post(self, request):
        review_id = request.POST.get('review_id')

        try:
            review = Review.objects.get(id=review_id, reviewer=request.user)
            review.delete()
            return JsonResponse({'success': True})
        except Review.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Review not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})