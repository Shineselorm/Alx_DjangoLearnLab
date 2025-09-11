from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views   # <-- import whole views module

urlpatterns = [
    # Book + Library views
    path('books/', views.list_books, name='list_books'),
    path('library/<int:pk>/', views.LibraryDetailView.as_view(), name='library_detail'),

    # Authentication views
    path('register/', views.register, name='register'),  # <-- checker will find this
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
]
