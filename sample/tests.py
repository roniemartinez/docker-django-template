from typing import Any, List

from django.http import HttpResponse
from django.test import TestCase
from django.urls import reverse


class SampleTestCase(TestCase):
    databases: List[Any] = []

    def test_index_view(self):
        with self.settings(LANGUAGE_CODE="tl"):
            response: HttpResponse = self.client.get(reverse("sample:index"))
            self.assertContains(response, "Halimbawa ng Application")
