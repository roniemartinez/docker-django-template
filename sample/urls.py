from django.urls import path

from sample import views

app_name = "sample"


urlpatterns = [
    path("", views.index, name="index"),
    path("cleanup/", views.cleanup, name="cleanup"),
]
