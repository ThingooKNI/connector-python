# thingoo-connector-python

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/4395fbd80be94f54a333b2431b5053ff)](https://app.codacy.com/gh/ThingooKNI/connector-python?utm_source=github.com&utm_medium=referral&utm_content=ThingooKNI/connector-python&utm_campaign=Badge_Grade_Settings)

Python library for devices to connect to Thingoo platform

# Installation
1. Install required dependencies:
    ```shell script
       $ pip install -r requirements.txt
    ```
1. Build the library (you will get **.whl** in **dist** directory):
    ```shell script
       $ python setup.py bdist_wheel
    ```
1. Now you can install it via pip:
    ```shell script
       $ pip install dist/thingooConnector-*.whl
    ```

# Basic usage
```python
import random
from thingooConnector.device_info import DeviceInfo
from thingooConnector.entity import Entity
from thingooConnector.httpconnector import HTTPCredentials
from thingooConnector.mqttconnector import MQTTCredentials
from thingooConnector.thingooconnector import ThingooConnector


def data_function():
    return float(random.randrange(100, 500))/100

# Device configuration
device_info = DeviceInfo("testDevice3", "test device")
temp = Entity("temp", "SENSOR", "DECIMAL", "C")
hum = Entity("hum", "SENSOR", "DECIMAL", "C")
entities = [temp, hum]

# Credentials
http_credentials = HTTPCredentials("thingoo-device", "---CLIENT_SECRET----")
mqtt_credentials = MQTTCredentials("---USERNAME---", "---PASSWORD---")

# Connector
connector = ThingooConnector("dev.thingoo.xyz", device_info, entities, http_credentials, mqtt_credentials)
connector.connect()

# Send readings
# temp.send_reading(connector,1.0) # Send a single reading to Thingoo instance
# Or send with given interval
temp.send_readings(connector, 10, data_function) # Send a reading every 10 seconds
```