# Generated by Django 4.1.7 on 2023-04-10 19:09

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
                ('email', models.EmailField(max_length=50, unique=True)),
                ('date_of_birth', models.DateField(auto_now_add=True)),
                ('bio', models.TextField(max_length=500)),
                ('is_private', models.BooleanField(default=False)),
                ('followers', models.PositiveBigIntegerField(default=0)),
                ('following', models.PositiveBigIntegerField(default=0)),
                ('posts', models.PositiveBigIntegerField(default=0)),
                ('fr_counts', models.PositiveBigIntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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
            name='Message',
            fields=[
                ('message_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('content', models.TextField(max_length=600)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('recipient_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipient_set', to='accounts.account')),
                ('sender_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('start_following_at', models.DateField(auto_now_add=True)),
                ('follower', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='follower_set', to='accounts.account')),
                ('following', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='following_set', to='accounts.account')),
            ],
            options={
                'db_table': 'follows',
                'ordering': ['start_following_at'],
            },
        ),
        migrations.CreateModel(
            name='FollowRQ',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_read', models.BooleanField(default=False)),
                ('accepted', models.CharField(choices=[('True', 'YES'), ('False', 'NO'), ('pending', 'PENDING')], default='PENDING', max_length=25)),
                ('sent_at', models.DateField(auto_now_add=True)),
                ('recipient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_set', to='accounts.account')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_set', to='accounts.account')),
            ],
            options={
                'db_table': 'follow_requests',
                'ordering': ['sent_at'],
            },
        ),
    ]
