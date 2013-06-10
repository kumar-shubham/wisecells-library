import os
import os.path
import sys

sys.path.append('~/DjangoTry/mysite/')
sys.path.append('~/Djangotry/mysite/mysite')

os.environ['DJANGO_SETTING_MODULE'] = 'mysite.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandlers()