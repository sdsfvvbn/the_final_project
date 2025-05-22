from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer', 'rated_user', 'rating', 'comment', 'created_at', 'is_completed')
    list_filter = ('rating', 'created_at', 'is_completed')
    search_fields = ('reviewer__username', 'rated_user__username', 'comment')
    date_hierarchy = 'created_at'
    raw_id_fields = ('reviewer', 'rated_user')