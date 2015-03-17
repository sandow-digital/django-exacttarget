from .client import ETClient

from celery import task


@task(name='django_exacttarget.tasks.add_subscriber')
def add_subscriber(email, properties):
    client = ETClient()
    client.add_subscriber(email, **properties)

@task(name='django_exacttarget.tasks.remove_subscriber_from_lists')
def remove_subscriber_from_lists(email, list_ids):
    client = ETClient()
    client.remove_subscriber_from_lists(email, list_ids)
