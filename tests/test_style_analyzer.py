import json
import pytest
from unittest.mock import patch

from app.style_engine.style_analyzer import analyze_style


VALID_PROFILE_JSON = json.dumps({
    "tone": "warm but direct",
    "sentence_length": "short, punchy",
    "vocabulary": ["honestly", "quick note", "let's"],
    "formatting_habits": "prefers short paragraphs, occasional bullets",
    "common_openers": ["Hey team,", "Quick update:"],
    "common_closers": ["Thanks!", "Talk soon,"],
    "quirks": ["uses em-dashes", "starts sentences with 'So'"],
})


@patch("app.style_engine.style_analyzer.call_llm")
def test_analyze_style_returns_parsed_profile(mock_call_llm):
    mock_call_llm.return_value = VALID_PROFILE_JSON

    samples = ["Hey team, quick update on the launch...", "So, here's where we are..."]
    profile = analyze_style(samples)

    assert profile["tone"] == "warm but direct"
    assert "honestly" in profile["vocabulary"]
    mock_call_llm.assert_called_once()


@patch("app.style_engine.style_analyzer.call_llm")
def test_analyze_style_strips_markdown_fences(mock_call_llm):
    mock_call_llm.return_value = f"```json\n{VALID_PROFILE_JSON}\n```"

    profile = analyze_style(["some sample text"])

    assert profile["tone"] == "warm but direct"


@patch("app.style_engine.style_analyzer.call_llm")
def test_analyze_style_raises_on_invalid_json(mock_call_llm):
    mock_call_llm.return_value = "not valid json at all"

    with pytest.raises(ValueError):
        analyze_style(["some sample text"])


def test_analyze_style_requires_samples():
    with pytest.raises(Exception):
        analyze_style([])