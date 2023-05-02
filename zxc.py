tickets = client.search(index='ticket', body={"size": 30})
races = client.search(index='race', body={"size": 30})
# Запускаем функцию для сохранения данных в CSV-файлы
save_to_csv('passenger', 'passenger', ['id', 'name', 'email', 'phone', 'address'])
save_to_csv('ticket', 'ticket', ['id', 'passenger_id', 'purchase_date', 'price', 'flight_id'])
save_to_csv('flight', 'flight', ['id', 'number', 'from', 'to', 'sold_tickets', 'remaining_tickets', 'departure_date', 'actual_departure_date', 'arrival_date', 'actual_arrival_date'])

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

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
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

raceSchema = StructType([
    StructField("name", StringType(), True),
    StructField("age", IntegerType(), True)
])

passengerSchema = StructType([
    StructField("id", StringType(), True),
    StructField("personalData", StringType(), True),
    StructField("age", IntegerType(), True)
])





# Create data
data = [('First', 1), ('Second', 2), ('Third', 3), ('Fourth', 4), ('Fifth', 5)]
df = sparkSession.createDataFrame(data)
# Write into HDFS
df.write.csv("hdfs://localhost:9000/chapter5/example.csv")
# Read from HDFS
df_load = sparkSession.read.csv('hdfs://localhost:9000/chapter5/example.csv')
df_load.show()

# чтобы уменьшить число сообщений INFO
spark.sparkContext.setLogLevel("WARN")
# читать внутреннюю схему csv-файла (если она указана в 1-ой строке)
spark.read.load("hdfs://localhost:9000/chapter5/example.csv", format="csv", sep=",",
inferSchema="true", header="true")
# создать DataFrame из csv-файла с внутренней схемой
data=spark.read.load("hdfs://localhost:9000/chapter5/example.csv", format="csv", sep=",",
inferSchema="true", header="true")
# зарегистрировать DataFrame как временную таблицу temp
data.registerTempTable("temp")
# выполнить оператор select и показать результаты
df = spark.sql("select * from temp").show()