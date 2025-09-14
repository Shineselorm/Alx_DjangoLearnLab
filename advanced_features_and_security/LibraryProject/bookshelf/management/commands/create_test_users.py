from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from datetime import date

User = get_user_model()


class Command(BaseCommand):
    help = 'Create test users and assign them to different groups'

    def handle(self, *args, **options):
        # Create test users
        test_users = [
            {
                'email': 'viewer@example.com',
                'username': 'viewer_user',
                'first_name': 'Viewer',
                'last_name': 'User',
                'password': 'viewer123',
                'group': 'Viewers'
            },
            {
                'email': 'editor@example.com',
                'username': 'editor_user',
                'first_name': 'Editor',
                'last_name': 'User',
                'password': 'editor123',
                'group': 'Editors'
            },
            {
                'email': 'admin@example.com',
                'username': 'admin_user',
                'first_name': 'Admin',
                'last_name': 'User',
                'password': 'admin123',
                'group': 'Admins'
            },
        ]

        for user_data in test_users:
            # Create user if they don't exist
            user, created = User.objects.get_or_create(
                email=user_data['email'],
                defaults={
                    'username': user_data['username'],
                    'first_name': user_data['first_name'],
                    'last_name': user_data['last_name'],
                    'date_of_birth': date(1990, 1, 1),
                    'is_active': True,
                }
            )
            
            if created:
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(
                    self.style.SUCCESS(f'Created user: {user.email}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'User already exists: {user.email}')
                )

            # Assign user to group
            try:
                group = Group.objects.get(name=user_data['group'])
                user.groups.add(group)
                self.stdout.write(
                    self.style.SUCCESS(f'Assigned {user.email} to {group.name} group')
                )
            except Group.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'Group {user_data["group"]} does not exist')
                )

        self.stdout.write(
            self.style.SUCCESS('\nTest users created successfully!')
        )
        self.stdout.write('Login credentials:')
        self.stdout.write('- viewer@example.com / viewer123 (Viewers group)')
        self.stdout.write('- editor@example.com / editor123 (Editors group)')
        self.stdout.write('- admin@example.com / admin123 (Admins group)')
