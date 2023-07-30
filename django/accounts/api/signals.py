from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from accounts.models import Account




@receiver(post_save, sender = User, dispatch_uid = 'create_profile_alongwith_user')
def create_Account(sender, instance, created, **kwargs):
    if instance.is_superuser:
        return
    user = None
    if created:
        user = instance
        Account.objects.create(
            user = user,
        )



    return user


