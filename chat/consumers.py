import json
from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timesince import timesince

from .templatetags.chat_tags import initials
from .models import Message, Room
from account.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f'chat_{self.room_name}'
        self.user = self.scope['user']

        # join channel room or room group
        
        await self.get_room()
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

        # Inform user on staff user join chat room
        if self.user.is_staff and (self.room.status == Room.WAITING or self.user.id == self.room.agent_id):
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "user_update",
                    "name": self.user.name,
                }
            )

    async def disconnect(self, close_code):
        # Leave channel room or group
        self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        if not self.user.is_staff:
            await self.set_room_closed()

    async def receive(self, text_data):
        # Receives message from websocket front end
        text_data_json = json.loads(text_data)
        type = text_data_json['type']
        message = text_data_json['message']
        agent = text_data_json['agent']
        name = text_data_json['name']

        if type == "message":
            new_message = await self.create_message(name, message, agent)
            # send message to group room
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type": "chat_message",
                    "name":name,
                    "message": message,
                    "agent": agent,
                    "initials": initials(name),
                    "created_at": timesince(new_message.created_at)
                }
            )
        elif type == "update":
            # send update to room
            await self.channel_layer.group_send(
                self.room_group_name, {
                    "type":"writing_message",
                    "message": message,
                    "name": name,
                    "agent": agent,
                    "initials": initials(name),
                }
            )

    async def chat_message(self, event):
        # send message to websocket frontend
        await self.send(text_data=json.dumps({
            "type": event['type'],
            "name": event['name'],
            "message": event['message'],
            "agent": event['agent'],
            "initials": event['initials'],
            "created_at": event['created_at']
        }))

    async def writing_message(self, event):
        await self.send(text_data=json.dumps({
            "type": event['type'],
            "name": event['name'],
            "message": event['message'],
            "agent": event['agent'],
            "initials": event['initials'],
        }))

    async def user_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "staff_user_join",
            "name": event['name'],
        }))

    @sync_to_async
    def get_room(self):
        self.room = Room.objects.get(uuid=self.room_name)

    @sync_to_async
    def create_message(self, sent_by, message, agent):
        message = Message.objects.create(sent_by=sent_by, content=message)

        if agent:
            requested_user = User.objects.get(id=agent)
            message.created_by = requested_user
            if not self.room.agent:
                self.room.agent = requested_user
                self.room.status = Room.ACTIVE
                self.room.save()
            message.save()

        self.room.messages.add(message)
        return message
    
    @sync_to_async
    def set_room_closed(self):
        self.room = Room.objects.get(uuid=self.room_name)
        self.room.status = Room.CLOSED
        self.room.save()