# Posts and Comments - Testing and Validation Guide

## Overview

This guide provides testing procedures and validation steps for the Posts and Comments functionality.

---

## Prerequisites

1. **Django installed** and database migrated
2. **User account** created (for authentication)
3. **Authentication token** obtained

### Quick Setup

```bash
# Navigate to project
cd /Users/sedziafa/Alx_DjangoLearnLab/social_media_api

# Run migrations (if Django is installed)
python manage.py makemigrations posts
python manage.py migrate

# Create superuser for testing
python manage.py createsuperuser
```

---

## Test Scenarios

### Scenario 1: Complete Post Lifecycle

#### Step 1: Register/Login
```bash
# Login to get token
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'
```

**Expected Response:**
```json
{
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user": {...},
    "message": "Login successful!"
}
```

#### Step 2: Create a Post
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My First Post",
    "content": "This is the content of my first post."
  }'
```

**Expected Response:** `201 Created`
```json
{
    "id": 1,
    "author": {...},
    "title": "My First Post",
    "content": "This is the content of my first post.",
    "created_at": "...",
    "updated_at": "...",
    "comment_count": 0,
    "comments": []
}
```

#### Step 3: Retrieve the Post
```bash
curl -X GET http://localhost:8000/api/posts/1/
```

**Expected Response:** `200 OK` with post details

#### Step 4: Update the Post
```bash
curl -X PATCH http://localhost:8000/api/posts/1/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Updated Post Title"
  }'
```

**Expected Response:** `200 OK` with updated post

#### Step 5: Add a Comment
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "post": 1,
    "content": "Great post!"
  }'
```

**Expected Response:** `201 Created`

#### Step 6: Delete the Post
```bash
curl -X DELETE http://localhost:8000/api/posts/1/ \
  -H "Authorization: Token YOUR_TOKEN"
```

**Expected Response:** `204 No Content`

---

### Scenario 2: Permission Testing

#### Test 1: Unauthenticated Create (Should Fail)
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test",
    "content": "Test"
  }'
```

**Expected Response:** `401 Unauthorized`

#### Test 2: Update Someone Else's Post (Should Fail)
```bash
# User A creates a post
# User B tries to update it

curl -X PATCH http://localhost:8000/api/posts/1/ \
  -H "Authorization: Token USER_B_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Trying to hack"
  }'
```

**Expected Response:** `403 Forbidden`

#### Test 3: Delete Someone Else's Comment (Should Fail)
```bash
curl -X DELETE http://localhost:8000/api/comments/1/ \
  -H "Authorization: Token DIFFERENT_USER_TOKEN"
```

**Expected Response:** `403 Forbidden`

---

### Scenario 3: Filtering and Search

#### Test 1: Search Posts by Keyword
```bash
curl -X GET "http://localhost:8000/api/posts/?search=django"
```

**Expected:** Posts containing "django" in title or content

#### Test 2: Filter Posts by Author
```bash
curl -X GET "http://localhost:8000/api/posts/?author=testuser"
```

**Expected:** Only posts by "testuser"

#### Test 3: Filter Comments by Post
```bash
curl -X GET "http://localhost:8000/api/comments/?post=1"
```

**Expected:** Only comments on post ID 1

#### Test 4: Ordering
```bash
# Most recent posts first
curl -X GET "http://localhost:8000/api/posts/?ordering=-created_at"

# Oldest posts first
curl -X GET "http://localhost:8000/api/posts/?ordering=created_at"
```

---

### Scenario 4: Pagination

#### Test 1: First Page
```bash
curl -X GET "http://localhost:8000/api/posts/"
```

**Expected Response:**
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/posts/?page=2",
    "previous": null,
    "results": [...]  // 10 items
}
```

#### Test 2: Second Page
```bash
curl -X GET "http://localhost:8000/api/posts/?page=2"
```

**Expected:** Next 10 items

---

### Scenario 5: Validation Testing

#### Test 1: Empty Title (Should Fail)
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "",
    "content": "Content"
  }'
```

**Expected Response:** `400 Bad Request`
```json
{
    "title": ["Post title cannot be empty."]
}
```

#### Test 2: Empty Content (Should Fail)
```bash
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Title",
    "content": ""
  }'
```

**Expected Response:** `400 Bad Request`

#### Test 3: Missing Post ID in Comment (Should Fail)
```bash
curl -X POST http://localhost:8000/api/comments/ \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Comment without post"
  }'
```

**Expected Response:** `400 Bad Request`

---

## Python Testing Script

```python
import requests
import json

BASE_URL = "http://localhost:8000/api"

