"""
Admin configuration for accounts app.
Customizes the Django admin interface for user management.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """Custom admin configuration for CustomUser model."""
    
    list_display = [
        'username', 'email', 'first_name', 'last_name',
        'is_staff', 'is_active', 'date_joined', 'get_follower_count'
    ]
    
    list_filter = [
        'is_staff', 'is_superuser', 'is_active',
        'date_joined', 'groups'
    ]
    
    search_fields = ['username', 'email', 'first_name', 'last_name', 'bio']
    
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'bio', 'profile_picture')
        }),
        (_('Permissions'), {
            'fields': (
                'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            ),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Social'), {'fields': ('followers',)}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'email', 'password1', 'password2',
                'first_name', 'last_name', 'bio'
            ),
        }),
    )
    
    filter_horizontal = ['groups', 'user_permissions', 'followers']
    
    def get_follower_count(self, obj):
        """Display follower count in admin list."""
        return obj.get_follower_count()
    
    get_follower_count.short_description = 'Followers'

