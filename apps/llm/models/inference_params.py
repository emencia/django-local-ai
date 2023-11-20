from django.db import models
from locallm import InferenceParams
from ..const import DEFAULT_INFERENCE_PARAMS


class InferenceParamsPreset(models.Model):
    name = models.CharField(
        verbose_name="Name", help_text="Name of the preset", max_length=128
    )
    max_tokens = models.IntegerField(
        default=DEFAULT_INFERENCE_PARAMS.max_tokens,  # type: ignore
        help_text=(
            "The maximum number of tokens to generate. "
            "If max_tokens <= 0, the maximum number of tokens to generate "
            "is unlimited and depends on the model's context window size (default)."
        ),
    )
    temperature = models.FloatField(
        default=DEFAULT_INFERENCE_PARAMS.temperature,  # type: ignore
        help_text="The temperature to use for sampling.",
    )
    top_p = models.FloatField(
        default=DEFAULT_INFERENCE_PARAMS.top_p,  # type: ignore
        help_text="The top-p value to use for sampling.",
    )
    top_k = models.PositiveIntegerField(
        default=DEFAULT_INFERENCE_PARAMS.top_k,  # type: ignore
        help_text="The top-k value to use for sampling.",
    )
    tfs = models.FloatField(
        default=DEFAULT_INFERENCE_PARAMS.tfs,  # type: ignore
        help_text="Tail free sampling: 1.0 (default) disables it",
    )
    stop = models.JSONField(
        blank=True,
        null=True,
        help_text="A list of strings to stop generation when encountered.",
    )
    repeat_penalty = models.FloatField(
        default=DEFAULT_INFERENCE_PARAMS.repeat_penalty,  # type: ignore
        help_text="The penalty to apply to repeated tokens: default: 1.",
    )
    presence_penalty = models.FloatField(
        default=DEFAULT_INFERENCE_PARAMS.presence_penalty,  # type: ignore
        help_text="The presence penalty: 0 (default) disables it",
    )
    frequency_penalty = models.FloatField(
        default=DEFAULT_INFERENCE_PARAMS.frequency_penalty,  # type: ignore
        help_text="The frequency penalty: 0 (default) disables it",
    )

    def __str__(self):
        return self.name

    def to_pydantic(self):
        return InferenceParams(**self.__dict__)
