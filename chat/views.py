from django.shortcuts import render,get_object_or_404
from django.http import Http404
# Create your views here.
from chat.forms import ChatMessageCreateForm

from chat.models import ChatGroup,GroupMessages

def chat_view(request,chat_name='new-chat'):
    chat_group=get_object_or_404(ChatGroup,chat_name=chat_name)
    chat_messages=chat_group.messages.all()
    form=ChatMessageCreateForm()
    
    other_user=None
    if chat_group.private:
        if request.user not in chat_group.members.all():
            raise Http404("You are not allowed to access this chat.")
        for member in chat_group.members.all():
            if member!=request.user:
                other_user=member
                break

    if chat_group.groupchat_name:
        if request.user not in chat_group.members.all():
            chat_group.members.add(request.user)
        

    if request.htmx:
        form=ChatMessageCreateForm(request.POST)
        if form.is_valid():
            messages=form.save(commit=False)
            messages.author=request.user
            messages.group=chat_group
            messages.save()
            context={
                'messages':messages,
                'user':request.user
            }
            return render(request,'chat/partial_message.html',context)


    context={
        "chat_messages":chat_messages,
        'form':form,
        'other_user':other_user,
        'chat_group':chat_group,
        }

    return render(request,'chat/chat.html',context)


def chatroom_edit_view(request,chatroom_name):
    chatroom=get_object_or_404(ChatGroup,chat_name=chatroom_name)
    context={"chatroom":chatroom}

    return render(request,'chat/chatroom_edit.html',context)