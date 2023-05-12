from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType, DateType

spark=SparkSession \
    .builder \
    .appName("Python Spark SQL basic example") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
spark.sparkContext.setLogLevel("WARN")
passengerSchema = StructType([
    StructField("id", StringType(), True),
    StructField("age", IntegerType(), True)
])
ticketSchema = StructType([
    StructField("race_id", StringType(), True),
    StructField("passenger_id", StringType(), True)
])
raceSchema = StructType([
    StructField("_id", StringType(), True),
    StructField("race_number", IntegerType(), True)
])
df_passenger= spark.read.load("hdfs://localhost:9000/chapter5/passenger.csv", format="csv", sep=",", inferScema="true", header="true", schema=passengerSchema)
df_race = spark.read.load("hdfs://localhost:9000/chapter5/race.csv", format="csv", sep=",", inferScema="true", header="true", schema=raceSchema)
df_ticket = spark.read.load("hdfs://localhost:9000/chapter5/ticket.csv", format="csv", sep=",", inferScema="true", header="true", schema=ticketSchema)
df_passenger.registerTempTable("passenger_t")
df_race.registerTempTable("race_t")
df_ticket.registerTempTable("ticket_t")

result_df = spark.sql(
    """
    SELECT race_t._id, COUNT(passenger_t.id)
    FROM race_t
    INNER JOIN ticket_t ON race_t._id = ticket_t.race_id
    INNER JOIN passenger_t ON passenger_t.id = ticket_t.passenger_id
    WHERE passenger_t.age < 12
    GROUP BY race_t._id
    """
)

result_df.show(n=result_df.count(), truncate=False)
input("Ctrl C")