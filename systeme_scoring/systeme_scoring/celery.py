import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'systeme_scoring.settings')

app = Celery('systeme_scoring')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.worker_pool = 'solo'
app.conf.broker_connection_retry_on_startup = True