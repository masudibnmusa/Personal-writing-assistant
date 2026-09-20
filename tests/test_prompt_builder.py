import pytest

from app.generation.prompt_builder import build_prompt


SAMPLE_PROFILE = {
    "tone": "warm but direct",
    "sentence_length": "short, punchy",
    "vocabulary": ["honestly", "quick note"],
    "formatting_habits": "short paragraphs, occasional bullets",
    "common_openers": ["Hey team,"],
    "common_closers": ["Thanks!"],
    "quirks": ["uses em-dashes"],
}


def test_build_prompt_includes_style_profile_fields():
    prompt = build_prompt(
        profile=SAMPLE_PROFILE,
        content_type="email",
        instructions="Write a follow-up about the Q3 deadline",
    )

    assert "warm but direct" in prompt["system"]
    assert "honestly" in prompt["system"]
    assert "Q3 deadline" in prompt["user"]


def test_build_prompt_includes_content_type_guidance():
    prompt = build_prompt(
        profile=SAMPLE_PROFILE,
        content_type="linkedin_post",
        instructions="Announce our new product",
    )

    assert "LinkedIn" in prompt["system"] or "hook" in prompt["system"].lower()


def test_build_prompt_rejects_unknown_content_type():
    with pytest.raises(ValueError):
        build_prompt(
            profile=SAMPLE_PROFILE,
            content_type="carrier_pigeon_letter",
            instructions="test",
        )


def test_build_prompt_includes_few_shot_examples_when_given():
    prompt = build_prompt(
        profile=SAMPLE_PROFILE,
        content_type="email",
        instructions="Write a thank-you note",
        few_shot_examples=["Hey team, thanks so much for pulling this off — honestly amazing work."],
    )

    assert "honestly amazing work" in prompt["user"]