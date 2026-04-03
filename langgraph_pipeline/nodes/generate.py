"""
Generate Variants Node — LLM-powered email variant generation.
"""

from langgraph_pipeline.state import CampaignState, VariantData
from app.core.config import settings
from prompts.base_email import get_campaign_prompt_template
import json


def get_llm():
    """Initialize the LLM based on settings."""
    if settings.llm_provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            api_key=settings.openai_api_key,
        )
    elif settings.llm_provider == "anthropic":
        from langchain_anthropic import ChatAnthropic

        return ChatAnthropic(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            api_key=settings.anthropic_api_key,
        )
    elif settings.llm_provider == "google":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            google_api_key=settings.google_api_key,
        )


def generate_variants_node(state: CampaignState) -> dict:
    """
    Generate 2+ email variants using the LLM with persona-conditioned prompts.
    """
    profile = state.get("customer_profile", {})
    segment = state.get("segment", "young_professional")
    goal = state.get("campaign_goal", "increase_engagement")
    prompt_history = state.get("prompt_history", [])

    # Get latest system guidance if any
    system_guidance = ""
    if prompt_history:
        system_guidance = prompt_history[-1].get("system_prompt", "")

    prompt = get_campaign_prompt_template(segment, system_guidance)
    llm = get_llm()

    chain = prompt | llm

    # We pass the unpacked profile minus some fields if needed, or explicitly extract
    response = chain.invoke(
        {
            "name": profile.get("name", "Customer"),
            "age": profile.get("age", ""),
            "interests": profile.get("interests", "general products"),
            "purchase_history": profile.get("purchase_history", "None yet"),
            "preferred_tone": profile.get("preferred_tone", "friendly"),
            "campaign_goal": goal,
        }
    )

    # Parse JSON from LLM output
    content = response.content
    # Clean possible markdown formatting
    if "```json" in content:
        content = content.split("```json")[1].split("```")[0]
    elif "```" in content:
        content = content.split("```")[1].split("```")[0]

    try:
        parsed_variants = json.loads(content.strip())
        variants_list = parsed_variants.get("variants", [])

        # Ensure they conform to VariantData schema
        variants: list[VariantData] = []
        for v in variants_list:
            variants.append(
                {
                    "variant_id": v.get("variant_id", "Unknown"),
                    "subject": v.get("subject", ""),
                    "body": v.get("body", ""),
                    "style_notes": v.get("style_notes", ""),
                }
            )
    except Exception as e:
        # Fallback if LLM fails JSON format
        variants = [
            {
                "variant_id": "A",
                "subject": "Error",
                "body": f"Failed to parse generation: {str(e)}",
                "style_notes": "Error",
            }
        ]

    # Increment iteration
    current_iter = state.get("iteration", 0) + 1

    from app.core.mlflow_utils import log_generation_iteration

    log_generation_iteration(current_iter, variants)

    return {
        "variants": variants,
        "iteration": current_iter,
    }
