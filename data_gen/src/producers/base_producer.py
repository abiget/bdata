from abc import ABC, abstractmethod
from confluent_kafka import Producer
from common.config.kafka import config
import logging
from typing import Tuple, Any
import time

class BaseProducer(ABC):
    def __init__(self, topic_name):
        self.topic = topic_name
        self.producer = Producer(config)
        self.logger = logging.getLogger(self.__class__.__name__)

    def delivery_report(self, err, msg):
        if err is not None:
            self.logger.error(f'Message delivery failed: {err}')
        else:
            self.logger.debug(f'Message delivered to {msg.topic()} [{msg.partition()}] with key {msg.key()}')

    @abstractmethod
    def generate_message(self) -> Tuple[str, Any]:
        """Generate a message to be sent to Kafka
        Returns:
            Tuple[str, Any]: (key, message) pair
        """
        pass

    def run(self):
        """Main producer loop"""
        try:
            while True:
                key, message = self.generate_message()
                self.producer.produce(
                    self.topic,
                    key=str(key).encode('utf-8'),
                    value=message.encode('utf-8'),
                    callback=self.delivery_report
                )
                self.producer.poll(0)
        except KeyboardInterrupt:
            self.logger.info("Shutting down producer")
        finally:
            self.producer.flush()
            time.sleep(1) # Give time for messages to be sent before exiting



            