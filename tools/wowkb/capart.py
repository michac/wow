"""Generate the Combat Assist Plus design artifacts from the docs that own them.

This tool assembles; it never decides. **It holds no color, no rate and no size.** Every
number it draws with is lifted out of `projects/combat-assist/specs/render-shelf.md`
Part 6 — the `render-tokens` JSON block — and every ability, lane and verdict comes from
`specs/havoc/catalog.md` and `specs/havoc/scenarios.md`. Change the look by editing the
shelf and rebuilding; change the walk by editing the scenario doc and re-importing. If a
number appears in this file, that is a bug.

Why it exists. The old Havoc stepper was a stylized diagram: two-letter abbreviations on
CSS gradients, and cue treatments invented on the spot with no relationship to anything
the client can draw. It validated the *logic* of the elimination walk and nothing about
the *look*, which left the eventual `Catalogs/Havoc.lua` a fresh design exercise rather
than a transcription. The artifact this builds is a **reproduction**: real Blizzard icon
art at the client's own icon size, real extracted flipbook sheets at their real frame
counts and durations, and cap's treatments composited the way the client composites
them.

The fidelity guard is the point, not a nicety:

* `SetVertexColor` **multiplies**, so a tint is `background-color` +
  `background-blend-mode: multiply`, never `filter: hue-rotate`. A hue rotation looks
  great and can recolor art the client **cannot** recolor — which is exactly the lie that
  makes a preview worthless.
* A primitive asking for `tint: "lane"` on art whose measured saturation says it carries a
  baked hue is a **hard error**, naming the measurement.
* `tint: "desaturate+lane"` builds but is stamped ⚠ *open*, because desaturate-then-tint
  is unverified in client.
* A flipbook whose `rows × cols` disagrees with its frame count, or whose cells stop being
  square, is a **warning** — that sheet animates wrong, and you want to see it animate wrong
  rather than be denied the page that shows you.

Only two things stop a build: the tint guard above, and a verdict or ability the vocabulary
does not know (which would render *nothing*, silently). Everything else — the base64 budget,
the literal-hex scan, the flipbook geometry — is a `check` concern or a warning, because
**nothing may block a rebuild you want to look at**. `check` is the CI-shaped gate; `build`
is the loop.

Usage:
    uv run python -m wowkb.capart tokens                # resolved tokens + the CSS block
    uv run python -m wowkb.capart assets                # per-asset byte table vs the budget
    uv run python -m wowkb.capart import scenarios      # seed the sidecar from scenarios.md
    uv run python -m wowkb.capart build havoc           # write the artifact
    uv run python -m wowkb.capart check havoc           # doc↔sidecar, staleness, strict CSS

    uv run python -m wowkb.serve projects/combat-assist/artifacts \\
        --watch projects/combat-assist/specs \\
        --on-change "python -m wowkb.capart build havoc"   # edit → rebuild → reload
"""

import argparse
import base64
import hashlib
import html as htmllib
import io
import json
import re
import sys
from datetime import date
from pathlib import Path

from PIL import Image

from . import uiart
from ._common import ROOT

PROJECT = ROOT / "projects" / "combat-assist"
SPECS = PROJECT / "specs"
SHELF = SPECS / "render-shelf.md"
ARTIFACTS = PROJECT / "artifacts"
TEMPLATE = ARTIFACTS / "template"
SIDECARS = ARTIFACTS / "data"
CACHE = uiart.OUT / "capart-cache"

BUILT_MARK = "<!-- capart built: {date} -->"
BUILT_RE = re.compile(r"<!-- capart built: (\d{4}-\d{2}-\d{2}) -->")

SPECS_BUILT = {
    "havoc": {
        "catalog": SPECS / "havoc" / "catalog.md",
        "scenarios": SPECS / "havoc" / "scenarios.md",
        "sidecar": SIDECARS / "havoc-scenarios.json",
        "out": ARTIFACTS / "havoc-stepper.html",
        # One ability per lane, so the primitives gallery can draw a lane swatch on real
        # art even when no scenario happens to exercise that lane.
        "lane_sample": {
            "COOLDOWN": "Metamorphosis",
            "ROTATION": "Blade Dance",
            "FALLBACK": "Fel Rush",
        },
    }
}

# Icon art for a handful of spells has no resolvable slug: `raw/spell-enrichment.json` is a
# talent cache (5 of our 15) and the Blizzard media endpoint 404s on demon-form override
# ids. For those the icon's FileDataID goes through CASC + BLP exactly like an atlas sheet.
# This is asset plumbing — a file id, not a design choice. Every value is read off
# `raw/wago/SpellMisc-*.csv` (column `SpellIconFileDataID`, keyed by `SpellID`), which is the
# same table the client reads, so these are looked up rather than guessed:
#   awk -F, 'NR==1{for(i=1;i<=NF;i++)h[$i]=i} $h["SpellID"]==452497 {print $h["SpellIconFileDataID"]}'
ICON_FDID = {
    191427: 1247262,   # Metamorphosis
    210152: 1309099,   # Death Sweep
    344859: 135561,    # Demon's Bite
    201427: 1303275,   # Annihilation     (Chaos Strike's demon-form override)
    452497: 136149,    # Abyssal Gaze     (Eye Beam's demon-form override)
    452487: 135794,    # Consuming Fire   (Immolation Aura's demon-form override)
}

