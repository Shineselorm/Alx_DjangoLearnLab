# Open Django shell
python manage.py shell

# Create a Book instance
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)

# Expected Output: A Book object created successfully
# Example: <Book: 1984 by George Orwell (1949)>
