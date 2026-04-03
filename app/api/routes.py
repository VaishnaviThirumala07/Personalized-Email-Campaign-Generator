from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from langgraph_pipeline.graph import build_campaign_graph
from app.core.mlflow_utils import log_campaign_start, log_campaign_end
from app.models.schemas import CustomerProfile, CampaignResponse, VariantResult

router = APIRouter()

class CampaignRequest(BaseModel):
    customer_profile: CustomerProfile
    campaign_goal: str

@router.post("/generate_campaign", response_model=CampaignResponse)
def generate_campaign(request: CampaignRequest, background_tasks: BackgroundTasks):
    """
    Trigger the LangGraph workflow to optimize an email campaign using A/B testing logic.
    """
    profile_dict = request.customer_profile.dict()
    segment = request.customer_profile.segment or "young_professional"
    
    # 1. Start MLFlow Tracking
    log_campaign_start(profile_dict, segment)
    
    # 2. Setup LangGraph Pipeline State
    graph = build_campaign_graph()
    initial_state = {
        "customer_profile": profile_dict,
        "segment": segment,
        "campaign_goal": request.campaign_goal,
        "variants": [],
        "simulation_results": [],
        "winner": None,
        "winner_confidence": 0.0,
        "is_winner_determined": False,
        "iteration": 0,
        "max_iterations": 3,
        "prompt_history": [],
        "error": None
    }
    
    # 3. Stream pipeline synchronously (we can make it asynchronous fully later)
    # Using `.invoke()` directly processes the entire graph until end.
    try:
        final_state = graph.invoke(initial_state, {"recursion_limit": 20})
        
        # 4. End MLFlow Tracking
        log_campaign_end(
            total_iterations=final_state.get("iteration", 0),
            is_winner_determined=final_state.get("is_winner_determined", False)
        )
        
        # Map back to our Pydantic response format
        variants_res = []
        for v in final_state.get("variants", []):
            variants_res.append(VariantResult(
                variant_id=v.get("variant_id"),
                subject=v.get("subject"),
                body=v.get("body"),
                style_notes=v.get("style_notes", "")
            ))
            
        winner_id = final_state.get("winner", {}).get("variant_id") if final_state.get("winner") else None
        
        return CampaignResponse(
            campaign_id=f"camp_{segment}_{final_state.get('iteration', 0)}",
            segment=final_state.get("segment", segment),
            generated_variants=variants_res,
            winning_variant_id=winner_id,
            confidence_score=final_state.get("winner_confidence", 0.0),
            iterations_run=final_state.get("iteration", 0)
        )
        
    except Exception as e:
        # Failsafe execution wrapper
        log_campaign_end(0, False)
        raise HTTPException(status_code=500, detail=str(e))