CHROME_START = "/* ===== CHROME START"
CHROME_END = "/* ===== CHROME END ====="
HEX_RE = re.compile(r"#[0-9a-fA-F]{3,8}\b")


def _die(msg: str) -> None:
    sys.exit(f"error: {msg}")


def _warn(msg: str) -> None:
    print(f"warning: {msg}", file=sys.stderr)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


# --------------------------------------------------------------------------- the shelf


def load_tokens() -> dict:
    """The `render-tokens` block out of render-shelf.md Part 6 — the whole style."""
    text = SHELF.read_text(encoding="utf-8")
    m = re.search(r"<!--\s*render-tokens v1\s*-->\s*```json\n(.*?)\n```", text, re.S)
    if not m:
        _die(f"no `<!-- render-tokens v1 -->` JSON block in {SHELF.relative_to(ROOT)}")
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError as exc:
        _die(f"render-tokens block is not valid JSON: {exc}")


# --------------------------------------------------------------------------- the roster


ROSTER_RE = re.compile(
    r"^\|\s*`(?P<key>[a-z_]+)`\s*\|\s*(?P<name>[^|]+?)\s*\|\s*`(?P<spell>\d+)`\s*\|"
    r"\s*(?P<override>[^|]*?)\s*\|\s*(?P<lane>[A-Z]+|—|-)\s*\|",
    re.M,
)
OVERRIDE_RE = re.compile(r"^(?P<name>[^⚠`]+?)\s*⚠\s*`(?P<spell>\d+)`")


def load_roster(catalog: Path) -> dict:
    """catalog.md's *Bound abilities* table → {display name: {key, spell, lane}}.

    Both the base name and the demon-form override name are keys, because a scenario row
    writes whichever name the client would *show* (R7 resolves the live `overrideSpellID`;
    cap authors none of it). Parsing the catalog rather than restating it is what keeps
    spell ids, lanes and override names from existing in two places.
    """
    text = catalog.read_text(encoding="utf-8")
    out: dict[str, dict] = {}
    for m in ROSTER_RE.finditer(text):
        lane = m.group("lane")
        if lane in {"—", "-"}:
            continue  # a row with no lane is an open fact, not a drawable button
        key, base_id = m.group("key"), int(m.group("spell"))
        out[m.group("name")] = {"key": key, "spell": base_id, "lane": lane}
        ov = OVERRIDE_RE.match(m.group("override"))
        if ov:
            out[ov.group("name").strip()] = {
                "key": key,
                "spell": int(ov.group("spell")),
                "lane": lane,
                "override_of": m.group("name"),
            }
    if not out:
        _die(f"no bound-abilities table rows found in {catalog.relative_to(ROOT)}")
    return out


# --------------------------------------------------------------------------- scraping


ENTRY_RE = re.compile(r"^(?P<name>.+?)\s+`(?P<verdict>[a-z-]+)`(?P<ann>.*)$")
GROUP_RE = re.compile(r"\{(?P<kind>dots|cues):\s*(?P<body>[^}]*)\}")


def _inline(md: str) -> str:
    """The small subset of markdown the docs use, as HTML. Escape first, then mark up."""
    out = htmllib.escape(md)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", out)
    out = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\*)", r"<em>\1</em>", out)
    return out


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def parse_row(raw: str) -> list[dict]:
    """The `- **CDM row.**` bullet's fixed grammar → an ordered list of row entries."""
    row = _flat(raw).rstrip(".")
    entries = []
    for chunk in row.split(" · "):
        chunk = chunk.strip()
        if not chunk:
            continue
        groups = {m.group("kind"): m.group("body") for m in GROUP_RE.finditer(chunk)}
        bare = GROUP_RE.sub("", chunk).strip()
        m = ENTRY_RE.match(bare)
        if not m:
            _die(f"CDM row entry does not parse: {chunk!r}\n"
                 "       expected: <Ability> `<verdict>` [{dots: …}] [{cues: …}]")
        entry = {"name": m.group("name").strip(), "verdict": m.group("verdict")}
        if "dots" in groups:
            dots = []
            for d in groups["dots"].split(","):
                d = d.strip()
                if not d:
                    continue
                label, _, state = d.rpartition(" ")
                if state not in {"go", "wait"}:
                    _die(f"dot state must be `go` or `wait`, got {d!r}")
                dots.append({"label": label.strip(), "state": state})
            entry["dots"] = dots
        if "cues" in groups:
            entry["cues"] = [c.strip() for c in groups["cues"].split(",") if c.strip()]
        entries.append(entry)
    return entries


def _step_names(text: str, row_names: list[str]) -> list[str]:
    """The abilities a numbered walk step is about, from its leading bold run."""
    m = re.match(r"\s*\*\*(?P<bold>[^*]+)\*\*", text)
    if not m:
        return []
    bold = m.group("bold")
    if "…" in bold or "..." in bold:
        ends = [p.strip() for p in re.split(r"…|\.\.\.", bold) if p.strip()]
        if len(ends) == 2 and ends[0] in row_names and ends[1] in row_names:
            i, j = row_names.index(ends[0]), row_names.index(ends[1])
            return row_names[i:j + 1]
        return [e for e in ends if e in row_names]
    return [p.strip() for p in bold.split(" / ") if p.strip() in row_names]


