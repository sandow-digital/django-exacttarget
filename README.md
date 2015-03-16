
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

client.add_subscriber(email='example@test.com', list_ids=[1, 2], Zip='10031')
```
