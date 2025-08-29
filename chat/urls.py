from django.urls import path
from chat import views

urlpatterns=[
    path('', views.chat_view, name='chat'),
    path('edit/<str:chatroom_name>/',views.chatroom_edit_view,name='edit-chatroom'),
]