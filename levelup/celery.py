import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'levelup.settings')

app = Celery('levelup')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


app.conf.beat_schedule = {
    'parse-csv-every-single-minute': {
        'task': 'product.tasks.parse_csv_task',
        'schedule': crontab(),
        # change to `crontab(minute=0, hour=0)` if you want it to run daily at midnight
    },
}
