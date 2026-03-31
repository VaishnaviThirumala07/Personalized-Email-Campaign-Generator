"""
MLflow utilities for the Email Campaign Generator.
"""
import mlflow
from app.core.config import settings

def init_mlflow():
    """Initialize MLflow connection and experiment."""
    if not settings.mlflow_tracking_uri:
        return
        
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    try:
        mlflow.set_experiment(settings.mlflow_experiment_name)
    except Exception as e:
        print(f"Warning: Could not set MLflow experiment: {e}")

def get_active_run_id():
    """Get the current MLflow run ID."""
    active_run = mlflow.active_run()
    return active_run.info.run_id if active_run else None

def log_campaign_start(customer_profile: dict, segment: str):
    """Start an MLflow run and log base customer info."""
    init_mlflow()
    mlflow.start_run(run_name=f"Campaign_{segment}")
    
    # Log tags to easily filter runs
    mlflow.set_tag("segment", segment)
    mlflow.set_tag("customer_age", str(customer_profile.get("age", "")))
    mlflow.set_tag("customer_tone", customer_profile.get("preferred_tone", ""))
    
    # Log simulation parameters
    mlflow.log_param("confidence_threshold", settings.ab_test_confidence_threshold)
    mlflow.log_param("max_iterations", settings.ab_test_max_iterations)

def log_generation_iteration(iteration: int, variants: list):
    """Log the generated variants for an iteration."""
    if not mlflow.active_run():
        return
        
    for v in variants:
        vid = v.get("variant_id", "X")
        # Log variant text as dict
        mlflow.log_dict(v, f"variants/iter_{iteration}/variant_{vid}.json")

def log_simulation_results(iteration: int, results: list):
    """Log CTR and Open Rate simulation performance metrics."""
    if not mlflow.active_run():
        return
        
    for r in results:
        vid = r.get("variant_id", "X")
        # MLflow metrics per iteration
        mlflow.log_metric(f"ctr_{vid}", r.get("ctr", 0), step=iteration)
        mlflow.log_metric(f"open_rate_{vid}", r.get("open_rate", 0), step=iteration)
        mlflow.log_metric(f"conversion_{vid}", r.get("conversion_rate", 0), step=iteration)

def log_evaluation_results(iteration: int, winner, confidence: float):
    """Log the Bayesian A/B test winner."""
    if not mlflow.active_run():
        return
        
    mlflow.log_metric("winner_confidence", confidence, step=iteration)
    if winner:
        mlflow.log_text(winner.get('variant_id', ''), f"winners/iter_{iteration}_winner_id.txt")
        mlflow.log_dict(winner, f"winners/iter_{iteration}_winner.json")

def log_campaign_end(total_iterations: int, is_winner_determined: bool):
    """Log end-of-campaign stats and close the MLflow run."""
    if not mlflow.active_run():
        return
        
    mlflow.log_metric("total_iterations", total_iterations)
    mlflow.set_tag("winner_determined", str(is_winner_determined))
    mlflow.end_run()
