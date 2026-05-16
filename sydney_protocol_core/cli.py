"""Command-line interface for Sydney Protocol Core."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import analyze_text, create_receipt, validate_reading_boundary


def _read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze text with Sydney Protocol Core.")
    parser.add_argument("input", nargs="?", help="Input text file. Reads stdin if omitted.")
    parser.add_argument("--profile", default="technbuddy_chat", help="App profile key.")
    parser.add_argument("--lang", default=None, help="Language: en or nl. Auto-detects if omitted.")
    parser.add_argument("--receipt", action="store_true", help="Emit compact receipt instead of full reading.")
    parser.add_argument("--check-boundary", action="store_true", help="Include boundary validation issues in output.")
    args = parser.parse_args(argv)

    reading = analyze_text(_read_input(args.input), profile=args.profile, language=args.lang)
    output = create_receipt(reading).to_dict() if args.receipt else reading.to_dict()
    if args.check_boundary:
        output["boundary_validation_issues"] = validate_reading_boundary(reading)
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
