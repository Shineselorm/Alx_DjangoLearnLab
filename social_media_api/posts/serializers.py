"""
Serializers for Posts and Comments.
Handles data serialization and validation for API endpoints.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Post, Comment, Like

User = get_user_model()


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for displaying author information in posts and comments.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'profile_picture']
        read_only_fields = fields


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for Comment model.
    Handles creation, retrieval, and updates of comments.
    """
    author = AuthorSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'author_id', 'content',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
    
    def validate_content(self, value):
        """Validate that comment content is not empty."""
        if not value or not value.strip():
            raise serializers.ValidationError('Comment content cannot be empty.')
        if len(value) > 1000:
            raise serializers.ValidationError('Comment content cannot exceed 1000 characters.')
        return value.strip()
    
    def create(self, validated_data):
        """Create a new comment with the authenticated user as author."""
        # Remove author_id if present (we'll use request.user instead)
        validated_data.pop('author_id', None)
        
        # Get the authenticated user from context
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['author'] = request.user
        
        return super().create(validated_data)


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for Post model.
    Handles creation, retrieval, and updates of posts.
    """
    author = AuthorSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    comment_count = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'author_id', 'title', 'content',
            'created_at', 'updated_at', 'comment_count', 'comments'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'comment_count']
    
    def get_comment_count(self, obj):
        """Return the number of comments on this post."""
        return obj.get_comment_count()
    
    def validate_title(self, value):
        """Validate post title."""
        if not value or not value.strip():
            raise serializers.ValidationError('Post title cannot be empty.')
        if len(value) > 200:
            raise serializers.ValidationError('Post title cannot exceed 200 characters.')
        return value.strip()
    
    def validate_content(self, value):
        """Validate post content."""
        if not value or not value.strip():
            raise serializers.ValidationError('Post content cannot be empty.')
        return value.strip()
    
    def create(self, validated_data):
        """Create a new post with the authenticated user as author."""
        # Remove author_id if present (we'll use request.user instead)
        validated_data.pop('author_id', None)
        
        # Get the authenticated user from context
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['author'] = request.user
        
        return super().create(validated_data)


class PostListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing posts (without comments).
    Used for list views to improve performance.
    """
    author = AuthorSerializer(read_only=True)
    comment_count = serializers.SerializerMethodField(read_only=True)
    like_count = serializers.SerializerMethodField(read_only=True)
    is_liked_by_user = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'content',
            'created_at', 'updated_at', 'comment_count',
            'like_count', 'is_liked_by_user'
        ]
        read_only_fields = fields
    
    def get_comment_count(self, obj):
        """Return the number of comments on this post."""
        return obj.get_comment_count()
    
    def get_like_count(self, obj):
        """Return the number of likes on this post."""
        return obj.likes.count()
    
    def get_is_liked_by_user(self, obj):
        """Check if the current user has liked this post."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for Like model.
    Handles liking and unliking posts.
    """
    user = AuthorSerializer(read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'post_title', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def validate(self, attrs):
        """Validate that a user hasn't already liked this post."""
        request = self.context.get('request')
        post = attrs.get('post')
        
        if request and post:
            # Check if user has already liked this post
            if Like.objects.filter(user=request.user, post=post).exists():
                raise serializers.ValidationError('You have already liked this post.')
        
        return attrs
    
    def create(self, validated_data):
        """Create a new like with the authenticated user."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        
        return super().create(validated_data)

