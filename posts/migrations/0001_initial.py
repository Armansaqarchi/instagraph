# Generated by Django 4.2.5 on 2023-10-02 10:29

from django.db import migrations, models
import django.db.models.deletion
import taggit.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('description', models.CharField(max_length=500)),
                ('likes', models.PositiveBigIntegerField(default=0)),
                ('comments', models.PositiveBigIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('location', models.CharField(max_length=50, null=True)),
                ('tags', taggit.managers.TaggableManager(help_text='used to tag the posts for search optimizations, filtering, ...', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='tags')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_posts', to='accounts.account')),
            ],
            options={
                'db_table': 'posts',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('content', models.CharField(max_length=300)),
                ('likes_count', models.PositiveBigIntegerField(default=0)),
                ('commented_at', models.DateField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='post_comments', to='posts.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
            options={
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='MediaPost',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('content_url', models.ImageField(max_length=200, upload_to='static/images/posts')),
                ('posted_at', models.DateField(auto_now_add=True)),
                ('page_num', models.IntegerField(default=1)),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='medias', to='posts.post')),
            ],
            options={
                'db_table': 'media_post',
                'ordering': ['posted_at'],
                'unique_together': {('post_id', 'page_num')},
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('liked_at', models.DateField(auto_now_add=True)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='posts.post')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
            options={
                'db_table': 'likes',
                'ordering': ['liked_at'],
                'unique_together': {('user', 'post')},
            },
        ),
    ]
