from __future__ import absolute_import, unicode_literals

import os

from .celery import app as celery_app

__all__ = ("celery_app",)


env_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "config", "env", ".env"
)
mode_value = None
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if line.strip() and not line.strip().startswith("#"):
                key_value = line.strip().split("=", 1)
                if len(key_value) == 2:
                    key, value = (
                        key_value[0].strip(),
                        key_value[1].strip().strip("'\""),
                    )

                    os.environ.setdefault(key, value)
                    if key == "MODE":
                        mode_value = value
