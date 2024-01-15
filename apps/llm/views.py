import json
from typing import Dict
from django.http import HttpResponseBadRequest, StreamingHttpResponse, JsonResponse
from django.http import HttpRequest
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from locallm import InferenceParams

from apps.llm.models.task import LmTask

from .lm import infer, generate, load_model, LM
from .utils import load_models_conf


@csrf_exempt
def load_model_view(request: HttpRequest) -> JsonResponse | HttpResponseBadRequest:
    if request.method == "POST":  # type: ignore
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        if "name" not in body:
            print("Provide a model name")
            return HttpResponseBadRequest()
        model_conf = {"name": body["name"]}
        if "ctx" in body:
            model_conf["ctx"] = body["ctx"]
        else:
            print("No context window size provided, using 2048")
            model_conf["ctx"] = 2048
    else:
        return HttpResponseBadRequest()
    err = ""
    try:
        load_model(model_conf["name"], model_conf["ctx"])
    except Exception:
        err = "Error loading model"
    return JsonResponse({"error": err})


@csrf_exempt
def generate_view(
    request: HttpRequest,
) -> StreamingHttpResponse | HttpResponseBadRequest:
    is_verbose = getattr(settings, "LLM_VERBOSE", False)
    if request.method == "POST":  # type: ignore
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        prompt = body["prompt"]
        if "params" in body:
            params = InferenceParams(**body["params"])
        else:
            params = InferenceParams(stream=True)
    else:
        print('Provide a prompt: post a payload of this format: {"prompt": "..."}')
        return HttpResponseBadRequest()
    if is_verbose is True:
        print("Prompt:")
        print(prompt)

    iter_stream = generate(prompt, params)

    response = StreamingHttpResponse(iter_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"

    return response


@csrf_exempt
def infer_view(request: HttpRequest) -> JsonResponse | HttpResponseBadRequest:
    is_verbose = getattr(settings, "LLM_VERBOSE", False)
    if request.method == "POST":  # type: ignore
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        prompt = body["prompt"]
        if "params" in body:
            params = InferenceParams(**body["params"])
        else:
            params = InferenceParams()
    else:
        print('Provide a prompt: post a payload of this format: {"prompt": "..."}')
        return HttpResponseBadRequest()
    if is_verbose is True:
        print("Prompt:")
        print(prompt)

    res = infer(prompt, params)

    return JsonResponse(res)


@csrf_exempt
def models_conf_views(request: HttpRequest) -> JsonResponse:
    models_conf = load_models_conf(settings.LLM_MODELS_DIR + "/templates.yml")
    # print(models_conf)
    # return JsonResponse({})
    tpls: Dict[str, Dict[str, str | int]] = {}
    for mc in models_conf:
        tpls[mc] = {
            "name": models_conf[mc][0]["template"],
            "ctx": models_conf[mc][1]["ctx"],
        }
    is_model_loaded = LM.loaded_model != ""
    res = {
        "ctx": 2048,
        "isModelLoaded": is_model_loaded,
        "loadedModel": LM.loaded_model,
        "models": tpls,
    }
    if is_model_loaded is True:
        res["ctx"] = res["models"][LM.loaded_model]["ctx"]  # type: ignore
    print(res)
    return JsonResponse(res)


@csrf_exempt
def execute_task_view(request: HttpRequest) -> JsonResponse | HttpResponseBadRequest:
    if request.method == "POST":  # type: ignore
        body_unicode = request.body.decode("utf-8")
        body = json.loads(body_unicode)
        task_name = body["name"]
        prompt = body["prompt"]
    else:
        print(
            "Provide a prompt and task name: post a payload of this format: "
            '{"prompt": "...", "name": "..."}'
        )
        return HttpResponseBadRequest("Provide a prompt and task name")
    try:
        task = LmTask.objects.get(name=task_name)
    except LmTask.ObjectDoesNotExist:
        print("Unknown task")
        return HttpResponseBadRequest("Unknown task")
    tpl = task.template.replace("{prompt}", prompt)
    res = infer(tpl, task.params)
    return JsonResponse(res)
