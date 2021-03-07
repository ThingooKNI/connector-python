import json
import logging
from http import HTTPStatus

import requests

from thingooConnector.config import REGISTER_ENDPOINT
from thingooConnector.encoder import ComplexEncoder

logger = logging.getLogger(__name__)


class ClientCredentials:
    """
    A class used for store client credentials which are used to get access token
    """

    def __init__(self, client_id, client_secret):
        self._client_id = client_id
        self._client_secret = client_secret

    def client_id(self):
        return self._client_id

    def client_secret(self):
        return self._client_secret


class HTTPException(Exception):
    def __init__(self, error_text, status_code, text):
        super().__init__(f'{error_text}: {status_code} {text}')


class RetrieveTokenException(HTTPException):
    def __init__(self, status_code, text):
        super().__init__("Fail to retrieve access token", status_code, text)


class RegisterDeviceException(HTTPException):
    def __init__(self, status_code, text):
        super().__init__("Fail to register device", status_code, text)


class Token:
    """
    A class used for store token
    """

    def __init__(self, json):
        """
        Create token from json
        :param json: A dict with token fields
        """
        self._access_token = json["access_token"]
        self._expires_in = json["expires_in"]

    def access_token(self):
        return self._access_token


class Connector:
    """
    Connector class to Thingoo instance
    """

    def __init__(self, device_info, host, client_credentials, entities):
        self._device_info = device_info
        self._host = host
        self._client_credentials = client_credentials
        self._token = None
        self._entities = entities

    def connect(self):
        """
        Connect to Thingoo instance: get token and register device
        """
        logger.info(f'Connecting to {self._host}...')
        # Get OAuth token or raise RetrieveTokenException
        self._token = self._get_token()
        # Register device or raise RegisterDeviceException
        self._register()
        logger.info(f'Device connected!')

    def _update_token(self):
        """
        Update token stored in self._token
        """
        try:
            self._token = self._get_token()
            logger.info("New OAuth token retrieved")
        except RetrieveTokenException:
            logger.warning("Fail to retrieve OAuth token")

    def _get_token(self):
        """
        Get OAuth access token
        :return: :class:`Token`
        :raises: :class:`RetrieveTokenException`
        """
        request_data = {
            "grant_type": "client_credentials",
            "client_id": self._client_credentials.client_id(),
            "client_secret": self._client_credentials.client_secret(),
        }
        url = f'https://{self._host}{REGISTER_ENDPOINT}'
        response = requests.post(url, data=request_data)
        if response.status_code == HTTPStatus.OK:
            return Token(response.json())
        raise RetrieveTokenException(response.status_code, response.text)

    def api_request(self, method, endpoint, data=None):
        """
        Send request to api
        :param method: A HTTP Method name GET/POST etc.
        :type method: str
        :param endpoint: A final endpoint, after default api prefix
        :type endpoint: str
        :param data: Optional data to send as json (if requests needs it)
        :return: :class:`Response`
        """
        url = f'https://{self._host}/api{endpoint}'
        headers = {
            "Authorization": "Bearer " + self._token.access_token(),
            "Content-Type": "application/json"
        }
        data = json.dumps(data, cls=ComplexEncoder)
        response = requests.request(method=method, url=url, data=data, headers=headers)
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            # Token expired, update token and try again
            self._update_token()
            response = requests.request(method=method, url=url, data=data, headers=headers)
        return response

    def _create_registration_form(self):
        """
        Create register form dict
        :return: A dict with key, macAddress, displayName and entities
        """
        info = self._device_info
        return {
            "key": info.key(),
            "macAddress": info.mac_address(),
            "displayName": info.display_name(),
            "entities": self._entities
        }

    def _register(self):
        """
        Send register POST request to api
        :raises: :class:`RegisterDeviceException`
        """
        data = self._create_registration_form()
        response = self.api_request("POST", "/devices", data)
        if response.status_code == HTTPStatus.OK:
            logger.info("Device registered successfully")
        else:
            raise RegisterDeviceException(response.status_code, response.text)

    def publish_entity_reading(self, entity, reading):
        """
        Publish reading from sensor to api
        :param entity: An Entity class
        :type entity: :class:`Entity`
        :param reading: Reading value
        """
        data = {
            "deviceKey": self._device_info.key(),
            "entityKey": entity.key(),
            "value": reading
        }
        response = self.api_request("POST", "/readings", data)
        if response.status_code == HTTPStatus.OK:
            logger.info(f'Reading {reading} from entity {entity.key()} published!')
        else:
            logger.warning(f'Fail to publish {reading} from entity {entity.key()} {response.text}')
