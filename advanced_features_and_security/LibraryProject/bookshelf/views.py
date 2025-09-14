from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from .models import Book, BookReview, ReadingList, UserProfile

User = get_user_model()


@permission_required('LibraryProject.bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display a list of all books.
    Requires can_view permission.
    """
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})


@permission_required('LibraryProject.bookshelf.can_view', raise_exception=True)
def book_detail(request, pk):
    """
    Display details of a specific book including reviews.
    Requires can_view permission.
    """
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all()
    
    # Check if current user has reviewed this book
    user_review = None
    if request.user.is_authenticated:
        try:
            user_review = reviews.get(reviewer=request.user)
        except BookReview.DoesNotExist:
            pass
    
    return render(request, 'bookshelf/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'user_review': user_review
    })


@permission_required('LibraryProject.bookshelf.can_create', raise_exception=True)
def add_book(request):
    """
    Allow authenticated users to add a new book.
    Requires can_create permission.
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        author = request.POST.get('author')
        isbn = request.POST.get('isbn')
        publication_date = request.POST.get('publication_date')
        
        if title and author and isbn:
            book = Book.objects.create(
                title=title,
                author=author,
                isbn=isbn,
                publication_date=publication_date,
                added_by=request.user
            )
            messages.success(request, f'Book "{book.title}" added successfully!')
            return redirect('book_detail', pk=book.pk)
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'bookshelf/add_book.html')


@permission_required('LibraryProject.bookshelf.can_create', raise_exception=True)
def add_review(request, book_pk):
    """
    Allow authenticated users to add or update a review for a book.
    Requires can_create permission.
    """
    book = get_object_or_404(Book, pk=book_pk)
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        review_text = request.POST.get('review_text')
        
        if rating and review_text:
            review, created = BookReview.objects.get_or_create(
                book=book,
                reviewer=request.user,
                defaults={'rating': rating, 'review_text': review_text}
            )
            
            if not created:
                review.rating = rating
                review.review_text = review_text
                review.save()
                messages.success(request, 'Review updated successfully!')
            else:
                messages.success(request, 'Review added successfully!')
            
            return redirect('book_detail', pk=book.pk)
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    # Check if user already has a review
    try:
        existing_review = BookReview.objects.get(book=book, reviewer=request.user)
        return render(request, 'bookshelf/edit_review.html', {
            'book': book,
            'review': existing_review
        })
    except BookReview.DoesNotExist:
        return render(request, 'bookshelf/add_review.html', {'book': book})


@permission_required('LibraryProject.bookshelf.can_view', raise_exception=True)
def my_reading_lists(request):
    """
    Display user's reading lists.
    Requires can_view permission.
    """
    reading_lists = ReadingList.objects.filter(owner=request.user)
    return render(request, 'bookshelf/my_reading_lists.html', {
        'reading_lists': reading_lists
    })


@permission_required('LibraryProject.bookshelf.can_create', raise_exception=True)
def create_reading_list(request):
    """
    Allow users to create a new reading list.
    Requires can_create permission.
    """
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        is_public = request.POST.get('is_public') == 'on'
        
        if name:
            reading_list = ReadingList.objects.create(
                name=name,
                description=description,
                is_public=is_public,
                owner=request.user
            )
            messages.success(request, f'Reading list "{reading_list.name}" created successfully!')
            return redirect('my_reading_lists')
        else:
            messages.error(request, 'Please provide a name for the reading list.')
    
    return render(request, 'bookshelf/create_reading_list.html')


@permission_required('LibraryProject.bookshelf.can_view', raise_exception=True)
def public_reading_lists(request):
    """
    Display public reading lists.
    Requires can_view permission.
    """
    reading_lists = ReadingList.objects.filter(is_public=True)
    return render(request, 'bookshelf/public_reading_lists.html', {
        'reading_lists': reading_lists
    })


@permission_required('LibraryProject.bookshelf.can_edit', raise_exception=True)
def edit_book(request, pk):
    """
    Allow users to edit a book.
    Requires can_edit permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book.title = request.POST.get('title', book.title)
        book.author = request.POST.get('author', book.author)
        book.isbn = request.POST.get('isbn', book.isbn)
        book.publication_date = request.POST.get('publication_date', book.publication_date)
        book.save()
        messages.success(request, f'Book "{book.title}" updated successfully!')
        return redirect('book_detail', pk=book.pk)
    
    return render(request, 'bookshelf/edit_book.html', {'book': book})


@permission_required('LibraryProject.bookshelf.can_delete', raise_exception=True)
def delete_book(request, pk):
    """
    Allow users to delete a book.
    Requires can_delete permission.
    """
    book = get_object_or_404(Book, pk=pk)
    
    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" deleted successfully!')
        return redirect('book_list')
    
    return render(request, 'bookshelf/delete_book.html', {'book': book})


@permission_required('LibraryProject.bookshelf.can_edit', raise_exception=True)
def edit_review(request, pk):
    """
    Allow users to edit their own review.
    Requires can_edit permission.
    """
    review = get_object_or_404(BookReview, pk=pk, reviewer=request.user)
    
    if request.method == 'POST':
        review.rating = request.POST.get('rating', review.rating)
        review.review_text = request.POST.get('review_text', review.review_text)
        review.save()
        messages.success(request, 'Review updated successfully!')
        return redirect('book_detail', pk=review.book.pk)
    
    return render(request, 'bookshelf/edit_review.html', {'review': review})


@permission_required('LibraryProject.bookshelf.can_delete', raise_exception=True)
def delete_review(request, pk):
    """
    Allow users to delete their own review.
    Requires can_delete permission.
    """
    review = get_object_or_404(BookReview, pk=pk, reviewer=request.user)
    book_pk = review.book.pk
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Review deleted successfully!')
        return redirect('book_detail', pk=book_pk)
    
    return render(request, 'bookshelf/delete_review.html', {'review': review})
