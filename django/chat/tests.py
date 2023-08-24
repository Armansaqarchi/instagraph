from django.test import TestCase
from channels.testing import WebsocketCommunicator, ChannelsLiveServerTestCase
from .consumers import ChatConsumer
from django.contrib.auth.models import User
from instagraph.asgi import application

class TestChat(ChannelsLiveServerTestCase):


    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username="Arman",
            password="Armans8118"
        )
        res = self.client.post("/api/token", data={"username" : "Arman", "password": "Armans8118"})
        self.valid_access = res.json()["access"]

    async def test_connect_consumer(self):
        communicator = WebsocketCommunicator(
            application,
            "chat/",  # Adjust the URL to match your routing configuration
            headers={"Authorization": f"Bearer {self.valid_access}", "chat_room": 1234},
        )

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

    async def test_send_consumer(self):
        pass


