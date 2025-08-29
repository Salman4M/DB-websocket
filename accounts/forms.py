from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import Profile



class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('displayname', 'image', 'info')




