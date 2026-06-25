"""Fetch official boss portrait renders for the M+ Memory Trainer.

For every `### <Boss> <!-- enc:NNN -->` heading in the eight
`knowledge/endgame/mythic-plus/<dungeon>.md` files, resolve the Blizzard
journal encounter → its creature → that creature's display render, download the
high-res "zoom" portrait, and process it with Pillow into an optimized `.webp`:

    journal-encounter/{enc}            → creatures[].creature_display.id
    media/creature-display/{id}        → assets[key="zoom"].value  (jpg URL)
    download jpg → raw/bosses/ (scratch) → resize+webp → app assets

Output: projects/mplus_memory/app/src/assets/bosses/<dungeonSlug>__<bossSlug>.webp

The `<bossSlug>` MUST use the SAME slug rule as build-content.mjs `slugify()`
(lowercase, non-alphanumeric runs → "-", trim) — that shared contract is how the
app's `cue.artKey` finds the file. Keep the two in sync.

Usage:
    uv run python -m wowkb.bossart            # all dungeons
    uv run python -m wowkb.bossart --only skyreach pit-of-saron
    uv run python -m wowkb.bossart --width 480 --quality 80
"""

import argparse
import re
import sys
from pathlib import Path

import requests
from PIL import Image

from ._common import RAW, ROOT
from .blizzard import get

MPLUS_DIR = ROOT / "knowledge" / "endgame" / "mythic-plus"
ASSETS_DIR = ROOT / "projects" / "mplus_memory" / "app" / "src" / "assets" / "bosses"

# `### <name> <!-- enc:NNN -->`
HEADING_RE = re.compile(r"^###\s+(.+?)\s*<!--\s*enc:(\d+)\s*-->", re.MULTILINE)


def slugify(name: str) -> str:
    """Mirror build-content.mjs slugify(): lowercase, non-alnum runs → '-', trim."""
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def clean_boss_name(heading: str) -> str:
    """Mirror cleanBossName(): drop a trailing legacy provenance id paren if any."""
    return re.sub(r"\s*\((?:[a-z][\w-]*\s+)?\d+\)\s*$", "", heading, flags=re.I).strip()


def parse_bosses(md_path: Path):
    """Yield (boss_name, enc_id) for each boss heading in a dungeon file."""
    text = md_path.read_text(encoding="utf-8")
    for m in HEADING_RE.finditer(text):
        yield clean_boss_name(m.group(1)), int(m.group(2))


def display_id_for(enc: int, boss_name: str) -> int | None:
    """journal-encounter → a creature display id (match the boss for councils)."""
    data = get(f"/data/wow/journal-encounter/{enc}", "static")
    creatures = data.get("creatures") or []
    if not creatures:
        return None
    # Prefer a creature whose name the boss heading contains (or vice-versa);
    # councils / duos fall back to the first creature.
    chosen = creatures[0]
    bl = boss_name.lower()
    for c in creatures:
        cn = (c.get("name") or "").lower()
        if cn and (cn in bl or bl in cn):
            chosen = c
            break
    display = chosen.get("creature_display") or {}
    return display.get("id")


def zoom_url_for(display_id: int) -> str | None:
    """media/creature-display → the 'zoom' asset URL (full-size render)."""
    media = get(f"/data/wow/media/creature-display/{display_id}", "static")
    for asset in media.get("assets") or []:
        if asset.get("key") == "zoom":
            return asset.get("value")
    # Fall back to the first asset if there's no explicit zoom.
    assets = media.get("assets") or []
    return assets[0].get("value") if assets else None


def process(jpg_bytes: bytes, out_path: Path, width: int, quality: int) -> None:
    """Resize to a consistent width and encode webp."""
    raw_dir = RAW / "bosses"
    raw_dir.mkdir(parents=True, exist_ok=True)
    cache = raw_dir / (out_path.stem + ".jpg")
    cache.write_bytes(jpg_bytes)

    img = Image.open(cache).convert("RGB")
    if img.width > width:
        height = round(img.height * width / img.width)
        img = img.resize((width, height), Image.LANCZOS)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(out_path, "WEBP", quality=quality, method=6)


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.bossart", description=__doc__)
    p.add_argument("--only", nargs="*", help="dungeon slugs to fetch (default: all)")
    p.add_argument("--width", type=int, default=480, help="output width in px")
    p.add_argument("--quality", type=int, default=80, help="webp quality 1-100")
    p.add_argument("--force", action="store_true", help="re-fetch even if the webp exists")
    args = p.parse_args()

    files = sorted(MPLUS_DIR.glob("*.md"))
    files = [f for f in files if f.stem != "season-1-overview"]
    if args.only:
        wanted = set(args.only)
        files = [f for f in files if f.stem in wanted]

    ok, skipped, failed = 0, 0, 0
    for md in files:
        dungeon_slug = md.stem
        for boss_name, enc in parse_bosses(md):
            key = f"{dungeon_slug}__{slugify(boss_name)}"
            out_path = ASSETS_DIR / f"{key}.webp"
            if out_path.exists() and not args.force:
                print(f"  · {key} (exists, skip)")
                skipped += 1
                continue
            try:
                display_id = display_id_for(enc, boss_name)
                if not display_id:
                    print(f"  ✗ {key}: no creature display for enc {enc}", file=sys.stderr)
                    failed += 1
                    continue
                url = zoom_url_for(display_id)
                if not url:
                    print(f"  ✗ {key}: no render asset for display {display_id}", file=sys.stderr)
                    failed += 1
                    continue
                resp = requests.get(url, timeout=30)
                resp.raise_for_status()
                process(resp.content, out_path, args.width, args.quality)
                print(f"  ✓ {key}  (enc {enc} · display {display_id})")
                ok += 1
            except Exception as e:  # noqa: BLE001 — report and continue the batch
                print(f"  ✗ {key}: {e}", file=sys.stderr)
                failed += 1

    print(f"\n  bossart: {ok} written · {skipped} skipped · {failed} failed → {ASSETS_DIR}")
    if failed:
        sys.exit(1)


if __name__ == "__main__":
    main()
