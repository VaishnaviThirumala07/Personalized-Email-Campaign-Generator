"""
Generate Synthetic Email Marketing Benchmarks.

Provides baseline open rates and CTR metrics per segment to represent
historical campaign performance data for the A/B testing simulator.
"""

import pandas as pd
import os

# Ensure output directory exists
os.makedirs("data/processed", exist_ok=True)


def generate_benchmarks():
    data = [
        {
            "segment": "young_professional",
            "base_open_rate": 0.35,
            "base_ctr": 0.08,
            "best_performing_style": "casual, concise, FOMO-driven",
            "avoid_style": "too formal, lengthy walls of text",
        },
        {
            "segment": "parent",
            "base_open_rate": 0.28,
            "base_ctr": 0.05,
            "best_performing_style": "friendly, benefit-focused, empathetic",
            "avoid_style": "overly aggressive urgency",
        },
        {
            "segment": "retiree",
            "base_open_rate": 0.42,
            "base_ctr": 0.10,
            "best_performing_style": "formal, detailed, trustworthy",
            "avoid_style": "slang, confusing tech jargon",
        },
        {
            "segment": "student",
            "base_open_rate": 0.22,
            "base_ctr": 0.04,
            "best_performing_style": "highly casual, meme-friendly, highly urgent",
            "avoid_style": "corporate speak",
        },
        {
            "segment": "executive",
            "base_open_rate": 0.38,
            "base_ctr": 0.07,
            "best_performing_style": "professional, highly concise, ROI-focused",
            "avoid_style": "fluff, friendly chit-chat",
        },
    ]
    return pd.DataFrame(data)


if __name__ == "__main__":
    print("Generating segment benchmarks...")
    df = generate_benchmarks()
    output_path = "data/processed/benchmarks.csv"
    df.to_csv(output_path, index=False)
    print(f"Saved {len(df)} segment benchmark metrics to {output_path}")
