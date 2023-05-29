from llama_cpp import Llama
from django.conf import settings


LLM: Llama | None = None


def load_llama_cpp(*args, **kwargs) -> Llama:
    global LLM
    if "n_ctx" not in kwargs:
        kwargs["n_ctx"] = 2048
    if LLM is None:
        LLM = Llama(
            model_path=settings.MODEL_PATH,
            **kwargs,
        )
    assert LLM is not None
    return LLM
