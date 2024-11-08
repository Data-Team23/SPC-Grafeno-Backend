import os
from celery import Celery
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

app = Celery(
    'backend',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/1',
)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'backup-postgres-daily': {
        'task': 'user_management.tasks.backup_postgres',
        'schedule': 120.0,
    },
    'backup-mongo-encrypt': {
        'task': 'user_management.tasks.backup_mongo_encrypt',
        'schedule': 120.0,
    },
    'backup-mongo-logs': {
        'task': 'user_management.tasks.backup_mongo_logs',
        'schedule': 120.0,
    },
}
