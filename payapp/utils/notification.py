from register.models import UserAccount
from ..models import Notification

def notify(user:UserAccount,title:str,message:str):
    return Notification.objects.create(
        user=user,
        title=title,
        message=message
    )