import secrets
from http import HTTPStatus
from typing import List
from unittest import mock

from django.contrib.auth import get_user_model
from django.core import mail
from django.http import HttpResponse
from django.template import loader
from django.test import TestCase
from django.urls import reverse


class RegisterViewTestCase(TestCase):
    databases: List[str] = ["default"]

    def test_get(self) -> None:
        response: HttpResponse = self.client.get(reverse("sample:register"))
        self.assertContains(response, "Register")
        self.assertContains(response, "Username")
        self.assertContains(response, "First name")
        self.assertContains(response, "Last name")
        self.assertContains(response, "Email address")
        self.assertContains(response, "Password")
        self.assertContains(response, "Password confirmation")
        self.assertContains(response, "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.")
        self.assertContains(response, "Your password can’t be too similar to your other personal information.")
        self.assertContains(response, "Your password must contain at least 8 characters.")
        self.assertContains(response, "Your password can’t be a commonly used password.")
        self.assertContains(response, "Your password can’t be entirely numeric.")
        self.assertContains(response, "Enter the same password as before, for verification.")

    @mock.patch.object(mail, "send_mail")
    @mock.patch.object(loader, "render_to_string")
    @mock.patch.object(secrets, "token_urlsafe")
    def test_post(
        self, mock_token_urlsafe: mock.Mock, mock_render_to_string: mock.Mock, mock_send_mail: mock.Mock
    ) -> None:
        with self.settings(EMAIL_HOST_USER="ron@sample.ron.sh"):
            mock_token_urlsafe.return_value = "sample-token"
            mock_render_to_string.return_value = "HTML message"
            response: HttpResponse = self.client.post(
                reverse("sample:register"),
                {
                    "username": "username",
                    "first_name": "John",
                    "last_name": "Doe",
                    "email": "user@sample.ron.sh",
                    "password1": "iff42bR6TX6vCp",
                    "password2": "iff42bR6TX6vCp",
                },
            )
            user = get_user_model().objects.get(username="username")
            self.assertRedirects(
                response,
                reverse("sample:registered", kwargs={"uuid": user.user_extension.uuid}),
                status_code=HTTPStatus.FOUND,
                target_status_code=HTTPStatus.OK,
                fetch_redirect_response=True,
            )
            mock_token_urlsafe.assert_called()
            mock_render_to_string.assert_called_with(
                "sample/verify-email.html", {"verification_url": "http://testserver/verify/sample-token/"}
            )
            mock_send_mail.assert_called_with(
                subject="Verify your account!",
                message="""Verify your account!

Use the following link to verify your account: http://testserver/verify/sample-token/

Cheers!
Ronie Martinez
""",
                from_email="Ronie Martinez <ron@sample.ron.sh>",
                recipient_list=["user@sample.ron.sh"],
                html_message="HTML message",
            )

    def test_post_different_passwords(self) -> None:
        response: HttpResponse = self.client.post(
            reverse("sample:register"),
            {
                "username": "username",
                "first_name": "John",
                "last_name": "Doe",
                "email": "user@sample.ron.sh",
                "password1": "iff42bR6TX6vCp",
                "password2": "R7kBv45jkYERk3",
            },
        )
        self.assertContains(response, "The two password fields didn’t match.")

    def test_post_missing_fields(self) -> None:
        response: HttpResponse = self.client.post(
            reverse("sample:register"),
            {},
        )
        self.assertContains(response, "This field is required.")

    def test_post_duplicate_email(self) -> None:
        user = get_user_model().objects.create(username="username", email="user@sample.ron.sh")
        user.save()
        response: HttpResponse = self.client.post(
            reverse("sample:register"),
            {
                "username": "username2",
                "first_name": "John",
                "last_name": "Doe",
                "email": "user@sample.ron.sh",
                "password1": "iff42bR6TX6vCp",
                "password2": "iff42bR6TX6vCp",
            },
        )
        self.assertContains(response, "Email already exists!")