class PostsAPITester:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.token = None
        self.base_url = BASE_URL
        
    def login(self):
        """Login and get authentication token"""
        response = requests.post(
            f"{self.base_url}/accounts/login/",
            json={"username": self.username, "password": self.password}
        )
        if response.status_code == 200:
            self.token = response.json()['token']
            print(f"✅ Login successful. Token: {self.token[:20]}...")
            return True
        else:
            print(f"❌ Login failed: {response.status_code}")
            return False
    
    def get_headers(self):
        """Get headers with authentication"""
        return {
            "Authorization": f"Token {self.token}",
            "Content-Type": "application/json"
        }
    
    def test_create_post(self):
        """Test creating a post"""
        print("\n📝 Testing: Create Post")
        response = requests.post(
            f"{self.base_url}/posts/",
            json={
                "title": "Test Post",
                "content": "This is a test post content."
            },
            headers=self.get_headers()
        )
        
        if response.status_code == 201:
            post = response.json()
            print(f"✅ Post created successfully. ID: {post['id']}")
            return post['id']
        else:
            print(f"❌ Failed to create post: {response.status_code}")
            print(response.json())
            return None
    
    def test_list_posts(self):
        """Test listing posts"""
        print("\n📋 Testing: List Posts")
        response = requests.get(f"{self.base_url}/posts/")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Listed posts successfully. Count: {data['count']}")
            return True
        else:
            print(f"❌ Failed to list posts: {response.status_code}")
            return False
    
    def test_get_post(self, post_id):
        """Test retrieving a specific post"""
        print(f"\n🔍 Testing: Get Post {post_id}")
        response = requests.get(f"{self.base_url}/posts/{post_id}/")
        
        if response.status_code == 200:
            post = response.json()
            print(f"✅ Retrieved post: {post['title']}")
            return True
        else:
            print(f"❌ Failed to get post: {response.status_code}")
            return False
    
    def test_update_post(self, post_id):
        """Test updating a post"""
        print(f"\n✏️  Testing: Update Post {post_id}")
        response = requests.patch(
            f"{self.base_url}/posts/{post_id}/",
            json={"title": "Updated Test Post"},
            headers=self.get_headers()
        )
        
        if response.status_code == 200:
            post = response.json()
            print(f"✅ Updated post: {post['title']}")
            return True
        else:
            print(f"❌ Failed to update post: {response.status_code}")
            return False
    
    def test_create_comment(self, post_id):
        """Test creating a comment"""
        print(f"\n💬 Testing: Create Comment on Post {post_id}")
        response = requests.post(
            f"{self.base_url}/comments/",
            json={
                "post": post_id,
                "content": "This is a test comment."
            },
            headers=self.get_headers()
        )
        
        if response.status_code == 201:
            comment = response.json()
            print(f"✅ Comment created successfully. ID: {comment['id']}")
            return comment['id']
        else:
            print(f"❌ Failed to create comment: {response.status_code}")
            return None
    
    def test_search_posts(self, query):
        """Test searching posts"""
        print(f"\n🔎 Testing: Search Posts for '{query}'")
        response = requests.get(f"{self.base_url}/posts/?search={query}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Search successful. Found: {data['count']} posts")
            return True
        else:
            print(f"❌ Search failed: {response.status_code}")
            return False
    
    def test_delete_post(self, post_id):
        """Test deleting a post"""
        print(f"\n🗑️  Testing: Delete Post {post_id}")
        response = requests.delete(
            f"{self.base_url}/posts/{post_id}/",
            headers=self.get_headers()
        )
        
        if response.status_code == 204:
            print(f"✅ Post deleted successfully")
            return True
        else:
            print(f"❌ Failed to delete post: {response.status_code}")
            return False
    
    def run_all_tests(self):
        """Run all tests"""
        print("="*60)
        print("🧪 POSTS AND COMMENTS API TESTING")
        print("="*60)
        
        if not self.login():
            return
        
        # Create a post
        post_id = self.test_create_post()
        if not post_id:
            return
        
        # List posts
        self.test_list_posts()
        
        # Get specific post
        self.test_get_post(post_id)
        
        # Update post
        self.test_update_post(post_id)
        
        # Create comment
        comment_id = self.test_create_comment(post_id)
        
        # Search posts
        self.test_search_posts("Test")
        
        # Delete post
        self.test_delete_post(post_id)
        
        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED")
        print("="*60)


# Run tests
if __name__ == "__main__":
    # Replace with your test credentials
    tester = PostsAPITester("testuser", "testpass123")
    tester.run_all_tests()
```

---

## Validation Checklist

### Functional Requirements

- [ ] Users can create posts
- [ ] Users can view all posts
- [ ] Users can view single post with comments
- [ ] Users can update their own posts
- [ ] Users can delete their own posts
- [ ] Users can create comments on posts
- [ ] Users can update their own comments
- [ ] Users can delete their own comments
- [ ] Unauthenticated users can view posts (read-only)
- [ ] Users cannot modify others' posts/comments

### Non-Functional Requirements

- [ ] Posts are paginated (10 per page)
- [ ] Comments are paginated (10 per page)
- [ ] Search works for post title and content
- [ ] Filtering by author works
- [ ] Filtering by post works for comments
- [ ] Ordering by created_at works
- [ ] Response times are acceptable
- [ ] Proper error messages are returned
- [ ] API follows RESTful conventions

### Security Requirements

- [ ] Authentication required for create operations
- [ ] Only authors can update their content
- [ ] Only authors can delete their content
- [ ] SQL injection is prevented
- [ ] XSS attacks are prevented
- [ ] Token authentication is secure

---

## Known Issues and Limitations

1. **No soft delete**: Deleted posts are permanently removed
2. **No edit history**: Post/comment updates don't track history
3. **No notifications**: Users aren't notified of comments on their posts
4. **No nested comments**: Comments are flat (no replies to comments)

---

## Performance Testing

### Load Testing

```bash
# Using Apache Bench (ab)
ab -n 1000 -c 10 http://localhost:8000/api/posts/

# Using wrk
wrk -t12 -c400 -d30s http://localhost:8000/api/posts/
```

### Expected Performance
- **List endpoint**: < 200ms for 100 items
- **Detail endpoint**: < 100ms
- **Create endpoint**: < 300ms
- **Update endpoint**: < 200ms

---

**Last Updated:** October 11, 2025  
**Version:** 1.0.0

