from rest_framework.test import APITestCase
from django.contrib.auth.models import User


class TestPostModelView(APITestCase):

    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username = "arman",
            password = "Armans8118",
            email = "arman.saghari81@gmail.com"
        )

    def test_post_create(self):
        post_data = {
            }
        