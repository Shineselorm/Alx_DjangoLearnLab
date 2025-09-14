from django.db import models
from django.contrib.auth import get_user_model

# Get the custom user model
User = get_user_model()


class Book(models.Model):
    """
    Book model that demonstrates integration with the custom user model.
    """
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    publication_date = models.DateField()
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books_added')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        return f"{self.title} by {self.author}"


class BookReview(models.Model):
    """
    Book review model that uses the custom user model.
    """
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_reviews')
    rating = models.IntegerField(choices=RATING_CHOICES)
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ['book', 'reviewer']  # One review per user per book
        verbose_name = 'Book Review'
        verbose_name_plural = 'Book Reviews'

    def __str__(self):
        return f"{self.reviewer.email}'s review of {self.book.title}"


class ReadingList(models.Model):
    """
    Reading list model that demonstrates many-to-many relationships with custom user model.
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_lists')
    books = models.ManyToManyField(Book, related_name='reading_lists', blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Reading List'
        verbose_name_plural = 'Reading Lists'

    def __str__(self):
        return f"{self.owner.email}'s {self.name}"


class UserProfile(models.Model):
    """
    Extended user profile that works with the custom user model.
    This demonstrates how to extend user functionality beyond the custom user model.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='extended_profile')
    bio = models.TextField(max_length=500, blank=True)
    favorite_genres = models.CharField(max_length=200, blank=True)
    reading_goal_books = models.IntegerField(default=0)
    reading_goal_pages = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Extended User Profile'
        verbose_name_plural = 'Extended User Profiles'

    def __str__(self):
        return f"{self.user.email}'s extended profile"
