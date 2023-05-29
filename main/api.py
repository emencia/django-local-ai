import json

from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponse, HttpRequest

from ninja import NinjaAPI
from ninja.security import django_auth
from ninja.errors import ValidationError

from apps.account.api import router as account_router
from apps.llm.api import router as llm_router

api_kwargs = {
    "auth": django_auth,
    "csrf": True,
    "docs_decorator": staff_member_required,
}
api = NinjaAPI(**api_kwargs)


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
