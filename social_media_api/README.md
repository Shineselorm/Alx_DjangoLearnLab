# Social Media API

A robust REST API for a social media platform built with Django and Django REST Framework. This API provides user authentication, profile management, and social networking features including a follower system.

## Features

- **User Authentication**
  - User registration with email validation
  - Token-based authentication
  - Login/Logout functionality
  - Password validation and security

- **User Profile Management**
  - Custom user model with bio and profile picture
  - View and update user profiles
  - List all users

- **Social Networking**
  - Follow/Unfollow users (generic and by user ID)
  - View followers list
  - View following list
  - Follower count tracking
  - **Personalized Feed** - View posts from followed users

- **Posts & Comments**
  - Create, read, update, and delete posts
  - Comment on posts
  - Search and filter posts
  - Pagination support
  - Author-only editing permissions

- **Likes & Notifications**
  - Like and unlike posts
  - View post likes
  - Automatic notifications for likes
  - Real-time notification system
  - Mark notifications as read
  - Unread notification count

## Technology Stack

- **Django 5.2.6** - Web framework
- **Django REST Framework** - API toolkit
- **Token Authentication** - Secure API access
- **SQLite** - Database (development)

## Project Structure

```
social_media_api/
├── accounts/                  # User authentication and profile management
│   ├── migrations/           # Database migrations
│   ├── __init__.py
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Custom user model
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views
│   ├── urls.py              # URL routing
│   └── tests.py             # Unit tests
├── posts/                     # Posts and Comments functionality
│   ├── migrations/           # Database migrations
│   ├── __init__.py
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Post, Comment, and Like models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views (includes Feed and Likes)
│   ├── urls.py              # URL routing
│   └── tests.py             # Unit tests
├── notifications/             # Notifications functionality
│   ├── migrations/           # Database migrations
│   ├── __init__.py
│   ├── admin.py             # Django admin configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Notification model
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views
│   ├── urls.py              # URL routing
│   └── tests.py             # Unit tests
├── social_media_api/         # Project settings
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── asgi.py
│   └── wsgi.py
├── manage.py                 # Django management script
├── README.md                 # This file
├── API_TESTING_GUIDE.md      # API testing documentation
├── FOLLOW_AND_FEED_DOCUMENTATION.md  # Follow & Feed docs
├── FOLLOW_FEED_IMPLEMENTATION_SUMMARY.md  # Implementation summary
├── LIKES_NOTIFICATIONS_DOCUMENTATION.md  # Likes & Notifications docs
└── LIKES_NOTIFICATIONS_IMPLEMENTATION_SUMMARY.md  # Implementation summary
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
cd /path/to/Alx_DjangoLearnLab/social_media_api
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install django djangorestframework pillow
```

**Required Packages:**
- `django` - Django web framework
- `djangorestframework` - Django REST Framework
- `pillow` - Image processing (for profile pictures)

### Step 4: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### Step 6: Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication Endpoints

#### 1. User Registration
- **URL:** `/api/accounts/register/`
- **Method:** `POST`
- **Authentication:** Not required
- **Request Body:**
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "securepassword123",
  "password_confirm": "securepassword123",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Hello, I'm John!"
}
```
- **Response (201 Created):**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Hello, I'm John!",
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "message": "User registered successfully!"
}
```

