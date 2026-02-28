# ============================================================
# settings.py — Django Configuration for LearnPython
# ============================================================

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Core ─────────────────────────────────────────────────────
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-change-me-in-production-use-a-long-random-string",
)
DEBUG = os.getenv("DEBUG", "true").lower() in ("true", "1", "yes")
ALLOWED_HOSTS = ["*"]

# ── Applications ─────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    # Third-party
    "rest_framework",
    "corsheaders",
    # Our app
    "api",
]

# ── Middleware ────────────────────────────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "learnpython.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "learnpython.wsgi.application"

# ── Database (SQLite only — no external DB needed) ──────────
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ── REST Framework ───────────────────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",
    ),
    "EXCEPTION_HANDLER": "api.utils.custom_exception_handler",
}

# ── CORS (public API — allow all origins) ────────────────────
CORS_ALLOW_ALL_ORIGINS = True

# ── Sandbox ──────────────────────────────────────────────────
SANDBOX_TIMEOUT_SECONDS = int(os.getenv("SANDBOX_TIMEOUT_SECONDS", "5"))
SANDBOX_MAX_OUTPUT_CHARS = int(os.getenv("SANDBOX_MAX_OUTPUT_CHARS", "5000"))

# ── i18n ─────────────────────────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ── Static ───────────────────────────────────────────────────
STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
