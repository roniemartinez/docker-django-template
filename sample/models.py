import uuid
from typing import Any

from django.conf import settings
from django.db import models
from django.db.models import signals
from django.dispatch import receiver


class UserExtension(models.Model):
    """
    Additional user information
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name="extension",
    )
    uuid = models.UUIDField(
        max_length=64,
        default=uuid.uuid4,
        editable=False,
    )
    verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)


@receiver(signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_or_save_user_extension(
    sender: settings.AUTH_USER_MODEL,
    instance: settings.AUTH_USER_MODEL,
    created: bool,
    **kwargs: Any,
) -> None:
    if created:
        UserExtension.objects.create(user=instance)
    else:
        instance.extension.save()
