from django.http import HttpResponse
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertContains


def test_landing_page(client: Client) -> None:
    response: HttpResponse = client.get(path=reverse("sample:landing"))
    assertContains(response, "<h2>Docker+Django Template</h2>", html=True)
