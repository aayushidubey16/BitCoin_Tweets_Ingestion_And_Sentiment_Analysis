## Dependancies
* Python 3.6 or greater
* Spark 3.2.1
* Kafka

## Link To Video Guide To Set-Up Project :
- https://drive.google.com/file/d/1EhjnnjSXyBsumOA-HWJ7RDbJ4_7r0auq/view?usp=sharing

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


