# BitCoin Tweets Ingestion And Sentiment Analysis

## Project Goal:
    The main goal of project is to build Bitcoin data ingestion pipeline using Kafka Message Queueing System and Spark Structured Streaming. 
Following steps are involved in data ingestion and analysis pipeline:
* In first step, Using KafkaProducer from Kafka module we are first pushing record by record data into kafka-topic. 
* Second step is the main step of pipeline in which through spark streaming job "BitCoinTweetDataIngestionStreaming" we are consuming messages from kafka-topic.
* In part(b) of second step we are filtering data and calculating a sentiment score for each and evry record with help of VADER (Valence Aware Dictionary and sEntiment Reasoner) sentiment analysis module later pushing each batch to MongoDB collection "BitCoinTweets".
* Last step is to find influence of Tweets on Bitcoin day to day prices. 

## Data Pipeline Architecture :

<br/>

![Data Pipeline Architecture](https://github.com/aayushidubey16/BitCoinTweetsIngestionAndSentimentAnalysis/blob/main/DataPipelineArchitecture.JPG?raw=true)


### Dataset:
* Source : [Kaggle.com](https://www.kaggle.com/datasets/kaushiksuresh147/bitcoin-tweets) <br/>
* Shape (size) : 3199999 records, 13 features (1.44 GB)<br/>

### Code : https://github.com/aayushidubey16/BitCoinTweetsIngestionAndSentimentAnalysis.git<br/>

### Project Structure :

```
project root folder
│   📜 ReadMe.md
│   📜 AboutMe.md
│   📜 Setup.py

└───📂 lib
    │   📜 mongo-java-driver-3.12.11.jar
    │   📜 mongo-spark-connector-10.0.1.jar

└───📂 outcome
    |   📜 DataPipelineArchitecture.JPG
    
└───📂 project
    └───📂 analysis
        |   📜 BitcoinTweetsAnalysis.ipynb
        |   📜 MyConfig.py
    └───📂 datasets : Its a placeholder to keep dataset files
            |   📜 BitCoin_tweets.csv
            |   📜 BTC-USD.csv
    └───📂 kafka_streaming
        └───📂 logs
            |   📜 application.log
        │   📜 BitCoinTweetDataIngestionStreaming.py
        │   📜 KafkaProducer.py
        |   📜 MyConfig.py
    

```
## VADER Sentiment Analysis :

    VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media. VADER uses a combination of A sentiment lexicon is a list of lexical features (e.g., words) which are generally labeled according to their semantic orientation as either positive or negative. VADER not only tells about the Positivity and Negativity score but also tells us about how positive or negative a sentiment is.

    The Compound score is a metric that calculates the sum of all the lexicon ratings which have been normalized between -1(most extreme negative) and +1 (most extreme positive).
    
* positive sentiment : (compound score >= 0.05) 
* neutral sentiment : (compound score > -0.05) and (compound score < 0.05) 
* negative sentiment : (compound score <= -0.05)

## Instructions to setup the Project:

1. To run the project we need Python 3.6>=, Spark 3.2.1 (PySpark 3.2.1) & Kafka
    * [Python Installation Guide](https://realpython.com/installing-python/)
    * [Spark Installation Guide](https://spark.apache.org/docs/latest/api/python/getting_started/install.html)
    * [Kafka Installation Guide](https://kafka.apache.org/quickstart) &  [Windows](https://www.geeksforgeeks.org/how-to-install-and-run-apache-kafka-on-windows/)

    Note : I am using mongodb to ingest all the raw records and for that need to keep two jar file in the jar folder in spark home directory:
    * `mongo-java-driver-3.12.11.jar`
    * `mongo-spark-connector-10.0.1.jar`
    
    I have kept this jars under lib folder in project.

2. Next step is to create a kafka-topic named "BitCoinTweets" for that first start [*zookeeper* and *kafka broker service*](https://kafka.apache.org/documentation/#quickstart_startserver).
    Command To create topic:

* linux/macOs : 
```
bin/kafka-topics.sh --create --topic BitCoinTweets --bootstrap-server localhost:9092
```
* windows : 
```
.\bin\windows\kafka-topics.bat --create --topic BitCoinTweets --bootstrap-server localhost:9092
```

To verify we can describe topic in kafka by command: 
```
bin/kafka-topics.sh --describe --topic BitCoinTweets --bootstrap-server localhost:9092
```

3. I have uploaded dataset CSV files in a zip on Google Drive to download it following is the link:<br/>
    https://drive.google.com/file/d/1tt-WSWd7VMS3eTJ3ZdY0oQddZj56EBgX/view?usp=sharing

    Need to keep this files at path `project\datasets`.

4. Third step is to run Setup.py to install all dependencies (change terminal or command-prompt directory to the project) and with this step project set-up is completed. <br/>
    command : `python .\project\Setup.py`<br/>
    MyConfi.py inside kafka_streaming also has a place to mention the dataset directory against variable "dataset_path"
    For BitcoinTweetsAnalysis.ipynb we need to mention absolute path of BTC-USD.csv path.

5. Now, First we will run spark-streaming job using spark-submit, with following command:<br/>
    ```
    spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.1.2,org.apache.kafka:kafka-clients:2.8.1 .\project\Kafka_Streaming\BitCoinTweetDataIngestionStreaming.py > .\project\Kafka_Streaming\logs\application.log
    ```

6. After starting streaming spark job we will start KafkaProducer.py to push records in topic "BitCoinTweets". <br/>
    command: `python .\project\Kafka_Streaming\KafkaProducer.py`

7. As ingestion finishes we can move to Analysis phase and open *".\Analysis\BitcoinTweetsAnalysis.ipynb"* in jupyter-notebook and run all the cells to visualize the graphs and data.

Notes : Please stop  `zookeeper, kafka-broker service` and `spark streaming job` after ingestion.

## Dependancies
* Python 3.6 or greater
* Spark 3.2.1
* Kafka

## Link To Video Guide To Set-Up Project :
- https://drive.google.com/file/d/1EhjnnjSXyBsumOA-HWJ7RDbJ4_7r0auq/view?usp=sharing


