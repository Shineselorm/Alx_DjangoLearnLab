"""
Admin configuration for notifications app.
"""

from django.contrib import admin
from .models import Notification


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """Admin interface for Notification model."""
    list_display = ['id', 'recipient', 'actor', 'verb', 'read', 'timestamp']
    list_filter = ['read', 'timestamp']
    search_fields = ['recipient__username', 'actor__username', 'verb']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    
    fieldsets = (
        ('Notification Info', {
            'fields': ('recipient', 'actor', 'verb')
        }),
        ('Target', {
            'fields': ('target_content_type', 'target_object_id')
        }),
        ('Status', {
            'fields': ('read', 'timestamp')
        }),
    )

