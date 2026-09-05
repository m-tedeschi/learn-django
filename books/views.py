from django.http import JsonResponse

from .models import Book


def book_list_api(request):
    books = Book.objects.order_by('title').values(
        'id',
        'title',
        'author',
        'published_year',
    )
    return JsonResponse({'books': list(books)})
