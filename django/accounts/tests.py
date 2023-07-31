from django.test import TestCase
from django.contrib.auth.models import User
from .models import Account
from .models import Follows
from django.test import Client

from django.http.response import HttpResponseNotFound
class AuthenticationInitializerTest(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.user1 = User.objects.create_user(
            username="john_doe",
            email="johnDoe@gmail.com",
            password="johnDoe123"
        )


class LoginTest(AuthenticationInitializerTest):
    def test_login_success(self):
        data = {
            "username": "john_doe",
            "password": "johnDoe123",
        }
        response = self.client.post("/accounts/login", data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "successfully logged in")
    def test_login_fail(self):
        data = {
            "username": "john_doe",
            "password": "johnDoe1234",
        }
        response = self.client.post("/accounts/login", data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Username or password may be incorrect")
    def test_login_again(self):
        data = {
            "username": "john_doe",
            "password": "johnDoe123",
        }
        Token = self.client.post("/api/token", data).json()["access"]
        response = self.client.post("/accounts/login", data, HTTP_AUTHORIZATION = f"Bearer {Token}" , content_type= "application/json")
        self.assertEqual(response.status_code, 208)
        self.assertEqual(response.json()["detail"], "already authenticated")
    def test_login_invalid_again(self):
        data = {
            "username": "john_doe",
            "password": "johnDoe123",
        }
        Token = self.client.post("/api/token", data).json()["access"]
        response = self.client.post("/accounts/login", data, HTTP_AUTHORIZATION = f"Bearer {Token} invalid" , content_type= "application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json()["detail"], "Authorization header must contain two space-delimited values")

class SignupTest(AuthenticationInitializerTest):
    def test_signup_success(self):
        """
        when credentials are correct
        """

        data = {
            "first_name" : "Arman",
            "last_name" : "sagharchi",
            "email" : "armanDoe@gmail.com",
            "username" : "Arman",
            "password" : "Armantest"
        }
        resposne = self.client.post("/accounts/signup", data)
        self.assertEqual(resposne.status_code, 201)
        self.assertEqual(resposne.json()["message"], "user created")
    def test_signup_fail(self):
        """
        Bad request formation
        """
        data = {
            "firstname_invalid_form" : "Arman",
            "last_name" : "sagharchi",
            "email" : "armanDoe@gmail.com",
            "username" : "Arman",
            "password" : "Armantest"
        }
        response = self.client.post("/accounts/signup", data)
        self.assertEqual(response.status_code, 400)
    def test_email_exists(self):
        """
        email already exists
        """
        data = {
            "first_name" : "Arman",
            "last_name" : "sagharchi",
            "email" : "johnDoe@gmail.com",
            "username" : "Arman",
            "password" : "Armantest"
        }
        response = self.client.post("/accounts/signup", data=data)
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json()["detail"], "The Email has already been taken by another user")


class FollowListInitializerTest(TestCase):
    def setUp(self) -> None:
        self.client = Client(enforce_csrf_checks=True)
        self.user1 = User.objects.create_user(
            username="Arman",
            password="Arman1",
            email="arman.saqarchi@gmail.com"
        )
        self.user2 = User.objects.create_user(
            username="John2",
            password="john2",
            email="johnDoe@gmail.com"
        )
        self.user3 = User.objects.create_user(
            username="jane",
            password="jane2",
            email="janeDoe@gmail.com"
        )
        Follows.objects.create(
            follower = self.user2.account,
            following = self.user1.account
        )
        Follows.objects.create(
            follower = self.user3.account,
            following = self.user1.account
        )
        Follows.objects.create(
            follower = self.user1.account,
            following = self.user3.account
        )


class FollowersViewTest(FollowListInitializerTest):
    def test_followers_success(self):
        self.client.login(username = "Arman", password = "Arman1")
        response = self.client.get("/accounts/followers/7?page=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["page_obj"]), 2)

    def test_followers_no_authority(self):
        self.client.login(username = "Arman", password = "Arman2")

        response = self.client.get("/accounts/followers/1?page=1")
        self.assertEqual(response.status_code, 403)

    def test_followers_no_such_user(self):
        self.client.login(username = "Arman", password = "Arman1")
        response = self.client.get("/accounts/followers/20?page=1")
        self.assertEqual(response.status_code, 404)

class FollowingListTest(FollowListInitializerTest):
    def test_following_success(self):
        login = self.client.login(username = "John2", password = "john2")
        response = self.client.get("/accounts/followings/16")
        self.assertEqual(response.status_code, 200)

    def test_following_fail(self):
        login = self.client.login(username = "John2", password = "john2")
        response = self.client.get("/accounts/followings/12")
        self.assertEqual(response.status_code, 403)

    def test_following_not_found(self):
        login = self.client.login(username = "John2", password = "john2")
        response = self.client.get("/accounts/followings/11111")
        self.assertEqual(response.status_code, 404)
    

class FriendFollowReqTest(TestCase):
    def setUp(self):
        
