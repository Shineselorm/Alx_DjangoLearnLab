# Posts and Comments API Documentation

## Overview

This document provides comprehensive documentation for the Posts and Comments API endpoints in the Social Media API. The API allows users to create, read, update, and delete posts and comments, with proper authentication and permissions.

---

## Table of Contents

1. [Authentication](#authentication)
2. [Posts API](#posts-api)
3. [Comments API](#comments-api)
4. [Permissions](#permissions)
5. [Filtering and Search](#filtering-and-search)
6. [Pagination](#pagination)
7. [Error Responses](#error-responses)
8. [Testing Guide](#testing-guide)

---

## Authentication

All endpoints except GET requests require authentication using Token Authentication.

### Headers
```http
Authorization: Token <your_token_here>
Content-Type: application/json
```

### Getting a Token
First register or login to get an authentication token:

```bash
# Register
POST /api/accounts/register/

# Login
POST /api/accounts/login/
```

---

## Posts API

### Base URL
```
/api/posts/
```

### Endpoints

#### 1. List All Posts

**Endpoint:** `GET /api/posts/`

**Authentication:** Optional (read-only access without authentication)

**Description:** Retrieves a paginated list of all posts.

**Request:**
```http
GET /api/posts/
```

**Response:** `200 OK`
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/posts/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "author": {
                "id": 1,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "profile_picture": "/media/profile_pictures/john.jpg"
            },
            "title": "My First Post",
            "content": "This is the content of my first post...",
            "created_at": "2024-01-15T10:30:00Z",
            "updated_at": "2024-01-15T10:30:00Z",
            "comment_count": 5
        },
        ...
    ]
}
```

---

#### 2. Create a New Post

**Endpoint:** `POST /api/posts/`

**Authentication:** Required

**Description:** Creates a new post. The authenticated user becomes the author.

**Request:**
```http
POST /api/posts/
Authorization: Token <your_token>
Content-Type: application/json

{
    "title": "Amazing Post Title",
    "content": "This is the content of my amazing post. It can be quite long..."
}
```

**Response:** `201 Created`
```json
{
    "id": 5,
    "author": {
        "id": 1,
        "username": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "profile_picture": "/media/profile_pictures/john.jpg"
    },
    "title": "Amazing Post Title",
    "content": "This is the content of my amazing post. It can be quite long...",
    "created_at": "2024-01-15T15:45:00Z",
    "updated_at": "2024-01-15T15:45:00Z",
    "comment_count": 0,
    "comments": []
}
```

**Validation Errors:** `400 Bad Request`
```json
{
    "title": ["Post title cannot be empty."],
    "content": ["Post content cannot be empty."]
}
```

---

#### 3. Retrieve a Specific Post

**Endpoint:** `GET /api/posts/{id}/`

**Authentication:** Optional

**Description:** Retrieves detailed information about a specific post, including all comments.

**Request:**
```http
GET /api/posts/5/
```

**Response:** `200 OK`
```json
{
    "id": 5,
    "author": {
        "id": 1,
        "username": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "profile_picture": "/media/profile_pictures/john.jpg"
    },
    "title": "Amazing Post Title",
    "content": "This is the content of my amazing post. It can be quite long...",
    "created_at": "2024-01-15T15:45:00Z",
    "updated_at": "2024-01-15T15:45:00Z",
    "comment_count": 2,
    "comments": [
        {
            "id": 1,
            "author": {
                "id": 2,
                "username": "jane_doe",
                "first_name": "Jane",
                "last_name": "Doe",
                "profile_picture": null
            },
            "post": 5,
            "content": "Great post!",
            "created_at": "2024-01-15T16:00:00Z",
            "updated_at": "2024-01-15T16:00:00Z"
        },
        ...
    ]
}
```

**Not Found:** `404 Not Found`
```json
{
    "detail": "Not found."
}
```

---

#### 4. Update a Post

**Endpoint:** `PUT /api/posts/{id}/` or `PATCH /api/posts/{id}/`

**Authentication:** Required (author only)

**Description:** Updates a post. Only the post author can update it.

**Request (Full Update - PUT):**
```http
PUT /api/posts/5/
Authorization: Token <your_token>
Content-Type: application/json

{
    "title": "Updated Post Title",
    "content": "This is the updated content..."
}
```

**Request (Partial Update - PATCH):**
```http
PATCH /api/posts/5/
Authorization: Token <your_token>
Content-Type: application/json

{
    "title": "Updated Post Title"
}
```

**Response:** `200 OK`
```json
{
    "id": 5,
    "author": {
        "id": 1,
        "username": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "profile_picture": "/media/profile_pictures/john.jpg"
    },
    "title": "Updated Post Title",
    "content": "This is the updated content...",
    "created_at": "2024-01-15T15:45:00Z",
    "updated_at": "2024-01-15T17:30:00Z",
    "comment_count": 2,
    "comments": [...]
}
```

**Permission Denied:** `403 Forbidden`
```json
{
    "detail": "You do not have permission to perform this action."
}
```

---

#### 5. Delete a Post

**Endpoint:** `DELETE /api/posts/{id}/`

**Authentication:** Required (author only)

**Description:** Deletes a post. Only the post author can delete it.

**Request:**
```http
DELETE /api/posts/5/
Authorization: Token <your_token>
```

**Response:** `204 No Content`

*(No response body)*

**Permission Denied:** `403 Forbidden`
```json
{
    "detail": "You do not have permission to perform this action."
}
```

---

#### 6. Get Comments for a Post

**Endpoint:** `GET /api/posts/{id}/comments/`

**Authentication:** Optional

**Description:** Retrieves all comments for a specific post.

**Request:**
```http
GET /api/posts/5/comments/
```

**Response:** `200 OK`
```json
[
    {
        "id": 1,
        "author": {
            "id": 2,
            "username": "jane_doe",
            "first_name": "Jane",
            "last_name": "Doe",
            "profile_picture": null
        },
        "post": 5,
        "content": "Great post!",
        "created_at": "2024-01-15T16:00:00Z",
        "updated_at": "2024-01-15T16:00:00Z"
    },
    ...
]
```

---

#### 7. Get My Posts

**Endpoint:** `GET /api/posts/my_posts/`

**Authentication:** Required

**Description:** Retrieves all posts created by the authenticated user.

**Request:**
```http
GET /api/posts/my_posts/
Authorization: Token <your_token>
```

**Response:** `200 OK`
```json
{
    "count": 5,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 5,
            "author": {
                "id": 1,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "profile_picture": "/media/profile_pictures/john.jpg"
            },
            "title": "My Post",
            "content": "Post content...",
            "created_at": "2024-01-15T15:45:00Z",
            "updated_at": "2024-01-15T15:45:00Z",
            "comment_count": 2
        },
        ...
    ]
}
```

---

## Comments API

### Base URL
```
/api/comments/
```

### Endpoints

#### 1. List All Comments

**Endpoint:** `GET /api/comments/`

**Authentication:** Optional

**Description:** Retrieves a paginated list of all comments.

**Request:**
```http
GET /api/comments/
```

**Response:** `200 OK`
```json
{
    "count": 50,
    "next": "http://localhost:8000/api/comments/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "post": 5,
            "author": {
                "id": 2,
                "username": "jane_doe",
                "first_name": "Jane",
                "last_name": "Doe",
                "profile_picture": null
            },
            "content": "Great post!",
            "created_at": "2024-01-15T16:00:00Z",
            "updated_at": "2024-01-15T16:00:00Z"
        },
        ...
    ]
}
```

---

#### 2. Create a Comment

**Endpoint:** `POST /api/comments/`

**Authentication:** Required

**Description:** Creates a new comment on a post. The authenticated user becomes the author.

**Request:**
```http
POST /api/comments/
Authorization: Token <your_token>
Content-Type: application/json

{
    "post": 5,
    "content": "This is my comment on the post!"
}
```

**Response:** `201 Created`
```json
{
    "id": 10,
    "post": 5,
    "author": {
        "id": 1,
        "username": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "profile_picture": "/media/profile_pictures/john.jpg"
    },
    "content": "This is my comment on the post!",
    "created_at": "2024-01-15T18:00:00Z",
    "updated_at": "2024-01-15T18:00:00Z"
}
```

**Validation Errors:** `400 Bad Request`
```json
{
    "content": ["Comment content cannot be empty."],
    "post": ["This field is required."]
}
```

---

#### 3. Retrieve a Specific Comment

**Endpoint:** `GET /api/comments/{id}/`

**Authentication:** Optional

**Description:** Retrieves detailed information about a specific comment.

**Request:**
```http
GET /api/comments/10/
```

**Response:** `200 OK`
```json
{
    "id": 10,
    "post": 5,
    "author": {
        "id": 1,
        "username": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "profile_picture": "/media/profile_pictures/john.jpg"
    },
    "content": "This is my comment on the post!",
    "created_at": "2024-01-15T18:00:00Z",
    "updated_at": "2024-01-15T18:00:00Z"
}
```

---

#### 4. Update a Comment

**Endpoint:** `PUT /api/comments/{id}/` or `PATCH /api/comments/{id}/`

**Authentication:** Required (author only)

**Description:** Updates a comment. Only the comment author can update it.

**Request:**
```http
PATCH /api/comments/10/
Authorization: Token <your_token>
Content-Type: application/json

{
    "content": "Updated comment content!"
}
```

**Response:** `200 OK`
```json
{
    "id": 10,
    "post": 5,
    "author": {
        "id": 1,
        "username": "john_doe",
        "first_name": "John",
        "last_name": "Doe",
        "profile_picture": "/media/profile_pictures/john.jpg"
    },
    "content": "Updated comment content!",
    "created_at": "2024-01-15T18:00:00Z",
    "updated_at": "2024-01-15T18:30:00Z"
}
```

---

#### 5. Delete a Comment

**Endpoint:** `DELETE /api/comments/{id}/`

**Authentication:** Required (author only)

**Description:** Deletes a comment. Only the comment author can delete it.

**Request:**
```http
DELETE /api/comments/10/
Authorization: Token <your_token>
```

**Response:** `204 No Content`

---

#### 6. Get My Comments

**Endpoint:** `GET /api/comments/my_comments/`

**Authentication:** Required

**Description:** Retrieves all comments created by the authenticated user.

**Request:**
```http
GET /api/comments/my_comments/
Authorization: Token <your_token>
```

**Response:** `200 OK`
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 10,
            "post": 5,
            "author": {
                "id": 1,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "profile_picture": "/media/profile_pictures/john.jpg"
            },
            "content": "My comment",
            "created_at": "2024-01-15T18:00:00Z",
            "updated_at": "2024-01-15T18:00:00Z"
        },
        ...
    ]
}
```

---

## Permissions

### Post Permissions
- **Create:** Authenticated users only
- **Read:** Anyone (authenticated or not)
- **Update:** Author only
- **Delete:** Author only

### Comment Permissions
- **Create:** Authenticated users only
- **Read:** Anyone (authenticated or not)
- **Update:** Author only
- **Delete:** Author only

---

## Filtering and Search

### Posts Filtering

#### Search by Title or Content
```http
GET /api/posts/?search=django
```

#### Filter by Author Username
```http
GET /api/posts/?author=john_doe
```

#### Search with Query Parameter
```http
GET /api/posts/?q=tutorial
```

#### Order Results
```http
# Most recent first (default)
GET /api/posts/?ordering=-created_at

# Oldest first
GET /api/posts/?ordering=created_at

# Alphabetical by title
GET /api/posts/?ordering=title
```

### Comments Filtering

#### Filter by Post ID
```http
GET /api/comments/?post=5
```

#### Filter by Author Username
```http
GET /api/comments/?author=jane_doe
```

#### Search Comment Content
```http
GET /api/comments/?search=great
```

#### Order Results
```http
# Oldest first (default - chronological)
GET /api/comments/?ordering=created_at

# Most recent first
GET /api/comments/?ordering=-created_at
```

### Combined Filters

You can combine multiple filters:
```http
GET /api/posts/?author=john_doe&search=django&ordering=-created_at
```

---

## Pagination

All list endpoints are paginated with **10 items per page** by default.

### Pagination Parameters

```http
# Get first page (default)
GET /api/posts/

# Get specific page
GET /api/posts/?page=2

# Pagination response includes:
{
    "count": 25,           # Total number of items
    "next": "url",         # URL for next page (null if last page)
    "previous": "url",     # URL for previous page (null if first page)
    "results": [...]       # Array of items on current page
}
```

---

## Error Responses

### 400 Bad Request
```json
{
    "field_name": ["Error message for this field."]
}
```

### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### 500 Internal Server Error
```json
{
    "detail": "An error occurred while processing your request."
}
```

---

## Testing Guide

### Using cURL

#### Create a Post
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Post",
    "content": "This is a test post content."
  }'
