import secrets
from typing import List

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class VerifyAccountViewTestCase(TestCase):
    databases: List[str] = ["default"]

    def test_get(self) -> None:
        user = get_user_model().objects.create(username="username")
        user.set_password("password")
        user.save()

        token = secrets.token_urlsafe()
        cache.set(f"verify-token-{token}", user.extension.uuid, 5)

        response: HttpResponse = self.client.get(reverse("sample:verify", kwargs={"token": token}))
        user.refresh_from_db()

        self.assertContains(response, "User Verified!")
        self.assertContains(response, "You may now start using Docker+Django Template.")
        self.assertTrue(user.extension.verified)

    def test_get_not_exist(self) -> None:
        user = get_user_model().objects.create(username="username")
        user.set_password("password")
        user.save()

        token = secrets.token_urlsafe()

        response: HttpResponse = self.client.get(reverse("sample:verify", kwargs={"token": token}))
        user.refresh_from_db()

        self.assertContains(response, "Invalid token!")
        self.assertContains(response, "Sorry but we cannot verify your account.")
        self.assertFalse(user.extension.verified)