#### 2. User Login
- **URL:** `/api/accounts/login/`
- **Method:** `POST`
- **Authentication:** Not required
- **Request Body:**
```json
{
  "username": "johndoe",
  "password": "securepassword123"
}
```
- **Response (200 OK):**
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
  "user": {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  "message": "Login successful!"
}
```

#### 3. User Logout
- **URL:** `/api/accounts/logout/`
- **Method:** `POST`
- **Authentication:** Required (Token)
- **Headers:** `Authorization: Token <your_token>`
- **Response (200 OK):**
```json
{
  "message": "Logged out successfully!"
}
```

### Profile Endpoints

#### 4. View/Update Own Profile
- **URL:** `/api/accounts/profile/`
- **Methods:** `GET`, `PUT`, `PATCH`
- **Authentication:** Required (Token)
- **Headers:** `Authorization: Token <your_token>`
- **GET Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "john@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Hello, I'm John!",
  "profile_picture": "/media/profile_pictures/john.jpg",
  "date_joined": "2024-01-15T10:30:00Z",
  "follower_count": 25,
  "following_count": 30,
  "is_following": false
}
```
- **PUT/PATCH Request Body:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "bio": "Updated bio",
  "email": "newemail@example.com"
}
```

#### 5. View Another User's Profile
- **URL:** `/api/accounts/users/<user_id>/`
- **Method:** `GET`
- **Authentication:** Required (Token)
- **Headers:** `Authorization: Token <your_token>`

#### 6. List All Users
- **URL:** `/api/accounts/users/`
- **Method:** `GET`
- **Authentication:** Required (Token)
- **Headers:** `Authorization: Token <your_token>`
- **Response:**
```json
{
  "count": 50,
  "next": "http://127.0.0.1:8000/api/accounts/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "johndoe",
      "first_name": "John",
      "last_name": "Doe",
      "bio": "Hello, I'm John!",
      "profile_picture": "/media/profile_pictures/john.jpg",
      "follower_count": 25
    },
    ...
  ]
}
```

### Social Networking Endpoints

#### 7. Follow/Unfollow User
- **URL:** `/api/accounts/follow/`
- **Method:** `POST`
- **Authentication:** Required (Token)
- **Headers:** `Authorization: Token <your_token>`
- **Request Body:**
```json
{
  "user_id": 2,
  "action": "follow"  // or "unfollow"
}
```
- **Response (200 OK):**
```json
{
  "message": "You are now following janedoe",
  "following": true
}
```

#### 8. View Followers
- **URL:** `/api/accounts/followers/`
- **Method:** `GET`
- **Authentication:** Required (Token)
- **Headers:** `Authorization: Token <your_token>`
- **Response:**
```json
{
  "count": 25,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "username": "janedoe",
      "first_name": "Jane",
      "last_name": "Doe",
      "bio": "Hi there!",
      "profile_picture": null,
      "follower_count": 30
    },
    ...
  ]
}
```

#### 9. View Following
- **URL:** `/api/accounts/following/`
- **Method:** `GET`
- **Authentication:** Required (Token)
- **Headers:** `Authorization: Token <your_token>`

#### 10. Follow User by ID
- **URL:** `/api/accounts/follow/<user_id>/`
- **Method:** `POST`
- **Authentication:** Required (Token)
- **Headers:** `Authorization: Token <your_token>`
- **Response (200 OK):**
```json
{
  "message": "You are now following janedoe",
  "following": true,
  "user": {
    "id": 2,
    "username": "janedoe"
  }
}
```

#### 11. Unfollow User by ID
- **URL:** `/api/accounts/unfollow/<user_id>/`
- **Method:** `POST`
- **Authentication:** Required (Token)
- **Headers:** `Authorization: Token <your_token>`
- **Response (200 OK):**
```json
{
  "message": "You have unfollowed janedoe",
  "following": false,
  "user": {
    "id": 2,
    "username": "janedoe"
  }
}
```

### Feed Endpoint

#### 12. View Personalized Feed
- **URL:** `/api/feed/`
- **Method:** `GET`
- **Authentication:** Required (Token)
- **Headers:** `Authorization: Token <your_token>`
- **Description:** Returns posts from users you follow, ordered by creation date (newest first)
- **Response (200 OK):**
```json
{
  "count": 25,
  "next": "http://127.0.0.1:8000/api/feed/?page=2",
  "previous": null,
  "following_count": 15,
  "results": [
    {
      "id": 42,
      "author": {
        "id": 2,
        "username": "janedoe",
        "first_name": "Jane",
        "last_name": "Doe",
        "profile_picture": null
      },
      "title": "My Latest Post",
      "content": "This is the content of my post...",
      "created_at": "2025-10-11T12:00:00Z",
      "updated_at": "2025-10-11T12:00:00Z",
      "comment_count": 5
    },
    ...
  ]
}
```

## Testing with Postman

### 1. Register a New User

1. Open Postman
2. Create a new POST request to `http://127.0.0.1:8000/api/accounts/register/`
3. Set Headers: `Content-Type: application/json`
4. Set Body (raw JSON):
```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "testpass123",
  "password_confirm": "testpass123",
  "bio": "Test user bio"
}
```
5. Send request
6. Copy the `token` from the response

