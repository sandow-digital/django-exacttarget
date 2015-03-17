
Installation
============

```bash
pip install -e git+https://github.com/sandow-digital/django-exacttarget.git#egg=django_exacttarget
```

Add settings for the Exact Target app:

```python
EXACT_TARGET_CLIENT_ID = 'xxxxxx'
EXACT_TARGET_CLIENT_SECRET = 'xxxxxx'
AVAILABLE_SUBSCRIBER_PROPERTIES = [
  'Zip',
  'FirstName',
  'LastName'
] (optional)
```

Usage
=====

```python
from django_exacttarget.client import ETClient

client = ETClient()

client.add_subscriber(email='example@test.com', Zip='10031', Lists=[{'ID': 1050},])
```

Celery
======

Waiting for the API calls to return can take some time and for most tasks isn't necessary. Celery tasks for those operations are included.

To use, add django_exacttarget to INSTALLED_APPS. The tasks are:

```python
add_subscriber(email, properties)
remove_subscriber_from_lists(email, list_ids)
```

Example usage:

```python
properties = {
  'Zip': zipcode,
  'FirstName': first_name,
  'LastName': last_name
}

add_subscriber.apply_async([email, properties], countdown=3)
```

