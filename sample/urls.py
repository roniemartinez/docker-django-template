from django.urls import path

from sample import views

app_name = "sample"


urlpatterns = [
    path("", views.LandingView.as_view(), name="landing"),
    path("error/<int:code>", views.ErrorView.as_view(), name="error"),
    path("protected/", views.ProtectedView.as_view(), name="protected"),
]
