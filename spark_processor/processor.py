# 📁 File: spark_processor/processor.py (with anomaly detection and Cassandra write)
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, DoubleType, IntegerType, StringType
from cassandra.cluster import Cluster

spark = SparkSession.builder.appName("TelemetryProcessor").getOrCreate()

schema = StructType() \
    .add("vehicle_id", IntegerType()) \
    .add("timestamp", StringType()) \
    .add("lat", DoubleType()) \
    .add("lon", DoubleType()) \
    .add("speed", DoubleType()) \
    .add("fuel_level", DoubleType()) \
    .add("engine_temp", DoubleType())

df = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "vehicle-telemetry") \
    .load()

df_parsed = df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), schema).alias("data")).select("data.*")

def write_to_cassandra(row):
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect('telemetry')

    # Insert into vehicle_data
    session.execute("""
        INSERT INTO vehicle_data (vehicle_id, timestamp, lat, lon, speed, fuel_level, engine_temp)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (row['vehicle_id'], row['timestamp'], row['lat'], row['lon'], row['speed'], row['fuel_level'], row['engine_temp']))

    # Check for anomalies
    if row['speed'] > 100 or row['engine_temp'] > 110 or row['fuel_level'] < 10:
        issue = []
        if row['speed'] > 100:
            issue.append("Overspeed")
        if row['engine_temp'] > 110:
            issue.append("Overheat")
        if row['fuel_level'] < 10:
            issue.append("Low Fuel")

        session.execute("""
            INSERT INTO alerts (vehicle_id, timestamp, issues)
            VALUES (%s, %s, %s)
        """, (row['vehicle_id'], row['timestamp'], ', '.join(issue)))

query = df_parsed.writeStream.foreach(lambda row: write_to_cassandra(row.asDict())).start()
query.awaitTermination()