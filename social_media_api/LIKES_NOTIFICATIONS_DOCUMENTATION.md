# Likes and Notifications - API Documentation

## Overview

This document provides comprehensive documentation for the Likes and Notifications functionality in the Social Media API. Users can like posts and receive notifications for various interactions such as new followers, likes on their posts, and comments.

---

## Table of Contents

1. [Models](#models)
2. [Like Endpoints](#like-endpoints)
3. [Notification Endpoints](#notification-endpoints)
4. [Testing Guide](#testing-guide)
5. [Complete Examples](#complete-examples)

---

## Models

### Like Model

**File:** `posts/models.py`

```python
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'post']  # A user can only like a post once
```

**Features:**
- User can like a post
- Unique constraint prevents double-liking
- Automatic timestamp tracking

---

### Notification Model

**File:** `notifications/models.py`

```python
class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    verb = models.CharField(max_length=255)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_object_id = models.PositiveIntegerField()
    target = GenericForeignKey('target_content_type', 'target_object_id')
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
```

**Features:**
- Generic foreign key to any model
- Read/unread status
- Actor-recipient relationship
- Automatic timestamp tracking

---

## Like Endpoints

### 1. Like a Post

**Endpoint:** `POST /api/posts/<pk>/like/`

**Authentication:** Required

**Description:** Like a specific post. Creates a notification for the post author.

**Request:**
```http
POST /api/posts/5/like/
Authorization: Token <your_token>
```

**Response:** `201 CREATED`
```json
{
    "message": "You liked \"My Awesome Post\"",
    "like": {
        "id": 1,
        "user": {
            "id": 2,
            "username": "john_doe",
            "first_name": "John",
            "last_name": "Doe",
            "profile_picture": null
        },
        "post": 5,
        "post_title": "My Awesome Post",
        "created_at": "2025-10-11T14:30:00Z"
    },
    "like_count": 15
}
```

**Error Response:** `400 BAD REQUEST`
```json
{
    "error": "You have already liked this post."
}
```

---

### 2. Unlike a Post

**Endpoint:** `POST /api/posts/<pk>/unlike/`

**Authentication:** Required

**Description:** Remove your like from a post.

**Request:**
```http
POST /api/posts/5/unlike/
Authorization: Token <your_token>
```

**Response:** `200 OK`
```json
{
    "message": "You unliked \"My Awesome Post\"",
    "like_count": 14
}
```

**Error Response:** `400 BAD REQUEST`
```json
{
    "error": "You have not liked this post."
}
```

---

### 3. Get Post Likes

**Endpoint:** `GET /api/posts/<pk>/likes/`

**Authentication:** Optional (Read-only for unauthenticated)

**Description:** Get a list of all users who liked a specific post.

**Request:**
```http
GET /api/posts/5/likes/
Authorization: Token <your_token>
```

**Response:** `200 OK`
```json
{
    "count": 15,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user": {
                "id": 2,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "profile_picture": null
            },
            "post": 5,
            "post_title": "My Awesome Post",
            "created_at": "2025-10-11T14:30:00Z"
        },
        ...
    ]
}
```

---

## Notification Endpoints

### 1. Get All Notifications

**Endpoint:** `GET /api/notifications/`

**Authentication:** Required

**Description:** Retrieve all notifications for the authenticated user.

**Query Parameters:**
- `read` (optional): Filter by read status (`true` or `false`)

**Request:**
```http
GET /api/notifications/
Authorization: Token <your_token>
```

**Response:** `200 OK`
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/notifications/?page=2",
    "previous": null,
    "unread_count": 5,
    "results": [
        {
            "id": 1,
            "recipient": 1,
            "actor": {
                "id": 2,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "profile_picture": null
            },
            "verb": "liked your post",
            "target_type": "post",
            "target_object_id": 5,
            "timestamp": "2025-10-11T14:30:00Z",
            "read": false
        },
        {
            "id": 2,
            "recipient": 1,
            "actor": {
                "id": 3,
                "username": "jane_smith",
                "first_name": "Jane",
                "last_name": "Smith",
                "profile_picture": null
            },
            "verb": "started following you",
            "target_type": null,
            "target_object_id": null,
            "timestamp": "2025-10-11T13:15:00Z",
            "read": false
        },
        ...
    ]
}
```

---

### 2. Get Unread Notifications Only

**Endpoint:** `GET /api/notifications/unread/`

**Authentication:** Required

**Description:** Retrieve only unread notifications.

**Request:**
```http
GET /api/notifications/unread/
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
            "id": 1,
            "recipient": 1,
            "actor": {
                "id": 2,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "profile_picture": null
            },
            "verb": "liked your post",
            "target_type": "post",
            "target_object_id": 5,
            "timestamp": "2025-10-11T14:30:00Z",
            "read": false
        },
        ...
    ]
}
```

---

### 3. Mark Notification as Read

**Endpoint:** `POST /api/notifications/<pk>/read/`

**Authentication:** Required

**Description:** Mark a specific notification as read.

**Request:**
```http
POST /api/notifications/1/read/
Authorization: Token <your_token>
```

**Response:** `200 OK`
```json
{
    "message": "Notification marked as read",
    "notification": {
        "id": 1,
        "recipient": 1,
        "actor": {
            "id": 2,
            "username": "john_doe",
            "first_name": "John",
            "last_name": "Doe",
            "profile_picture": null
        },
        "verb": "liked your post",
        "target_type": "post",
        "target_object_id": 5,
        "timestamp": "2025-10-11T14:30:00Z",
        "read": true
    }
}
```

---

### 4. Mark All Notifications as Read

**Endpoint:** `POST /api/notifications/mark-all-read/`

**Authentication:** Required

**Description:** Mark all user notifications as read.

**Request:**
```http
POST /api/notifications/mark-all-read/
Authorization: Token <your_token>
```

**Response:** `200 OK`
```json
{
    "message": "5 notifications marked as read",
    "updated_count": 5
}
```

---

### 5. Delete Notification

**Endpoint:** `DELETE /api/notifications/<pk>/`

**Authentication:** Required

**Description:** Delete a specific notification.

**Request:**
```http
DELETE /api/notifications/1/
Authorization: Token <your_token>
```

**Response:** `204 NO CONTENT`
```json
{
    "message": "Notification deleted successfully"
}
```

---

## Testing Guide

### Test Scenario 1: Like a Post

```bash
# Login to get token
TOKEN=$(curl -s -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}' \
  | jq -r '.token')

# Like a post
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Token $TOKEN"
```

**Expected Result:**
```json
{
    "message": "You liked \"Post Title\"",
    "like": {...},
    "like_count": 1
}
```

---

### Test Scenario 2: View Notifications

```bash
# Get all notifications
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Token $TOKEN"

# Get only unread notifications
curl -X GET http://localhost:8000/api/notifications/unread/ \
  -H "Authorization: Token $TOKEN"
```

**Expected Result:**
- List of notifications
- Unread count included
- Recent notifications first

---

### Test Scenario 3: Mark Notifications as Read

```bash
# Mark single notification as read
curl -X POST http://localhost:8000/api/notifications/1/read/ \
  -H "Authorization: Token $TOKEN"

# Mark all notifications as read
curl -X POST http://localhost:8000/api/notifications/mark-all-read/ \
  -H "Authorization: Token $TOKEN"
```

**Expected Result:**
- Notification read status updated
- Updated count returned

---

### Test Scenario 4: Unlike a Post

```bash
# Unlike a post
curl -X POST http://localhost:8000/api/posts/1/unlike/ \
  -H "Authorization: Token $TOKEN"
```

**Expected Result:**
```json
{
    "message": "You unliked \"Post Title\"",
    "like_count": 0
}
```

---

## Complete Examples

### Python Example: Complete Like and Notification Workflow

```python
import requests

BASE_URL = "http://localhost:8000/api"

class SocialMediaClient:
    def __init__(self, token):
        self.token = token
        self.headers = {
            "Authorization": f"Token {token}",
            "Content-Type": "application/json"
        }
    
    def like_post(self, post_id):
        """Like a post"""
        response = requests.post(
            f"{BASE_URL}/posts/{post_id}/like/",
            headers=self.headers
        )
        return response.json()
    
    def unlike_post(self, post_id):
        """Unlike a post"""
        response = requests.post(
            f"{BASE_URL}/posts/{post_id}/unlike/",
            headers=self.headers
        )
        return response.json()
    
    def get_post_likes(self, post_id):
        """Get all likes on a post"""
        response = requests.get(
            f"{BASE_URL}/posts/{post_id}/likes/",
            headers=self.headers
        )
        return response.json()
    
    def get_notifications(self, unread_only=False):
        """Get notifications"""
        endpoint = "/notifications/unread/" if unread_only else "/notifications/"
        response = requests.get(
            f"{BASE_URL}{endpoint}",
            headers=self.headers
        )
        return response.json()
    
    def mark_notification_read(self, notification_id):
        """Mark a notification as read"""
        response = requests.post(
            f"{BASE_URL}/notifications/{notification_id}/read/",
            headers=self.headers
        )
        return response.json()
    
    def mark_all_notifications_read(self):
        """Mark all notifications as read"""
        response = requests.post(
            f"{BASE_URL}/notifications/mark-all-read/",
            headers=self.headers
        )
        return response.json()

# Usage
client = SocialMediaClient("your_token_here")

# Like a post
result = client.like_post(1)
print(f"✅ {result['message']}")

# View notifications
notifications = client.get_notifications(unread_only=True)
print(f"📬 You have {notifications['count']} unread notifications")

# Display notifications
for notif in notifications['results']:
    actor = notif['actor']['username']
    verb = notif['verb']
    print(f"  - {actor} {verb}")

# Mark all as read
result = client.mark_all_notifications_read()
print(f"✅ {result['message']}")
```

---

### cURL Complete Workflow

```bash
# 1. Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}' \
  | jq -r '.token')

