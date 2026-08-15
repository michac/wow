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
  baked hue is a **hard error**, naming the measurement. The guard is art-agnostic: it began
  on the flipbook emphasis rings and, since those retired, covers the badge sprites.
* `tint: "desaturate+lane"` builds but is stamped ⚠ *open*, because desaturate-then-tint
  is unverified in client.

Only two things stop a build: the tint guard above, and a verdict, cue or ability the
vocabulary does not know (which would render *nothing*, silently). Everything else — the
base64 budget, the literal-hex scan — is a `check` concern or a warning, because **nothing may
block a rebuild you want to look at**. `check` is the CI-shaped gate; `build` is the loop.

`check` additionally asserts the **reading rule** (`elimination_gate`): for every scenario the
leftmost entry that is neither swiped nor veiled nor carrying a **negative** cue must be the entry
the doc calls the press. That is what makes a mostly-negative cue vocabulary safe to ship. Two
gates fence the exception: at most ONE cue may declare `polarity: "positive"`, and every declared
cue must be worn by some scenario row (a cue that renders nowhere is `spec.md` §3.2's defect).
Two more make the shelf's own mechanical claims true rather than promised: the veil is derived
from cue polarity (`render-shelf.md` Part 2.5) and slot 3 belongs to the positive cue (Part 1).

Usage:
    uv run python -m wowkb.capart tokens                # resolved tokens + the CSS block
    uv run python -m wowkb.capart assets                # per-asset byte table vs the budget
    uv run python -m wowkb.capart import scenarios      # seed the sidecar from scenarios.md
    uv run python -m wowkb.capart build havoc           # write the artifact
    uv run python -m wowkb.capart export lua            # the same tokens as CombatAssistPlus/Style.lua
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
        # art even when no scenario happens to exercise that lane. CHARGES is a render-time
        # substitution off a client fact, so its sample is simply an ability the catalog
        # marks as having charges — the lane falls out, it is not assigned here.
        "lane_sample": {
            "COOLDOWN": "Metamorphosis",
            "ROTATION": "Blade Dance",
            "FALLBACK": "Fel Rush",
            "CHARGES": "Immolation Aura",
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

ADDON_SRC = PROJECT / "addon" / "CombatAssistPlus"
STYLE_LUA = ADDON_SRC / "Style.lua"
BADGE_DIR = ADDON_SRC / "Media" / "badges"
# Where the client looks for a vendored texture. Plumbing, not a design number.
BADGE_TEXTURE_ROOT = "Interface\\AddOns\\CombatAssistPlus\\Media\\badges\\"
# `artifact` is annotated in the shelf as a viewing aid the addon does not have, and Part 7's
# `lab` is by construction not the style. Neither may reach the client.
NOT_THE_STYLE = ("artifact", "lab")

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
    r"\s*(?P<override>[^|]*?)\s*\|\s*(?P<lane>[A-Z]+|—|-)\s*\|\s*(?P<charges>[^|]*?)\s*\|",
    re.M,
)
OVERRIDE_RE = re.compile(r"^(?P<name>[^⚠`]+?)\s*⚠\s*`(?P<spell>\d+)`")

# The catalog's Charges column. A number means the client will report charges on that row,
# which is what makes the border read CHARGES instead of the role lane (render-shelf V2).
# Anything else — a dash, a "⚠ unresolved" note — is NOT a charge ability here: an unmeasured
# fact must never render as a measured one.
CHARGES_RE = re.compile(r"^\s*(?:(?P<n>\d+)|yes)\b")


def load_roster(catalog: Path) -> dict:
    """catalog.md's *Bound abilities* table → {display name: {key, spell, lane, charges}}.

    Both the base name and the demon-form override name are keys, because a scenario row
    writes whichever name the client would *show* (R7 resolves the live `overrideSpellID`;
    cap authors none of it). Parsing the catalog rather than restating it is what keeps
    spell ids, lanes, charge counts and override names from existing in two places.

    `lane` stays the **authored role lane** even for a charge ability. The CHARGES border is a
    render-time substitution off a client fact, not a re-authoring of priority — so the
    catalog keeps saying ROTATION for Immolation Aura and the renderer decides what colour
    that draws as.
    """
    text = catalog.read_text(encoding="utf-8")
    out: dict[str, dict] = {}
    for m in ROSTER_RE.finditer(text):
        lane = m.group("lane")
        if lane in {"—", "-"}:
            continue  # a row with no lane is an open fact, not a drawable button
        cm = CHARGES_RE.match(m.group("charges"))
        # `yes` = the client reports charges but the count is not Tier-1 sourced. The border
        # only needs the boolean, so `yes` is enough to substitute — and it is not a guess at
        # a number nobody measured.
        charges = (int(cm.group("n")) if cm.group("n") else "yes") if cm else 0
        key, base_id = m.group("key"), int(m.group("spell"))
        out[m.group("name")] = {"key": key, "spell": base_id, "lane": lane,
                                "charges": charges}
        ov = OVERRIDE_RE.match(m.group("override"))
        if ov:
            out[ov.group("name").strip()] = {
                "key": key,
                "spell": int(ov.group("spell")),
                "lane": lane,
                "charges": charges,
                "override_of": m.group("name"),
            }
    if not out:
        _die(f"no bound-abilities table rows found in {catalog.relative_to(ROOT)}")
    return out


def border_lane(entry: dict) -> str:
    """Which of tokens.lanes the border draws — the one place the substitution happens."""
    return "CHARGES" if entry.get("charges") else entry["lane"]


# --------------------------------------------------------------------------- scraping


ENTRY_RE = re.compile(r"^(?P<name>.+?)\s+`(?P<verdict>[a-z-]+)`(?P<ann>.*)$")
GROUP_RE = re.compile(r"\{(?P<kind>cues):\s*(?P<body>[^}]*)\}")
# The retired `{dots: X go, Y wait}` group. It is matched separately and rejected by NAME,
# because a silently-ignored group would let a scenario keep asserting a cue the style no
# longer draws — which is exactly the doc↔render divergence this tool exists to catch.
DEAD_GROUP_RE = re.compile(r"\{(?P<kind>dots)\s*:")


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
        if DEAD_GROUP_RE.search(chunk):
            _die(f"CDM row entry still carries a retired `{{dots: …}}` group: {chunk!r}\n"
                 "       The green/red dependency dots were retired 2026-08-13 with "
                 "render-shelf V6.\n"
                 "       A SATISFIED dependency now draws nothing — delete the group. A "
                 "BLOCKED one is\n"
                 "       `{cues: blocked}` on a `hold-readable` row.")
        groups = {m.group("kind"): m.group("body") for m in GROUP_RE.finditer(chunk)}
        bare = GROUP_RE.sub("", chunk).strip()
        m = ENTRY_RE.match(bare)
        if not m:
            _die(f"CDM row entry does not parse: {chunk!r}\n"
                 "       expected: <Ability> `<verdict>` [{cues: …}]")
        entry = {"name": m.group("name").strip(), "verdict": m.group("verdict")}
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


def assert_tintable(what: str, source: str, tint: str, sat, tintable) -> bool:
    """THE TINT GUARD. Returns True if the primitive should be stamped ⚠ *open*.

    This is the shelf's one mechanical promise, and it is deliberately **art-agnostic**: it
    started life guarding the flipbook emphasis rings, those retired with V1, and it now guards
    the badge sprites. The claim it enforces was never about rings — it is *art the shelf
    recolors must be art `SetVertexColor` can actually recolor*. `tint: "lane"` is the token
    spelling of that claim (the colour comes from the shelf, not from the art).

    Losing this silently would be the worst possible outcome of retiring a primitive, so
    `cmd_check` separately asserts that SOMETHING still declares `tint: "lane"` — a guard whose
    subject set quietly emptied keeps passing while guaranteeing nothing.
    """
    if tint == "lane" and tintable is False:
        _die(
            f"{what} declares tint: \"lane\" but {source} measured mean saturation {sat} — it "
            "carries a BAKED HUE.\n"
            "       SetVertexColor multiplies, so that art can only be darkened toward its own "
            "hue; the authored colour is not drawable on it, and a preview that showed one "
            "would be a lie.\n"
            "       Fix it one of three ways: pick neutral art (the vendored Kenney frames "
            "measure 0.000); declare tint: \"none\" and accept the art's own hue; or declare "
            "tint: \"desaturate+lane\", which builds but stamps a visible ⚠ because "
            "desaturate-then-tint is unverified in client."
        )
    return tint == "desaturate+lane"


def badge_assets(tokens: dict) -> dict:
    """The cue sprite frames (V5), from files we vendor rather than from CASC.

    Every frame is white with its shape in the alpha channel, which is what makes
    `SetVertexColor` able to take it to the authored hue at full strength — the same reason
    CDMProbe shipped Kenney's `star_07` instead of a Blizzard atlas. In CSS the faithful analogue
    of that multiply is `mask-image` + `background-color`: the alpha shapes it, the color IS the
    multiply result for white art. It is not a hue-rotate and it is not a lie.

    Saturation is measured here, per frame, rather than trusted from prose — which is what lets
    the tint guard keep a real subject now that the atlas rings are gone.
    """
    badges = tokens["badges"]
    root = ROOT / "projects" / "combat-assist" / badges["asset_root"]
    tint = badges.get("tint", "none")
    out: dict[str, dict] = {}
    for key, cue in tokens["cues"].items():
        for frame in cue["frames"]:
            if frame in out:
                continue
            path = root / f"{frame}.png"
            if not path.exists():
                _die(f"cue {key!r} names frame {frame!r}, not found at "
                     f"{(root / f'{frame}.png').relative_to(ROOT)} — "
                     f"tokens.badges.asset_root is {badges['asset_root']!r}")
            img = Image.open(path).convert("RGBA")
            measure = uiart.tintability(img)
            open_flag = assert_tintable(
                f"badge sprite {frame!r} (cue {key!r})", str(path.relative_to(ROOT)),
                tint, measure["mean_saturation"], measure["tintable"],
            )
            buf = io.BytesIO()
            img.save(buf, "PNG", optimize=True)
            uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
            out[frame] = {
                "uri": uri, "bytes": len(uri), "size": list(img.size),
                "mean_saturation": measure["mean_saturation"],
                "tintable": measure["tintable"], "tint": tint, "open": open_flag,
            }
    return out


# ------------------------------------------------------------------- export into the addon


def addon_style(tokens: dict) -> dict:
    """The part of the token block the client draws with, plus where its art landed."""
    out = {k: v for k, v in tokens.items() if k not in NOT_THE_STYLE}
    out["badges"] = dict(out["badges"])
    out["badges"]["texture_root"] = BADGE_TEXTURE_ROOT
    # The two shapes CSS gets from `border-radius` and `radial-gradient` and the client gets
    # only as art, named here so `Paint` reads their file names rather than restating them.
    out["badges"]["plate"] = dict(out["badges"]["plate"], texture=PLATE_TEXTURE)
    out["badges"]["halo_texture"] = HALO_TEXTURE
    return out


def _lua_scalar(v) -> str:
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, int):
        return str(v)
    if isinstance(v, float):
        return f"{v:.2f}" if v.is_integer() else repr(v)
    s = str(v).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
    return f'"{s}"'