def parse_walk(raw: str, row_names: list[str]) -> list[dict]:
    """The `- **Walk.**` bullet → ordered steps, each knowing which icons it is about.

    A step that names nothing explicitly ("Everything above … is on cooldown") inherits
    the span between the previous step's furthest icon and the next step's first, so the
    stepper still advances through the row rather than stalling at zero.
    """
    body = raw.strip()
    if not body:
        # The AoE variants are deltas on a single-target scenario and carry no walk of
        # their own. No walk means no stepping — the row simply shows whole.
        return []
    items = re.split(r"(?m)^\s*\d+\.\s+", "\n" + body)
    items = [i for i in (x.strip() for x in items) if i]
    if len(items) <= 1:
        # An unnumbered walk is one step covering the whole row (ST-10's shape).
        return [{"names": list(row_names), "html": _inline(_flat(body))}]

    steps = [{"names": _step_names(t, row_names), "raw": _flat(t)} for t in items]

    furthest = 0
    for idx, step in enumerate(steps):
        if step["names"]:
            furthest = max(furthest, max(row_names.index(n) for n in step["names"]) + 1)
            continue
        nxt = next((s for s in steps[idx + 1:] if s["names"]), None)
        stop = min(row_names.index(n) for n in nxt["names"]) if nxt else len(row_names)
        step["names"] = row_names[furthest:stop]
        if step["names"]:
            furthest = stop
    return [{"names": s["names"], "html": _inline(s["raw"])} for s in steps]


HEADING_RE = re.compile(r"^###\s+(?P<id>(?:ST|AoE)-\d+)\s+·\s+(?P<title>.+?)\s*$", re.M)


def scrape_scenarios(path: Path) -> list[dict]:
    """scenarios.md → the ordered scenario list. The doc leads; this reads it."""
    text = path.read_text(encoding="utf-8")
    marks = list(HEADING_RE.finditer(text))
    if not marks:
        _die(f"no `### ST-n · …` scenario headings in {path.relative_to(ROOT)}")

    out = []
    for i, m in enumerate(marks):
        body = text[m.end(): marks[i + 1].start() if i + 1 < len(marks) else len(text)]
        bullets = {}
        order = []
        for part in re.split(r"(?m)^- \*\*", "\n" + body)[1:]:
            label, _, rest = part.partition("**")
            label = label.split("(")[0].strip().rstrip(".")
            bullets[label] = rest.strip()
            order.append(label)

        if "CDM row" not in bullets:
            _die(f"{m.group('id')} has no `- **CDM row.**` bullet — the artifact cannot render it")
        row = parse_row(bullets["CDM row"])
        row_names = [e["name"] for e in row]

        extras = [
            {"label": lbl, "html": _inline(_flat(bullets[lbl]))}
            for lbl in order
            if lbl not in {"State", "CDM row", "Walk"}
        ]
        out.append({
            "id": m.group("id"),
            "title": m.group("title"),
            "state": _inline(_flat(bullets.get("State", ""))),
            "row": row,
            "steps": parse_walk(bullets.get("Walk", ""), row_names),
            "extras": extras,
        })
    return out


def validate_lab_isolation(tokens: dict) -> None:
    """Part 7's rule 1: the lab is unreachable from the declared style.

    The lab exists so an idea can be *drawn* without being *adopted*, and the only thing that
    keeps that true is that nothing a scenario can reach may name it. A `cues` entry quietly
    pointing at a lab badge would make an experiment load-bearing without anyone deciding to
    promote it — which is exactly the drift Part 7 is written to prevent. So: mechanical check,
    every build.
    """
    lab = tokens.get("lab")
    if not lab:
        return
    keys = {k for k in lab if not k.startswith("_")}
    blob = json.dumps({"verdicts": tokens["verdicts"], "cues": tokens["cues"]})
    for k in sorted(keys):
        if f'"{k}"' in blob:
            _die(f"tokens.verdicts/cues names lab entry {k!r} — the lab has no authority and "
                 "nothing a scenario can reach may reference it (render-shelf.md Part 7, rule 1).\n"
                 "       Promote it by MOVING it into Parts 1-6, or rename the colliding key.")
    for name, entry in ((n, e) for n, e in lab.items() if not n.startswith("_")):
        if isinstance(entry, dict) and not entry.get("asks"):
            _warn(f"lab entry {name!r} has no `asks` — Part 7 says an entry that cannot say what "
                  "it is asking is decoration")


def validate(scenarios: list[dict], tokens: dict, roster: dict) -> None:
    validate_lab_isolation(tokens)
    verdicts = set(tokens["verdicts"])
    cues = set(tokens["cues"])
    for sc in scenarios:
        for e in sc["row"]:
            if e["verdict"] not in verdicts:
                _die(f"{sc['id']}: verdict {e['verdict']!r} is not in the closed vocabulary "
                     f"({', '.join(sorted(verdicts))})")
            if e["name"] not in roster:
                _die(f"{sc['id']}: {e['name']!r} is not in catalog.md's bound-abilities table")
            for c in e.get("cues", []):
                if c not in cues:
                    _die(f"{sc['id']}: cue {c!r} is not declared in render-shelf.md tokens.cues")


