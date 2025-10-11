# Generated migration for posts app

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the post', max_length=200, verbose_name='title')),
                ('content', models.TextField(help_text='Main content of the post', verbose_name='content')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the post was created', verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the post was last updated', verbose_name='updated at')),
                ('author', models.ForeignKey(help_text='User who created this post', on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(help_text='Content of the comment', verbose_name='content')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Timestamp when the comment was created', verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Timestamp when the comment was last updated', verbose_name='updated at')),
                ('author', models.ForeignKey(help_text='User who wrote this comment', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(help_text='Post this comment belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='posts.post')),
            ],
            options={
                'verbose_name': 'comment',
                'verbose_name_plural': 'comments',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['-created_at'], name='posts_post_created_idx'),
        ),
        migrations.AddIndex(
            model_name='post',
            index=models.Index(fields=['author'], name='posts_post_author_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['post', 'created_at'], name='posts_comme_post_id_created_idx'),
        ),
        migrations.AddIndex(
            model_name='comment',
            index=models.Index(fields=['author'], name='posts_comme_author_idx'),
        ),
    ]

