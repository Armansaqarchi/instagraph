from channels.generic.websocket import AsyncWebsocketConsumer
import json


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Perform any necessary setup when a connection is established
        await self.accept()

    async def disconnect(self, close_code):
        # Perform any necessary cleanup when a connection is closed
        pass

    async def receive(self, text_data):
        # Handle incoming messages from the client
        print("dsfagsags", self.scope)
        await self.send(text_data=text_data)

    async def echo(self, event):
        # Handle the 'echo' event, which is triggered by the test case
        message = event['message']
        await self.send(text_data=message)