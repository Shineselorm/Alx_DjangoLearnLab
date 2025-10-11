"""
Views for Notifications functionality.
Implements notification retrieval and management.
"""

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Notification
from .serializers import NotificationSerializer, NotificationListSerializer


class NotificationListView(generics.ListAPIView):
    """
    API endpoint for viewing user notifications.
    
    GET /api/notifications/
    Headers: Authorization: Token <token>
    Query params:
    - read: Filter by read status (true/false)
    
    Returns: List of notifications for the authenticated user
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return notifications for the authenticated user."""
        queryset = Notification.objects.filter(
            recipient=self.request.user
        ).select_related('actor', 'target_content_type').order_by('-timestamp')
        
        # Filter by read status if provided
        read_param = self.request.query_params.get('read', None)
        if read_param is not None:
            if read_param.lower() == 'true':
                queryset = queryset.filter(read=True)
            elif read_param.lower() == 'false':
                queryset = queryset.filter(read=False)
        
        return queryset
    
    def list(self, request, *args, **kwargs):
        """Override list to add unread count."""
        queryset = self.filter_queryset(self.get_queryset())
        unread_count = queryset.filter(read=False).count()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['unread_count'] = unread_count
            return response
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'unread_count': unread_count,
            'results': serializer.data
        })


class UnreadNotificationListView(generics.ListAPIView):
    """
    API endpoint for viewing unread notifications only.
    
    GET /api/notifications/unread/
    Headers: Authorization: Token <token>
    
    Returns: List of unread notifications
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return only unread notifications."""
        return Notification.objects.filter(
            recipient=self.request.user,
            read=False
        ).select_related('actor', 'target_content_type').order_by('-timestamp')


class MarkNotificationReadView(APIView):
    """
    API endpoint for marking a notification as read.
    
    POST /api/notifications/<pk>/read/
    Headers: Authorization: Token <token>
    
    Returns: Updated notification
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        """Mark notification as read."""
        notification = get_object_or_404(
            Notification,
            pk=pk,
            recipient=request.user
        )
        
        notification.mark_as_read()
        
        serializer = NotificationSerializer(notification)
        return Response({
            'message': 'Notification marked as read',
            'notification': serializer.data
        }, status=status.HTTP_200_OK)


class MarkAllNotificationsReadView(APIView):
    """
    API endpoint for marking all notifications as read.
    
    POST /api/notifications/mark-all-read/
    Headers: Authorization: Token <token>
    
    Returns: Success message
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Mark all user notifications as read."""
        updated_count = Notification.objects.filter(
            recipient=request.user,
            read=False
        ).update(read=True)
        
        return Response({
            'message': f'{updated_count} notifications marked as read',
            'updated_count': updated_count
        }, status=status.HTTP_200_OK)


class DeleteNotificationView(APIView):
    """
    API endpoint for deleting a notification.
    
    DELETE /api/notifications/<pk>/
    Headers: Authorization: Token <token>
    
    Returns: Success message
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def delete(self, request, pk):
        """Delete a notification."""
        notification = get_object_or_404(
            Notification,
            pk=pk,
            recipient=request.user
        )
        
        notification.delete()
        
        return Response({
            'message': 'Notification deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)

