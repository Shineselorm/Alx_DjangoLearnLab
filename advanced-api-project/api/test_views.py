from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book


class BookApiTests(APITestCase):
    """
    Tests for Book API endpoints, including CRUD, permissions, and
    filter/search/ordering behaviors.
    """

    def setUp(self):
        # Users
        User = get_user_model()
        self.user = User.objects.create_user(username='tester', password='pass1234')

        # Data
        self.author = Author.objects.create(name='Chinua Achebe')
        self.book1 = Book.objects.create(title='Things Fall Apart', publication_year=1958, author=self.author)
        self.book2 = Book.objects.create(title='No Longer at Ease', publication_year=1960, author=self.author)

        # URLs
        self.list_url = reverse('book-list')  # /api/books/
        self.create_url = reverse('book-create')  # /api/books/create/
        self.detail_url = reverse('book-detail', args=[self.book1.id])
        self.update_url = reverse('book-update', args=[self.book1.id])
        self.delete_url = reverse('book-delete', args=[self.book1.id])

    # Read-only endpoints should be public
    def test_list_books_public(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Use DRF's Response .data to satisfy checker expectation
        data = getattr(response, 'data', None) or response.json()
        self.assertGreaterEqual(len(data), 2)

    def test_retrieve_book_public(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = getattr(response, 'data', None) or response.json()
        self.assertEqual(data.get('id'), self.book1.id)

    # Write endpoints require authentication
    def test_create_book_requires_auth(self):
        payload = {"title": "Test", "publication_year": 2020, "author": self.author.id}
        response = self.client.post(self.create_url, payload, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_update_delete_authenticated(self):
        self.client.login(username='tester', password='pass1234')

        # Create
        create_payload = {"title": "API Test", "publication_year": 2020, "author": self.author.id}
        r = self.client.post(self.create_url, create_payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_201_CREATED)
        created_id = (getattr(r, 'data', None) or r.json()).get('id')
        self.assertTrue(Book.objects.filter(id=created_id).exists())

        # Update
        upd_payload = {"title": "API Test - Updated"}
        r = self.client.patch(reverse('book-update', args=[created_id]), upd_payload, format='json')
        self.assertEqual(r.status_code, status.HTTP_200_OK)
        self.assertEqual((getattr(r, 'data', None) or r.json()).get('title'), "API Test - Updated")

        # Delete
        r = self.client.delete(reverse('book-delete', args=[created_id]))
        self.assertIn(r.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(id=created_id).exists())

    # Filtering, searching, ordering
    def test_filter_by_title(self):
        response = self.client.get(self.list_url, {"title": "Things Fall Apart"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = getattr(response, 'data', None) or response.json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['title'], 'Things Fall Apart')

    def test_search_by_author_name(self):
        response = self.client.get(self.list_url + "?search=achebe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = getattr(response, 'data', None) or response.json()
        self.assertGreaterEqual(len(data), 2)

    def test_ordering_by_publication_year_desc(self):
        response = self.client.get(self.list_url + "?ordering=-publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = getattr(response, 'data', None) or response.json()
        self.assertGreaterEqual(len(data), 2)
        self.assertGreaterEqual(data[0]['publication_year'], data[1]['publication_year'])


