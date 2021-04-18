from http import HTTPStatus
from typing import Any, List

from django.core import exceptions
from django.core.handlers.wsgi import WSGIRequest
from django.http import Http404, HttpResponse
from django.test import TestCase, override_settings
from django.urls import include, path
from django.views import View

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
    path("error/<int:code>/", ErrorView.as_view(), name="error"),
]

handler400 = views.Handle400View.as_view()
handler403 = views.Handle403View.as_view()
handler404 = views.Handle404View.as_view()
handler500 = views.handle500_view


@override_settings(ROOT_URLCONF=__name__)
class JobCreateViewTestCase(TestCase):
    databases: List[str] = ["default"]

    def test_get_400(self) -> None:
        with self.settings(DEBUG=False):
            response: HttpResponse = self.client.get("/error/400/")
            self.assertContains(response, "400 Bad Request", status_code=HTTPStatus.BAD_REQUEST)
            self.assertContains(
                response, "Bad request syntax or unsupported method", status_code=HTTPStatus.BAD_REQUEST
            )

    def test_get_403(self) -> None:
        with self.settings(DEBUG=False):
            response: HttpResponse = self.client.get("/error/403/")
            self.assertContains(response, "403 Forbidden", status_code=HTTPStatus.FORBIDDEN)
            self.assertContains(
                response, "Request forbidden -- authorization will not help", status_code=HTTPStatus.FORBIDDEN
            )

    def test_get_404(self) -> None:
        with self.settings(DEBUG=False):
            response: HttpResponse = self.client.get("/error/404/")
            self.assertContains(response, "404 Not Found", status_code=HTTPStatus.NOT_FOUND)
            self.assertContains(response, "Nothing matches the given URI", status_code=HTTPStatus.NOT_FOUND)

    def test_get_500(self) -> None:
        response: HttpResponse = self.client.get("/error/500/")
        self.assertContains(response, "500 Internal Server Error", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        self.assertContains(response, "Server got itself in trouble", status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
