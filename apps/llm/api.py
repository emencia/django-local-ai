from typing import Dict, Tuple

from django.http import HttpRequest, StreamingHttpResponse
from django.conf import settings
from locallm import InferenceParams
from locallm.schemas import InferenceResult
from ninja import Router

from apps.llm.lm import infer, generate
from apps.llm.schemas import InferContract


router = Router(tags=["llm"])


@router.post(
    "/generate",
    response={200: Dict, 403: None, 400: Dict},
)
def infer_api_view(
    request: HttpRequest,
    data: InferContract,
) -> Tuple[int, InferenceResult | Dict]:
    is_verbose = getattr(settings, "LLM_VERBOSE", False)
    payload = data.model_dump(exclude_unset=True, exclude_none=True)
    # print("DATa", payload)
    if "prompt" not in payload:
        msg = 'Provide a prompt: post a payload of this format: {"prompt": "..."}'
        print(msg)
        return 400, {"error": msg}
    prompt = payload["prompt"]
    if "params" in payload:
        params = InferenceParams(**payload["params"])
    else:
        params = InferenceParams()
    if is_verbose is True:
        print("Prompt:")
        print(prompt)
    res = infer(prompt, params=params)
    return 200, res


@router.post(
    "/infer",
    response={200: Dict, 403: None, 400: Dict},
)
def generate_api_view(
    request: HttpRequest,
    data: InferContract,
):
    is_verbose = getattr(settings, "LLM_VERBOSE", False)
    payload = data.model_dump(exclude_unset=True, exclude_none=True)
    # print("DATa", payload)
    if "prompt" not in payload:
        msg = 'Provide a prompt: post a payload of this format: {"prompt": "..."}'
        print(msg)
        return 400, {"error": msg}
    prompt = payload["prompt"]
    if "params" in payload:
        params = InferenceParams(**payload["params"])
    else:
        params = InferenceParams()
    if is_verbose is True:
        print("Prompt:")
        print(prompt)
    iter_stream = generate(prompt, params)

    response = StreamingHttpResponse(iter_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"

    return response
