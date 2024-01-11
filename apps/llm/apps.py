from django.apps import AppConfig


class LlmConfig(AppConfig):
    name = "apps.llm"

    def ready(self):
        from apps.llm.lm import init_lm

        init_lm()
