from elasticsearch import Elasticsearch
from py2neo import Graph, Node, Relationship, NodeMatcher
import json

graph_db = Graph("neo4j://localhost:7687/", auth = ('neo4j', 'iu6-magisters'))

result = graph_db.run(
    """
    MATCH (p:Passenger)-[r:Buy_ticket_on]->(f:Race) 
    WITH f, count(r) AS num 
    RETURN f, num 
    ORDER BY num DESC 
    LIMIT 1
    """
)

print(result)