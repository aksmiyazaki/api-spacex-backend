import unittest
from unittest.mock import patch

import pytest

from sink.postgres import PostgresSink
from tests import fixtures


class TestPostgresSink(unittest.TestCase):
    def setUp(self):
        self.expected_sql_query = "INSERT INTO test_table (column1, column2) VALUES (%s, %s)"
        self.database_configs = {
            "connection": {
                "host": "localhost",
                "user": "test_user",
                "password": "test_password",
                "dbname": "test_db"
            },
            "batch_size": 2,
            "insertion_sql": self.expected_sql_query
        }

        self.sink = PostgresSink(self.database_configs, False)

    @patch('sink.postgres.psycopg2.connect')
    def test_should_insert_objects_and_commit_when_requested(self, patch_connect):
        self.sink.insert_object(fixtures.transformed_objects[0])
        self.sink.insert_object(fixtures.transformed_objects[1], force_commit=True)

        ## This patch is a tricky one.
        ## Whenever you use an object with a `with` clause, it calls this enter method.
        patch_connect().__enter__().cursor().__enter__().executemany.assert_called_once_with(self.expected_sql_query,
                                                                                             fixtures.transformed_objects)


    def test_should_extract_columns_from_sql_query(self):
        fields = self.sink.fetch_insertion_fields_from_sql()
        assert fields == ["column1", "column2"]

    def test_should_trigger_error_with_malformed_sql(self):
        self.database_configs["insertion_sql"] = "INSERT INTO invalid_query values"
        self.sink = PostgresSink(self.database_configs, clear_after_commit=False)
        with pytest.raises(PostgresSink.CannotExtractInsertionColumnsFromQuery):
            self.sink.fetch_insertion_fields_from_sql()

    @patch('sink.postgres.psycopg2.connect')
    def test_should_clear_after_commit_when_initialized_default(self, _):
        self.sink = PostgresSink(self.database_configs)
        self.sink.insert_object(fixtures.transformed_objects[0])
        self.sink.insert_object(fixtures.transformed_objects[1], force_commit=True)

        assert self.sink.amount_of_queued_objects == 0

if __name__ == '__main__':
    unittest.main()
