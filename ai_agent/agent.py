import google.generativeai as genai
from django.conf import settings
from .config import SYSTEM_PROMPT

class AIAgent:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.chat = self.model.start_chat(history=[])
        # 發送系統提示
        self.chat.send_message(SYSTEM_PROMPT)

    def get_response(self, user_input):
        try:
            response = self.chat.send_message(user_input)
            return response.text
        except Exception as e:
            return f"抱歉，發生錯誤：{str(e)}"

    def reset_chat(self):
        self.chat = self.model.start_chat(history=[])
        # 重新發送系統提示
        self.chat.send_message(SYSTEM_PROMPT)