#!/usr/bin/env python
"""Extract events from kafka and write them to hdfs
"""

import json
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, from_json
from pyspark.sql.types import StructType, StructField, StringType

def purchase_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- item_purchased: string (nullable = true)
    |-- timestamp: string (nullable = true)
    |-- type: string (nullable = true)
    """
    return StructType([
        StructField("Accept",StringType(), True),
        StructField("Host",StringType(), True),
        StructField("User-Agent",StringType(), True),
        StructField("event_type",StringType(), True),
        StructField("item_purchased",StringType(), True),
        StructField("type",StringType(), True),
    ])


def guild_schema():
    """
    root
    |-- Accept: string (nullable = true)
    |-- Host: string (nullable = true)
    |-- User-Agent: string (nullable = true)
    |-- event_type: string (nullable = true)
    |-- guild_name: string (nullable = true)
    |-- timestamp: string (nullable = true)
    """

    return StructType([
        StructField("Accept",StringType(), True),
        StructField("Host",StringType(), True),
        StructField("User-Agent",StringType(), True),
        StructField("event_type",StringType(), True),
        StructField("guild_name",StringType(), True),
    ])


@udf('int')
def action(event_as_json):
    event = json.loads(event_as_json)
    if event['event_type'] == 'purchase':
        return 0
    elif event['event_type'] == 'create_guild':
        return 1 
    elif event['event_type'] == 'join_guild':
        return 2 
    return 9999

def main():
    """main
    """
    spark = SparkSession \
        .builder \
        .appName("ExtractEventsJob") \
        .getOrCreate()

    raw_events = spark \
        .readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "kafka:29092") \
        .option("subscribe", "events") \
        .load()

    # Purchase Events
    purchase_events = raw_events \
         .filter(action(raw_events.value.cast('string')) == 0) \
         .select(raw_events.value.cast('string').alias('raw_event0'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                purchase_schema()).alias('json')) \
         .select('timestamp', 'json.*')

    # Create Guild Events
    create_events = raw_events \
         .filter(action(raw_events.value.cast('string')) == 1) \
         .select(raw_events.value.cast('string').alias('raw_event1'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                guild_schema()).alias('json')) \
         .select('timestamp', 'json.*')

    # Join Guild Events
    join_events = raw_events \
         .filter(action(raw_events.value.cast('string')) == 2) \
         .select(raw_events.value.cast('string').alias('raw_event2'),
                raw_events.timestamp.cast('string'),
                from_json(raw_events.value.cast('string'),
                guild_schema()).alias('json')) \
         .select('timestamp', 'json.*')

    #Writing
    sink_purchases =  purchase_events\
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_purchases") \
        .option("path", "/tmp/purchases") \
        .trigger(processingTime="60 seconds") \
        .start()

    sink_create =  create_events\
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_create") \
        .option("path", "/tmp/create") \
        .trigger(processingTime="60 seconds") \
        .start()

    sink_join =  join_events\
        .writeStream \
        .format("parquet") \
        .option("checkpointLocation", "/tmp/checkpoints_for_join") \
        .option("path", "/tmp/join") \
        .trigger(processingTime="60 seconds") \
        .start()

    sink_purchases.awaitTermination()
    sink_create.awaitTermination()
    sink_join.awaitTermination()


if __name__ == "__main__":
    main()
