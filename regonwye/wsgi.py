from __future__ import absolute_import, unicode_literals

import os

from django.core.wsgi import get_wsgi_application

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "regonwye.settings.production")
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "regonwye.settings.production")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "regonwye.settings")

application = get_wsgi_application()
