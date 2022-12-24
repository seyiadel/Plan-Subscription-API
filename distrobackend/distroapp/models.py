from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from distroapp.managers import DistroUserManager
import random
import string
# Create your models here.


def generate_account_number():
    numbers='543' +''.join(random.choices(string.digits, k=6))
    account_number=int(numbers)
    return account_number

class Plan(models.Model):
    name=models.CharField(max_length= 200)
    description=models.TextField() 
    price=models.IntegerField()
    date_created=models.DateTimeField(auto_now_add=True)

class DistroUser(AbstractUser):
    user_id=models.CharField(default=uuid.uuid4, max_length=24, unique=True)
    username = None
    first_name=models.CharField(max_length=290)
    last_name=models.CharField(max_length=23)
    email=models.EmailField(unique=True)
    account_number=models.IntegerField(default=generate_account_number(), null=True)
    plan=models.ForeignKey(Plan, on_delete=models.CASCADE, null=True)
    status=models.BooleanField(default=False)

    objects = DistroUserManager()
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self) -> str:
        return self.email