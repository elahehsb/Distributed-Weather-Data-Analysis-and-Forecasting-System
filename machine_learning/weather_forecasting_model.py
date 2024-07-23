from pyspark.ml import Pipeline
from pyspark.ml.regression import LinearRegression
from pyspark.ml.feature import VectorAssembler
from pyspark.sql import SparkSession

def main():
    spark = SparkSession.builder \
        .appName("Weather Forecasting Model") \
        .getOrCreate()

    # Load and preprocess data
    df = spark.read.csv("hdfs://namenode:9000/data/weather_data.csv", header=True)
    assembler = VectorAssembler(inputCols=["temp", "pressure", "humidity"], outputCol="features")

    # Split data
    (training_data, test_data) = df.randomSplit([0.7, 0.3])

    # Define model
    lr = LinearRegression(labelCol="temp", featuresCol="features")

    # Build pipeline
    pipeline = Pipeline(stages=[assembler, lr])

    # Train model
    model = pipeline.fit(training_data)

    # Evaluate model
    predictions = model.transform(test_data)
    predictions.select("features", "temp", "prediction").show()

    spark.stop()

if __name__ == "__main__":
    main()
