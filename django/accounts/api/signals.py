from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from accounts.models import Account




@receiver(post_save, sender = User, dispatch_uid = 'create_profile_alongwith_user')
def create_user(sender, instance, created, **kwargs):
    if created:
        
        first_name = kwargs['username'] if 'username' in kwargs else ''
        last_name = kwargs['lastname']  if 'lastname' in kwargs else ''
        date_of_birth = kwargs['date_of_birth'] if 'date_of_birth' in kwargs else None
        bio = kwargs['bio'] if 'bio' in kwargs else ''
        

        user = instance
        account = account.objects.create(
            user = user,
            email = user.email,
            username = user.username,
            bio = bio,
            date_of_birth = date_of_birth,
            first_name = first_name,
            last_name = last_name
        )


