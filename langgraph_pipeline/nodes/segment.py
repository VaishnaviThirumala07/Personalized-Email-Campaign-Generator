"""
Segment Node — Classify and validate customer segments.
"""

from langgraph_pipeline.state import CampaignState

VALID_SEGMENTS = {"young_professional", "parent", "retiree", "student", "executive"}

def segment_node(state: CampaignState) -> dict:
    """
    Classify/validate the customer into a segment based on their profile.

    Takes the raw customer profile and resolves it into one of the
    predefined segments. Defaults to 'young_professional' if invalid.
    """
    profile = state.get("customer_profile", {})
    
    raw_segment = profile.get("segment", "").lower()
    segment = raw_segment if raw_segment in VALID_SEGMENTS else "young_professional"
    
    # Also extract the campaign goal from the state, defaulting if missing
    goal = state.get("campaign_goal", "increase_engagement")

    return {
        "segment": segment,
        "campaign_goal": goal,
        "iteration": state.get("iteration", 0),
        "max_iterations": state.get("max_iterations", 5),
        "is_winner_determined": False
    }
