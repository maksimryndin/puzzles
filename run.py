#!/usr/bin/env python
import tornado.ioloop
from tornado.options import options
from proxy.app import create_app

import settings     # Required for options definitions
from proxy.parser import provide_initial_data
from elasticsearch.client import Elasticsearch, IndicesClient


def main():
    app = create_app()
    app.listen(options.port)
    print("Puzzles Service Running on http://localhost:{port}".format(port=options.port))
    provide_initial_data(app)
    es = Elasticsearch(hosts=[options.es_host])
    indices = IndicesClient(es)
    indices.delete([options.index_name])
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
