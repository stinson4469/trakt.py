from requests import Request
import json


class TraktRequest(object):
    def __init__(self, client, **kwargs):
        self.client = client
        self.configuration = client.configuration
        self.kwargs = kwargs

        self.request = None

        # Parsed Attributes
        self.path = None
        self.params = None

        self.data = None
        self.method = None

    def prepare(self):
        self.request = Request()

        self.transform_parameters()
        self.request.url = self.construct_url()

        self.request.method = self.transform_method()
        self.request.headers = self.transform_headers()

        data = self.transform_data()

        if data:
            self.request.data = json.dumps(data)

        return self.request.prepare()

    def transform_parameters(self):
        # Transform `path`
        self.path = self.kwargs.get('path')

        if not self.path.startswith('/'):
            self.path = '/' + self.path

        if self.path.endswith('/'):
            self.path = self.path[:-1]

        # Transform `params` into list
        self.params = self.kwargs.get('params') or []

        if isinstance(self.params, basestring):
            self.params = [self.params]

    def transform_method(self):
        self.method = self.kwargs.get('method')

        # Pick `method` (if not provided)
        if not self.method:
            self.method = 'POST' if self.data else 'GET'

        return self.method

    def transform_headers(self):
        headers = self.kwargs.get('headers') or {}
        headers['Content-Type'] = 'application/json'

        headers['trakt-api-key'] = self.client.configuration['client.id']
        headers['trakt-api-version'] = '2'

        if self.configuration['auth.login'] and self.configuration['auth.token']:
            # xAuth
            headers['trakt-user-login'] = self.configuration['auth.login']
            headers['trakt-user-token'] = self.configuration['auth.token']

        if self.configuration['oauth.token']:
            # OAuth
            headers['Authorization'] = 'Bearer %s' % self.configuration['oauth.token']

        return headers

    def transform_data(self):
        return self.kwargs.get('data') or None

    def construct_url(self):
        """Construct a full trakt request URI, with `api_key` and `params`."""
        path = [self.path]
        path.extend(self.params)

        return self.client.base_url + '/'.join(x for x in path if x)
