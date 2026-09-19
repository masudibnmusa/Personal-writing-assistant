"""
Thin wrapper around the Anthropic API.
"""
from anthropic import Anthropic

from app.config import Config, load_config


def call_llm(system: str, user_message: str, config: Config = None) -> str:
    config = config or load_config()
    client = Anthropic(api_key=config.anthropic_api_key)

    response = client.messages.create(
        model=config.model_name,
        max_tokens=config.max_tokens,
        system=system,
        messages=[{"role": "user", "content": user_message}],
    )

    return "".join(
        block.text for block in response.content if block.type == "text"
    )


def generate_content(prompt: dict, config: Config = None) -> str:
    """prompt is the dict returned by prompt_builder.build_prompt()."""
    return call_llm(system=prompt["system"], user_message=prompt["user"], config=config)