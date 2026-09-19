"""Ollama cloud-usage OCR parsing and optional desktop capture."""

from .core import UsageResult, crop_box, parse_usage

__all__ = ["UsageResult", "crop_box", "parse_usage"]

