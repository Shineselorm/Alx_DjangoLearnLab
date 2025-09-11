from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView, register_view

urlpatterns = [
    # Function-based view
    path('books/', list_books, name='list_books'),

    # Class-based view
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # Custom register view
    path('register/', register_view, name='register'),

    # Built-in LoginView
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),

    # Built-in LogoutView
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
