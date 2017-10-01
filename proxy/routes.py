from tornado.web import url
from .handlers import PuzzlesListHandler, SinglePuzzleHandler
from .helpers import get_api_url_prefix


def initialize_routes(schema):
    url_prefix = get_api_url_prefix(schema)
    routes = [
        url(url_prefix + r"/", PuzzlesListHandler),
        url(url_prefix + r"/(?P<id>[0-9a-zA-Z]+)", SinglePuzzleHandler),
    ]
    return routes
