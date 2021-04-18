from gettext import gettext
from http import HTTPStatus
from typing import Any, Dict

from django import http
from django.contrib import auth
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView as AuthLoginView
from django.core.cache import cache
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, TemplateView

from sample.forms import RegisterForm
from sample.models import UserExtension
from sample.utils import get_main_url, send_verification_email


class LandingView(TemplateView):
    template_name = "sample/landing.html"


class ProtectedView(TemplateView):
    template_name = "sample/protected.html"


class LoginView(AuthLoginView):
    template_name = "sample/login.html"

    def form_valid(self, form: AuthenticationForm) -> http.HttpResponseRedirect:
        user = form.get_user()
        user_extension, _ = UserExtension.objects.get_or_create(user=user)
        if form.is_valid() and not (user_extension.verified or user.is_staff):
            form.errors[NON_FIELD_ERRORS] = form.error_class([gettext("User not verified!")])
            return render(self.request, self.template_name, context={"form": form})
        return super(LoginView, self).form_valid(form)


class RegisterView(CreateView):
    model = auth.get_user_model()
    form_class = RegisterForm
    template_name = "sample/register.html"

    def get_success_url(self) -> str:
        user_extension, _ = UserExtension.objects.get_or_create(user=self.object)
        return reverse("sample:registered", kwargs={"uuid": user_extension.uuid})

    def form_valid(self, form: RegisterForm) -> http.HttpResponseRedirect:
        response = super(RegisterView, self).form_valid(form)
        user_extension, _ = UserExtension.objects.get_or_create(user=self.object)
        main_url = get_main_url(self.request)
        send_verification_email(main_url, user_extension.uuid, self.object.email)
        return response


class RegisteredView(TemplateView):
    template_name = "sample/registered.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super(RegisteredView, self).get_context_data(**kwargs)
        context_data["email"] = UserExtension.objects.get(uuid=kwargs.get("uuid")).user.email
        return context_data


class VerifyAccountView(TemplateView):
    template_name = "sample/verify.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context_data = super(VerifyAccountView, self).get_context_data(**kwargs)
        verification_token = kwargs.get("token")
        key = f"verify-token-{verification_token}"
        uuid = cache.get(key)
        if uuid:
            context_data["verified"] = True
            UserExtension.objects.filter(uuid=uuid).update(verified=True)
            cache.delete(key)
        return context_data


class CleanUpView(View):
    def get(self, request: WSGIRequest) -> HttpResponse:
        # do something
        return HttpResponse()


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
