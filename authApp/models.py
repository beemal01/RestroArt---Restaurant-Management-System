from django.db import models
from django.contrib.auth.models import AbstractUser, Permission
# Create your models here.

Registration_Choices = [
    ('email', 'Email'),
]

class User(AbstractUser):
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, blank=True)
    registration = models.CharField(choices=Registration_Choices, default=email)


    def __str__(self):
        return self.name

