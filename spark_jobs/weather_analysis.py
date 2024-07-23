from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, FloatType

def main():
    spark = SparkSession.builder \
        .appName("Weather Analysis") \
        .getOrCreate()

    schema = StructType([
        StructField("main", StructType([
            StructField("temp", FloatType(), True),
            StructField("pressure", FloatType(), True),
            StructField("humidity", FloatType(), True)
        ]), True),
        StructField("name", StringType(), True)
    ])

    kafka_df = spark.readStream.format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "weather") \
        .load()

    weather_df = kafka_df.selectExpr("CAST(value AS STRING)") \
        .select(from_json(col("value"), schema).alias("data")) \
        .select("data.*")

    query = weather_df.writeStream \
        .outputMode("append") \
        .format("console") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
