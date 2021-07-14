import threading
import logging

logger = logging.getLogger(__name__)


class Entity:
    def __init__(self, key, type_val, value_type, unit_display_type):
        self._key = key
        self._type = type_val
        self._value_type = value_type
        self._unit_display_type = unit_display_type

    def on_command(self, connector, callback_function):
        connector.subscribe_to_commands(self, callback_function)

    def send_reading(self, connector, value):
        """
        Send single reading to api
        :param connector: A connector to Thingoo instance
        :type connector: :class:`Connector`
        :param value: Value to send to api
        """
        connector.publish_entity_reading(self, value)

    def send_readings(self, connector, interval, data_function):
        """
        Send data to api periodically with given interval
        :param connector: A connector to Thingoo instance
        :type connector: :class:`Connector`
        :param interval: Interval in seconds between execution this function
        :param data_function: Function which return data from sensor
        """
        # Get reading
        threading.Timer(
            interval, self.send_readings, [connector, interval, data_function]
        ).start()
        value = data_function()
        self.send_reading(connector, value)

    def key(self):
        return self._key

    def __repr__(self):
        return str(self.to_json())

    def __str__(self):
        return self.__repr__()

    def to_json(self):
        return {
            "key": self._key,
            "type": self._type,
            "valueType": self._value_type,
            "unitDisplayName": self._unit_display_type,
        }
