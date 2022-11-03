from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Initialization test users'

    def handle(self, *args, **options):
        User.objects.create_user(
            username='user1',
            password='user1'
        )
        User.objects.create_user(
            username='user2',
            password='user2'
        )
        print('Test users created successfully.')
