"""
ASGI config for greatkart project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from configurations.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "greatkart.settings")
os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

application = get_asgi_application()
