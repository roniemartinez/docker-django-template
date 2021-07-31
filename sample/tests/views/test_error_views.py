from http import HTTPStatus
from typing import Any

import pytest
from django.core import exceptions
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponse
from django.test import Client
from django.urls import include, path
from django.views import View
from pytest_django.asserts import assertContains
from pytest_django.fixtures import SettingsWrapper

from sample import views


class ErrorView(View):
    @staticmethod
    def get(request: WSGIRequest, **kwargs: Any) -> HttpResponse:
        code: int = kwargs.get("code", 0)
        exception = {400: exceptions.BadRequest, 403: exceptions.PermissionDenied, 404: Http404}.get(code)
        if exception:
            raise exception
        # FIXME:
        #  "raise Exception" logs "ERROR    django.request:log.py:224 Internal Server Error: /error/500/"
        #  but the handler does not return the provided template
        # raise Exception
        return views.handle500_view(request)


urlpatterns = [
    path("", include("sample.urls")),
    path("accounts/", include("allauth.urls")),
    path("error/<int:code>/", ErrorView.as_view(), name="error"),
]

handler400 = views.Handle400View.as_view()
handler403 = views.Handle403View.as_view()
handler404 = views.Handle404View.as_view()
handler500 = views.handle500_view


@pytest.mark.urls(__name__)
def test_400(settings: SettingsWrapper, client: Client) -> None:
    settings.DEBUG = False
    response: HttpResponse = client.get(path="/error/400/")
    assertContains(response, "400 Bad Request", status_code=HTTPStatus.BAD_REQUEST)
    assertContains(response, "Bad request syntax or unsupported method", status_code=HTTPStatus.BAD_REQUEST)


@pytest.mark.urls(__name__)
def test_403(settings: SettingsWrapper, client: Client) -> None:
    settings.DEBUG = False
    response: HttpResponse = client.get(path="/error/403/")
    assertContains(response, "403 Forbidden", status_code=HTTPStatus.FORBIDDEN)
    assertContains(response, "Request forbidden -- authorization will not help", status_code=HTTPStatus.FORBIDDEN)


@pytest.mark.urls(__name__)
def test_404(settings: SettingsWrapper, client: Client) -> None:
    settings.DEBUG = False
    response: HttpResponse = client.get(path="/error/404/")
    assertContains(response, "404 Not Found", status_code=HTTPStatus.NOT_FOUND)
    assertContains(response, "Nothing matches the given URI", status_code=HTTPStatus.NOT_FOUND)


@pytest.mark.urls(__name__)
def test_500(client: Client) -> None:
    response: HttpResponse = client.get(path="/error/500/")
    assertContains(response, "500 Internal Server Error", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
    assertContains(response, "Server got itself in trouble", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
