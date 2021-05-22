from typing import List

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class ProtectedViewTestCase(TestCase):
    databases: List[str] = ["default"]

    def test_get(self) -> None:
        response: HttpResponse = self.client.get(reverse("sample:protected"))
        self.assertRedirects(response, expected_url=reverse("sample:login") + "?next=%2Fprotected%2F")

    def test_get_logged_in(self) -> None:
        user = get_user_model().objects.create(username="username")
        user.set_password("password")
        user.extension.verified = True
        user.save()
        self.client.login(username="username", password="password")
        response: HttpResponse = self.client.get(reverse("sample:protected"))
        self.assertContains(response, "You are logged in as username")
