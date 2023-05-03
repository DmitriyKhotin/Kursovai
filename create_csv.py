from elasticsearch import Elasticsearch

client = Elasticsearch("http://localhost:9200")

tickets = client.search(index="ticket", body={"size": 30})
races = client.search(index="race", body={"size": 30})

with open("ticket.csv", "w") as ticket_f:
    with open("passenger.csv", "w") as passenger_f:
        ticket_f.write(
            "race_id,passenger_id\n"
        )
        passenger_f.write(
            "id,age\n"
        )
        age = 1
        for hit in tickets['hits']['hits']:
            ticket_f.write("{},{}\n".format(
                hit['_source']["race_id"],
                hit['_source']["id"])
            )
            passenger_f.write("{},{}\n".format(
                hit['_source']["id"],
                age)
            )
            age = age + 1


with open("race.csv", "w") as race_f:
    race_f.write(
        "_id,race_number\n"
    )
    for hit in races["hits"]["hits"]:
        race_f.write("{},{}\n".format(
            hit["_id"],
            hit['_source']["race_number"]
        ))
