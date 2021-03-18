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
from thingooConnector.httpconnector import HTTPConnector, HTTPCredentials
from thingooConnector.device_info import DeviceInfo
from thingooConnector.entity import Entity
import random


def data_function():
    return float(random.randrange(100, 500))/100

device_info = DeviceInfo("testDevice", "test device")
credentials = ClientCredentials("thingoo-device", "CLIENT_SECRET")
temp = Entity("temp", "SENSOR", "DECIMAL", "C")
connector = HTTPConnector(device_info, "dev.thingoo.xyz", credentials, [temp])
connector.connect()
# temp.send_reading(connector,1.0) # Send a single reading to Thingoo instance
# Or send with given interval
temp.send_readings(connector, 10, data_function) # Send a reading every 10 seconds
```