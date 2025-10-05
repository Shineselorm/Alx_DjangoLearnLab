# Authentication System Overview

This document describes how user authentication is implemented in the Django Blog project.

## Features
- User registration (username, email, password)
- Login and logout using Django auth views
- Profile view/edit for first name, last name, email
- Flash messages for success feedback
- Login redirect to profile

## URLs
- `/login/` – Login (Django auth `LoginView`)
- `/logout/` – Logout (Django auth `LogoutView`)
- `/register/` – Registration form
- `/profile/` – View and edit profile (login required)
- `/` – Home page

## Key Code
- `blog/forms.py`: `RegistrationForm` (extends `UserCreationForm`), `ProfileForm`
- `blog/views.py`: `home`, `register`, `profile`
- `blog/urls.py`: URL patterns for auth and home
- `django_blog/urls.py`: includes `blog.urls`
- `django_blog/settings.py`: `LOGIN_REDIRECT_URL`, `LOGIN_URL`

## Templates
- `templates/auth/login.html`
- `templates/auth/logout.html`
- `templates/auth/register.html`
- `templates/auth/profile.html`
- `templates/base.html` (includes nav and message display)

## Security Notes
- CSRF tokens included in all POST forms via `{% csrf_token %}`
- Passwords stored using Django's password hashing
- Login required for `/profile/`

## How to Test
1. Start server: `source .venv/bin/activate && python manage.py runserver`
2. Visit `/register/`, create a user (with email)
3. After success message, go to `/login/` and sign in
4. You’ll be redirected to `/profile/`; update your profile and save
5. Use nav links to logout and login again
