import importlib
import os
from unittest import TestCase
from unittest.mock import patch


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