def _lua_key(k: str) -> str:
    """`hold-readable` is a legal verdict name and an illegal Lua identifier."""
    return k if re.fullmatch(r"[A-Za-z_]\w*", k) else f'["{k}"]'


def _lua_value(v, indent: int) -> str:
    pad, inner = "  " * indent, "  " * (indent + 1)
    if isinstance(v, dict):
        if not v:
            return "{}"
        lines = [f"{inner}{_lua_key(k)} = {_lua_value(v[k], indent + 1)}," for k in sorted(v)]
        return "{\n" + "\n".join(lines) + f"\n{pad}}}"
    if isinstance(v, list):
        if all(isinstance(x, (int, float)) and not isinstance(x, bool) for x in v):
            return "{ " + ", ".join(_lua_scalar(x) for x in v) + " }"
        lines = [f"{inner}{_lua_value(x, indent + 1)}," for x in v]
        return "{\n" + "\n".join(lines) + f"\n{pad}}}"
    return _lua_scalar(v)


def style_lua(tokens: dict) -> str:
    """`Style.lua` — Part 6 as a Lua table, data only, so `Treatment`/`Paint` hold no numbers."""
    return (
        "-- Style.lua — GENERATED from specs/render-shelf.md Part 6. Do not edit this file.\n"
        "--   uv run python -m wowkb.capart export lua\n"
        "-- Data only: the logic that reads it is Treatment.lua and Paint.lua.\n"
        "local ADDON, ns = ...\n"
        "\n"
        f"ns.Style = {_lua_value(addon_style(tokens), 0)}\n"
    )


