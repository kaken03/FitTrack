from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Create a regular (non-admin) owner account for gym managers'

    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, required=True, help='Username for the owner account')
        parser.add_argument('--email', type=str, required=True, help='Email for the owner account')
        parser.add_argument('--password', type=str, required=True, help='Password for the owner account')

    def handle(self, *args, **options):
        username = options['username']
        email = options['email']
        password = options['password']

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            raise CommandError(f'User "{username}" already exists')

        # Create regular user (not staff, not superuser)
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_staff=False,
                is_superuser=False
            )
            self.stdout.write(
                self.style.SUCCESS(
                    f'Owner account "{username}" created successfully! '
                    f'They can now log in at /login/ and manage their own members & plans.'
                )
            )
        except Exception as e:
            raise CommandError(f'Error creating user: {str(e)}')
