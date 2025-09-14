# Generated manually to add custom permissions to models

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LibraryProject.bookshelf', '0002_customuser'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={
                'ordering': ['-created_at'],
                'permissions': [
                    ('can_view', 'Can view books'),
                    ('can_create', 'Can create books'),
                    ('can_edit', 'Can edit books'),
                    ('can_delete', 'Can delete books'),
                ],
                'verbose_name': 'Book',
                'verbose_name_plural': 'Books',
            },
        ),
        migrations.AlterModelOptions(
            name='bookreview',
            options={
                'ordering': ['-created_at'],
                'permissions': [
                    ('can_view', 'Can view book reviews'),
                    ('can_create', 'Can create book reviews'),
                    ('can_edit', 'Can edit book reviews'),
                    ('can_delete', 'Can delete book reviews'),
                ],
                'verbose_name': 'Book Review',
                'verbose_name_plural': 'Book Reviews',
            },
        ),
        migrations.AlterModelOptions(
            name='readinglist',
            options={
                'ordering': ['-created_at'],
                'permissions': [
                    ('can_view', 'Can view reading lists'),
                    ('can_create', 'Can create reading lists'),
                    ('can_edit', 'Can edit reading lists'),
                    ('can_delete', 'Can delete reading lists'),
                ],
                'verbose_name': 'Reading List',
                'verbose_name_plural': 'Reading Lists',
            },
        ),
    ]
