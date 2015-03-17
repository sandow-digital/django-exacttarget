from .client import ETClient

from celery import shared_task


@shared_task
def add_subscriber(email, properties):
    client = ETClient()
    client.add_subscriber(email, **properties)
