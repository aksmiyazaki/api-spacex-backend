import re
from logging import DEBUG, INFO

import psycopg2


class PostgresSink:
    class CannotExtractInsertionColumnsFromQuery(Exception):
        def __init__(self, query):
            super().__init__(f"Unable to extract the columns from your SQL query: {query}")

    def __init__(self, database_configs, clear_after_commit=True, logger=None):
        self.__database_configs = database_configs["connection"]
        self.__batch_size = database_configs["batch_size"]
        self.__insertion_sql = database_configs["insertion_sql"]
        self.__objects_to_insert = []
        self.__clear_after_commit = clear_after_commit
        self.__logger = logger

    def __log_if_set(self, msg, level=INFO):
        if self.__logger:
            self.__logger.log(level, msg)

    @property
    def amount_of_queued_objects(self):
        return len(self.__objects_to_insert)

    def insert_object(self, loaded_object, force_commit=False):
        self.__objects_to_insert.append(loaded_object)
        self.__log_if_set(f"Inserted Object {loaded_object}", DEBUG)

        if force_commit or len(self.__objects_to_insert) == self.__batch_size:
            self.commit_changes()

    def commit_changes(self):
        self.__log_if_set(f"Commiting changes")
        if len(self.__objects_to_insert) > 0:
            self.__persist_on_data_store()
        if self.__clear_after_commit:
            self.__objects_to_insert.clear()

    def fetch_insertion_fields_from_sql(self):
        columns_match = re.search(r'\((.*?)\)', self.__insertion_sql)
        if columns_match:
            columns_content = columns_match.group(1)
            return [column.strip() for column in columns_content.split(',')]
        else:
            raise PostgresSink.CannotExtractInsertionColumnsFromQuery(self.__insertion_sql)

    def __persist_on_data_store(self):
        with psycopg2.connect(**self.__database_configs) as conn:
            with conn.cursor() as cur:
                cur.executemany(self.__insertion_sql, self.__objects_to_insert)
                conn.commit()
