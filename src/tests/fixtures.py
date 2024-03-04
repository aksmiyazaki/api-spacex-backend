json_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "dummy": {
            "type": "string"
        }
    },
    "required": ["dummy"]
}

correct_json = {
    "dummy": "very_dummy"
}

incorrect_json = {
    "not_dummy": "very_dummy"
}

pristine_set_of_objects = '{"id": "123", "value": 1}\n{"id": "23", "value": 4}'
pristine_set_of_nested_objects = (
    """{"id": "abc123", "value": 42, "nested": {"first_nested": "first_value", "second_nested": {"third_nested": "third_value"}}}
{"id": "xyz789", "value": 99, "nested": {"first_nested": "another_value", "second_nested": {"third_nested": "more_value"}}}
{"id": "123xyz", "value": 73, "nested": {"first_nested": "nested_value", "second_nested": {"third_nested": "final_value"}}}""")

object_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {
            "type": "string"
        },
        "value": {
            "type": "integer"
        },
        "nested": {
            "type": "object",
            "properties": {
                "first_nested": {
                    "type": "string"
                },
                "second_nested": {
                    "type": "object",
                    "properties": {
                        "third_nested": {
                            "type": "string"
                        }
                    }

                }

            }
        }
    },
    "required": ["id", "value"]
}

objects_to_extract = [
    {"id": 123, "nested.first_nested.second_nested": "value1"},
    {"id": 666, "nested.first_nested.second_nested": "value32"}
]
transformed_objects = [
    [123, "value1"],
    [666, "value32"]
]


objects_to_extract_noncompliant_names = [
    {"xpto": 123, "asdfg": "value1"},
    {"xpto": 666, "asdfg": "value32"}
]
extraction_list = ["id", "nested.first_nested.second_nested"]
rename_list = [{"json_object_name": "xpto", "query_column_name": "id"},
               {"json_object_name": "asdfg", "query_column_name": "nested.first_nested.second_nested"}]
