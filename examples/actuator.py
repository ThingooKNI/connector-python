import random

from examples.credentials import HTTP_CLIENT_ID, HTTP_CLIENT_SECRET, MQTT_USERNAME, MQTT_PASSWORD
from thingooConnector.device_info import DeviceInfo
from thingooConnector.entity import Entity
from thingooConnector.httpconnector import HTTPCredentials
from thingooConnector.mqttconnector import MQTTCredentials
from thingooConnector.thingooconnector import ThingooConnector


def data_function():
    return float(random.randrange(100, 500)) / 100


# Device configuration
device_info = DeviceInfo("testDevice3", "test device")
light_switch = Entity("light_switch", "ACTUATOR", "BOOLEAN", "")
heater = Entity("heater", "ACTUATOR", "BOOLEAN", "")
entities = [light_switch, heater]

# Credentials
http_credentials = HTTPCredentials(HTTP_CLIENT_ID, HTTP_CLIENT_SECRET)
mqtt_credentials = MQTTCredentials(MQTT_USERNAME, MQTT_PASSWORD)

# Connector
connector = ThingooConnector("dev.thingoo.xyz", device_info, entities, http_credentials, mqtt_credentials)
connector.connect()


def on_light_switch_command(topic, payload):
    print(payload)


def on_heater_command(topic, payload):
    print(payload)


# Send readings
light_switch.on_command(connector, on_light_switch_command)
heater.on_command(connector, on_heater_command)

input()  # don't close program, wait for commands
