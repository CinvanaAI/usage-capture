from __future__ import annotations

import argparse
from dataclasses import asdict
import json
from pathlib import Path

from .capture import DEFAULT_RATIOS, capture_usage
from .core import parse_usage


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Parse or capture visible Ollama cloud usage.")
    commands = parser.add_subparsers(dest="command", required=True)

    parse_command = commands.add_parser("parse-text", help="Parse a saved OCR text file.")
    parse_command.add_argument("path", type=Path)

    capture_command = commands.add_parser("capture", help="Control the desktop and capture the active browser window.")
    capture_command.add_argument("--output-dir", type=Path, default=Path("output"))
    capture_command.add_argument("--load-seconds", type=float, default=5.0)
    capture_command.add_argument("--crop", nargs=4, type=float, metavar=("LEFT", "TOP", "RIGHT", "BOTTOM"), default=DEFAULT_RATIOS)
    capture_command.add_argument("--close-tab", action="store_true")
    capture_command.add_argument("--force", action="store_true", help="Replace this tool's known evidence files")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "parse-text":
        result = parse_usage(args.path.read_text(encoding="utf-8", errors="replace"))
        print(json.dumps(asdict(result), indent=2))
        return 0 if result.complete else 2

    artifacts = capture_usage(
        args.output_dir,
        load_seconds=args.load_seconds,
        ratios=tuple(args.crop),
        close_tab=args.close_tab,
        force=args.force,
    )
    print(json.dumps({key: str(value) for key, value in asdict(artifacts).items()}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
