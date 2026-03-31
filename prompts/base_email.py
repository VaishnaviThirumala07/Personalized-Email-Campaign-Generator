"""
LangChain templates for dynamic, persona-conditioned email generation.
Uses FewShotPromptTemplate to inject the right segment examples.
"""

from langchain.prompts import (
    PromptTemplate,
    FewShotPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate
)
import json
import os

def load_few_shot_examples() -> dict:
    """Load the JSON repository of few-shot examples."""
    path = os.path.join(os.path.dirname(__file__), "few_shot_examples.json")
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def get_campaign_prompt_template(segment: str, system_guidance: str = "") -> ChatPromptTemplate:
    """
    Constructs a dynamic ChatPromptTemplate equipped with segment-specific few-shot examples.
    
    Args:
        segment: The customer segment (e.g., "young_professional").
        system_guidance: Dynamically evolved instructions from the optimization loop.
    """
    
    # 1. Base System Prompt
    system_template = """You are an expert, world-class email marketing copywriter. 
Your goal is to write highly personalized email marketing copy that drives high CTR.
You are writing for the customer segment: {segment}.
{system_guidance}

You MUST follow the constraints:
1. Provide the output in exactly the requested format.
2. Ensure the tone matches strictly the user's preferred tone if specified.
3. Be persuasive but natural.
"""

    # 2. Few-shot formatting
    example_template = """
Customer Context: {customer_context}
---
Subject: {subject}
Body: {body}
Variant Style: {variant_style}
"""
    example_prompt = PromptTemplate(
        input_variables=["customer_context", "subject", "body", "variant_style"],
        template=example_template
    )
    
    # Retrieve segment examples
    all_examples = load_few_shot_examples()
    segment_examples = all_examples.get(segment, [])
    
    # Prefix text introducing the examples
    prefix = ""
    if segment_examples:
        prefix = "Here are some highly successful examples for this segment previously:"
        
    few_shot_prompt = FewShotPromptTemplate(
        examples=segment_examples,
        example_prompt=example_prompt,
        prefix=prefix,
        suffix="Now generate exactly TWO distinct variants (Variant A and Variant B) for the following customer.",
        input_variables=[],
        example_separator="\n\n"
    )

    # 3. Final Human Command
    human_template = """
Customer Profile Details:
- Name: {name}
- Age: {age}
- Interests: {interests}
- Purchase History Summary: {purchase_history}
- Preferred Tone: {preferred_tone}

Campaign Objective: {campaign_goal}

Generate Variant A and Variant B. They must take DIFFERENT psychological approaches (e.g., urgency vs curiosity, or emotional vs logical).

Format your response EXACTLY as valid JSON with the following structure:
{{
  "variants": [
    {{
      "variant_id": "A",
      "subject": "...",
      "body": "...",
      "style_notes": "Brief explanation of the psychological approach used"
    }},
    {{
      "variant_id": "B",
      "subject": "...",
      "body": "...",
      "style_notes": "Brief explanation of the psychological approach used"
    }}
  ]
}}
Ensure the JSON is perfectly valid and contains no markdown backticks outside of what's strictly required by the API.
"""
    
    # Assemble into a sequence
    return ChatPromptTemplate.from_messages([
        SystemMessagePromptTemplate.from_template(system_template),
        HumanMessagePromptTemplate.from_template(few_shot_prompt.format()),
        HumanMessagePromptTemplate.from_template(human_template)
    ]).partial(segment=segment, system_guidance=system_guidance)
