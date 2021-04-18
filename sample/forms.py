from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        help_text=gettext_lazy("Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."),
    )
    first_name = forms.CharField(
        label="First name", widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    last_name = forms.CharField(
        label="Last name", widget=forms.TextInput(attrs={"class": "form-control"}), required=True
    )
    email = forms.CharField(
        label="Email address", widget=forms.EmailInput(attrs={"class": "form-control"}), required=True
    )
    password1 = forms.CharField(
        label=gettext_lazy("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=gettext_lazy("Password confirmation"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),
        strip=False,
        help_text=gettext_lazy("Enter the same password as before, for verification."),
    )

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email")

    def clean_email(self) -> str:
        email = self.cleaned_data.get("email")
        if get_user_model().objects.filter(email=email).exists():
            raise ValidationError(gettext("Email already exists!"), code="email_exists")
        return email
