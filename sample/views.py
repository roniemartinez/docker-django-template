from django.conf import settings
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import translation


async def index(request: WSGIRequest) -> HttpResponse:
    translation.activate("tl")  # use translation.activate() to change language dynamically
    response = render(request, "sample/index.html")
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, translation.get_language())
    return response


async def cleanup(request: WSGIRequest) -> HttpResponse:
    # do something
    return HttpResponse()
