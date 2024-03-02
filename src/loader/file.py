import json


class FileLoader:
    def __init__(self, input_file_path):
        self.__input_file_path = input_file_path
        self.__file = None

    def initialize_loader(self):
        self.__file = open(self.__input_file_path, "r")

    def load_object(self):
        line = self.__file.readline()
        if line:
            return json.loads(line)
        else:
            return None
