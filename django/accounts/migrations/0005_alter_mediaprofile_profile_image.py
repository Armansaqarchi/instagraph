# Generated by Django 4.1.7 on 2023-06-10 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_account_last_seen_posts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediaprofile',
            name='profile_image',
            field=models.ImageField(default='static/images/users/profile/default.png', max_length=200, null=True, upload_to='static/images/users/'),
        ),
    ]