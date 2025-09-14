from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from datetime import date

User = get_user_model()


class CustomUserModelTest(TestCase):
    """Test cases for the CustomUser model."""
    
    def setUp(self):
        """Set up test data."""
        self.user_data = {
            'email': 'test@example.com',
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User',
            'date_of_birth': date(1990, 1, 1),
        }
    
    def test_create_user(self):
        """Test creating a regular user."""
        user = User.objects.create_user(
            email=self.user_data['email'],
            username=self.user_data['username'],
            password='testpass123',
            first_name=self.user_data['first_name'],
            last_name=self.user_data['last_name'],
            date_of_birth=self.user_data['date_of_birth']
        )
        
        self.assertEqual(user.email, self.user_data['email'])
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.first_name, self.user_data['first_name'])
        self.assertEqual(user.last_name, self.user_data['last_name'])
        self.assertEqual(user.date_of_birth, self.user_data['date_of_birth'])
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
    
    def test_create_superuser(self):
        """Test creating a superuser."""
        user = User.objects.create_superuser(
            email='admin@example.com',
            username='admin',
            password='adminpass123'
        )
        
        self.assertEqual(user.email, 'admin@example.com')
        self.assertEqual(user.username, 'admin')
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
    
    def test_email_required(self):
        """Test that email is required for user creation."""
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                username='testuser',
                password='testpass123'
            )
    
    def test_email_uniqueness(self):
        """Test that email addresses must be unique."""
        User.objects.create_user(
            email='test@example.com',
            username='user1',
            password='testpass123'
        )
        
        with self.assertRaises(Exception):  # IntegrityError
            User.objects.create_user(
                email='test@example.com',
                username='user2',
                password='testpass123'
            )
    
    def test_user_str_representation(self):
        """Test the string representation of the user."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        self.assertEqual(str(user), 'test@example.com')
    
    def test_user_model_settings(self):
        """Test that the custom user model settings are correct."""
        self.assertEqual(User.USERNAME_FIELD, 'email')
        self.assertEqual(User.REQUIRED_FIELDS, ['username'])


class CustomUserManagerTest(TestCase):
    """Test cases for the CustomUserManager."""
    
    def test_create_user_with_email(self):
        """Test creating user with email and password."""
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        self.assertTrue(user.check_password('testpass123'))
        self.assertEqual(user.email, 'test@example.com')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_create_superuser_validation(self):
        """Test superuser creation validation."""
        # Test that is_staff=True is required
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                username='admin',
                password='adminpass123',
                is_staff=False
            )
        
        # Test that is_superuser=True is required
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email='admin@example.com',
                username='admin',
                password='adminpass123',
                is_superuser=False
            )
