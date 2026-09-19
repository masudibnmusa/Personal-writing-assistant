"""
Build, validate, and persist structured style profiles as JSON.
"""
import json
from pathlib import Path
from typing import Dict

PROFILES_DIR = Path("data/style_profiles")

REQUIRED_KEYS = {
    "tone", "sentence_length", "vocabulary",
    "formatting_habits", "common_openers", "common_closers", "quirks",
}


def validate_profile(profile: Dict) -> None:
    missing = REQUIRED_KEYS - profile.keys()
    if missing:
        raise ValueError(f"Style profile missing required keys: {missing}")


def save_profile(profile: Dict, name: str = "default") -> Path:
    validate_profile(profile)
    PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = PROFILES_DIR / f"{name}.json"
    out_path.write_text(json.dumps(profile, indent=2), encoding="utf-8")
    return out_path


def load_profile(name: str = "default") -> Dict:
    path = PROFILES_DIR / f"{name}.json"
    if not path.exists():
        raise FileNotFoundError(
            f"No style profile named '{name}'. Run 'analyze' first."
        )
    return json.loads(path.read_text(encoding="utf-8"))


def profile_to_prompt_text(profile: Dict) -> str:
    """Render a style profile as a compact block of prompt text."""
    lines = [
        f"Tone: {profile['tone']}",
        f"Sentence length: {profile['sentence_length']}",
        f"Characteristic vocabulary: {', '.join(profile['vocabulary'])}",
        f"Formatting habits: {profile['formatting_habits']}",
        f"Typical openers: {', '.join(profile['common_openers'])}",
        f"Typical closers: {', '.join(profile['common_closers'])}",
        f"Quirks: {', '.join(profile['quirks'])}",
    ]
    return "\n".join(lines)