# accounts/models.py
from django.contrib.auth.models import AbstractUser
from phone_field import PhoneField
from phonenumber_field.modelfields import PhoneNumberField
from django.db import models

class CustomUser(AbstractUser):
    BLOC_CHOICES = [
        ('b1', 'B1'),
        ('b2', 'B2'),
        ('b3', 'B3'),
        ('b4', 'B4'),
        ('b5', 'B5'),
        ('b6', 'B6'),
        ('b7', 'B7'),
        ('b8', 'B8'),
        ('b9', 'B9'),
        ('b10', 'B10'),
    ]
    address = models.CharField(max_length=100, blank=True)
    phone_number = PhoneNumberField(blank=True)
    feecharge = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    bloc = models.CharField(max_length=3, choices=BLOC_CHOICES, default='b1')
    has_changed_password = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # Si c'est une nouvelle instance (création)
            self.set_password('admin')  # Définir le mot de passe par défaut
            self.has_changed_password = False
        super().save(*args, **kwargs)