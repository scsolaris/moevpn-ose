import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'moevpn.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
