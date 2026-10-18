#!/usr/bin/env python3
"""Merges exported lists (e.g. from the app's "Prepare cards" → Export) into spotify.csv.

Usage:
  python3 tools/merge.py export.csv [more.csv ...]            # add new songs only
  python3 tools/merge.py --replace export.csv [more.csv ...]  # also overwrite differing matches

New songs are added; songs already listed keep their current YouTube video
unless --replace is given (use that when the export contains fixes). Lines
that don't look like a song (wrong ID format, header lines) are skipped and
reported. The result is written back sorted, ready for tools/check.py.
"""
import csv
import re
import sys
from pathlib import Path

PATH = Path(__file__).resolve().parent.parent / "spotify.csv"
HEADER = ["spotify_id", "youtube_id"]
SPOTIFY = re.compile(r"^[A-Za-z0-9]{22}$")
YOUTUBE = re.compile(r"^[A-Za-z0-9_-]{11}$")


def read_pairs(path: Path):
    with path.open(newline="", encoding="utf-8") as f:
        for n, row in enumerate(csv.reader(f), start=1):
            cells = [c.strip() for c in row]
            if len(cells) < 2 or cells[:2] == HEADER:
                continue
            sp, yt = cells[0], cells[1]
            if SPOTIFY.match(sp) and YOUTUBE.match(yt):
                yield sp, yt
            elif any(cells):
                print(f"{path.name} line {n}: skipped (not a spotify_id,youtube_id pair): {','.join(cells)}")


def main(args) -> int:
    replace = "--replace" in args
    files = [Path(a) for a in args if a != "--replace"]
    if not files:
        print(__doc__)
        return 2

    current = dict(read_pairs(PATH))
    added = replaced = kept = same = 0
    for path in files:
        for sp, yt in read_pairs(path):
            old = current.get(sp)
            if old is None:
                current[sp] = yt
                added += 1
            elif old == yt:
                same += 1
            elif replace:
                current[sp] = yt
                replaced += 1
            else:
                kept += 1
                print(f"{sp}: list has {old}, export has {yt} — kept the list's (use --replace to take the export's)")

    with PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(HEADER)
        for sp in sorted(current):
            w.writerow([sp, current[sp]])

    print(f"added {added}, replaced {replaced}, kept {kept} differing, {same} already identical — {len(current)} songs total")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
