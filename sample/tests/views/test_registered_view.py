from typing import List

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse

from sample.models import UserExtension


class RegisteredViewTestCase(TestCase):
    databases: List[str] = ["default"]

    def test_get(self) -> None:
        user = get_user_model().objects.create(username="username", email="user@sample.ron.sh")
        user.set_password("password")
        user.save()
        user_extension = UserExtension(user=user, verified=True)
        user_extension.save()

        response: HttpResponse = self.client.get(reverse("sample:registered", kwargs={"uuid": user_extension.uuid}))
        self.assertContains(response, "Registration Successful!")
        self.assertContains(response, "We have sent a verification email to")
        self.assertContains(response, "user@sample.ron.sh")
