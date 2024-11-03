from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    display_picture = models.ImageField(upload_to='profile_photo/', null=True, blank=True)

    def __str__(self):
        return self.email