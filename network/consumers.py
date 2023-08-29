import json
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rest.settings')
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
django.setup()

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Chat, Message, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name, 
            self.channel_name
        )


    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get("message")
        message_sender = text_data_json.get("from")
        message_receiver = text_data_json.get("to")

        sender = User.objects.get(username=message_sender)
        receiver = User.objects.get(username=message_receiver)
        chats = Chat.objects.all()
        chat = None

        for i in chats:
            if receiver in i.participants.all() and sender in i.participants.all():
                chat = i
                break
            
        new_message = Message(sender=sender, message=message, chat=chat)

        new_message.save()

        await self.channel_layer.group_send(
            self.room_group_name, {
                "type": "chat_message",
                "sender": message_sender,
                "message": message
            }
        )

    async def chat_message(self, event):
        sender = event["sender"]
        message = event["message"]

        # Send message to WebSocket
        await self.send(text_data=json.dumps(
            {
                "sender": sender,
                "message": message
            }
        ))
