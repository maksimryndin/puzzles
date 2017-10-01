from tornado import web, gen
from tornado.options import options
from jsonschema import ValidationError

from .helpers import validate_puzzle_data


class BaseHandler(web.RequestHandler):

    def initialize(self):
        self.set_header("Content-Type", "application/json")
        self.schema = self.application.schema

    def write_error(self, status_code, **kwargs):
        self.clear()
        self.set_status(status_code)
        exception = kwargs["exc_info"][1]
        if isinstance(exception, ValidationError):
            self.set_status(400)
            self.write({'status': 'validation error', 'data': str(exception)})
            self.finish()
        else:
            self.set_status(500)
            self.write({'status': 'fail', 'data': str(exception) if options.debug else ''})
            self.finish()


class PuzzlesListHandler(BaseHandler):
    """Search and creation handler.
    """

    async def get(self, *args, **kwargs):
        result = yield self.application.es_client.search(index=options.index_name)
        self.finish(result)

    @web.asynchronous
    @gen.engine
    def post(self, *args, **kwargs):
        raw_data = self.request.body
        data = validate_puzzle_data(self.schema, raw_data)
        result = yield self.application.es_client.index(index=options.index_name,
                                                        doc_type=options.es_type,
                                                        body=data)
        self.finish(result)


class SinglePuzzleHandler(BaseHandler):
    """Read, Update and Delete handler.
    """

    @web.asynchronous
    @gen.engine
    def delete(self, *args, **kwargs):
        result = yield self.application.es_client.delete(index=options.index_name, doc_type=options.es_type,
                                                         id=self.path_kwargs['id'])
        self.finish(result)

    @web.asynchronous
    @gen.engine
    def get(self, *args, **kwargs):
        result = yield self.application.es_client.get(index=options.index_name, doc_type=options.es_type,
                                                      id=self.path_kwargs['id'])
        self.finish(result)

    @web.asynchronous
    @gen.engine
    def put(self, *args, **kwargs):
        raw_data = self.request.body
        #data = validate_puzzle_data(self.schema, raw_data)
        result = yield self.application.es_client.index(index=options.index_name, doc_type=options.es_type,
                                                        id=self.path_kwargs['id'], body=raw_data)
        self.finish(result)
