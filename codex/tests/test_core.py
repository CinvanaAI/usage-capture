import pytest

from codex_usage_grabber.core import crop_box, parse_usage, render_result


def test_parses_labeled_percentages() -> None:
    result = parse_usage("5h: 23%\nWeekly: 81%")
    assert result.five_hour == 23
    assert result.weekly == 81
    assert result.strategy == "labels"
    assert result.complete


def test_parses_expanded_labels_and_decimals() -> None:
    result = parse_usage("Five-hour limit 12.5% Weekly limit 64,5%")
    assert result.five_hour == 12.5
    assert result.weekly == 64.5


def test_falls_back_to_position_when_ocr_loses_labels() -> None:
    result = parse_usage("limits remaining 7% then 44%")
    assert result.five_hour == 7
    assert result.weekly == 44
    assert result.strategy == "position"


def test_rejects_out_of_range_percentages() -> None:
    result = parse_usage("5h: 101%\nWeekly: 90%")
    assert result.five_hour is None
    assert result.weekly == 90
    assert not result.complete


def test_result_round_trip() -> None:
    original = parse_usage("5h: 9% Weekly: 39%")
    assert parse_usage(render_result(original)) == original


def test_crop_box() -> None:
    assert crop_box(1000, 500, (0.10, 0.20, 0.90, 0.80)) == (100, 100, 900, 400)


@pytest.mark.parametrize(
    "ratios",
    [(-0.1, 0, 1, 1), (0.5, 0, 0.4, 1), (0, 0.8, 1, 0.2), (0, 0, 1.1, 1)],
)
def test_crop_box_rejects_invalid_ratios(ratios: tuple[float, float, float, float]) -> None:
    with pytest.raises(ValueError):
        crop_box(100, 100, ratios)



@pytest.mark.parametrize("text", ["-5% then -40%", "+5% then +40%", "1000.5% then 9999,4%", "\u22125% then \u221240%", "\uff0d5% then \uff0d40%"])
def test_invalid_tokens_cannot_become_valid_positional_values(text):
    result = parse_usage(text)
    assert not result.complete
    assert result.weekly is None
    assert result.five_hour is None


@pytest.mark.parametrize("text", ["5h: -5% Weekly: -40%", "5h -5% Weekly -40%"])
def test_negative_labeled_values_are_not_separator_hyphens(text):
    result = parse_usage(text)
    assert result.five_hour is None and result.weekly is None
