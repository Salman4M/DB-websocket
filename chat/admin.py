from django.contrib import admin

# Register your models here.
from chat.models import ChatGroup,GroupMessages

admin.site.register(ChatGroup)
admin.site.register(GroupMessages)