from django.urls import re_path
from chat import consumers

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<chatroom_name>[-\w]+)/$", consumers.ChatRoomConsumer.as_asgi()),
]
