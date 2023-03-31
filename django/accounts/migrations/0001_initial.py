# Generated by Django 4.1.7 on 2023-03-30 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('date_of_birth', models.DateField(auto_now_add=True)),
                ('bio', models.TextField(max_length=500)),
                ('followers', models.PositiveBigIntegerField(default=0)),
                ('following', models.PositiveBigIntegerField(default=0)),
                ('posts', models.PositiveBigIntegerField(default=0)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'accounts',
                'ordering': ['date_of_birth'],
            },
        ),
        migrations.CreateModel(
            name='Story',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('content_url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
            options={
                'db_table': 'stories',
            },
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start_following_at', models.DateField(auto_now_add=True)),
                ('follower_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower_id', to='accounts.account')),
                ('following_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following_id', to='accounts.account')),
            ],
            options={
                'db_table': 'follows',
                'ordering': ['start_following_at'],
            },
        ),
    ]