# --------------------------------------------------------------------------- assets


def _data_uri(img: Image.Image, tokens: dict) -> tuple[str, int]:
    buf = io.BytesIO()
    fmt = tokens["assets"].get("encode", "webp")
    if fmt == "webp":
        img.save(buf, "WEBP", quality=tokens["assets"].get("quality", 90), method=6)
        mime = "image/webp"
    else:
        img.save(buf, "PNG", optimize=True)
        mime = "image/png"
    uri = f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    return uri, len(uri)


def _cached(key: str, produce) -> Image.Image:
    """Extracted art is cached as PNG so a rebuild is offline and byte-stable."""
    path = CACHE / f"{key}.png"
    if path.exists():
        return Image.open(path).copy()
    img = produce()
    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, "PNG", optimize=True)
    return img


def ring_assets(tokens: dict) -> dict:
    """Extract each declared ring, and refuse the ones that would render a lie."""
    out = {}
    for name, ring in tokens["rings"].items():
        atlas = ring["atlas"]
        entry_box: dict = {}

        def produce(atlas=atlas, box=entry_box):
            img, entry = uiart.atlas_image(atlas)
            box.update(entry)
            return img

        img = _cached(f"atlas-{atlas}", produce)
        if not entry_box:
            _, entry_box = uiart.atlas_image(atlas)

        rows, cols = ring["grid"]["rows"], ring["grid"]["cols"]
        if rows * cols != ring["frames"]:
            _warn(f"ring {name!r}: grid {rows}x{cols} is {rows * cols} cells but frames is "
                  f"{ring['frames']} — the flipbook will animate wrong")
        # Blizzard's committed rects are not integer multiples of their grid — the ants
        # sheet is 333x400 over 6x5, i.e. 66.60 x 66.67 cells — so "divides evenly" is the
        # wrong test and would reject real art. The error this actually needs to catch is a
        # SWAPPED or WRONG grid, which shows up as cells that stop being square: 5x6 on the
        # same sheet gives 55.5 x 80.0. Percentage background-sizing handles the fraction.
        w, h = img.size
        cw, ch = w / cols, h / rows
        if abs(cw - ch) / max(cw, ch) > 0.02:
            _warn(f"ring {name!r}: {atlas} crops to {w}x{h}; grid {rows}x{cols} gives "
                  f"{cw:.2f}x{ch:.2f} cells, which are not square — rows and cols are "
                  "probably swapped, and the flipbook will walk the sheet diagonally")

        tint = ring.get("tint", "none")
        sat = (entry_box.get("tint") or {}).get("mean_saturation")
        tintable = (entry_box.get("tint") or {}).get("tintable")
        open_flag = False
        if tint == "lane" and tintable is False:
            _die(
                f"ring {name!r} declares tint: \"lane\" but {atlas} measured mean saturation "
                f"{sat} — it carries a BAKED HUE.\n"
                "       SetVertexColor multiplies, so that art can only be darkened toward its "
                "own hue; a multi-hue lane ladder is not drawable on it, and a preview that "
                "showed one would be a lie.\n"
                "       Fix it one of three ways: pick neutral art (visualalert_ants_flipbook, "
                "saturation 0.00); declare tint: \"none\" and use the sheet for one lane; or "
                "declare tint: \"desaturate+lane\", which builds but stamps a visible ⚠ because "
                "desaturate-then-tint is unverified in client."
            )
        if tint == "desaturate+lane":
            open_flag = True

        uri, nbytes = _data_uri(img, tokens)
        out[name] = {
            "atlas": atlas, "uri": uri, "bytes": nbytes, "size": list(img.size),
            "file_data_id": entry_box.get("file_data_id"),
            "mean_saturation": sat, "tintable": tintable,
            "grid": ring["grid"], "frames": ring["frames"],
            "duration_s": ring["duration_s"], "host_scale": ring["host_scale"],
            "tint": tint, "open": open_flag,
        }
    return out


def lab_assets(tokens: dict) -> dict:
    """Part 7's sprite frames, from files we vendor rather than from CASC.

    Every frame is white with its shape in the alpha channel (measured saturation 0.000), which is
    what makes `SetVertexColor` able to take it to any lane hue at full strength — the same reason
    CDMProbe shipped Kenney's `star_07` instead of a Blizzard atlas. In CSS the faithful analogue
    of that multiply is `mask-image` + `background-color`: the alpha shapes it, the color IS the
    multiply result for white art. It is not a hue-rotate and it is not a lie.
    """
    lab = tokens.get("lab")
    if not lab:
        return {}
    root = ROOT / "projects" / "combat-assist" / lab["asset_root"]
    out: dict[str, dict] = {}
    for entry in lab.values():
        if not isinstance(entry, dict):
            continue
        for badge in entry.get("badges", {}).values():
            for frame in badge["frames"]:
                if frame in out:
                    continue
                path = root / f"{frame}.png"
                if not path.exists():
                    _die(f"lab frame {frame!r} not found at {path.relative_to(ROOT)} — "
                         f"tokens.lab.asset_root is {lab['asset_root']!r}")
                img = Image.open(path).convert("RGBA")
                buf = io.BytesIO()
                img.save(buf, "PNG", optimize=True)
                uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
                out[frame] = {"uri": uri, "bytes": len(uri), "size": list(img.size)}
    return out


