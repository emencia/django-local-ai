from django.contrib import admin

from apps.llm.models import InferenceParamsPreset, LmTask


@admin.register(InferenceParamsPreset)
class InferenceParamsPresetAdmin(admin.ModelAdmin):
    list_display = ("name", "max_tokens", "temperature", "top_p")
    search_fields = ("name",)


@admin.register(LmTask)
class LmTaskAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "model")
    search_fields = ("name",)
