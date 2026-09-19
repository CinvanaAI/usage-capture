from __future__ import annotations

from dataclasses import dataclass
import re


_PERCENT = re.compile(r"(?<!\d)(\d{1,3}(?:[.,]\d+)?)\s*%")


@dataclass(frozen=True)
class UsageResult:
    five_hour: float | None
    weekly: float | None
    strategy: str

    @property
    def complete(self) -> bool:
        return self.five_hour is not None and self.weekly is not None


def _valid_percentage(raw: str) -> float | None:
    value = float(raw.replace(",", "."))
    return value if 0 <= value <= 100 else None


def _labeled(text: str, label: str) -> float | None:
    match = re.search(
        rf"{label}\s*[:\-]?\s*(\d{{1,3}}(?:[.,]\d+)?)\s*%",
        text,
        re.IGNORECASE,
    )
    return _valid_percentage(match.group(1)) if match else None


def parse_usage(text: str) -> UsageResult:
    """Parse five-hour and weekly usage percentages from Codex status OCR."""
    five_hour = _labeled(text, r"(?:5\s*h(?:our)?(?:\s+limit)?|five[- ]?hour(?:\s+limit)?)")
    weekly = _labeled(text, r"weekly(?:\s+limit)?")
    if five_hour is not None or weekly is not None:
        return UsageResult(five_hour=five_hour, weekly=weekly, strategy="labels")

    values = [value for value in (_valid_percentage(m.group(1)) for m in _PERCENT.finditer(text)) if value is not None]
    return UsageResult(
        five_hour=values[0] if values else None,
        weekly=values[1] if len(values) > 1 else None,
        strategy="position",
    )


def crop_box(
    width: int,
    height: int,
    ratios: tuple[float, float, float, float],
) -> tuple[int, int, int, int]:
    if width <= 0 or height <= 0:
        raise ValueError("Image dimensions must be positive.")
    left, top, right, bottom = ratios
    if not (0 <= left < right <= 1 and 0 <= top < bottom <= 1):
        raise ValueError("Crop ratios must describe an ordered box within 0..1.")
    return (
        int(width * left),
        int(height * top),
        int(width * right),
        int(height * bottom),
    )


def format_percentage(value: float | None) -> str:
    return "NOT FOUND" if value is None else f"{value:g}%"


def render_result(result: UsageResult) -> str:
    return (
        f"5h: {format_percentage(result.five_hour)}\n"
        f"Weekly: {format_percentage(result.weekly)}\n"
    )

