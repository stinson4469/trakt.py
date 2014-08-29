from trakt.helpers import build_url
from trakt.interfaces.base import Interface


class OAuthInterface(Interface):
    path = 'oauth'

    def authorize_url(self, redirect_uri, response_type='code', state=None, username=None):
        return build_url(
            self.client.base_url,
            self.path, 'authorize',

            client_id=self.client.client_id,

            redirect_uri=redirect_uri,
            response_type=response_type,
            state=state,
            username=username
        )

    def token(self, code=None, redirect_uri=None, grant_type='authorization_code'):
        response = self.request('token', method='POST', data={
            'client_id': self.client.client_id,
            'client_secret': self.client.client_secret,

            'code': code,
            'redirect_uri': redirect_uri,
            'grant_type': grant_type
        })

        data = self.get_data(response, catch_errors=False)

        if not data:
            return None

        return data
