"""
WSGI config for EPLF project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application
import os
import sys

sys.path.insert(0, '/home/ubuntu/Gestion_associative/EPLF')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EPLF.settings')

application = get_wsgi_application()