echo "Token: $TOKEN"

# 2. Like some posts
curl -X POST http://localhost:8000/api/posts/1/like/ \
  -H "Authorization: Token $TOKEN"

curl -X POST http://localhost:8000/api/posts/2/like/ \
  -H "Authorization: Token $TOKEN"

# 3. View who liked a post
curl -X GET http://localhost:8000/api/posts/1/likes/ \
  -H "Authorization: Token $TOKEN"

# 4. View your notifications
curl -X GET http://localhost:8000/api/notifications/ \
  -H "Authorization: Token $TOKEN"

# 5. View only unread notifications
curl -X GET http://localhost:8000/api/notifications/unread/ \
  -H "Authorization: Token $TOKEN"

# 6. Mark all as read
curl -X POST http://localhost:8000/api/notifications/mark-all-read/ \
  -H "Authorization: Token $TOKEN"

# 7. Unlike a post
curl -X POST http://localhost:8000/api/posts/1/unlike/ \
  -H "Authorization: Token $TOKEN"
```

---

## API Endpoint Summary

### Like Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/posts/<pk>/like/` | Required | Like a post |
| POST | `/api/posts/<pk>/unlike/` | Required | Unlike a post |
| GET | `/api/posts/<pk>/likes/` | Optional | Get post likes |

### Notification Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/notifications/` | Required | Get all notifications |
| GET | `/api/notifications/unread/` | Required | Get unread notifications |
| POST | `/api/notifications/<pk>/read/` | Required | Mark as read |
| POST | `/api/notifications/mark-all-read/` | Required | Mark all as read |
| DELETE | `/api/notifications/<pk>/` | Required | Delete notification |

