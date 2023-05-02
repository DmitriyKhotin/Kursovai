from pyspark.sql import SparkSession
sparkSession = SparkSession.builder.appName("example-pyspark-read-and-write").getOrCreate()
# Create data
data = [('First', 1), ('Second', 2), ('Third', 3), ('Fourth', 4), ('Fifth', 5)]
df = sparkSession.createDataFrame(data)
# Write into HDFS
df.write.csv("hdfs://localhost:9000/chapter5/example.csv")
# Read from HDFS
df_load = sparkSession.read.csv('hdfs://localhost:9000/chapter5/example.csv')
df_load.show()