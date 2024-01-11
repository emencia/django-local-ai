from typing import Any, Callable, Generator
from django.conf import settings
from locallm import LocalLm, LmParams, InferenceParams
from locallm.schemas import InferenceResult


params = dict(
    models_dir=settings.LLM_MODELS_DIR,
    is_verbose=getattr(settings, "LLM_VERBOSE", False),
)
LM = LocalLm(LmParams(**params))


def init_lm():
    global LM
    params = dict(
        models_dir=settings.LLM_MODELS_DIR,
        is_verbose=getattr(settings, "LLM_VERBOSE", False),
    )
    if settings.LLM_THREADS:
        params["threads"] = settings.LLM_THREADS
    if settings.LLM_GPU_LAYERS:
        params["gpu_layers"] = settings.LLM_GPU_LAYERS
    if settings.LLM_EMBEDDING is True:
        params["embedding"] = True
    LM = LocalLm(LmParams(**params))


def load_model(model: str | None = None, ctx: int | None = None):
    if model is None:
        if LM.loaded_model == "":
            is_verbose = getattr(settings, "LLM_VERBOSE", False)
            if is_verbose:
                print(
                    "Loading default model",
                    settings.LLM_DEFAULT_MODEL,
                    "with a",
                    settings.LLM_DEFAULT_CTX,
                    "context window",
                )
            LM.load_model(settings.LLM_DEFAULT_MODEL, settings.LLM_DEFAULT_CTX)
    else:
        if ctx is None:
            raise ValueError("Provide a context window size using the ctx parameter")
        LM.load_model(model, ctx)


def infer(prompt: str, params: InferenceParams = InferenceParams()) -> InferenceResult:
    load_model()
    return LM.infer(prompt, params)


def generate(
    prompt: str, params: InferenceParams = InferenceParams()
) -> Callable[[], Generator[str, Any, None]]:
    load_model()
    stream = LM.generate(prompt, params)

    def iter_stream():
        i = 1
        for event in stream:
            token = event["choices"][0]["text"]
            if LM.is_verbose is True:
                print(token, end="", flush=True)
            payload = f"data: {token}\n\n"
            # print(payload.replace("\n", "\\n"))
            yield payload
            i += 1

    return iter_stream
