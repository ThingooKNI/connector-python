from thingooConnector.device_info import DeviceInfo
from thingooConnector.entity import Entity
from thingooConnector.httpconnector import HTTPCredentials, HTTPConnector


# def test_get_token():
#     device_info = DeviceInfo("test", "test device")
#     credentials = ClientCredentials("thingoo-device", "SECRET")
#     connector = HTTPConnector(device_info, "dev.thingoo.xyz", credentials, [])
#     connector.connect()


def test_json():
    device_info = DeviceInfo("test", "test device")
    credentials = HTTPCredentials("#", "#")
    temp = Entity("temp", "SENSOR", "DECIMAL", "C")
    hum = Entity("hum", "SENSOR", "DECIMAL", "%")
    connector = HTTPConnector("#", device_info, [temp, hum], credentials)

    data = connector._create_registration_form()
    # FIXME Testing with real macAddress
    if str(
            data) != "{'key': 'test', 'macAddress': '00:00:00:00:00:00', 'displayName': 'test device', 'entities': [{'key': 'temp', 'type': 'SENSOR', 'valueType': 'DECIMAL', 'unitDisplayName': 'C'}, {'key': 'hum', 'type': 'SENSOR', 'valueType': 'DECIMAL', 'unitDisplayName': '%'}]}":
        raise AssertionError
