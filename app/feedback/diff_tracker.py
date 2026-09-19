"""
Compares a user's edited version of generated content against the original draft.
"""
import difflib
from typing import List, Dict


def get_diff(original: str, edited: str) -> List[str]:
    """Return a unified diff between the generated draft and the user's edited version."""
    return list(
        difflib.unified_diff(
            original.splitlines(),
            edited.splitlines(),
            fromfile="generated",
            tofile="edited",
            lineterm="",
        )
    )


def diff_summary(original: str, edited: str) -> Dict:
    """Lightweight stats about how much changed, for logging to generation_history."""
    diff = get_diff(original, edited)
    added = sum(1 for line in diff if line.startswith("+") and not line.startswith("+++"))
    removed = sum(1 for line in diff if line.startswith("-") and not line.startswith("---"))
    return {
        "lines_added": added,
        "lines_removed": removed,
        "diff": diff,
    }