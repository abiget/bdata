FROM python:3.10-slim

# Set the working directory
WORKDIR /data_gen

# First create the src directory
RUN mkdir -p /data_gen/src

# Copy the requirements file into the container
COPY requirements/producer.txt ./src/requirements.txt

# Install system dependencies and Python packages
RUN apt-get update && \
    apt-get install -y \
        librdkafka-dev \
        gcc \
        python3-dev && \
    pip3 install --no-cache-dir -r src/requirements.txt && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY src/producers ./src/producers
COPY src/common ./src/common
COPY data ./data

# Set python path
ENV PYTHONPATH=/data_gen/src

# Make python scripts executable
RUN chmod +x ./src/producers/*.py
