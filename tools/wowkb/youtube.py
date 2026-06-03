"""Fetch YouTube transcripts / list channel uploads into raw/youtube/.

Usage:
    uv run python -m wowkb.youtube transcript <video-url-or-id>
    uv run python -m wowkb.youtube channel <channel-url> [--limit 10]
"""

import argparse
import re
import sys

import requests
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi

from ._common import save_raw


def video_id(url: str) -> str:
    m = re.search(r"(?:v=|youtu\.be/|/shorts/)([\w-]{11})", url)
    return m.group(1) if m else url  # assume bare ID


def _fallback_autosubs(info: dict) -> list[dict]:
    """yt-dlp auto-captions fallback: fetch the en json3 track."""
    tracks = (info.get("automatic_captions") or {}).get("en", [])
    track = next((t for t in tracks if t.get("ext") == "json3"), None)
    if not track:
        sys.exit("error: no transcript and no English auto-captions available")
    events = requests.get(track["url"], timeout=30).json().get("events", [])
    return [
        {"start": e["tStartMs"] / 1000, "text": "".join(s.get("utf8", "") for s in e["segs"]).strip()}
        for e in events
        if e.get("segs")
    ]


def transcript(url: str) -> None:
    vid = video_id(url)
    with yt_dlp.YoutubeDL({"quiet": True, "skip_download": True}) as ydl:
        info = ydl.extract_info(f"https://www.youtube.com/watch?v={vid}", download=False)

    try:
        fetched = YouTubeTranscriptApi().fetch(vid, languages=["en"])
        snippets = [{"start": s.start, "text": s.text} for s in fetched]
    except Exception as exc:  # noqa: BLE001 — fall back to auto-subs on any transcript failure
        print(f"youtube-transcript-api failed ({exc.__class__.__name__}), trying yt-dlp auto-subs", file=sys.stderr)
        snippets = _fallback_autosubs(info)

    lines = [
        f"# {info.get('title', vid)}",
        "",
        f"- channel: {info.get('channel', '?')}",
        f"- uploaded: {info.get('upload_date', '?')}",
        f"- url: https://www.youtube.com/watch?v={vid}",
        "",
    ]
    for s in snippets:
        m, sec = divmod(int(s["start"]), 60)
        text = s["text"].replace("\n", " ").strip()
        if text:
            lines.append(f"[{m:02d}:{sec:02d}] {text}")
    out = save_raw("youtube", f"{vid}.md", "\n".join(lines) + "\n")
    print(out)


def channel(url: str, limit: int) -> None:
    opts = {"quiet": True, "extract_flat": True, "playlist_items": f"1-{limit}"}
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url.rstrip("/") + "/videos", download=False)
    for e in info.get("entries", []):
        print(f"{e['id']}  {e.get('title', '?')}")


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.youtube", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("transcript", help="fetch transcript → raw/youtube/<id>.md")
    t.add_argument("url")
    c = sub.add_parser("channel", help="list recent uploads for a channel")
    c.add_argument("url")
    c.add_argument("--limit", type=int, default=10)
    args = p.parse_args()
    if args.cmd == "transcript":
        transcript(args.url)
    else:
        channel(args.url, args.limit)


if __name__ == "__main__":
    main()