def badge_frames(tokens: dict) -> list[str]:
    """Every sprite frame the cue vocabulary names, in declaration order, deduplicated."""
    out = []
    for cue in tokens["cues"].values():
        for frame in cue["frames"]:
            if frame not in out:
                out.append(frame)
    return out


# A badge glyph draws at roughly a quarter of the shelf's icon, so 128px source art reaches the
# client as a heavy minification. Downsampling here (Pillow, LANCZOS) beats doing it at draw time.
SPRITE_PX = 64
SHAPE_PX = 64          # texture resolution for the generated shapes — plumbing, not a look
SHAPE_SS = 4           # supersampling factor for the disc's edge
PLATE_TEXTURE, HALO_TEXTURE = "plate", "halo"


def shape_images(tokens: dict) -> dict:
    """The two shapes CSS gets for free and the client does not: the disc and the halo.

    A `border-radius` and a `radial-gradient` are one CSS property each; in the client both are
    art. Part 4 says shapes no CC0 pack carries are authored from a script so they regenerate
    rather than accumulate as binary mystery — this is that script. Both are white with the
    shape in the alpha channel, so `SetVertexColor` takes them to the authored hue.
    """
    big = SHAPE_PX * SHAPE_SS
    disc = Image.new("L", (big, big), 0)
    from PIL import ImageDraw
    ImageDraw.Draw(disc).ellipse((0, 0, big - 1, big - 1), fill=255)
    plate = Image.merge("RGBA", (Image.new("L", (big, big), 255),) * 3
                        + (disc,)).resize((SHAPE_PX, SHAPE_PX), Image.LANCZOS)

    # The halo is the CSS gradient's own recipe: opaque at the centre, transparent at
    # `tokens.badges.halo_falloff` of the radius.
    stop = tokens["badges"]["halo_falloff"]
    halo = Image.new("RGBA", (SHAPE_PX, SHAPE_PX))
    c = (SHAPE_PX - 1) / 2
    px = halo.load()
    for y in range(SHAPE_PX):
        for x in range(SHAPE_PX):
            r = ((x - c) ** 2 + (y - c) ** 2) ** 0.5 / c
            a = 0.0 if r >= stop else 1.0 - r / stop
            px[x, y] = (255, 255, 255, round(a * 255))
    return {PLATE_TEXTURE: plate, HALO_TEXTURE: halo}


def _write_tga(img: Image.Image, name: str) -> tuple[int, int]:
    w, h = img.size
    if w & (w - 1) or h & (h - 1):
        _die(f"{name} is {w}x{h} — the client wants power-of-two texture dimensions")
    # 32-bit RLE, top-left origin — byte-for-byte the header shape of the Kenney TGAs
    # CDMProbe already ships and the client already reads.
    img.save(BADGE_DIR / f"{name}.tga", "TGA", compression="tga_rle", orientation=1)
    return img.size


