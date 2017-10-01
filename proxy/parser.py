#!/usr/bin/env python
import re
from tornado.options import options
from elasticsearch.helpers import bulk
from elasticsearch.client import Elasticsearch
import jsonschema

from .helpers import get_puzzle_definition


class Puzzle:
    def __init__(self):
        self.name = None
        self.description = None
        self.answer = None
        self.tags = []


class Parser:

    def __init__(self, file_path, schema):
        self.file_path = file_path
        self.schema = schema
        self.puzzle_definition = get_puzzle_definition(self.schema)

    def parse_file(self):
        with open(self.file_path) as input_file:
            allowed_attributes = self.puzzle_definition['properties'].keys()
            puzzle = {}
            for line in input_file:
                if line == "\n":
                    if puzzle:
                        try:
                            jsonschema.validate(
                                puzzle,
                                self.puzzle_definition,
                            )
                        except jsonschema.ValidationError:
                            print("Invalid data {}".format(puzzle))
                        else:
                            yield puzzle
                    puzzle = {}
                else:
                    match = re.search(r"^(?P<attribute>\w+):\s(?P<value>.*)\n$", line, re.IGNORECASE)
                    if match:
                        attribute = match.group('attribute').lower() if match.group('attribute') else None
                        if attribute in allowed_attributes:
                            value = match.group('value')
                            puzzle[attribute] = value


def provide_initial_data(app, es=None):
    puzzles = Parser(options.data_file_path, app.schema).parse_file()
    actions = [{
        "_index": options.index_name,
        "_type": options.es_type,
        "_source": puzzle
    } for puzzle in puzzles]
    if es is None:
        es = Elasticsearch(hosts=[options.es_host])
    bulk(es, actions)

