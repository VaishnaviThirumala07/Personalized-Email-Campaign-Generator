"""
Pydantic request/response schemas for the REST API.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ── Request Models ─────────────────────────────────────────────────


class PurchaseHistory(BaseModel):
    """Customer's purchase history summary."""

    avg_order_value: float = Field(..., description="Average order value in USD")
    frequency: str = Field(
        ..., description="Purchase frequency: daily, weekly, monthly, yearly"
    )
    categories: list[str] = Field(
        default_factory=list, description="Product categories purchased"
    )


class CustomerProfile(BaseModel):
    """Input: customer profile for personalized email generation."""

    customer_id: str = Field(..., description="Unique customer identifier")
    name: str = Field(..., description="Customer's full name")
    age: int = Field(..., ge=13, le=120, description="Customer age")
    segment: str = Field(
        default="young_professional",
        description="Customer segment: young_professional, parent, retiree, student, executive",
    )
    interests: list[str] = Field(
        default_factory=list, description="List of customer interests"
    )
    purchase_history: PurchaseHistory = Field(
        ..., description="Summary of purchase behavior"
    )
    preferred_tone: str = Field(
        default="friendly",
        description="Preferred email tone: casual, formal, friendly",
    )
    engagement_score: float = Field(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Historical engagement score (0-1)",
    )


class CampaignRequest(BaseModel):
    """Input: request to run a full A/B optimization campaign for a segment."""

    segment: str = Field(
        ...,
        description="Target customer segment",
    )
    campaign_goal: str = Field(
        default="increase_engagement",
        description="Campaign objective",
    )
    num_iterations: int = Field(
        default=3,
        ge=1,
        le=10,
        description="Number of optimization iterations",
    )


# ── Response Models ────────────────────────────────────────────────


class EmailVariant(BaseModel):
    """A single generated email variant."""

    variant_id: str = Field(..., description="Variant identifier (A, B, etc.)")
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content")
    predicted_ctr: Optional[float] = Field(
        None, description="Predicted click-through rate"
    )
    predicted_open_rate: Optional[float] = Field(
        None, description="Predicted open rate"
    )


class EmailResponse(BaseModel):
    """Output: the best-performing personalized email."""

    customer_id: str
    segment: str
    winning_variant: EmailVariant
    all_variants: list[EmailVariant] = Field(
        default_factory=list,
        description="All generated variants for reference",
    )
    optimization_iterations: int = Field(
        default=1, description="Number of iterations run"
    )
    confidence: Optional[float] = Field(
        None, description="Bayesian confidence that winner is truly better"
    )


class CampaignResult(BaseModel):
    """Output: results of a full campaign optimization run."""

    segment: str
    total_iterations: int
    best_variant: EmailVariant
    segment_avg_ctr: float
    segment_avg_open_rate: float
    improvement_pct: float = Field(
        ..., description="Percentage CTR improvement over baseline"
    )


class VariantResult(BaseModel):
    """A generated variant result with style notes."""

    variant_id: str = Field(..., description="Variant identifier (A, B, etc.)")
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Email body content")
    style_notes: str = Field(default="", description="Style approach description")


class CampaignResponse(BaseModel):
    """Response from the campaign generation endpoint."""

    campaign_id: str = Field(..., description="Generated campaign ID")
    segment: str = Field(..., description="Target segment")
    generated_variants: list[VariantResult] = Field(
        default_factory=list, description="Generated email variants"
    )
    winning_variant_id: Optional[str] = Field(
        None, description="ID of the winning variant"
    )
    confidence_score: float = Field(
        default=0.0, description="Bayesian confidence score"
    )
    iterations_run: int = Field(default=0, description="Total iterations run")


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    version: str = "0.1.0"
    environment: str = "development"
