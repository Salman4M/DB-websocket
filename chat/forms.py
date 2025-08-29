from chat.models import ChatGroup,GroupMessages
from django import forms



class ChatMessageCreateForm(forms.ModelForm):
    class Meta:
        model = GroupMessages
        fields = ['content']
        widgets = {
            'content' : forms.TextInput(attrs={'placeholder': 'Add message ...', 'class': 'p-4 text-black', 'maxlength' : '300', 'autofocus': True }),
        }
        
