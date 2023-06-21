from django.db import models


class LlmTask(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name


class LlmModel(models.Model):
    name = models.CharField(max_length=255, unique=True)
    path = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    mtype = models.CharField(max_length=255, blank=True, null=True)
    family = models.CharField(max_length=255, blank=True, null=True)
    disabled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class LlmTemplate(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    mtype = models.CharField(max_length=255, blank=True, null=True)
    family = models.CharField(max_length=255, blank=True, null=True)
    disabled = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name


class LlmPrompt(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    mtype = models.CharField(max_length=255, blank=True, null=True)
    family = models.CharField(max_length=255, blank=True, null=True)
    disabled = models.BooleanField(default=False)
    model = models.ForeignKey(LlmModel, null=True, blank=True, on_delete=models.CASCADE)
    template = models.ForeignKey(
        LlmTemplate, null=True, blank=True, on_delete=models.CASCADE
    )
    task = models.ForeignKey(LlmTask, null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.name
