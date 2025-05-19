from django.shortcuts import render, redirect
from .models import Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils import timezone
from django.db.models import F
#用render 回傳 (request對象 / 模板路徑 / (字典 要傳給模板東西))
User = get_user_model()

@login_required  # Add this decorator to ensure only authenticated users can access
def message_page(request, username = None):
    # Remove the hardcoded user assignment
    # request.user = User.objects.get(username="alan")  # Remove this line
    
    # If no username provided, just show the chat interface without a specific conversation
    other_user = None
    messages = []
    
    if username:
        try:
            other_user = User.objects.get(username=username)
            # Find all messages between these users
            messages = Message.objects.filter(
                sender__in=[request.user, other_user],
                receiver__in=[request.user, other_user]
            ).order_by('created_at', 'id')

            # Mark unread messages as read
            Message.objects.filter(
                sender=other_user,
                receiver=request.user,
                is_read=False
            ).update(is_read=True)
        except User.DoesNotExist:
            # Handle case where username doesn't exist
            return redirect('message:message_page_without_username')
    
    # Find all users who have chatted with the current user
    contacted_users = User.objects.filter(
        id__in=Message.objects.filter(
            sender=request.user
        ).values_list('receiver_id', flat=True)
    ).union(
        User.objects.filter(
            id__in=Message.objects.filter(
                receiver=request.user
            ).values_list('sender_id', flat=True)
        )
    )    
    recent_contacts = []
    for contact in contacted_users:
        last_msg = Message.objects.filter(
            Q(sender=request.user, receiver=contact) |
            Q(sender=contact, receiver=request.user)
        ).order_by('-created_at').first()

        unread = Message.objects.filter(sender=contact, receiver=request.user, is_read=False).count()

        recent_contacts.append({
            'user': contact,
            'last_message': last_msg,
            'unread_count': unread
        })
    # CRUD(Create)
    # 如果是 POST 請求，則處理發送訊息
    if request.method == 'POST':
        text = request.POST.get('text')  # 取得用戶輸入的訊息
        if text:
            # 創建新的訊息
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text=text,
                is_read=False  # 設置為未讀
            )
            # 重定向回當前的聊天頁面，以顯示新訊息
            return redirect('message:message_page', username=other_user.username)


    return render(request, 'message/message_page.html', {
        'messages': messages,
        'other_user': other_user,
        'recent_contacts': recent_contacts,
        #unread / last_message 包在recent_contacts裡
        # 'unread_count': unread_count,
        #  'last_message': last_message,
    })

@login_required
def add_contact(request, username):
    try:
        other_user = User.objects.get(username=username)
        
        # 檢查是否已經有對話記錄
        existing_messages = Message.objects.filter(
            Q(sender=request.user, receiver=other_user) |
            Q(sender=other_user, receiver=request.user)
        ).exists()
        
        if not existing_messages:
            # 創建一個初始訊息
            Message.objects.create(
                sender=request.user,
                receiver=other_user,
                text="Hi! I'd like to connect with you.",
                is_read=False
            )
        
        # 重定向到聊天頁面
        return redirect('message:message_page', username=username)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
