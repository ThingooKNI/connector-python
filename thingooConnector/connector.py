from abc import ABC, abstractmethod


class Connector(ABC):
    def __init__(self, host, device_info, entities):
        self._host = host
        self._device_info = device_info
        self._entities = entities

    @abstractmethod
    def connect(self):
        pass

    def _create_registration_form(self):
        """
        Create register form dict
        :return: A dict with key, macAddress, displayName and entities
        """
        info = self._device_info
        return {
            "key": info.key(),
            "macAddress": info.mac_address(),
            "displayName": info.display_name(),
            "entities": self._entities
        }

    @abstractmethod
    def publish_entity_reading(self, entity, reading):
        pass
