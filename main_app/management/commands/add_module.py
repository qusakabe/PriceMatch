from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Starts the process'

    def handle(self, *args, **kwargs):
          with connection.cursor() as cursor:
              cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
