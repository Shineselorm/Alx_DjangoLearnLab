"""
Models for Notifications functionality.
Defines the database structure for user notifications and activity tracking.
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class Notification(models.Model):
    """
    Model representing a notification for user activities.
    
    Fields:
    - recipient: User who receives the notification
    - actor: User who triggered the notification
    - verb: Description of the action (e.g., 'liked your post', 'followed you')
    - target_content_type: ContentType of the target object
    - target_object_id: ID of the target object
    - target: GenericForeignKey to any model instance
    - timestamp: When the notification was created
    - read: Whether the notification has been read
    
    Examples:
    - "John liked your post 'Hello World'"
    - "Jane started following you"
    - "Bob commented on your post"
    """
    
    recipient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text=_('User who receives this notification')
    )
    
    actor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='sent_notifications',
        help_text=_('User who triggered this notification')
    )
    
    verb = models.CharField(
        _('verb'),
        max_length=255,
        help_text=_('Description of the action (e.g., "liked your post")')
    )
    
    # GenericForeignKey to any model
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text=_('Content type of the target object')
    )
    
    target_object_id = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text=_('ID of the target object')
    )
    
    target = GenericForeignKey('target_content_type', 'target_object_id')
    
    timestamp = models.DateTimeField(
        _('timestamp'),
        auto_now_add=True,
        help_text=_('When the notification was created')
    )
    
    read = models.BooleanField(
        _('read'),
        default=False,
        help_text=_('Whether the notification has been read')
    )
    
    class Meta:
        verbose_name = _('notification')
        verbose_name_plural = _('notifications')
        ordering = ['-timestamp']  # Most recent first
        indexes = [
            models.Index(fields=['recipient', '-timestamp']),
            models.Index(fields=['recipient', 'read']),
        ]
    
    def __str__(self):
        """String representation of the notification."""
        return f"{self.actor.username} {self.verb} - {self.recipient.username}"
    
    def mark_as_read(self):
        """Mark this notification as read."""
        if not self.read:
            self.read = True
            self.save(update_fields=['read'])
    
    def mark_as_unread(self):
        """Mark this notification as unread."""
        if self.read:
            self.read = False
            self.save(update_fields=['read'])

