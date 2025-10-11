"""
Views for User Authentication and Profile Management.
Handles user registration, login, profile management, and follow/unfollow functionality.
"""

from rest_framework import status, generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import (
    UserRegistrationSerializer,
    UserLoginSerializer,
    UserProfileSerializer,
    UserListSerializer,
    FollowSerializer
)

User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    """
    API endpoint for user registration.
    
    POST /api/accounts/register/
    Body: {
        "username": "string",
        "email": "string",
        "password": "string",
        "password_confirm": "string",
        "first_name": "string" (optional),
        "last_name": "string" (optional),
        "bio": "string" (optional)
    }
    
    Returns: {
        "id": int,
        "username": "string",
        "email": "string",
        "token": "string"
    }
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        """Create a new user and return user data with authentication token."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        
        return Response({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'bio': user.bio,
            'token': user.token,
            'message': 'User registered successfully!'
        }, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    API endpoint for user login.
    
    POST /api/accounts/login/
    Body: {
        "username": "string",
        "password": "string"
    }
    
    Returns: {
        "token": "string",
        "user": {
            "id": int,
            "username": "string",
            "email": "string"
        }
    }
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = UserLoginSerializer
    
    def post(self, request):
        """Authenticate user and return authentication token."""
        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        return Response({
            'token': serializer.validated_data['token'],
            'user': serializer.validated_data['user'],
            'message': 'Login successful!'
        }, status=status.HTTP_200_OK)


class UserLogoutView(APIView):
    """
    API endpoint for user logout.
    
    POST /api/accounts/logout/
    Headers: Authorization: Token <token>
    
    Returns: {
        "message": "Logged out successfully"
    }
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Delete user's authentication token."""
        try:
            # Delete the user's token to logout
            request.user.auth_token.delete()
            return Response({
                'message': 'Logged out successfully!'
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API endpoint for viewing and updating user profile.
    
    GET /api/accounts/profile/
    Headers: Authorization: Token <token>
    
    PUT/PATCH /api/accounts/profile/
    Headers: Authorization: Token <token>
    Body: {
        "first_name": "string" (optional),
        "last_name": "string" (optional),
        "bio": "string" (optional),
        "email": "string" (optional)
    }
    
    Returns: User profile data
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        """Return the current authenticated user."""
        return self.request.user


class UserDetailView(generics.RetrieveAPIView):
    """
    API endpoint for viewing another user's profile.
    
    GET /api/accounts/users/<user_id>/
    Headers: Authorization: Token <token>
    
    Returns: User profile data
    """
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'


class UserListView(generics.ListAPIView):
    """
    API endpoint for listing all users.
    
    GET /api/accounts/users/
    Headers: Authorization: Token <token>
    
    Returns: List of users
    """
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]


class FollowUserView(APIView):
    """
    API endpoint for following/unfollowing users.
    
    POST /api/accounts/follow/
    Headers: Authorization: Token <token>
    Body: {
        "user_id": int,
        "action": "follow" | "unfollow"
    }
    
    Returns: Success message
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request):
        """Follow or unfollow a user."""
        serializer = FollowSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        user_to_follow = get_object_or_404(
            User,
            pk=serializer.validated_data['user_id']
        )
        action = serializer.validated_data['action']
        
        if action == 'follow':
            request.user.follow(user_to_follow)
            message = f'You are now following {user_to_follow.username}'
        else:
            request.user.unfollow(user_to_follow)
            message = f'You have unfollowed {user_to_follow.username}'
        
        return Response({
            'message': message,
            'following': request.user.is_following(user_to_follow)
        }, status=status.HTTP_200_OK)


class FollowersListView(generics.ListAPIView):
    """
    API endpoint for viewing user's followers.
    
    GET /api/accounts/followers/
    Headers: Authorization: Token <token>
    
    Returns: List of followers
    """
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return list of users following the current user."""
        return self.request.user.followers.all()


class FollowingListView(generics.ListAPIView):
    """
    API endpoint for viewing users that the current user is following.
    
    GET /api/accounts/following/
    Headers: Authorization: Token <token>
    
    Returns: List of users being followed
    """
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Return list of users that current user is following."""
        return self.request.user.following.all()

