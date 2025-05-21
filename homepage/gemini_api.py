import google.generativeai as genai
from django.conf import settings

# 配置 Gemini API
def configure_genai():
    genai.configure(api_key=settings.GEMINI_API_KEY)

# 初始化聊天模型
def get_chat_model():
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[])
    return chat

# 獲取 AI 回應
def get_ai_response(message):
    try:
        chat = get_chat_model()
        response = chat.send_message(message)
        return response.text
    except Exception as e:
        return f"抱歉，發生了一些錯誤：{str(e)}"