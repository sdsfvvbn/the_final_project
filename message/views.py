from django.shortcuts import render, redirect
from .models import Message
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone
from django.db.models import F
#用render 回傳 (request對象 / 模板路徑 / (字典 要傳給模板東西))
User = get_user_model()
@login_required

def message_page(request, username = None):
    # 如果沒有提供 username，則重定向到主頁或其他頁面
    # request.user = User.objects.get(username="alan")
    
    # 如果沒有提供 username，則不設置 other_user
    other_user = None
    messages = []
    
    if username:
        other_user = User.objects.get(username=username)
        # 找出跟這個人的所有訊息，按時間升序排序，並確保精確排序
        messages = Message.objects.filter(
            sender__in=[request.user, other_user],
            receiver__in=[request.user, other_user]
        ).order_by('created_at', 'id')  # 添加 id 作為次要排序條件

        # 打印消息順序用於調試
        for msg in messages:
            print(f"Message: {msg.text}, Time: {msg.created_at}, Sender: {msg.sender.username}, ID: {msg.id}")

        # 將所有未讀消息標記為已讀
        Message.objects.filter(
            sender=other_user,
            receiver=request.user,
            is_read=False
        ).update(is_read=True)
    
    # 找出所有聊天過的人（左邊列表用）
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
