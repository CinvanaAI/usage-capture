# Usage Capture

Turn a visible usage display into local, inspectable values. Choose the Codex or Ollama account-display adapter; both keep their original Python APIs and commands.

## Try a parser

Python 3.11+. Parsing requires no account, browser, screenshot or OCR installation.

| Display | Install from this checkout | Run the synthetic example |
| --- | --- | --- |
| Codex five-hour / weekly | `python -m pip install -e ./codex` | `codex-usage parse-text codex/examples/synthetic-ocr.txt` |
| Ollama hosted session / weekly | `python -m pip install -e ./ollama` | `ollama-usage parse-text ollama/examples/synthetic-ocr.txt` |

The examples report 73 and 41 with `strategy: labels`. See the actual [Codex result](codex/examples/result.json) and [Ollama result](ollama/examples/result.json).

## Why retain the evidence?

OCR can lose labels, and a percentage alone does not tell you whether the source meant used or remaining. Each adapter retains the capture, OCR text, parse strategy and normalized values. Positional fallback remains visibly different from a labeled parse.

## Optional Windows capture

Read the selected [Codex adapter](codex/README.md) or [Ollama adapter](ollama/README.md) for capture dependencies and commands. Desktop capture requires Tesseract, the optional capture dependencies, a logged-in app and a matching foreground title. It preserves existing captures unless `--force` is deliberate. The title check reduces accidental focus mistakes; it does not establish the identity of a web page or account.

Live capture has not been validated against your current display layout. The text parsers and crop calculations can be used independently. Keep account screenshots local until reviewed.

Both subpackages use the [MIT license](LICENSE.md). They share one visitor purpose while retaining their distinct display assumptions.
