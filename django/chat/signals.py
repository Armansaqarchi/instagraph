from django.dispatch import receiver
from django.db.models.signals import pre_save
from .models.chatModel import PrivateChat, GroupChat, Chat


@receiver(pre_save, sender=PrivateChat)
@receiver(pre_save, sender=GroupChat)
def after_private_group_created(sender, instance, **kwargs):

    chat = Chat.objects.create(
        type= Chat.CHAT_TYPE[0][0]
    )
    instance.thread = chat

    return instance


