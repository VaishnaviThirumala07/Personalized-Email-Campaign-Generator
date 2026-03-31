"""
Test: LangGraph state schema is well-formed.
"""

from langgraph_pipeline.state import CampaignState


def test_campaign_state_can_be_instantiated():
    """Verify CampaignState TypedDict can be created with expected fields."""
    state: CampaignState = {
        "customer_profile": {"name": "Test User", "age": 30},
        "segment": "young_professional",
        "campaign_goal": "increase_engagement",
        "variants": [],
        "simulation_results": [],
        "winner": None,
        "winner_confidence": 0.0,
        "is_winner_determined": False,
        "iteration": 0,
        "max_iterations": 5,
        "prompt_history": [],
        "error": None,
    }

    assert state["segment"] == "young_professional"
    assert state["iteration"] == 0
    assert state["is_winner_determined"] is False
    assert state["max_iterations"] == 5
