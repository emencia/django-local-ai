from ninja import Schema
from locallm import InferenceParams


class InferContract(Schema):
    prompt: str
    params: InferenceParams | None
