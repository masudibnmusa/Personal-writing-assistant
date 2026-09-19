"""
Uses an LLM call to extract tone, vocabulary, and structural patterns
from a set of writing samples.
"""
import json
from typing import List, Dict

from app.config import load_config
from app.generation.llm import call_llm

ANALYSIS_SYSTEM_PROMPT = """You are a writing style analyst. Given several writing samples \
from the same author, extract a structured style profile.

Return ONLY valid JSON (no markdown fences, no preamble) matching this schema:
{
  "tone": "string describing overall tone (e.g. warm but direct, formal, dry-humored)",
  "sentence_length": "short/medium/long/varied, with a brief note",
  "vocabulary": ["list", "of", "characteristic", "words/phrases"],
  "formatting_habits": "bullets vs prose, emoji use, paragraph length, etc.",
  "common_openers": ["typical opening lines or greetings"],
  "common_closers": ["typical sign-offs or closing lines"],
  "quirks": ["distinctive habits: contractions, em-dashes, rhetorical questions, etc."]
}"""


def analyze_style(samples: List[str]) -> Dict:
    """Send samples to the LLM and parse the returned style profile JSON."""
    config = load_config()
    joined = "\n\n---SAMPLE---\n\n".join(samples)

    user_prompt = f"Writing samples:\n\n{joined}\n\nExtract the style profile as JSON."

    raw_response = call_llm(
        system=ANALYSIS_SYSTEM_PROMPT,
        user_message=user_prompt,
        config=config,
    )

    cleaned = raw_response.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()

    try:
        profile = json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"Style analyzer returned invalid JSON: {e}\nRaw: {raw_response}")

    return profile