import json


class MyConditionsData:
    _instance = None

    def __new__(cls, filename):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            with open(filename) as f:
                cls._instance.data = json.load(f)
        return cls._instance

    def get(self, key):
        value = self.data.get(key)
        if value is not None:
            return value
        else:
            return set()
