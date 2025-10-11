# Follow and Feed - Quick Testing Guide

This guide provides step-by-step instructions to quickly test the Follow and Feed functionality.

---

## Prerequisites

1. **Server Running:** Ensure the development server is running:
   ```bash
   python manage.py runserver
   ```

2. **User Accounts:** You need at least 2-3 user accounts to test follow functionality.

---

## Quick Test Workflow

### Step 1: Create Test Users

```bash
# Register User 1
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "password": "alice123",
    "password_confirm": "alice123",
    "bio": "Alice here!"
  }'

# Save the token from response
# TOKEN_ALICE="<token_here>"

# Register User 2
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "bob",
    "email": "bob@example.com",
    "password": "bob123",
    "password_confirm": "bob123",
    "bio": "Bob here!"
  }'

# TOKEN_BOB="<token_here>"

# Register User 3
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "charlie",
    "email": "charlie@example.com",
    "password": "charlie123",
    "password_confirm": "charlie123",
    "bio": "Charlie here!"
  }'

# TOKEN_CHARLIE="<token_here>"
```

---

### Step 2: Create Posts (as Bob and Charlie)

```bash
# Bob creates a post
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token $TOKEN_BOB" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Bob'\''s First Post",
    "content": "Hello from Bob! This is my first post."
  }'

# Charlie creates a post
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token $TOKEN_CHARLIE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Charlie'\''s Adventure",
    "content": "Just went hiking today! Amazing views."
  }'

# Bob creates another post
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Token $TOKEN_BOB" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Bob'\''s Second Post",
    "content": "Update: Working on a new project!"
  }'
```

---

### Step 3: Get User IDs

```bash
# List all users to get their IDs
curl -X GET http://localhost:8000/api/accounts/users/ \
  -H "Authorization: Token $TOKEN_ALICE"
```

**Expected Response:**
```json
{
  "count": 3,
  "results": [
    {
      "id": 1,
      "username": "alice",
      ...
    },
    {
      "id": 2,
      "username": "bob",
      ...
    },
    {
      "id": 3,
      "username": "charlie",
      ...
    }
  ]
}
```

Note Bob's ID (e.g., 2) and Charlie's ID (e.g., 3).

---

### Step 4: Alice Follows Bob and Charlie

```bash
# Alice follows Bob (user ID 2)
curl -X POST http://localhost:8000/api/accounts/follow/2/ \
  -H "Authorization: Token $TOKEN_ALICE"

# Expected: {"message": "You are now following bob", "following": true, ...}

# Alice follows Charlie (user ID 3)
curl -X POST http://localhost:8000/api/accounts/follow/3/ \
  -H "Authorization: Token $TOKEN_ALICE"

# Expected: {"message": "You are now following charlie", "following": true, ...}
```

---

### Step 5: Check Who Alice is Following

```bash
# Get Alice's following list
curl -X GET http://localhost:8000/api/accounts/following/ \
  -H "Authorization: Token $TOKEN_ALICE"
```

**Expected Response:**
```json
{
  "count": 2,
  "results": [
    {
      "id": 2,
      "username": "bob",
      ...
    },
    {
      "id": 3,
      "username": "charlie",
      ...
    }
  ]
}
```

---

### Step 6: View Alice's Feed

```bash
# Get Alice's personalized feed
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token $TOKEN_ALICE"
```

**Expected Response:**
```json
{
  "count": 3,
  "following_count": 2,
  "results": [
    {
      "id": 3,
      "author": {
        "id": 2,
        "username": "bob",
        ...
      },
      "title": "Bob's Second Post",
      "content": "Update: Working on a new project!",
      "created_at": "2025-10-11T12:30:00Z",
      ...
    },
    {
      "id": 2,
      "author": {
        "id": 3,
        "username": "charlie",
        ...
      },
      "title": "Charlie's Adventure",
      "content": "Just went hiking today! Amazing views.",
      "created_at": "2025-10-11T12:15:00Z",
      ...
    },
    {
      "id": 1,
      "author": {
        "id": 2,
        "username": "bob",
        ...
      },
      "title": "Bob's First Post",
      "content": "Hello from Bob! This is my first post.",
      "created_at": "2025-10-11T12:00:00Z",
      ...
    }
  ]
}
```

