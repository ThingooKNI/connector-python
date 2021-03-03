import requests

from config import REGISTER_ENDPOINT


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

    def __init__(self, device_info, host, client_credentials, entities):
        self._device_info = device_info
        self._host = host
        self._client_credentials = client_credentials
        self._token = None
        self._entities = entities

    def connect(self):
        self._get_and_save_token()
        self._register()

    def _get_and_save_token(self):
        self._token = self._get_token()

    def _get_token(self):
        request_data = {
            "grant_type": "client_credentials",
            "client_id": self._client_credentials.client_id(),
            "client_secret": self._client_credentials.client_secret(),
        }
        url = f'https://{self._host}{REGISTER_ENDPOINT}'
        r = requests.post(url, data=request_data)
        return Token(r.json())

    def api_request(self, method, endpoint, data=None):
        url = f'https://{self._host}/api{endpoint}'
        headers = {
            "Authorization": "Bearer " + self._token.access_token(),
            "Content-Type": "application/json"
        }
        response = requests.request(method=method, url=url, json=data, headers=headers)
        if response.status_code == 401:
            self._get_and_save_token()
            response = requests.request(method=method, url=url, json=data, headers=headers)
        return response

    def _create_registration_form(self):
        info = self._device_info
        return {
            "key": info.key(),
            "macAddress": info.mac_address(),
            "displayName": info.display_name(),
            "entities": self._entities
        }

    def _register(self):
        data = self._create_registration_form()
        return self.api_request("POST", "/devices", data)
