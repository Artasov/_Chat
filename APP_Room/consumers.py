import datetime
import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.conf import settings
from django.contrib.auth.models import User

from .models import Room, Message


def serialize_date_for_chat(date):
    if isinstance(date, (datetime.date, datetime.datetime)):
        return date.strftime("%Y/%m/%d %H:%M:%S")


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        # Info about a connected users
        await self.add_connected_user(username=self.scope['user'],
                                      room=self.room_name)
        count_connected_users = await self.get_count_connected_users(room=self.room_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_count_connected_users',
                'count_connected_users': count_connected_users,
            }
        )

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        # Info about a connected users
        await self.del_connected_user(username=self.scope['user'],
                                      room=self.room_name)
        count_connected_users = await self.get_count_connected_users(room=self.room_name)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_count_connected_users',
                'count_connected_users': count_connected_users,
            }
        )

    # Receive the message from WS
    async def receive(self, text_data):
        data = dict(json.loads(text_data))
        if data.get('pagination'):
            message_count = data.get('message_count')
            pagination_new_msgs = await self.get_pagination_new_msgs(
                room=self.room_name, number_new_first_msg=message_count)
            if pagination_new_msgs is None:
                return
            await self.send(text_data=json.dumps({
                'pagination': pagination_new_msgs,
            }))
            return

        message = data['message']
        if len(message) < 1:
            return
        if data.get('message_temp_id'):
            message_temp_id = data['message_temp_id']
        else:
            message_temp_id = 0
        username = data['username']
        room = data['room']

        new_msg: Message = await self.create_message(username, room, message)
        # Send the message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message_temp_id': message_temp_id,
                'message': new_msg.content,
                'username': new_msg.user.username,
                'date': serialize_date_for_chat(new_msg.date_added)
            }
        )

    async def send_count_connected_users(self, event):
        count_connected_users = event['count_connected_users']
        # Send the count_connected_users to WS
        await self.send(text_data=json.dumps({
            'count_connected_users': count_connected_users,
        }))

    # Receive the message from room group
    async def chat_message(self, event):
        message_temp_id = event['message_temp_id']
        message = event['message']
        username = event['username']
        date = event['date']
        # Send the message to WS
        await self.send(text_data=json.dumps({
            'message_temp_id': message_temp_id,
            'message': message,
            'username': username,
            'date': date
        }))

    @database_sync_to_async
    def create_message(self, username, room, message) -> Message:
        user = User.objects.get(username=username)
        room = Room.objects.get(slug=room)
        return Message.objects.create(user=user, room=room, content=message)

    @database_sync_to_async
    def add_connected_user(self, username, room):
        room = Room.objects.get(slug=room)
        room.users.add(User.objects.get(username=username))

    @database_sync_to_async
    def del_connected_user(self, username, room):
        room = Room.objects.get(slug=room)
        room.users.remove(User.objects.get(username=username))

    @database_sync_to_async
    def get_count_connected_users(self, room) -> Room:
        return Room.objects.get(slug=room).users.count()

    @database_sync_to_async
    def get_pagination_new_msgs(self, room, number_new_first_msg):
        msgs_count = Message.objects.count()
        if number_new_first_msg >= msgs_count:
            return None
        number_new_last_msg = number_new_first_msg + settings.PAGINATION_MSGS_LIMIT
        if msgs_count < number_new_last_msg:
            number_new_last_msg = msgs_count
        messages = Message.objects.filter(
            room=Room.objects.get(slug=room)
        ).reverse()[number_new_first_msg:number_new_last_msg]
        return [m.as_json() for m in messages]
