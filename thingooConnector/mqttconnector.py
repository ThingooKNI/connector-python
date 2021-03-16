import logging

import paho.mqtt.client as mqtt

from thingooConnector.connector import Connector

logger = logging.getLogger(__name__)


class MQTTCredentials:
    def __init__(self, username, password):
        self._username = username
        self._password = password

    def username(self):
        return self._username

    def password(self):
        return self._password


class MQTTConnector(Connector):
    def __init__(self, host, device_info, entities, mqtt_credentials, port=443):
        super().__init__(host, device_info, entities)
        self._port = port
        self._client = None
        self._mqtt_credentials = mqtt_credentials
        self._device_info = device_info

    def connect(self):
        self._client = mqtt.Client(
            client_id=self._device_info.key() + "ABCDEFGH",  # TODO Generate identifier
            transport="websockets"
        )
        self._client.username_pw_set(self._mqtt_credentials.username(), self._mqtt_credentials.password())
        self._client.on_connect = self._on_connect
        self._client.tls_set()
        self._client.connect(self._host, port=self._port)

    def _on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info('Connected to MQTT')
        else:
            logger.warning(f'Connection to MQTT failed with status code: {rc}')
        self._register()

    def _register(self):
        # Not used in the current implementation
        pass

    def publish_entity_reading(self, entity, reading):
        # TODO Implement publishing entity reading
        pass
