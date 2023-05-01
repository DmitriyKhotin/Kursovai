from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200")

result = client.get(index="race", id="643c0a96e30e8aebb3d4113e");

print(result)