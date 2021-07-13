import logging

import paho.mqtt.client as mqtt

from thingooConnector.config import DEVICE_READINGS, DEVICE_COMMANDS
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
        self._subscriptions = {}

    def connect(self):
        self._client = mqtt.Client(
            client_id=self._device_info.key() + "ABCDEFGH",  # TODO Generate identifier
            transport="websockets",
        )
        self._client.username_pw_set(
            self._mqtt_credentials.username(), self._mqtt_credentials.password()
        )
        self._client.on_connect = self._on_connect
        self._client.on_message = self._on_message
        self._client.tls_set()
        self._client.connect(self._host, port=self._port)
        self._client.loop_start()

    def _on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            logger.warning(f"Connection to MQTT failed with status code: {rc}")
            return
        logger.info("Connected to MQTT")
        self._register()
        self._renew_subscriptions()

    def _renew_subscriptions(self):
        for topic, function in self._subscriptions.items():
            self.subscribe_topic(topic, function)

    def _on_message(self, client, userdata, msg):
        topic = msg.topic
        payload = msg.payload.decode("utf-8")
        if topic in self._subscriptions:
            function = self._subscriptions[topic]
            if function is not None:
                function(topic, payload)
            else:
                self._mqtt_message_default_function(topic, payload)

    def _mqtt_message_default_function(self, topic, payload):
        text = f"{self._host}:{self._port} {topic} {payload}"
        logger.info(text)

    def _register(self):
        # Not used in the current implementation
        pass

    def publish_entity_reading(self, entity, reading):
        topic = DEVICE_READINGS.format(
            device_key=self._device_info.key(), entity_key=entity.key()
        )
        self._client.publish(topic, reading, qos=1)
        self.subscribe_topic(topic + "/response")
        logger.info(f"Reading {reading} from entity {entity.key()} published via MQTT!")

    def subscribe_to_commands(self, entity, callback_function):
        topic = DEVICE_COMMANDS.format(
            device_key=self._device_info.key(), entity_key=entity.key()
        )
        self.subscribe_topic(topic, callback_function)

    def subscribe_topic(self, topic, function=None):
        self._client.subscribe(topic)
        self._subscriptions[topic] = function
