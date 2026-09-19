# Origin

This repository extracts and hardens a one-off Windows script created to answer a practical question: how much Ollama cloud usage remains when the available value is visible in the settings interface but not conveniently available to a local workflow.

The original proof used browser automation, an active-window screenshot, a ratio-based crop, Tesseract OCR, and a round-trip validation file. This public extraction keeps that approach while removing machine-specific paths, separating parsing from desktop automation, making capture explicitly opt-in, and adding tests for the reusable logic.

