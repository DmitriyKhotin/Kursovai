from elasticsearch import Elasticsearch
from py2neo import Graph, Node, Relationship, NodeMatcher
import json

client = Elasticsearch("http://localhost:9200")

graph_db = Graph("neo4j://localhost:7687/", auth = ('neo4j', 'iu6-magisters'))
graph_db.delete_all()

tickets = client.search(index="ticket", body={"size": 30})

for ticket in tickets['hits']['hits']:
    print("\n")
    print("\n")
    try:
        PassengerNode = Node("Passenger", id=ticket["_source"]["id"], personal_data=ticket["_source"]["personal_data"])
        graph_db.create(PassengerNode)
    except Exception as e:
        print("Не удалось создать ноду Passenger")
        continue

    print("Поиск рейса в Elasticsearch")
    try:
        race = client.get(index="race", id=ticket["_source"]["race_id"])
    except Exception as e:
        print("Не удалось найти race")
        continue

    print("Создаем узел рейса")
    RaceNode = graph_db.nodes.match("Race", race_number=race["_source"]["race_number"], date_out=race["_source"]["date_out"],date_out_fact=race["_source"]["date_out_fact"],date_in=race["_source"]["date_in"],date_in_fact=race["_source"]["date_in_fact"]).first()
    if RaceNode == None:
        print("Такая нода рейса еще не существует")
        RaceNode = Node("Race", race_number=race["_source"]["race_number"], date_out=race["_source"]["date_out"],date_out_fact=race["_source"]["date_out_fact"],date_in=race["_source"]["date_in"],date_in_fact=race["_source"]["date_in_fact"])
        graph_db.create(RaceNode)
    try:
        NodesRelationship = Relationship(PassengerNode, "Buy_ticket_on", RaceNode, buy_date=ticket["_source"]["buy_date"], amount=ticket["_source"]["amount"])
        graph_db.create(NodesRelationship)
        print("Отношение создано")
    except Exception as e:
        print("Не удалось создать отношение")
        continue

