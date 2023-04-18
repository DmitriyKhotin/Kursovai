import json
from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200")

ticketIndexName = "moving"
racesIndexName = "flight"

ticketDocType = "ticket"
raceDocType = "race"

# client.indices.delete(index=indexName)
client.indices.create(index=ticketIndexName)
client.indices.create(index=racesIndexName)

ticketMapping = {
    "properties": {
        "id": {
            "type": "text",
            "fielddata": True
        },
        "personal_data": {
            "type": "text",
            "fielddata": True
        },
        "buy_date": {
            "type": "text",
            "fielddata": True
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
}

raceMapping = {
    "properties": {
        "race_number": {
            "type": "integer",
            "fielddata": True
        },
        "info": {
            "type": "text",
            "fielddata": True
        },
        "from": {
            "type": "text",
            "fielddata": True
        },
        "to": {
            "type": "text",
            "fielddata": True
        },
        "sold_tickets_count": {
            "type": "integer",
            "fielddata": True
        },
        "remaining_tickets_count": {
            "type": "integer",
            "fielddata": True
        },
        "date_out": {
            "type": "text",
            "fielddata": True
        },
        "date_out_fact": {
            "type": "text",
            "fielddata": True
        },
        "date_in": {
            "type": "text",
            "fielddata": True
        },
        "date_in_fact": {
            "type": "text",
            "fielddata": True
        }
    }
}

client.indices.put_mapping(index=ticketIndexName,
                            doc_type=ticketDocType,
                            include_type_name="true",
                            body=ticketMapping
                            )

with open('tickets.json', 'r') as f:
    dataStore = json.load(f)
for data in dataStore:
    try:
        client.index(
            index=data["index"],
            doc_type=data["doc_type"],
            id=data["id"],
            body=data["body"]
        )
    except Exception as e:
        print(e)

client.indices.put_mapping(index=racesIndexName,
                            doc_type=raceDocType,
                            include_type_name="true",
                            body=raceMapping
                            )

with open('races.json', 'r') as f:
    dataStore = json.load(f)
for data in dataStore:
    try:
        client.index(
            index=data["index"],
            doc_type=data["doc_type"],
            id=data["id"],
            body=data["body"]
        )
    except Exception as e:
        print(e)

