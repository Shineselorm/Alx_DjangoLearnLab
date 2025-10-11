# Social Media API - Testing Guide

## Quick Start Testing with Postman

This guide provides step-by-step instructions for testing the Social Media API using Postman.

## Prerequisites

1. Start the Django development server:
```bash
python manage.py runserver
```

2. Install Postman or use an API testing tool

## Testing Workflow

### Step 1: Register a New User

**Request:**
- **Method:** POST
- **URL:** `http://127.0.0.1:8000/api/accounts/register/`
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123!",
    "password_confirm": "SecurePass123!",
    "first_name": "Test",
    "last_name": "User",
    "bio": "This is my test bio"
  }
  ```

**Expected Response (201 Created):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "bio": "This is my test bio",
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "message": "User registered successfully!"
}
```

**Important:** Save the `token` value! You'll need it for authenticated requests.

---

### Step 2: Login (Alternative to Registration)

**Request:**
- **Method:** POST
- **URL:** `http://127.0.0.1:8000/api/accounts/login/`
- **Headers:**
  ```
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "username": "testuser",
    "password": "SecurePass123!"
  }
  ```

**Expected Response (200 OK):**
```json
{
  "token": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  },
  "message": "Login successful!"
}
```

---

### Step 3: View Your Profile

**Request:**
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/accounts/profile/`
- **Headers:**
  ```
  Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
  ```

**Expected Response (200 OK):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "Test",
  "last_name": "User",
  "bio": "This is my test bio",
  "profile_picture": null,
  "date_joined": "2024-01-15T10:30:00Z",
  "follower_count": 0,
  "following_count": 0,
  "is_following": false
}
```

---

### Step 4: Update Your Profile

**Request:**
- **Method:** PATCH
- **URL:** `http://127.0.0.1:8000/api/accounts/profile/`
- **Headers:**
  ```
  Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "bio": "Updated bio with more information",
    "first_name": "TestUpdated"
  }
  ```

**Expected Response (200 OK):**
```json
{
  "id": 1,
  "username": "testuser",
  "email": "test@example.com",
  "first_name": "TestUpdated",
  "last_name": "User",
  "bio": "Updated bio with more information",
  "profile_picture": null,
  "date_joined": "2024-01-15T10:30:00Z",
  "follower_count": 0,
  "following_count": 0,
  "is_following": false
}
```

---

### Step 5: Create a Second User (for Follow Testing)

Repeat Step 1 with different credentials:

**Body:**
```json
{
  "username": "janedoe",
  "email": "jane@example.com",
  "password": "JanePass123!",
  "password_confirm": "JanePass123!",
  "first_name": "Jane",
  "last_name": "Doe",
  "bio": "Hello, I'm Jane!"
}
```

**Save the second user's token for later use.**

---

### Step 6: List All Users

**Request:**
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/accounts/users/`
- **Headers:**
  ```
  Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
  ```

**Expected Response (200 OK):**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "username": "testuser",
      "first_name": "TestUpdated",
      "last_name": "User",
      "bio": "Updated bio with more information",
      "profile_picture": null,
      "follower_count": 0
    },
    {
      "id": 2,
      "username": "janedoe",
      "first_name": "Jane",
      "last_name": "Doe",
      "bio": "Hello, I'm Jane!",
      "profile_picture": null,
      "follower_count": 0
    }
  ]
}
```

---

### Step 7: View Another User's Profile

**Request:**
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/accounts/users/2/`
- **Headers:**
  ```
  Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
  ```

**Expected Response (200 OK):**
```json
{
  "id": 2,
  "username": "janedoe",
  "email": "jane@example.com",
  "first_name": "Jane",
  "last_name": "Doe",
  "bio": "Hello, I'm Jane!",
  "profile_picture": null,
  "date_joined": "2024-01-15T11:00:00Z",
  "follower_count": 0,
  "following_count": 0,
  "is_following": false
}
```

---

### Step 8: Follow a User

**Request:**
- **Method:** POST
- **URL:** `http://127.0.0.1:8000/api/accounts/follow/`
- **Headers:**
  ```
  Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "user_id": 2,
    "action": "follow"
  }
  ```

**Expected Response (200 OK):**
```json
{
  "message": "You are now following janedoe",
  "following": true
}
```

---

### Step 9: View Your Followers

