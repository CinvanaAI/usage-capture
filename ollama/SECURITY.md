# Security and privacy

The `parse-text` command is an offline parser. The `capture` command opens an authenticated browser page, controls the foreground desktop, reads the clipboard, captures an image, and writes OCR evidence.

- Sign in to Ollama yourself in the default browser. This tool does not read, copy, or store browser credentials.
- Close or hide unrelated private windows before capture and do not change focus during the wait. A focus error can screenshot the wrong window.
- `--close-tab` closes whichever browser tab is active at the end, so use it only when focus is controlled.
- Settings screenshots and OCR may expose account details or other private page content beyond the parsed percentages. Review every artifact before sharing it.
- Known evidence files are no-overwrite by default. Use `--force` only after checking the exact output directory.
- OCR output is untrusted text and is never executed.

Prefer an official machine-readable usage surface if one becomes available for the workflow.
