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
# '{"one": "two"}\n{"three":"four"}'

object_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        "id": {
            "type": "string"
        },
        "value": {
            "type": "integer"
        }
    },
    "required": ["id", "value"]
}
