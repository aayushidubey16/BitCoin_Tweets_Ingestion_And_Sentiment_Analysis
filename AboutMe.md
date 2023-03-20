# BitCoin Tweets Ingestion And Sentiment Analysis

## Team Members : 
- Aayushi Dubey(825874459) 
- Pallavi Prasanna Kumar(826230204)

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