from typing import List

from django.http import HttpRequest
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.auth.models import AbstractBaseUser

from apps.account.utils.token import encode_token


def email_message(message: str, subject: str, to_email: str) -> int:
    """Send an email message

    Args:
        message (str): the email body message
        subject (str): the email subject
        to_email (str): the email to send to

    Returns:
        int: a status
    """
    return send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email])


def email_activation_token(
    request: HttpRequest,
    user: AbstractBaseUser,
    to_email: str,
    subject: str,
    template: List[str] | str,
) -> int:
    """Send an email activation message containing a token

    Args:
        request (HttpRequest): the Django http request
        user (AbstractBaseUser): a Django user
        to_email (str): the email to send to
        subject (str): the email subject
        template (List[str] | str): the template to use to render the mail

    Returns:
        int: a status
    """
    current_site = get_current_site(request)
    domain = current_site.domain
    token = encode_token(user.email)
    message = render_to_string(
        template,
        {"domain": domain, "token": token},
    )
    return email_message(message, subject, to_email)
