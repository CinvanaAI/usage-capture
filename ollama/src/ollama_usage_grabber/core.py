from __future__ import annotations

from dataclasses import dataclass
import re


_PERCENT = re.compile(r"(?<![\d.,+\-\u2212\ufe63\uff0d\uff0b])(\d{1,3}(?:[.,]\d+)?)\s*%")


@dataclass(frozen=True)
class UsageResult:
    session: float | None
    weekly: float | None
    strategy: str

    @property
    def complete(self) -> bool:
        return self.session is not None and self.weekly is not None


def _valid_percentage(raw: str) -> float | None:
    value = float(raw.replace(",", "."))
    return value if 0 <= value <= 100 else None


def _labeled(text: str, label: str) -> float | None:
    match = re.search(
        rf"(?<!\w){label}\s*(?::\s*|-\s+)?(\d{{1,3}}(?:[.,]\d+)?)\s*%",
        text,
        re.IGNORECASE,
    )
    return _valid_percentage(match.group(1)) if match else None


def parse_usage(text: str) -> UsageResult:
    """Parse session and weekly usage percentages from OCR or saved text."""
    session = _labeled(text, "session")
    weekly = _labeled(text, "weekly")
    if session is not None or weekly is not None:
        return UsageResult(session=session, weekly=weekly, strategy="labels")

    values = [value for value in (_valid_percentage(m.group(1)) for m in _PERCENT.finditer(text)) if value is not None]
    return UsageResult(
        session=values[0] if values else None,
        weekly=values[1] if len(values) > 1 else None,
        strategy="position",
    )


def crop_box(
    width: int,
    height: int,
    ratios: tuple[float, float, float, float],
) -> tuple[int, int, int, int]:
    """Convert normalized left/top/right/bottom ratios into a pixel box."""
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
    if value is None:
        return "NOT FOUND"
    return f"{value:g}%"


def render_result(result: UsageResult) -> str:
    return (
        f"Session: {format_percentage(result.session)}\n"
        f"Weekly: {format_percentage(result.weekly)}\n"
    )
