from __future__ import absolute_import, unicode_literals

import os

from celery import Celery  # type: ignore
from celery.schedules import crontab  # type: ignore  # noqa: F401
from django.conf import settings  # type: ignore

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")

app = Celery("config")


app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


app.conf.update(
    # CELERY_QUEUES=settings.CELERY_QUEUES,
    # CELERY_ROUTES=settings.CELERY_ROUTES,
    CELERY_DEFAULT_QUEUE=settings.CELERY_DEFAULT_QUEUE,
    CELERY_DEFAULT_EXCHANGE="tasks",
    CELERY_DEFAULT_ROUTING_KEY="task.default",
)


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