def icon_assets(names: list[str], roster: dict, tokens: dict) -> dict:
    size = tokens["assets"]["icon_size"]
    out = {}
    for name in names:
        spell = roster[name]["spell"]

        def produce(spell=spell, name=name):
            try:
                img, _ = uiart.icon_image(spell, size)
                return img
            except LookupError:
                fdid = ICON_FDID.get(spell)
                if not fdid:
                    _die(f"no icon for {name} (spell {spell}) — no slug resolved and no "
                         f"FileDataID fallback registered in capart.ICON_FDID")
                img, _ = uiart.icon_image(f"fdid:{fdid}", size)
                return img

        img = _cached(f"icon-{spell}-{size}", produce)
        if img.size != (size, size):
            img = img.resize((size, size), Image.LANCZOS)
        uri, nbytes = _data_uri(img.convert("RGB"), tokens)
        out[name] = {"uri": uri, "bytes": nbytes, "spell": spell}
    return out


# --------------------------------------------------------------------------- CSS


def root_css(tokens: dict, rings: dict) -> str:
    s, v, c = tokens["surfaces"], tokens["veil"], tokens["cues"]
    ring = rings["emphasis"]
    rows, cols = ring["grid"]["rows"], ring["grid"]["cols"]

    def rgba(col, alpha=1.0):
        r, g, b = (round(x * 255) for x in col)
        return f"rgba({r},{g},{b},{alpha})"

    lines = [
        "/* GENERATED from specs/render-shelf.md Part 6 — do not edit here, edit the shelf. */",
        ":root {",
        f"  --icon: {s['icon_px']}px;",
        f"  --row-gap: {s['row_gap_px']}px;",
        f"  --border-px: {s['border_px']}px;",
        f"  --swipe-color: {rgba(s['swipe']['color'], s['swipe']['alpha'])};",
        "  /* A scenario states `cd`, never a time, so the dial is drawn at a nominal",
        "     fraction: it means \"ruled out\", nothing more. Not a shelf value. */",
        "  --swipe-frac: 0.62turn;",
        f"  --veil-color: {rgba(v['rgb'], v['alpha'])};",
        f"  --pulse-floor: {tokens['pulse']['floor']};",
        f"  --dot-size: {s['corner_dot']['size_px']}px;",
        f"  --dot-inset: {s['corner_dot']['inset_px']}px;",
        f"  --dot-go: {rgba(c['dot']['go'])};",
        f"  --dot-wait: {rgba(c['dot']['wait'])};",
        f"  --cue-gap: {s['center_row']['gap_px']}px;",
        f"  --cue-height: {s['center_row']['height_pct']};",
        f"  --ring-sheet: url({ring['uri']});",
        f"  --ring-size: {cols * 100}% {rows * 100}%;",
        f"  --ring-scale: {ring['host_scale']};",
        f"  --ring-dur: {ring['duration_s']}s;",
        f"  --ring-row-dur: {ring['duration_s'] / rows:.4f}s;",
        f"  --ring-steps-x: steps({cols});",
        f"  --ring-steps-y: steps({rows});",
        # A sprite cell i sits at position i/(n-1) of the track, but steps(n) over 0→X
        # lands on i·X/n — so the keyframe endpoint is 100·n/(n-1), not 100.
        f"  --ring-x-end: {100 * cols / (cols - 1):.4f}%;",
        f"  --ring-y-end: {100 * rows / (rows - 1):.4f}%;",
    ]

    # Part 7 · the lab. Same rule as everything above: no number is authored here.
    lab = tokens.get("lab", {})
    ba = lab.get("border-arrival")
    if ba:
        a = ba["arrival"]
        lines += [
            "  /* lab · L1 border-arrival */",
            f"  --lab-arrive-from: {a['from_scale']};",
            f"  --lab-arrive-dur: {a['duration_s']}s;",
            f"  --lab-arrive-alpha0: {a['from_alpha']};",
            f"  --lab-arrive-every: {a['replay_every_s']}s;",
        ]
        for lane, t in ba["lanes"].items():
            lines.append(f"  --lab-border-{lane.lower()}: {rgba(t['rgb'])};")
            lines.append(f"  --lab-border-{lane.lower()}-px: {t['thickness_px']}px;")
    bs = lab.get("badge-slots")
    if bs:
        d = bs["diameter_pct"] / 100 * s["icon_px"]
        step = d + bs["padding_px"]
        p = bs["plate"]
        lines += [
            "  /* lab · L2 badge-slots — slot 1's CENTER sits on the icon's top-right corner,",
            "     so it half-overhangs; 2 steps left along the top, 3 steps down the right. */",
            f"  --lab-badge-d: {d:.2f}px;",
            f"  --lab-badge-step: {step:.2f}px;",
            f"  --lab-plate: {rgba(p['rgb'], p['alpha'])};",
            f"  --lab-plate-scale: {p['scale']};",
        ]
    lines.append("}")
    return "\n".join(lines)


