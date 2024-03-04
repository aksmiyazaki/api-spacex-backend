import io
import json
import unittest
from unittest.mock import patch, Mock, call

from loader.file import FileLoader
from tests import fixtures


class FileLoaderTest(unittest.TestCase):
    def setUp(self):
        self.__expected_file_path = "dummy_path"
        self.__expected_schema_path = "dummy_schema_path"

    def initialize_file_loader(self):
        file_loader = FileLoader(self.__expected_file_path, self.__expected_schema_path)
        file_loader.initialize_loader()
        return file_loader

    @patch("loader.file.open")
    def test_should_initialize_loader(self, open_patch):
        open_patch.side_effect = ["", io.StringIO(json.dumps(fixtures.object_schema))]
        loader = self.initialize_file_loader()

        open_patch.assert_has_calls([call(self.__expected_file_path, "r"),
                                     call(self.__expected_schema_path, "r")])
        assert loader.schema_keys == ["id", "value", "nested.first_nested", "nested.second_nested.third_nested"]



    @patch("loader.file.open")
    def test_should_load_object_when_requested(self, open_patch):
        open_patch.side_effect = [io.StringIO(fixtures.pristine_set_of_objects),
                                  io.StringIO(json.dumps(fixtures.object_schema))]
        file_mock_object = Mock()
        file_mock_object.readline.return_value = json.dumps(fixtures.correct_json)
        open_patch.return_value = file_mock_object

        file_loader = self.initialize_file_loader()
        res = file_loader.load_object_based_on_schema()

        assert res["id"] == "123"
        assert res["value"] == 1

    @patch("loader.file.open")
    def test_should_return_none_when_finish(self, open_patch):

        file_mock_object = Mock()
        file_mock_object.readline.return_value = None
        open_patch.side_effect = [file_mock_object,
                                  io.StringIO(json.dumps(fixtures.object_schema))]

        file_loader = self.initialize_file_loader()
        res = file_loader.load_object_based_on_schema()

        assert res is None

    @patch("loader.file.open")
    def test_should_load_object_when_input_is_nested_json(self, open_patch):
        open_patch.side_effect = [io.StringIO(fixtures.pristine_set_of_nested_objects),
                                  io.StringIO(json.dumps(fixtures.object_schema))]
        file_mock_object = Mock()
        file_mock_object.readline.return_value = json.dumps(fixtures.correct_json)
        open_patch.return_value = file_mock_object

        file_loader = self.initialize_file_loader()
        res = file_loader.load_object_based_on_schema()

        assert res["id"] == "abc123"
        assert res["value"] == 42


if __name__ == '__main__':
    unittest.main()
