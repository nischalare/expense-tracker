"""
ASGI config for backend_expense_tracker_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information, see:
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import django
from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_expense_tracker_project.settings")

# ✅ Ensure Django is initialized before ASGI application is created
django.setup()

# ✅ Initialize ASGI application
application = get_asgi_application()
