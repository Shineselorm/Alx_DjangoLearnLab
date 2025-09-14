"""
Test file for Django Permissions and Groups system.
This file demonstrates how to test the permission system.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from .models import Book, BookReview, ReadingList

User = get_user_model()


class PermissionsTestCase(TestCase):
    """Test cases for the permissions and groups system."""
    
    def setUp(self):
        """Set up test data."""
        # Create test users
        self.viewer_user = User.objects.create_user(
            email='viewer@test.com',
            username='viewer',
            password='testpass123'
        )
        
        self.editor_user = User.objects.create_user(
            email='editor@test.com',
            username='editor',
            password='testpass123'
        )
        
        self.admin_user = User.objects.create_user(
            email='admin@test.com',
            username='admin',
            password='testpass123'
        )
        
        # Create groups
        self.viewers_group = Group.objects.create(name='Viewers')
        self.editors_group = Group.objects.create(name='Editors')
        self.admins_group = Group.objects.create(name='Admins')
        
        # Get permissions
        book_content_type = ContentType.objects.get_for_model(Book)
        review_content_type = ContentType.objects.get_for_model(BookReview)
        reading_list_content_type = ContentType.objects.get_for_model(ReadingList)
        
        # Assign permissions to groups
        view_permissions = Permission.objects.filter(
            codename='can_view',
            content_type__in=[book_content_type, review_content_type, reading_list_content_type]
        )
        create_permissions = Permission.objects.filter(
            codename='can_create',
            content_type__in=[book_content_type, review_content_type, reading_list_content_type]
        )
        edit_permissions = Permission.objects.filter(
            codename='can_edit',
            content_type__in=[book_content_type, review_content_type, reading_list_content_type]
        )
        delete_permissions = Permission.objects.filter(
            codename='can_delete',
            content_type__in=[book_content_type, review_content_type, reading_list_content_type]
        )
        
        # Assign permissions
        self.viewers_group.permissions.set(view_permissions)
        self.editors_group.permissions.set(view_permissions | create_permissions | edit_permissions)
        self.admins_group.permissions.set(
            view_permissions | create_permissions | edit_permissions | delete_permissions
        )
        
        # Assign users to groups
        self.viewer_user.groups.add(self.viewers_group)
        self.editor_user.groups.add(self.editors_group)
        self.admin_user.groups.add(self.admins_group)
        
        # Create test book
        self.test_book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            isbn='1234567890123',
            publication_date='2023-01-01',
            added_by=self.admin_user
        )
        
        # Create test client
        self.client = Client()
    
    def test_viewer_permissions(self):
        """Test that viewers can only view content."""
        # Login as viewer
        self.client.login(email='viewer@test.com', password='testpass123')
        
        # Should be able to view book list
        response = self.client.get(reverse('bookshelf:book_list'))
        self.assertEqual(response.status_code, 200)
        
        # Should be able to view book detail
        response = self.client.get(reverse('bookshelf:book_detail', args=[self.test_book.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Should NOT be able to add books
        response = self.client.get(reverse('bookshelf:add_book'))
        self.assertEqual(response.status_code, 403)  # Permission denied
        
        # Should NOT be able to edit books
        response = self.client.get(reverse('bookshelf:edit_book', args=[self.test_book.pk]))
        self.assertEqual(response.status_code, 403)  # Permission denied
        
        # Should NOT be able to delete books
        response = self.client.get(reverse('bookshelf:delete_book', args=[self.test_book.pk]))
        self.assertEqual(response.status_code, 403)  # Permission denied
    
    def test_editor_permissions(self):
        """Test that editors can view, create, and edit content."""
        # Login as editor
        self.client.login(email='editor@test.com', password='testpass123')
        
        # Should be able to view book list
        response = self.client.get(reverse('bookshelf:book_list'))
        self.assertEqual(response.status_code, 200)
        
        # Should be able to add books
        response = self.client.get(reverse('bookshelf:add_book'))
        self.assertEqual(response.status_code, 200)
        
        # Should be able to edit books
        response = self.client.get(reverse('bookshelf:edit_book', args=[self.test_book.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Should NOT be able to delete books
        response = self.client.get(reverse('bookshelf:delete_book', args=[self.test_book.pk]))
        self.assertEqual(response.status_code, 403)  # Permission denied
    
    def test_admin_permissions(self):
        """Test that admins can perform all operations."""
        # Login as admin
        self.client.login(email='admin@test.com', password='testpass123')
        
        # Should be able to view book list
        response = self.client.get(reverse('bookshelf:book_list'))
        self.assertEqual(response.status_code, 200)
        
        # Should be able to add books
        response = self.client.get(reverse('bookshelf:add_book'))
        self.assertEqual(response.status_code, 200)
        
        # Should be able to edit books
        response = self.client.get(reverse('bookshelf:edit_book', args=[self.test_book.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Should be able to delete books
        response = self.client.get(reverse('bookshelf:delete_book', args=[self.test_book.pk]))
        self.assertEqual(response.status_code, 200)
    
    def test_unauthenticated_user(self):
        """Test that unauthenticated users cannot access protected views."""
        # Should NOT be able to view book list
        response = self.client.get(reverse('bookshelf:book_list'))
        self.assertEqual(response.status_code, 403)  # Permission denied
        
        # Should NOT be able to add books
        response = self.client.get(reverse('bookshelf:add_book'))
        self.assertEqual(response.status_code, 403)  # Permission denied
    
    def test_permission_checks_in_templates(self):
        """Test that permission checks work in templates."""
        # Login as viewer
        self.client.login(email='viewer@test.com', password='testpass123')
        
        # Get book list page
        response = self.client.get(reverse('bookshelf:book_list'))
        self.assertEqual(response.status_code, 200)
        
        # Check that user has correct permissions
        self.assertTrue(self.viewer_user.has_perm('LibraryProject.bookshelf.can_view'))
        self.assertFalse(self.viewer_user.has_perm('LibraryProject.bookshelf.can_create'))
        self.assertFalse(self.viewer_user.has_perm('LibraryProject.bookshelf.can_edit'))
        self.assertFalse(self.viewer_user.has_perm('LibraryProject.bookshelf.can_delete'))
    
    def test_group_assignment(self):
        """Test that users are correctly assigned to groups."""
        self.assertIn(self.viewers_group, self.viewer_user.groups.all())
        self.assertIn(self.editors_group, self.editor_user.groups.all())
        self.assertIn(self.admins_group, self.admin_user.groups.all())
    
    def test_permission_inheritance(self):
        """Test that group permissions are correctly inherited by users."""
        # Test viewer permissions
        self.assertTrue(self.viewer_user.has_perm('LibraryProject.bookshelf.can_view'))
        self.assertFalse(self.viewer_user.has_perm('LibraryProject.bookshelf.can_create'))
        
        # Test editor permissions
        self.assertTrue(self.editor_user.has_perm('LibraryProject.bookshelf.can_view'))
        self.assertTrue(self.editor_user.has_perm('LibraryProject.bookshelf.can_create'))
        self.assertTrue(self.editor_user.has_perm('LibraryProject.bookshelf.can_edit'))
        self.assertFalse(self.editor_user.has_perm('LibraryProject.bookshelf.can_delete'))
        
        # Test admin permissions
        self.assertTrue(self.admin_user.has_perm('LibraryProject.bookshelf.can_view'))
        self.assertTrue(self.admin_user.has_perm('LibraryProject.bookshelf.can_create'))
        self.assertTrue(self.admin_user.has_perm('LibraryProject.bookshelf.can_edit'))
        self.assertTrue(self.admin_user.has_perm('LibraryProject.bookshelf.can_delete'))
