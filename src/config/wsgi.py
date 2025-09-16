import os

from django.core.wsgi import get_wsgi_application

from config import mode_value

os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{mode_value}")

application = get_wsgi_application()
