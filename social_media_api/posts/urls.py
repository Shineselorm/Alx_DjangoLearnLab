"""
URL Configuration for posts app.
Defines routing for posts and comments endpoints using DRF routers.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

app_name = 'posts'

urlpatterns = [
    # Feed endpoint - shows posts from followed users
    path('feed/', FeedView.as_view(), name='feed'),
    
    # Include all routes from the router
    path('', include(router.urls)),
]

