#!/usr/bin/env python3
"""Save one YouTube page transcript extraction as markdown."""
from __future__ import annotations

import re
import sys
from pathlib import Path

OUT = Path("/workspace/waqar-asim/transcripts")
OUT.mkdir(parents=True, exist_ok=True)


def make_slug(title: str) -> str:
    s = title.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")[:80].strip("-")
    return s or "untitled"


def existing_for(vid: str) -> Path | None:
    matches = list(OUT.glob(f"*--{vid}.md"))
    return matches[0] if matches else None


def save(vid: str, duration: str, title: str, body: str) -> Path:
    existing = existing_for(vid)
    if existing:
        print(f"SKIP {vid} {existing.name}")
        return existing
    slug = make_slug(title)
    path = OUT / f"{slug}--{vid}.md"
    body = body.strip()
    if not body:
        body = "TRANSCRIPT_FETCH_FAILED"
    header = (
        f"# {title}\n\n"
        f"- **Video ID:** `{vid}`\n"
        f"- **URL:** https://www.youtube.com/watch?v={vid}\n"
        f"- **Duration (seconds):** {duration}\n"
        f"- **Source:** YouTube page transcript extraction\n\n"
        f"---\n\n"
    )
    path.write_text(header + body + "\n", encoding="utf-8")
    print(f"SAVED {path.name} chars={len(body)}")
    return path


def main() -> int:
    if len(sys.argv) < 5:
        print("usage: _save_one.py VIDEO_ID DURATION TITLE TEXT_FILE", file=sys.stderr)
        return 2
    vid, duration, title, text_file = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
    body = Path(text_file).read_text(encoding="utf-8")
    # Strip WebFetch markdown wrapper if present.
    if body.startswith("# Content from https://www.youtube.com/watch?v="):
        lines = body.split("\n", 2)
        body = lines[-1].lstrip("\n") if len(lines) >= 2 else body
    save(vid, duration, title, body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
