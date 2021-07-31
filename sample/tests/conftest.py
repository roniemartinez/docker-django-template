import pytest
from pytest_django.fixtures import SettingsWrapper


@pytest.fixture(autouse=True)
def email_backend_setup(settings: SettingsWrapper) -> None:
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