---

## Features Summary

### Like System
✅ Like posts  
✅ Unlike posts  
✅ View post likes list  
✅ Like count on posts  
✅ Prevent duplicate likes  
✅ Automatic notification creation  

### Notification System
✅ Generic notification model  
✅ Read/unread status  
✅ Filter by read status  
✅ Mark single as read  
✅ Mark all as read  
✅ Delete notifications  
✅ Unread count  
✅ Paginated results  

---

## Notification Types

The system automatically creates notifications for:

1. **Post Likes:** When someone likes your post
   - Verb: "liked your post"
   - Target: Post object

2. **New Followers:** When someone follows you (from accounts app)
   - Verb: "started following you"
   - Target: None

3. **Post Comments:** When someone comments on your post
   - Verb: "commented on your post"
   - Target: Comment object

---

## Security

- All endpoints require authentication except viewing post likes
- Users can only:
  - Like/unlike posts once
  - View their own notifications
  - Mark their own notifications as read
  - Delete their own notifications
- Post authors don't receive notifications for their own likes

---

## Performance Considerations

- Like queries use `unique_together` constraint for efficient lookups
- Notification queries are optimized with `select_related` and indexes
- Pagination limits response size
- Database indexes on frequently queried fields

---

**Last Updated:** October 11, 2025  
**Version:** 1.0.0  
**Repository:** Alx_DjangoLearnLab/social_media_api