```

#### List Posts
```bash
curl -X GET http://localhost:8000/api/posts/
```

#### Create a Comment
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "This is a test comment."
  }'
```

#### Update a Post
```bash
curl -X PATCH http://localhost:8000/api/posts/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Title"
  }'
```

#### Delete a Post
```bash
curl -X DELETE http://localhost:8000/api/posts/1/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Using Python Requests

```python
import requests

# Base URL
BASE_URL = "http://localhost:8000/api"

# Get token (login first)
response = requests.post(f"{BASE_URL}/accounts/login/", json={
    "username": "your_username",
    "password": "your_password"
})
token = response.json()['token']

# Set headers
headers = {
    "Authorization": f"Token {token}",
    "Content-Type": "application/json"
}

# Create a post
response = requests.post(f"{BASE_URL}/posts/", 
    json={
        "title": "My Post",
        "content": "Post content"
    },
    headers=headers
)
print(response.json())

# List posts
response = requests.get(f"{BASE_URL}/posts/")
print(response.json())

# Create a comment
response = requests.post(f"{BASE_URL}/comments/",
    json={
        "post": 1,
        "content": "My comment"
    },
    headers=headers
)
print(response.json())
```

---

## Complete API Endpoint Summary

| Method | Endpoint | Auth Required | Description |
|--------|----------|---------------|-------------|
| GET | `/api/posts/` | No | List all posts |
| POST | `/api/posts/` | Yes | Create a new post |
| GET | `/api/posts/{id}/` | No | Get specific post details |
| PUT/PATCH | `/api/posts/{id}/` | Yes (Author) | Update a post |
| DELETE | `/api/posts/{id}/` | Yes (Author) | Delete a post |
| GET | `/api/posts/{id}/comments/` | No | Get all comments for a post |
| GET | `/api/posts/my_posts/` | Yes | Get authenticated user's posts |
| GET | `/api/comments/` | No | List all comments |
| POST | `/api/comments/` | Yes | Create a new comment |
| GET | `/api/comments/{id}/` | No | Get specific comment details |
| PUT/PATCH | `/api/comments/{id}/` | Yes (Author) | Update a comment |
| DELETE | `/api/comments/{id}/` | Yes (Author) | Delete a comment |
| GET | `/api/comments/my_comments/` | Yes | Get authenticated user's comments |

---

## Support and Additional Resources

- **Main API Documentation:** `README.md`
- **Accounts API Documentation:** `API_TESTING_GUIDE.md`
- **GitHub Repository:** [Alx_DjangoLearnLab](https://github.com/Shineselorm/Alx_DjangoLearnLab)
- **Project Directory:** `social_media_api`

---

**Last Updated:** October 11, 2025  
**Version:** 1.0.0  
**API Base URL:** `http://localhost:8000/api/`

