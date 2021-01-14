import json

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.template.loader import render_to_string

from apps.users.models import AirTrafficController, User

from .models import Chat, Forum


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.id = self.scope['url_route']['kwargs']['forum_id']
        self.room_group_name = 'forum_%s' % self.id
        # join room group
        await self.channel_layer.group_add(self.room_group_name,
                                           self.channel_name)
        # accept connection
        await self.accept()

    async def disconnect(self, close_code):
        # leave room group
        await self.channel_layer.group_discard(self.room_group_name,
                                               self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['message_type']
        chat_id = str(text_data_json["chat_id"])
        forum_id = self.scope['url_route']['kwargs']['forum_id']
        forum = await self.get_forum(forum_id)
        user = self.scope["user"]
        g_user = await self.get_atc_user(user)
        message = None
        chat = None

        if not message_type == "deletion":
            message = text_data_json['message']

        if message_type == "addition":
            chat = await self.create_chat_message(g_user, message, forum, chat_id)
            context = {'chat': chat,
                       'g_user': g_user,
                       'forum': forum,
                       'broadcast': True
                       }
            message = await self.get_message_ready(context)
            message_for_sender = await self.get_message_ready(context, for_sender=True)

        elif message_type == "edit":
            chat = await self.edit_chat_message(chat_id, message)
            context = {'chat': chat,
                       'g_user': g_user,
                       'forum': forum,
                       'broadcast': True
                       }
            message = await self.get_message_ready(context)
            message_for_sender = await self.get_message_ready(context, for_sender=True)

        elif message_type == "deletion":
            await self.delete_chat_message(chat_id)

        # send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {'type': 'chat_message',
                                   'message': message,
                                   'message_for_sender': message_for_sender,
                                   'message_type': message_type,
                                   'chat_id': chat_id,
                                   })

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))


    @database_sync_to_async
    def create_chat_message(self, g_user, message, forum, chat_id):
        reply = None
        if chat_id.isdigit() and chat_id != "0":
            reply = Chat.objects.get(active=True, id=int(chat_id))
        return Chat.objects.create(user=g_user,
                                   content=message,
                                   forum=forum,
                                   reply=reply)

    @database_sync_to_async
    def edit_chat_message(self, chat_id, message):
        chat = Chat.objects.get(id=int(chat_id))
        chat.content = message
        chat.save()
        return chat

    @database_sync_to_async
    def delete_chat_message(self, chat_id):
        if Chat.objects.filter(id=int(chat_id)).exists():
            chat = Chat.objects.get(id=int(chat_id))
            chat.delete()
        return

    @database_sync_to_async
    def get_forum(self, forum_id):
        return Forum.objects.get(id=forum_id)

    @sync_to_async
    def get_message_ready(self, context, for_sender=False):
        context['broadcast'] = True
        if for_sender:
            context['broadcast'] = False
        return render_to_string('forum/chat-box.html', context)

    @sync_to_async
    def get_atc_user(self, user: User) -> AirTrafficController:
        return AirTrafficController.objects.get(user=user)
