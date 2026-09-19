from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import subprocess
import time

from .core import crop_box, parse_usage, render_result


DEFAULT_RATIOS = (0.12, 0.58, 0.94, 0.90)


@dataclass(frozen=True)
class CaptureArtifacts:
    screenshot: Path
    crop: Path
    ocr_text: Path
    result: Path
    validation: Path



def _require_foreground_title(marker: str) -> None:
    """Refuse desktop actions when the expected app is not foreground."""
    import ctypes
    from ctypes import wintypes
    user32 = ctypes.windll.user32
    user32.GetForegroundWindow.restype = wintypes.HWND
    user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
    user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]
    window = user32.GetForegroundWindow()
    length = user32.GetWindowTextLengthW(window)
    title = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(window, title, length + 1)
    if marker.casefold() not in title.value.casefold():
        raise RuntimeError(f"Expected a foreground window containing {marker!r}; capture stopped before the next desktop action.")


def capture_usage(
    output_dir: Path,
    working_directory: Path,
    *,
    launch_seconds: float = 3.0,
    status_seconds: float = 2.0,
    ratios: tuple[float, float, float, float] = DEFAULT_RATIOS,
    close_session: bool = False,
    force: bool = False,
) -> CaptureArtifacts:
    """Launch Codex and OCR `/status`. This function controls the desktop."""
    if os.name != "nt":
        raise RuntimeError("Desktop capture is currently implemented for Windows only.")
    try:
        import pyautogui
        from PIL import Image, ImageGrab
        import pytesseract
    except ImportError as exc:
        raise RuntimeError('Install capture dependencies with: pip install -e ".[capture]"') from exc

    working_directory = working_directory.resolve()
    if not working_directory.is_dir():
        raise ValueError(f"Working directory does not exist: {working_directory}")
    output_dir = output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    artifacts = CaptureArtifacts(
        screenshot=output_dir / "codex_status_window.png",
        crop=output_dir / "codex_status_limits_crop.png",
        ocr_text=output_dir / "codex_status_ocr_raw.txt",
        result=output_dir / "codex_status_limits.txt",
        validation=output_dir / "codex_status_validation.txt",
    )

    if not force and any(path.exists() for path in artifacts.__dict__.values()):
        raise FileExistsError("Capture output exists; use --force only after reviewing the output directory.")

    subprocess.Popen(
        ["cmd.exe", "/k", "title Codex Usage Capture"],
        cwd=working_directory,
        creationflags=subprocess.CREATE_NEW_CONSOLE,
    )
    time.sleep(2)
    _require_foreground_title("Codex")
    pyautogui.write("codex", interval=0.03)
    pyautogui.press("enter")
    time.sleep(launch_seconds)
    _require_foreground_title("Codex")
    pyautogui.write("/status", interval=0.03)
    pyautogui.press("enter")
    time.sleep(status_seconds)
    _require_foreground_title("Codex")
    pyautogui.hotkey("alt", "printscreen")
    time.sleep(1)

    image = ImageGrab.grabclipboard()
    if not isinstance(image, Image.Image):
        raise RuntimeError("The clipboard did not contain an image after Alt+PrintScreen.")
    image = image.convert("RGB")
    image.save(artifacts.screenshot)
    cropped = image.crop(crop_box(*image.size, ratios))
    cropped.save(artifacts.crop)

    ocr_text = pytesseract.image_to_string(cropped)
    artifacts.ocr_text.write_text(ocr_text, encoding="utf-8", errors="replace")
    parsed = parse_usage(ocr_text)
    artifacts.result.write_text(render_result(parsed), encoding="utf-8")
    round_trip = parse_usage(artifacts.result.read_text(encoding="utf-8"))
    valid = parsed.complete and parsed.five_hour == round_trip.five_hour and parsed.weekly == round_trip.weekly
    artifacts.validation.write_text(
        f"Parser strategy: {parsed.strategy}\n"
        f"Complete OCR parse: {'PASS' if parsed.complete else 'FAIL'}\n"
        f"Result round trip: {'PASS' if valid else 'FAIL'}\n",
        encoding="utf-8",
    )

    if close_session:
        _require_foreground_title("Codex")
        pyautogui.write("/exit", interval=0.03)
        pyautogui.press("enter")
        time.sleep(1)
        pyautogui.write("exit", interval=0.03)
        pyautogui.press("enter")
    return artifacts

