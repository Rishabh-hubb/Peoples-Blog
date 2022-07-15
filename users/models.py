from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# Create your models here.
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    image = models.ImageField(default='profile_pics/default.jpg',upload_to='profile_pics')

    def __str__(self):
        return f"{self.user.username} Profile"


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 400 or img.width > 400:
            output_size = (400,400)
            img.thumbnail(output_size)
            img.save(self.image.path)

