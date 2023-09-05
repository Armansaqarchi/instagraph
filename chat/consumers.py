from channels.generic.websocket import AsyncWebsocketConsumer
from .models.messageModel import TextMessage, BaseMessage
from .exception_handler import ws_exception_handler
from django.db import transaction
from asgiref.sync import sync_to_async
from .chatSerializer import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):

    serializer_class = MessageSerializer

    def dispatch(self, message):
        try:
            return super().dispatch(message)
        except Exception as exc:
            context = self.scope
            ws_exception_handler(exc=exc, context=context)


    async def connect(self):
        self.chat = self.scope["chat"]
        self.user = self.scope["user"]
        if self.user.is_authenticated:
            await self.accept()
            await self.channel_layer.group_add(
                str(self.scope["chat"].thread),
                self.channel_name
            )


    async def disconnect(self, close_code):
        # Perform any necessary cleanup when a connection is closed
        self.channel_layer.group_discard(
            self.chat.thread,
            self.channel_name
        )

    async def receive(self, text_data):

        
        msg = await self.create_message(text_data=text_data)
        serialized_message = self.serializer_class(instance=msg)
        await self.channel_layer.group_send(
            str(self.chat.thread),
            {
                "type" : "send",
                "text" : serialized_message.data
            }
        )


    async def create_message(self, text_data = None, bytea_data = None):
        if text_data:
            return await self.create_text_message(text_data)
        elif bytea_data:
            return await self.create_bytea_message(bytea_data)

    
    @sync_to_async
    @transaction.atomic
    def create_text_message(self, text_data):
        base_msg = BaseMessage.objects.create(
            chat = self.chat,
            sender = self.user.account
        )

        text_msg = TextMessage.objects.create(
            base_message = base_msg,
            content = text_data
        )

        return text_msg
    

    @sync_to_async
    @transaction.atomic
    def create_bytea_messsage(self, bytea_message):
        pass
