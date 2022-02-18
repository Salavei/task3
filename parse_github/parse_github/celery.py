import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parse_github.settings')

app = Celery('parse_github')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
