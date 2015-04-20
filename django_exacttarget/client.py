from django.conf import settings

from FuelSDK import ET_Client, ET_Subscriber, \
    ET_List, ET_DataExtension, ET_DataExtension_Row


SUBSCRIBER_EXISTS_ERROR_CODE = 12014


class ETClient(ET_Client):
    def __init__(self, properties=None):

        params = {
            'clientid': settings.EXACT_TARGET_CLIENT_ID,
            'clientsecret': settings.EXACT_TARGET_CLIENT_SECRET,
            'defaultwsdl': getattr(settings, 'EXACT_TARGET_WSDL_URL',
                'https://webservice.exacttarget.com/etframework.wsdl'),
            'authenticationurl': getattr(settings, 'EXACT_TARGET_AUTH_URL',
                'https://auth.exacttargetapis.com/v1/requestToken?legacy=1'),
            'appsignature': None,
        }

        if properties:
            params.update(properties)

        ET_Client.__init__(self, get_server_wsdl=False,
            debug=False, params=params)


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


class Subscriber(object):
    def __init__(self, email=None, client=None):
        self.email = email
        if client:
            self.client = client
        else:
            self.client = ETClient()

    def fetch(self):
        if self.email:
            subscriber = ET_Subscriber()
            subscriber.auth_stub = self.client

    def remove_from_lists(self, list_ids):
        subscriber = ET_Subscriber()
        subscriber.auth_stub = self.client
        subscriber.props = {'SubscriberKey': email, 'EmailAddress': email,
            'Lists': [{'ID': x} for x in list_ids]}
        del_resp = subscriber.delete()

        return del_resp


    def save(self, properties=None):
        default_properties = {'EmailAddress': self.email,
            'SubscriberKey': self.email}

        if properties:
            default_properties.update(properties)


        subscriber = ET_Subscriber()
        subscriber.auth_stub = self.client
        subscriber.props = default_properties
        sub_response = subscriber.post()

        if sub_response.status is False and \
            sub_response.results[0]['ErrorCode'] == SUBSCRIBER_EXISTS_ERROR_CODE:
            sub_response = subscriber.patch()

        return sub_response


class DataExtension(object):
    def __init__(self, fields=None, name=None, client=None):
        self.fields = fields
        self.name = name
        if client:
            self.client = client
        else:
            self.client = ETClient()

    def add_row(self, properties, name=None, update=False):
        row = ET_DataExtension_Row()
        row.auth_stub = self.client
        row.CustomerKey = name if name else self.name
        row.props = properties
        if update:
            row_resp = row.patch()
        else:
            row_resp = row.post()
        if not row_resp and not update:
            # Error and we didn't do an update so
            # try to patch in case of primary key collision
            row_resp = row.patch()
        return row_resp

    def delete_row(self, properties, name=None):
        row = ET_DataExtension_Row()
        row.auth_stub = self.client
        row.CustomerKey = name if name else self.name
        row.props = properties

        return row.delete()


    def get_row_by_email(self, email, name=None, fields=None):
        row = ET_DataExtension_Row()
        row.auth_stub = self.client
        row.CustomerKey = name if name else self.name
        row.props = fields if fields else self.fields
        row.search_filter = {'Property': 'SubscriberKey',
            'SimpleOperator': 'equals', 'Value': email}

        return row.get()


    def get_rows(self, name=None, fields=None):
        rows = ET_DataExtension_Row()
        rows.auth_stub = self.client
        rows.CustomerKey = name if name else self.name
        rows.props = fields if fields else self.fields
        return rows.get()


    def get_all(self):
        de = ET_DataExtension()
        de.auth_stub = self.client
        de.props = ['CustomerKey', 'Name']
        return de.get()
