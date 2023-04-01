from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from accounts.models import Account




@receiver(post_save, sender = User, dispatch_uid = 'create_profile_alongwith_user')
def create_Account(sender, instance, created, **kwargs):
    if created:

        user = instance
        Account.objects.create(
            user = user,
            email = user.email,
            username = user.username,
            first_name = user.first_name,
            last_name = user.last_name,
        )



    return user


