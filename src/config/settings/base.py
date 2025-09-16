from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(BASE_DIR / "env/.env")

SECRET_KEY = env.get_value("BOOKJO_SECRET_KEY")

DEFAULT_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "rest_framework_simplejwt",
    "django_lifecycle_checks",
    "django_celery_beat",
    "drf_spectacular",
    "rest_framework",
    "corsheaders",
]
PROJECT_APPS = [
    "apps.core",
    "apps.library",
]

INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + PROJECT_APPS

MIDDLEWARE = [
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "fa"
LANGUAGES = [
    ("en-us", "English"),
    ("fa", "Persian"),
]
LOCALE_PATHS = [
    BASE_DIR / "locale",
]
TIME_ZONE = "Asia/Tehran"
USE_I18N = True
USE_TZ = True

STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = "/static/"

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


CELERY_DEFAULT_QUEUE = "default"
CELERY_RESULT_BACKEND = env.get_value("CELERY_BROKER_URL")
CELERY_BROKER_URL = env.get_value("CELERY_RESULT_BACKEND")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_RESULT_EXPIRES = 3600
CELERY_TASK_ACKS_LATE = True


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": env.get_value("ACCESS_TOKEN_LIFETIME"),
    "REFRESH_TOKEN_LIFETIME": env.get_value("REFRESH_TOKEN_LIFETIME"),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": (env.get_value("AUTH_HEADER_TYPES"),),
}


SPECTACULAR_SETTINGS = {
    "TITLE": "BookJo API",
    "DESCRIPTION": "API Documentation for BookJo",
    "VERSION": "1.0.0",
    "CONTACT": {"name": "Ahmad Asadi", "email": "madassandd@gmail.com"},
    "SERVE_INCLUDE_SCHEMA": True,
}
