# CRUD Operations for Bookshelf App

## 1. Create
- **Functionality**: Add a new book to the bookshelf.
- **Endpoint**: `/books/create/`
- **Method**: POST
- **Fields**: `title`, `author`, `published_date`, `isbn`

## 2. Read
- **Functionality**: View all books or a single book.
- **Endpoint**: `/books/` (all books), `/books/<id>/` (single book)
- **Method**: GET

## 3. Update
- **Functionality**: Edit an existing book.
- **Endpoint**: `/books/update/<id>/`
- **Method**: POST/PUT
- **Fields**: `title`, `author`, `published_date`, `isbn`

## 4. Delete
- **Functionality**: Remove a book from the bookshelf.
- **Endpoint**: `/books/delete/<id>/`
- **Method**: POST/DELETE
