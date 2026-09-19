"""
Refines an existing style profile based on user edits/feedback.
Kept intentionally simple for v1 — merges manual overrides.
Automated inference from edit patterns is a v2 feature (see feedback/learner.py).
"""
from typing import Dict

from app.style_engine.style_profile import load_profile, save_profile, validate_profile


def apply_manual_override(name: str, field: str, value) -> Dict:
    """Manually override a single field in a saved profile."""
    profile = load_profile(name)
    if field not in profile:
        raise KeyError(f"Unknown style profile field: {field}")
    profile[field] = value
    validate_profile(profile)
    save_profile(profile, name)
    return profile


def merge_profile_updates(name: str, updates: Dict) -> Dict:
    """Merge a dict of field updates into an existing profile."""
    profile = load_profile(name)
    profile.update(updates)
    validate_profile(profile)
    save_profile(profile, name)
    return profile