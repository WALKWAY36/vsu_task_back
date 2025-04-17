import os
from pathlib import Path

import pytest
from django.conf import settings
from dotenv import load_dotenv


def pytest_runtest_logreport(report):
    if report.when == 'call':
        if report.failed:
            print(f"❌ Тест {report.nodeid} не прошёл! \n")
        else:
            print(f"✅ Тест {report.nodeid} прошёл успешно! \n")


@pytest.fixture(autouse=True)
def disable_throttling():
    settings.REST_FRAMEWORK['DEFAULT_THROTTLE_CLASSES'] = []
    settings.REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {}


def pytest_configure(config):
    env_path = Path(__file__).resolve().parents[2] / ".env.dev"
    load_dotenv(dotenv_path=env_path, override=True)

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")

    config.option.timeout = 30
