from elasticsearch.client import Elasticsearch
from tornado_elasticsearch import (AsyncHttpConnection as TornadoESAsyncHttpConnection,
                                   AsyncElasticsearch as TornadoESAsyncElasticsearch,
                                   AsyncTransport)


class AsyncHttpConnection(TornadoESAsyncHttpConnection):
    """Patch due to AttributeError: 'AsyncHttpConnection' object has no attribute 'transport_schema'
    """
    transport_schema = "http"


class AsyncElasticsearch(TornadoESAsyncElasticsearch):

    def __init__(self, *args, **kwargs):
        kwargs['connection_class'] = AsyncHttpConnection
        kwargs['transport_class'] = AsyncTransport
        Elasticsearch.__init__(self, *args, **kwargs)
