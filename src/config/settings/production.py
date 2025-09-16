from config.settings.base import *  # noqa: F403

DEBUG = env.bool("DEBUG")  # noqa: F405

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")  # noqa: F405

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env.get_value("DB_NAME"),  # noqa: F405
        "USER": env.get_value("DB_USER"),  # noqa: F405
        "PASSWORD": env.get_value("DB_PASSWORD"),  # noqa: F405
        "HOST": env.get_value("DB_HOST", default="localhost"),  # noqa: F405
        "PORT": env.get_value("DB_PORT", default="5432"),  # noqa: F405
    }
}

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")  # noqa: F405
CORS_ALLOW_CREDENTIALS = True