**Request:**
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/accounts/followers/`
- **Headers:**
  ```
  Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
  ```

**Expected Response (200 OK):**
```json
{
  "count": 0,
  "next": null,
  "previous": null,
  "results": []
}
```

---

### Step 10: View Who You're Following

**Request:**
- **Method:** GET
- **URL:** `http://127.0.0.1:8000/api/accounts/following/`
- **Headers:**
  ```
  Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
  ```

**Expected Response (200 OK):**
```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 2,
      "username": "janedoe",
      "first_name": "Jane",
      "last_name": "Doe",
      "bio": "Hello, I'm Jane!",
      "profile_picture": null,
      "follower_count": 1
    }
  ]
}
```

---

### Step 11: Unfollow a User

**Request:**
- **Method:** POST
- **URL:** `http://127.0.0.1:8000/api/accounts/follow/`
- **Headers:**
  ```
  Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
  Content-Type: application/json
  ```
- **Body (raw JSON):**
  ```json
  {
    "user_id": 2,
    "action": "unfollow"
  }
  ```

**Expected Response (200 OK):**
```json
{
  "message": "You have unfollowed janedoe",
  "following": false
}
```

---

### Step 12: Logout

**Request:**
- **Method:** POST
- **URL:** `http://127.0.0.1:8000/api/accounts/logout/`
- **Headers:**
  ```
  Authorization: Token a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0
  ```

**Expected Response (200 OK):**
```json
{
  "message": "Logged out successfully!"
}
```

**Note:** After logout, the token is deleted and can no longer be used.

---

## Error Responses

### 400 Bad Request
**Example:** Missing required fields
```json
{
  "username": ["This field is required."],
  "password": ["This field is required."]
}
```

### 401 Unauthorized
**Example:** Invalid or missing token
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
**Example:** Invalid credentials
```json
{
  "non_field_errors": ["Invalid credentials. Please try again."]
}
```

### 404 Not Found
**Example:** User does not exist
```json
{
  "detail": "Not found."
}
```

---

## Common Issues & Solutions

### Issue: "Authentication credentials were not provided"
**Solution:** Ensure you include the Authorization header with the correct token format:
```
Authorization: Token <your_token_here>
```

### Issue: "Invalid token"
**Solution:** 
1. Log in again to get a new token
2. Ensure there are no extra spaces in the token
3. Make sure you're using the format `Token <token>` not `Bearer <token>`

### Issue: "This field is required"
**Solution:** Check that all required fields are included in your request body

### Issue: "A user with this username already exists"
**Solution:** Use a different username or log in with the existing account

---

## Testing Checklist

- [ ] Register a new user and receive a token
- [ ] Login with existing credentials
- [ ] View own profile
- [ ] Update profile information
- [ ] List all users
- [ ] View another user's profile
- [ ] Follow a user
- [ ] View followers list
- [ ] View following list
- [ ] Unfollow a user
- [ ] Logout successfully

---

## Advanced Testing

### Upload Profile Picture

**Request:**
- **Method:** PATCH
- **URL:** `http://127.0.0.1:8000/api/accounts/profile/`
- **Headers:**
  ```
  Authorization: Token <your_token>
  ```
- **Body:** form-data
  - Key: `profile_picture` (file)
  - Value: Select an image file

### Test Rate Limiting

Make more than 100 requests per hour as an anonymous user to test rate limiting:

**Expected Response (429 Too Many Requests):**
```json
{
  "detail": "Request was throttled. Expected available in 3600 seconds."
}
```

---

## Postman Collection

You can create a Postman collection with all these requests:

1. Create a new collection named "Social Media API"
2. Add an environment variable `base_url` = `http://127.0.0.1:8000`
3. Add an environment variable `auth_token` to store your token
4. Use `{{base_url}}` and `{{auth_token}}` in your requests
5. Add a test script to automatically save tokens:

```javascript
// In the Tests tab of login/register requests:
if (pm.response.code === 200 || pm.response.code === 201) {
    var jsonData = pm.response.json();
    pm.environment.set("auth_token", jsonData.token);
}
```

---

## Additional Resources

- API Documentation: See README.md
- Django Admin: `http://127.0.0.1:8000/admin/`
- DRF Browsable API: `http://127.0.0.1:8000/api/accounts/`

---

**Happy Testing! 🚀**
