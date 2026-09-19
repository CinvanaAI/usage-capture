import pytest

from ollama_usage_grabber import capture
from ollama_usage_grabber.core import crop_box, parse_usage, render_result


def test_parses_labeled_percentages() -> None:
    result = parse_usage("Cloud Usage\nSession: 12.5%\nWeekly: 84%")
    assert result.session == 12.5
    assert result.weekly == 84
    assert result.strategy == "labels"
    assert result.complete


def test_falls_back_to_position_when_ocr_loses_labels() -> None:
    result = parse_usage("Cloud Usage remaining 9% and 61.5%")
    assert result.session == 9
    assert result.weekly == 61.5
    assert result.strategy == "position"


def test_rejects_out_of_range_percentages() -> None:
    result = parse_usage("Session: 120%\nWeekly: 75%")
    assert result.session is None
    assert result.weekly == 75
    assert not result.complete


def test_result_round_trip() -> None:
    original = parse_usage("Session: 7% Weekly: 40%")
    assert parse_usage(render_result(original)) == original


def test_crop_box() -> None:
    assert crop_box(1000, 500, (0.25, 0.20, 0.75, 0.80)) == (250, 100, 750, 400)


@pytest.mark.parametrize(
    "ratios",
    [(-0.1, 0, 1, 1), (0.5, 0, 0.4, 1), (0, 0.8, 1, 0.2), (0, 0, 1.1, 1)],
)
def test_crop_box_rejects_invalid_ratios(ratios: tuple[float, float, float, float]) -> None:
    with pytest.raises(ValueError):
        crop_box(100, 100, ratios)


def test_capture_fails_closed_off_windows(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(capture.os, "name", "posix")
    with pytest.raises(RuntimeError, match="Windows only"):
        capture.capture_usage(tmp_path)
    assert not any(tmp_path.iterdir())
