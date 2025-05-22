from django.shortcuts import render
from django.http import JsonResponse
from .gemini_api import get_ai_response, configure_genai

# Create your views here.
def home(request):
    return render(request, 'homepage/TalentSwap.html')

def agent(request):
    return render(request, 'homepage/Agent.html')

def chat_with_ai(request):
    if request.method == 'POST':
        message = request.POST.get('message', '')
        if message:
            # 配置 Gemini API
            configure_genai()
            # 獲取 AI 回應
            response = get_ai_response(message)
            return JsonResponse({'response': response})
    return JsonResponse({'error': '無效的請求'}, status=400)