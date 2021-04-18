import uuid

from django.conf import settings
from django.db import models


class UserExtension(models.Model):
    """
    Additional user information
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True, related_name="user_extension"
    )
    uuid = models.UUIDField(max_length=64, default=uuid.uuid4, editable=False)
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
