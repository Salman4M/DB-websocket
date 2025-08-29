from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User=get_user_model()

class ContentMixin(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class ChatGroup(ContentMixin):
    chat_name=models.CharField(max_length=255,unique=True)
    groupchat_name=models.CharField(max_length=255,blank=True,null=True)
    admin=models.ForeignKey(User,on_delete=models.CASCADE,related_name='admin_chat_groups')
    members=models.ManyToManyField(User,related_name='chat_groups')
    online_members=models.ManyToManyField(User,related_name='online_chat_groups',blank=True)
    private=models.BooleanField(default=False)

    def __str__(self):
        return self.chat_name
    

class GroupMessages(ContentMixin):
    group=models.ForeignKey(ChatGroup,on_delete=models.CASCADE,related_name='messages')
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name='group_messages')
    # file=models.FileField(upload_to='group_files/',blank=True,null=True)
    content=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering=['-created_at']

    def __str__(self):
        return f"Message from {self.author} in {self.group}: {self.content[:20]}"