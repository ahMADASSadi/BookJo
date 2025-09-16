#!/usr/bin/env python

import os
import sys


def main():
    """Run administrative tasks."""

    from config import mode_value
    # env_path = os.path.join(
    #     os.path.dirname(os.path.abspath(__file__)), "config", "env", ".env"
    # )
    # mode_value = None
    # if os.path.exists(env_path):
    #     with open(env_path) as f:
    #         for line in f:
    #             if line.strip() and not line.strip().startswith("#"):
    #                 key_value = line.strip().split("=", 1)
    #                 if len(key_value) == 2:
    #                     key, value = (
    #                         key_value[0].strip(),
    #                         key_value[1].strip().strip("'\""),
    #                     )

    #                     os.environ.setdefault(key, value)
    #                     if key == "MODE":
    #                         mode_value = value

    # # Check if mode_value was found, otherwise default to something safe
    # if not mode_value:
    #     raise ValueError("MODE is not set in your .env file.")
    # print(mode_value)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{mode_value}")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
