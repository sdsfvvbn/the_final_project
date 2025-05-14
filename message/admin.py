from django.contrib import admin
from message.models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'text', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'text')
    date_hierarchy = 'created_at'