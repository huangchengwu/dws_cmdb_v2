import os
from celery import Celery
from django.conf import settings  # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dws_cmdb.settings')

app = Celery('dws_cmdb')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