def strict_css(path: Path) -> list[str]:
    """Literal colors outside the chrome block are opinions this file may not hold."""
    bad = []
    in_chrome = False
    for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if CHROME_START in line:
            in_chrome = True
        elif CHROME_END in line:
            in_chrome = False
            continue
        if in_chrome:
            continue
        if HEX_RE.search(line):
            bad.append(f"{path.name}:{n}: literal color outside the chrome block — {line.strip()}")
    return bad


# --------------------------------------------------------------------------- build


def build(spec: str, tokens: dict, when: str) -> str:
    cfg = SPECS_BUILT[spec]
    roster = load_roster(cfg["catalog"])
    if not cfg["sidecar"].exists():
        _die(f"no sidecar at {cfg['sidecar'].relative_to(ROOT)} — run: "
             f"wowkb.capart import scenarios")
    sidecar = json.loads(cfg["sidecar"].read_text(encoding="utf-8"))
    scenarios = sidecar["scenarios"]
    validate(scenarios, tokens, roster)

    rings = ring_assets(tokens)
    used = sorted({e["name"] for sc in scenarios for e in sc["row"]}
                  | set(cfg["lane_sample"].values()))
    missing = [n for n in cfg["lane_sample"].values() if n not in roster]
    if missing:
        _die(f"lane sample {missing} not in the roster")
    icons = icon_assets(used, roster, tokens)
    lab_frames = lab_assets(tokens)

    # A lab entry names abilities so it can draw on real art; they must be real roster entries,
    # and their icons have to be in the payload even when no scenario uses them.
    lab_icons = sorted({t["ability"]
                        for e in tokens.get("lab", {}).values() if isinstance(e, dict)
                        for t in e.get("triggers", [])})
    unknown = [n for n in lab_icons if n not in roster]
    if unknown:
        _die(f"lab trigger names {unknown} are not in catalog.md's bound-abilities table")
    if lab_icons:
        icons |= icon_assets([n for n in lab_icons if n not in icons], roster, tokens)
        used = sorted(set(used) | set(lab_icons))

    # The base64 budget is a fact to report, not a gate: an oversized page is still a page
    # you can look at, and `wowkb.capart assets` prints the per-asset table that fixes it.
    total = (sum(a["bytes"] for a in rings.values()) + sum(a["bytes"] for a in icons.values())
             + sum(a["bytes"] for a in lab_frames.values()))

    abilities = {
        name: {"key": roster[name]["key"], "spell": roster[name]["spell"],
               "lane": roster[name]["lane"], "icon": icons[name]["uri"]}
        for name in used
    }

    open_rings = [r["atlas"] for r in rings.values() if r["open"]]
    notes = []
    if open_rings:
        notes.append(
            "Ring art " + ", ".join(open_rings) + " is drawn through desaturate-then-tint, "
            "which is <b>unverified in client</b>. Whether a desaturated baked-hue sheet takes a "
            "clean lane hue has not been measured, so treat these rings as a proposal, not a "
            "preview."
        )

    data = {
        "built": when,
        "abilities": abilities,
        "lane_sample": cfg["lane_sample"],
        "scenarios": scenarios,
        "notes": notes,
        "lab_frames": lab_frames,
        "provenance_html": provenance_html(spec, tokens, rings, icons, lab_frames, total, when),
    }

    page = (TEMPLATE / "page.html").read_text(encoding="utf-8")
    page = page.replace("/*__ROOT_TOKENS__*/", root_css(tokens, rings))
    page = page.replace("/*__SHELF_CSS__*/", (TEMPLATE / "shelf.css").read_text(encoding="utf-8"))
    page = page.replace("/*__STEPPER_JS__*/", (TEMPLATE / "stepper.js").read_text(encoding="utf-8"))
    page = page.replace("/*__TOKENS_JSON__*/", json.dumps(tokens, separators=(",", ":")))
    page = page.replace("/*__DATA_JSON__*/", json.dumps(data, separators=(",", ":")))
    return BUILT_MARK.format(date=when) + "\n" + page


