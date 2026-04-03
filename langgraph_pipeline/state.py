"""
LangGraph state definition for the campaign optimization pipeline.

The state flows through: segment → generate → simulate → evaluate → update
"""

from typing import TypedDict, Optional


class VariantData(TypedDict):
    """A single email variant with its metadata."""

    variant_id: str  # "A", "B", etc.
    subject: str  # Email subject line
    body: str  # Email body content
    style_notes: str  # Description of the style approach used


class SimulationResult(TypedDict):
    """Simulated A/B test results for a single variant."""

    variant_id: str
    open_rate: float  # Simulated open rate (0-1)
    ctr: float  # Simulated click-through rate (0-1)
    conversion_rate: float  # Simulated conversion rate (0-1)
    num_recipients: int  # Number of simulated recipients
    num_opens: int  # Simulated opens
    num_clicks: int  # Simulated clicks


class PromptSnapshot(TypedDict):
    """Snapshot of prompt state at a given iteration."""

    iteration: int
    system_prompt: str
    few_shot_examples: list[dict]
    winning_variant_id: Optional[str]


class CampaignState(TypedDict):
    """
    Central state for the LangGraph campaign optimization pipeline.

    This state is passed between all nodes and accumulates data
    as the pipeline progresses through iterations.
    """

    # ── Input ──────────────────────────────────────────────────────
    customer_profile: dict  # Full customer profile (from API)
    segment: str  # Resolved customer segment
    campaign_goal: str  # E.g., "increase_engagement"

    # ── Generation ─────────────────────────────────────────────────
    variants: list[VariantData]  # Generated email variants (A & B)

    # ── Simulation ─────────────────────────────────────────────────
    simulation_results: list[SimulationResult]  # Per-variant sim results

    # ── Evaluation ─────────────────────────────────────────────────
    winner: Optional[VariantData]  # The winning variant (if determined)
    winner_confidence: float  # Bayesian confidence (0-1)
    is_winner_determined: bool  # Whether a clear winner was found

    # ── Iteration Tracking ─────────────────────────────────────────
    iteration: int  # Current iteration number
    max_iterations: int  # Maximum allowed iterations
    prompt_history: list[PromptSnapshot]  # Evolution of prompts over time

    # ── Error Handling ─────────────────────────────────────────────
    error: Optional[str]  # Error message if something fails