def export_badges(tokens: dict) -> list[tuple[str, tuple[int, int]]]:
    """Vendor the badge art into the addon as 32-bit TGA — what the client reads.

    The tint guard runs here too, on the art that actually ships, so a baked-hue frame cannot
    reach the client through a path the artifact never rendered.
    """
    badges = tokens["badges"]
    src = ROOT / "projects" / "combat-assist" / badges["asset_root"]
    tint = badges.get("tint", "none")
    BADGE_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for frame in badge_frames(tokens):
        path = src / f"{frame}.png"
        if not path.exists():
            _die(f"cue frame {frame!r} not found at {path.relative_to(ROOT)}")
        img = Image.open(path).convert("RGBA")
        measure = uiart.tintability(img)
        assert_tintable(f"badge sprite {frame!r}", str(path.relative_to(ROOT)),
                        tint, measure["mean_saturation"], measure["tintable"])
        if img.size[0] > SPRITE_PX:
            img = img.resize((SPRITE_PX, SPRITE_PX), Image.LANCZOS)
        written.append((frame, _write_tga(img, frame)))
    for name, img in shape_images(tokens).items():
        written.append((name, _write_tga(img, name)))
    licence = src / "LICENSE.txt"
    if licence.exists():
        (BADGE_DIR / "LICENSE.txt").write_text(licence.read_text(encoding="utf-8"),
                                               encoding="utf-8")
    return written


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


