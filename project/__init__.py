# All this codes in this page are copied from this celery website :
# https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html#using-celery-with-django

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ('celery_app',)