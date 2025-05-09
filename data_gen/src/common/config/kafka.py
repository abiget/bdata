# Kafka producer configuration
# When running in Docker, use the internal network address
# When running locally, use localhost
import os

# Get bootstrap servers from environment variable or use default
bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'broker:29092')

config = {
    'bootstrap.servers': bootstrap_servers,  # Will use environment variable if set
    'security.protocol': 'PLAINTEXT'        # Using plaintext for local development
}

# Schema Registry configuration (commented out for local development)
# Uncomment and configure if using Schema Registry
sr_config = {
    'url': os.getenv('SCHEMA_REGISTRY_URL', 'http://localhost:8081'),
    'basic.auth.user.info': os.getenv('SCHEMA_REGISTRY_AUTH', '')
}