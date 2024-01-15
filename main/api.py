import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpRequest
from django.conf import settings

from ninja import NinjaAPI
from ninja.errors import ValidationError
from ninja.security import HttpBearer

from apps.account.api import router as account_router
from apps.llm.api import router as llm_router


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        # print("T", token, "/", settings.LLM_API_KEY)
        if token == settings.LLM_API_KEY:
            return token


api_kwargs = {
    "auth": AuthBearer(),
    "csrf": False,
    "docs_decorator": staff_member_required,
}
api = NinjaAPI(**api_kwargs)  # type: ignore


@api.exception_handler(ValidationError)
def custom_validation_errors(
    request: HttpRequest, exc: ValidationError
) -> HttpResponse:
    """A validator that will fire a 418 and a message \
    if the data is not compliant to the endpoint schema

    Args:
        request (HttpRequest): the Django http request
        exc (Exception): an exception

    Returns:
        HttpResponse: a Django http response
    """
    print(json.dumps(exc.errors, indent=2))
    return api.create_response(request, {"detail": exc.errors}, status=418)


api.add_router("/account/", account_router)
api.add_router("/llm/", llm_router)
