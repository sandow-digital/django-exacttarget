
Installation

Add to INSTALLED_APPS

Add settings for Exact Target app:

EXACT_TARGET_CLIENT_ID
EXACT_TARGET_CLIENT_SECRET


Usage

from django_exacttarget import FuelClient

client = FuelClient(client_id=settings.CLIENT_ID, )

