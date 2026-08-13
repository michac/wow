"""Extract Blizzard UI art (atlas members, flipbook sheets, spell icons) as image files.

This is the asset door for the Combat Assist Plus **render shelf**
(`projects/combat-assist/specs/render-shelf.md`): it turns a Blizzard atlas name
into real pixels, so a design artifact can render the *actual* client art instead
of a hand-drawn approximation, and so the numbers a renderer needs (grid, cell
size, host scale) come from data rather than from a guess.

The pipeline, and why each step exists:

    raw/wago/UiTextureAtlasMember*.csv   member name  → UiTextureAtlasID + committed rect
    https://wago.tools/atlas/{id}        atlas id     → sheet FileDataID + sheet dimensions
    https://wago.tools/api/casc/{fdid}   FileDataID   → raw BLP bytes  (documented public endpoint)
    _decode_blp2()                       BLP2         → RGBA           (Pillow can't do encoding 3)
    crop(committed rect)                 sheet        → the member's own image

⚠ Two things bite here, both measured:

* `wago.tools/api/casc` **requires a browser User-Agent.** With a bot UA the
  request hangs and returns nothing at all — not a 403, just silence.
* Pillow reads BLP headers but raises `Unknown BLP encoding 3` on the
  uncompressed-BGRA form Blizzard uses for UI sheets. Mip 0 of those is plain
  BGRA at `mipOffset[0]`, so we decode it ourselves and let Pillow keep the
  palette/DXT forms it does support.

Usage:
    uv run python -m wowkb.uiart find flipbook
    uv run python -m wowkb.uiart find proc-loop --json
    uv run python -m wowkb.uiart atlas ui-hud-actionbar-proc-loop-flipbook --grid 6x5
    uv run python -m wowkb.uiart atlas ui-cooldownmanager-alert-flipbook --webp --data-uri
    uv run python -m wowkb.uiart icon 191427 198013 --size 56 --data-uri
    uv run python -m wowkb.uiart icon fdid:1247262            # spells with no resolvable slug
    uv run python -m wowkb.uiart manifest

`atlas_image()` and `icon_image()` are the library door — they return pixels and never
write files or exit, so `wowkb.capart` can assemble an artifact from the same pipeline
the CLI prints.
"""

import argparse
import base64
import csv
import html
import io
import json
import re
import struct
import sys
from pathlib import Path

import requests
from PIL import Image

from ._common import RAW, ROOT

OUT = RAW / "uiart"
BLP_CACHE = OUT / "blp"
MANIFEST = OUT / "manifest.json"

# wago.tools/api/casc silently stalls on a non-browser UA — this is not politeness, it is required.
_BROWSER_UA = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    )
}

ICON_RENDER = "https://render.worldofwarcraft.com/us/icons/{size}/{slug}.jpg"
ENRICHMENT = RAW / "spell-enrichment.json"


# --------------------------------------------------------------------------- atlas members


def _member_csv() -> Path:
    hits = sorted(RAW.glob("wago/UiTextureAtlasMember*.csv"))
    if not hits:
        sys.exit(
            "error: no raw/wago/UiTextureAtlasMember*.csv — run:\n"
            "  uv run python -m wowkb.wago UiTextureAtlasMember"
        )
    return hits[-1]


def _members() -> list[dict]:
    with _member_csv().open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def find_members(needle: str) -> list[dict]:
    """Atlas members whose CommittedName contains `needle` (case-insensitive)."""
    low = needle.lower()
    return [m for m in _members() if low in m["CommittedName"].lower()]


def resolve_member(name: str) -> dict:
    """Exact CommittedName match, else a unique substring match."""
    low = name.lower()
    rows = _members()
    for m in rows:
        if m["CommittedName"].lower() == low:
            return m
    hits = [m for m in rows if low in m["CommittedName"].lower()]
    if not hits:
        sys.exit(f"error: no atlas member matching {name!r} (try: wowkb.uiart find {name})")
    if len(hits) > 1:
        names = ", ".join(sorted(h["CommittedName"] for h in hits)[:8])
        sys.exit(f"error: {name!r} is ambiguous — {len(hits)} matches: {names} …")
    return hits[0]


def sheet_for_atlas(atlas_id: int) -> dict:
    """UiTextureAtlasID → {FileDataID, AtlasWidth, AtlasHeight} via the wago atlas page."""
    resp = requests.get(f"https://wago.tools/atlas/{atlas_id}", headers=_BROWSER_UA, timeout=60)
    resp.raise_for_status()
    m = re.search(r'data-page="([^"]+)"', resp.text)
    if not m:
        sys.exit(f"error: wago.tools/atlas/{atlas_id} did not carry a page payload")
    atlas = json.loads(html.unescape(m.group(1)))["props"].get("atlas")
    if not atlas:
        sys.exit(f"error: wago.tools has no atlas {atlas_id}")
    return atlas


