"""
Serializers for User Authentication and Profile Management.
Handles serialization/deserialization of user data for API endpoints.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.password_validation import validate_password
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    Creates a new user with validated data and returns an authentication token.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    token = serializers.CharField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'password', 'password_confirm',
            'first_name', 'last_name', 'bio', 'profile_picture', 'token'
        ]
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'bio': {'required': False},
            'profile_picture': {'required': False},
        }
    
    def validate(self, attrs):
        """Validate that passwords match."""
        if attrs.get('password') != attrs.get('password_confirm'):
            raise serializers.ValidationError({
                'password': 'Password fields must match.'
            })
        return attrs
    
    def validate_email(self, value):
        """Ensure email is unique."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('A user with this email already exists.')
        return value
    
    def validate_username(self, value):
        """Ensure username is unique."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('A user with this username already exists.')
        return value
    
    def create(self, validated_data):
        """Create a new user with validated data."""
        # Remove password_confirm from validated data
        validated_data.pop('password_confirm')
        
        # Create user using create_user method to properly hash password
        user = User.objects.create_user(**validated_data)
        
        # Create authentication token for the user
        token = Token.objects.create(user=user)
        
        # Add token to user object for serialization
        user.token = token.key
        
        return user


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login.
    Authenticates user credentials and returns an authentication token.
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'}
    )
    token = serializers.CharField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    
    def get_user(self, obj):
        """Return basic user information."""
        user = obj.get('user')
        if user:
            return {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        return None
    
    def validate(self, attrs):
        """Authenticate user credentials."""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(
                request=self.context.get('request'),
                username=username,
                password=password
            )
            
            if not user:
                raise serializers.ValidationError(
                    'Invalid credentials. Please try again.',
                    code='authorization'
                )
            
            if not user.is_active:
                raise serializers.ValidationError(
                    'User account is disabled.',
                    code='authorization'
                )
            
            # Get or create token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            attrs['user'] = user
            attrs['token'] = token.key
        else:
            raise serializers.ValidationError(
                'Must include "username" and "password".',
                code='authorization'
            )
        
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile management.
    Provides detailed user information including follower/following counts.
    """
    follower_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'bio', 'profile_picture', 'date_joined', 'follower_count',
            'following_count', 'is_following'
        ]
        read_only_fields = ['id', 'username', 'date_joined']
    
    def get_follower_count(self, obj):
        """Return the count of followers."""
        return obj.get_follower_count()
    
    def get_following_count(self, obj):
        """Return the count of users being followed."""
        return obj.get_following_count()
    
    def get_is_following(self, obj):
        """Check if the current user is following this user."""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user.is_following(obj)
        return False


class UserListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for listing multiple users.
    Provides basic user information for user lists.
    """
    follower_count = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'bio', 'profile_picture', 'follower_count'
        ]
    
    def get_follower_count(self, obj):
        """Return the count of followers."""
        return obj.get_follower_count()


class FollowSerializer(serializers.Serializer):
    """
    Serializer for follow/unfollow actions.
    """
    user_id = serializers.IntegerField(required=True)
    action = serializers.ChoiceField(
        choices=['follow', 'unfollow'],
        required=True
    )
    
    def validate_user_id(self, value):
        """Validate that the user exists."""
        try:
            User.objects.get(pk=value)
        except User.DoesNotExist:
            raise serializers.ValidationError('User does not exist.')
        return value
    
    def validate(self, attrs):
        """Validate that user is not trying to follow themselves."""
        request = self.context.get('request')
        user_id = attrs.get('user_id')
        
        if request and request.user.id == user_id:
            raise serializers.ValidationError('You cannot follow/unfollow yourself.')
        
        return attrs

