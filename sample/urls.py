from django.contrib.auth.views import LogoutView
from django.urls import path

from sample import views
from sample.utils import verified_login_required

app_name = "sample"


urlpatterns = [
    path("", views.LandingView.as_view(), name="landing"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", views.RegisterView.as_view(), name="register"),
    path("registered/<uuid:uuid>/", views.RegisteredView.as_view(), name="registered"),
    path("verify/<slug:token>/", views.VerifyAccountView.as_view(), name="verify"),
    path("protected/", verified_login_required(views.ProtectedView.as_view()), name="protected"),
    path("cleanup/", views.CleanUpView.as_view(), name="cleanup"),
    path("error/<int:code>", views.ErrorView.as_view(), name="error"),
]
