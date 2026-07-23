import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djoser_advanced.settings")

app = Celery("djoser_advanced")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()