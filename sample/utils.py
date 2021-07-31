from django.conf import settings


def display_username(user: settings.AUTH_USER_MODEL) -> str:
    return f"@{user.username}"
