from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a custom superuser with additional fields'

    def add_arguments(self, parser):
        parser.add_argument('--email', type=str, help='Email address')
        parser.add_argument('--username', type=str, help='Username')
        parser.add_argument('--password', type=str, help='Password')
        parser.add_argument('--first-name', type=str, help='First name')
        parser.add_argument('--last-name', type=str, help='Last name')
        parser.add_argument('--date-of-birth', type=str, help='Date of birth (YYYY-MM-DD)')

    def handle(self, *args, **options):
        email = options.get('email') or 'admin@example.com'
        username = options.get('username') or 'admin'
        password = options.get('password') or 'admin123'
        first_name = options.get('first_name') or 'Admin'
        last_name = options.get('last_name') or 'User'
        date_of_birth_str = options.get('date_of_birth') or '1990-01-01'
        
        try:
            date_of_birth = date.fromisoformat(date_of_birth_str)
        except ValueError:
            self.stdout.write(
                self.style.ERROR('Invalid date format. Use YYYY-MM-DD')
            )
            return

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.WARNING(f'User with email {email} already exists')
            )
            return

        user = User.objects.create_superuser(
            email=email,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth
        )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created superuser: {user.email}'
            )
        )
