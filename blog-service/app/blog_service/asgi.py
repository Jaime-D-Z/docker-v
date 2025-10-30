"""
ASGI config for blog_service project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
import sys

# Agregar el directorio app al path para que Django pueda encontrar los módulos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app_path = os.path.join(BASE_DIR, 'app')
if app_path not in sys.path:
    sys.path.insert(0, app_path)

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_service.settings')

application = get_asgi_application()

