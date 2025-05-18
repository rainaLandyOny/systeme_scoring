from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings
from ml_models.retrainer import retrain_all_models

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'credit_scoring.settings')

app = Celery('credit_scoring')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task
def monthly_retraining():
    retrain_all_models()

app.conf.beat_schedule = {
    'monthly-retraining': {
        'task': 'tasks.celery.monthly_retraining',
        'schedule': crontab(day_of_month='L', hour=22, minute=0),
        'options': {'timezone': 'Indian/Antananarivo'}
    },
}