from confluent_kafka.admin import AdminClient, NewTopic
from common.config.kafka import config
import logging
import time

def create_topic_if_not_exists(topic_name, num_partitions=3, replication_factor=1):
    """Create Kafka topic if it doesn't exist"""
    admin = AdminClient(config)
    
    cluster = admin.list_topics()
    if topic_name not in cluster.topics:
        logging.info(f"Topic {topic_name} does not exist. Creating...")
        new_topic = admin.create_topics([
            NewTopic(
                topic_name,
                num_partitions=num_partitions,
                replication_factor=replication_factor
            )
        ])
        time.sleep(2)  # Wait for topic creation
        logging.info(f"Topic {topic_name} created with {num_partitions} partitions")
        return topic_name
    else:
        logging.info(f"Topic {topic_name} already exists")
        return topic_name