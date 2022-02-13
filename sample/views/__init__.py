from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .errors import (
    ErrorView,
    Handle400View,
    Handle403View,
    Handle404View,
    Handle500View,
    HandleErrorView,
    handle500_view,
)

__all__ = [
    "ErrorView",
    "Handle400View",
    "Handle403View",
    "Handle404View",
    "Handle500View",
    "HandleErrorView",
    "handle500_view",
]


class LandingView(TemplateView):
    template_name = "sample/landing.html"


@method_decorator(login_required, name="dispatch")
class ProtectedView(TemplateView):
    template_name = "sample/protected.html"
