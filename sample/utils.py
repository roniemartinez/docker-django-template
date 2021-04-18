import secrets
from typing import Callable, Dict
from urllib.parse import urljoin

from django import http
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core import mail
from django.core.cache import cache
from django.core.handlers.wsgi import WSGIRequest
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy

VERIFICATION_TOKEN_EXPIRY = 86_400  # 24 hours


def is_verified_user_or_staff(user: User) -> bool:
    from sample.models import UserExtension

    user_extension, _ = UserExtension.objects.get_or_create(user=user)
    return user_extension.verified or user.is_staff


def verified_login_required(view_func: Callable) -> http.HttpResponseRedirect:
    login_url = reverse_lazy("sample:login")
    _verified_login_required = user_passes_test(is_verified_user_or_staff, login_url=login_url)
    return login_required(_verified_login_required(view_func), login_url=login_url)


def get_main_url(request: WSGIRequest) -> str:
    return f"{request.scheme}://{request.get_host()}"


def get_email_message(context: Dict[str, str]) -> str:
    return gettext_lazy(
        """Verify your account!

Use the following link to verify your account: {verification_url}

Cheers!
Ronie Martinez
"""
    ).format(**context)


def send_verification_email(main_url: str, uuid: str, recipient: str) -> None:
    verification_token = secrets.token_urlsafe()
    cache.set(f"verify-token-{verification_token}", uuid, VERIFICATION_TOKEN_EXPIRY)
    verify_url = reverse("sample:verify", kwargs={"token": verification_token})
    context = {"verification_url": urljoin(main_url, verify_url)}

    message = get_email_message(context)
    html_message = loader.render_to_string("sample/verify-email.html", context)

    mail.send_mail(
        subject="Verify your account!",
        message=message,
        from_email=f"Ronie Martinez <{settings.EMAIL_HOST_USER}>",
        recipient_list=[recipient],
        html_message=html_message,
    )
