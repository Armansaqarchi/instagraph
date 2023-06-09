# Generated by Django 4.1.7 on 2023-07-05 17:04

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_remove_account_fr_counts_remove_account_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account_stories', to='accounts.account'),
        ),
        migrations.CreateModel(
            name='MediaStory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('story_image', models.ImageField(default='static/images/stories', max_length=200, null=True, upload_to='static/images/users/story/default.png')),
                ('added_at', models.DateField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='story_set', to='accounts.account')),
            ],
            options={
                'db_table': 'story_image',
                'ordering': ['added_at'],
            },
        ),
    ]
