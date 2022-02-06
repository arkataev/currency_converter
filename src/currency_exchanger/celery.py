from celery import Celery

app = Celery(broker='rabbitmq')

app.conf.beat_schedule = {
    'refresh_erm_every_24h': {
        'task': 'refresh_erm',
        'schedule': 30.0,
    },
}
app.autodiscover_tasks()
