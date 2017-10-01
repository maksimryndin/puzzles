import json
from tornado.testing import AsyncHTTPTestCase, gen_test
from tornado.options import options
from tornado import escape
from elasticsearch.client import IndicesClient, Elasticsearch

from proxy.app import create_app
from proxy.parser import provide_initial_data
from proxy.helpers import get_api_url_prefix
import tests.settings


class TestPuzzles(AsyncHTTPTestCase):

    def setUp(self):
        self.assertIn('test-', options.index_name)
        super().setUp()
        provide_initial_data(self._app)
        self.base_url = self.get_url("{url_prefix}".format(url_prefix=get_api_url_prefix(self._app.schema)))

    def tearDown(self):
        super().tearDown()
        self.delete_test_index()

    def delete_test_index(self):
        self.assertIn('test-', options.index_name)
        es = Elasticsearch(hosts=[options.es_host])
        indices = IndicesClient(es)
        indices.delete([options.index_name])

    def get_app(self):
        return create_app()

    @gen_test
    def test_create_and_get_puzzle(self):
        puzzle = {"name": "Тестовая задача", "description": "Тестовое описание", "answer": "Тестовый ответ"}
        response = yield self.http_client.fetch(self.base_url + "/", method='POST',
                                                headers={"Content-Type": "application/json"}, body=json.dumps(puzzle))
        created_puzzle = escape.json_decode(response.body)
        id = created_puzzle['_id']
        response = yield self.http_client.fetch(self.base_url + "/" + id, method='GET',
                                                headers={"Content-Type": "application/json"})
        fetched_puzzle = escape.json_decode(response.body)["_source"]
        self.assertEqual(puzzle["name"], fetched_puzzle["name"])

    @gen_test
    def test_create_and_delete_puzzle(self):
        puzzle = {"name": "Тестовая задача", "description": "Тестовое описание", "answer": "Тестовый ответ"}
        response = yield self.http_client.fetch(self.base_url + "/", method='POST',
                                                headers={"Content-Type": "application/json"}, body=json.dumps(puzzle))
        created_puzzle = escape.json_decode(response.body)
        id = created_puzzle['_id']
        response = yield self.http_client.fetch(self.base_url + "/" + id, method='DELETE',
                                     headers={"Content-Type": "application/json"})

        self.assertEqual("deleted", escape.json_decode(response.body)["result"])

    @gen_test
    def test_create_and_update_puzzle(self):
        puzzle = {"name": "Тестовая задача", "description": "Тестовое описание", "answer": "Тестовый ответ"}
        response = yield self.http_client.fetch(self.base_url + "/", method='POST',
                                                headers={"Content-Type": "application/json"}, body=json.dumps(puzzle))
        created_puzzle = escape.json_decode(response.body)
        id = created_puzzle['_id']
        puzzle_updated = {"name": "Тестовая задача обновлена", "description": "Тестовое описание обновлено"}
        response = yield self.http_client.fetch(self.base_url + "/" + id, method='PUT',
                                                headers={"Content-Type": "application/json"}, body=json.dumps(puzzle_updated))
        self.assertEqual("updated", escape.json_decode(response.body)["result"])
        self.assertFalse(escape.json_decode(response.body)["created"])
