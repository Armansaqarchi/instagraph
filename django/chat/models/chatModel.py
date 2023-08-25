# Create your models here.
from django.db import models
from uuid import uuid4
from accounts.models import Account


class Chat(models.Model):

    CHAT_TYPE = (
        ("PRIVATE", "private"),
        ("GROUP", "group")
    )

    thread = models.UUIDField(default=uuid4, primary_key=True, editable=False, blank=False, null=False)
    created = models.DateField(auto_now_add=True)
    type = models.CharField(choices=CHAT_TYPE, max_length=50)

class GroupChat(models.Model):
    chat_id = models.OneToOneField(Chat, unique=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

class PrivateChat(models.Model):
    chat_id = models.OneToOneField(Chat, unique=True, on_delete=models.CASCADE)
    member1 = models.OneToOneField(Account, on_delete=models.DO_NOTHING, related_name="member1")
    member2 = models.OneToOneField(Account, on_delete=models.DO_NOTHING, related_name="member2")

    class Meta:
        unique_together = ["member1", "member2"]
        constraints = [
            models.CheckConstraint(check = ~models.Q(member1 = models.F("member2")), name="no_chat_yourself")
        ]

class GroupMedia(models.Model):
    picture = models.ImageField(upload_to="groups/", null=True, blank=True, default="groups/default/default.png")
    chat_id = models.ForeignKey(Chat, on_delete=models.CASCADE)
    members = models.ManyToManyField(Account)