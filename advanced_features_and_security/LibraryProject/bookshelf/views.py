from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.utils.html import escape
from django.core.paginator import Paginator
import logging
from .models import Book, BookReview, ReadingList, UserProfile
from .forms import SecureBookForm, SecureReviewForm, SecureReadingListForm, SecureSearchForm

# Security logger
security_logger = logging.getLogger('security')

User = get_user_model()


@permission_required('LibraryProject.bookshelf.can_view', raise_exception=True)
def book_list(request):
    """
    Display a list of all books with secure search functionality.
    Requires can_view permission.
    Prevents SQL injection through Django ORM parameterization.
    """
    books = Book.objects.all()
    
    # Secure search implementation
    search_query = request.GET.get('search', '').strip()
    if search_query:
        # Log search activity for security monitoring
        security_logger.info(f"Search query from user {request.user.email}: {escape(search_query)}")
        
        # Use Django ORM to prevent SQL injection
        # The ORM automatically escapes and parameterizes queries
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(isbn__icontains=search_query)
        )
    
    # Pagination for better performance and security
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    
    # Create search form for template
    search_form = SecureSearchForm(initial={'query': search_query})
    
    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'search_form': search_form,
        'search_query': escape(search_query) if search_query else '',
    })


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


@csrf_protect
@permission_required('LibraryProject.bookshelf.can_create', raise_exception=True)
def add_book(request):
    """
    Allow authenticated users to add a new book using secure form.
    Requires can_create permission.
    Implements CSRF protection and input validation.
    """
    if request.method == 'POST':
        form = SecureBookForm(request.POST, user=request.user)
        if form.is_valid():
            try:
                book = form.save()
                security_logger.info(f"Book created by user {request.user.email}: {book.title}")
                messages.success(request, f'Book "{book.title}" added successfully!')
                return redirect('bookshelf:book_detail', pk=book.pk)
            except Exception as e:
                security_logger.error(f"Error creating book by user {request.user.email}: {str(e)}")
                messages.error(request, 'An error occurred while creating the book.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SecureBookForm(user=request.user)
    
    return render(request, 'bookshelf/add_book.html', {'form': form})


@csrf_protect
@permission_required('LibraryProject.bookshelf.can_create', raise_exception=True)
def add_review(request, book_pk):
    """
    Allow authenticated users to add or update a review for a book using secure form.
    Requires can_create permission.
    Implements CSRF protection and input validation.
    """
    book = get_object_or_404(Book, pk=book_pk)
    
    # Check if user already has a review
    try:
        existing_review = BookReview.objects.get(book=book, reviewer=request.user)
        form = SecureReviewForm(
            request.POST or None,
            instance=existing_review,
            user=request.user,
            book=book
        )
        template = 'bookshelf/edit_review.html'
    except BookReview.DoesNotExist:
        form = SecureReviewForm(
            request.POST or None,
            user=request.user,
            book=book
        )
        template = 'bookshelf/add_review.html'
    
    if request.method == 'POST':
        if form.is_valid():
            try:
                review = form.save()
                security_logger.info(f"Review {'updated' if existing_review else 'created'} by user {request.user.email} for book {book.title}")
                messages.success(request, f'Review {"updated" if existing_review else "added"} successfully!')
                return redirect('bookshelf:book_detail', pk=book.pk)
            except Exception as e:
                security_logger.error(f"Error saving review by user {request.user.email}: {str(e)}")
                messages.error(request, 'An error occurred while saving the review.')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    return render(request, template, {
        'book': book,
        'form': form,
        'existing_review': existing_review if 'existing_review' in locals() else None
    })


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


def form_example(request):
    """
    Display secure form examples with CSRF protection.
    Demonstrates security best practices in form handling.
    """
    # Create sample forms to demonstrate security features
    book_form = SecureBookForm(user=request.user if request.user.is_authenticated else None)
    review_form = SecureReviewForm(user=request.user if request.user.is_authenticated else None)
    reading_list_form = SecureReadingListForm(user=request.user if request.user.is_authenticated else None)
    
    return render(request, 'bookshelf/form_example.html', {
        'book_form': book_form,
        'review_form': review_form,
        'reading_list_form': reading_list_form,
    })


@csrf_protect
@require_http_methods(["POST"])
def secure_api_endpoint(request):
    """
    Example of a secure API endpoint with CSRF protection.
    Demonstrates proper security practices for API endpoints.
    """
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    # Log API access for security monitoring
    security_logger.info(f"API access by user {request.user.email}: {request.path}")
    
    # Validate input data
    data = request.POST.get('data', '').strip()
    if not data:
        return JsonResponse({'error': 'Data is required'}, status=400)
    
    # Sanitize input to prevent XSS
    sanitized_data = escape(data)
    
    return JsonResponse({
        'success': True,
        'message': 'Data processed securely',
        'processed_data': sanitized_data,
    })
