from django.urls import path
from . import views

app_name = 'bookshelf'

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('book/<int:pk>/', views.book_detail, name='book_detail'),
    path('book/<int:pk>/add-review/', views.add_review, name='add_review'),
    path('book/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('book/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('add-book/', views.add_book, name='add_book'),
    path('my-reading-lists/', views.my_reading_lists, name='my_reading_lists'),
    path('create-reading-list/', views.create_reading_list, name='create_reading_list'),
    path('public-reading-lists/', views.public_reading_lists, name='public_reading_lists'),
    path('review/<int:pk>/edit/', views.edit_review, name='edit_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
]
