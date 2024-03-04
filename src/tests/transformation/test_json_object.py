import unittest

from tests import fixtures
from transformation.json_object import JSONObjectToListTransformer


class TestJSONObjectToListTransformer(unittest.TestCase):
    def setUp(self):
        self.__testing = JSONObjectToListTransformer(fixtures.extraction_list)

    def test_should_extract_when_deeply_nested(self):
        res = self.__testing.transform(fixtures.objects_to_extract[0])
        assert res == [123, "value1"]

    def test_should_extract_when_rename_fields(self):
        self.__testing = JSONObjectToListTransformer(fixtures.extraction_list, fixtures.rename_list)
        res = self.__testing.transform(fixtures.objects_to_extract_noncompliant_names[0])
        assert res == [123, "value1"]

if __name__ == '__main__':
    unittest.main()
