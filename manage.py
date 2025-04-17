#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from webapp.initializer import Initializer


def configure_temp_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


def main():
    configure_temp_logging()

    env_path = os.path.join(Path(__file__).resolve().parent, ".env.dev")
    load_dotenv(env_path)
    
    Initializer().execute() 
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()