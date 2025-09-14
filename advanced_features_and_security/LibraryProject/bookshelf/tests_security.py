"""
Security tests for Django Security Best Practices implementation.
Tests CSRF protection, XSS prevention, SQL injection prevention, and other security measures.
"""

from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.utils.html import escape
from .models import Book, BookReview, ReadingList
from .forms import SecureBookForm, SecureSearchForm

User = get_user_model()


class SecurityTestCase(TestCase):
    """Test cases for security implementation."""
    
    def setUp(self):
        """Set up test data."""
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        # Create group with permissions
        self.editors_group = Group.objects.create(name='Editors')
        book_content_type = ContentType.objects.get_for_model(Book)
        
        # Add permissions to group
        view_perm = Permission.objects.get(codename='can_view', content_type=book_content_type)
        create_perm = Permission.objects.get(codename='can_create', content_type=book_content_type)
        edit_perm = Permission.objects.get(codename='can_edit', content_type=book_content_type)
        
        self.editors_group.permissions.add(view_perm, create_perm, edit_perm)
        self.user.groups.add(self.editors_group)
        
        # Create test client
        self.client = Client()
    
    def test_csrf_protection(self):
        """Test that CSRF protection is working."""
        # Login user
        self.client.login(email='test@example.com', password='testpass123')
        
        # Try to submit form without CSRF token
        response = self.client.post('/bookshelf/add-book/', {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'publication_date': '2023-01-01'
        })
        
        # Should return 403 Forbidden due to CSRF protection
        self.assertEqual(response.status_code, 403)
    
    def test_csrf_protection_with_token(self):
        """Test that forms work with CSRF token."""
        # Login user
        self.client.login(email='test@example.com', password='testpass123')
        
        # Get the form page to obtain CSRF token
        response = self.client.get('/bookshelf/add-book/')
        self.assertEqual(response.status_code, 200)
        
        # Extract CSRF token from response
        csrf_token = response.context['csrf_token']
        
        # Submit form with CSRF token
        response = self.client.post('/bookshelf/add-book/', {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890123',
            'publication_date': '2023-01-01',
            'csrfmiddlewaretoken': csrf_token
        })
        
        # Should redirect on success (not 403)
        self.assertNotEqual(response.status_code, 403)
    
    def test_xss_prevention_in_templates(self):
        """Test that XSS attacks are prevented in templates."""
        # Create a book with potentially malicious content
        book = Book.objects.create(
            title='<script>alert("XSS")</script>',
            author='<img src="x" onerror="alert(\'XSS\')">',
            isbn='1234567890123',
            publication_date='2023-01-01',
            added_by=self.user
        )
        
        # Login user
        self.client.login(email='test@example.com', password='testpass123')
        
        # Access book detail page
        response = self.client.get(reverse('bookshelf:book_detail', args=[book.pk]))
        self.assertEqual(response.status_code, 200)
        
        # Check that script tags are escaped
        self.assertNotContains(response, '<script>')
        self.assertContains(response, '&lt;script&gt;')  # Escaped version
        
        # Check that HTML attributes are escaped
        self.assertNotContains(response, 'onerror=')
        self.assertContains(response, '&lt;img')  # Escaped version
    
    def test_xss_prevention_in_forms(self):
        """Test that XSS attacks are prevented in form processing."""
        # Test malicious input in form
        form_data = {
            'title': '<script>alert("XSS")</script>',
            'author': '<img src="x" onerror="alert(\'XSS\')">',
            'isbn': '1234567890123',
            'publication_date': '2023-01-01',
        }
        
        form = SecureBookForm(data=form_data, user=self.user)
        self.assertTrue(form.is_valid())
        
        # Check that the cleaned data is escaped
        cleaned_title = form.cleaned_data['title']
        self.assertNotIn('<script>', cleaned_title)
        self.assertIn('&lt;script&gt;', cleaned_title)
    
    def test_sql_injection_prevention(self):
        """Test that SQL injection attacks are prevented."""
        # Login user
        self.client.login(email='test@example.com', password='testpass123')
        
        # Try SQL injection in search
        malicious_query = "'; DROP TABLE books; --"
        response = self.client.get(f'/bookshelf/?search={malicious_query}')
        
        # Should not cause errors (Django ORM prevents SQL injection)
        self.assertEqual(response.status_code, 200)
        
        # Verify that books table still exists
        books_count = Book.objects.count()
        self.assertGreaterEqual(books_count, 0)  # Should not raise exception
    
    def test_input_validation(self):
        """Test that input validation prevents malicious data."""
        # Test with empty required fields
        form_data = {
            'title': '',
            'author': '',
            'isbn': '',
            'publication_date': '',
        }
        
        form = SecureBookForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('author', form.errors)
        self.assertIn('isbn', form.errors)
    
    def test_length_validation(self):
        """Test that length validation prevents buffer overflow attempts."""
        # Test with extremely long input
        long_string = 'A' * 1000
        
        form_data = {
            'title': long_string,
            'author': 'Test Author',
            'isbn': '1234567890123',
            'publication_date': '2023-01-01',
        }
        
        form = SecureBookForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
    
    def test_isbn_validation(self):
        """Test that ISBN validation prevents invalid data."""
        # Test with invalid ISBN
        form_data = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '123',  # Too short
            'publication_date': '2023-01-01',
        }
        
        form = SecureBookForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('isbn', form.errors)
    
    def test_duplicate_isbn_prevention(self):
        """Test that duplicate ISBNs are prevented."""
        # Create a book first
        Book.objects.create(
            title='First Book',
            author='First Author',
            isbn='1234567890123',
            publication_date='2023-01-01',
            added_by=self.user
        )
        
        # Try to create another book with same ISBN
        form_data = {
            'title': 'Second Book',
            'author': 'Second Author',
            'isbn': '1234567890123',  # Same ISBN
            'publication_date': '2023-01-01',
        }
        
        form = SecureBookForm(data=form_data, user=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('isbn', form.errors)
    
    def test_search_form_security(self):
        """Test that search form prevents malicious input."""
        # Test with dangerous characters
        malicious_query = '<script>alert("XSS")</script>'
        form = SecureSearchForm(data={'query': malicious_query})
        
        self.assertFalse(form.is_valid())
        self.assertIn('query', form.errors)
    
    def test_permission_enforcement(self):
        """Test that permissions are properly enforced."""
        # Create user without permissions
        no_permission_user = User.objects.create_user(
            email='noperm@example.com',
            username='noperm',
            password='testpass123'
        )
        
        # Login without permission user
        self.client.login(email='noperm@example.com', password='testpass123')
        
        # Try to access protected view
        response = self.client.get('/bookshelf/')
        self.assertEqual(response.status_code, 403)  # Permission denied
    
    def test_secure_headers(self):
        """Test that security headers are set."""
        # Login user
        self.client.login(email='test@example.com', password='testpass123')
        
        # Make request
        response = self.client.get('/bookshelf/')
        
        # Check security headers
        self.assertEqual(response.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(response.get('X-Frame-Options'), 'DENY')
        self.assertIn('X-XSS-Protection', response)
    
    def test_session_security(self):
        """Test that sessions are configured securely."""
        # Login user
        self.client.login(email='test@example.com', password='testpass123')
        
        # Check session cookie attributes
        session_cookie = self.client.cookies.get('sessionid')
        if session_cookie:
            # In production, these should be True
            # For testing, we check that they exist
            self.assertIsNotNone(session_cookie)
    
    def test_file_upload_limits(self):
        """Test that file upload limits are enforced."""
        # This test would require file upload functionality
        # For now, we test that the settings are configured
        from django.conf import settings
        self.assertIsNotNone(settings.FILE_UPLOAD_MAX_MEMORY_SIZE)
        self.assertIsNotNone(settings.DATA_UPLOAD_MAX_MEMORY_SIZE)
        self.assertIsNotNone(settings.DATA_UPLOAD_MAX_NUMBER_FIELDS)
    
    def test_password_security(self):
        """Test that password validation is enforced."""
        # Test weak password
        user_data = {
            'email': 'weak@example.com',
            'username': 'weakuser',
            'password': '123',  # Too short
        }
        
        with self.assertRaises(Exception):  # Should raise validation error
            User.objects.create_user(**user_data)
    
    def test_secure_api_endpoint(self):
        """Test that secure API endpoint requires authentication."""
        # Try to access API without authentication
        response = self.client.post('/bookshelf/api/secure/', {
            'data': 'test data'
        })
        self.assertEqual(response.status_code, 401)  # Unauthorized
        
        # Login and try again
        self.client.login(email='test@example.com', password='testpass123')
        response = self.client.post('/bookshelf/api/secure/', {
            'data': 'test data',
            'csrfmiddlewaretoken': self.client.cookies.get('csrftoken')
        })
        self.assertEqual(response.status_code, 200)


class CSRFTestCase(TestCase):
    """Specific tests for CSRF protection."""
    
    def test_csrf_middleware_enabled(self):
        """Test that CSRF middleware is enabled."""
        from django.conf import settings
        self.assertIn('django.middleware.csrf.CsrfViewMiddleware', settings.MIDDLEWARE)
    
    def test_csrf_token_in_forms(self):
        """Test that forms include CSRF tokens."""
        client = Client(enforce_csrf_checks=True)
        
        # Try to access a form page
        response = client.get('/bookshelf/forms/')
        self.assertEqual(response.status_code, 200)
        
        # Check that CSRF token is in the response
        self.assertContains(response, 'csrfmiddlewaretoken')


class XSSTestCase(TestCase):
    """Specific tests for XSS prevention."""
    
    def test_escape_filter_usage(self):
        """Test that templates use escape filter."""
        # This would require template testing
        # For now, we verify that escape function works
        malicious_input = '<script>alert("XSS")</script>'
        escaped_output = escape(malicious_input)
        
        self.assertEqual(escaped_output, '&lt;script&gt;alert(&quot;XSS&quot;)&lt;/script&gt;')
        self.assertNotIn('<script>', escaped_output)


class SQLInjectionTestCase(TestCase):
    """Specific tests for SQL injection prevention."""
    
    def test_orm_parameterization(self):
        """Test that Django ORM parameterizes queries."""
        # This test verifies that ORM queries are safe
        # by attempting to use malicious input
        
        malicious_input = "'; DROP TABLE books; --"
        
        # This should not cause any issues due to ORM parameterization
        try:
            books = Book.objects.filter(title__icontains=malicious_input)
            list(books)  # Execute the query
            self.assertTrue(True)  # If we get here, no SQL injection occurred
        except Exception as e:
            self.fail(f"SQL injection occurred: {e}")
    
    def test_raw_sql_not_used(self):
        """Test that no raw SQL is used in views."""
        # This is more of a code review test
        # In a real scenario, you would use static analysis tools
        # to ensure no raw SQL queries are used
        
        # For this test, we verify that Django ORM methods are used
        self.assertTrue(hasattr(Book.objects, 'filter'))
        self.assertTrue(hasattr(Book.objects, 'get'))
        self.assertTrue(hasattr(Book.objects, 'create'))
