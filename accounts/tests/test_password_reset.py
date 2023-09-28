from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class ResetPasswordTestCase(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username = "Arman",
            password = "Armans8118",
            email = "arman.saghari81@gmail.com"
        )

    def test_reset_password(self) -> None:
        response = self.client.post("/accounts/profile/forgot_password", {"to_email": self.user1.email})
        self.assertEqual(response.status_code, 200)
        print(response.json())