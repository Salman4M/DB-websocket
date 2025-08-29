from django.dispatch import receiver
from django.db.models.signals import post_save,pre_save
from django.contrib.auth import get_user_model
from accounts.models import Profile
User=get_user_model()

@receiver(post_save,sender=User)
def create_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)



@receiver(pre_save,sender=User)
def lowcase_username(sender,instance,**kwargs):
    if instance.username:
        instance.username=instance.username.lower()


