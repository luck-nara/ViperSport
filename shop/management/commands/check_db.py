from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Test database connection (Supabase PostgreSQL or SQLite)'

    def handle(self, *args, **options):
        db = settings.DATABASES['default']
        engine = db['ENGINE']
        self.stdout.write(f'Engine: {engine}')

        if 'postgresql' in engine:
            self.stdout.write(f"Host: {db.get('HOST')}")
            self.stdout.write(f"Database: {db.get('NAME')}")

        try:
            with connection.cursor() as cursor:
                cursor.execute('SELECT 1')
            self.stdout.write(self.style.SUCCESS('Database connection OK'))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'Connection failed: {exc}'))
            raise SystemExit(1) from exc
