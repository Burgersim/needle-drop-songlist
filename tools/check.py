#!/usr/bin/env python3
"""Validates spotify.csv: header, ID formats, no duplicates, sorted.

Usage:
  python3 tools/check.py          # check (also run automatically on pull requests)
  python3 tools/check.py --fix    # sort and drop exact duplicate lines
"""
import csv
import re
import sys
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "spotify.csv"
HEADER = ["spotify_id", "youtube_id"]
SPOTIFY = re.compile(r"^[A-Za-z0-9]{22}$")
YOUTUBE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def main() -> int:
    fix = "--fix" in sys.argv
    with PATH.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))

    errors = []
    if not rows or [c.strip() for c in rows[0]] != HEADER:
        errors.append(f"line 1: header must be '{','.join(HEADER)}'")

    first_line = {}  # spotify_id -> (line number, youtube_id)
    entries = []
    for n, row in enumerate(rows[1:], start=2):
        if not row or all(not c.strip() for c in row):
            continue
        if len(row) != 2:
            errors.append(f"line {n}: expected 2 columns, got {len(row)}")
            continue
        sp, yt = (c.strip() for c in row)
        if not SPOTIFY.match(sp):
            errors.append(f"line {n}: '{sp}' is not a Spotify track ID (22 letters/digits)")
        if not YOUTUBE.match(yt):
            errors.append(f"line {n}: '{yt}' is not a YouTube video ID (11 characters)")
        if sp in first_line:
            line, other = first_line[sp]
            if other == yt and fix:
                continue  # exact duplicate: --fix drops it
            errors.append(f"line {n}: {sp} is already listed on line {line}")
            continue
        first_line[sp] = (n, yt)
        entries.append((sp, yt))

    if fix:
        if errors:
            for e in errors:
                print(e)
            print("not fixed: resolve the problems above first")
            return 1
        with PATH.open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f, lineterminator="\n")
            w.writerow(HEADER)
            for sp, yt in sorted(entries):
                w.writerow([sp, yt])
        print(f"ok: {len(entries)} entries, sorted")
        return 0

    ids = [sp for sp, _ in entries]
    if ids != sorted(ids):
        errors.append("entries must be sorted by spotify_id (run: python3 tools/check.py --fix)")
    for e in errors:
        print(f"::error file=spotify.csv::{e}")
    print(f"{len(entries)} entries, {len(errors)} problems")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
