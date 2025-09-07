from django.db import models
from typing import TYPE_CHECKING, Any


class Author(models.Model):
    name = models.CharField(max_length=100)
    
    if TYPE_CHECKING:
        objects: Any

    def __str__(self):
        return str(self.name)


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    
    if TYPE_CHECKING:
        objects: Any

    def __str__(self):
        return str(self.title)


class Library(models.Model):
    name = models.CharField(max_length=100)
    books = models.ManyToManyField(Book, related_name="libraries")
    
    if TYPE_CHECKING:
        objects: Any

    def __str__(self):
        return str(self.name)


class Librarian(models.Model):
    name = models.CharField(max_length=100)
    library = models.OneToOneField(Library, on_delete=models.CASCADE, related_name="librarian")
    
    if TYPE_CHECKING:
        objects: Any

    def __str__(self):
        return str(self.name)

