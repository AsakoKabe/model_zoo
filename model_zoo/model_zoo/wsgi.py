"""
WSGI config for model_zoo project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from cv.registry import CVRegistry
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'model_zoo.settings')

application = get_wsgi_application()

cv_registry = CVRegistry()
