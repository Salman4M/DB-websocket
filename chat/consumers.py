import json
from chat.models import ChatGroup,GroupMessages
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string

import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from django.shortcuts import get_object_or_404
from chat.models import ChatGroup, GroupMessages

class ChatRoomConsumer(WebsocketConsumer):
    ## when user connects to the chat
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, chat_name=self.chatroom_name)
        # print(self.scope['url_route'])
        #results: {'args': (), 'kwargs': {'chatroom_name': 'new-chat'}}
        # print(self.scope['url_route']['kwargs'])
        #results: {'chatroom_name': 'new-chat'}

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )
        # print(f"CHANNEL LAYER: {self.channel_layer}")
        #RESULTS: CHANNEL LAYER: RedisChannelLayer(hosts=[{'host': '127.0.0.1', 'port': 6379}])
        if self.user not in self.chatroom.online_members.all():
            self.chatroom.online_members.add(self.user)

        self.accept()

    def disconnect(self, close_code):
        ## when user disconnects from the chat

        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )
        if self.user in self.chatroom.online_members.all():
            self.chatroom.online_members.remove(self.user)


    def receive(self, text_data):
        #text_data is a JSON string sent by the client via a Websocket
        data = json.loads(text_data)
        content = data['content'].strip()
        if not content:
            return
        ## we take the value and create it
        message = GroupMessages.objects.create(
            content=content,
            author=self.user,
            group=self.chatroom,
        )
        ##then we send it to event to use in message handler
        event = {
            "type": "message_handler",
            "message_id": message.id,
        }
        # Send the event to the channel layer group 
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_name,
            event
        )


    def message_handler(self, event):
        ## when a message is received we take the message
        message_id = event['message_id']
        message = GroupMessages.objects.get(id=message_id)
        ## send the message to the WebSocket to all connected clients
        # now we format the message and send it to the WebSocket to that chatroom
        self.send(text_data=json.dumps({
            "author": message.author.username,
            "content": message.content,
            "timestamp": str(message.created_at),
        }))
