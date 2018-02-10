"""
Michael duPont - michael@mdupont.com
rocky.views.login.oauth
"""

import json
# library
from flask import url_for, request, redirect, session
from rauth import OAuth1Service, OAuth2Service
# module
from config import OAUTH_CREDENTIALS

KEY_MAPPER = {
    'facebook': {
        'email': 'email'
    }
}

def make_social_id(source: str, sid: int) -> str:
    """Create social ID from OAuth source and source id"""
    return '{}${}'.format(source, sid)

def make_user_data(source: str, resp: dict) -> dict:
    data = {'social_id': make_social_id(source, resp['id'])}
    for key, val in KEY_MAPPER[source].items():
        if key in resp:
            data[val] = resp[key]
    return data

def decoder(data: str) -> object:
    """Strict decode a JSON payload"""
    return json.loads(data.decode('utf-8', 'strict'))

class OAuthSignIn(object):
    providers = None

    def __init__(self, provider_name: str):
        self.provider_name = provider_name
        credentials = OAUTH_CREDENTIALS[provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        raise NotImplementedError()

    def callback(self):
        raise NotImplementedError()

    def get_callback_url(self):
        return url_for('oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(self, provider_name: str) -> 'OAuth Provider':
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]

class FacebookSignIn(OAuthSignIn):

    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://graph.facebook.com/oauth/authorize',
            access_token_url='https://graph.facebook.com/oauth/access_token',
            base_url='https://graph.facebook.com/'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url()
        ))

    def callback(self):
        if 'code' not in request.args:
            return None, None, None
        oauth_session = self.service.get_auth_session(
            data={'code': request.args['code'],
                  'grant_type': 'authorization_code',
                  'redirect_uri': self.get_callback_url()},
            decoder=json.loads
        )
        me = oauth_session.get('me?fields=id,email').json()
        return make_user_data('facebook', me)
