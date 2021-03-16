import json
import logging
from http import HTTPStatus

import requests

from thingooConnector import config
from thingooConnector.config import TOKEN_ENDPOINT
from thingooConnector.connector import Connector
from thingooConnector.encoder import ComplexEncoder

logger = logging.getLogger(__name__)


class ClientCredentials:
    """
         A class used for store client credentials which are used to get access token.
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


class TokenRetrievalException(HTTPException):
    def __init__(self, status_code, text):
        super().__init__("Failed to retrieve access token", status_code, text)


class DeviceRegistrationException(HTTPException):
    def __init__(self, status_code, text):
        super().__init__("Failed to register device", status_code, text)


class Token:
    """
    A class used to store the access token.
    """

    def __init__(self, json):
        """
        Creates a token instance from the provided JSON.
        :param json: A dict with token fields
        """
        self._access_token = json["access_token"]
        self._expires_in = json["expires_in"]

    def access_token(self):
        return self._access_token


class HTTPConnector(Connector):
    """
    A class used for connecting the device to a chosen Thingoo instance.
    """

    def __init__(self, host, device_info, entities, client_credentials):
        super().__init__(host, device_info, entities)
        self._client_credentials = client_credentials
        self._token = None

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
            logger.info("New JWT retrieved")
        except TokenRetrievalException:
            logger.warning("Fail to retrieve JWT")

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
        url = f'https://{self._host}{TOKEN_ENDPOINT}'
        response = requests.post(url, data=request_data)
        if response.status_code == HTTPStatus.OK:
            return Token(response.json())
        raise TokenRetrievalException(response.status_code, response.text)

    @staticmethod
    def _send_request(method, url, data, headers):
        """
        Send request to given URL
        :param method: A HTTP method
        :type method: str
        :param url: A HTTP request url
        :type url: str
        :param data: A data to be send
        :param headers: A HTTP headers
        :return: :class:`Response`
        """
        return requests.request(method=method, url=url, data=data, headers=headers)

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
        response = self._send_request(method, url, data, headers)
        if response.status_code == HTTPStatus.UNAUTHORIZED:
            # Token expired, update token and try again
            self._update_token()
            response = self._send_request(method, url, data, headers)
        return response

    def _register(self):
        """
        Send register POST request to api
        :raises: :class:`RegisterDeviceException`
        """
        data = self._create_registration_form()
        response = self.api_request("POST", config.DEVICES, data)
        if response.status_code == HTTPStatus.OK:
            logger.info("Device registered successfully")
        else:
            raise DeviceRegistrationException(response.status_code, response.text)

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
        response = self.api_request("POST", config.READINGS, data)
        if response.status_code == HTTPStatus.OK:
            logger.info(f'Reading {reading} from entity {entity.key()} published!')
        else:
            logger.warning(f'Fail to publish {reading} from entity {entity.key()} {response.text}')
