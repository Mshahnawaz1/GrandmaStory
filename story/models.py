from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    # add fields for follower, following etc
    pass

class Response(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subject_user")
    input = models.CharField(max_length=10000 , blank=False)
    response = models.CharField(max_length=10000 , blank=False)

    def __str__(self):
        return f"{self.input}"