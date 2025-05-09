# Start the services
bash run.sh start

# View logs
bash run.sh logs

# Stop services
bash run.sh stop

# Rebuild and start
bash run.sh build && bash run.sh start


## Possible data sources
- https://www.kaggle.com/datasets/karkavelrajaj/amazon-sales-dataset

- https://www.kaggle.com/datasets/saibattula/retail-price-dataset-sales-data

- https://www.kaggle.com/datasets/lokeshparab/amazon-products-dataset/data

<!-- create topic -->
docker exec kafka-broker /opt/kafka/bin/kafka-topics.sh \
    --create \
    --topic price_updates_topic \
    --bootstrap-server localhost:9092 \
    --partitions 1 \
    --replication-factor 1
    
<!-- list topics -->
docker exec kafka-broker /opt/kafka/bin/kafka-topics.sh --list --bootstrap-server localhost:9092

<!-- Monitor the output topic -->
docker exec kafka-broker opt/kafka/bin/kafka-console-consumer.sh \
    --bootstrap-server localhost:9092 \
    --topic price_updates_topic \
    --from-beginning