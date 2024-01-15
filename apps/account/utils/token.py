from typing import Tuple

import jwt

from django.conf import settings


def decode_token(token: str) -> Tuple[bool, str]:
    """Decode and validate an activation token

    Args:
        token (str): the token

    Returns:
        Tuple[bool, str]: is the token valid and the user email
    """
    email = ""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload["email"]
    except jwt.ExpiredSignatureError:
        print("Token decode signature expired error")
        return (False, email)
    except Exception as e:
        print("Token decode error:", e)
        return (False, email)
    return (True, email)


def encode_token(email: str) -> str:
    """Encode a token

    Args:
        email (str): the email to encode

    Returns:
        str: the encoded token
    """
    return jwt.encode({"email": email}, settings.SECRET_KEY, algorithm="HS256")
