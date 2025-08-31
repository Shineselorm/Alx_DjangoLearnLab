# Open Django shell
python manage.py shell

# Delete the book
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm deletion by retrieving all books
print(Book.objects.all())

# Expected Output:
# <QuerySet []>  (empty list, meaning no books in the database)
