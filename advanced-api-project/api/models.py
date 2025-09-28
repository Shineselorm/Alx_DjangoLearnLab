from django.db import models


class Author(models.Model):
    """
    Represents a book author.

    Fields:
    - name: Stores the full name of the author.
    """

    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    """
    Represents a book entity authored by a specific author.

    Fields:
    - title: Title of the book.
    - publication_year: Year the book was published. Used for validation in serializers.
    - author: ForeignKey linking to Author, establishing a one-to-many relationship
      (one Author to many Books).
    """

    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, related_name='books', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.title} ({self.publication_year})"
