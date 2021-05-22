from http import HTTPStatus
from typing import List

from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class LoginViewTestCase(TestCase):
    databases: List[str] = ["default"]

    def test_get(self) -> None:
        response: HttpResponse = self.client.get(reverse("sample:login"))
        self.assertContains(response, "Login")
        self.assertContains(response, "Username")
        self.assertContains(response, "Password")

    def test_post(self) -> None:
        user = get_user_model().objects.create(username="username")
        user.set_password("password")
        user.extension.verified = True
        user.save()

        response: HttpResponse = self.client.post(
            reverse("sample:login"), {"username": "username", "password": "password"}, follow=True
        )
        self.assertRedirects(
            response,
            reverse("sample:protected"),
            status_code=HTTPStatus.FOUND,
            target_status_code=HTTPStatus.OK,
            fetch_redirect_response=True,
        )

    def test_post_unverified(self) -> None:
        user = get_user_model().objects.create(username="username")
        user.set_password("password")
        user.save()

        response: HttpResponse = self.client.post(
            reverse("sample:login"), {"username": "username", "password": "password"}, follow=True
        )
        self.assertContains(response, "Login")
        self.assertContains(response, "User not verified!")
        self.assertContains(response, "Username")
        self.assertContains(response, "Password")

    def test_post_incorrect(self) -> None:
        user = get_user_model().objects.create(username="username")
        user.set_password("password")
        user.save()

        response: HttpResponse = self.client.post(
            reverse("sample:login"), {"username": "username", "password": "incorrect"}, follow=True
        )
        self.assertContains(response, "Login")
        self.assertContains(
            response, "Please enter a correct username and password. Note that both fields may be case-sensitive."
        )
        self.assertContains(response, "Username")
        self.assertContains(response, "Password")
