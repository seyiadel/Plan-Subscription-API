from django.contrib.auth.models import BaseUserManager

class DistroUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, account_number, password=None):
        if not email:
            raise ValueError("Enter your valid email address!")
        distrouser=self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
            account_number=account_number
        )
        distrouser.set_password(password)
        distrouser.save()
        return distrouser

    def create_superuser(self, first_name, last_name, email, password=None):
        if not email:
            raise ValueError("Enter a valid email address")
        distrouser= self.model(
            first_name=first_name,
            last_name=last_name,
            email=self.normalize_email(email),
        )
        distrouser.is_active = True
        distrouser.is_staff=True
        distrouser.is_superuser =True
        distrouser.set_password(password)
        distrouser.save()
        return distrouser
