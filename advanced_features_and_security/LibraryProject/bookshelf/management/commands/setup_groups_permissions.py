from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from LibraryProject.bookshelf.models import Book, BookReview, ReadingList


class Command(BaseCommand):
    help = 'Set up groups and assign permissions for the bookshelf application'

    def handle(self, *args, **options):
        # Get content types for our models
        book_content_type = ContentType.objects.get_for_model(Book)
        review_content_type = ContentType.objects.get_for_model(BookReview)
        reading_list_content_type = ContentType.objects.get_for_model(ReadingList)

        # Get all permissions for our models
        book_permissions = Permission.objects.filter(content_type=book_content_type)
        review_permissions = Permission.objects.filter(content_type=review_content_type)
        reading_list_permissions = Permission.objects.filter(content_type=reading_list_content_type)

        # Create Viewers group
        viewers_group, created = Group.objects.get_or_create(name='Viewers')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Viewers group'))
        
        # Viewers can only view content
        view_permissions = []
        for perm in book_permissions.filter(codename='can_view'):
            view_permissions.append(perm)
        for perm in review_permissions.filter(codename='can_view'):
            view_permissions.append(perm)
        for perm in reading_list_permissions.filter(codename='can_view'):
            view_permissions.append(perm)
        
        viewers_group.permissions.set(view_permissions)
        self.stdout.write(self.style.SUCCESS('Assigned view permissions to Viewers group'))

        # Create Editors group
        editors_group, created = Group.objects.get_or_create(name='Editors')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Editors group'))
        
        # Editors can view, create, and edit content
        editor_permissions = []
        for perm in book_permissions.filter(codename__in=['can_view', 'can_create', 'can_edit']):
            editor_permissions.append(perm)
        for perm in review_permissions.filter(codename__in=['can_view', 'can_create', 'can_edit']):
            editor_permissions.append(perm)
        for perm in reading_list_permissions.filter(codename__in=['can_view', 'can_create', 'can_edit']):
            editor_permissions.append(perm)
        
        editors_group.permissions.set(editor_permissions)
        self.stdout.write(self.style.SUCCESS('Assigned editor permissions to Editors group'))

        # Create Admins group
        admins_group, created = Group.objects.get_or_create(name='Admins')
        if created:
            self.stdout.write(self.style.SUCCESS('Created Admins group'))
        
        # Admins have all permissions
        admin_permissions = []
        admin_permissions.extend(book_permissions)
        admin_permissions.extend(review_permissions)
        admin_permissions.extend(reading_list_permissions)
        
        admins_group.permissions.set(admin_permissions)
        self.stdout.write(self.style.SUCCESS('Assigned all permissions to Admins group'))

        self.stdout.write(
            self.style.SUCCESS('\nSuccessfully set up groups and permissions:')
        )
        self.stdout.write(f'- Viewers: {viewers_group.permissions.count()} permissions')
        self.stdout.write(f'- Editors: {editors_group.permissions.count()} permissions')
        self.stdout.write(f'- Admins: {admins_group.permissions.count()} permissions')
