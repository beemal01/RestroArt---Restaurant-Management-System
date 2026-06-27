import os
import sys

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Restro.settings')

app = Celery('restroApp')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# On Windows, use the 'solo' pool to avoid PermissionError with billiard's
# multiprocessing implementation (shared memory handle access denied).
if sys.platform == 'win32':
    app.conf.worker_pool = 'solo'