# Generated by Django 4.1.3 on 2023-06-26 07:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_mediaprofile_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='fr_counts',
        ),
        migrations.RemoveField(
            model_name='account',
            name='posts',
        ),
    ]
