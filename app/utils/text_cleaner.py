"""
Basic text cleaning utilities for writing samples.
"""
import re


def clean_text(text: str) -> str:
    """Strip excessive whitespace, normalize line endings, remove control chars."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def strip_email_signature(text: str) -> str:
    """Naive signature stripper — cuts text at common sign-off markers."""
    markers = ["--\n", "\nBest,", "\nRegards,", "\nThanks,", "\nSent from my"]
    for marker in markers:
        idx = text.find(marker)
        if idx != -1:
            text = text[:idx]
    return text.strip()