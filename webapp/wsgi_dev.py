import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

from .initializer import Initializer

env_path = os.path.join(Path(__file__).resolve().parent.parent, ".env.dev")
if os.path.exists(env_path):
    load_dotenv(env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webapp.settings')

application = get_wsgi_application()

Initializer().execute()
