from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.auth import get_user_model

User=get_user_model()



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    displayname = models.CharField(max_length=100,blank=True,null=True)
    image = models.ImageField(blank=True,null=True)
    info = models.TextField(blank=True,null=True)


    def __str__(self):
        return self.user.username
    

    @property
    def name(self):
            if self.displayname:
                 return self.displayname
            return self.user.username
    
    @property
    def prof_image(self):
        if self.image:
            return self.image.url
        return f'{settings.STATIC_URL}images/image.jpg'