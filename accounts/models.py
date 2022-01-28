from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=30, unique=True, primary_key= True)
    phone_number = models.CharField(max_length=11, unique=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    bio = models.CharField(max_length=100, blank=True)
    profile_image = models.ImageField(null = True, blank = True, default= 'default.jpg')

    followers = models.ManyToManyField(User, related_name="following", null = True)

