from django.db import models


# Create your models here.
class Currency(models.TextChoices):
    GBP='GBP','British Pound'
    USD='USD','United States Dollar'
    EUR='EUR','Euro'

class MoneyRequestStatus(models.TextChoices):
    APPROVED='APPROVED','Approved'
    DENIED='DENIED','Denied'
    PENDING='PENDING','Pending'

class Transaction(models.Model):
    sender=models.ForeignKey('register.UserAccount', on_delete=models.CASCADE, related_name='sender')
    recipient=models.ForeignKey('register.UserAccount', on_delete=models.CASCADE, related_name='recipient')
    amount=models.DecimalField(decimal_places=2,max_digits=10)
    sender_balance=models.DecimalField(decimal_places=2,max_digits=10)
    recipient_balance=models.DecimalField(decimal_places=2,max_digits=10)
    currency=models.CharField(max_length=5,choices=Currency.choices,default=Currency.USD)
    datetime=models.DateTimeField(auto_now_add=True)

class MoneyRequest(models.Model):
    sender=models.ForeignKey('register.UserAccount', on_delete=models.CASCADE, related_name='request_sender')
    recipient=models.ForeignKey('register.UserAccount', on_delete=models.CASCADE, related_name='request_recipient')
    amount=models.DecimalField(decimal_places=2,max_digits=10)
    currency=models.CharField(max_length=5,choices=Currency.choices,default=Currency.USD)
    datetime=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=10,choices=MoneyRequestStatus.choices,default=MoneyRequestStatus.PENDING)

class Notification(models.Model):
    user=models.ForeignKey('register.UserAccount', on_delete=models.CASCADE, related_name='notification_user')
    datetime=models.DateTimeField(auto_now_add=True)
    message=models.TextField(default="")
    title=models.TextField(default="")