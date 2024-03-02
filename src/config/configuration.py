import json
from jsonschema import validate

class Configuration:
    def __init__(self, config_path, config_schema_path):
        with open(config_path, 'r') as config_file:
            self.configuration = json.load(config_file)

        with open(config_schema_path, 'r') as schema_file:
            self.__config_schema = json.load(schema_file)
        validate(instance=self.configuration, schema=self.__config_schema)
