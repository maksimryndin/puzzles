import tornado.web
from tornado.options import options, parse_command_line

from .helpers import get_schema
from .routes import initialize_routes
from .es_client import AsyncElasticsearch


def create_app():
    parse_command_line()
    schema = get_schema(options.schema_path)
    app = tornado.web.Application(initialize_routes(schema), debug=options.debug)
    app.schema = schema
    app.es_client = AsyncElasticsearch(hosts=["http://localhost:9200"])
    return app
