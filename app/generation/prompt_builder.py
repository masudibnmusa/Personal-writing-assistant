"""
Combines the style profile + relevant few-shot examples + the user's task
into a single prompt for generation.
"""
from typing import Dict, Optional, List

from app.style_engine.style_profile import profile_to_prompt_text
from app.generation.content_types import CONTENT_TYPES


def build_prompt(
    profile: Dict,
    content_type: str,
    instructions: str,
    few_shot_examples: Optional[List[str]] = None,
) -> Dict[str, str]:
    """Returns {'system': ..., 'user': ...} ready to pass to the LLM."""
    if content_type not in CONTENT_TYPES:
        raise ValueError(f"Unknown content type: {content_type}")

    template = CONTENT_TYPES[content_type]
    style_block = profile_to_prompt_text(profile)

    system_prompt = f"""You are a writing assistant that writes exactly like the user \
described below. Match their tone, vocabulary, sentence structure, and formatting habits.

STYLE PROFILE:
{style_block}

FORMAT GUIDANCE for {content_type}:
{template['guidance']}

Write ONLY the requested content — no preamble, no explanation, no markdown fences."""

    examples_block = ""
    if few_shot_examples:
        examples_block = "\n\nExamples of the user's past writing in this style:\n\n"
        examples_block += "\n\n---\n\n".join(few_shot_examples)

    user_prompt = f"Task: {instructions}{examples_block}"

    return {"system": system_prompt, "user": user_prompt}