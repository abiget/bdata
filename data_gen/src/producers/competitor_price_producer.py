import os
import json
import uuid
import pandas as pd
from typing import Tuple, Any
from base_producer import BaseProducer
from common.utils.json_serializer import json_serializer
from common.utils.kafka_utils import create_topic_if_not_exists

class CompetitorPriceProducer(BaseProducer):
    def __init__(self, topic_name: str, csv_file: str):
        super().__init__(topic_name)
        self.data = self._load_data(csv_file)
        self.current_index = 0
        self.logger.info(f"Producer for topic {topic_name} initialized")

    def _load_data(self, csv_file: str) -> pd.DataFrame:
        """Load data from CSV file"""
        try:
            data = pd.read_csv(csv_file)
            # Convert timestamp to UNIX timestamp
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            data['timestamp'] = data['timestamp'].astype(int) // 10**9  # Convert to UNIX timestamp
            data['product_id'] = data['product_id'].astype(str)
            data['competitor_id'] = data['competitor_id'].astype(str)
            data['platform'] = data['platform'].astype(str)
            data['competitor_price'] = data['competitor_price'].astype(float)
            return data
        except Exception as e:
            self.logger.error(f"Error loading data: {e}")
            raise

    def generate_message(self) -> Tuple[str, Any]:
        """Generate a message to be sent to Kafka"""
        if self.current_index >= len(self.data):
            self.current_index = 0 # Reset to beginning of dataset
            
        if not self.data.empty:            
            row = self.data.iloc[self.current_index]
            self.logger.info(f"Generating message for row {self.current_index}: {row.to_dict()}")
            
            # Create a unique message ID
            message_id = "CP-" + str(uuid.uuid4())
            
            # Create the message
            message_dict = {
                'timestamp': row['timestamp'],
                'product_id': row['product_id'],
                'competitor_id': row['competitor_id'],
                'platform': row['platform'],
                'competitor_price': row['competitor_price']
            }

            # increment the index for the next message 
            self.current_index += 1
            
            return message_id, json.dumps(message_dict, default=json_serializer)
        else:
            self.logger.warning("No more data to send")
            return None, None
        
if __name__ == "__main__":
    # Create the topic if it doesn't exist
    topic_name = create_topic_if_not_exists("competitor_prices_topic")

    # Path to the CSV file
    csv_file = os.path.join(os.getcwd(), "data/competitor_prices.csv")

    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"CSV file not found: {csv_file}")
    
    # Initialize the producer
    producer = CompetitorPriceProducer(topic_name, csv_file)
    producer.run()