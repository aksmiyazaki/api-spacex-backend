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
