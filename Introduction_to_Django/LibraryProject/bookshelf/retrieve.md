# Open Django shell
python manage.py shell

# Retrieve and display all attributes of the created book
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(book.title, book.author, book.publication_year)

# Expected Output:
# 1984 George Orwell 1949
