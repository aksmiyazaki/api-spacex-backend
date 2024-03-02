import json

from jsonschema.validators import validate


class FileLoader:
    def __init__(self, input_file_path, json_schema_path):
        self.__input_file_path = input_file_path
        self.__json_schema_path = json_schema_path
        self.__file = None
        self.__schema_file = None
        self.schema_keys = []

    def initialize_loader(self):
        self.__file = open(self.__input_file_path, "r")
        self.__schema_file = json.load(open(self.__json_schema_path, "r"))
        self.schema_keys = self.__extract_schema_keys(self.__schema_file)


    def __extract_schema_keys(self, schema):
        for key, value in schema.items():
            if key == "properties":
                return list(value.keys())

    def load_object_based_on_schema(self):
        line = self.__file.readline()
        if line:
            loaded_json = json.loads(line.strip())
            validate(instance=loaded_json, schema=self.__schema_file)
            return self.__filter_schema_fields(loaded_json)
        else:
            return None


    def __filter_schema_fields(self, json_object):
        new_object = {}
        for element in self.schema_keys:
            new_object[element] = json_object[element]
        return new_object

