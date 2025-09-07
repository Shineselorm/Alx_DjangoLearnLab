import os
import django

# Configure Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_models.settings')
django.setup()

from relationship_app.models import Author, Book, Library, Librarian

# --------- Query functions ---------
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return author.books.all()

def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

def librarian_of_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian

def library_by_librarian(librarian_name):
    librarian = Librarian.objects.get(name=librarian_name)
    return librarian.library

# --------- Seed + Demo run ---------
if __name__ == "__main__":
    # Seed sample data safely (won't duplicate on re-run)
    achebe, _ = Author.objects.get_or_create(name="Chinua Achebe")
    arrow, _ = Book.objects.get_or_create(title="Arrow of God", author=achebe)
    things, _ = Book.objects.get_or_create(title="Things Fall Apart", author=achebe)

    central, _ = Library.objects.get_or_create(name="Central Library")
    # Add books to library (add ignores duplicates)
    central.books.add(arrow, things)

    mary, _ = Librarian.objects.get_or_create(name="Mary Mensah", library=central)

    # Run queries
    print("Books by Chinua Achebe:", list(books_by_author("Chinua Achebe")))
    print("Books in Central Library:", list(books_in_library("Central Library")))
    print("Librarian of Central Library:", librarian_of_library("Central Library"))
    print("Library managed by Mary Mensah:", library_by_librarian("Mary Mensah"))
