# Security and privacy

The `parse-text` command is an offline text parser. The `capture` command is different: it opens a console, sends keystrokes to the foreground desktop, reads the clipboard, captures an image, and writes OCR evidence.

- Close or hide unrelated private windows before capture.
- Do not change focus until the capture finishes. A focus failure can send `codex`, `/status`, or `/exit` to the wrong application.
- Use a dedicated output directory and review every screenshot and OCR file before sharing it. Status output can expose local configuration, paths, account limits, or other session details beyond the two parsed percentages.
- The program uses the local Codex installation's existing authentication. It does not read, copy, or store Codex credentials.
- OCR output is untrusted text. This project parses it as data and never executes it.

For unattended or security-sensitive use, prefer an official machine-readable usage surface if one becomes available instead of foreground automation.