def provenance_html(spec, tokens, rings, icons, lab_frames, total, when) -> str:
    cfg = SPECS_BUILT[spec]
    rows = [
        ("render-shelf.md", f"sha {_sha(SHELF)} · Part 6 render-tokens v{tokens['version']}"),
        ("scenarios.md", f"sha {_sha(cfg['scenarios'])}"),
        ("catalog.md", f"sha {_sha(cfg['catalog'])}"),
        ("sidecar", f"{cfg['sidecar'].name} · sha {_sha(cfg['sidecar'])}"),
    ]
    for name, r in rings.items():
        verdict = ("neutral — tints to any hue" if r["tintable"]
                   else "baked hue — one lane only")
        rows.append((
            f"ring · {name}",
            f"{r['atlas']} · FileDataID {r['file_data_id']} · {r['size'][0]}x{r['size'][1]} · "
            f"{r['grid']['rows']}x{r['grid']['cols']}/{r['frames']}f @ {r['duration_s']}s · "
            f"mean saturation {r['mean_saturation']} ({verdict}) · tint {r['tint']} · "
            f"{r['bytes'] / 1024:.1f} KB b64"
        ))
    rows.append(("icons", f"{len(icons)} × {tokens['assets']['icon_size']}px "
                          f"{tokens['assets']['encode']} · "
                          f"{sum(i['bytes'] for i in icons.values()) / 1024:.1f} KB b64"))
    if lab_frames:
        rows.append((
            "lab · Part 7",
            f"{len(lab_frames)} sprite frames from <code>{tokens['lab']['asset_root']}</code> "
            "(Kenney Board Game Icons, CC0) · saturation 0.000, so <code>SetVertexColor</code> "
            "takes them to any lane hue at full strength · "
            f"{sum(f['bytes'] for f in lab_frames.values()) / 1024:.1f} KB b64 · "
            "<b>no authority — nothing in verdicts/cues may reference it</b>"
        ))
    rows.append(("payload", f"{total / 1024:.0f} KB of {tokens['budget']['max_base64_kb']} KB budget"))
    rows.append(("built", when))
    rows.append(("command", "uv run python -m wowkb.capart build " + spec))

    body = "".join(f"<tr><th>{htmllib.escape(k)}</th><td>{v}</td></tr>" for k, v in rows)
    return (
        "<h2>Provenance</h2>"
        "<p class='muted'>Generated — never hand-edited. Every treatment above is composited the "
        "way the client would composite it: <code>SetVertexColor</code> as a multiply against the "
        "sheet's own alpha, never a hue rotation. Edit "
        "<code>specs/render-shelf.md</code> and rebuild.</p>"
        f"<div class='scroll'><table>{body}</table></div>"
    )


# --------------------------------------------------------------------------- commands


def cmd_tokens(args) -> None:
    tokens = load_tokens()
    print(f"render-tokens v{tokens['version']} · {SHELF.relative_to(ROOT)} (sha {_sha(SHELF)})\n")
    for lane, t in tokens["lanes"].items():
        r, g, b = (round(x * 255) for x in t["rgb"])
        print(f"  lane {lane:<9} rgb({r:>3},{g:>3},{b:>3})  alpha {t['alpha']:.2f}  "
              f"{t['pulse_hz']} Hz  {t['thickness_px']}px")
    p = tokens["pulse"]
    print(f"\n  pulse      floor {p['floor']}  phase {p['phase_offset_s']}s  "
          f"{p['smoothing']}/{p['loop']}")
    print(f"  veil       alpha {tokens['veil']['alpha']}")
    print(f"  promotion  scale {tokens['promotion']['scale']}  alpha {tokens['promotion']['alpha']}")
    for name, ring in tokens["rings"].items():
        print(f"  ring {name:<9} {ring['atlas']} {ring['grid']['rows']}x{ring['grid']['cols']}"
              f"/{ring['frames']}f @{ring['duration_s']}s scale {ring['host_scale']} "
              f"tint {ring['tint']}")
    print(f"\n  verdicts   {', '.join(tokens['verdicts'])}")
    print(f"  cues       {', '.join(tokens['cues'])}")

    if args.css:
        print("\n" + root_css(tokens, ring_assets(tokens)))


def cmd_assets(args) -> None:
    tokens = load_tokens()
    rings = ring_assets(tokens)
    cfg = SPECS_BUILT[args.spec]
    roster = load_roster(cfg["catalog"])
    if cfg["sidecar"].exists():
        scenarios = json.loads(cfg["sidecar"].read_text(encoding="utf-8"))["scenarios"]
    else:
        scenarios = scrape_scenarios(cfg["scenarios"])
    used = sorted({e["name"] for sc in scenarios for e in sc["row"]}
                  | set(cfg["lane_sample"].values()))
    icons = icon_assets(used, roster, tokens)

    print(f"{'asset':<40} {'kind':<6} {'b64 KB':>8}  notes")
    print("-" * 92)
    for name, r in rings.items():
        note = f"{r['grid']['rows']}x{r['grid']['cols']}/{r['frames']}f · sat {r['mean_saturation']}"
        print(f"{r['atlas']:<40} {'sheet':<6} {r['bytes'] / 1024:>8.1f}  {note}")
    for name in used:
        a = icons[name]
        print(f"{name:<40} {'icon':<6} {a['bytes'] / 1024:>8.1f}  spell {a['spell']}")
    total = sum(a["bytes"] for a in rings.values()) + sum(a["bytes"] for a in icons.values())
    cap = tokens["budget"]["max_base64_kb"]
    print("-" * 92)
    print(f"{'TOTAL':<40} {'':<6} {total / 1024:>8.1f}  of {cap} KB budget "
          f"({total / 1024 / cap * 100:.0f}%)")
    if total > cap * 1024:
        sys.exit(1)


