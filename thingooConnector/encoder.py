import json


class ComplexEncoder(json.JSONEncoder):
    def default(self, o):  # pylint: disable=E0202
        if hasattr(o, "to_json"):
            return o.to_json()
        else:
            return json.JSONEncoder.default(self, o)
