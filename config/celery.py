from celery.schedules import crontab
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.timezone = 'UTC'

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'prcessing-deliverys-20-seconds': {
        'task': 'processing_entity_delivery',
        'schedule': 5.0,
    },
    'update-battery-10-seconds': {
        'task': 'update_battery_entity',
        'schedule': 5.0,
    },
    'change_state-15-seconds': {
        'task': 'change_state',
        'schedule': 30.0,
    },
}
