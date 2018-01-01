"""
WSGI config for cms project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import newrelic.agent
from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cms.settings")

application = get_wsgi_application()
application = DjangoWhiteNoise(application)  # Django自身不能在生产环境提供静态文件服务，WhiteNoise允许Django在不依赖CDN的情况下提供自己的静态文件

newrelic.agent.initialize('newrelic.ini')
application = newrelic.agent.WSGIApplicationWrapper(application)
