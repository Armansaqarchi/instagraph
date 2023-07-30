from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class AuthenticationTest(TestCase):
    def setUp(self):
            self.client = Client(enforce_csrf_checks=True)
            self.user1 = User.objects.create_user(
                username="john_doe",
                email="johnDoe@gmail.com",
                password="johnDoe123"
            )
            self.account1 = 


class LoginTest(AuthenticationTest):
    
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

class SignupTest(AuthenticationTest):
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
        resposne = self.client.post("/accounts/signup", data)
        self.assertEqual(resposne.status_code, 400)
    def test_email_exists(self):
        """
        email already exists
        """
        data = {
            "firstname" : "Arman",
            "last_name" : "sagharchi",
            "email" : "armanDoe@gmail.com",
            "username" : "Arman",
            "password" : "Armantest"
        }