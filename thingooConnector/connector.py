import requests

from thingooConnector.config import TOKEN_ENDPOINT
from thingooConnector.device_info import DeviceInfo


class ClientCredentials:
    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret

    def client_id(self):
        return self._client_id

    def client_secret(self):
        return self._client_secret


class Token:
    def __init__(self, json_obj):
        self._access_token = json_obj["access_token"]
        self._expires_in = json_obj["expires_in"]

    def access_token(self):
        return self._access_token


class Connector:

    def __init__(self, device_id, host, client_credentials, entities):
        self._device_info = DeviceInfo(device_id)
        self._host = host
        self._client_credentials = client_credentials
        self._token = None

    def connect(self):
        self._token = self._get_token()
        self._register()

    def _get_token(self):
        request_data = {
            "grant_type": "client_credentials",
            "client_id": self._client_credentials.client_id(),
            "client_secret": self._client_credentials.client_secret()
        }
        url = f'https://{self._host}{TOKEN_ENDPOINT}'
        r = requests.post(url, data=request_data)
        return Token(r.json())

    def _register(self):
        pass
