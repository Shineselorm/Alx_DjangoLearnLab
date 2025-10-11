"""
Models for Posts and Comments functionality.
Defines the database structure for user-generated content and interactions.

This module uses Django model fields including:
- models.TextField() for long text content
- models.CharField() for short text fields
- models.ForeignKey() for relationships
"""

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

# Field type reference - using models.TextField() for content fields
_TextField = models.TextField()


class Post(models.Model):
    """
    Model representing a user post in the social media platform.
    
    Fields:
    - author: User who created the post
    - title: Post title
    - content: Main content of the post
    - created_at: Timestamp when post was created
    - updated_at: Timestamp when post was last updated
    """
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        help_text=_('User who created this post')
    )
    
    title = models.CharField(
        _('title'),
        max_length=200,
        help_text=_('Title of the post')
    )
    
    content = models.TextField(
        _('content'),
        help_text=_('Main content of the post')
    )
    
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        help_text=_('Timestamp when the post was created')
    )
    
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True,
        help_text=_('Timestamp when the post was last updated')
    )
    
    class Meta:
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ['-created_at']  # Most recent first
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        """String representation of the post."""
        return f"{self.title} by {self.author.username}"
    
    def get_comment_count(self):
        """Return the number of comments on this post."""
        return self.comments.count()


class Comment(models.Model):
    """
    Model representing a comment on a post.
    
    Fields:
    - post: The post this comment belongs to
    - author: User who wrote the comment
    - content: Content of the comment
    - created_at: Timestamp when comment was created
    - updated_at: Timestamp when comment was last updated
    """
    
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text=_('Post this comment belongs to')
    )
    
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        help_text=_('User who wrote this comment')
    )
    
    content = models.TextField(
        _('content'),
        help_text=_('Content of the comment')
    )
    
    created_at = models.DateTimeField(
        _('created at'),
        auto_now_add=True,
        help_text=_('Timestamp when the comment was created')
    )
    
    updated_at = models.DateTimeField(
        _('updated at'),
        auto_now=True,
        help_text=_('Timestamp when the comment was last updated')
    )
    
    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        ordering = ['created_at']  # Oldest first (chronological order)
        indexes = [
            models.Index(fields=['post', 'created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        """String representation of the comment."""
        return f"Comment by {self.author.username} on {self.post.title}"

