# """
# WSGI config for itclass project.
#
# It exposes the WSGI callable as a module-level variable named ``application``.
#
# For more information on this file, see
# https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
# """
#
# import os
#
# from django.core.wsgi import get_wsgi_application
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'itclass.settings')
#
# application = get_wsgi_application()


# -*- coding: utf-8 -*-
import os, sys
sys.path.insert(0, '/var/www/u0692673/data/www/it-class1158.site/itclass')
sys.path.insert(1, '/var/www/u0692673/data/www/it-class1158.site/itclass/venv/lib/python3.8/site-packages')
os.environ['DJANGO_SETTINGS_MODULE'] = 'itclass.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()