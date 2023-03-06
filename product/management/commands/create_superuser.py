from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        username = 'levelup'
        email = 'levelup@example.com'
        password = 'PASSWORD'

        if not User.objects.filter(username=username).exists():
            admin = User.objects.create_superuser(
                email=email, username=username, password=password)
        else:
            print('Admin account has already been initialized.')
