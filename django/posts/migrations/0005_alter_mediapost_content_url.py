# Generated by Django 4.1.7 on 2023-06-10 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_mediapost_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediapost',
            name='content_url',
            field=models.ImageField(max_length=200, upload_to='static/images/posts'),
        ),
    ]
