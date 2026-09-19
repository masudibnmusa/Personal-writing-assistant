"""
Placeholder for automated style-profile refinement from repeated edit patterns.

NOTE: Intentionally minimal for v1. Reliably inferring *why* an edit was made
(tone correction vs. factual fix vs. one-off preference) from a raw diff is hard.
This module currently just logs edits for future analysis; it does not yet
auto-update the style profile. See profile_updater.py for manual overrides.
"""
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict

HISTORY_DIR = Path("data/generation_history")


def log_edit(profile_name: str, original: str, edited: str, diff_summary: Dict) -> Path:
    HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    entry = {
        "profile_name": profile_name,
        "timestamp": timestamp,
        "original": original,
        "edited": edited,
        "diff_summary": diff_summary,
    }
    out_path = HISTORY_DIR / f"{profile_name}_{timestamp}.json"
    out_path.write_text(json.dumps(entry, indent=2), encoding="utf-8")
    return out_path


def suggest_profile_updates(profile_name: str) -> None:
    """
    Future work: scan generation_history for this profile, look for repeated
    edit patterns (e.g. consistently shortening sentences, removing emoji),
    and propose field-level updates for human review before applying.
    """
    raise NotImplementedError("Automated learning is a v2 feature.")