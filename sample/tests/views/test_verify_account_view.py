import secrets
from typing import List

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from sample.models import UserExtension


class VerifyAccountViewTestCase(TestCase):
    databases: List[str] = ["default"]

    def test_get(self) -> None:
        user = get_user_model().objects.create(username="username")
        user.set_password("password")
        user.save()
        user_extension = UserExtension(user=user, verified=False)
        user_extension.save()

        token = secrets.token_urlsafe()
        cache.set(f"verify-token-{token}", user_extension.uuid, 5)

        response: HttpResponse = self.client.get(reverse("sample:verify", kwargs={"token": token}))

        self.assertContains(response, "User Verified!")
        self.assertContains(response, "You may now start using Docker+Django Template.")
        self.assertTrue(UserExtension.objects.get(user=user).verified)

    def test_get_not_exist(self) -> None:
        user = get_user_model().objects.create(username="username")
        user.set_password("password")
        user.save()
        user_extension = UserExtension(user=user, verified=False)
        user_extension.save()

        token = secrets.token_urlsafe()

        response: HttpResponse = self.client.get(reverse("sample:verify", kwargs={"token": token}))

        self.assertContains(response, "Invalid token!")
        self.assertContains(response, "Sorry but we cannot verify your account.")
        self.assertFalse(UserExtension.objects.get(user=user).verified)
