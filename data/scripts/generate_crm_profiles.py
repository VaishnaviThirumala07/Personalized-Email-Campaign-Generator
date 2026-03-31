"""
Generate Synthetic CRM Customer Profiles.

Creates realistic (fake) customer data to simulate an email marketing CRM.
Includes segments, purchase history, and demographics.
"""

import pandas as pd
import os
import random
import uuid
from faker import Faker
import json

fake = Faker()

# Ensure output directory exists
os.makedirs("data/processed", exist_ok=True)

SEGMENTS = ["young_professional", "parent", "retiree", "student", "executive"]
INTERESTS_POOL = [
    "technology", "fitness", "cooking", "travel", "investing", 
    "gaming", "fashion", "reading", "home decor", "automobiles"
]
FREQUENCIES = ["daily", "weekly", "monthly", "yearly", "rarely"]
TONES = ["casual", "formal", "friendly"]

def generate_purchase_history():
    return json.dumps({
        "avg_order_value": round(random.uniform(15.0, 500.0), 2),
        "frequency": random.choice(FREQUENCIES),
        "categories": random.sample(INTERESTS_POOL, k=random.randint(1, 3))
    })

def generate_profiles(num_profiles=500):
    data = []
    for _ in range(num_profiles):
        segment = random.choice(SEGMENTS)
        
        # Age correlated loosely with segment
        if segment == "student":
            age = random.randint(18, 24)
        elif segment == "young_professional":
            age = random.randint(23, 35)
        elif segment == "parent":
            age = random.randint(28, 55)
        elif segment == "executive":
            age = random.randint(35, 65)
        elif segment == "retiree":
            age = random.randint(60, 90)
            
        data.append({
            "customer_id": str(uuid.uuid4()),
            "name": fake.name(),
            "age": age,
            "segment": segment,
            "interests": json.dumps(random.sample(INTERESTS_POOL, k=random.randint(2, 4))),
            "purchase_history": generate_purchase_history(),
            "preferred_tone": random.choice(TONES),
            "engagement_score": round(random.uniform(0.1, 0.95), 2)
        })
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Generating synthetic CRM profiles...")
    df = generate_profiles(500)
    output_path = "data/processed/crm_profiles.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} customer profiles to {output_path}")
