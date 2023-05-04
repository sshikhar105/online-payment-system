from django.db import models
from django.contrib.auth.models import AbstractUser

from decimal import Decimal

from payapp.models import Currency


# Create your models here.
class UserAccount(AbstractUser):
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(1000.00), blank=True)
    base_currency = models.CharField(max_length=5, choices=Currency.choices, default=Currency.GBP)


    @property
    def full_name(self):
        if len(self.first_name)>0 or len(self.last_name)>0:
            return f'{self.first_name} {self.last_name}'
        return self.username

    def __str__(self):
        return self.full_name