# --------------------------------------------------------------------------- BLP


def fetch_blp(fdid: int, refresh: bool = False) -> bytes:
    """CASC file bytes for a FileDataID, cached under raw/uiart/blp/."""
    cached = BLP_CACHE / f"{fdid}.blp"
    if cached.exists() and not refresh:
        return cached.read_bytes()
    resp = requests.get(
        f"https://wago.tools/api/casc/{fdid}", headers=_BROWSER_UA, timeout=180
    )
    resp.raise_for_status()
    cached.parent.mkdir(parents=True, exist_ok=True)
    cached.write_bytes(resp.content)
    return resp.content


def _decode_blp2(data: bytes) -> Image.Image:
    """Uncompressed-BGRA BLP2 (encoding 3) → RGBA. Pillow handles the other encodings."""
    if data[:4] != b"BLP2":
        raise ValueError("not a BLP2 file")
    encoding = data[8]
    width, height = struct.unpack("<II", data[12:20])
    offsets = struct.unpack("<16I", data[20:84])
    sizes = struct.unpack("<16I", data[84:148])
    if encoding != 3:
        raise ValueError(f"BLP2 encoding {encoding} is not the uncompressed-BGRA form")
    raw = data[offsets[0] : offsets[0] + sizes[0]]
    expected = width * height * 4
    if len(raw) != expected:
        raise ValueError(f"mip 0 is {len(raw)} bytes, expected {expected}")
    img = Image.frombytes("RGBA", (width, height), raw)
    b, g, r, a = img.split()
    return Image.merge("RGBA", (r, g, b, a))


def blp_to_image(data: bytes) -> Image.Image:
    """BLP bytes → RGBA image, whichever encoding it is."""
    try:
        return Image.open(io.BytesIO(data)).convert("RGBA")
    except Exception:
        return _decode_blp2(data)


# --------------------------------------------------------------------------- outputs


def tintability(img: Image.Image) -> dict:
    """Mean HSV saturation over the visible pixels — i.e. can SetVertexColor recolor this?

    `SetVertexColor` MULTIPLIES, so art with a baked hue can only ever be darkened
    toward that hue: a gold ring cannot be made blue. Art whose RGB is near-neutral
    (shape carried in the alpha channel) tints to any hue at full strength. This is
    the measurement that decides whether an atlas can carry a multi-hue tier ladder,
    and it is why Blizzard can ship five tints of its own CDM alert.
    """
    import colorsys

    px = [p for p in img.convert("RGBA").getdata() if p[3] > 40]
    if not px:
        return {"mean_saturation": None, "tintable": None, "sampled": 0}
    sats = [colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[1] for r, g, b, _ in px]
    mean = sum(sats) / len(sats)
    return {"mean_saturation": round(mean, 3), "tintable": mean < 0.15, "sampled": len(px)}


def _encode(img: Image.Image, path: Path, webp: bool, quality: int) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if webp:
        path = path.with_suffix(".webp")
        img.save(path, "WEBP", quality=quality, method=6)
    else:
        img.save(path, "PNG", optimize=True)
    return path


def _data_uri(path: Path) -> str:
    mime = {"png": "image/png", "webp": "image/webp", "jpg": "image/jpeg"}[
        path.suffix.lstrip(".").replace("jpeg", "jpg")
    ]
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def _record(entry: dict) -> None:
    """Append/replace an entry in raw/uiart/manifest.json, keyed by name."""
    data = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    data[entry["name"]] = entry
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    MANIFEST.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


# --------------------------------------------------------------------------- library API
#
# These two are the door for other tools (`wowkb.capart`): they return pixels and
# metadata, and they never write files or exit. The `cmd_*` functions below are thin
# CLI wrappers over them, so there is exactly one copy of each pipeline.


