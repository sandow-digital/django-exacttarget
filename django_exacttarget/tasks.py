from .client import ETClient, Subscriber, DataExtension

from celery import task


@task(name='django_exacttarget.tasks.add_subscriber')
def add_subscriber(email, properties=None, client_id=None, client_secret=None):
    subscriber = Subscriber(email=email, client_id=client_id, client_secret=client_secret)
    sub_resp = subscriber.save(properties)


@task(name='django_exacttarget.tasks.remove_subscriber_from_lists')
def remove_subscriber_from_lists(email, list_ids, client_id=None, client_secret=None):
    subscriber = Subscriber(email=email, client_id=client_id, client_secret=client_secret)
    subscriber.remove_from_lists(list_ids)

@task(name='django_exacttarget.tasks.add_dataextension_row')
def add_dataextension_row(name, properties, client_id=None, client_secret=None):
    de = DataExtension(name=name, client_id=client_id, client_secret=client_secret)
    de.add_row(properties)
