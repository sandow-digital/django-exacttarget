from .client import ETClient, Subscriber, DataExtension, TriggeredSend

from celery import task


@task(name='django_exacttarget.tasks.triggered_send')
def triggered_send(email, customer_key, client_id=None, client_secret=None):
    ts_send = TriggeredSend(client_id=None, client_secret=None)
    ts_send.send(customer_key, [email])

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

@task(name='django_exacttarget.tasks.add_subscriber_doubleoptin')
def add_subscriber_doubleoptin(email, properties=None, client_id=None, client_secret=None):
    # check if email already added in account
    subscriber = Subscriber(email=email, client_id=client_id, client_secret=client_secret)
    sub_resp = subscriber.fetch()
    if not sub_resp.results:
        # New subscriber, add as unsubed to support double opt-in
        if properties:
            properties.update({'Status': 'Unsubscribed'})
        else:
            properties = {'Status': 'Unsubscribed'}
        sub_resp = subscriber.save(properties)

@task(name='django_exacttarget.tasks.add_subscriber_doubleoptin_confirm')
def add_subscriber_doubleoptin_confirm(email, properties=None, client_id=None, client_secret=None):
    subscriber = Subscriber(email=email, client_id=client_id, client_secret=client_secret)
    sub_resp = subscriber.fetch()
    if sub_resp.results:
        sub_resp = subscriber.save({'Status': 'Active'})
