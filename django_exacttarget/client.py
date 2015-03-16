from django.conf import settings

from FuelSDK import ET_Client, ET_Subscriber


SUBSCRIBER_EXISTS_ERROR_CODE = 12014

class ETClient(ET_Client):
    def __init__(self):

        params = {
            'clientid': settings.EXACT_TARGET_CLIENT_ID,
            'clientsecret': settings.EXACT_TARGET_CLIENT_SECRET,
            'defaultwsdl': getattr(settings, 'EXACT_TARGET_WSDL_URL',
                'https://webservice.exacttarget.com/etframework.wsdl'),
            'authenticationurl': getattr(settings, 'EXACT_TARGET_AUTH_URL',
                'https://auth.exacttargetapis.com/v1/requestToken?legacy=1'),
            'appsignature': None,
        }

        ET_Client.__init__(self, get_server_wsdl=False,
            debug=False, params=params)


    def add_subscriber(self, email, list_ids=[], **kwargs):
        properties = {"EmailAddress": email, "SubscriberKey": email}

        if len(list_ids) > 0:
            properties['Lists'] = [{'ID': x} for x in list_ids]

        if kwargs:
            properties['Attributes'] = []
            for k, v in kwargs.iteritems():
                if hasattr(settings, AVAILABLE_SUBSCRIBER_PROPERTIES):
                    if k not in settings.AVAILABLE_SUBSCRIBER_PROPERTIES:
                        continue

                if v is not None and v != '':
                    properties['Attributes'].append({
                        'Name': k,
                        'Value': v
                    })


        subscriber = ET_Subscriber()
        subscriber.auth_stub = self
        subscriber.props = properties
        sub_response = subscriber.post()

        if sub_response.status is False and \
            sub_response.results[0]['ErrorCode'] == SUBSCRIBER_EXISTS_ERROR_CODE:
            # subscriber already exists, so update instead
            subscriber = ET_Subscriber()
            subscriber.auth_stub = self
            subscriber.props = properties
            sub_response = subscriber.patch()

        return sub_response
