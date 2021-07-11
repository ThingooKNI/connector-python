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
temp = Entity("temp", "SENSOR", "DECIMAL", "C")
hum = Entity("hum", "SENSOR", "DECIMAL", "C")
entities = [temp, hum]

# Credentials
http_credentials = HTTPCredentials(HTTP_CLIENT_ID, HTTP_CLIENT_SECRET)
mqtt_credentials = MQTTCredentials(MQTT_USERNAME, MQTT_PASSWORD)

# Connector
connector = ThingooConnector("dev.thingoo.xyz", device_info, entities, http_credentials, mqtt_credentials)
connector.connect()

# Send readings
# temp.send_reading(connector,1.0) # Send a single reading to Thingoo instance
# Or send with given interval
temp.send_readings(connector, 10, data_function)  # Send a reading every 10 seconds
