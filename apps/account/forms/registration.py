from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


class RegistrationForm(UserCreationForm):
    """A form to register a user

    Args:
        UserCreationForm (ModelForm): the base user creation form from Django that we \
        inherit from

    Raises:
        forms.ValidationError: if a field is not correctly validated

    Returns:
        forms.Form: the Django form
    """

    error_messages = {
        "duplicate_email": "This email address is already in use.",
        "password_mismatch": "The two passwords you filled out do not match.",
    }

    name = forms.CharField(
        max_length=255,
        widget=forms.TextInput(
            attrs={"placeholder": "Full name", "autocomplete": "name"}
        ),
        help_text=None,
    )

    email = forms.EmailField(
        max_length=255,
        widget=forms.EmailInput(
            attrs={"placeholder": "Email", "autocomplete": "username"}
        ),
        help_text=None,
    )

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"placeholder": "Password"}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"placeholder": "Password confirmation"}),
        strip=False,
        help_text="Please re-enter your password for verification purposes.",
    )

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        try:
            User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages["duplicate_email"])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = super().clean_password2()
        if bool(password1) ^ bool(password2):
            raise forms.ValidationError("Fill out both fields")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = False
        user.set_password(self.cleaned_data["password1"])
        user.username = user.email
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2")
