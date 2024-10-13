class JsonParser:
    def __init__(self, json_data):
        self.data = json_data

    def __getattr__(self, attr):
        if isinstance(self.data, dict):
            if attr in self.data:
                value = self.data[attr]
                if isinstance(value, (dict, list)):
                    return JsonParser(value)
                return value
        return JsonParser({})

    def __getitem__(self, key):
        if isinstance(self.data, list):
            if isinstance(key, int) and 0 <= key < len(self.data):
                value = self.data[key]
                if isinstance(value, (dict, list)):
                    return JsonParser(value)
                return value
        return JsonParser({})

    def __str__(self):
        return str(self.data)

    def __bool__(self):
        return bool(self.data)



