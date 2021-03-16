from thingooConnector.connector import Connector

from thingooConnector.httpconnector import HTTPConnector
from thingooConnector.mqttconnector import MQTTConnector


class ThingooConnector(Connector):
    def __init__(self, host, device_info, entities, client_credentials, mqtt_credentials=None, http_only=False):
        """
        :param host: Thingoo host
        :param device_info: A device info object
        :type device_info: :class:`DeviceInfo`
        :param entities: A list of entities
        :param client_credentials: A ClientCredentials object used to get access_token
        :type device_info: :class:`ClientCredentials`
        :param mqtt_credentials: A UserData object used to connect to MQTT
        :type mqtt_credentials: :class:`MQTTCredentials`
        :param http_only: A boolean value that indicates if the device should only use http without connecting to mqtt
        :type http_only: bool
        """
        super().__init__(host, device_info, entities)
        self._http_connector = HTTPConnector(device_info, host, client_credentials, entities)
        self._http_only = http_only
        if not self._http_only:
            self._mqtt_connector = MQTTConnector(host, device_info, entities, mqtt_credentials)

    def connect(self):
        # Get access_token and register device via http
        self._http_connector.connect()
        if not self._http_only:
            # Connect to MQTT
            self._mqtt_connector.connect()

    def publish_entity_reading(self, entity, reading):
        if not self._http_only:
            # Publish via HTTP
            self._mqtt_connector.publish_entity_reading(entity, reading)
        else:
            # Publish via MQTT
            self._http_connector.publish_entity_reading(entity, reading)
