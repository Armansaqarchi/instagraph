from rest_framework.test import APITestCase, APIClient
from accounts.models import MediaProfile
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile

class MediaProfileTestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username= "Arman",
            password= "Armans8118"
        )


    def test_profile_creation(self):
        data = {
            "firstname" : "Arman",
            "lastname" : "sagharchi",
            "username" : "armans81",
            "bio" : "Arman sagharchi as you all know",
            "gender" : "Male"
        }
        file = {}

        

        with open("accounts/tests/test_media_profile.png", "rb") as image_file:
            uploaded_image = SimpleUploadedFile(
                name='image.jpg',
                content=image_file.read(),
                content_type='image/jpeg'
            )

        res = self.client.put("/accounts/profile/1", data=data, content_type="application/multipart", FILES = {"image" : uploaded_image})
        print(res.json())