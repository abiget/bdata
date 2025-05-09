from pyflink.table import EnvironmentSettings, TableEnvironment
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_kafka_source_table(t_env):
    """Create Kafka source table with proper time attribute"""
    try:
        t_env.execute_sql("""
            CREATE TABLE competitor_prices (
                `timestamp` BIGINT,                 
                product_id STRING,
                competitor_price DOUBLE,
                event_time AS TO_TIMESTAMP_LTZ(`timestamp`, 3),
                platform STRING,
                WATERMARK FOR event_time AS event_time - INTERVAL '5' SECONDS
            ) WITH (
                'connector' = 'kafka',
                'topic' = 'competitor_prices_topic',
                'properties.bootstrap.servers' = 'kafka-broker:29092',
                'properties.group.id' = 'price_analyzer_group',
                'scan.startup.mode' = 'earliest-offset',
                'format' = 'json'
            )
        """)
        logger.info("Kafka source table created successfully")
    except Exception as e:
        logger.error(f"Failed to create Kafka source table: {e}")
        raise

def create_simple_sink(t_env):
    """Create a sink table using Upsert Kafka."""
    try:
        t_env.execute_sql("""
            CREATE TABLE price_updates (
                product_id STRING,
                platform STRING,
                price DOUBLE,
                PRIMARY KEY (product_id, platform) NOT ENFORCED
            ) WITH (
                'connector' = 'upsert-kafka',
                'topic' = 'price_updates_topic',
                'properties.bootstrap.servers' = 'kafka-broker:29092',
                'key.format' = 'json',
                'value.format' = 'json'
            )
        """)
        logger.info("Simple sink table created successfully")
    except Exception as e:
        logger.error(f"Failed to create sink table: {e}")
        raise

def create_raw_sink(t_env):
    """Create raw data sink table with cleaned schema."""
    t_env.execute_sql("""
        CREATE TABLE price_raw (
            event_timestamp TIMESTAMP(3),
            product_code STRING,
            price DECIMAL(10,2),
            platform_name STRING,
            is_premium_price BOOLEAN,
            processed_at TIMESTAMP(3)
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/prices_db',
            'table-name' = 'price_raw',
            'username' = 'postgres',
            'password' = 'postgres'
        )
    """)

def create_aggregated_sink(t_env):
    """Create aggregated data sink table."""
    t_env.execute_sql("""
        CREATE TABLE price_aggregated (
            product_code STRING,
            platform_name STRING,
            avg_price DOUBLE,
            min_price DOUBLE,
            max_price DOUBLE,
            update_count BIGINT,
            price_range DOUBLE,
            premium_count BIGINT,
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            PRIMARY KEY (product_code, platform_name, window_start) NOT ENFORCED
        ) WITH (
            'connector' = 'jdbc',
            'url' = 'jdbc:postgresql://postgres:5432/prices_db',
            'table-name' = 'price_aggregated',
            'username' = 'postgres',
            'password' = 'postgres'
        )
    """)

def analyze_prices():
    try:
        env_settings = EnvironmentSettings.in_streaming_mode()
        t_env = TableEnvironment.create(env_settings)
        
        # Create tables
        create_kafka_source_table(t_env)
        create_raw_sink(t_env)
        create_aggregated_sink(t_env)
        
        # Clean and transform raw data
        cleaned_data = t_env.sql_query("""
            SELECT 
                -- Rename and cast timestamp
                CAST(`timestamp` AS TIMESTAMP(3)) AS event_timestamp,
                -- Convert product_id to uppercase
                UPPER(product_id) AS product_code,
                -- Clean and cast price
                CAST(ROUND(competitor_price, 2) AS DECIMAL(10,2)) AS price,
                -- Normalize platform names
                CASE 
                    WHEN LOWER(platform) LIKE '%amazon%' THEN 'AMAZON'
                    WHEN LOWER(platform) LIKE '%ebay%' THEN 'EBAY'
                    ELSE UPPER(TRIM(platform))
                END AS platform_name,
                -- Add derived columns
                CAST(competitor_price > 100 AS BOOLEAN) AS is_premium_price,
                processing_time AS processed_at
            FROM competitor_prices
            WHERE 
                -- Filter out invalid data
                competitor_price > 0 AND
                product_id IS NOT NULL AND
                platform IS NOT NULL
        """)
        
        # Store cleaned raw data
        cleaned_data.execute_insert('price_raw')
        
        # Aggregations with cleaned data
        aggregated_data = t_env.sql_query("""
            SELECT 
                product_code,
                platform_name,
                AVG(price) as avg_price,
                MIN(price) as min_price,
                MAX(price) as max_price,
                COUNT(*) as update_count,
                -- Add price range calculation
                MAX(price) - MIN(price) as price_range,
                -- Add premium product flag
                SUM(CASE WHEN is_premium_price THEN 1 ELSE 0 END) as premium_count,
                TUMBLE_START(event_timestamp, INTERVAL '1' HOUR) as window_start,
                TUMBLE_END(event_timestamp, INTERVAL '1' HOUR) as window_end
            FROM cleaned_data
            GROUP BY 
                product_code,
                platform_name,
                TUMBLE(event_timestamp, INTERVAL '1' HOUR)
        """)
        
        aggregated_data.execute_insert('price_aggregated')
        
    except Exception as e:
        logger.error(f"Failed to execute price analysis: {e}")
        raise

if __name__ == "__main__":
    analyze_prices()