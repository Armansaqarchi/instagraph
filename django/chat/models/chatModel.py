# Create your models here.
from django.db import models
from uuid import uuid4
from accounts.models import Account




class Chat(models.Model):

    CHAT_TYPE = (
        ("PRIVATE", "private"),
        ("GROUP", "group")
    )

    thread = models.AutoField()
    created = models.DateTimeField(auto_now_add=True, editable=False)
    type = models.CharField(choices=CHAT_TYPE)

class GroupChat(models.Model):
    chat_id = models.OneToOneField(unique=True)
    name = models.CharField()

class PrivateChat(models.Model):
    chat_id = models.OneToOneField(unique=True)
    member1 = models.OneToOneField(Account, on_delete=models.DO_NOTHING)
    member2 = models.OneToOneField(Account, on_delete=models.DO_NOTHING)


    class Meta:
        constaints = [
            models.CheckConstraint(~models.Q(member1 = models.F("member2")))
        ]

class GroupMedia(models.Model):
    picture = models.ImageField(upload_to="groups/", null=True, blank=True, default="groups/default/default.png")
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    members = models.ManyToManyField(Account)