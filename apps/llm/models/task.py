from django.db import models
from .inference_params import InferenceParamsPreset


class LmTask(models.Model):
    name = models.CharField(
        verbose_name="Name", help_text="Name of the task", max_length=128
    )
    description = models.TextField(verbose_name="Task description")
    model = models.CharField(
        verbose_name="Model file",
        help_text="The gguf model file to use for this task",
        max_length=255,
    )
    params = models.ForeignKey(InferenceParamsPreset, on_delete=models.PROTECT)
    template = models.TextField(verbose_name="Prompt template")

    def __str__(self):
        return self.name
