import json
from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200")

ticketIndexName = "ticket"
racesIndexName = "race"

# client.indices.delete(index=indexName)
client.indices.delete(index=ticketIndexName)
client.indices.delete(index=racesIndexName)


