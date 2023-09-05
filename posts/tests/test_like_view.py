from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from ..models import Like, Post

class LikeTestCase(APITestCase):


    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username = "Arman",
            password = "Armans8118"
        )
        self.user2 = User.objects.create_user(
            username = "Arman2",
            password = "Armans8118"
        )
        self.user3 = User.objects.create_user(
            username = "Arman3",
            password = "Armans8118"
        )
        self.post1 = Post.objects.create(
            user = self.user1.account,
            description = "some fake description",
            location = "bruh abad"
        )
        self.like1 = Like.objects.create(
            user = self.user2.account,
            post = self.post1
        )


    def test_create_like(self):
        login = self.client.login(username = "Arman", password = "Armans8118")
        self.assertTrue(login)
        res = self.client.get(f"/posts/likes/create/{self.post1.id}")
        self.assertEqual(res.status_code, 201)
    

    def test_create_like_twice(self):
        login = self.client.login(username = "Arman", password = "Armans8118")
        self.assertTrue(login)
        res1 = self.client.get(f"/posts/likes/create/{self.post1.id}")
        res2 = self.client.get(f"/posts/likes/create/{self.post1.id}")
        self.assertEqual(res1.status_code, 201)
        self.assertEqual(res2.status_code, 409)

    def test_delete_like_success(self):
        login = self.client.login(username = "Arman2", password = "Armans8118")
        self.assertTrue(login)
        res = self.client.delete(f"/posts/likes/delete/{self.like1.id}")
        self.assertEqual(res.status_code, 204)


    def test_delete_like_no_permission(self):
        login = self.client.login(username = "Arman", password = "Armans8118")
        self.assertTrue(login)
        res = self.client.delete(f"/posts/likes/delete/{self.like1.id}")
        self.assertEqual(res.status_code, 403)

    # def test_list_like_success(self):
    #     login = self.client.login(username = "Arman", password = "Armans8118")
    #     self.assertTrue(login)
    #     res = self.client.delete(f"/posts/likes/delete/{self.like1.id}")
    #     self.assertEqual(res.status_code, 403)