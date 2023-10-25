from typing import Optional
from django.contrib.auth.backends import ModelBackend


class CustomModelBackend(ModelBackend):
    """
    to user more oop concepts, the authenticate method does not need to refuse users having is_active set to False,
    activation of users is handled by otp codes so even the authetnication was successful, users are not logged in 
    till their activation is verified
    """

    def user_can_authenticate(self, user) -> bool:
        return True