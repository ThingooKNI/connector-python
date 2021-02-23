class Entity:
    def __init__(self, id_val, key, display_name, type_val, unit_type, unit_display_type):
        self._id = id_val
        self._key = key
        self._display_name = display_name
        self._type = type_val
        self._unit_type = unit_type
        self._unit_display_type = unit_display_type

    def publish_data(self, connector):
        # TODO Publish data
        pass

    def __repr__(self):
        return str({
            "id": self._id,
            "key": self._key,
            "displayName": self._display_name,
            "type": self._type,
            "unitType": self._unit_type,
            "unitDisplayName": self._unit_display_type
        })

    def __str__(self):
        return self.__repr__()
