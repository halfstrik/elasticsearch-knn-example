from elasticsearch import Elasticsearch, RequestsHttpConnection, helpers
# from requests_aws4auth import AWS4Auth
# import boto3
import pandas as pd
# import numpy as np
from sentence_transformers import SentenceTransformer

# TensorFlow's installation on M1 mac is complicated, trying different options
# import tensorflow as tf
# import tensorflow_hub as tf_hub


if __name__ == '__main__':
    print('Hello world')

    # Step 1
    # credentials = boto3.Session().get_credentials()
    # awsAuth = AWS4Auth(
    #     credentials.access_key, credentials.secret_key, 'us-east-1', 'es',
    #     session_token=credentials.token
    # )
    # es = Elasticsearch(
    #     hosts=['https://vpc-rle-es-dev-mvbzqquajug7dlrxhzebkre5qq.us-east-1.es.amazonaws.com'],
    #     http_auth=awsAuth,
    #     use_ssl=True,
    #     verify_certs=True,
    #     connection_class=RequestsHttpConnection
    # )
    es = Elasticsearch(hosts='http://localhost:9200', request_timeout=30)
    es.ping()
    for index in es.indices.get('*'):
        print(index)

    # Step 2
    df = pd.read_csv('netflix_titles.csv')
    print(df.head(3))
    titles = df['title'].to_list()
    print('Titles count:', len(titles))

    # Step 3
    # embed = tf_hub.KerasLayer('https://tfhub.dev/google/nnlm-en-dim128/2')
    model = SentenceTransformer('all-MiniLM-L6-v2')

    vectors = []

    # for title in titles:
    #     # x = tf.constant([title])
    #     # embeddings = embed(x)
    #     # x = np.asarray(embeddings)
    #     # x = x[0].tolist()
    #     sentence_embeddings = model.encode(title)
    #     vectors.append(sentence_embeddings.tolist())
    #
    # print('Vectors count:', len(vectors))
    # print('Vector dim:', len(vectors[0]))

    settings = {
        'settings': {
            'number_of_shards': 1,
            # 'number_of_replicas': 1,
            'elastiknn': True
        },
        'mappings': {
            'dynamic': 'true',
            '_source': {
                'enabled': 'true'
            },
            'properties': {
                'title': {
                    'type': 'text'
                },
                'title_vector': {
                    'type': 'elastiknn_dense_float_vector',
                    "elastiknn": {
                        "dims": 384
                    }
                    # 'dimension': 128
                }
            }
        }
    }
    index_name = 'myml'
    # If index already created, skip
    # es.indices.delete(index=index_name, ignore=[400, 404])
    # my = es.indices.create(index=index_name, ignore=[400, 404], body=settings)
    # print(my)

    # Bulk insert, skip if already inserted
    # actions = [
    #     {
    #         '_index': 'myml',
    #         '_source': {
    #             'title': titles[i],
    #             'title_vector': vectors[i]
    #         }
    #     }
    #     for i in range(len(titles))
    # ]
    # helpers.bulk(es, actions)

    es.indices.refresh(index=index_name)
    print(es.cat.count(index=index_name, params={"format": "json"}))

    # Search testing
    search_term = 'Swiss Army Man'
    x = model.encode(search_term).tolist()
    print(x)
    # x = tf.constant([search_term])
    # embeddings = embed(x)
    # x = np.asarray(embeddings)
    # x = x[0].tolist()

    # TODO: find out if we can make cosineSimilarity to work
    # script_query = {
    #     'script_score': {
    #         'query': {
    #             'match_all': {},
    #             'script': {
    #                 'source': 'cosineSimilarity(params.query_vector, doc[\'title_vector\']) + 1.0',
    #                 'params': {'query_vector': x}
    #             }
    #         }
    #     }
    # }

    script_query_1 = {
        'elastiknn_nearest_neighbors': {
            'field': 'title_vector',
            'vec': {
                'values': x,
            },
            "model": "exact",
            "similarity": "cosine",
        }
    }

    response = es.search(
        index=index_name,
        body={
            'size': 10,
            'query': script_query_1,
            '_source': {'includes': ['title', 'body']}
        }
    )

    for hit in response['hits']['hits']:
        print(f"id: {hit['_id']}, score: {hit['_score']}")
        print(hit['_source'])
