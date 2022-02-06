import os

from celery import Celery

app = Celery(broker='rabbitmq')

app.conf.beat_schedule = {
    'refresh_erm_every_24h': {
        'task': 'refresh_erm',
        'schedule': os.environ.get('CER_UPDATE_PERIOD', 30),
    },
}
app.autodiscover_tasks()
