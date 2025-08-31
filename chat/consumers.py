import json
from chat.models import ChatGroup, GroupMessages
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404
from asgiref.sync import async_to_sync

class ChatRoomConsumer(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.chatroom_name = self.scope['url_route']['kwargs']['chatroom_name']
        self.chatroom = get_object_or_404(ChatGroup, chat_name=self.chatroom_name)

        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_name,
            self.channel_name
        )

        if self.user not in self.chatroom.online_members.all():
            self.chatroom.online_members.add(self.user)

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_name,
            self.channel_name
        )
        if self.user in self.chatroom.online_members.all():
            self.chatroom.online_members.remove(self.user)

    def receive(self, text_data):
        data = json.loads(text_data)

        if 'content' in data:  # message
            content = data['content'].strip()
            if content:
                message = GroupMessages.objects.create(
                    content=content,
                    author=self.user,
                    group=self.chatroom,
                )
                event = {
                    "type": "message_handler",
                    "message_id": message.id,
                }
                async_to_sync(self.channel_layer.group_send)(
                    self.chatroom_name,
                    event
                )

        elif 'typing' in data:  # typing
            typing_status = data['typing']
            async_to_sync(self.channel_layer.group_send)(
                self.chatroom_name,
                {
                    "type": "typing_status",
                    "typing": typing_status,
                    "user": self.user.username,   
                }
            )

    # def message_handler(self, event):
    #     message_id = event['message_id']
    #     message = GroupMessages.objects.get(id=message_id)
    #     self.send(text_data=json.dumps({
    #         "action": "new_message",
    #         "author": message.author.username,
    #         "content": message.content,
    #         "timestamp": str(message.created_at),
    #     }))


    def typing_status(self, event):
        self.send(text_data=json.dumps({
            "action": "typing",
            "typing": event['typing'],
            "user": event['user'],   # 👈 send user too
        }))
