from django.urls import path
from .views import infer_view, generate_view, load_model_view, models_conf_views


urlpatterns = [
    path("infer/", infer_view),
    path("generate/", generate_view),
    path("models/", models_conf_views),
    path("load_model/", load_model_view),
]
