# Generated by Django 4.1.7 on 2023-09-02 15:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_rename_created_at_comment_commented_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='sender',
            new_name='user',
        ),
    ]
