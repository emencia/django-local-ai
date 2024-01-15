from typing import Dict, Tuple

from django.middleware.csrf import get_token
from django.http import HttpRequest
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.conf import settings

from ninja import Router

from apps.base.schemas import (
    MsgResponseContract,
    FormInvalidResponseContract,
)
from apps.account.schemas import (
    LoginFormContract,
    StateContract,
)


router = Router(tags=["account"])


@router.post(
    "/login",
    auth=None,
    response={
        200: Dict,
        422: FormInvalidResponseContract,
        401: MsgResponseContract,
    },
)
def authlogin(
    request: HttpRequest, data: LoginFormContract
) -> Tuple[int, Dict | FormInvalidResponseContract | MsgResponseContract]:
    """Login a user from a username and password payload

    Endpoint url: /api/account/login

    Args:
        request (HttpRequest): the django http request object
        data (LoginFormContract): the username and password payload

    Returns:
        Tuple[int, None | FormInvalidResponseContract | MsgResponseContract]:
        the http status code and the data payload
    """
    form = AuthenticationForm(data=data.dict())
    if form.is_valid() is False:
        return 422, FormInvalidResponseContract.parse_obj(
            {"errors": form.errors.get_json_data(escape_html=True)}
        )

    user = authenticate(
        username=form.cleaned_data.get("username"),
        password=form.cleaned_data.get("password"),
    )
    if user is not None:
        login(request, user)  # returns a 200
        return 200, {"key": settings.LLM_API_KEY}
    else:
        return 401, MsgResponseContract(**{"message": "Login refused"})


@router.get(
    "/logout",
    response={200: MsgResponseContract, 403: None},
)
def authlogout(request: HttpRequest) -> Tuple[int, MsgResponseContract | None]:
    """Logout a user

    Endpoint url: /api/account/logout

    Args:
        request (HttpRequest): the django http request object

    Returns:
        Tuple[int, None]: the http status code and None
    """
    if request.user.is_anonymous is True:
        return 403, None
    logout(request)  # returns a 200
    return 200, MsgResponseContract(message="ok")


@router.get("/state", auth=None, response={200: StateContract})
def global_state(request: HttpRequest) -> Tuple[int, StateContract]:
    """Returns info on user state and set a csrf token

    Endpoint url: /api/account/state

    Args:
        request (HttpRequest): the django http request object

    Returns:
        Tuple[int, StateContract]: the http status code and the data payload
    """
    out = {"is_connected": False, "username": "anonymous", "key": ""}
    if request.user.is_anonymous is False:
        out["is_connected"] = True
        out["username"] = request.user.get_username()
        out["key"] = settings.LLM_API_KEY
    # set a csrf token cookie
    get_token(request)
    return 200, StateContract(**out)
