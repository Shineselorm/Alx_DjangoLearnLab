"""
Views for Posts and Comments functionality.
Implements CRUD operations with proper permissions and filtering.
"""

from rest_framework import viewsets, permissions, filters, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Post, Comment
from .serializers import (
    PostSerializer,
    PostListSerializer,
    CommentSerializer
)

User = get_user_model()


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of an object to edit or delete it.
    Read permissions are allowed to any authenticated user.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request (GET, HEAD, OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the author
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model providing CRUD operations.
    
    Endpoints:
    - GET /api/posts/ - List all posts
    - POST /api/posts/ - Create a new post
    - GET /api/posts/{id}/ - Retrieve a specific post
    - PUT/PATCH /api/posts/{id}/ - Update a post (author only)
    - DELETE /api/posts/{id}/ - Delete a post (author only)
    
    Filtering:
    - Search by title or content: ?search=keyword
    - Filter by author: ?author=username
    
    Ordering:
    - Order by created_at: ?ordering=-created_at
    """
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content', 'author__username']
    ordering_fields = ['created_at', 'updated_at', 'title']
    ordering = ['-created_at']  # Default ordering
    
    def get_queryset(self):
        """
        Get queryset with optional filtering.
        Supports filtering by author username.
        """
        queryset = Post.objects.all().select_related('author').prefetch_related('comments')
        
        # Filter by author username if provided
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__username=author)
        
        # Filter by title or content if 'q' parameter is provided
        query = self.request.query_params.get('q', None)
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(content__icontains=query)
            )
        
        return queryset
    
    def get_serializer_class(self):
        """
        Use different serializers for list and detail views.
        List view uses simplified serializer for performance.
        """
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer
    
    def perform_create(self, serializer):
        """Set the author to the current user when creating a post."""
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        """
        Custom action to retrieve all comments for a specific post.
        GET /api/posts/{id}/comments/
        """
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def my_posts(self, request):
        """
        Custom action to retrieve posts created by the authenticated user.
        GET /api/posts/my_posts/
        """
        posts = Post.objects.filter(author=request.user)
        
        page = self.paginate_queryset(posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Comment model providing CRUD operations.
    
    Endpoints:
    - GET /api/comments/ - List all comments
    - POST /api/comments/ - Create a new comment
    - GET /api/comments/{id}/ - Retrieve a specific comment
    - PUT/PATCH /api/comments/{id}/ - Update a comment (author only)
    - DELETE /api/comments/{id}/ - Delete a comment (author only)
    
    Filtering:
    - Filter by post: ?post=post_id
    - Filter by author: ?author=username
    - Search content: ?search=keyword
    """
    
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['content', 'author__username']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['created_at']  # Default ordering (chronological)
    
    def get_queryset(self):
        """
        Get queryset with optional filtering.
        Supports filtering by post ID and author username.
        """
        queryset = Comment.objects.all().select_related('author', 'post')
        
        # Filter by post ID if provided
        post_id = self.request.query_params.get('post', None)
        if post_id:
            queryset = queryset.filter(post_id=post_id)
        
        # Filter by author username if provided
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__username=author)
        
        return queryset
    
    def perform_create(self, serializer):
        """Set the author to the current user when creating a comment."""
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_comments(self, request):
        """
        Custom action to retrieve comments created by the authenticated user.
        GET /api/comments/my_comments/
        """
        comments = Comment.objects.filter(author=request.user)
        
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(comments, many=True)
        return Response(serializer.data)


class FeedView(generics.ListAPIView):
    """
    API endpoint for viewing feed of posts from followed users.
    
    GET /api/feed/
    Headers: Authorization: Token <token>
    
    Returns: Posts from users that the authenticated user follows,
             ordered by creation date (most recent first)
    """
    serializer_class = PostListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        Get posts from users that the current user follows.
        Returns posts ordered by creation date, most recent first.
        """
        # Get the current user
        current_user = self.request.user
        
        # Get all users that the current user is following
        following_users = current_user.following.all()
        
        # Get posts from those users, ordered by creation date (most recent first)
        # Using following.all() which returns users the current user follows
        # Filter posts by followed users and order by creation date
        feed_posts = Post.objects.filter(author__in=following_users).order_by('-created_at')
        
        # Optimize query with select_related and prefetch_related
        feed_posts = feed_posts.select_related('author').prefetch_related('comments')
        
        return feed_posts
    
    def list(self, request, *args, **kwargs):
        """
        Override list to provide custom response with additional context.
        """
        queryset = self.filter_queryset(self.get_queryset())
        following_count = request.user.following.count()
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            response = self.get_paginated_response(serializer.data)
            response.data['following_count'] = following_count
            return response
        
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'count': queryset.count(),
            'following_count': following_count,
            'results': serializer.data
        })

