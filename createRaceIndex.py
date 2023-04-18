import json
from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200")

raceIndexName = "race"

raceMapping = {
    "mappings": {
        "properties": {
            "race_number": {
                "type": "integer",
            },
            "info": {
                "type": "text",
                "fielddata": True,
                "analyzer": "my_analyzer"
            },
            "from": {
                "type": "text",
                "fielddata": True,
                "analyzer": "my_analyzer"
            },
            "to": {
                "type": "text",
                "fielddata": True,
                "analyzer": "my_analyzer"
            },
            "sold_tickets_count": {
                "type": "integer",
            },
            "remaining_tickets_count": {
                "type": "integer",
            },
            "date_out": {
                "type":   "date",
                "format": "yyyy-MM-dd'T'HH:mm:ss.SSSZ||strict_date_optional_time",
            },
            "date_out_fact": {
                "type":   "date",
                "format": "yyyy-MM-dd'T'HH:mm:ss.SSSZ||strict_date_optional_time",
            },
            "date_in": {
                "type":   "date",
                "format": "yyyy-MM-dd'T'HH:mm:ss.SSSZ||strict_date_optional_time",
            },
            "date_in_fact": {
                "type":   "date",
                "format": "yyyy-MM-dd'T'HH:mm:ss.SSSZ||strict_date_optional_time",
            },
        },
    },
    "settings": {
        "analysis":{
             "analyzer":{
                "my_analyzer":{
                   "type":"custom",
                   "tokenizer":"standard",
                   "filter":[
                      "lowercase",
                       "airlines_stop",
                        "english_stemming"
                   ]
                },
             },
             "filter":{
                "airlines_stop":{
                   "type":"stop",
                   "stopwords": ["Catar"]
                },
                "english_stemming": {
                    "type": "snowball",
                    "language": "English"
                }
             }
        }
    }
}


client.indices.create(index=raceIndexName, body=raceMapping)

with open('races.json', 'r') as f:
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
