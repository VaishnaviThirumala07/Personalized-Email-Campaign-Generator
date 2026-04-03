from app.core.config import settings
from langgraph_pipeline.graph import build_campaign_graph

def run():
    print(f"Building LangGraph pipeline using model {settings.llm_model} ...")
    graph = build_campaign_graph()
    
    # Mock a customer profile from one of the synthetic ones
    mock_profile = {
        "customer_id": "12345",
        "name": "Alex Mercer",
        "age": 28,
        "segment": "young_professional",
        "interests": ["technology", "fitness"],
        "purchase_history": {"avg_order_value": 150, "frequency": "monthly"},
        "preferred_tone": "casual",
        "engagement_score": 0.85
    }
    
    initial_state = {
        "customer_profile": mock_profile,
        "segment": "young_professional",
        "campaign_goal": "Sell smart fitness watch",
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
    
    print("Running pipeline...")
    for output in graph.stream(initial_state, {"recursion_limit": 20}):
        for node_name, state in output.items():
            print(f"--- Node Executed: {node_name} ---")
            if "variants" in state and node_name == "generate_variants":
                print(f"Generated {len(state['variants'])} variants.")
                for v in state['variants']:
                    print(f"[{v.get('variant_id')}] Subj: {v.get('subject')}")
            
            if "simulation_results" in state and node_name == "simulate":
                for res in state['simulation_results']:
                    print(f"Variant {res.get('variant_id')} CTR: {res.get('ctr')*100:.2f}% (Opens: {res.get('open_rate')*100:.2f}%)")
                    
            if node_name == "evaluate":
                if state.get("is_winner_determined"):
                    print(f"WINNER DECIDED! Variant {state['winner']['variant_id']} won with {state['winner_confidence']*100:.2f}% confidence.")
                else:
                    print("No clear winner yet.")

if __name__ == "__main__":
    run()
