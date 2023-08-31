# Generated by Django 4.1.7 on 2023-08-31 08:31

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseMessage',
            fields=[
                ('message_id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('is_read', models.BooleanField(default=False)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('thread', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateField(auto_now_add=True)),
                ('type', models.CharField(choices=[('PRIVATE', 'private'), ('GROUP', 'group')], max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TextMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=600)),
                ('base_message', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='chat.basemessage')),
            ],
        ),
        migrations.CreateModel(
            name='PrivateChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('member1', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='member1', to='accounts.account')),
                ('member2', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='member2', to='accounts.account')),
                ('thread', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='chat.chat')),
            ],
        ),
        migrations.CreateModel(
            name='PostMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('base_message', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='chat.basemessage')),
                ('post_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
        migrations.CreateModel(
            name='GroupMedia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(blank=True, default='groups/default/default.png', null=True, upload_to='groups/')),
                ('chat_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chat')),
                ('members', models.ManyToManyField(to='accounts.account')),
            ],
        ),
        migrations.CreateModel(
            name='GroupChat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('thread', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='chat.chat')),
            ],
        ),
        migrations.AddField(
            model_name='basemessage',
            name='chat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chat'),
        ),
        migrations.AddConstraint(
            model_name='privatechat',
            constraint=models.CheckConstraint(check=models.Q(('member1', models.F('member2')), _negated=True), name='no_chat_yourself'),
        ),
        migrations.AlterUniqueTogether(
            name='privatechat',
            unique_together={('member1', 'member2')},
        ),
        migrations.AddIndex(
            model_name='basemessage',
            index=models.Index(fields=['chat'], name='chat_baseme_chat_id_487229_idx'),
        ),
    ]
