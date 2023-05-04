from django.contrib import admin
from .models import Transaction, MoneyRequest, Notification

# Register your models here.
admin.site.register(Transaction)
admin.site.register(MoneyRequest)
admin.site.register(Notification)