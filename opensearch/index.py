from opensearchpy import OpenSearch

os_client = OpenSearch(hosts='http://localhost:9200', request_timeout=30)
os_client.ping()
for index in os_client.indices.get('*'):
    print(index)

index_name = 'my_knn_index'


index_body = {
    "settings": {
        "index": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        }
    },
    "mappings": {
        "properties": {
          "age": {
            "type": "integer"
          }
        }
    }
}

response = os_client.indices.create(index_name, body=index_body)
