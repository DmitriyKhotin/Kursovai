from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from elasticsearch import Elasticsearch

spark=SparkSession \
.builder \
.appName("Python Spark SQL basic example") \
.config("spark.some.config.option", "some-value") \
.getOrCreate()
# чтобы уменьшить число сообщений INFO
spark.sparkContext.setLogLevel("WARN")
client = Elasticsearch("http://localhost:9200")

tickets = client.search(index="ticket", body={"size": 30})
races = client.search(index="race", body={"size": 30})

def load_csv(index, data_frame, schema):
    df = sparkSession.createDataFrame(data_frame, schema)
    # Write into HDFS
    df.write.csv("hdfs://localhost:9000/chapter5/" + index + ".csv")
    # Read from HDFS
    df_load = sparkSession.read.csv("hdfs://localhost:9000/chapter5/" + index + ".csv")
    df_load.show()


ticketSchema = StructType([
    StructField("id", StringType(), True),
    StructField("buy_date", StringType(), True),
    StructField("amount", StringType(), True),
    StructField("race_id", StringType(), True)
])

raceSchema = StructType([
    StructField("id", StringType(), True),
    StructField("race_number", IntegerType(), True),
    StructField("info", StringType(), True),
    StructField("from", StringType(), True),
    StructField("to", StringType(), True),
    StructField("sold_tickets_count", IntegerType(), True),
    StructField("remaining_tickets_count", IntegerType(), True),
    StructField("date_out", StringType(), True),
    StructField("date_out_fact", StringType(), True),
    StructField("date_in", StringType(), True),
    StructField("date_in_fact", StringType(), True),
])

passengerSchema = StructType([
    StructField("id", StringType(), True),
    StructField("personal_data", StringType(), True),
    StructField("age", IntegerType(), True)
])

passenger_array = []
ticket_array = []
race_arrray = []

age = 1
for hit in tickets['hits']['hits']:
    passenger_array.append((hit['_source']["id"], hit['_source']["personal_data"], age))
    age = age + 1

for hit in tickets['hits']['hits']:
    ticket_array.append((hit["_id"], hit['_source']["buy_date"], hit['_source']["amount"], hit['_source']["race_id"]))

for hit in races['hits']['hits']:
    race_arrray.append((hit["_id"], hit['_source']["race_number"], hit['_source']["info"], hit['_source']["from"], hit['_source']["to"], hit['_source']["sold_tickets_count"], hit['_source']["remaining_tickets_count"], hit['_source']["date_out"], hit['_source']["date_out_fact"], hit['_source']["date_in"], hit['_source']["date_in_fact"]))

load_csv('ticket', ticketSchema, ticket_array)
load_csv('passenger', passengerSchema, passenger_array)
load_csv('race', raceSchema, race_arrray)