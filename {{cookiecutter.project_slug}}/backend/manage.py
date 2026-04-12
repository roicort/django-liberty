#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

# ensure the backend/src directory is on Python path when manage.py is
# executed from the backend top level; this mirrors the previous layout
# where manage.py lived inside src and allowed package imports.
BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# load a .env file if present (useful for local development)
# this is deliberately optional so that environments which already
# set needed variables aren't disturbed.
try:
    from pathlib import Path
    from dotenv import load_dotenv

    env_path = Path(BASE_DIR) / ".env"
    if env_path.is_file():
        print(f"Loading environment variables from {env_path}")
        load_dotenv(env_path)
except ImportError:
    pass

def main():
    """Run administrative tasks."""
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        os.environ.get("DJANGO_SETTINGS_MODULE", "main.settings.base"),
    )
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