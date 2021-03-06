from thingooConnector.connector import ClientCredentials, Connector
from thingooConnector.device_info import DeviceInfo
from thingooConnector.entity import Entity


# def test_get_token():
#     device_info = DeviceInfo("test", "test device")
#     credentials = ClientCredentials("thingoo-device", "SECRET")
#     connector = Connector(device_info, "dev.thingoo.xyz", credentials, [])
#     connector.connect()


def test_json():
    device_info = DeviceInfo("test", "test device")
    credentials = ClientCredentials("#", "#")
    temp = Entity("temp", "temperature", "SENSOR", "DECIMAL", "C")
    hum = Entity("hum", "humidity", "SENSOR", "DECIMAL", "%")
    connector = Connector(device_info, "#", credentials, [temp, hum])

    data = connector._create_registration_form()
    # FIXME Testing with real macAddress
    if str(
            data) != "{'key': 'test', 'macAddress': '00:00:00:00:00:00', 'displayName': 'test device', 'entities': [{'key': 'temp', 'displayName': 'temperature', 'type': 'SENSOR', 'unitType': 'DECIMAL', 'unitDisplayName': 'C'}, {'key': 'hum', 'displayName': 'humidity', 'type': 'SENSOR', 'unitType': 'DECIMAL', 'unitDisplayName': '%'}]}":
        raise AssertionError
