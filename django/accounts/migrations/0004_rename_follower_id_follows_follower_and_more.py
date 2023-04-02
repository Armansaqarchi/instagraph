# Generated by Django 4.1.7 on 2023-04-01 13:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_account_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='follows',
            old_name='follower_id',
            new_name='follower',
        ),
        migrations.RenameField(
            model_name='follows',
            old_name='following_id',
            new_name='following',
        ),
        migrations.AddField(
            model_name='account',
            name='fr_counts',
            field=models.PositiveBigIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='FollowRQ',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('is_read', models.BooleanField(default=False)),
                ('accepted', models.CharField(choices=[('True', 'YES'), ('False', 'NO'), ('pending', 'PENDING')], default='PENDING', max_length=25)),
                ('recipient', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_set', to='accounts.account')),
                ('sender', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_set', to='accounts.account')),
            ],
        ),
    ]