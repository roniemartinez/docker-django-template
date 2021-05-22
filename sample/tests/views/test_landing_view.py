from typing import List

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class LandingViewTestCase(TestCase):
    databases: List[str] = ["default"]

    def test_get(self) -> None:
        user = get_user_model().objects.create(username="username")
        user.set_password("password")
        user.save()
        user.extension.verified = True
        user.save()
        self.client.login(username="username", password="password")
        response: HttpResponse = self.client.get(reverse("sample:landing"))
        self.assertContains(response, "<h2>Docker+Django Template</h2>", html=True)
