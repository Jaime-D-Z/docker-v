"""
WSGI config for blog_service project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
import sys

# Agregar el directorio app al path para que Django pueda encontrar los módulos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
app_path = os.path.join(BASE_DIR, 'app')
if app_path not in sys.path:
    sys.path.insert(0, app_path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_service.settings')

application = get_wsgi_application()

