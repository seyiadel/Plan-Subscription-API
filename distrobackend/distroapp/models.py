from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from distroapp.managers import DistroUserManager
import random
import string
from datetime import timedelta , datetime
# Create your models here.


def generate_account_number() -> int:
    numbers='543' +''.join(random.choices(string.digits, k=6))
    account_number=int(numbers)
    return account_number

class Plan(models.Model):
    name=models.CharField(max_length= 200)
    description=models.TextField() 
    price=models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField()
    date_created=models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class DistroUser(AbstractUser):
    user_id=models.UUIDField(default=uuid.uuid4, max_length=37, unique=True)
    username = None
    first_name=models.CharField(max_length=290) 
    last_name=models.CharField(max_length=23)
    email=models.EmailField(unique=True)
    account_number=models.IntegerField(default=generate_account_number,unique=True, null=True)
    plan=models.CharField(max_length=50, null = True)
    status=models.BooleanField(default=False)
    plan_start_date = models.DateTimeField(auto_created=False, auto_now_add=False, auto_now=False, blank=True, null=True)
    objects = DistroUserManager()
   
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self) -> str:
        return self.email
        
    @property
    def plan_end_date(self):
        """this is to convert plan duration (month) to days,
        the days is set to be 30 days due to company's policy"""
        month = self.plan.duration * 30
        end_date = self.plan_start_date + timedelta(days=month)
        return end_date
    
    def revert_status_to_false(self):
        """This function to revert DistroUser.status to False when
        plan_end_date is reached"""
        if not self.status:
            return
        if datetime.now() == self.plan_end_date:
            self.status == False
            return self.save(update_fields=["status"])
