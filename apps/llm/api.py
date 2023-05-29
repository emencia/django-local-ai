from typing import Tuple
from django.http import HttpRequest
from ninja import Router

from apps.base.schemas import (
    MsgResponseContract,
    FormInvalidResponseContract,
)
from apps.llm.schemas import InferContract, InferResponseContract, InferTemplateContract
from apps.llm.llama import load_llama_cpp
from apps.llm.tasks import infer, infertemplate

router = Router(tags=["llm"])


@router.post(
    "/inferhttp",
    response={
        200: InferResponseContract,
        422: FormInvalidResponseContract,
        401: MsgResponseContract,
    },
)
def inferhttp(
    request: HttpRequest, data: InferContract
) -> Tuple[int, None | FormInvalidResponseContract | MsgResponseContract]:
    LLM = load_llama_cpp()
    prompt: str = data.dict()["prompt"]
    print("Prompt:")
    print(prompt)
    output = LLM.create_completion(prompt, max_tokens=1024)
    print("Response:")
    print(output)
    text: str = output["choices"][0]["text"]
    resp = InferResponseContract(
        text=text,
        finish_reason=output["choices"][0]["finish_reason"],
        usage=output["usage"],
    )
    return 200, resp


@router.post(
    "/inferstream",
    response={
        200: None,
        422: FormInvalidResponseContract,
        401: MsgResponseContract,
    },
)
def inferstream(request: HttpRequest, data: InferContract):
    prompt: str = data.dict()["prompt"]
    print("Calling LLama.cpp infer task with,", prompt)
    infer(prompt)
    return 200, None


@router.post(
    "/inferlc",
    response={
        200: None,
        422: FormInvalidResponseContract,
        401: MsgResponseContract,
    },
)
def inferlc(request: HttpRequest, data: InferTemplateContract):
    prompt: str = data.dict()["prompt"]
    template: str = data.dict()["template"]
    print("Calling Langchain infer task with template", template)
    print("For prompt", prompt)
    infertemplate(prompt, template)
    return 200, None
