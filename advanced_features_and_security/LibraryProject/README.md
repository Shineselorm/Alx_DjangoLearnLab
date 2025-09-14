# LibraryProject - Django Advanced Features and Security

## Overview

This Django project demonstrates advanced features including custom user models, permissions, and groups management. The project implements a comprehensive bookshelf application with role-based access control.

## Project Structure

```
LibraryProject/
├── LibraryProject/              # Django project settings
│   ├── __init__.py
│   ├── settings.py             # Project settings with custom user model
│   ├── urls.py                 # Main URL configuration
│   ├── wsgi.py
│   └── asgi.py
├── bookshelf/                  # Main application with custom user model
│   ├── models.py              # CustomUser model and bookshelf models
│   ├── views.py               # Views with permission enforcement
│   ├── admin.py               # Admin configuration
│   ├── urls.py                # App URL patterns
│   ├── management/
│   │   └── commands/          # Custom management commands
│   └── migrations/            # Database migrations
├── relationship_app/           # Original relationship models
│   ├── models.py              # Models using custom user model
│   ├── views.py               # Views with custom user forms
│   └── templates/             # HTML templates
└── README.md                  # This file
```

## Features Implemented

### 1. Custom User Model

**Location**: `bookshelf/models.py`

The project implements a custom user model that extends Django's `AbstractUser`:

```python
class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField(_('date of birth'), null=True, blank=True)
    profile_photo = models.ImageField(
        _('profile photo'), 
        upload_to='profile_photos/', 
        null=True, 
        blank=True
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
```

**Key Features**:
- Email-based authentication
- Additional fields: `date_of_birth` and `profile_photo`
- Custom user manager with proper validation
- Admin integration

### 2. Permissions and Groups System

**Location**: `bookshelf/models.py`, `bookshelf/views.py`

The project implements a comprehensive permissions system:

#### Custom Permissions
- `can_view`: View content
- `can_create`: Create content
- `can_edit`: Edit content
- `can_delete`: Delete content

#### User Groups
- **Viewers**: Read-only access (`can_view` only)
- **Editors**: Content creation and editing (`can_view`, `can_create`, `can_edit`)
- **Admins**: Full access (all permissions)

#### Permission Enforcement
All views are protected using Django's permission decorators:

```python
@permission_required('LibraryProject.bookshelf.can_view', raise_exception=True)
def book_list(request):
    """Display a list of all books."""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
```

### 3. Models and Relationships

**Bookshelf Models**:
- `Book`: Book information with custom user relationship
- `BookReview`: User reviews with rating system
- `ReadingList`: User-created reading lists
- `UserProfile`: Extended user profile information

**Key Relationships**:
- Books linked to users who added them
- Reviews linked to both books and users
- Reading lists owned by users with many-to-many book relationships

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Database Setup

```bash
# Create and apply migrations
python manage.py makemigrations
python manage.py migrate

# Set up groups and permissions
python manage.py setup_groups_permissions

# Create test users
python manage.py create_test_users
```

### 3. Create Superuser

```bash
python manage.py create_custom_superuser \
    --email admin@example.com \
    --username admin \
    --password admin123
```

## Usage

### Management Commands

#### Setup Groups and Permissions
```bash
python manage.py setup_groups_permissions
```
Creates Viewers, Editors, and Admins groups with appropriate permissions.

#### Create Test Users
```bash
python manage.py create_test_users
```
Creates test users for each group:
- `viewer@example.com` / `viewer123` (Viewers)
- `editor@example.com` / `editor123` (Editors)
- `admin@example.com` / `admin123` (Admins)

### Testing Permissions

1. **Login as Viewer**:
   - Can view books, reviews, and reading lists
   - Cannot create, edit, or delete content

2. **Login as Editor**:
   - Can view, create, and edit content
   - Cannot delete content

3. **Login as Admin**:
   - Full access to all operations

### URL Patterns

The bookshelf application provides these protected URLs:

```
/bookshelf/                          # Book list (can_view)
/bookshelf/book/<id>/                # Book detail (can_view)
/bookshelf/add-book/                 # Add book (can_create)
/bookshelf/book/<id>/edit/           # Edit book (can_edit)
/bookshelf/book/<id>/delete/         # Delete book (can_delete)
/bookshelf/book/<id>/add-review/     # Add review (can_create)
/bookshelf/review/<id>/edit/         # Edit review (can_edit)
/bookshelf/review/<id>/delete/       # Delete review (can_delete)
/bookshelf/my-reading-lists/         # My reading lists (can_view)
/bookshelf/create-reading-list/      # Create reading list (can_create)
/bookshelf/public-reading-lists/     # Public reading lists (can_view)
```

## Configuration

### Settings

**Custom User Model**:
```python
AUTH_USER_MODEL = 'LibraryProject.bookshelf.CustomUser'
```

**Media Files**:
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

### Admin Interface

The custom user model is fully integrated with Django admin:
- Custom admin class with organized field layout
- Search and filter functionality
- Proper form organization for user creation and editing

## Security Features

### Permission System
- Principle of least privilege
- Group-based access control
- Explicit permission checks on all sensitive operations
- Graceful error handling for permission denials

### User Management
- Email-based authentication
- Secure password handling
- Profile photo upload with proper validation
- Extended user profiles

## Testing

### Automated Tests

Run the test suite:
```bash
python manage.py test LibraryProject.bookshelf.tests_permissions
```

### Manual Testing

1. Create groups and permissions: `python manage.py setup_groups_permissions`
2. Create test users: `python manage.py create_test_users`
3. Login with different user accounts and test permissions
4. Verify that users can only access allowed functionality

## Documentation

- **Main Documentation**: `../README.md` - Project overview and implementation details
- **Permissions Guide**: `../PERMISSIONS_GROUPS_GUIDE.md` - Detailed permissions system documentation
- **Implementation Summary**: `../IMPLEMENTATION_SUMMARY.md` - Complete feature summary

## Development

### Adding New Permissions

1. Define in model Meta class:
```python
permissions = [
    ("new_permission", "Description of new permission"),
]
```

2. Create migration:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Update groups in `setup_groups_permissions.py`

4. Protect views:
```python
@permission_required('app.new_permission', raise_exception=True)
def new_view(request):
    # Implementation
```

### Extending Models

All models properly use the custom user model via `get_user_model()`:
```python
from django.contrib.auth import get_user_model
User = get_user_model()
```

## Requirements

- Django 5.2.6
- Python 3.10+
- SQLite (default) or other supported database

## License

This project is part of the ALX Django Learning Lab curriculum.
