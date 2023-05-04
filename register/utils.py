from .models import UserAccount


def check_username_exists(username: str) -> bool:
    return UserAccount.objects.filter(username=username).exists()
