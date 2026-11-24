#!/usr/bin/env python3
"""Ship It Friday entry: emit the one-line commit message to $MAKEFUN_OUTPUT_DIR/entry.txt.

Reads entry.txt next to this script, validates it against the contest gate
(UTF-8, 1-159 characters, not only whitespace, single line), and writes the
normalized bytes to the output directory. Pure Python standard library only.
"""

import os
import sys
from pathlib import Path

MAX_CHARS = 159


def main() -> int:
    here = Path(__file__).resolve().parent
    src = here / "entry.txt"
    try:
        raw = src.read_bytes()
    except OSError as exc:
        print(f"error: cannot read {src}: {exc}", file=sys.stderr)
        return 1
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        print(f"error: entry.txt is not valid UTF-8: {exc}", file=sys.stderr)
        return 1
    if text.endswith("\n"):
        text = text[:-1]
    if text.endswith("\r"):
        text = text[:-1]
    if not 1 <= len(text) <= MAX_CHARS:
        print(
            f"error: entry must be 1-{MAX_CHARS} characters, got {len(text)}",
            file=sys.stderr,
        )
        return 1
    if not text.strip():
        print("error: entry must not be only whitespace", file=sys.stderr)
        return 1
    if "\n" in text or "\r" in text:
        print(
            "error: entry must be a single line "
            "(no newline or carriage return inside)",
            file=sys.stderr,
        )
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "entry.txt"
    out_path.write_bytes(text.encode("utf-8"))
    os.chmod(out_path, 0o644)
    print(f"entry.txt: {len(text)} characters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
