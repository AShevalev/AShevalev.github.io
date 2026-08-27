#!/usr/bin/env python3
"""Download YouTube captions for every Waqar Asim video listed in videos.tsv."""

from __future__ import annotations

import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    NoTranscriptFound,
    TranscriptsDisabled,
    VideoUnavailable,
    YouTubeRequestFailed,
)

ROOT = Path("/workspace/waqar-asim")
LIST = Path("/tmp/waqar-yt/videos.tsv")
OUT = ROOT / "transcripts"
LOG = ROOT / "_download_log.txt"

OUT.mkdir(parents=True, exist_ok=True)


def slug(title: str, vid: str) -> str:
    s = re.sub(r"[^\w\s-]", "", title, flags=re.UNICODE)
    s = re.sub(r"[\s-]+", "-", s).strip("-").lower()
    s = s[:80] or "untitled"
    return f"{s}--{vid}"


def fmt_ts(seconds: float) -> str:
    s = int(seconds)
    h, s = divmod(s, 3600)
    m, s = divmod(s, 60)
    if h:
        return f"{h:d}:{m:02d}:{s:02d}"
    return f"{m:d}:{s:02d}"


def fetch_one(vid: str, duration: str, title: str) -> tuple[str, str]:
    api = YouTubeTranscriptApi()
    try:
        fetched = api.fetch(vid, languages=["en", "en-US", "en-GB"])
        lines = []
        for snippet in fetched:
            start = getattr(snippet, "start", snippet.get("start") if isinstance(snippet, dict) else 0)
            text = getattr(snippet, "text", snippet.get("text") if isinstance(snippet, dict) else "")
            text = text.replace("\n", " ").strip()
            if text:
                lines.append(f"[{fmt_ts(start)}] {text}")
        body = "\n".join(lines)
        if not body.strip():
            return vid, "empty"
        path = OUT / f"{slug(title, vid)}.md"
        path.write_text(
            f"# {title}\n\n"
            f"- **Video ID:** `{vid}`\n"
            f"- **URL:** https://www.youtube.com/watch?v={vid}\n"
            f"- **Duration (seconds):** {duration}\n"
            f"- **Source:** YouTube captions (auto or uploaded)\n\n"
            f"---\n\n{body}\n",
            encoding="utf-8",
        )
        return vid, "ok"
    except (NoTranscriptFound, TranscriptsDisabled) as e:
        return vid, f"no_captions:{type(e).__name__}"
    except VideoUnavailable:
        return vid, "unavailable"
    except YouTubeRequestFailed as e:
        return vid, f"request_failed:{e}"
    except Exception as e:
        return vid, f"error:{type(e).__name__}:{e}"


def main() -> int:
    rows = []
    for line in LIST.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        vid, duration, title = line.split("\t", 2)
        rows.append((vid, duration, title))

    log_lines = []
    ok = fail = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(fetch_one, *row): row for row in rows}
        for i, fut in enumerate(as_completed(futs), 1):
            vid, duration, title = futs[fut]
            status = fut.result()[1]
            if status == "ok":
                ok += 1
            else:
                fail += 1
            msg = f"{i}/{len(rows)} {status} {vid} {title}"
            print(msg, flush=True)
            log_lines.append(f"{vid}\t{status}\t{title}")
            if i % 20 == 0:
                time.sleep(0.4)

    LOG.write_text("\n".join(log_lines) + f"\n\nOK={ok} FAIL={fail} TOTAL={len(rows)}\n", encoding="utf-8")
    print(f"DONE ok={ok} fail={fail} total={len(rows)}")
    return 0 if fail < len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
