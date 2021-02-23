def get_mac_address():
    # TODO Get real MAC address from device
    return "00:00:00:00:00:00"


class DeviceInfo:
    def __init__(self, device_id):
        self._device_id = device_id
        self._mac_address = get_mac_address()

    def device_id(self):
        return self._device_id

    def mac_address(self):
        return self._mac_address
