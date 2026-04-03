"""
Simulate Node — Simulate A/B test with synthetic email metrics.
"""

from langgraph_pipeline.state import CampaignState, SimulationResult
from app.core.config import settings
import pandas as pd
import numpy as np

def simulate_node(state: CampaignState) -> dict:
    """
    Simulate open rates and CTR for each variant using synthetic benchmarks.
    """
    segment = state.get("segment", "young_professional")
    variants = state.get("variants", [])
    
    # Load benchmarks
    try:
        df = pd.read_csv("data/processed/benchmarks.csv")
        benchmark = df[df['segment'] == segment].iloc[0]
        base_open_rate = float(benchmark['base_open_rate'])
        base_ctr = float(benchmark['base_ctr'])
    except Exception:
        # Fallback if file missing or segment not found
        base_open_rate = 0.30
        base_ctr = 0.05

    n_recipients = settings.ab_test_simulated_recipients
    simulation_results: list[SimulationResult] = []

    for idx, v in enumerate(variants):
        # We simulate that Variant A and B perform differently.
        # Add random noise to the mean (shift the base rate per variant)
        # We artificially make one slightly better, or just pure noise
        variant_ctr_mu = np.clip(np.random.normal(base_ctr, 0.015), 0.01, 0.99)
        variant_open_mu = np.clip(np.random.normal(base_open_rate, 0.05), 0.05, 0.99)
        
        # We simulate the exact number of opens and clicks
        num_opens = np.random.binomial(n_recipients, variant_open_mu)
        # Clicks are conditional on opens, but here we model as % of total recipients
        num_clicks = np.random.binomial(n_recipients, variant_ctr_mu)
        
        # Calculate real observed rates
        obs_open_rate = num_opens / n_recipients
        obs_ctr = num_clicks / n_recipients
        # Conversion typically a % of clicks
        conversion_rate = np.random.uniform(0.01, 0.15) * obs_ctr

        simulation_results.append({
            "variant_id": v.get("variant_id", f"Var_{idx}"),
            "open_rate": float(obs_open_rate),
            "ctr": float(obs_ctr),
            "conversion_rate": float(conversion_rate),
            "num_recipients": n_recipients,
            "num_opens": int(num_opens),
            "num_clicks": int(num_clicks),
        })

    from app.core.mlflow_utils import log_simulation_results
    log_simulation_results(state.get("iteration", 0), simulation_results)

    return {
        "simulation_results": simulation_results,
    }
