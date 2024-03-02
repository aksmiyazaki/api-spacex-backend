import unittest
from unittest.mock import patch, Mock

import pytest
from jsonschema.exceptions import ValidationError

from config.configuration import Configuration
from test.config import fixtures


class TestConfiguration(unittest.TestCase):

    @patch("config.configuration.json")
    @patch("config.configuration.open")
    def test_should_load_configuration_when_match_schema(self, _, json_patch):
        json_patch.load.side_effect = [fixtures.correct_json, fixtures.json_schema]
        config = Configuration("dummy_path", "dummy_schema_path")

        assert config.configuration["dummy"] == "very_dummy"

    @patch("config.configuration.json")
    @patch("config.configuration.open")
    def test_should_fail_load_configuration_when_mismatched_schema(self, _, json_patch):
        json_patch.load.side_effect = [fixtures.incorrect_json, fixtures.json_schema]
        with pytest.raises(ValidationError):
            Configuration("dummy_path", "dummy_schema_path")

if __name__ == '__main__':
    unittest.main()