def atlas_image(name: str, refresh: bool = False) -> tuple[Image.Image, dict]:
    """Atlas member name → (its cropped image, a metadata entry).

    The entry carries everything a renderer needs to reproduce the art — the sheet's
    FileDataID, the committed rect, the crop size and the tintability measure — but
    NOT a grid: the grid is a declaration about how the art is meant to be walked, so
    it belongs to the caller (the render shelf's token block), not to extraction.
    """
    member = resolve_member(name)
    committed = member["CommittedName"]
    atlas_id = int(member["UiTextureAtlasID"])
    left, right = int(member["CommittedLeft"]), int(member["CommittedRight"])
    top, bottom = int(member["CommittedTop"]), int(member["CommittedBottom"])

    sheet = sheet_for_atlas(atlas_id)
    fdid = int(sheet["FileDataID"])
    crop = blp_to_image(fetch_blp(fdid, refresh=refresh)).crop((left, top, right, bottom))

    entry = {
        "name": committed,
        "atlas_id": atlas_id,
        "file_data_id": fdid,
        "rect": {"left": left, "right": right, "top": top, "bottom": bottom},
        "size": list(crop.size),
        "sheet_size": [sheet.get("AtlasWidth"), sheet.get("AtlasHeight")],
        "tint": tintability(crop),
    }
    return crop, entry


def icon_image(spell: str | int, size: int = 56) -> tuple[Image.Image, str]:
    """Spell id / icon slug → (icon image, the slug or `fdid:<n>` it resolved through).

    Two routes, in order. The render endpoint keyed by icon *slug* is the good one —
    it is the same art the client shows, at the client's size. But a slug only exists
    if some catalog knows the spell, and several of the demon-form override ids do not
    resolve: `raw/spell-enrichment.json` is a talent cache and the Blizzard media
    endpoint 404s on override spells. For those the caller passes the icon's
    **FileDataID** as `fdid:<n>`, which goes through CASC + BLP exactly like an atlas
    sheet. No new network path — `fetch_blp` already does it.
    """
    token = str(spell)
    if token.startswith("fdid:"):
        fdid = int(token.split(":", 1)[1])
        img = blp_to_image(fetch_blp(fdid)).convert("RGB")
        if img.size != (size, size):
            img = img.resize((size, size), Image.LANCZOS)
        return img, token

    slug = token if not token.isdigit() else _icon_slug(int(token))
    if not slug:
        raise LookupError(f"no icon slug for {spell!r} — pass fdid:<FileDataID> instead")
    resp = requests.get(ICON_RENDER.format(size=size, slug=slug), headers=_BROWSER_UA, timeout=60)
    if resp.status_code != 200:
        raise LookupError(f"{spell} ({slug}): icon render HTTP {resp.status_code}")
    return Image.open(io.BytesIO(resp.content)).convert("RGB"), slug


# --------------------------------------------------------------------------- commands


def cmd_find(args) -> None:
    hits = find_members(args.needle)
    if args.json:
        print(json.dumps(hits, indent=2))
        return
    if not hits:
        print(f"no atlas member matching {args.needle!r}")
        return
    for m in sorted(hits, key=lambda m: m["CommittedName"]):
        w = int(m["CommittedRight"]) - int(m["CommittedLeft"])
        h = int(m["CommittedBottom"]) - int(m["CommittedTop"])
        print(f"{m['CommittedName']:<58} atlas {m['UiTextureAtlasID']:>6}  {w}x{h}")
    print(f"\n{len(hits)} match(es)")


def cmd_atlas(args) -> None:
    crop, entry = atlas_image(args.name, refresh=args.refresh)
    name = entry["name"]
    rect, tint = entry["rect"], entry["tint"]

    out = _encode(crop, OUT / f"{name}.png", args.webp, args.quality)
    entry["file"] = str(out.relative_to(ROOT))

    print(f"{name}")
    print(f"  atlas {entry['atlas_id']} · sheet FileDataID {entry['file_data_id']} "
          f"({entry['sheet_size'][0]}x{entry['sheet_size'][1]})")
    print(f"  rect  L{rect['left']} R{rect['right']} T{rect['top']} B{rect['bottom']}"
          f"  →  {crop.size[0]}x{crop.size[1]}")
    verdict = (
        "NEUTRAL — SetVertexColor reaches any hue"
        if tint["tintable"]
        else "BAKED HUE — multiply cannot reach another hue (desaturate first, or use neutral art)"
    )
    print(f"  tint  mean saturation {tint['mean_saturation']} · {verdict}")
    if args.grid:
        rows, cols = (int(v) for v in args.grid.lower().split("x"))
        cw, ch = crop.size[0] / cols, crop.size[1] / rows
        entry["grid"] = {"rows": rows, "cols": cols, "frames": rows * cols,
                         "cell": [round(cw, 2), round(ch, 2)]}
        print(f"  grid  {rows}x{cols} = {rows * cols} frames · cell {cw:.2f}x{ch:.2f}")
        print(f"  css   background-size: {cols * 100}% {rows * 100}%; "
              f"animation: flip <dur> steps({rows * cols}) infinite;")
    print(f"  wrote {out.relative_to(ROOT)}")

    if args.data_uri:
        uri = _data_uri(out)
        uri_path = out.with_suffix(out.suffix + ".datauri.txt")
        uri_path.write_text(uri)
        entry["data_uri_bytes"] = len(uri)
        print(f"  data URI {len(uri) / 1024:.1f} KB → {uri_path.relative_to(ROOT)}")

    _record(entry)


