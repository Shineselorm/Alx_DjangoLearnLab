# Advanced Features and Security - Custom User Model Implementation

This project implements a custom user model in Django, extending the default Django user model with additional fields and functionality.

## Features Implemented

### 1. Custom User Model (`accounts.models.CustomUser`)
- Extends Django's `AbstractUser` class
- Additional fields:
  - `date_of_birth`: Date field for user's birth date
  - `profile_photo`: Image field for user's profile picture
- Uses email as the primary username field
- Custom user manager with `create_user` and `create_superuser` methods

### 2. Custom User Manager (`accounts.models.CustomUserManager`)
- Handles user creation with email as primary identifier
- Proper validation for superuser creation
- Supports all custom fields during user creation

### 3. Django Admin Integration (`accounts.admin.CustomUserAdmin`)
- Custom admin interface for the custom user model
- Displays additional fields in list view and forms
- Proper field organization in admin forms
- Search and filter functionality

### 4. Settings Configuration
- `AUTH_USER_MODEL` set to `'accounts.CustomUser'`
- Media file configuration for profile photo uploads
- Accounts app added to `INSTALLED_APPS`

### 5. Application Integration
- Updated existing models to use `get_user_model()`
- Custom user creation form for registration
- Updated views to work with custom user model
- Maintained backward compatibility with existing UserProfile model

## Project Structure

```
advanced_features_and_security/
├── accounts/                          # Custom user model app
│   ├── __init__.py
│   ├── admin.py                       # Custom admin configuration
│   ├── apps.py                        # App configuration
│   ├── models.py                      # Custom user model and manager
│   ├── migrations/
│   │   ├── __init__.py
│   │   └── 0001_initial.py            # Initial migration for CustomUser
│   └── tests.py
├── LibraryProject/
│   ├── relationship_app/
│   │   ├── models.py                  # Updated to use custom user model
│   │   ├── views.py                   # Updated with custom user creation form
│   │   └── migrations/
│   │       └── 0004_alter_userprofile_user.py  # Migration to update UserProfile
│   ├── settings.py                    # Updated with AUTH_USER_MODEL
│   └── urls.py                        # Updated with media file serving
├── manage.py
├── requirements.txt
└── README.md
```

## Key Implementation Details

### Custom User Model
- **Email as Username**: The model uses email as the primary authentication field
- **Additional Fields**: `date_of_birth` and `profile_photo` fields added
- **Manager**: Custom manager ensures proper handling of email-based authentication

### Django Admin
- **Field Organization**: Logical grouping of fields in admin forms
- **Search/Filter**: Email and username search, staff status filtering
- **Read-only Fields**: Date joined and last login are read-only

### Migration Strategy
- Created initial migration for CustomUser model
- Updated existing UserProfile model to reference CustomUser
- Maintained data integrity during transition

### Form Integration
- Custom user creation form with validation
- Password confirmation and validation
- Support for all custom fields in registration

## Usage

1. **User Registration**: Users can register with email, username, and additional fields
2. **Admin Management**: Administrators can manage users through Django admin
3. **Profile Photos**: Users can upload profile photos (served via media files)
4. **Backward Compatibility**: Existing UserProfile functionality maintained

## Security Considerations

- Email uniqueness enforced at model level
- Proper password validation through custom manager
- Media file serving only in development mode
- All Django security best practices maintained

This implementation demonstrates proper Django custom user model practices while maintaining application functionality and security.
