from elasticsearch import helpers
from elasticsearch import Elasticsearch
from src.crawler import ImportedFileCrawler
from pathlib import Path

elastichost = 'localhost'
port        = 9200
index_name = 'mori_text'
counter     = 0
saveSize    = 3
es = Elasticsearch([{'host': elastichost, 'port' : port, 'scheme': 'http'}], verify_certs=False)

if es.ping():
    print("Connected to Elasticsearch")
else:
    print("Could not connect to Elasticsearch")

if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)
print("1")

data_path = Path(__file__).parent / "../data/products.json"
products_crawler = ImportedFileCrawler(data_path)
products_crawler.obtain_data()

actions = []
products = products_crawler.get_data()


print("1")

for product in products:
    source = product
    action = {
        "_index": index_name,
        "_id": counter,
        "_source": source
            }
    actions.append(action)
    counter += 1
    if len(actions) >= saveSize:
          helpers.bulk(es, actions)
          del actions[0:len(actions)]
    if counter >= 1:
        break

if len(actions) > 0:
  helpers.bulk(es, actions)

print('All Finished')