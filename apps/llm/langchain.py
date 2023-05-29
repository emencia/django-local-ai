from typing import Any
from langchain.llms import LlamaCpp
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from django.conf import settings
from instant.producers import publish


LLM: LlamaCpp | None = None
TOKS = 0


class WsCallbackHandler(StreamingStdOutCallbackHandler):
    """Callback handler for websockets. Only works with LLMs that support streaming."""

    def on_llm_new_token(self, token: str, **kwargs: Any) -> None:
        """Run on new LLM token. Only available when streaming is enabled."""
        global TOKS
        TOKS += 1
        if TOKS == 1:
            publish("$llm", "#STARTSTREAM#")
        publish("$llm", token)


def load_langchain(*args, **kwargs) -> LlamaCpp:
    global LLM, TOKS
    TOKS = 0
    if LLM is None:
        LLM = LlamaCpp(
            model_path=settings.MODEL_PATH,
            callback_manager=CallbackManager([WsCallbackHandler()]),
            verbose=True,
            **kwargs,
        )
    return LLM
