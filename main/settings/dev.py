from .settings import BASE_DIR

EMAIL_FILE_PATH = BASE_DIR / "email"
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
