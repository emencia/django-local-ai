from locallm import InferenceParams


DEFAULT_INFERENCE_PARAMS = InferenceParams(
    max_tokens=-1,
    temperature=0.2,
    top_p=0.95,
    top_k=40,
    tfs=1.0,
    repeat_penalty=1.0,
    presence_penalty=0,
    frequency_penalty=0,
)
