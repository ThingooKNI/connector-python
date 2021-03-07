import threading


class Entity:
    def __init__(self, key, type_val, unit_type, unit_display_type):
        self._key = key
        self._type = type_val
        self._unit_type = unit_type
        self._unit_display_type = unit_display_type

    def publish_data(self, connector):
        # TODO Publish data
        pass

    def __repr__(self):
        return str(self.to_json())

    def __str__(self):
        return self.__repr__()

    def to_json(self):
        return {
            "key": self._key,
            "type": self._type,
            "unitType": self._unit_type,
            "unitDisplayName": self._unit_display_type
        }
