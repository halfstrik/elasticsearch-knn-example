Sample project to help understand ElasticSearch with kNN

Idea link:
https://www.youtube.com/watch?v=qfCabSGzSZQ

kNN doc link:
https://docs.aws.amazon.com/opensearch-service/latest/developerguide/knn.html

Install requirements.txt
```
pip install -r requirements.txt
```

Setup Elasticsearch locally in docker (knn index not working, use AWS):
```
docker network create elastic
docker pull elasticsearch:7.17.4
docker run --name es01-test --net elastic -p 127.0.0.1:9200:9200 -p 127.0.0.1:9300:9300 -e "discovery.type=single-node" elasticsearch:7.17.4
```

CloudSentry creds:
```
export AWS_PROFILE=GR_GG_COF_AWS_SharedTech_Risk_Dev_Developer
cloudsentry access get --account cof-sharedtech-risk-dev --ba BASHAREDRISKSERVICES
```
