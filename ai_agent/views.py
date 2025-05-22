from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
import json
from .agent import AIAgent

# 創建一個全局的 AIAgent 實例
ai_agent = AIAgent()

@login_required
def chat_page(request):
    return render(request, 'ai_agent/chat.html')

@csrf_exempt
@require_http_methods(["POST"])
def chat(request):
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')

        if not user_message:
            return JsonResponse({'error': '訊息不能為空'}, status=400)

        response = ai_agent.get_response(user_message)
        return JsonResponse({'response': response})

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
