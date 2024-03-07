import json

from jsonschema.validators import validate


class FileLoader:
    def __init__(self, input_file_path, json_schema_path, logger=None):
        self.__input_file_path = input_file_path
        self.__json_schema_path = json_schema_path
        self.__file = None
        self.__schema_file = None
        self.__logger = logger
        self.schema_keys = []

    def __log_if_set(self, msg, level="INFO"):
        if self.__logger:
            self.__logger.log(msg, level)

    def initialize_loader(self):
        self.__file = open(self.__input_file_path, "r")
        self.__schema_file = json.load(open(self.__json_schema_path, "r"))
        self.schema_keys = self.__extract_schema_keys(self.__schema_file)
        self.__log_if_set("FileLoader Initialized")

    def __extract_schema_keys(self, schema):
        items = schema["properties"]
        accum = []

        def recursive_fetch(accum_key, items):
            for key, value in items.items():
                complete_key = f"{accum_key}.{key}" if accum_key else key
                if "properties" not in value:
                    accum.append(complete_key)
                else:
                    recursive_fetch(complete_key, value["properties"])

        recursive_fetch("", items)
        return accum

    def load_object_based_on_schema(self):
        line = self.__file.readline()
        if line:
            loaded_json = json.loads(line.strip())
            validate(instance=loaded_json, schema=self.__schema_file)
            self.__log_if_set(f"Object Loaded: {loaded_json}", "DEBUG")
            return self.__filter_schema_fields(loaded_json)
        else:
            return None

    def __filter_schema_fields(self, json_object):
        new_object = {}
        for element in self.schema_keys:
            if self.__nested_path_exists(json_object, element):
                new_object[element] = self.__index_nested_dict(json_object, element)
        return new_object

    def __index_nested_dict(self, nested_dict, dict_path):
        keys = dict_path.split('.')
        result = nested_dict

        try:
            for key in keys:
                result = result[key]
            return result
        except (KeyError, TypeError):
            return None

    def __nested_path_exists(self, nested_dict, dict_path):
        keys = dict_path.split('.')
        current_dict = nested_dict

        try:
            for key in keys:
                current_dict = current_dict[key]
            return True
        except (KeyError, TypeError):
            return False
