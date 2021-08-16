from http import HTTPStatus
from typing import Any

from django import http
from django.core.handlers.wsgi import WSGIRequest
from django.template.response import TemplateResponse
from django.views import View
from django.views.generic import TemplateView


class HandleErrorView(TemplateView):
    template_name = "sample/error.html"
    error: HTTPStatus

    def get(self, request: WSGIRequest, *args: Any, **kwargs: Any) -> TemplateResponse:
        context = self.get_context_data(**kwargs)
        return self.render_to_response({**context, "error": self.error}, status=self.error)


class Handle400View(HandleErrorView):
    error = HTTPStatus.BAD_REQUEST


class Handle403View(HandleErrorView):
    error = HTTPStatus.FORBIDDEN


class Handle404View(HandleErrorView):
    error = HTTPStatus.NOT_FOUND


class Handle500View(HandleErrorView):
    error = HTTPStatus.INTERNAL_SERVER_ERROR


def handle500_view(request: WSGIRequest) -> http.HttpResponse:
    return Handle500View.as_view()(request)


class ErrorView(View):
    """
    This is only used for manual testing of error handlers.
    """

    @staticmethod
    def get(request: WSGIRequest, **kwargs: Any) -> None:  # pragma: no cover
        from django.core import exceptions

        code: int = kwargs.get("code", 0)
        raise {400: exceptions.BadRequest, 403: exceptions.PermissionDenied, 404: http.Http404}.get(code, Exception)
