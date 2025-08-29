import json
from chat.models import ChatGroup,GroupMessages
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user=self.scope['user']
        self.chatroom_name=self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom=get_object_or_404(ChatGroup,chat_name=self.chatroom_name)
        async_to_sync(self.channel_layer.group_add)(self.chatroom_name,self.channel_name)

        if self.user not in self.chatroom.online_members.all():
            self.chatroom.online_members.add(self.user)
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard(self.chatroom_name,self.channel_name))
        if self.user in self.chatroom.online_members.all():
            self.chatroom.online_members.remove(self.user)
    

    def receive(self, text_data):
        data = json.loads(text_data)
        content=data['content']

        message = GroupMessages.objects.create(
            content=content,
            author=self.user,
            group=self.chatroom,
            )
        event={
            "type":"message_handler",
            "message":message.id,
        }
        async_to_sync(self.channel_layer.group_send)(self.chatroom_name,event)


    def message_handler(self,event):
        message_id=event['message_id']
        message=GroupMessages.objects.get(id=message_id)
        context={
            "message":message,
            'user':self.user,
            "chat_group":self.chatroom,
        }
        
        html=render_to_string('chat/partial_message.html',context)
        self.send(text_data=html)