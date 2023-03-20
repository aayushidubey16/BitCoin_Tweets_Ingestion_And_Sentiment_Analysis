from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from MyConfig import *

spark = SparkSession \
    .builder \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.11:2.3.2') \
    .master("local[*]") \
    .getOrCreate()

df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
  .option("subscribe", kafka_topic) \
  .option("startingOffsets", "latest") \
  .load()

df.printSchema() 

df = df.selectExpr("CAST(value AS STRING)")

sch = StructType([StructField("user_name",StringType(),True)
,StructField("user_location",StringType(), True)
,StructField("user_description",StringType() , True)
,StructField("user_created",TimestampType() , True)
,StructField("user_followers",StringType() , True)
,StructField("user_friends",StringType() , True)
,StructField("user_favourites",StringType() , True)
,StructField("user_verified",StringType() , True)
,StructField("date",TimestampType() , True)
,StructField("text",StringType() , True)
,StructField("hashtags",StringType() , True)
,StructField("source",StringType() , True)
,StructField("is_retweet",StringType() , True)])

df2=df.withColumn("value",from_json(df.value,sch))
df2.printSchema()

df3 = df2.select("value.*")
df3.printSchema()

df3 = df3.na.drop(subset=["text"]).filter(~(lower(col("source")).contains("bot")))

def cleanTweet(text):
    text = text.replace("#", "")
    text = re.sub('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', '', text, flags=re.MULTILINE)
    text = re.sub('@\\w+ *', '', text, flags=re.MULTILINE)
    return text 

convertUDF = udf(lambda z: cleanTweet(z)) 

df3 = df3.withColumn("text", convertUDF(col("text")))
df3.printSchema()

analyzer = SentimentIntensityAnalyzer()

def analyzeSentiment(text):
    return analyzer.polarity_scores(text)["compound"]

convertUDF = udf(lambda z: analyzeSentiment(z), DoubleType()) 

df3 = df3.withColumn("compound_sentiment_score", convertUDF(col("text")))
df3.printSchema()

rawQuery = df3 \
        .writeStream \
        .queryName("qraw")\
        .format("console")\
        .outputMode("append") \
        .start()

query = df3\
    .writeStream \
    .format("mongodb") \
    .option("checkpointLocation", stream_check_point_path) \
    .option("forceDeleteTempCheckpointLocation", "true") \
    .option("spark.mongodb.connection.uri", "mongodb+srv://" + mongo_user_name + ":" + mongo_password + "@cluster0.nwuw7.mongodb.net") \
    .option("spark.mongodb.database", mongo_db) \
    .option("spark.mongodb.collection", mongo_bitcoin_collection) \
    .outputMode("append") \
    .start()

query.awaitTermination()
rawQuery.awaitTermination()