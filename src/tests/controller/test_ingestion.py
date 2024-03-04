import unittest
from unittest.mock import Mock, call

from controller.ingestion import IngestionController
from tests import fixtures


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.loader = Mock()
        self.sink = Mock()
        self.transformations = [Mock(), Mock()]

        self.controller = IngestionController(self.loader, self.sink, self.transformations)

    def test_ingest_calls_load_transform_and_insert(self):
        self.loader.load_object_based_on_schema.side_effect = [*fixtures.objects_to_extract, None]

        self.controller.ingest()

        assert self.loader.load_object_based_on_schema.call_count == 3
        self.transformations[0].transform.assert_has_calls([call(fixtures.objects_to_extract[0]),
                                                            call(fixtures.objects_to_extract[1])])
        self.sink.insert_object.assert_has_calls(
            [call(self.__nest_transformation_calls_on_object(self.transformations, fixtures.objects_to_extract[0])),
             call(self.__nest_transformation_calls_on_object(self.transformations, fixtures.objects_to_extract[1]))])

    def __nest_transformation_calls_on_object(self, transformations, object):
        transformed = object
        for t in transformations:
            transformed = t.transform(object)
        return transformed

    def test_ingest_commits_changes(self):
        self.loader.load_object_based_on_schema.return_value = None
        self.controller.ingest()
        self.sink.commit_changes.assert_called_with()


if __name__ == '__main__':
    unittest.main()
