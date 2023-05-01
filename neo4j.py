from elasticsearch import Elasticsearch
from py2neo import Graph, Node, Relationship

# Создание клиента для связи с Elasticsearch
client = Elasticsearch("http://localhost:9200")

# Подключение к графовой базе neo4j
graph_db = Graph("http://localhost:7474/", auth = ('neo4j', 'iu6-magisters'))

# в следующей строке необходимо снять комментарий,  если программа запускается 
# повторно
# graph_db.delete_all()

# Поиск по билетам
tickets = client.search(index="ticket")

# Цикл по билетам
for ticket in tickets:
    try:
        # Создание узла типа «Passenger» в графе для текущего билета
        PassengerNode = Node("Passenger", id=ticket["_source"]["id"], personal_data=ticket["_source"]["personal_data"])
        graph_db.create(PassengerNode)
    except Exception as e:
        print(e)
        continue
    # Поиск рейса в Elasticsearch, на который был куплен билет
    race = client.get(index="race", id=ticket["_source"]["id"])
    print(race)
    # Создаем узел рейса
    try:
        # Поиск в графе текущего рейса
        RaceNode = graph_db.nodes.match("Race", race_number=race["_source"]["race_number"], date_out=race["_source"]["date_out"],date_out_fact=race["_source"]["date_out_fact"],date_in=race["_source"]["date_in"],date_in_fact=race["_source"]["date_in_fact"])
        if RaceNode == None:
            # Если нет, то создать узел типа «Race» в графе для текущего пассажира
            RaceNode = Node("Race", race_number=race["_source"]["race_number"], date_out=race["_source"]["date_out"],date_out_fact=race["_source"]["date_out_fact"],date_in=race["_source"]["date_in"],date_in_fact=race["_source"]["date_in_fact"])
            graph_db.create(RaceNode)
        # Cвязать в графе узел пассажира (PassengerNode) и узел рейса (RaceNode)
        # отношением (связью) типа Куплен_билет_на
        NodesRelationship = Relationship(PassengerNode, "Buy_ticket_on", RaceNode, buy_date=ticket["_source"]["buy_date"], amount=ticket["_source"]["amount"])
        graph_db.create(NodesRelationship)
    except Exception as e:
        print(e)
        continue

result = graph_db.run("MATCH (p:Passenger)-[r:Buy_ticket_on]->(f:Race) RETURN p.id, f.race_number, r.amount")
for row in result:
    print(row)