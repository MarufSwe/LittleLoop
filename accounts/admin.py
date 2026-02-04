from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for UserProfile model.
    """
    list_display = ['user', 'full_name', 'phone_number', 'location', 'is_complete', 'created_at']
    list_filter = ['is_complete', 'created_at']
    search_fields = ['user__email', 'full_name', 'phone_number', 'location']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('User Information', {
            'fields': ('user', 'full_name', 'phone_number', 'location')
        }),
        ('About', {
            'fields': ('bio',)
        }),
        ('Status', {
            'fields': ('is_complete',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
