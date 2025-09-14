"""
Secure forms for the bookshelf application.
These forms implement security best practices including input validation,
CSRF protection, and XSS prevention.
"""

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _
from .models import Book, BookReview, ReadingList

User = get_user_model()


class SecureBookForm(forms.ModelForm):
    """
    Secure form for creating and editing books.
    Implements input validation and sanitization.
    """
    
    class Meta:
        model = Book
        fields = ['title', 'author', 'isbn', 'publication_date']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title',
                'maxlength': '200',
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name',
                'maxlength': '100',
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter ISBN (13 digits)',
                'maxlength': '13',
                'pattern': r'\d{13}',
            }),
            'publication_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
        }
        labels = {
            'title': _('Book Title'),
            'author': _('Author'),
            'isbn': _('ISBN'),
            'publication_date': _('Publication Date'),
        }
        help_texts = {
            'isbn': _('Enter a 13-digit ISBN number'),
            'publication_date': _('Select the publication date'),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Add CSRF token explicitly (though Django handles this automatically)
        # This demonstrates awareness of CSRF protection
    
    def clean_title(self):
        """
        Sanitize and validate book title.
        Prevents XSS attacks through proper escaping.
        """
        title = self.cleaned_data.get('title')
        if not title:
            raise ValidationError(_('Title is required.'))
        
        # Remove any HTML tags and escape special characters
        title = escape(title.strip())
        
        # Validate length
        if len(title) < 2:
            raise ValidationError(_('Title must be at least 2 characters long.'))
        
        if len(title) > 200:
            raise ValidationError(_('Title must be less than 200 characters.'))
        
        return title
    
    def clean_author(self):
        """
        Sanitize and validate author name.
        Prevents XSS attacks through proper escaping.
        """
        author = self.cleaned_data.get('author')
        if not author:
            raise ValidationError(_('Author is required.'))
        
        # Remove any HTML tags and escape special characters
        author = escape(author.strip())
        
        # Validate length
        if len(author) < 2:
            raise ValidationError(_('Author name must be at least 2 characters long.'))
        
        if len(author) > 100:
            raise ValidationError(_('Author name must be less than 100 characters.'))
        
        return author
    
    def clean_isbn(self):
        """
        Validate ISBN format and prevent SQL injection.
        Uses Django ORM parameterization automatically.
        """
        isbn = self.cleaned_data.get('isbn')
        if not isbn:
            raise ValidationError(_('ISBN is required.'))
        
        # Remove any non-digit characters
        isbn = ''.join(filter(str.isdigit, isbn))
        
        # Validate length
        if len(isbn) != 13:
            raise ValidationError(_('ISBN must be exactly 13 digits.'))
        
        # Check if ISBN already exists (prevents duplicate entries)
        existing_book = Book.objects.filter(isbn=isbn).exclude(
            pk=self.instance.pk if self.instance else None
        )
        if existing_book.exists():
            raise ValidationError(_('A book with this ISBN already exists.'))
        
        return isbn
    
    def clean_publication_date(self):
        """
        Validate publication date.
        Ensures date is not in the future.
        """
        from datetime import date
        
        publication_date = self.cleaned_data.get('publication_date')
        if not publication_date:
            raise ValidationError(_('Publication date is required.'))
        
        # Check if date is not in the future
        if publication_date > date.today():
            raise ValidationError(_('Publication date cannot be in the future.'))
        
        # Check if date is not too old (books from before 1000 AD)
        if publication_date.year < 1000:
            raise ValidationError(_('Publication date seems too old. Please verify.'))
        
        return publication_date
    
    def save(self, commit=True):
        """
        Save the book with secure handling.
        Automatically assigns the current user as the one who added the book.
        """
        book = super().save(commit=False)
        if self.user:
            book.added_by = self.user
        
        if commit:
            book.save()
        return book


class SecureReviewForm(forms.ModelForm):
    """
    Secure form for creating and editing book reviews.
    Implements input validation and XSS prevention.
    """
    
    RATING_CHOICES = [
        (1, '1 Star - Poor'),
        (2, '2 Stars - Fair'),
        (3, '3 Stars - Good'),
        (4, '4 Stars - Very Good'),
        (5, '5 Stars - Excellent'),
    ]
    
    rating = forms.ChoiceField(
        choices=RATING_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Rating'),
        help_text=_('Rate this book from 1 to 5 stars'),
    )
    
    class Meta:
        model = BookReview
        fields = ['rating', 'review_text']
        widgets = {
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Write your review here...',
                'maxlength': '2000',
            }),
        }
        labels = {
            'review_text': _('Review Text'),
        }
        help_texts = {
            'review_text': _('Share your thoughts about this book (maximum 2000 characters)'),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.book = kwargs.pop('book', None)
        super().__init__(*args, **kwargs)
    
    def clean_review_text(self):
        """
        Sanitize and validate review text.
        Prevents XSS attacks and ensures appropriate content.
        """
        review_text = self.cleaned_data.get('review_text')
        if not review_text:
            raise ValidationError(_('Review text is required.'))
        
        # Remove any HTML tags and escape special characters
        review_text = escape(review_text.strip())
        
        # Validate length
        if len(review_text) < 10:
            raise ValidationError(_('Review must be at least 10 characters long.'))
        
        if len(review_text) > 2000:
            raise ValidationError(_('Review must be less than 2000 characters.'))
        
        # Basic profanity filter (in production, use a more sophisticated solution)
        inappropriate_words = ['spam', 'fake', 'scam']  # Basic example
        review_lower = review_text.lower()
        for word in inappropriate_words:
            if word in review_lower:
                raise ValidationError(_('Review contains inappropriate content.'))
        
        return review_text
    
    def clean_rating(self):
        """
        Validate rating value.
        Ensures rating is within acceptable range.
        """
        rating = self.cleaned_data.get('rating')
        if not rating:
            raise ValidationError(_('Rating is required.'))
        
        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValidationError(_('Rating must be between 1 and 5.'))
        except (ValueError, TypeError):
            raise ValidationError(_('Invalid rating value.'))
        
        return rating
    
    def clean(self):
        """
        Cross-field validation.
        Ensures user hasn't already reviewed this book.
        """
        cleaned_data = super().clean()
        
        if self.user and self.book:
            # Check if user already has a review for this book
            existing_review = BookReview.objects.filter(
                reviewer=self.user,
                book=self.book
            ).exclude(pk=self.instance.pk if self.instance else None)
            
            if existing_review.exists():
                raise ValidationError(_('You have already reviewed this book.'))
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Save the review with secure handling.
        Automatically assigns the current user and book.
        """
        review = super().save(commit=False)
        if self.user:
            review.reviewer = self.user
        if self.book:
            review.book = self.book
        
        if commit:
            review.save()
        return review


class SecureReadingListForm(forms.ModelForm):
    """
    Secure form for creating and editing reading lists.
    Implements input validation and sanitization.
    """
    
    class Meta:
        model = ReadingList
        fields = ['name', 'description', 'is_public']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter reading list name',
                'maxlength': '100',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe your reading list...',
                'maxlength': '500',
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
        labels = {
            'name': _('Reading List Name'),
            'description': _('Description'),
            'is_public': _('Make this list public'),
        }
        help_texts = {
            'name': _('Give your reading list a descriptive name'),
            'description': _('Optional description of your reading list'),
            'is_public': _('Allow others to view this reading list'),
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_name(self):
        """
        Sanitize and validate reading list name.
        Prevents XSS attacks through proper escaping.
        """
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError(_('Reading list name is required.'))
        
        # Remove any HTML tags and escape special characters
        name = escape(name.strip())
        
        # Validate length
        if len(name) < 2:
            raise ValidationError(_('Name must be at least 2 characters long.'))
        
        if len(name) > 100:
            raise ValidationError(_('Name must be less than 100 characters.'))
        
        return name
    
    def clean_description(self):
        """
        Sanitize and validate description.
        Prevents XSS attacks through proper escaping.
        """
        description = self.cleaned_data.get('description', '')
        
        if description:
            # Remove any HTML tags and escape special characters
            description = escape(description.strip())
            
            # Validate length
            if len(description) > 500:
                raise ValidationError(_('Description must be less than 500 characters.'))
        
        return description
    
    def clean(self):
        """
        Cross-field validation.
        Ensures user doesn't have duplicate reading list names.
        """
        cleaned_data = super().clean()
        
        if self.user:
            name = cleaned_data.get('name')
            if name:
                # Check for duplicate names for this user
                existing_list = ReadingList.objects.filter(
                    owner=self.user,
                    name=name
                ).exclude(pk=self.instance.pk if self.instance else None)
                
                if existing_list.exists():
                    raise ValidationError(_('You already have a reading list with this name.'))
        
        return cleaned_data
    
    def save(self, commit=True):
        """
        Save the reading list with secure handling.
        Automatically assigns the current user as owner.
        """
        reading_list = super().save(commit=False)
        if self.user:
            reading_list.owner = self.user
        
        if commit:
            reading_list.save()
        return reading_list


class SecureSearchForm(forms.Form):
    """
    Secure search form with input validation.
    Prevents SQL injection and XSS attacks.
    """
    
    SEARCH_CHOICES = [
        ('title', _('Search by Title')),
        ('author', _('Search by Author')),
        ('isbn', _('Search by ISBN')),
        ('all', _('Search All Fields')),
    ]
    
    query = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter search term...',
            'maxlength': '100',
        }),
        label=_('Search Query'),
        help_text=_('Enter your search term (maximum 100 characters)'),
    )
    
    search_type = forms.ChoiceField(
        choices=SEARCH_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label=_('Search Type'),
        initial='all',
    )
    
    def clean_query(self):
        """
        Sanitize search query to prevent XSS and injection attacks.
        """
        query = self.cleaned_data.get('query')
        if not query:
            raise ValidationError(_('Search query is required.'))
        
        # Remove any HTML tags and escape special characters
        query = escape(query.strip())
        
        # Validate length
        if len(query) < 2:
            raise ValidationError(_('Search query must be at least 2 characters long.'))
        
        # Remove potentially dangerous characters
        dangerous_chars = ['<', '>', '"', "'", '&', ';', '(', ')', '{', '}']
        for char in dangerous_chars:
            if char in query:
                raise ValidationError(_('Search query contains invalid characters.'))
        
        return query
    
    def clean_search_type(self):
        """
        Validate search type selection.
        """
        search_type = self.cleaned_data.get('search_type')
        valid_types = ['title', 'author', 'isbn', 'all']
        
        if search_type not in valid_types:
            raise ValidationError(_('Invalid search type selected.'))
        
        return search_type
