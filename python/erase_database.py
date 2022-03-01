from datetime import datetime
from engora.database import database
from engora.database.httpcache import http_response


db = database(name='engora_test_http_response')
db.create(http_response.Base, True)
