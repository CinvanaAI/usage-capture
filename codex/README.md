# Usage Capture: Codex adapter

Turn a visible Codex usage display into local machine-readable evidence when only the UI exposes it.

## Try it

Python 3.11+. Run from this checkout:

```sh
python -m pip install -e .
codex-usage parse-text examples/synthetic-ocr.txt
```

**Input:** Synthetic labeled OCR: 5h: 73%; Weekly: 41%.

**Result:** The parser returns five_hour=73, weekly=41 and strategy=labels without opening an app or touching the desktop.

See [the captured example](examples/RESULT.md) for the observed output and reproduction command.

## How it works

A text parser, normalized crop calculation and optional screenshot/OCR capture are kept separate. Evidence includes the screenshot, OCR text, extracted values and parse strategy.

Source: [src/codex_usage_grabber/core.py](src/codex_usage_grabber/core.py), [src/codex_usage_grabber/capture.py](src/codex_usage_grabber/capture.py).

## Use it for your work

Install `.[capture]` and Tesseract for explicit `codex-usage capture`. Capture checks the foreground title before desktop actions and preserves existing files unless `--force` is supplied. Review screenshots locally; titles are a focus check, not proof of account or page identity.

## Scope

Percentages retain the display’s meaning; the parser does not infer used versus remaining. Positional fallback is less reliable than labels. Live capture is a Windows foreground-window workaround and has not been verified against your current app layout.

Owned code is available under the [MIT license](LICENSE.md).