def root_css(tokens: dict) -> str:
    s, v = tokens["surfaces"], tokens["veil"]
    a, b = tokens["arrival"], tokens["badges"]

    def rgba(col, alpha=1.0):
        r, g, b_ = (round(x * 255) for x in col)
        return f"rgba({r},{g},{b_},{alpha})"

    d = b["diameter_pct"] / 100 * s["icon_px"]
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
        "",
        "  /* V2 · lane border + the one-shot arrival snap. */",
        f"  --arrive-from: {a['from_scale']};",
        f"  --arrive-dur: {a['duration_s']}s;",
        f"  --arrive-alpha0: {a['from_alpha']};",
    ]
    for lane, t in tokens["lanes"].items():
        lines.append(f"  --lane-{lane.lower()}: {rgba(t['rgb'])};")
        lines.append(f"  --lane-{lane.lower()}-px: {t['thickness_px']}px;")

    # Slot 1 hangs off the top-right corner: its right edge sits `overhang` past the icon's
    # right edge and its top edge `overhang` above the top, so it reads as ON the icon rather
    # than inside it. Slot 2 steps one diameter+padding left along the top; slot 3 the same
    # distance down the right.
    lines += [
        "",
        "  /* V5 · corner badges. Slot 1 overhangs the top-right corner by --badge-over;",
        "     2 steps left along the top edge, 3 steps down the right edge. */",
        f"  --badge-d: {d:.2f}px;",
        f"  --badge-over: {b['overhang_px']}px;",
        f"  --badge-step: {d + b['padding_px']:.2f}px;",
        f"  --badge-inset: {b['sprite_inset_pct']}%;",
        f"  --badge-tint: {rgba(b['rgb'])};",
        f"  --plate: {rgba(b['plate']['rgb'], b['plate']['alpha'])};",
        f"  --plate-scale: {b['plate']['scale']};",
        f"  --badge-halo-stop: {b['halo_falloff'] * 100:.0f}%;",
    ]

    # A cue may override the shared badge hue. The negatives deliberately do not — one red for
    # every "skip this" is what makes the vocabulary readable at a glance — so in practice this
    # emits the single positive cue's gold and nothing else. `tokens.badges.rgb` stays the default.
    for key, cue in tokens["cues"].items():
        if "rgb" in cue:
            lines.append(f"  --cue-{key}-tint: {rgba(cue['rgb'])};")
        g = cue.get("glow")
        if g:
            lines += [
                f"  --cue-{key}-glow-dur: {1.0 / g['hz']:.4f}s;",
                f"  --cue-{key}-glow-a0: {g['alpha_min']};",
                f"  --cue-{key}-glow-a1: {g['alpha_max']};",
                f"  --cue-{key}-glow-scale: {g['scale']};",
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

    used = sorted({e["name"] for sc in scenarios for e in sc["row"]}
                  | set(cfg["lane_sample"].values()))
    missing = [n for n in cfg["lane_sample"].values() if n not in roster]
    if missing:
        _die(f"lane sample {missing} not in the roster")
    icons = icon_assets(used, roster, tokens)
    frames = badge_assets(tokens)

    # The base64 budget is a fact to report, not a gate: an oversized page is still a page
    # you can look at, and `wowkb.capart assets` prints the per-asset table that fixes it.
    total = sum(a["bytes"] for a in icons.values()) + sum(f["bytes"] for f in frames.values())

    abilities = {
        name: {"key": roster[name]["key"], "spell": roster[name]["spell"],
               # `lane` is the AUTHORED role lane; `border` is what actually draws, after the
               # CHARGES substitution. Both travel, so the artifact can show the substitution
               # rather than silently applying it.
               "lane": roster[name]["lane"], "border": border_lane(roster[name]),
               "charges": roster[name].get("charges", 0), "icon": icons[name]["uri"]}
        for name in used
    }

    notes = []
    open_frames = sorted(n for n, f in frames.items() if f["open"])
    if open_frames:
        notes.append(
            "Badge sprite(s) " + ", ".join(open_frames) + " are drawn through "
            "desaturate-then-tint, which is <b>unverified in client</b>. Whether desaturated "
            "baked-hue art takes a clean authored hue has not been measured, so treat these as a "
            "proposal, not a preview."
        )
    # A lane the roster can never draw is a real finding about the catalog, not a build error —
    # under the CHARGES substitution every Havoc FALLBACK ability turns out to have charges.
    drawable = {border_lane(roster[n]) for n in used}
    dark = [ln for ln in tokens["lanes"] if ln not in drawable]
    if dark:
        notes.append(
            "Lane(s) <b>" + ", ".join(dark) + "</b> are declared in the shelf but no ability in "
            "this catalog draws them — every candidate is displaced by the CHARGES substitution "
            "(shelf V2). The gallery swatch below still shows the lane; no CDM row does."
        )

    data = {
        "built": when,
        "abilities": abilities,
        "lane_sample": cfg["lane_sample"],
        "scenarios": scenarios,
        "notes": notes,
        "frames": frames,
        "provenance_html": provenance_html(spec, tokens, icons, frames, total, when),
    }

    page = (TEMPLATE / "page.html").read_text(encoding="utf-8")
    page = page.replace("/*__ROOT_TOKENS__*/", root_css(tokens))
    page = page.replace("/*__SHELF_CSS__*/", (TEMPLATE / "shelf.css").read_text(encoding="utf-8"))
    page = page.replace("/*__STEPPER_JS__*/", (TEMPLATE / "stepper.js").read_text(encoding="utf-8"))
    page = page.replace("/*__TOKENS_JSON__*/", json.dumps(tokens, separators=(",", ":")))
    page = page.replace("/*__DATA_JSON__*/", json.dumps(data, separators=(",", ":")))
    return BUILT_MARK.format(date=when) + "\n" + page


def provenance_html(spec, tokens, icons, frames, total, when) -> str:
    cfg = SPECS_BUILT[spec]
    rows = [
        ("render-shelf.md", f"sha {_sha(SHELF)} · Part 6 render-tokens v{tokens['version']}"),
        ("scenarios.md", f"sha {_sha(cfg['scenarios'])}"),
        ("catalog.md", f"sha {_sha(cfg['catalog'])}"),
        ("sidecar", f"{cfg['sidecar'].name} · sha {_sha(cfg['sidecar'])}"),
    ]
    rows.append((
        "border · V2",
        " · ".join(f"<b>{ln}</b> {t['thickness_px']}px" for ln, t in tokens["lanes"].items())
        + " — solid <code>SetColorTexture</code> strips, <b>no art</b>, so nothing to extract "
        "and nothing to go stale across a patch. One-shot arrival snap "
        f"{tokens['arrival']['from_scale']}× → 1× over {tokens['arrival']['duration_s']}s "
        f"({tokens['arrival']['smoothing']}); replayed every "
        f"{tokens['artifact']['arrival_replay_s']}s here only so it can be watched."
    ))
    rows.append(("icons", f"{len(icons)} × {tokens['assets']['icon_size']}px "
                          f"{tokens['assets']['encode']} · "
                          f"{sum(i['bytes'] for i in icons.values()) / 1024:.1f} KB b64"))
    if frames:
        sats = sorted({f["mean_saturation"] for f in frames.values()})
        rows.append((
            "badge sprites · V5",
            f"{len(frames)} frames from <code>{tokens['badges']['asset_root']}</code> "
            "(Kenney <b>Board Game Icons</b>, <b>CC0</b> — licence vendored beside the art) · "
            f"measured mean saturation {', '.join(str(s) for s in sats)}, so "
            "<code>SetVertexColor</code> takes them to the authored hue at full strength · "
            f"declared <code>tint: \"{tokens['badges']['tint']}\"</code>, which is what puts them "
            "under the tint guard · "
            f"{sum(f['bytes'] for f in frames.values()) / 1024:.1f} KB b64"
        ))
    rows.append(("payload", f"{total / 1024:.0f} KB of {tokens['budget']['max_base64_kb']} KB budget"))
    rows.append(("built", when))
    rows.append(("command", "uv run python -m wowkb.capart build " + spec))

    body = "".join(f"<tr><th>{htmllib.escape(k)}</th><td>{v}</td></tr>" for k, v in rows)
    return (
        "<h2>Provenance</h2>"
        "<p class='muted'>Generated — never hand-edited. Every treatment above is composited the "
        "way the client would composite it: <code>SetVertexColor</code> as a multiply against the "
        "sprite's own alpha, never a hue rotation. Edit "
        "<code>specs/render-shelf.md</code> and rebuild.</p>"
        f"<div class='scroll'><table>{body}</table></div>"
    )


# --------------------------------------------------------------------------- commands


def cmd_tokens(args) -> None:
    tokens = load_tokens()
    print(f"render-tokens v{tokens['version']} · {SHELF.relative_to(ROOT)} (sha {_sha(SHELF)})\n")
    print("  V2 · lane border (solid, no art)")
    for lane, t in tokens["lanes"].items():
        r, g, b = (round(x * 255) for x in t["rgb"])
        print(f"    {lane:<9} rgb({r:>3},{g:>3},{b:>3})  {t['thickness_px']}px")
    a = tokens["arrival"]
    print(f"    arrival  {a['from_scale']}x -> 1x over {a['duration_s']}s "
          f"{a['smoothing']}, from alpha {a['from_alpha']} — ONE SHOT, no loop")

    b = tokens["badges"]
    d = b["diameter_pct"] / 100 * tokens["surfaces"]["icon_px"]
    r, g, bl = (round(x * 255) for x in b["rgb"])
    print(f"\n  V5 · corner badges  {b['diameter_pct']}% of "
          f"{tokens['surfaces']['icon_px']}px = {d:.1f}px · overhang {b['overhang_px']}px · "
          f"sprite inset {b['sprite_inset_pct']}%")
    overrides = [k for k, c in tokens["cues"].items() if "rgb" in c]
    print(f"    tint     shared rgb({r},{g},{bl}) for every negative cue · "
          f"declared tint {b['tint']!r}")
    if overrides:
        print(f"             own hue: {', '.join(sorted(overrides))} (colour carries polarity)")
    print(f"    art      {b['asset_root']}")
    over, gap = b["overhang_px"], tokens["surfaces"]["row_gap_px"]
    print(f"    row fit  overhangs {over}px past the edge, row gap {gap}px — "
          f"{'CLEARS' if over < gap else 'COLLIDES'}")

    print("\n  cues (negative BY DEFAULT — a cue draws when a button is RULED OUT; the one "
          "positive\n        cue reports impending loss and does NOT eliminate its own button)")
    for key, cue in tokens["cues"].items():
        pol = cue.get("polarity", "negative")
        print(f"    {key:<9} {'+' if pol == 'positive' else '-'} slot {cue['slot']} · "
              f"{len(cue['frames'])}f @{cue['duration_s']}s {cue['loop']:<7} {cue['means'][:48]}")

    print(f"\n  veil       alpha {tokens['veil']['alpha']}")
    t = tokens["text"]
    print(f"  text       max {t['max_hz']} Hz · duty {t['duty']} · alpha floor {t['alpha_floor']} "
          "(MIL-STD-1472F — safety, not taste)")
    print(f"  artifact   arrival replayed every {tokens['artifact']['arrival_replay_s']}s "
          "(VIEWING AID — not the style)")

    borderless = [k for k, v in tokens["verdicts"].items() if not v["border"]]
    veiled = [k for k, v in tokens["verdicts"].items() if v["veil"]]
    print(f"\n  verdicts   {', '.join(tokens['verdicts'])}")
    print(f"    no border  {', '.join(borderless)}")
    print(f"    veiled     {', '.join(veiled)}")
    if "lab" in tokens:
        print(f"\n  lab        {', '.join(k for k in tokens['lab'] if not k.startswith('_'))}")
    else:
        print("\n  lab        empty (Part 7)")

    if args.css:
        print("\n" + root_css(tokens))


def cmd_assets(args) -> None:
    tokens = load_tokens()
    frames = badge_assets(tokens)
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
    for name in sorted(frames):
        f = frames[name]
        verdict = "neutral — tints to the authored hue" if f["tintable"] else "BAKED HUE"
        print(f"{name:<40} {'badge':<6} {f['bytes'] / 1024:>8.1f}  "
              f"sat {f['mean_saturation']} ({verdict}) · tint {f['tint']}")
    for name in used:
        a = icons[name]
        print(f"{name:<40} {'icon':<6} {a['bytes'] / 1024:>8.1f}  spell {a['spell']}")
    total = sum(f["bytes"] for f in frames.values()) + sum(a["bytes"] for a in icons.values())
    cap = tokens["budget"]["max_base64_kb"]
    print("-" * 92)
    print(f"{'TOTAL':<40} {'':<6} {total / 1024:>8.1f}  of {cap} KB budget "
          f"({total / 1024 / cap * 100:.0f}%)")
    print("\nThe lane border (V2) is four SetColorTexture strips and carries NO asset — that is "
          "the point of it.")
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


def cmd_export(args) -> None:
    tokens = load_tokens()
    if not ADDON_SRC.exists():
        _die(f"no addon checkout at {ADDON_SRC.relative_to(ROOT)} — "
             "run: uv run python -m wowkb.addon pull cap")
    what = args.what
    if what in ("lua", "all"):
        STYLE_LUA.write_text(style_lua(tokens), encoding="utf-8")
        print(f"wrote {STYLE_LUA.relative_to(ROOT)} — render-tokens v{tokens['version']} "
              f"(shelf sha {_sha(SHELF)})")
    if what in ("badges", "all"):
        for frame, size in export_badges(tokens):
            print(f"  {frame + '.tga':<24} {size[0]}x{size[1]} 32-bit → "
                  f"{BADGE_DIR.relative_to(ROOT)}")


def _cues_of(entry: dict, tokens: dict) -> list[str]:
    """Every cue key an entry wears — its verdict's, plus any the row bullet names."""
    rule = tokens["verdicts"][entry["verdict"]]
    return list(rule.get("cues") or []) + list(entry.get("cues") or [])


def positive_gate(scenarios: list[dict], tokens: dict) -> list[str]:
    """PASS 1 OF THE OPERATOR HEURISTIC, MECHANISED (render-shelf.md Part 0.5).

    *Scan left to right for a positive cue. If one is present, press it.* A positive cue is
    pre-emptive by design — impending loss reported after the eye has walked past it has been
    reported too late — so a scenario where the leftmost positive cue sits on something OTHER
    than the press is a scenario that reads wrong.

    This is the half the elimination gate deliberately cannot see: that gate counts negative cues
    only, precisely so a positive cue can ride its own press without eliminating it. Which leaves
    the positive cue itself ungated, and this is that gate. A scenario wearing no positive cue at
    all is simply not pass-1's subject and passes trivially.
    """
    fails = []
    for sc in scenarios:
        press = [e["name"] for e in sc["row"] if e["verdict"].startswith("press")]
        first = next((e for e in sc["row"]
                      if any(tokens["cues"].get(k, {}).get("polarity") == "positive"
                             for k in _cues_of(e, tokens))), None)
        if first is None or len(press) != 1:
            continue                         # not pass 1's subject; the other gates own this
        if first["name"] != press[0]:
            fails.append(
                f"{sc['id']}: the leftmost positive cue is on {first['name']!r}, but the doc "
                f"presses {press[0]!r}.\n"
                "    Pass 1 presses the first positive cue it reaches, so this row directs the "
                "eye to the wrong\n"
                "    ability. Either the cue does not belong on that entry, or the positive "
                "vocabulary is being\n"
                "    used for something other than impending loss — which is a Part 0.5 "
                "decision, not a row edit."
            )
    return fails


def elimination_gate(scenarios: list[dict], tokens: dict) -> list[str]:
    """THE READING RULE, MECHANISED (render-shelf.md Part 0.5 + Part 5).

    *Scan the row left to right and press the first button that is not ruled out.* So for every
    scenario, the **leftmost** entry that is neither swiped (`cd`) nor veiled nor carrying a red
    cue must be the entry the doc calls the press. `weave` is skipped over — it is off the GCD and
    pressed in parallel, so it never competes for the GCD press.

    ⚠ **"Carrying a cue" means carrying a NEGATIVE cue.** Since 2026-08-14 the vocabulary is
    negative *by default* rather than negative-only, and a positive cue must not eliminate its own
    button — `capped` rides ST-8's press, so reading polarity is what keeps this gate meaningful
    instead of making the one scenario it exists to protect unrepresentable. Polarity is declared
    per cue in the shelf; a cue that declares none is treated as negative, because that is the
    reading that can only ever make the gate stricter.
    """
    def eliminating(keys) -> bool:
        return any(tokens["cues"].get(k, {}).get("polarity", "negative") == "negative"
                   for k in (keys or []))

    fails = []
    for sc in scenarios:
        press = [e["name"] for e in sc["row"] if e["verdict"].startswith("press")]
        if len(press) != 1:
            fails.append(f"{sc['id']}: expected exactly one `press*` entry, found {press or 'none'}")
            continue
        first = None
        for e in sc["row"]:
            rule = tokens["verdicts"][e["verdict"]]
            if e["verdict"] == "weave":
                continue                     # off the GCD — pressed alongside, not instead
            if rule["swipe"] or rule["veil"]:
                continue                     # ruled out natively, or by the veil
            if eliminating(rule.get("cues")) or eliminating(e.get("cues")):
                continue                     # ruled out by a red badge
            first = e
            break
        if first is None:
            fails.append(f"{sc['id']}: elimination reaches the END of the row without an "
                         f"un-ruled-out button, but the doc presses {press[0]!r}")
        elif first["name"] != press[0]:
            fails.append(
                f"{sc['id']}: the leftmost un-ruled-out button is {first['name']!r} "
                f"({first['verdict']}), but the doc presses {press[0]!r}.\n"
                "    A left-to-right scan lands on the wrong ability. Either the row is wrong, or "
                "this scenario\n"
                "    genuinely cannot be led by elimination — which is the finding that justifies "
                "a positive cue.\n"
                "    One such cue now exists (`capped`), and it is scoped to impending loss ONLY. "
                "Widening it, or\n"
                "    adding a second, is a shelf decision to take deliberately — not a way to "
                "silence this gate."
            )
    return fails


def cmd_check(args) -> None:
    tokens = load_tokens()
    cfg = SPECS_BUILT[args.spec]
    fails = []

    for line in strict_css(TEMPLATE / "shelf.css"):
        fails.append(line)

    # 0 · the tint guard still has a subject. `assert_tintable` is the shelf's one mechanical
    # promise, and a guard whose subject set quietly emptied keeps passing while guaranteeing
    # nothing — which is exactly what retiring the flipbook rings could have done to it.
    if tokens["badges"].get("tint") != "lane":
        fails.append("nothing declares tint: \"lane\" any more — the Part 4 tint guard has no "
                     "subject and is guaranteeing nothing. If art really did leave the style, "
                     "delete the guard deliberately rather than letting it pass vacuously.")

    # 0b · exactly one positive cue, because pass 1 has no tie-break. Part 0.5's procedure says
    # "scan for A positive cue and press it" — that is unambiguous with one positive cue in the
    # vocabulary and undefined with two, since a row could then wear both and the heuristic would
    # not say which wins. So this is an ORDERING gate, not merely a vocabulary one.
    positives = [k for k, c in tokens["cues"].items() if c.get("polarity") == "positive"]
    if len(positives) > 1:
        fails.append(f"{len(positives)} positive cues declared ({', '.join(sorted(positives))}) — "
                     "Part 0.5 allows exactly one, because a second one is a second pass-1 "
                     "candidate and the procedure says nothing about how two of them rank. "
                     "Rewrite Part 0.5 to define that ordering first, then relax this gate.")

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
                ka = [(e["name"], e["verdict"], e.get("cues")) for e in a["row"]]
                kb = [(e["name"], e["verdict"], e.get("cues")) for e in b["row"]]
                if ka != kb:
                    fails.append(f"{a['id']}: CDM row in scenarios.md differs from the sidecar")
                    for x, y in zip(ka, kb):
                        if x != y:
                            fails.append(f"    doc {x} != sidecar {y}")
                    if len(ka) != len(kb):
                        fails.append(f"    doc has {len(ka)} entries, sidecar {len(kb)}")

    # 1b · both passes of the reading rule hold. Pass 1: a positive cue, being pre-emptive,
    # points at the press. Pass 2: the eye reaches the press by elimination alone.
    fails += positive_gate(doc, tokens)
    fails += elimination_gate(doc, tokens)

    # 0c · the veil is DERIVED, not authored (render-shelf.md Part 2.5). The shelf claims this is
    # "mechanical rather than a promise", and until this gate existed it was a promise: `veil` is
    # hand-written per verdict in tokens.verdicts with nothing reconciling it against the cues that
    # verdict carries. A verdict veiled with no negative cue is the "skipped, and cap will not say
    # why" state Part 2.5 says cannot occur; an un-veiled verdict carrying one is a skip with no dim.
    for key, rule in tokens["verdicts"].items():
        derived = any(tokens["cues"].get(c, {}).get("polarity", "negative") == "negative"
                      for c in (rule.get("cues") or []))
        if bool(rule.get("veil")) != derived:
            fails.append(
                f"verdict {key!r} declares veil={bool(rule.get('veil'))} but its cues derive "
                f"veil={derived} — render-shelf.md Part 2.5 says a row is veiled *iff* it wears at "
                "least one negative cue. Fix the token, not this gate.")

    # 0d · slot 3 is the positive cue's, and only the positive cue's (render-shelf.md Part 1).
    # Position carries polarity there as well as colour, which is only true while nothing negative
    # can land in slot 3 and nothing positive can land beside the negatives on the top edge.
    for key, cue in tokens["cues"].items():
        positive = cue.get("polarity") == "positive"
        if positive and cue.get("slot") != 3:
            fails.append(f"cue {key!r} is positive but sits in slot {cue.get('slot')} — Part 1 puts "
                         "the positive cue in slot 3, down the right edge, so polarity is legible "
                         "from position and not only from colour.")
        if not positive and cue.get("slot") == 3:
            fails.append(f"cue {key!r} is negative but sits in slot 3, which Part 1 reserves for "
                         "the single positive cue. A negative badge there reads as the opposite of "
                         "what it means.")

    # 1c · every declared cue actually draws somewhere. spec.md §3.2 — "a catalog form that
    # loads successfully and then renders nothing is a defect" — and a cue nobody wears is that
    # defect at the shelf level. It matters most for the positive cue, whose whole justification
    # is one scenario: if ST-8 ever stops carrying it, the exception has no subject and should be
    # retired rather than left declared.
    worn = {k for s in doc for e in s["row"]
            for k in list(tokens["verdicts"][e["verdict"]].get("cues") or []) + list(e.get("cues") or [])}
    for key in tokens["cues"]:
        if key not in worn:
            fails.append(f"cue {key!r} is declared in the shelf but no scenario row wears it — "
                         "it renders nowhere, which spec.md §3.2 calls a defect. Give it a "
                         "subject or retire it.")

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

    # 3 · the addon carries the same style as the artifact. Generation buys nothing the first
    # time someone edits one and not the other, so the committed Lua is gated exactly like the
    # committed HTML. Skipped entirely when the gitignored addon checkout is absent — that is a
    # missing clone, not a stale style.
    if not ADDON_SRC.exists():
        _warn(f"no addon checkout at {ADDON_SRC.relative_to(ROOT)} — Style.lua gate skipped")
    elif not STYLE_LUA.exists():
        fails.append(f"no {STYLE_LUA.relative_to(ROOT)} — run: wowkb.capart export lua")
    elif STYLE_LUA.read_text(encoding="utf-8") != style_lua(tokens):
        fails.append(f"{STYLE_LUA.name} disagrees with the shelf — "
                     "run: wowkb.capart export lua")
    if ADDON_SRC.exists():
        want = badge_frames(tokens) + [PLATE_TEXTURE, HALO_TEXTURE]
        missing = [f for f in want if not (BADGE_DIR / f"{f}.tga").exists()]
        if missing:
            fails.append(f"badge art with no shipped texture ({', '.join(missing)}) — "
                         "run: wowkb.capart export badges")

    if fails:
        print("FAIL")
        for f in fails:
            print(f"  {f}")
        sys.exit(1)
    print(f"ok · {args.spec}: scenarios.md matches the sidecar, the artifact is current, "
          "shelf.css holds no literal colors,\n"
          "     the tint guard still has a subject, every veil is derived from its cues' polarity "
          "and the positive\n"
          f"     cue owns slot 3, and all {len(doc)} scenarios read correctly under both passes —\n"
          "     every positive cue sits on its own press, and every press is reached by "
          "elimination alone")


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

    e = sub.add_parser("export", help="write the shelf into the addon (Style.lua + badge art)")
    e.add_argument("what", nargs="?", default="all", choices=["lua", "badges", "all"])
    e.set_defaults(func=cmd_export)

    c = sub.add_parser("check", help="doc-vs-sidecar and artifact-staleness gates")
    c.add_argument("spec", choices=sorted(SPECS_BUILT))
    c.set_defaults(func=cmd_check)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
