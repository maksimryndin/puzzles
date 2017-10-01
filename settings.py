import os
from tornado.options import define


PROJECT_ROOT = os.environ.get("PROJECT_ROOT", os.path.dirname(os.path.abspath(__file__)))

define("port", default=os.environ.get('PORT', 8888), help="run on the given port", type=int)
define("debug", default=os.environ.get('DEBUG', False), help="debug mode")

define("schema_path", default=os.environ.get('SCHEMA_PATH', os.path.join(PROJECT_ROOT, "docs", "puzzles_spec.yml")),
       help="schema path")
define("data_file_path", default=os.environ.get('DATA_FILE_PATH', os.path.join(PROJECT_ROOT, "sample", "data.txt")),
       help="initial data file path")
define("index_name", default=os.environ.get('INDEX_NAME', 'puzzles-index'),
       help="Index name for Elasticsearch")
define("es_type", default=os.environ.get('ES_TYPE', 'puzzle'),
       help="Type name for Elasticsearch")
define("es_host", default=os.environ.get('ES_HOST', "http://localhost:9200"),
       help="Elasticsearch protocol://domain:port")
