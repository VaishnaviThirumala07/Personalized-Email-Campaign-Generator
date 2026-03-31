"""
Update Prompt Node — Evolve prompts based on winning variants.
"""

from langgraph_pipeline.state import CampaignState, PromptSnapshot
import json
import os

def update_prompt_node(state: CampaignState) -> dict:
    """
    Update few-shot examples and system prompt based on the winning variant.
    """
    winner = state.get("winner")
    segment = state.get("segment", "young_professional")
    goal = state.get("campaign_goal", "increase_engagement")
    prompt_history = state.get("prompt_history", [])
    
    if winner and state.get("is_winner_determined", False):
        # 1. Update the few-shot JSON bank
        examples_path = "prompts/few_shot_examples.json"
        
        # Load existing
        try:
            with open(examples_path, "r", encoding="utf-8") as f:
                examples = json.load(f)
        except Exception:
            examples = {}
            
        if segment not in examples:
            examples[segment] = []
            
        # Append winner
        examples[segment].append({
            "customer_context": f"Goal: {goal}. Style Notes: {winner.get('style_notes', 'N/A')}",
            "subject": winner.get("subject"),
            "body": winner.get("body"),
            "variant_style": "Winner"
        })
        
        # Save back
        try:
            with open(examples_path, "w", encoding="utf-8") as f:
                json.dump(examples, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save few-shot examples: {e}")
            
        # 2. Evolve system guidance
        new_guidance = (
            f"The previous winning approach used: {winner.get('style_notes', 'N/A')}. "
            "Incorporate similar psychological triggers but keep it fresh."
        )
        
        prompt_history.append({
            "iteration": state.get("iteration", 0),
            "system_prompt": new_guidance,
            "few_shot_examples": examples[segment],
            "winning_variant_id": winner.get("variant_id")
        })

    return {
        "prompt_history": prompt_history,
    }
