from django.test import TestCase
from channels.testing import WebsocketCommunicator, ChannelsLiveServerTestCase
from .consumers import ChatConsumer
from django.contrib.auth.models import User
from instagraph.asgi import application
from .models.chatModel import PrivateChat, GroupChat

class TestChat(ChannelsLiveServerTestCase):


    def setUp(self) -> None:
        self.user1 = User.objects.create_user(
            username="Arman",
            password="Armans8118"
        )
        self.user2 = User.objects.create_user(
            username= "Arman2",
            password= "Armans8118"
        )
        self.private_chat1 = PrivateChat.objects.create(
            member1 = self.user1.account,
            member2 = self.user2.account
        )
        res = self.client.post("/api/token", data={"username" : "Arman", "password": "Armans8118"})
        self.valid_access1 = res.json()["access"]
        res = self.client.post("/api/token", data={"username" : "Arman2", "password": "Armans8118"})
        self.valid_access2 = res.json()["access"]
        

    async def test_connect_consumer(self):

        communicator = WebsocketCommunicator(
            application,
            f"chat/?thread={self.private_chat1.thread.thread}",  # Adjust the URL to match your routing configuration
            headers={"Authorization": f"Bearer {self.valid_access1}"},
        )

        connected, _ = await communicator.connect()
        self.assertTrue(connected)

    async def test_send_consumer(self):
        communicator1 = WebsocketCommunicator(
            application,
            f"chat/?thread={self.private_chat1.thread.thread}",  # Adjust the URL to match your routing configuration
            headers={"Authorization": f"Bearer {self.valid_access1}"},
        )

        communicator2 = WebsocketCommunicator(
            application,
            f"chat/?thread={self.private_chat1.thread.thread}",  # Adjust the URL to match your routing configuration
            headers={"Authorization": f"Bearer {self.valid_access2}"},
        )

        await communicator1.connect()
        await communicator2.connect()

        # Test sending text
        await communicator1.send_to(text_data="hello")
        response = await communicator2.receive_output()
        print(response)
        


