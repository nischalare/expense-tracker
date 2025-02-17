"""
WSGI config for backend_expense_tracker_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information, see:
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# ✅ Set default settings module for the 'wsgi' application
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend_expense_tracker_project.settings")

try:
    application = get_wsgi_application()
    print("✅ WSGI application loaded successfully.")
except Exception as e:
    print(f"❌ WSGI application failed to load: {e}", file=sys.stderr)
