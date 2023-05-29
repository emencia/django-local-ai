from django.test.client import RequestFactory
from apps.account.forms.registration import RegistrationForm
from apps.account.utils.email import email_activation_token
from django.core import mail

from apps.account.utils.token import encode_token, decode_token


def test_email_message():
    form = RegistrationForm(
        data={
            "name": "John Doe",
            "email": "mymail@example.com",
            "password1": "xxxzzzxxx",
            "password2": "xxxzzzxxx",
        }
    )
    form.is_valid()
    form.save()
    user = form.instance
    rf = RequestFactory()

    email_data = {
        "request": rf.post(
            "/api/account/register",
            data=form.cleaned_data,
        ),
        "user": user,
        "to_email": form.cleaned_data.get("email"),
        "subject": "Activate your account.",
        "template": "active_email.html",
    }
    email = email_activation_token(**email_data)
    assert email
    assert len(mail.outbox) == 1  # type: ignore
    assert mail.outbox[0].subject == "Activate your account."  # type: ignore


def test_encode_decode_token():
    token = encode_token("dummy@dummy.dummy")
    mail_from_token = decode_token(token)
    assert mail_from_token == (True, "dummy@dummy.dummy")


def test_decode_token_error():
    mail_from_token = decode_token("dummy")
    assert mail_from_token == (False, "")
