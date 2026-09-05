from django.urls import path

from . import views

urlpatterns = [
    path('api/books/', views.book_list_api, name='book-list-api'),
]
