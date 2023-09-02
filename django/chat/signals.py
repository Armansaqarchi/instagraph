from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from .models.chatModel import PrivateChat, GroupChat, Chat
from .models.messageModel import BaseMessage


@receiver(pre_save, sender=PrivateChat)
@receiver(pre_save, sender=GroupChat)
def after_private_group_created(sender, instance, created, **kwargs):
    """
    Private chat and Group chat have a disjoint specialization in databsae scheam.
    Thus, every private chat and group chat have an associated 'basic chat' which 
    defines the basics of chatroom
    """
    if not created:
        return
    chat = Chat.objects.create(
        type= Chat.CHAT_TYPE[0][0]
    )
    instance.thread = chat
    return instance


@receiver(post_save, sender = BaseMessage)
def after_message_sent(sender, instance, created, **kwargs):

    """
    one way to order the chats is to store the last message
    by having the last message, we will be able to order the chats based on the last message or interaction
    in the chat
    """
    if not created:
        return    
    chat = instance.chat
    chat.last_message = instance
    chat.save()

    return instance





