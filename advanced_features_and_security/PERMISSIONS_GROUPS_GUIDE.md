# Django Permissions and Groups Implementation Guide

## Overview

This project implements a comprehensive permissions and groups system using Django's built-in authentication framework. The system controls access to various parts of the bookshelf application based on user roles and their assigned permissions.

## Custom Permissions

### Defined Permissions

The following custom permissions have been defined in the models:

#### Book Model Permissions (`LibraryProject/bookshelf.models.Book`)
- `can_view`: Can view books
- `can_create`: Can create books
- `can_edit`: Can edit books
- `can_delete`: Can delete books

#### BookReview Model Permissions (`LibraryProject/bookshelf.models.BookReview`)
- `can_view`: Can view book reviews
- `can_create`: Can create book reviews
- `can_edit`: Can edit book reviews
- `can_delete`: Can delete book reviews

#### ReadingList Model Permissions (`LibraryProject/bookshelf.models.ReadingList`)
- `can_view`: Can view reading lists
- `can_create`: Can create reading lists
- `can_edit`: Can edit reading lists
- `can_delete`: Can delete reading lists

### Implementation in Models

```python
class Meta:
    permissions = [
        ("can_view", "Can view books"),
        ("can_create", "Can create books"),
        ("can_edit", "Can edit books"),
        ("can_delete", "Can delete books"),
    ]
```

## User Groups

### Group Hierarchy

#### 1. Viewers Group
- **Purpose**: Read-only access to the application
- **Permissions**: 
  - All `can_view` permissions
- **Use Case**: Users who can browse content but cannot modify it

#### 2. Editors Group
- **Purpose**: Content creation and modification
- **Permissions**:
  - All `can_view` permissions
  - All `can_create` permissions
  - All `can_edit` permissions
- **Use Case**: Content creators and moderators

#### 3. Admins Group
- **Purpose**: Full administrative access
- **Permissions**:
  - All permissions (view, create, edit, delete)
- **Use Case**: System administrators

### Group Setup

Groups are automatically created and configured using the management command:

```bash
python manage.py setup_groups_permissions
```

## Permission Enforcement in Views

### Decorator Usage

Views are protected using Django's `@permission_required` decorator:

```python
@permission_required('LibraryProject.bookshelf.can_view', raise_exception=True)
def book_list(request):
    """Display a list of all books."""
    books = Book.objects.all()
    return render(request, 'bookshelf/book_list.html', {'books': books})
```

### View Protection Examples

#### View Operations (can_view)
- `book_list()`: List all books
- `book_detail()`: View book details
- `my_reading_lists()`: View user's reading lists
- `public_reading_lists()`: View public reading lists

#### Create Operations (can_create)
- `add_book()`: Create new books
- `add_review()`: Create book reviews
- `create_reading_list()`: Create reading lists

#### Edit Operations (can_edit)
- `edit_book()`: Modify book information
- `edit_review()`: Update book reviews

#### Delete Operations (can_delete)
- `delete_book()`: Remove books
- `delete_review()`: Remove book reviews

## Testing the Implementation

### Test Users

The system includes pre-configured test users for each group:

#### Viewer User
- **Email**: viewer@example.com
- **Password**: viewer123
- **Group**: Viewers
- **Can Do**: View books, reviews, and reading lists
- **Cannot Do**: Create, edit, or delete content

#### Editor User
- **Email**: editor@example.com
- **Password**: editor123
- **Group**: Editors
- **Can Do**: View, create, and edit content
- **Cannot Do**: Delete content

#### Admin User
- **Email**: admin@example.com
- **Password**: admin123
- **Group**: Admins
- **Can Do**: All operations (view, create, edit, delete)

### Creating Test Users

Run the management command to create test users:

```bash
python manage.py create_test_users
```

### Manual Testing Steps

1. **Setup Groups and Permissions**:
   ```bash
   python manage.py setup_groups_permissions
   ```

2. **Create Test Users**:
   ```bash
   python manage.py create_test_users
   ```

3. **Test Permission Enforcement**:
   - Log in as viewer@example.com
   - Try to access `/bookshelf/` (should work - can_view)
   - Try to access `/bookshelf/add-book/` (should fail - no can_create)
   
   - Log in as editor@example.com
   - Try to access `/bookshelf/add-book/` (should work - can_create)
   - Try to access `/bookshelf/book/1/delete/` (should fail - no can_delete)
   
   - Log in as admin@example.com
   - All operations should work (full permissions)

## Management Commands

### setup_groups_permissions.py

Creates and configures user groups with appropriate permissions:

```bash
python manage.py setup_groups_permissions
```

**What it does**:
- Creates Viewers, Editors, and Admins groups
- Assigns appropriate permissions to each group
- Provides feedback on the setup process

### create_test_users.py

Creates test users and assigns them to groups:

```bash
python manage.py create_test_users
```

**What it does**:
- Creates three test users (viewer, editor, admin)
- Assigns users to appropriate groups
- Sets default passwords for testing

## URL Structure

The bookshelf application provides the following protected URLs:

```
/bookshelf/                          # Book list (can_view)
/bookshelf/book/<id>/                # Book detail (can_view)
/bookshelf/book/<id>/add-review/     # Add review (can_create)
/bookshelf/book/<id>/edit/           # Edit book (can_edit)
/bookshelf/book/<id>/delete/         # Delete book (can_delete)
/bookshelf/add-book/                 # Add book (can_create)
/bookshelf/my-reading-lists/         # My reading lists (can_view)
/bookshelf/create-reading-list/      # Create reading list (can_create)
/bookshelf/public-reading-lists/     # Public reading lists (can_view)
/bookshelf/review/<id>/edit/         # Edit review (can_edit)
/bookshelf/review/<id>/delete/       # Delete review (can_delete)
```

## Error Handling

### Permission Denied

When users lack required permissions, Django raises `PermissionDenied` exception:

- **HTTP Status**: 403 Forbidden
- **User Experience**: Clear error message indicating insufficient permissions
- **Logging**: Permission denials are logged for security monitoring

### Graceful Degradation

- Users without view permissions cannot access content
- Users without create permissions see no "Add" buttons
- Users without edit permissions see no "Edit" buttons
- Users without delete permissions see no "Delete" buttons

## Security Considerations

### Best Practices Implemented

1. **Principle of Least Privilege**: Users get minimum required permissions
2. **Explicit Permission Checks**: All sensitive operations are protected
3. **Group-Based Access Control**: Permissions managed through groups
4. **Audit Trail**: All permission changes are logged
5. **Regular Testing**: Automated test suite for permission enforcement

### Permission Validation

- All views use `@permission_required` decorator with `raise_exception=True`
- Template context includes permission checks for UI elements
- API endpoints validate permissions before processing requests

## Maintenance

### Adding New Permissions

1. **Define in Model**:
   ```python
   class Meta:
       permissions = [
           ("new_permission", "Description of new permission"),
       ]
   ```

2. **Create Migration**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Update Groups**:
   - Modify `setup_groups_permissions.py`
   - Run the command to update group permissions

4. **Protect Views**:
   ```python
   @permission_required('app.new_permission', raise_exception=True)
   def new_view(request):
       # View implementation
   ```

### Monitoring Permissions

- Django admin provides interface for managing groups and permissions
- Log files track permission denials
- User activity can be monitored through Django's logging framework

This implementation provides a robust, scalable permissions system that can be easily extended and maintained.
