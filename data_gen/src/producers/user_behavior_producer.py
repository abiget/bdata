import os
import json
import uuid
import pandas as pd
from typing import Tuple, Any
from base_producer import BaseProducer
from common.utils.json_serializer import json_serializer
from common.utils.kafka_utils import create_topic_if_not_exists

class UserBehaviorProducer(BaseProducer):
    def __init__(self, topic_name: str, csv_file: str):
        super().__init__(topic_name)
        self.data = self._load_data(csv_file)
        self.current_index = 0
        self.logger.info(f"Producer for topic {topic_name} initialized")

    def _load_data(self, csv_file: str):
        """Load data from CSV file"""
        try:
            # timestamp,user_id,product_id,event_type,device,location

            data = pd.read_csv(csv_file)
            # Convert timestamp to UNIX timestamp
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            data['timestamp'] = data['timestamp'].astype(int) // 10**9  # Convert to UNIX timestamp
            data['user_id'] = data['user_id'].astype(str)
            data['product_id'] = data['product_id'].astype(str)
            data['event_type'] = data['event_type'].astype(str)
            data['device'] = data['device'].astype(str)
            data['location'] = data['location'].astype(str)
            return data
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise
    def generate_message(self) -> Tuple[str, Any]:
        """Generate a message to be sent to Kafka"""
        if self.current_index >= len(self.data):
            self.current_index = 0 # Reset to beginning of dataset

        if self.current_index < len(self.data):
            row = self.data.iloc[self.current_index]

            # Create a unique message ID
            message_id = "UB-" + str(uuid.uuid4())

            # Create the message
            message_dict = {
                'timestamp': row['timestamp'],
                'user_id': row['user_id'],
                'product_id': row['product_id'],
                'event_type': row['event_type'],
                'device': row['device'],
                'location': row['location']
            }

            # increment the index for the next message
            self.current_index += 1

            return message_id, json.dumps(message_dict, default=json_serializer)
        else:
            self.logger.warning("No more data to send")
            return None, None

if __name__ == "__main__":
    # Create the topic if it doesn't exist
    topic_name = create_topic_if_not_exists("user_behavior_topic")

    # Path to the CSV file
    csv_file = os.path.join(os.getcwd(), "data/user_behavior_logs.csv")

    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")
        
    # Initialize the producer
    producer = UserBehaviorProducer(topic_name, csv_file)
    producer.run()
