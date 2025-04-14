import os
from pathlib import Path

from channels.routing import ProtocolTypeRouter
from django.core.asgi import get_asgi_application
from dotenv import load_dotenv

from .initializer import Initializer

env_path = os.path.join(Path(__file__).resolve().parent.parent, ".env.dev")
if os.path.exists(env_path):
    load_dotenv(env_path)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "webapp.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
    }
)

Initializer().execute()
