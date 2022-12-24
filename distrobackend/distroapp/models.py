from django.db import models
from django.contrib.auth.models import AbstractBaseUser
import uuid
from distroapp.managers import DistroUserManager
# Create your models here.

class Plan(models.Model):
    name=models.CharField(max_length= 200)
    description=models.TextField() 
    price=models.IntegerField()
    date_created=models.DateTimeField(auto_now_add=True)

class DistroUser(AbstractBaseUser):
    user_id=models.CharField(default=uuid.uuid4, unique=True)
    first_name=models.CharField(max_length=290)
    last_name=models.CharField()
    email=models.EmailField()
    account_number=models.IntegerField()
    plan=models.ForeignKey(Plan, on_delete=models.CASCADE)
    status=models.BooleanField(default=False)

    objects = DistroUserManager()
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self) -> str:
        return self.email