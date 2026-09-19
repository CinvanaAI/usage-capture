# Origin

This repository extracts and hardens a one-off Windows script that opened Codex, requested `/status`, captured the terminal window, and used OCR to recover the displayed five-hour and weekly usage percentages.

The public extraction removes machine-specific working paths, separates OCR parsing from desktop control, makes capture explicitly opt-in, and adds a tested text-only mode. It remains a visual fallback rather than an official machine-readable usage API.

