# Generated by Django 4.1.3 on 2023-06-26 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0005_alter_mediapost_content_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='location',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
