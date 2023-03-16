# accounts/models.py
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

class CustomUser(AbstractUser):
    address = models.CharField(max_length=100, blank=True)
    phone_number = PhoneNumberField(blank=True)
    feecharge = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    # add additional fields in here

    def __str__(self):
        return self.username