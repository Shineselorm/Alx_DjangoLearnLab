from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, Book, BookReview, ReadingList, UserProfile


class CustomUserAdmin(BaseUserAdmin):
    """
    Admin configuration for the CustomUser model.
    """
    # Fields to display in the list view
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_staff', 'date_of_birth')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    # Search functionality
    search_fields = ('email', 'username', 'first_name', 'last_name')
    
    # Ordering
    ordering = ('email',)
    
    # Fields for the user creation/edit form
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields for the add user form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
        (_('Personal info'), {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'date_of_birth', 'profile_photo')
        }),
        (_('Permissions'), {
            'classes': ('wide',),
            'fields': ('is_active', 'is_staff', 'is_superuser'),
        }),
    )
    
    # Read-only fields
    readonly_fields = ('date_joined', 'last_login')


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


# Register the CustomUser model with the custom admin class
admin.site.register(CustomUser, CustomUserAdmin)
