"""
URL Configuration for notifications app.
Defines routing for notification endpoints.
"""

from django.urls import path
from .views import (
    NotificationListView,
    UnreadNotificationListView,
    MarkNotificationReadView,
    MarkAllNotificationsReadView,
    DeleteNotificationView
)

app_name = 'notifications'

urlpatterns = [
    # Notification list endpoints
    path('', NotificationListView.as_view(), name='notification-list'),
    path('unread/', UnreadNotificationListView.as_view(), name='unread-notifications'),
    
    # Mark as read endpoints
    path('<int:pk>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('mark-all-read/', MarkAllNotificationsReadView.as_view(), name='mark-all-read'),
    
    # Delete notification
    path('<int:pk>/', DeleteNotificationView.as_view(), name='delete-notification'),
]

