import pprint
from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200")
indexName = "ticket"

searchBody = {
    "_source": ["id", "personal_data", "buy_date", "amount", "race_id"],
    "query": {
        "simple_query_string": {
            "query": 'Orchestrator',
            "fields": ["personal_data"]
        },
    },
}

result = client.search(index=indexName, body=searchBody)
pprint.pprint(result)