def cmd_import(args) -> None:
    cfg = SPECS_BUILT[args.spec]
    tokens = load_tokens()
    roster = load_roster(cfg["catalog"])
    scenarios = scrape_scenarios(cfg["scenarios"])
    validate(scenarios, tokens, roster)
    payload = {
        "_comment": (
            "SEEDED by `wowkb.capart import scenarios` from specs/havoc/scenarios.md, then "
            "reviewed by eye. The DOC leads: `capart check` re-scrapes the CDM-row bullets and "
            "fails if they disagree with this file. Edit the doc, re-import, review."
        ),
        "spec": args.spec,
        "source": str(cfg["scenarios"].relative_to(ROOT)),
        "scenarios": scenarios,
    }
    cfg["sidecar"].parent.mkdir(parents=True, exist_ok=True)
    cfg["sidecar"].write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
                              encoding="utf-8")
    print(f"wrote {cfg['sidecar'].relative_to(ROOT)} — {len(scenarios)} scenarios, "
          f"{sum(len(s['row']) for s in scenarios)} row entries")
    for sc in scenarios:
        press = next((e["name"] for e in sc["row"]
                      if e["verdict"].startswith("press")), "—")
        print(f"  {sc['id']:<6} {len(sc['row']):>2} icons · {len(sc['steps'])} steps · press {press}")


def cmd_build(args) -> None:
    tokens = load_tokens()
    when = args.date or date.today().isoformat()
    page = build(args.spec, tokens, when)
    out = SPECS_BUILT[args.spec]["out"]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(page, encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} · {len(page) / 1024:.0f} KB · built {when}")
    cap = tokens["budget"]["max_base64_kb"]
    if len(page) / 1024 > cap:
        _warn(f"page is over the {cap} KB budget in tokens.budget — "
              "run `wowkb.capart assets` for the per-asset table")


def cmd_check(args) -> None:
    tokens = load_tokens()
    cfg = SPECS_BUILT[args.spec]
    fails = []

    for line in strict_css(TEMPLATE / "shelf.css"):
        fails.append(line)

    # 1 · the doc leads the sidecar.
    doc = scrape_scenarios(cfg["scenarios"])
    if not cfg["sidecar"].exists():
        fails.append(f"no sidecar at {cfg['sidecar'].relative_to(ROOT)}")
    else:
        side = json.loads(cfg["sidecar"].read_text(encoding="utf-8"))["scenarios"]
        d_ids = [s["id"] for s in doc]
        s_ids = [s["id"] for s in side]
        if d_ids != s_ids:
            fails.append(f"scenario ids differ — doc {d_ids} vs sidecar {s_ids}")
        else:
            for a, b in zip(doc, side):
                ka = [(e["name"], e["verdict"], e.get("dots"), e.get("cues")) for e in a["row"]]
                kb = [(e["name"], e["verdict"], e.get("dots"), e.get("cues")) for e in b["row"]]
                if ka != kb:
                    fails.append(f"{a['id']}: CDM row in scenarios.md differs from the sidecar")
                    for x, y in zip(ka, kb):
                        if x != y:
                            fails.append(f"    doc {x} != sidecar {y}")
                    if len(ka) != len(kb):
                        fails.append(f"    doc has {len(ka)} entries, sidecar {len(kb)}")

    # 2 · the committed HTML is not stale.
    out = cfg["out"]
    if not out.exists():
        fails.append(f"no artifact at {out.relative_to(ROOT)} — run: wowkb.capart build {args.spec}")
    else:
        committed = out.read_text(encoding="utf-8")
        m = BUILT_RE.search(committed)
        if not m:
            fails.append(f"{out.name} carries no build stamp — rebuild it")
        elif build(args.spec, tokens, m.group(1)) != committed:
            fails.append(f"{out.name} is stale — rebuild: wowkb.capart build {args.spec}")

    if fails:
        print("FAIL")
        for f in fails:
            print(f"  {f}")
        sys.exit(1)
    print(f"ok · {args.spec}: scenarios.md matches the sidecar, the artifact is current, "
          "and shelf.css holds no literal colors")


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.capart", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    t = sub.add_parser("tokens", help="resolved render-shelf tokens (and the CSS they generate)")
    t.add_argument("--css", action="store_true", help="also print the generated :root block")
    t.set_defaults(func=cmd_tokens)

    a = sub.add_parser("assets", help="per-asset base64 byte table against the budget")
    a.add_argument("spec", nargs="?", default="havoc", choices=sorted(SPECS_BUILT))
    a.set_defaults(func=cmd_assets)

    i = sub.add_parser("import", help="seed the scenario sidecar from the doc")
    i.add_argument("what", choices=["scenarios"])
    i.add_argument("spec", nargs="?", default="havoc", choices=sorted(SPECS_BUILT))
    i.set_defaults(func=cmd_import)

    b = sub.add_parser("build", help="render the artifact")
    b.add_argument("spec", choices=sorted(SPECS_BUILT))
    b.add_argument("--date", help="stamp this build date instead of today (used by `check`)")
    b.set_defaults(func=cmd_build)

    c = sub.add_parser("check", help="doc-vs-sidecar and artifact-staleness gates")
    c.add_argument("spec", choices=sorted(SPECS_BUILT))
    c.set_defaults(func=cmd_check)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
