from typing import List

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class RegisteredViewTestCase(TestCase):
    databases: List[str] = ["default"]

    def test_get(self) -> None:
        user = get_user_model().objects.create(username="username", email="user@sample.ron.sh")
        user.set_password("password")
        user.extension.verified = True
        user.save()

        response: HttpResponse = self.client.get(reverse("sample:registered", kwargs={"uuid": user.extension.uuid}))
        self.assertContains(response, "Registration Successful!")
        self.assertContains(response, "We have sent a verification email to")
        self.assertContains(response, "user@sample.ron.sh")
