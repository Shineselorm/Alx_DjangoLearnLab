from django.contrib import admin
from .models import Book, BookReview, ReadingList, UserProfile


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'publication_date', 'added_by', 'created_at')
    list_filter = ('publication_date', 'created_at', 'author')
    search_fields = ('title', 'author', 'isbn')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('added_by',)


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'reviewer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'reviewer__email', 'review_text')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('book', 'reviewer')


@admin.register(ReadingList)
class ReadingListAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_public', 'books_count', 'created_at')
    list_filter = ('is_public', 'created_at')
    search_fields = ('name', 'owner__email', 'description')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('owner',)
    filter_horizontal = ('books',)

    def books_count(self, obj):
        return obj.books.count()
    books_count.short_description = 'Number of Books'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'reading_goal_books', 'reading_goal_pages', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__email', 'bio', 'favorite_genres')
    readonly_fields = ('created_at', 'updated_at')
    raw_id_fields = ('user',)
