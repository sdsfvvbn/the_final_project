from django.contrib import admin
from .models import Mentor

@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = ('name', 'mode', 'location')
    list_filter = ('mode', )
    search_fields = ('user_profile__user__username', 'user_profile__city')
    readonly_fields = ('name', 'avatar', 'title', 'location', 'personality', 'skills')
