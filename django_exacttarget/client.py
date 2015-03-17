from django.conf import settings

from FuelSDK import ET_Client, ET_Subscriber, \
    ET_List, ET_DataExtension, ET_DataExtension_Row


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

    def add_to_dataextension(self, de_name, properties, update=False):
        de_row = ET_DataExtension_Row()
        de_row.CustomerKey = de_name
        de_row.auth_stub = self
        de_row.props = properties
        if update:
            de_row_resp = de_row.patch()
        else:
            de_row_resp = de_row.post()

        if not de_row_resp.status and not update:
            # try to patch instead
            de_row_resp = de_row.patch()


        return de_row_resp


    def get_rows_from_dataextension(self, de_name, fields):
        de_rows = ET_DataExtension_Row()
        de_rows.auth_stub = self
        de_rows.CustomerKey = de_name
        de_rows.props = fields
        de_resp = de_rows.get()

        return de_resp

    def get_all_dataextensions(self):
        de = ET_DataExtension()
        de.auth_stub = self
        de.props = ['CustomerKey', 'Name']
        de_resp = de.get()

        return de_resp


    def get_lists(self):
        lists = ET_List()
        lists.auth_stub = self
        lists.props = ["ID", "ListName"]
        list_resp = lists.get()

        return list_resp

    def get_list_by_name(self, name):
        lists = ET_List()
        lists.auth_stub = self
        lists.props = ["ID", "ListName"]
        lists.search_filter = {'Property': 'ListName',
            'SimpleOperator': 'equals', 'Value': name}
        list_resp = lists.get()

        return list_resp


    def remove_subscriber_from_lists(self, email, list_ids):
        subscriber = ET_Subscriber()
        subscriber.auth_stub = self
        subscriber.props = {'SubscriberKey': email, 'EmailAddress': email,
            'Lists': [{'ID': x} for x in list_ids]}
        del_resp = subscriber.delete()

        return del_resp

    def add_subscriber(self, email, **kwargs):
        properties = {"EmailAddress": email, "SubscriberKey": email}

        if kwargs:
            properties['Attributes'] = []
            for k, v in kwargs.iteritems():
                if hasattr(settings, 'AVAILABLE_SUBSCRIBER_PROPERTIES') and \
                    k not in settings.AVAILABLE_SUBSCRIBER_PROPERTIES:
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
