import logging
import os

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

logger = logging.getLogger(__name__)

ADMIN_USERNAME = os.getenv('ADMIN_USERNAME')
ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD')

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **options):
        if not User.objects.filter(username=ADMIN_USERNAME).exists():
            admin = User.objects.create_superuser(
                username=ADMIN_USERNAME, password=ADMIN_PASSWORD)
        else:
            logger.info('Admin account has already been initialized.')
