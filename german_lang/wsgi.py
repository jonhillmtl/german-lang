"""
WSGI config for template project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# TODO TEMPLATE-USER: you can rename the "template" folder to something else,
# but you need to change it here
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "german_lang.settings")

application = get_wsgi_application()
