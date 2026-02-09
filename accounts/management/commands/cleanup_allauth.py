"""
Management command to remove django-allauth tables from database
"""
from django.core.management.base import BaseCommand
from django.db import connection


class Command(BaseCommand):
    help = 'Remove django-allauth tables from the database'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            # Drop all django-allauth related tables
            tables_to_drop = [
                'socialaccount_socialtoken',
                'socialaccount_socialapp_sites',
                'socialaccount_socialapp',
                'socialaccount_socialaccount',
                'account_emailconfirmation',
                'account_emailaddress',
                'django_site',
            ]
            
            self.stdout.write('Dropping allauth tables...')
            for table in tables_to_drop:
                try:
                    cursor.execute(f'DROP TABLE IF EXISTS {table} CASCADE')
                    self.stdout.write(self.style.SUCCESS(f'✓ Dropped table: {table}'))
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f'⚠ Could not drop {table}: {e}'))
            
            # Delete allauth migration records
            self.stdout.write('\nCleaning migration records...')
            try:
                cursor.execute("DELETE FROM django_migrations WHERE app IN ('socialaccount', 'account', 'sites')")
                self.stdout.write(self.style.SUCCESS('✓ Removed allauth migration records'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ Error removing migrations: {e}'))
            
            self.stdout.write(self.style.SUCCESS('\n✅ All Done! Allauth tables and migrations removed.'))
