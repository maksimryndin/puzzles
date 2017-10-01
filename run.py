#!/usr/bin/env python
import tornado.ioloop
from tornado.options import options
from proxy.app import create_app

import settings     # Required for options definitions
from proxy.parser import provide_initial_data
from elasticsearch.client import Elasticsearch, IndicesClient


def main():
    app = create_app()
    es = Elasticsearch(hosts=[options.es_host])
    indices = IndicesClient(es)
    if not indices.exists([options.index_name]):
        provide_initial_data(app, es=None)
    # TODO not load data after restart if exists
    #else:
        #indices.delete([options.index_name])
    app.listen(options.port)
    print("Puzzles Service Running on http://localhost:{port}".format(port=options.port))
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
