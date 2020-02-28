import os
import sys

path = '/home/choonz/choonz_project/'
if path not in sys.path;
    sys.path.append(path)

os.chdir(path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'choonz_project.settings')

import django
django.setup()

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
