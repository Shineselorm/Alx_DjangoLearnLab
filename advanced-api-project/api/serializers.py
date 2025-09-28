from datetime import date

from rest_framework import serializers

from .models import Author, Book


class BookSerializer(serializers.ModelSerializer):
    """
    Serializes the Book model including all fields.

    Validation:
    - Ensures the publication_year is not in the future relative to the current year.
    """

    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'publication_year',
            'author',
        ]

    def validate_publication_year(self, value: int) -> int:
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(
                f"publication_year cannot be in the future (got {value}, current year is {current_year})."
            )
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializes the Author model with nested books.

    Fields:
    - name: author's name
    - books: nested list of BookSerializer representing the one-to-many relationship.

    Relationship Handling:
    - Uses the related_name 'books' from Book.author to include all books written by the author.
    - This serializer is read-only for nested books by default to avoid complex write operations.
    """

    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'books',
        ]


