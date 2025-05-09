FROM flink:1.17.0-scala_2.12-java11

RUN wget -P /opt/flink/lib/ https://jdbc.postgresql.org/download/postgresql-42.7.3.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-connector-kafka/1.17.0/flink-connector-kafka-1.17.0.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-sql-avro-confluent-registry/1.17.0/flink-sql-avro-confluent-registry-1.17.0.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/kafka/kafka-clients/3.2.3/kafka-clients-3.2.3.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-json/1.17.0/flink-json-1.17.0.jar; \
    wget -P /opt/flink/lib/ https://repo.maven.apache.org/maven2/org/apache/flink/flink-csv/1.17.0/flink-csv-1.17.0.jar; \
    wget -P /opt/flink/lib/ https://github.com/knaufk/flink-faker/releases/download/v0.5.2/flink-faker-0.5.2.jar;

RUN chown -R flink:flink /opt/flink/lib

ENV APP_HOME=processing


RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-dev build-essential curl unzip && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY src/ ./src/
ENV PYTHONPATH=${APP_HOME}/src

# CMD ["python3", "-u", "src/price_analyzer.py"]