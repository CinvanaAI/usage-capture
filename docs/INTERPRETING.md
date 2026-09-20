# Decide whether a captured value is usable

The adapters grew from one-off Windows OCR workflows. They now separate parsing,
cropping and desktop control so the useful parsing mechanism can be tried without
an account or screen access. The [Codex origin](../codex/ORIGIN.md) and
[Ollama origin](../ollama/ORIGIN.md) describe those separate beginnings.

From the repository root:

```sh
python -m pip install -e ./codex -e ./ollama
python examples/walkthrough.py
```

The [synthetic result](../examples/result.json) compares both adapters over four
cases. Labels assign values by meaning even if the display order changes. If
only the weekly label is readable, the other value remains null. If neither label
matches, positional fallback takes the first two valid unsigned percentages.
Malformed long decimals and negative/signed tokens are not reinterpreted as
positive values. This repair belongs to the public parser continuation.

| Result | Interpretation |
| --- | --- |
| `labels`, both values | Two recognized fields; still compare with the screenshot |
| `labels`, one null | Partial parse; do not replace the missing value with zero |
| `position`, both values | Two numbers found in order; labels/meaning remain unverified |
| null values | No usable number for that field |

`complete` means both fields contain a parsed number, not that OCR or ordering was
correct. The `parse-text` command exits 0 for a complete parse (including position)
and 2 for an incomplete one. A consumer requiring labeled evidence should also
check `strategy == "labels"`. Duplicate/contradictory labels, unrelated percentages
and layouts outside the patterns require human inspection; this is not a general
OCR language model.

Numbers preserve the source display's semantics. Nothing in this parser decides
used versus remaining, local token consumption, billing cost, reset time or account
identity. A round-trip PASS means rendered numbers can be parsed again; it cannot
validate the original OCR against the display.

For optional capture, keep screenshot, crop, raw OCR, normalized text and validation
file together in a dedicated local output folder. The capture command can finish
and save evidence even when its parse is incomplete: read the validation file.
Review the screenshot before trusting the values. A foreground-title check is a
focus check only. Live display compatibility was not exercised for this edition.
