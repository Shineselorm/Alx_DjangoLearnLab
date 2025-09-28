from rest_framework import generics, permissions, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Book
from .serializers import BookSerializer


class BookListView(generics.ListAPIView):
    """
    Read-only endpoint returning a list of all books.

    Uses DRF's ListAPIView generic to provide GET /books/.
    Accessible to unauthenticated users.
    """

    queryset = Book.objects.select_related('author').all().order_by('id')
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    # Enable filtering, searching, and ordering on the list endpoint
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    # Filter by exact field values
    filterset_fields = ['title', 'author', 'publication_year']
    # Search across text fields; author will search by related author's name
    search_fields = ['title', 'author__name']
    # Allow clients to order by specified fields (asc/desc via leading '-')
    ordering_fields = ['title', 'publication_year', 'id']
    # Default ordering when none provided
    ordering = ['id']


class BookDetailView(generics.RetrieveAPIView):
    """
    Read-only endpoint returning a single book by primary key.

    Uses DRF's RetrieveAPIView to provide GET /books/<pk>/.
    Accessible to unauthenticated users.
    """

    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    """
    Create a new Book instance.

    Only authenticated users can create books. Validation is handled by
    BookSerializer, including future-year checks for publication_year.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing Book instance by primary key.

    Only authenticated users can update books. Supports PUT/PATCH.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete an existing Book instance by primary key.

    Only authenticated users can delete books.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