**✅ Feed shows only posts from Bob and Charlie (users Alice follows)**  
**✅ Posts are ordered by creation date (newest first)**

---

### Step 7: Test Empty Feed

```bash
# Bob's feed (Bob doesn't follow anyone yet)
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token $TOKEN_BOB"
```

**Expected Response:**
```json
{
  "count": 0,
  "following_count": 0,
  "results": []
}
```

**✅ Empty feed when not following anyone**

---

### Step 8: Test Unfollow

```bash
# Alice unfollows Charlie (user ID 3)
curl -X POST http://localhost:8000/api/accounts/unfollow/3/ \
  -H "Authorization: Token $TOKEN_ALICE"

# Expected: {"message": "You have unfollowed charlie", "following": false, ...}

# Check Alice's feed again
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token $TOKEN_ALICE"
```

**Expected:**  
✅ Feed now shows only Bob's posts (not Charlie's)

---

### Step 9: Test Self-Follow Prevention

```bash
# Try to follow yourself
curl -X POST http://localhost:8000/api/accounts/follow/1/ \
  -H "Authorization: Token $TOKEN_ALICE"
```

**Expected Response:**
```json
{
  "error": "You cannot follow yourself."
}
```

**✅ Self-follow is prevented**

---

### Step 10: Test Followers List

```bash
# Check Bob's followers (should include Alice)
curl -X GET http://localhost:8000/api/accounts/followers/ \
  -H "Authorization: Token $TOKEN_BOB"
```

**Expected Response:**
```json
{
  "count": 1,
  "results": [
    {
      "id": 1,
      "username": "alice",
      ...
    }
  ]
}
```

**✅ Bob's followers list shows Alice**

---

## Test Checklist

Use this checklist to verify all functionality:

### Follow/Unfollow
- [ ] Can follow a user by ID
- [ ] Can unfollow a user by ID
- [ ] Cannot follow yourself (error message)
- [ ] Following list shows correct users
- [ ] Followers list shows correct users
- [ ] Following count is accurate

### Feed
- [ ] Feed shows only posts from followed users
- [ ] Posts are in chronological order (newest first)
- [ ] Feed updates when following new users
- [ ] Feed updates when unfollowing users
- [ ] Empty feed when not following anyone
- [ ] Feed includes following_count
- [ ] Feed pagination works (if > 10 posts)

### Security
- [ ] All endpoints require authentication
- [ ] Unauthenticated requests are rejected
- [ ] Users can only modify their own following list

---

## Automated Test Script

