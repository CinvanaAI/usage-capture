# Usage Capture: Ollama adapter

Extract session and weekly usage percentages from a visible Ollama account page with evidence of what was captured.

## Try it

Python 3.11+. Run from this checkout:

```sh
python -m pip install -e .
ollama-usage parse-text examples/synthetic-ocr.txt
```

**Input:** Synthetic OCR: Session: 73%; Weekly: 41%.

**Result:** The parser returns session=73, weekly=41 and strategy=labels, without a browser or account.

See [the captured example](examples/RESULT.md) for the observed output and reproduction command.

## How it works

OCR text parsing is independently usable; optional browser capture preserves the supporting screenshot and raw text.

Source: [src/ollama_usage_grabber/core.py](src/ollama_usage_grabber/core.py), [src/ollama_usage_grabber/capture.py](src/ollama_usage_grabber/capture.py).

## Use it for your work

Install `.[capture]` and Tesseract for Windows `ollama-usage capture`. It opens the configured settings page and checks the foreground title. Existing captures require `--force`; keep account screenshots private.

## Scope

This adapter concerns the hosted account display, not local inference token usage. Percent meaning belongs to the source display. A title check does not verify page identity; positional parsing is uncertain.

Owned code is available under the [MIT license](LICENSE.md).
