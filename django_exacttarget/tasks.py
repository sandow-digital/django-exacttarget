from .client import ETClient, Subscriber, DataExtension

from celery import task


@task(name='django_exacttarget.tasks.add_subscriber')
def add_subscriber(email, properties=None):
    subscriber = Subscriber(email=email)
    sub_resp = subscriber.save(properties)


@task(name='django_exacttarget.tasks.remove_subscriber_from_lists')
def remove_subscriber_from_lists(email, list_ids):
    subscriber = Subscriber(email=email)
    subscriber.remove_from_lists(list_ids)

@task(name='django_exacttarget.tasks.add_dataextension_row')
def add_dataextension_row(name, properties):
    de = DataExtension(name=name)
    de.add_row(properties)
