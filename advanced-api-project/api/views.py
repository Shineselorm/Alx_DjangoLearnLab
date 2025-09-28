from rest_framework import generics, permissions

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
    permission_classes = [permissions.AllowAny]


class BookDetailView(generics.RetrieveAPIView):
    """
    Read-only endpoint returning a single book by primary key.

    Uses DRF's RetrieveAPIView to provide GET /books/<pk>/.
    Accessible to unauthenticated users.
    """

    queryset = Book.objects.select_related('author').all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    """
    Create a new Book instance.

    Only authenticated users can create books. Validation is handled by
    BookSerializer, including future-year checks for publication_year.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    """
    Update an existing Book instance by primary key.

    Only authenticated users can update books. Supports PUT/PATCH.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    """
    Delete an existing Book instance by primary key.

    Only authenticated users can delete books.
    """

    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
