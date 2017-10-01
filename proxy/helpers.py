import json

import ruamel.yaml
import jsonschema


def get_schema(schema_path):
    with open(schema_path) as schema_file:
        return ruamel.yaml.safe_load(schema_file)


def get_api_url_prefix(schema):
    return schema['basePath'][:-1]    # Remove trailing slash for clarity


def get_puzzle_definition(schema):
    return schema['definitions']['Puzzle']


def validate_puzzle_data(schema, raw_data):
    try:
        data = json.loads(raw_data.decode("UTF-8"))
    except ValueError:
        raise jsonschema.ValidationError(
            "Could not decode JSON object. Please check encoding."
        )
    jsonschema.validate(
        data,
        get_puzzle_definition(schema),
    )
    return data
