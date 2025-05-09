import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import uuid
import os

# Settings
num_products = 500
num_users = 1000
num_competitors = 5
days = 30
start_date = datetime.now() - timedelta(days=days)

# Directories
output_dir = "data"
# 1. Product Catalog
product_ids = [f"P{str(i).zfill(5)}" for i in range(num_products)]
categories = ["Electronics", "Home", "Books", "Clothing", "Toys"]
product_catalog = pd.DataFrame({
    "product_id": product_ids,
    "product_name": [f"Product_{i}" for i in range(num_products)],
    "category": np.random.choice(categories, num_products),
    "base_price": np.round(np.random.uniform(10, 500, num_products), 2),
    "stock": np.random.randint(10, 1000, num_products)
})
product_catalog.to_csv(f"{output_dir}/product_catalog.csv", index=False)

# 2. Competitor Prices (hourly updates)
competitor_ids = [f"C{str(i).zfill(3)}" for i in range(num_competitors)]
platforms = ["Amazon", "eBay", "Walmart", "BestBuy", "Target"]

competitor_price_data = []
for day in range(days):
    for hour in range(24):
        timestamp = start_date + timedelta(days=day, hours=hour)
        for pid in random.sample(product_ids, k=300):  # only some products updated each hour
            for cid, platform in zip(competitor_ids, platforms):
                price_variation = np.random.normal(0, 10)
                base_price = product_catalog.loc[product_catalog["product_id"] == pid, "base_price"].values[0]
                price = max(1, round(base_price + price_variation, 2))
                competitor_price_data.append({
                    "timestamp": timestamp.isoformat(),
                    "product_id": pid,
                    "competitor_id": cid,
                    "platform": platform,
                    "competitor_price": price
                })
competitor_prices = pd.DataFrame(competitor_price_data)
competitor_prices.to_csv(f"{output_dir}/competitor_prices.csv", index=False)

# 3. User Behavior Logs
event_types = ["view", "add_to_cart", "purchase"]
devices = ["mobile", "desktop", "tablet"]
locations = ["US", "EU", "ASIA", "SA", "AFRICA"]

user_behavior_data = []
for day in range(days):
    for user_id in range(num_users):
        num_events = random.randint(2, 10)
        for _ in range(num_events):
            timestamp = start_date + timedelta(days=day, seconds=random.randint(0, 86400))
            product_id = random.choice(product_ids)
            event_type = np.random.choice(event_types, p=[0.7, 0.2, 0.1])
            user_behavior_data.append({
                "timestamp": timestamp.isoformat(),
                "user_id": f"U{str(user_id).zfill(5)}",
                "product_id": product_id,
                "event_type": event_type,
                "device": random.choice(devices),
                "location": random.choice(locations)
            })
user_logs = pd.DataFrame(user_behavior_data)
user_logs.to_csv(f"{output_dir}/user_behavior_logs.csv", index=False)

# Return file paths
output_dir
