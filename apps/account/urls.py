from django.urls import path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView


urlpatterns = [
    path(
        "activate/<token>/",
        TemplateView.as_view(template_name="index.html"),
        name="activate",
    ),
    path("login/", RedirectView.as_view(url="/", permanent=True), name="login"),
]
