# Generated by Django 4.1.7 on 2023-07-10 16:24

import accounts.models
import chat.models
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '__first__'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('posts', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseMessage',
            fields=[
                ('message_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('message_type', models.CharField(choices=[(1, 'post_message'), (2, 'text_message')], max_length=50)),
                ('is_read', models.BooleanField()),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('object_id', models.PositiveIntegerField()),
                ('content_type', models.ForeignKey(limit_choices_to={'model_in': (accounts.models.Account, chat.models.Group)}, on_delete=django.db.models.deletion.CASCADE, related_name='recipient_set', to='contenttypes.contenttype')),
                ('sender_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.account')),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('group_id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TextMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=600)),
                ('message_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='chat.basemessage')),
            ],
        ),
        migrations.CreateModel(
            name='PostMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='chat.basemessage')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
        migrations.AddIndex(
            model_name='basemessage',
            index=models.Index(fields=['object_id', 'content_type'], name='chat_baseme_object__dcddc2_idx'),
        ),
        migrations.AddIndex(
            model_name='basemessage',
            index=models.Index(fields=['sender_id', 'object_id', 'content_type'], name='chat_baseme_sender__95f5d3_idx'),
        ),
        migrations.AddIndex(
            model_name='basemessage',
            index=models.Index(fields=['sender_id', 'object_id', 'content_type', 'sent_at'], name='chat_baseme_sender__5efa5f_idx'),
        ),
    ]
