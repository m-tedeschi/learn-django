from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Book


class BookViewsTests(TestCase):
    def test_book_list_api_returns_books(self):
        Book.objects.create(
            title='Harry Potter',
            author='J.K. Rowling',
            published_year=1997,
        )

        response = self.client.get(reverse('book-list-api'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                'books': [
                    {
                        'id': 1,
                        'title': 'Harry Potter',
                        'author': 'J.K. Rowling',
                        'published_year': 1997,
                    }
                ]
            },
        )


class AdminSiteTests(TestCase):
    def test_view_site_link_points_to_vite_frontend(self):
        user_model = get_user_model()
        user_model.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='password',
        )
        self.client.login(username='admin', password='password')

        response = self.client.get(reverse('admin:index'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="http://localhost:5173/"')
