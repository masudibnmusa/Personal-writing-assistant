"""
Ingest writing samples from a directory (or pasted text) into a list of strings.
"""
import os
from pathlib import Path
from typing import List

from app.utils.text_cleaner import clean_text

SUPPORTED_EXTENSIONS = {".txt", ".md"}


def collect_samples(samples_dir: str) -> List[str]:
    """Read all supported files from samples_dir and return cleaned text samples."""
    path = Path(samples_dir)
    if not path.exists():
        raise FileNotFoundError(f"Samples directory not found: {samples_dir}")

    samples = []
    for file in sorted(path.iterdir()):
        if file.suffix.lower() in SUPPORTED_EXTENSIONS:
            raw = file.read_text(encoding="utf-8", errors="ignore")
            samples.append(clean_text(raw))

    if not samples:
        raise ValueError(f"No writing samples found in {samples_dir}")

    return samples


def collect_pasted_samples(raw_texts: List[str]) -> List[str]:
    """Clean a list of pasted text blocks (e.g. from a UI textarea)."""
    return [clean_text(t) for t in raw_texts if t.strip()]