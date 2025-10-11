# Follow and Feed Functionality - API Documentation

## Overview

This document provides comprehensive documentation for the User Follow and Feed functionality in the Social Media API. Users can follow other users and view an aggregated feed of posts from the users they follow.

---

## Table of Contents

1. [User Model Updates](#user-model-updates)
2. [Follow Management Endpoints](#follow-management-endpoints)
3. [Feed Endpoint](#feed-endpoint)
4. [Testing Guide](#testing-guide)
5. [Complete Examples](#complete-examples)

---

## User Model Updates

### CustomUser Model Fields

The CustomUser model includes a `followers` field for managing follow relationships.

**File:** `accounts/models.py`

```python
followers = models.ManyToManyField(
    'self',
    symmetrical=False,
    related_name='following',
    blank=True,
    help_text='Users who follow this user'
)
```

### Model Relationships

- **`user.followers`** - QuerySet of users who follow this user
- **`user.following`** - QuerySet of users this user follows

### Helper Methods

```python
# Follow a user
user.follow(other_user)

# Unfollow a user
user.unfollow(other_user)

# Check if following
user.is_following(other_user)  # Returns boolean

# Check if followed by
user.is_followed_by(other_user)  # Returns boolean

# Get counts
user.get_follower_count()  # Number of followers
user.get_following_count()  # Number of users following
```

---

## Follow Management Endpoints

### 1. Follow a User (Generic Endpoint)

**Endpoint:** `POST /api/accounts/follow/`

**Authentication:** Required

**Description:** Follow or unfollow a user using the generic endpoint.

**Request:**
```http
POST /api/accounts/follow/
Authorization: Token <your_token>
Content-Type: application/json

{
    "user_id": 5,
    "action": "follow"
}
```

**Response:** `200 OK`
```json
{
    "message": "You are now following john_doe",
    "following": true
}
```

---

### 2. Follow User by ID

**Endpoint:** `POST /api/accounts/follow/<user_id>/`

**Authentication:** Required

**Description:** Follow a specific user by their ID.

**Request:**
```http
POST /api/accounts/follow/5/
Authorization: Token <your_token>
```

**Response:** `200 OK`
```json
{
    "message": "You are now following john_doe",
    "following": true,
    "user": {
        "id": 5,
        "username": "john_doe"
    }
}
```

**Error Response:** `400 Bad Request`
```json
{
    "error": "You cannot follow yourself."
}
```

---

### 3. Unfollow User by ID

**Endpoint:** `POST /api/accounts/unfollow/<user_id>/`

**Authentication:** Required

**Description:** Unfollow a specific user by their ID.

**Request:**
```http
POST /api/accounts/unfollow/5/
Authorization: Token <your_token>
```

**Response:** `200 OK`
```json
{
    "message": "You have unfollowed john_doe",
    "following": false,
    "user": {
        "id": 5,
        "username": "john_doe"
    }
}
```

---

### 4. Get My Followers

**Endpoint:** `GET /api/accounts/followers/`

**Authentication:** Required

**Description:** Retrieves a list of users who follow the authenticated user.

**Request:**
```http
GET /api/accounts/followers/
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
            "id": 2,
            "username": "jane_smith",
            "first_name": "Jane",
            "last_name": "Smith",
            "bio": "Tech enthusiast",
            "profile_picture": "/media/profile_pictures/jane.jpg",
            "follower_count": 25
        },
        ...
    ]
}
```

---

### 5. Get Users I'm Following

**Endpoint:** `GET /api/accounts/following/`

**Authentication:** Required

**Description:** Retrieves a list of users that the authenticated user follows.

**Request:**
```http
GET /api/accounts/following/
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
            "id": 5,
            "username": "john_doe",
            "first_name": "John",
            "last_name": "Doe",
            "bio": "Developer",
            "profile_picture": "/media/profile_pictures/john.jpg",
            "follower_count": 50
        },
        ...
    ]
}
```

---

## Feed Endpoint

### Get Feed

**Endpoint:** `GET /api/feed/`

**Authentication:** Required

**Description:** Retrieves an aggregated feed of posts from users that the authenticated user follows. Posts are ordered by creation date, with the most recent posts appearing first.

**Request:**
```http
GET /api/feed/
Authorization: Token <your_token>
```

**Response:** `200 OK`
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/feed/?page=2",
    "previous": null,
    "following_count": 15,
    "results": [
        {
            "id": 42,
            "author": {
                "id": 5,
                "username": "john_doe",
                "first_name": "John",
                "last_name": "Doe",
                "profile_picture": "/media/profile_pictures/john.jpg"
            },
            "title": "Latest Update from John",
            "content": "This is John's latest post...",
            "created_at": "2025-10-11T12:00:00Z",
            "updated_at": "2025-10-11T12:00:00Z",
            "comment_count": 5
        },
        {
            "id": 41,
            "author": {
                "id": 8,
                "username": "alice_wonderland",
                "first_name": "Alice",
                "last_name": "Wonderland",
                "profile_picture": null
            },
            "title": "Alice's Thoughts",
            "content": "Sharing my thoughts today...",
            "created_at": "2025-10-11T11:30:00Z",
            "updated_at": "2025-10-11T11:30:00Z",
            "comment_count": 3
        },
        ...
    ]
}
```

### Feed Features

- **Personalized Feed**: Only shows posts from users you follow
- **Chronological Order**: Most recent posts first
- **Paginated**: 10 posts per page (default)
- **Following Count**: Includes count of users you follow
- **Optimized Queries**: Uses select_related and prefetch_related for performance

### Empty Feed Response

If you don't follow anyone or they haven't posted:

```json
{
    "count": 0,
    "following_count": 0,
    "results": []
}
```

---

## Testing Guide

### Test Scenario 1: Follow a User

```bash
# Login to get token
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Follow user with ID 5
curl -X POST http://localhost:8000/api/accounts/follow/5/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Expected Result:**
```json
{
    "message": "You are now following john_doe",
    "following": true,
    "user": {
        "id": 5,
        "username": "john_doe"
    }
}
```

---

### Test Scenario 2: View Feed

```bash
# Get your personalized feed
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Expected Result:**
- Posts from users you follow
- Ordered by creation date (newest first)
- Paginated with 10 posts per page

---

### Test Scenario 3: Get Followers and Following

```bash
# Get your followers
curl -X GET http://localhost:8000/api/accounts/followers/ \
  -H "Authorization: Token YOUR_TOKEN"

# Get users you're following
curl -X GET http://localhost:8000/api/accounts/following/ \
  -H "Authorization: Token YOUR_TOKEN"
```

---

### Test Scenario 4: Unfollow a User

```bash
# Unfollow user with ID 5
curl -X POST http://localhost:8000/api/accounts/unfollow/5/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Expected Result:**
```json
{
    "message": "You have unfollowed john_doe",
    "following": false,
    "user": {
        "id": 5,
        "username": "john_doe"
    }
}
```

---

## Complete Examples

### Python Example: Complete Follow Workflow

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
    
    def follow_user(self, user_id):
        """Follow a specific user"""
        response = requests.post(
            f"{BASE_URL}/accounts/follow/{user_id}/",
            headers=self.headers
        )
        return response.json()
    
    def unfollow_user(self, user_id):
        """Unfollow a specific user"""
        response = requests.post(
            f"{BASE_URL}/accounts/unfollow/{user_id}/",
            headers=self.headers
        )
        return response.json()
    
    def get_followers(self):
        """Get list of followers"""
        response = requests.get(
            f"{BASE_URL}/accounts/followers/",
            headers=self.headers
        )
        return response.json()
    
    def get_following(self):
        """Get list of users I'm following"""
        response = requests.get(
            f"{BASE_URL}/accounts/following/",
            headers=self.headers
        )
        return response.json()
    
    def get_feed(self):
        """Get personalized feed"""
        response = requests.get(
            f"{BASE_URL}/feed/",
            headers=self.headers
        )
        return response.json()

# Usage
client = SocialMediaClient("your_token_here")

# Follow a user
result = client.follow_user(5)
print(f"✅ {result['message']}")

# Get feed
feed = client.get_feed()
print(f"📰 Feed has {feed['count']} posts from {feed['following_count']} users")

# Display feed posts
for post in feed['results']:
    author = post['author']['username']
    title = post['title']
    print(f"  - {title} by @{author}")

# Get following list
following = client.get_following()
print(f"👥 Following {following['count']} users")
```

---

### cURL Complete Workflow

```bash
# 1. Login
TOKEN=$(curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","password":"testpass123"}' \
  | jq -r '.token')

echo "Token: $TOKEN"

# 2. Follow some users
curl -X POST http://localhost:8000/api/accounts/follow/5/ \
  -H "Authorization: Token $TOKEN"

curl -X POST http://localhost:8000/api/accounts/follow/7/ \
  -H "Authorization: Token $TOKEN"

curl -X POST http://localhost:8000/api/accounts/follow/9/ \
  -H "Authorization: Token $TOKEN"

# 3. Check who you're following
curl -X GET http://localhost:8000/api/accounts/following/ \
  -H "Authorization: Token $TOKEN"

# 4. View your feed
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token $TOKEN"

# 5. View your followers
curl -X GET http://localhost:8000/api/accounts/followers/ \
  -H "Authorization: Token $TOKEN"
```

---

## API Endpoint Summary

### Follow Management Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/accounts/follow/` | Required | Follow/unfollow with body data |
| POST | `/api/accounts/follow/<user_id>/` | Required | Follow specific user |
| POST | `/api/accounts/unfollow/<user_id>/` | Required | Unfollow specific user |
| GET | `/api/accounts/followers/` | Required | Get my followers |
| GET | `/api/accounts/following/` | Required | Get users I'm following |

### Feed Endpoint

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/feed/` | Required | Get personalized feed |

---

## Features Summary

### Follow System
✅ Follow users by ID  
✅ Unfollow users by ID  
✅ View followers list  
✅ View following list  
✅ Prevent self-following  
✅ Follower/following counts  
✅ Paginated results  

### Feed System
✅ Personalized feed based on following  
✅ Chronological order (newest first)  
✅ Optimized database queries  
✅ Paginated results (10 per page)  
✅ Shows following count  
✅ Empty state handling  

---

## Implementation Details

### Database Optimization

The feed uses optimized queries:
```python
Post.objects.filter(
    author__in=following_users
).select_related('author').prefetch_related('comments').order_by('-created_at')
```

**Optimizations:**
- `select_related('author')` - Reduces queries for author data
- `prefetch_related('comments')` - Efficient comment loading
- `order_by('-created_at')` - Newest posts first
- Uses `following.all()` which leverages database indexes

### Security

- All endpoints require authentication
- Users can only modify their own following list
- Cannot follow yourself
- Proper permission checks in place

---

## Troubleshooting

### Issue: Empty Feed

**Possible Causes:**
1. Not following anyone
2. Followed users haven't created posts

**Solution:**
```bash
# Check who you're following
curl -X GET http://localhost:8000/api/accounts/following/ \
  -H "Authorization: Token YOUR_TOKEN"

# Follow some users
curl -X POST http://localhost:8000/api/accounts/follow/5/ \
  -H "Authorization: Token YOUR_TOKEN"
```

### Issue: Cannot Follow User

**Error:** "You cannot follow yourself"

**Solution:** You're trying to follow your own account. Follow a different user.

---

## Performance Considerations

- Feed queries are optimized with select_related/prefetch_related
- Results are paginated to limit response size
- Database indexes on created_at field for efficient ordering
- Many-to-many relationship handled efficiently by Django ORM

---

**Last Updated:** October 11, 2025  
**Version:** 1.0.0  
**Repository:** Alx_DjangoLearnLab/social_media_api

