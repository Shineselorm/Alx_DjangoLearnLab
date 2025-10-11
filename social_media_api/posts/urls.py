"""
URL Configuration for posts app.
Defines routing for posts and comments endpoints using DRF routers.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PostViewSet, 
    CommentViewSet, 
    FeedView,
    LikePostView,
    UnlikePostView,
    PostLikesListView
)

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='post')
router.register(r'comments', CommentViewSet, basename='comment')

app_name = 'posts'

urlpatterns = [
    # Feed endpoint - shows posts from followed users
    path('feed/', FeedView.as_view(), name='feed'),
    
    # Like/Unlike endpoints
    path('posts/<int:pk>/like/', LikePostView.as_view(), name='like-post'),
    path('posts/<int:pk>/unlike/', UnlikePostView.as_view(), name='unlike-post'),
    path('posts/<int:pk>/likes/', PostLikesListView.as_view(), name='post-likes'),
    
    # Include all routes from the router
    path('', include(router.urls)),
]

