"""
LangGraph campaign optimization graph.

Flow: segment → generate_variants → simulate → evaluate → [conditional]
  ├── winner found → update_prompt → END
  └── no winner   → generate_variants (loop back, max N iterations)

This file assembles the full graph from individual node functions.
Actual node implementations are in langgraph_pipeline/nodes/.
"""

from langgraph.graph import StateGraph, END
from langgraph_pipeline.state import CampaignState


def should_continue(state: CampaignState) -> str:
    """
    Conditional edge: decide whether to continue iterating or finish.

    Returns:
        "update_prompt" if a winner is found or max iterations reached
        "generate_variants" to loop back and try again
    """
    if state.get("is_winner_determined", False):
        return "update_prompt"

    if state.get("iteration", 0) >= state.get("max_iterations", 5):
        # Max iterations reached — pick best available and move on
        return "update_prompt"

    # No winner yet and iterations remain — loop back
    return "generate_variants"


def build_campaign_graph() -> StateGraph:
    """
    Construct and compile the LangGraph campaign optimization graph.

    Returns:
        Compiled StateGraph ready for invocation.
    """
    # Import node functions (will be implemented in Phase 4)
    from langgraph_pipeline.nodes.segment import segment_node
    from langgraph_pipeline.nodes.generate import generate_variants_node
    from langgraph_pipeline.nodes.simulate import simulate_node
    from langgraph_pipeline.nodes.evaluate import evaluate_node
    from langgraph_pipeline.nodes.update_prompt import update_prompt_node

    # ── Build Graph ────────────────────────────────────────────────
    graph = StateGraph(CampaignState)

    # Add nodes
    graph.add_node("segment", segment_node)
    graph.add_node("generate_variants", generate_variants_node)
    graph.add_node("simulate", simulate_node)
    graph.add_node("evaluate", evaluate_node)
    graph.add_node("update_prompt", update_prompt_node)

    # Set entry point
    graph.set_entry_point("segment")

    # Add edges (linear flow)
    graph.add_edge("segment", "generate_variants")
    graph.add_edge("generate_variants", "simulate")
    graph.add_edge("simulate", "evaluate")

    # Conditional edge after evaluation
    graph.add_conditional_edges(
        "evaluate",
        should_continue,
        {
            "update_prompt": "update_prompt",
            "generate_variants": "generate_variants",
        },
    )

    # Terminal edge
    graph.add_edge("update_prompt", END)

    return graph.compile()