def _icon_slug(spell_id: int) -> str | None:
    """Icon slug for a spell id, from the cached enrichment or the media endpoint."""
    if ENRICHMENT.exists():
        data = json.loads(ENRICHMENT.read_text())
        entry = data.get(str(spell_id)) or data.get(spell_id)
        if entry and entry.get("icon"):
            return entry["icon"].rstrip("/").rsplit("/", 1)[-1].removesuffix(".jpg")
    from .blizzard import get  # local import: needs Blizzard credentials

    try:
        payload = get(f"/data/wow/media/spell/{spell_id}", "static")
    except requests.HTTPError as exc:
        # Not every spell id has a media entry (passives, damage-effect ids). One miss
        # must not abort the batch.
        print(f"{spell_id}: media lookup failed ({exc.response.status_code})", file=sys.stderr)
        return None
    for asset in payload.get("assets", []):
        if asset.get("key") == "icon":
            return asset["value"].rstrip("/").rsplit("/", 1)[-1].removesuffix(".jpg")
    return None


def cmd_icon(args) -> None:
    for spell in args.spells:
        try:
            img, slug = icon_image(spell, args.size)
        except LookupError as exc:
            print(exc, file=sys.stderr)
            continue
        stem = slug.replace("fdid:", "")
        out = _encode(img, OUT / "icons" / f"{stem}.png", args.webp, args.quality)
        line = f"{spell:>8}  {slug:<44} {out.relative_to(ROOT)}"
        if args.data_uri:
            uri = _data_uri(out)
            out.with_suffix(out.suffix + ".datauri.txt").write_text(uri)
            line += f"  ({len(uri) / 1024:.1f} KB b64)"
        print(line)


def cmd_manifest(args) -> None:
    if not MANIFEST.exists():
        print("no assets extracted yet — run: wowkb.uiart atlas <member-name>")
        return
    data = json.loads(MANIFEST.read_text())
    for name, e in sorted(data.items()):
        grid = e.get("grid")
        suffix = f" · {grid['rows']}x{grid['cols']}/{grid['frames']}f" if grid else ""
        tint = e.get("tint") or {}
        mark = "" if tint.get("tintable") is None else (
            f" · {'neutral' if tint['tintable'] else 'baked'} sat {tint['mean_saturation']}"
        )
        print(f"{name:<52} fdid {e['file_data_id']:<9} {e['size'][0]}x{e['size'][1]}{suffix}{mark}")
    print(f"\n{len(data)} asset(s) · {MANIFEST.relative_to(ROOT)}")


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.uiart", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    f = sub.add_parser("find", help="search atlas member names")
    f.add_argument("needle")
    f.add_argument("--json", action="store_true")
    f.set_defaults(func=cmd_find)

    a = sub.add_parser("atlas", help="extract one atlas member as an image")
    a.add_argument("name", help="CommittedName, e.g. ui-hud-actionbar-proc-loop-flipbook")
    a.add_argument("--grid", help="flipbook grid as ROWSxCOLS, e.g. 6x5 — prints the CSS recipe")
    a.add_argument("--webp", action="store_true", help="encode WebP instead of PNG")
    a.add_argument("--quality", type=int, default=90)
    a.add_argument("--data-uri", action="store_true", help="also write a base64 data: URI")
    a.add_argument("--refresh", action="store_true", help="re-download the sheet")
    a.set_defaults(func=cmd_atlas)

    i = sub.add_parser("icon", help="fetch spell icons by id or slug")
    i.add_argument("spells", nargs="+",
                   help="spell ids, icon slugs, and/or fdid:<FileDataID> for spells with no slug")
    i.add_argument("--size", type=int, default=56, choices=[56])
    i.add_argument("--webp", action="store_true")
    i.add_argument("--quality", type=int, default=90)
    i.add_argument("--data-uri", action="store_true")
    i.set_defaults(func=cmd_icon)

    m = sub.add_parser("manifest", help="list extracted assets")
    m.set_defaults(func=cmd_manifest)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
