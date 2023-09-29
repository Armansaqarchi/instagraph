# Generated by Django 4.2.5 on 2023-09-29 09:18

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
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('date_of_birth', models.DateField(auto_now_add=True)),
                ('bio', models.TextField(max_length=500)),
                ('gender', models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Unknown', 'Prefer not to say')], default='Prefer not to say', max_length=100)),
                ('is_private', models.BooleanField(default=False)),
                ('followers', models.PositiveBigIntegerField(default=0)),
                ('following', models.PositiveBigIntegerField(default=0)),
                ('last_seen_posts', models.DateField(auto_now_add=True)),
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
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('content_url', models.ImageField(default='static/images/stories', max_length=200, upload_to='users/story/default.png')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('expires_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_stories', to='accounts.account')),
            ],
            options={
                'db_table': 'stories',
            },
        ),
        migrations.CreateModel(
            name='MediaProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('profile_image', models.ImageField(default='static/images/users/profile/default.png', max_length=200, null=True, upload_to='users/')),
                ('set_at', models.DateField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
            options={
                'db_table': 'profile',
                'ordering': ['set_at'],
            },
        ),
        migrations.CreateModel(
            name='Follows',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
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
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('recipient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_set', to='accounts.account')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_set', to='accounts.account')),
            ],
            options={
                'db_table': 'follow_requests',
                'ordering': ['sent_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='follows',
            constraint=models.CheckConstraint(check=models.Q(('follower', models.F('following')), _negated=True), name='dont_follow_yourself'),
        ),
        migrations.AddConstraint(
            model_name='follows',
            constraint=models.UniqueConstraint(fields=('follower', 'following'), name='only_follow_once'),
        ),
        migrations.AddConstraint(
            model_name='followrq',
            constraint=models.CheckConstraint(check=models.Q(('sender', models.F('recipient')), _negated=True), name='dont request yourself'),
        ),
    ]
