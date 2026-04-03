"""
Evaluate Node — Bayesian A/B testing to determine the winning variant.
"""

from langgraph_pipeline.state import CampaignState, VariantData
from app.core.config import settings
import numpy as np
from scipy.stats import beta


def evaluate_node(state: CampaignState) -> dict:
    """
    Perform Bayesian A/B testing on the simulation results.
    """
    results = state.get("simulation_results", [])
    variants = state.get("variants", [])

    if len(results) < 2:
        return {"is_winner_determined": False}

    # Extract Variant A and B data (assuming 2 variants for simplicity)
    res_A = results[0]
    res_B = results[1]

    # Prior: Beta(1, 1) — Uniform prior
    alpha_prior = 1
    beta_prior = 1

    # Posterior for A
    alpha_A = alpha_prior + res_A["num_clicks"]
    beta_A = beta_prior + (res_A["num_recipients"] - res_A["num_clicks"])

    # Posterior for B
    alpha_B = alpha_prior + res_B["num_clicks"]
    beta_B = beta_prior + (res_B["num_recipients"] - res_B["num_clicks"])

    # Monte Carlo simulation to compute P(p_A > p_B)
    samples = 100000
    samples_A = beta.rvs(alpha_A, beta_A, size=samples)
    samples_B = beta.rvs(alpha_B, beta_B, size=samples)

    prob_A_beats_B = np.mean(samples_A > samples_B)
    prob_B_beats_A = 1.0 - prob_A_beats_B

    threshold = settings.ab_test_confidence_threshold

    winner: VariantData | None = None
    winner_confidence = 0.0
    is_winner_determined = False

    if prob_A_beats_B > threshold:
        winner = variants[0]
        winner_confidence = prob_A_beats_B
        is_winner_determined = True
    elif prob_B_beats_A > threshold:
        winner = variants[1]
        winner_confidence = prob_B_beats_A
        is_winner_determined = True

    from app.core.mlflow_utils import log_evaluation_results

    log_evaluation_results(state.get("iteration", 0), winner, float(winner_confidence))

    return {
        "winner": winner,
        "winner_confidence": float(winner_confidence),
        "is_winner_determined": is_winner_determined,
    }
