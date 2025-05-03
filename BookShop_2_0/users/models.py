from django.contrib.auth.models import AbstractUser
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)



    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    photo = models.ImageField(upload_to='user-photo/')
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='users',blank=True,null=True,default=None)

    def __str__(self):
        return self.username



