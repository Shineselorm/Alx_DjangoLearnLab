# Open Django shell
python manage.py shell

# Update the title of the book
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()

# Expected Output:
# The book title updated successfully.
# Example: <Book: Nineteen Eighty-Four by George Orwell (1949)>