### 2. Login

1. Create a new POST request to `http://127.0.0.1:8000/api/accounts/login/`
2. Set Body (raw JSON):
```json
{
  "username": "testuser",
  "password": "testpass123"
}
```
3. Send request
4. Copy the `token` from the response

### 3. Access Protected Endpoints

1. Create a new GET request to `http://127.0.0.1:8000/api/accounts/profile/`
2. Set Headers: `Authorization: Token <paste_your_token_here>`
3. Send request

## Custom User Model

The CustomUser model extends Django's AbstractUser with these additional fields:

```python
class CustomUser(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    followers = models.ManyToManyField('self', symmetrical=False, related_name='following', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Key Features:
- **bio**: User biography (max 500 characters)
- **profile_picture**: User profile image
- **followers**: Many-to-many relationship for follower system (non-symmetrical)
- **Timestamps**: Automatic creation and update tracking

### Helper Methods:
- `get_follower_count()`: Returns number of followers
- `get_following_count()`: Returns number of users being followed
- `follow(user)`: Follow another user
- `unfollow(user)`: Unfollow a user
- `is_following(user)`: Check if following a user
- `is_followed_by(user)`: Check if followed by a user

## Authentication System

The API uses **Token Authentication** provided by Django REST Framework:

1. **Registration**: User registers and receives a token
2. **Login**: User logs in and receives a token
3. **Token Usage**: Include token in Authorization header for all protected endpoints
4. **Token Format**: `Authorization: Token <token_string>`
5. **Logout**: Token is deleted from the database

## Security Features

- Password validation (minimum length, complexity requirements)
- Token-based authentication
- Email uniqueness validation
- Username uniqueness validation
- Secure password storage (hashing)
- CSRF protection
- Rate limiting (100 requests/hour for anonymous, 1000/hour for authenticated users)

## Database Schema

### CustomUser Model
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password`: Hashed password
- `first_name`: User's first name
- `last_name`: User's last name
- `bio`: User biography
- `profile_picture`: Image file
- `followers`: Many-to-many to self
- `created_at`: Timestamp
- `updated_at`: Timestamp
- `is_active`: Boolean
- `is_staff`: Boolean
- `date_joined`: Timestamp

### Token Model (from rest_framework.authtoken)
- `key`: Token string (primary key)
- `user`: Foreign key to CustomUser
- `created`: Timestamp

## Development

### Running Tests

```bash
python manage.py test accounts
```

### Creating Migrations

```bash
python manage.py makemigrations accounts
python manage.py migrate
```

### Accessing Admin Interface

1. Create a superuser: `python manage.py createsuperuser`
2. Navigate to `http://127.0.0.1:8000/admin/`
3. Login with superuser credentials

## API Best Practices

1. **Always include authentication token** for protected endpoints
2. **Use appropriate HTTP methods**: GET (read), POST (create), PUT/PATCH (update), DELETE (delete)
3. **Handle errors gracefully**: Check response status codes
4. **Follow rate limits**: Avoid excessive requests
5. **Validate data**: Ensure required fields are provided
6. **Secure passwords**: Use strong passwords with validation

## Troubleshooting

### Common Issues

1. **"No module named 'rest_framework'"**
   - Solution: `pip install djangorestframework`

2. **"No module named 'PIL'"**
   - Solution: `pip install pillow`

3. **"AUTH_USER_MODEL" error**
   - Solution: Ensure migrations are applied before creating users

4. **Token not working**
   - Solution: Check Authorization header format: `Token <token_string>`

5. **404 on API endpoints**
   - Solution: Ensure URLs are correctly configured and server is running

## Future Enhancements

- [ ] Posts and comments functionality
- [ ] Like and share features
- [ ] Direct messaging
- [ ] Notifications system
- [ ] Search functionality
- [ ] JWT authentication option
- [ ] Email verification
- [ ] Password reset
- [ ] OAuth integration (Google, Facebook)
- [ ] Activity feed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is part of the ALX Django Learning Lab.

## Contact

For questions or support, please contact the development team.

---

**Version:** 1.0.0  
**Last Updated:** 2024-01-15  
**Repository:** Alx_DjangoLearnLab  
**Directory:** social_media_api