Save this as `test_follow_feed.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000/api"

echo "🧪 Testing Follow and Feed Functionality"
echo "========================================"

# Step 1: Register users
echo -e "\n📝 Step 1: Registering test users..."

ALICE_RESPONSE=$(curl -s -X POST $BASE_URL/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test_alice","email":"test_alice@example.com","password":"test123","password_confirm":"test123","bio":"Test Alice"}')
TOKEN_ALICE=$(echo $ALICE_RESPONSE | jq -r '.token')
echo "✅ Alice registered (Token: ${TOKEN_ALICE:0:10}...)"

BOB_RESPONSE=$(curl -s -X POST $BASE_URL/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test_bob","email":"test_bob@example.com","password":"test123","password_confirm":"test123","bio":"Test Bob"}')
TOKEN_BOB=$(echo $BOB_RESPONSE | jq -r '.token')
echo "✅ Bob registered (Token: ${TOKEN_BOB:0:10}...)"

# Step 2: Bob creates posts
echo -e "\n📝 Step 2: Bob creating posts..."
curl -s -X POST $BASE_URL/posts/ \
  -H "Authorization: Token $TOKEN_BOB" \
  -H "Content-Type: application/json" \
  -d '{"title":"Bob Post 1","content":"First post from Bob"}' > /dev/null
echo "✅ Bob created post 1"

curl -s -X POST $BASE_URL/posts/ \
  -H "Authorization: Token $TOKEN_BOB" \
  -H "Content-Type: application/json" \
  -d '{"title":"Bob Post 2","content":"Second post from Bob"}' > /dev/null
echo "✅ Bob created post 2"

# Step 3: Get user IDs
echo -e "\n📝 Step 3: Getting user IDs..."
USERS_RESPONSE=$(curl -s -X GET $BASE_URL/accounts/users/ \
  -H "Authorization: Token $TOKEN_ALICE")
BOB_ID=$(echo $USERS_RESPONSE | jq -r '.results[] | select(.username=="test_bob") | .id')
echo "✅ Bob's ID: $BOB_ID"

# Step 4: Alice follows Bob
echo -e "\n📝 Step 4: Alice following Bob..."
FOLLOW_RESPONSE=$(curl -s -X POST $BASE_URL/accounts/follow/$BOB_ID/ \
  -H "Authorization: Token $TOKEN_ALICE")
echo "✅ $(echo $FOLLOW_RESPONSE | jq -r '.message')"

# Step 5: Check Alice's feed
echo -e "\n📝 Step 5: Checking Alice's feed..."
FEED_RESPONSE=$(curl -s -X GET $BASE_URL/feed/ \
  -H "Authorization: Token $TOKEN_ALICE")
POST_COUNT=$(echo $FEED_RESPONSE | jq -r '.count')
FOLLOWING_COUNT=$(echo $FEED_RESPONSE | jq -r '.following_count')
echo "✅ Feed has $POST_COUNT posts from $FOLLOWING_COUNT followed users"

# Step 6: Test self-follow prevention
echo -e "\n📝 Step 6: Testing self-follow prevention..."
ALICE_ID=$(echo $USERS_RESPONSE | jq -r '.results[] | select(.username=="test_alice") | .id')
SELF_FOLLOW_RESPONSE=$(curl -s -X POST $BASE_URL/accounts/follow/$ALICE_ID/ \
  -H "Authorization: Token $TOKEN_ALICE")
ERROR_MSG=$(echo $SELF_FOLLOW_RESPONSE | jq -r '.error')
if [ "$ERROR_MSG" != "null" ]; then
    echo "✅ Self-follow prevented: $ERROR_MSG"
else
    echo "❌ Self-follow was not prevented!"
fi

echo -e "\n🎉 All tests completed!"
```

**Run the script:**
```bash
chmod +x test_follow_feed.sh
./test_follow_feed.sh
```

---

## Common Issues and Solutions

### Issue 1: Empty Feed Despite Following Users

**Problem:** Feed is empty even though you follow users.

**Solution:**
- Check that the followed users have created posts
- Verify following list: `GET /api/accounts/following/`
- Check all posts: `GET /api/posts/`

### Issue 2: 401 Unauthorized

**Problem:** Getting "Authentication credentials were not provided"

**Solution:**
- Ensure you're including the token header
- Format: `Authorization: Token <your_token>`
- Check token is valid (login again if needed)

### Issue 3: Feed Shows All Posts

**Problem:** Feed shows posts from users you don't follow

**Solution:**
- This shouldn't happen. Check the implementation
- Verify you're using `/api/feed/` not `/api/posts/`

---

## Performance Testing

To test feed performance with many posts:

```python
# Create many posts (run in Django shell)
from django.contrib.auth import get_user_model
from posts.models import Post

User = get_user_model()
user = User.objects.get(username='bob')

# Create 100 posts
for i in range(100):
    Post.objects.create(
        author=user,
        title=f"Test Post {i}",
        content=f"This is test post number {i}"
    )

print("Created 100 posts")
```

Then check feed pagination:
```bash
curl -X GET http://localhost:8000/api/feed/ \
  -H "Authorization: Token $TOKEN_ALICE"
```

**✅ Should return 10 posts per page with pagination links**

---

## Verification Summary

After completing all tests, you should have verified:

1. ✅ Users can follow other users by ID
2. ✅ Users can unfollow other users by ID
3. ✅ Self-follow is prevented
4. ✅ Feed shows only posts from followed users
5. ✅ Feed is chronologically ordered (newest first)
6. ✅ Empty feed when not following anyone
7. ✅ Following/followers lists are accurate
8. ✅ Pagination works correctly
9. ✅ Authentication is required for all endpoints
10. ✅ Unfollowing removes posts from feed

---

**Happy Testing! 🎉**

If you encounter any issues, check the implementation logs or refer to `FOLLOW_AND_FEED_DOCUMENTATION.md` for detailed API documentation.

