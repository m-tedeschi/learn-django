import importlib
import os
import unittest
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from django.test import SimpleTestCase


FRONTEND_INDEX = Path(__file__).resolve().parent.parent / 'frontend' / 'dist' / 'index.html'


@unittest.skipUnless(FRONTEND_INDEX.exists(), 'frontend must be built before testing SPA routes')
class FrontendRouteTests(SimpleTestCase):
    def test_root_serves_vue_app(self):
        response = self.client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div id="app"></div>', html=True)

    def test_vue_route_serves_vue_app(self):
        response = self.client.get('/books')

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<div id="app"></div>', html=True)


class DatabaseUrlSettingsTests(TestCase):
    def test_database_url_configures_postgres_connection(self):
        with patch.dict(
            os.environ,
            {
                'DATABASE_URL': (
                    'postgresql://railway_user:secret@'
                    'postgres.railway.internal:5432/railway'
                )
            },
        ):
            settings = importlib.reload(importlib.import_module('config.settings'))

        database = settings.DATABASES['default']
        self.assertEqual(database['ENGINE'], 'django.db.backends.postgresql')
        self.assertEqual(database['NAME'], 'railway')
        self.assertEqual(database['USER'], 'railway_user')
        self.assertEqual(database['PASSWORD'], 'secret')
        self.assertEqual(database['HOST'], 'postgres.railway.internal')
        self.assertEqual(database['PORT'], 5432)

    def test_production_host_settings_come_from_environment(self):
        with patch.dict(
            os.environ,
            {
                'DEBUG': '0',
                'ALLOWED_HOSTS': 'example.up.railway.app,api.example.com',
                'CSRF_TRUSTED_ORIGINS': 'https://example.up.railway.app',
            },
        ):
            settings = importlib.reload(importlib.import_module('config.settings'))

        self.assertFalse(settings.DEBUG)
        self.assertEqual(
            settings.ALLOWED_HOSTS,
            ['example.up.railway.app', 'api.example.com'],
        )
        self.assertEqual(
            settings.CSRF_TRUSTED_ORIGINS,
            ['https://example.up.railway.app'],
        )
