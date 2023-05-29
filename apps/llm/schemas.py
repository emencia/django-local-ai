from ninja import Schema


class InferContract(Schema):
    prompt: str


class InferTemplateContract(InferContract):
    template: str


class InferUsageContract(Schema):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class InferResponseContract(Schema):
    text: str
    finish_reason: str
    usage: InferUsageContract
