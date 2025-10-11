"""
Custom User Model for Social Media API
Extends Django's AbstractUser to include additional fields for social media functionality.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom User model extending AbstractUser with social media specific fields.
    
    Additional Fields:
    - bio: User's biography/description
    - profile_picture: User's profile image
    - followers: ManyToMany relationship for follower system
    """
    
    # Additional fields for social media functionality
    bio = models.TextField(
        _('biography'),
        max_length=500,
        blank=True,
        help_text=_('Write a brief description about yourself')
    )
    
    profile_picture = models.ImageField(
        _('profile picture'),
        upload_to='profile_pictures/',
        blank=True,
        null=True,
        help_text=_('Upload your profile picture')
    )
    
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
        help_text=_('Users who follow this user')
    )
    
    # Additional metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
    
    def __str__(self):
        """String representation of the user."""
        return self.username
    
    def get_full_name(self):
        """Return the user's full name."""
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.username
    
    def get_follower_count(self):
        """Return the count of followers."""
        return self.followers.count()
    
    def get_following_count(self):
        """Return the count of users this user is following."""
        return self.following.count()
    
    def follow(self, user):
        """Follow another user."""
        if user != self:
            user.followers.add(self)
    
    def unfollow(self, user):
        """Unfollow another user."""
        user.followers.remove(self)
    
    def is_following(self, user):
        """Check if this user is following another user."""
        return user.followers.filter(pk=self.pk).exists()
    
    def is_followed_by(self, user):
        """Check if this user is followed by another user."""
        return self.followers.filter(pk=user.pk).exists()


