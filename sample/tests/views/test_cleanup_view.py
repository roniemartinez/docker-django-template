from http import HTTPStatus
from typing import List

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class CleanUpViewTestCase(TestCase):
    databases: List[str] = ["default"]

    def test_get(self) -> None:
        response: HttpResponse = self.client.get(reverse("sample:cleanup"))
        self.assertEqual(response.status_code, HTTPStatus.NO_CONTENT)
