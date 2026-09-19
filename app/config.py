"""
Loads configuration (API keys, model settings) from environment variables.
"""
import os
from dataclasses import dataclass

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


@dataclass
class Config:
    anthropic_api_key: str
    model_name: str = "claude-sonnet-4-6"
    max_tokens: int = 1024


def load_config() -> Config:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key."
        )
    return Config(
        anthropic_api_key=api_key,
        model_name=os.environ.get("MODEL_NAME", "claude-sonnet-4-6"),
        max_tokens=int(os.environ.get("MAX_TOKENS", "1024")),
    )