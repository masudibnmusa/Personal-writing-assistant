from unittest.mock import patch, MagicMock

from app.generation.llm import call_llm, generate_content
from app.config import Config


FAKE_CONFIG = Config(anthropic_api_key="fake-key", model_name="claude-sonnet-4-6", max_tokens=512)


def _mock_text_block(text):
    block = MagicMock()
    block.type = "text"
    block.text = text
    return block


@patch("app.generation.llm.Anthropic")
def test_call_llm_returns_text_from_response(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [_mock_text_block("Generated draft content.")]
    mock_client.messages.create.return_value = mock_response
    mock_anthropic_cls.return_value = mock_client

    result = call_llm(system="You are a writer.", user_message="Write something.", config=FAKE_CONFIG)

    assert result == "Generated draft content."
    mock_client.messages.create.assert_called_once()


@patch("app.generation.llm.Anthropic")
def test_call_llm_joins_multiple_text_blocks(mock_anthropic_cls):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [_mock_text_block("Part one. "), _mock_text_block("Part two.")]
    mock_client.messages.create.return_value = mock_response
    mock_anthropic_cls.return_value = mock_client

    result = call_llm(system="sys", user_message="usr", config=FAKE_CONFIG)

    assert result == "Part one. Part two."


@patch("app.generation.llm.call_llm")
def test_generate_content_uses_prompt_dict(mock_call_llm):
    mock_call_llm.return_value = "final output"

    prompt = {"system": "sys prompt", "user": "user prompt"}
    result = generate_content(prompt, config=FAKE_CONFIG)

    assert result == "final output"
    mock_call_llm.assert_called_once_with(system="sys prompt", user_message="user prompt", config=FAKE_CONFIG)