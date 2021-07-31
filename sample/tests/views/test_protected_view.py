from http import HTTPStatus

import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertContains, assertRedirects


@pytest.mark.django_db
def test_protected_page(client: Client) -> None:
    user = get_user_model().objects.create(username="username")

    client.force_login(user)
    response = client.get(path=reverse("sample:protected"))
    assert response.status_code == HTTPStatus.OK
    assertContains(response, "You are logged in as username")


@pytest.mark.django_db
def test_protected_page_not_logged_in(client: Client) -> None:
    response = client.get(path=reverse("sample:protected"))
    assertRedirects(
        response,
        expected_url=reverse("account_login") + "?next=%2Fprotected%2F",
        status_code=HTTPStatus.FOUND,
        target_status_code=HTTPStatus.OK,
    )
