import json
from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200")

ticketIndexName = "ticket"
racesIndexName = "race"

ticketMapping = {
    "mappings": {
        "properties": {
            "id": {
                "type": "text",
                "fielddata": True
            },
            "personal_data": {
                "type": "text",
                "fielddata": True,
                "analyzer": "my_analyzer"
            },
            "buy_date": {
                "type":   "date",
                "format": "yyyy-MM-dd'T'HH:mm:ss.SSSZ||strict_date_optional_time",
            },
            "amount": {
                "type": "text",
                "fielddata": True
            },
            "race_id": {
                "type": "text",
                "fielddata": True
            }
        }
    },
    "settings": {
        "analysis":{
             "analyzer":{
                "my_analyzer":{
                   "type":"custom",
                   "tokenizer":"standard",
                   "filter":[
                      "lowercase",
                       "gender_stop",
                        "english_stemming"
                   ]
                },
             },
             "filter":{
                "gender_stop":{
                   "type":"stop",
                   "stopwords": ["male", "female"]
                },
                "english_stemming": {
                    "type": "snowball",
                    "language": "English"
                }
             }
        }
    }
}

client.indices.create(index=ticketIndexName, body=ticketMapping)

with open('tickets.json', 'r') as f:
    dataStore = json.load(f)
for data in dataStore:
    try:
        client.index(
            index=data["index"],
            id=data["id"],
            body=data["body"]
        )
    except Exception as e:
        print(e)