"""
WSGI config for learningMS project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'learningMS.settings')
sys.path.append('/home/raghav/learningMS/learningMS/')

sys.path.append('/home/raghav/learningMS/venv/lib/python3.7/site-packages')

application = get_wsgi_application()
