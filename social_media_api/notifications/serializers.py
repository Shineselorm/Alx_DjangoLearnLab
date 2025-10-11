"""
Serializers for Notifications.
Handles data serialization and validation for notification API endpoints.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Notification

User = get_user_model()


class ActorSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying actor (user who triggered notification) information.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_picture']
        read_only_fields = fields


class NotificationSerializer(serializers.ModelSerializer):
    """
    Serializer for Notification model.
    Handles retrieval and display of notifications.
    """
    actor = ActorSerializer(read_only=True)
    target_type = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'recipient', 'actor', 'verb', 
            'target_type', 'target_object_id',
            'timestamp', 'read'
        ]
        read_only_fields = ['id', 'recipient', 'actor', 'timestamp']
    
    def get_target_type(self, obj):
        """Return the model name of the target object."""
        if obj.target_content_type:
            return obj.target_content_type.model
        return None


class NotificationListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing notifications.
    Used for list views to improve performance.
    """
    actor_username = serializers.CharField(source='actor.username', read_only=True)
    
    class Meta:
        model = Notification
        fields = [
            'id', 'actor_username', 'verb', 'timestamp', 'read'
        ]
        read_only_fields = fields

