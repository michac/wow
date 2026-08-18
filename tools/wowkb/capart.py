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

`check` additionally asserts the **reading rule**, and it asserts it as the ORDERED procedure
`render-shelf.md` Part 0.5 actually defines, not as two independent claims:

    pass 1 — scan for a positive cue; if one is present, press it.
    pass 2 — OTHERWISE scan left to right and press the first entry not ruled out.

`reading_gate` runs that chain. A scenario wearing a positive cue is judged by pass 1 alone, and a
scenario without one by pass 2 alone. **Pass 1 overriding elimination is the entire reason a
positive cue exists** — elimination expresses rank, and "you are wasting a charge right now" is not
a rank claim — so demanding that both passes agree would forbid the one case the exception was
carved for. (It did, until 2026-08-17: the two gates ran independently and every scenario had to
satisfy both.) What keeps pass 1 unambiguous is the separate rule that at most ONE cue may declare
`polarity: "positive"`; that gate is untouched and is what this chain rests on. Two more gates
stand beside it: every declared cue must be worn by some scenario row (a cue that renders nowhere
is `spec.md` §3.2's defect), and slot 3 belongs to the positive cue (`render-shelf.md` Part 1).

Usage:
    uv run python -m wowkb.capart tokens                # resolved tokens + the CSS block
    uv run python -m wowkb.capart assets                # per-asset byte table vs the budget
    uv run python -m wowkb.capart import scenarios      # seed the sidecar from scenarios.md
    uv run python -m wowkb.capart build havoc           # write the artifact
    uv run python -m wowkb.capart export lua            # the same tokens as CombatAssistPlus/Style.lua
    uv run python -m wowkb.capart export ring           # V2's ring textures, one per lane thickness
    uv run python -m wowkb.capart export lab            # Part 7 as Lab.lua + Media/lab/ (gallery only)
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
LAB_LUA = ADDON_SRC / "Lab.lua"
MEDIA_DIR = ADDON_SRC / "Media"
BADGE_DIR = MEDIA_DIR / "badges"
LAB_DIR = MEDIA_DIR / "lab"
# Where the client looks for a vendored texture. Plumbing, not a design number.
MEDIA_TEXTURE_ROOT = "Interface\\AddOns\\CombatAssistPlus\\Media\\"
BADGE_TEXTURE_ROOT = MEDIA_TEXTURE_ROOT + "badges\\"
LAB_TEXTURE_ROOT = MEDIA_TEXTURE_ROOT + "lab\\"
LAB_SHEET_TEXTURE = "stripes"
# `artifact` is annotated in the shelf as a viewing aid the addon does not have, and Part 7's
# `lab` is by construction not the style. Neither may reach `ns.Style`.
#
# ⚠ `lab` staying here is not the same claim it used to be. Since 2026-08-16 a lab entry MAY be
# drawn — by the in-game `/cap style` gallery, on cap-owned frames — because you cannot judge a
# treatment without seeing the client draw it. What it may never do is reach the LIVE OVERLAY. So
# the lab crosses into the addon, but through its OWN file and its OWN global (`ns.LabStyle` in
# `Lab.lua`), never through `ns.Style`: every module already reads `ns.Style`, so a `lab` key on it
# would put the guarantee back on everyone remembering. A separate global makes the reach visible
# and greppable, which is exactly what `cmd_check`'s LabStyle reach gate keys off.
NOT_THE_STYLE = ("artifact", "lab")
# The only two files that may name `ns.LabStyle`: the generated data, and the gallery that draws it.
LAB_READERS = ("Lab.lua", "StylePanel.lua")

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
    # V2's ring art. The client builds a file name from the prefix and a lane's own thickness, so
    # no lane→file map exists anywhere: change a thickness and both sides follow it.
    if "ring" in out:
        out["ring"] = dict(out["ring"], texture_root=MEDIA_TEXTURE_ROOT)
    # V11's hatch sheet, beside the ring. Same reason: the client builds a file name from the
    # prefix and the shelf's own texture name, so no path is spelled out in Lua.
    if "hatch" in out:
        out["hatch"] = dict(out["hatch"], texture_root=MEDIA_TEXTURE_ROOT)
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


def addon_lab(tokens: dict) -> dict:
    """Part 7 as the client gets it — the whole `lab` table, plus where its art landed.

    Underscore keys travel too: `_sheet` is the shared tiling geometry every striped render needs,
    and the gallery cannot draw a stripe without it. Entries are still the non-underscore keys,
    exactly as everywhere else.
    """
    lab = tokens.get("lab") or {}
    out = {k: v for k, v in lab.items()}
    hatch = tokens.get("hatch")
    if hatch:
        # Synthesized, not copied through: the sheet is the STYLE's since L4 was promoted, and the
        # gallery still needs its geometry and its path. Only the tiling fields travel — the
        # style's own rgb/alpha/phase are V11's statement and are not the lab's to borrow.
        out["_sheet"] = {k: hatch[k] for k in ("tile_px", "pitch_px", "duty") if k in hatch}
        out["_sheet"]["direction"] = hatch.get("direction", "down")
        out["_sheet"]["texture_root"] = MEDIA_TEXTURE_ROOT
        out["_sheet"]["texture"] = hatch["texture"]
    return out


def lab_lua(tokens: dict) -> str:
    """`Lab.lua` — Part 7 as its OWN Lua table under its OWN global, for the gallery only.

    Deliberately not a `lab` key on `ns.Style`: every module reads `ns.Style`, so hanging the lab
    off it would make "a lab treatment never reaches the live overlay" a matter of everyone
    remembering. `ns.LabStyle` is greppable, and `capart check` greps it.
    """
    return (
        "-- Lab.lua — GENERATED from specs/render-shelf.md Part 7. Do not edit this file.\n"
        "--   uv run python -m wowkb.capart export lab\n"
        "-- NO AUTHORITY. These treatments are drawn by the `/cap style` GALLERY only, on\n"
        "-- cap-owned frames, so a treatment can be judged in the client before anyone adopts it.\n"
        "-- They must NEVER reach the live overlay: `ns.LabStyle` may be read by StylePanel.lua and\n"
        "-- nothing else, and `capart check` fails the build if any other file names it.\n"
        "local ADDON, ns = ...\n"
        "\n"
        f"ns.LabStyle = {_lua_value(addon_lab(tokens), 0)}\n"
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


# ON THE STYLE'S SHIP PATH (V11) SINCE 2026-08-16, when L4 was promoted and the sheet went with it.
# It was lab art until then, and the comment below is kept because the reasoning still holds: it is
# generated rather than vendored, and it is neutral so every render tints its own copy. `export_lab`
# no longer writes it — `export_hatch` does, to `Media/`, and the gallery reads that same file. The
# retired note read: `export_lab` writes this as a
# TGA and `check` requires it, because the `/cap style` gallery has to draw the real texture in the
# client to be worth looking at. That is NOT authority: promotion is still Part 7 rule 4, moving the
# entry into Parts 1-6 — reaching the LIVE OVERLAY is what a lab treatment still may not do.
def hatch_sheet(params: dict) -> Image.Image:
    """A tileable diagonal stripe sheet, white with the stripe in the alpha channel.

    Blizzard ships no such art (searched 2026-08-16: `stripe` returns only the auction-house
    row banding, `hazard`/`hatch`/`caution` return nothing), so Part 4's rule applies and it is
    authored from a script rather than vendored as a binary mystery. White RGB on every pixel,
    opacity only in alpha: each render multiplies its OWN colour onto it (`SetVertexColor` in
    the client, `mask-image` + `background-color` in CSS), so no hue is ever baked in here.

    Seamless tiling is the whole job. The stripe is a function of the diagonal coordinate
    `d = x + y` (or `x - y`), which repeats with period `pitch_px` — so the sheet's own edges
    line up **iff the pitch divides the tile**, and that is asserted rather than assumed.
    """
    tile = int(params["tile_px"])
    pitch = int(params["pitch_px"])
    duty = float(params["duty"])
    direction = params.get("direction", "down")
    if pitch <= 0 or tile <= 0 or tile % pitch:
        _die(f"hatch: pitch_px {pitch} does not divide tile_px {tile} — the stripe repeats "
             f"every {pitch}px along the diagonal, so a tile that is not a whole number of "
             "pitches shows a visible seam where it wraps. Pick a pitch that divides the tile.")
    if direction not in ("down", "up"):
        _die(f"hatch: direction {direction!r} — expected \"down\" (d = x+y) or \"up\" (x-y)")

    # Supersampled, and drawn ONE PITCH WIDER on every side than the tile that is kept. The
    # LANCZOS kernel is wider than a pixel, so at the sheet's own edge Pillow clamps instead of
    # wrapping and the last column's anti-aliasing comes out wrong — a faint but real seam in a
    # texture whose entire job is to tile. The pattern is periodic in the pitch, so a one-pitch
    # margin is exactly the neighbouring tile, and cropping it off afterwards leaves edge pixels
    # that were filtered against their true neighbours.
    margin = pitch
    side, pb = (tile + 2 * margin) * SHAPE_SS, pitch * SHAPE_SS
    on = round(duty * pb)
    # One period, tiled out to twice the sheet: row y is the same run of bytes, offset. Building
    # it by slice rather than by a per-pixel loop keeps the supersample cheap.
    period = bytes(255 if i < on else 0 for i in range(pb))
    full = period * (2 * side // pb)
    rows = [full[y:y + side] if direction == "down" else full[side - y:2 * side - y]
            for y in range(side)]
    grown = (tile + 2 * margin,) * 2
    mask = (Image.frombytes("L", (side, side), b"".join(rows))
            .resize(grown, Image.LANCZOS)
            .crop((margin, margin, margin + tile, margin + tile)))
    white = Image.new("L", (tile, tile), 255)
    return Image.merge("RGBA", (white, white, white, mask))


# ON THE STYLE'S SHIP PATH (V2). ONE sheet, N frames of the arrival laid out in a grid, stepped
# with SetTexCoord on the same shared ticker the badge sprites walk.
def ring_flipbook(params: dict) -> Image.Image:
    """V2's lane border: a square annulus arriving, as one white-alpha sprite sheet.

    Frame 1 is the ring at its widest — one `gutter_px` inside its cell, so no frame ever touches a
    cell boundary and texture filtering cannot sample the neighbouring frame — at
    `from_alpha`. The last frame is the ring at rest, `travel_px` further in, at full alpha. The
    frames between ease inward, so the arrival is painted into the art rather than produced by
    scaling a frame; a flipbook draws inside its own rect, always, which is why this border can
    never reach a neighbouring row.

    Same house pattern as `shape_images` and `hatch_sheet`: an `L` mask drawn supersampled,
    LANCZOS-downsampled, then merged under pure white so no hue can be baked in.
    """
    from PIL import ImageDraw

    tile = int(params["tile_px"])
    grid = int(params["grid"])
    frames = int(params["frames"])
    thickness = int(params["thickness_px"])
    corner = int(params.get("corner_px", 0))
    travel = int(params.get("travel_px", 0))
    gutter = int(params.get("gutter_px", 0))
    from_alpha = float(params.get("from_alpha", 0.0))
    ease = params.get("smoothing", "OUT")

    side = tile * grid
    if tile <= 0 or side & (side - 1):
        _die(f"tokens.ring: {grid}x{grid} cells of {tile}px is a {side}x{side} sheet, which is not "
             "a power of two — the client wants power-of-two texture dimensions")
    if frames < 2 or frames > grid * grid:
        _die(f"tokens.ring: {frames} frames do not fit a {grid}x{grid} grid (and a one-frame "
             "arrival is a still image, not an arrival)")
    outer = gutter + travel
    if thickness <= 0 or 2 * (outer + thickness) >= tile:
        _die(f"tokens.ring: thickness_px {thickness} plus gutter {gutter} and travel {travel} does "
             f"not leave a transparent centre in a {tile}px cell")
    if corner < 0 or 2 * corner > tile:
        _die(f"tokens.ring: corner_px {corner} does not fit twice across a {tile}px cell")

    def eased(t: float) -> float:
        return 1.0 - (1.0 - t) ** 2 if ease == "OUT" else t

    sheet = Image.new("RGBA", (side, side))
    big = tile * SHAPE_SS
    for i in range(frames):
        t = eased(i / (frames - 1))
        inset = round(gutter + travel * t)
        alpha = from_alpha + (1.0 - from_alpha) * t
        mask = Image.new("L", (big, big), 0)
        draw = ImageDraw.Draw(mask)
        lo, hi = inset * SHAPE_SS, big - 1 - inset * SHAPE_SS
        band = thickness * SHAPE_SS
        r_out = max(corner - inset, 0) * SHAPE_SS

        def rect(box, radius, fill):
            if radius:
                draw.rounded_rectangle(box, radius=radius, fill=fill)
            else:
                draw.rectangle(box, fill=fill)

        rect((lo, lo, hi, hi), r_out, round(alpha * 255))
        rect((lo + band, lo + band, hi - band, hi - band), max(r_out - band, 0), 0)
        cell = Image.merge("RGBA", (Image.new("L", (big, big), 255),) * 3 + (mask,)) \
            .resize((tile, tile), Image.LANCZOS)
        sheet.paste(cell, ((i % grid) * tile, (i // grid) * tile))
    return sheet


def ring_image(tokens: dict) -> Image.Image | None:
    """The sheet that ships, measured under the tint guard on this path and on `export_ring`'s.

    The guard runs over the WHOLE sheet rather than one frame: a sheet whose frames are neutral but
    whose sheet is not would be exactly the bug the guard exists to catch.
    """
    ring = tokens.get("ring")
    if not ring:
        return None
    return ring_flipbook(dict(ring, from_alpha=tokens["arrival"]["from_alpha"],
                              smoothing=tokens["arrival"]["smoothing"]))


def ring_asset(tokens: dict) -> dict | None:
    """V2's ring sheet as the artifact draws it: a `data:` URI plus its measurement.

    The artifact uses it as a `mask-image` over the lane hue and steps `mask-position` at
    `tokens.motion.tick_s`, which is the same art, the same walk and the same rate as the client.
    """
    img = ring_image(tokens)
    if img is None:
        return None
    ring = tokens["ring"]
    measure = uiart.tintability(img)
    assert_tintable("lane border ring sheet (V2)", "capart.ring_flipbook (generated)",
                    ring.get("tint", "none"), measure["mean_saturation"], measure["tintable"])
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    return {"uri": uri, "bytes": len(uri), "size": list(img.size),
            "mean_saturation": measure["mean_saturation"], "tintable": measure["tintable"],
            "frames": ring["frames"], "grid": ring["grid"], "tile_px": ring["tile_px"],
            "thickness_px": ring["thickness_px"], "travel_px": ring.get("travel_px", 0),
            "tint": ring.get("tint", "none")}


def hatch_asset(tokens: dict) -> dict | None:
    """V11's stripe sheet as a data URI, measured and put under the tint guard.

    It measures 0.000 by construction — the point of running the guard on it anyway is that
    nobody can later bake a colour into the generator and have the preview keep its promise.

    One sheet serves both surfaces. V11 draws it as the style and Part 7's remaining stripe
    entries borrow it at their own colours, so there is exactly one texture to keep honest
    rather than two that can drift.
    """
    sheet = tokens.get("hatch")
    if not sheet:
        return None
    img = hatch_sheet(sheet)
    measure = uiart.tintability(img)
    assert_tintable("cooldown hatch sheet (V11)", "capart.hatch_sheet (generated)",
                    sheet.get("tint", "none"), measure["mean_saturation"], measure["tintable"])
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    return {"uri": uri, "bytes": len(uri), "size": list(img.size),
            "mean_saturation": measure["mean_saturation"], "tintable": measure["tintable"],
            "tile_px": sheet["tile_px"], "pitch_px": sheet["pitch_px"],
            "duty": sheet["duty"], "direction": sheet.get("direction", "down")}


def _write_tga(img: Image.Image, name: str, dest: Path = BADGE_DIR) -> tuple[int, int]:
    w, h = img.size
    if w & (w - 1) or h & (h - 1):
        _die(f"{name} is {w}x{h} — the client wants power-of-two texture dimensions")
    # 32-bit RLE, top-left origin — byte-for-byte the header shape of the Kenney TGAs
    # CDMProbe already ships and the client already reads.
    dest.mkdir(parents=True, exist_ok=True)
    img.save(dest / f"{name}.tga", "TGA", compression="tga_rle", orientation=1)
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


def export_ring(tokens: dict) -> list[tuple[str, tuple[int, int]]]:
    """Vendor V2's ring flipbook into `Media/`, beside `Media/badges/` — declared art, not lab art.

    Lab art lives in `Media/lab/` and style art does not, so `ls Media/` still says which is which.
    The tint guard runs here as well as on the artifact path, so a sheet with a hue baked into it
    cannot reach the client through a route the preview never rendered.
    """
    img = ring_image(tokens)
    if img is None:
        return []
    ring = tokens["ring"]
    measure = uiart.tintability(img)
    assert_tintable("lane border ring sheet (V2, ship path)",
                    "capart.ring_flipbook (generated)", ring.get("tint", "none"),
                    measure["mean_saturation"], measure["tintable"])
    return [(ring["texture"], _write_tga(img, ring["texture"], MEDIA_DIR))]


def export_hatch(tokens: dict) -> list[tuple[str, tuple[int, int]]]:
    """Vendor V11's stripe sheet into `Media/`, beside the ring — declared art, not lab art.

    It moved out of `Media/lab/` when L4 was promoted. The gallery now reads this same file
    through `Lab.lua`'s generated `_sheet`, so promotion did not leave two copies behind.
    """
    sheet = tokens.get("hatch")
    if not sheet:
        return []
    img = hatch_sheet(sheet)
    measure = uiart.tintability(img)
    assert_tintable("cooldown hatch sheet (V11, ship path)",
                    "capart.hatch_sheet (generated)", sheet.get("tint", "none"),
                    measure["mean_saturation"], measure["tintable"])
    return [(sheet["texture"], _write_tga(img, sheet["texture"], MEDIA_DIR))]


LAB_PROVENANCE = """\
GENERATED — do not edit, and do not add art here by hand.

This directory is Part 7 art: art that exists only so the `/cap style` gallery can draw a lab
treatment on cap-owned frames. It must never be drawn into a live CDM row.

It is EMPTY today, and the directory itself is not created until something needs it. The stripe
sheet lived here until 2026-08-16, when L4 was promoted to V11 and the sheet became the style's —
it is `Media/stripes.tga` now, generated from `tokens.hatch`, and the gallery reads that one file
rather than keeping a copy that could drift from it.

Art written here is generated rather than vendored, is neutral (white RGB, pattern in alpha) so
every render tints its own copy, and passes the same tint guard the shipped badge art passes.
Vendored CC0 art lives beside its LICENSE.txt in ../badges/.
"""


def export_lab(tokens: dict) -> list[tuple[str, tuple[int, int]]]:
    """Ship the lab's generated art into the addon as 32-bit TGA, under its own directory.

    `Media/lab/` rather than a naming convention inside `Media/badges/`, so "this is lab art" is
    legible from `ls`. The tint guard runs on the ship path exactly as `export_badges` runs it: the
    sheet measures 0.000 by construction, and the point of asserting it anyway is that a future
    edit which bakes a colour into the generator fails here instead of shipping a lie.
    """
    written: list[tuple[str, tuple[int, int]]] = []
    # Nothing here today. The stripe sheet moved to `Media/` with V11's promotion, and the
    # gallery reads it there; this stays because the next lab entry that needs its own art
    # should get it under `Media/lab/` rather than beside the style's.
    if written:
        (LAB_DIR / "PROVENANCE.txt").write_text(LAB_PROVENANCE, encoding="utf-8")
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


def _ring_pos(index: int, grid: int) -> str:
    """A frame's `mask-position` in a grid-times-100% mask. The same walk stepper.js does."""
    def pct(k: int) -> str:
        return f"{(k / (grid - 1)) * 100:.4f}%" if grid > 1 else "0%"
    return f"{pct(index % grid)} {pct(index // grid)}"


def root_css(tokens: dict) -> str:
    s = tokens["surfaces"]
    a, b, r = tokens["arrival"], tokens["badges"], tokens["ring"]

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
        "",
        "  /* V2 · lane border. One ring flipbook, tinted per lane; the frame is chosen by",
        "     --ring-pos, which stepper.js walks at --tick, and the sheet URI is set inline",
        "     (it is a build-time data: URI, not a shelf value). */",
        f"  --arrive-dur: {a['duration_s']}s;",
        f"  --tick: {tokens['motion']['tick_s']}s;",
        f"  --ring-grid: {r['grid']};",
        f"  --ring-frames: {r['frames']};",
        f"  --ring-size: {r['grid'] * 100}% {r['grid'] * 100}%;",
        f"  --ring-rest: {_ring_pos(r['frames'] - 1, r['grid'])};",
        "  --ring-pos: var(--ring-rest);",
    ]
    for lane, t in tokens["lanes"].items():
        lines.append(f"  --lane-{lane.lower()}: {rgba(t['rgb'])};")

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

    # V11 · the cooldown hatch, and Part 7's remaining stripe entries, which borrow its sheet.
    # Geometry is emitted once because two stripes that disagree on pitch cannot interleave;
    # colour and phase are emitted PER RENDER, because they are what tell one condition from
    # another. There is deliberately no shared "striped" property for several renders to feed.
    sheet = tokens.get("hatch")
    if sheet:
        lines += [
            "",
            "  /* V11 + Part 7 · the stripe sheet. The mask URI is set inline by stepper.js (it",
            "     is a build-time data: URI, not a shelf value); the geometry is the shelf's. */",
            f"  --lab-stripe-tile: {sheet['tile_px']}px;",
            f"  --lab-stripe-pitch: {sheet['pitch_px']}px;",
            f"  --hatch-rgb: {rgba(sheet['rgb'], sheet.get('alpha', 1.0))};",
            f"  --hatch-phase: {sheet['pitch_px'] * sheet.get('phase_pct', 0) / 100:.2f}px;",
        ]
    lab = tokens.get("lab") or {}
    if sheet:
        for key, entry in lab.items():
            if key.startswith("_") or not isinstance(entry, dict) or "rgb" not in entry:
                continue
            phase = sheet["pitch_px"] * entry.get("phase_pct", 0) / 100
            lines.append(f"  --lab-{key}-rgb: {rgba(entry['rgb'], entry.get('alpha', 1.0))};")
            lines.append(f"  --lab-{key}-phase: {phase:.2f}px;")
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

    # Lab cells draw real icons on real verdicts, so their ability names are held to exactly the
    # same standard a scenario row's are — an experiment on invented art proves nothing.
    lab_names = set()
    for key, entry in ((k, e) for k, e in (tokens.get("lab") or {}).items()
                       if not k.startswith("_")):
        for cell in entry.get("cells", []):
            name = cell.get("ability")
            if name is None:
                continue
            if name not in roster:
                _die(f"lab.{key}: {name!r} is not in catalog.md's bound-abilities table")
            if cell.get("verdict") and cell["verdict"] not in tokens["verdicts"]:
                _die(f"lab.{key}: verdict {cell['verdict']!r} is not in the closed vocabulary")
            lab_names.add(name)

    used = sorted({e["name"] for sc in scenarios for e in sc["row"]}
                  | set(cfg["lane_sample"].values()) | lab_names)
    missing = [n for n in cfg["lane_sample"].values() if n not in roster]
    if missing:
        _die(f"lane sample {missing} not in the roster")
    icons = icon_assets(used, roster, tokens)
    frames = badge_assets(tokens)
    stripes = hatch_asset(tokens)
    ring = ring_asset(tokens)

    # The base64 budget is a fact to report, not a gate: an oversized page is still a page
    # you can look at, and `wowkb.capart assets` prints the per-asset table that fixes it.
    total = (sum(a["bytes"] for a in icons.values()) + sum(f["bytes"] for f in frames.values())
             + (stripes["bytes"] if stripes else 0) + (ring["bytes"] if ring else 0))

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
        "ring": ring,
        "lab_stripes": stripes,
        "provenance_html": provenance_html(spec, tokens, icons, frames, stripes, ring, total,
                                           when),
    }

    page = (TEMPLATE / "page.html").read_text(encoding="utf-8")
    page = page.replace("/*__ROOT_TOKENS__*/", root_css(tokens))
    page = page.replace("/*__SHELF_CSS__*/", (TEMPLATE / "shelf.css").read_text(encoding="utf-8"))
    page = page.replace("/*__STEPPER_JS__*/", (TEMPLATE / "stepper.js").read_text(encoding="utf-8"))
    page = page.replace("/*__TOKENS_JSON__*/", json.dumps(tokens, separators=(",", ":")))
    page = page.replace("/*__DATA_JSON__*/", json.dumps(data, separators=(",", ":")))
    return BUILT_MARK.format(date=when) + "\n" + page


def provenance_html(spec, tokens, icons, frames, stripes, ring, total, when) -> str:
    cfg = SPECS_BUILT[spec]
    rows = [
        ("render-shelf.md", f"sha {_sha(SHELF)} · Part 6 render-tokens v{tokens['version']}"),
        ("scenarios.md", f"sha {_sha(cfg['scenarios'])}"),
        ("catalog.md", f"sha {_sha(cfg['catalog'])}"),
        ("sidecar", f"{cfg['sidecar'].name} · sha {_sha(cfg['sidecar'])}"),
    ]
    r = tokens["ring"]
    rows.append((
        "border · V2",
        " · ".join(f"<b>{ln}</b>" for ln in tokens["lanes"])
        + f" — one ring flipbook, {r['thickness_px']}px band, tinted per lane with a single "
        "<code>SetVertexColor</code>; the lanes differ by hue alone. One-shot arrival: "
        f"{r['frames']} frames at {tokens['motion']['tick_s']}s = "
        f"{tokens['arrival']['duration_s']}s ({tokens['arrival']['smoothing']}), stepped in place "
        "so nothing ever draws outside the row's own cell; replayed every "
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
    if stripes:
        rows.append((
            "stripe sheet · lab",
            f"{stripes['size'][0]}×{stripes['size'][1]} generated by "
            "<code>capart.hatch_sheet</code> — pitch "
            f"{stripes['pitch_px']}px, duty {stripes['duty']}, {stripes['direction']} · "
            f"measured mean saturation {stripes['mean_saturation']}, so "
            "<code>SetVertexColor</code> takes it to whatever colour the render passes · "
            "declared <code>tint: \"lane\"</code>, which is what puts it under the tint guard · "
            "<b>Part 7, no authority</b> — shipped by <code>export lab</code> to "
            "<code>Media/lab/</code> for the in-game <code>/cap style</code> gallery only, never "
            "a live CDM row · "
            f"{stripes['bytes'] / 1024:.1f} KB b64"
        ))
    if ring:
        rows.append((
            "ring sheet · V2",
            f"{ring['size'][0]}×{ring['size'][1]} generated by <code>capart.ring_flipbook</code> — "
            f"{ring['frames']} frames in a {ring['grid']}×{ring['grid']} grid of "
            f"{ring['tile_px']}px cells, band {ring['thickness_px']}px, travelling "
            f"{ring['travel_px']}px inward across the arrival · measured mean saturation "
            f"{ring['mean_saturation']}, so <code>SetVertexColor</code> takes it to the lane hue · "
            f"declared <code>tint: \"{ring['tint']}\"</code>, which is what puts it under the tint "
            "guard · shipped by <code>export ring</code> to <code>Media/</code>, and drawn here as "
            "<code>mask-image</code> over the lane hue — the same art, the same walk, the same "
            f"rate · {ring['bytes'] / 1024:.1f} KB b64"
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
    ring = tokens.get("ring")
    print("  V2 · lane border (one ring flipbook; the lanes differ by hue alone)")
    for lane, t in tokens["lanes"].items():
        r, g, b = (round(x * 255) for x in t["rgb"])
        print(f"    {lane:<9} rgb({r:>3},{g:>3},{b:>3})")
    a = tokens["arrival"]
    if ring:
        print(f"    art      {ring['texture']}, {ring['frames']} frames in a "
              f"{ring['grid']}x{ring['grid']} grid of {ring['tile_px']}px cells, band "
              f"{ring['thickness_px']}px · declared tint {ring.get('tint', 'none')!r}")
        print(f"    arrival  {ring['frames']} frames at {tokens['motion']['tick_s']}s = "
              f"{a['duration_s']}s {a['smoothing']}, from alpha {a['from_alpha']}, travelling "
              f"{ring.get('travel_px', 0)}px inward — ONE SHOT, no loop, never leaves its own rect")

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

    t = tokens["text"]
    print()
    print(f"  text       max {t['max_hz']} Hz · duty {t['duty']} · alpha floor {t['alpha_floor']} "
          "(MIL-STD-1472F — safety, not taste)")
    print(f"  artifact   arrival replayed every {tokens['artifact']['arrival_replay_s']}s "
          "(VIEWING AID — not the style)")

    borderless = [k for k, v in tokens["verdicts"].items() if not v["border"]]
    badged = [k for k, v in tokens["verdicts"].items() if v.get("cues")]
    print(f"\n  verdicts   {', '.join(tokens['verdicts'])}")
    print(f"    no border  {', '.join(borderless)}")
    print(f"    badged     {', '.join(badged)}")
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
    stripes = hatch_asset(tokens)
    if stripes:
        print(f"{'lab stripe sheet':<40} {'lab':<6} {stripes['bytes'] / 1024:>8.1f}  "
              f"sat {stripes['mean_saturation']} (generated, neutral by construction) · "
              f"{stripes['size'][0]}px tile, pitch {stripes['pitch_px']}px")
    ring = ring_asset(tokens)
    if ring:
        print(f"{'ring flipbook':<40} {'ring':<6} {ring['bytes'] / 1024:>8.1f}  "
              f"sat {ring['mean_saturation']} (generated, neutral by construction) · "
              f"{ring['frames']} frames in {ring['grid']}x{ring['grid']} × {ring['tile_px']}px, "
              f"band {ring['thickness_px']}px")
    for name in used:
        a = icons[name]
        print(f"{name:<40} {'icon':<6} {a['bytes'] / 1024:>8.1f}  spell {a['spell']}")
    total = (sum(f["bytes"] for f in frames.values()) + sum(a["bytes"] for a in icons.values())
             + (stripes["bytes"] if stripes else 0) + (ring["bytes"] if ring else 0))
    cap = tokens["budget"]["max_base64_kb"]
    print("-" * 92)
    print(f"{'TOTAL':<40} {'':<6} {total / 1024:>8.1f}  of {cap} KB budget "
          f"({total / 1024 / cap * 100:.0f}%)")
    print("\nThe lane border (V2) is ONE ring flipbook: every lane draws the same band and differs "
          "by hue alone.")
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
    if what in ("ring", "all"):
        for name, size in export_ring(tokens):
            print(f"  {name + '.tga':<24} {size[0]}x{size[1]} 32-bit → "
                  f"{MEDIA_DIR.relative_to(ROOT)}")
    if what in ("hatch", "all"):
        for name, size in export_hatch(tokens):
            print(f"  {name + '.tga':<24} {size[0]}x{size[1]} 32-bit → "
                  f"{MEDIA_DIR.relative_to(ROOT)}")
    # `lab` is its own target and its own file, for the same reason it is its own global: the lab
    # ships so the `/cap style` gallery can draw it, and nothing about that is the style.
    if what in ("lab", "all"):
        LAB_LUA.write_text(lab_lua(tokens), encoding="utf-8")
        entries = [k for k in (tokens.get("lab") or {}) if not k.startswith("_")]
        print(f"wrote {LAB_LUA.relative_to(ROOT)} — ns.LabStyle, {len(entries)} entries "
              f"({', '.join(entries) or 'none'}) · gallery only, never the live overlay")
        for name, size in export_lab(tokens):
            print(f"  {name + '.tga':<24} {size[0]}x{size[1]} 32-bit → "
                  f"{LAB_DIR.relative_to(ROOT)}")


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

    Called only for scenarios that wear one, by `reading_gate`. A scenario wearing no positive cue
    is not pass 1's subject and passes trivially, which is why the same loop is safe to run over
    the whole set.
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
    scenario, the **leftmost** entry that is neither swiped (`cd`) nor carrying a red cue must be
    the entry the doc calls the press. `weave` is skipped over — it is off the GCD and pressed in
    parallel, so it never competes for the GCD press.

    ⚠ Since the veil was retired (2026-08-16) there are exactly **two** eliminating signals left,
    Blizzard's swipe and cap's negative badge, and that is the point of the change rather than an
    incidental simplification: every scenario still resolves to the same press without a dim doing
    any of the work. If a scenario stops passing here, the reading model has a real hole in it.

    ⚠ **"Carrying a cue" means carrying a NEGATIVE cue.** Since 2026-08-14 the vocabulary is
    negative *by default* rather than negative-only, and a positive cue must not eliminate its own
    button. Polarity is declared per cue in the shelf; a cue that declares none is treated as
    negative, because that is the reading that can only ever make the gate stricter.

    ⚠ **This is pass 2, and pass 2 does not run on a scenario that wears a positive cue.**
    `reading_gate` owns that choice. Calling this directly on every scenario — which `check` did
    until 2026-08-17 — silently re-imposes "both passes must agree", and that forbids the one
    thing a positive cue is for.
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
            if rule["swipe"]:
                continue                     # ruled out natively by Blizzard's own dial
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


def wears_positive(scenario: dict, tokens: dict) -> bool:
    """Does any entry in this row carry a cue the shelf declares positive?"""
    return any(tokens["cues"].get(k, {}).get("polarity") == "positive"
               for e in scenario["row"] for k in _cues_of(e, tokens))


def reading_gate(scenarios: list[dict], tokens: dict) -> list[str]:
    """THE OPERATOR HEURISTIC AS AN ORDERED CHAIN (render-shelf.md Part 0.5).

    Part 0.5 is a procedure with a fallback, not a conjunction of two rules:

        pass 1 — scan for a positive cue; if one is present, press it.
        pass 2 — OTHERWISE scan left to right and press the first entry not ruled out.

    So each scenario is judged by exactly one pass: the one the reader would actually reach. A row
    wearing a positive cue answers to `positive_gate`; every other row answers to
    `elimination_gate`.

    ⚠ **Why this is a chain and not two assertions.** Running both on every scenario means both
    must name the same press — which makes "pass 1 legitimately overrides elimination"
    unrepresentable, and that override is the *whole* justification for having a positive cue at
    all. Elimination expresses rank; "you are wasting a charge right now" is a claim about loss,
    not rank, and it is allowed to jump the queue. Havoc's rung 10 is exactly this: a banked
    Immolation Aura charge outranks buttons sitting to its left, and no row position can say so.

    What keeps the chain honest is the gate that is deliberately NOT relaxed: at most one cue may
    declare `polarity: "positive"`, so "scan for a positive cue" always has one answer. Widening
    that is a Part 0.5 decision — pass 1 says nothing about how two positive cues would rank.
    """
    # Both passes quietly abstain on a row without exactly one press, so the chain has to assert
    # it itself or a malformed row would be judged by neither.
    fails = [f"{sc['id']}: expected exactly one `press*` entry, found "
             f"{[e['name'] for e in sc['row'] if e['verdict'].startswith('press')] or 'none'}"
             for sc in scenarios
             if len([e for e in sc["row"] if e["verdict"].startswith("press")]) != 1]
    positive = [sc for sc in scenarios if wears_positive(sc, tokens)]
    plain = [sc for sc in scenarios if not wears_positive(sc, tokens)]
    return fails + positive_gate(positive, tokens) + elimination_gate(plain, tokens)


def lab_gates(tokens: dict) -> list[str]:
    """PART 7 IN THE ADDON — the four gates that make shipping the lab safe.

    Until 2026-08-16 the lab could not reach the client at all, and that was the guarantee. The
    author retired it for a reason that is hard to argue with: you cannot judge whether a treatment
    *renders* without watching the client render it, and the `/cap style` gallery draws on cap-owned
    frames — it shows nobody a CDM row. So the lab now ships.

    What replaces the old guarantee is gate 3 below. The isolation that actually mattered is
    unchanged and still enforced by `validate_lab_isolation` (nothing in `verdicts`/`cues` may name
    a lab entry); these gates add the second half — the lab arrives in its own file under its own
    global, and exactly two files may reach for it.
    """
    fails: list[str] = []
    lab_keys = [k for k in (tokens.get("lab") or {}) if not k.startswith("_")]

    if not ADDON_SRC.exists():
        if lab_keys:
            _warn(f"no addon checkout at {ADDON_SRC.relative_to(ROOT)} — Lab.lua gates skipped")
        return fails

    # 4 · Style.lua carries no lab. Cheap, and it is what pins `NOT_THE_STYLE`: the live modules all
    # read `ns.Style`, so a lab key appearing there would put every one of them one field access
    # away from a treatment nobody adopted.
    if STYLE_LUA.exists():
        style = STYLE_LUA.read_text(encoding="utf-8")
        leaked = [k for k in lab_keys if k in style]
        if leaked or "LabStyle" in style:
            fails.append(
                f"Style.lua carries the lab ({', '.join(leaked) or 'a LabStyle reference'}) — "
                "Part 7 says nothing below it is the style, and `ns.Style` is what every live "
                "module reads.\n"
                "    `lab` must stay in capart.NOT_THE_STYLE; the lab ships through Lab.lua "
                "(ns.LabStyle) and the gallery alone.")

    # 5 · Lab.lua is current — generated data is worth nothing the first time someone edits one
    # side and not the other, so it is byte-gated exactly as Style.lua is.
    if not lab_keys:
        pass
    elif not LAB_LUA.exists():
        fails.append(f"no {LAB_LUA.relative_to(ROOT)} — run: wowkb.capart export lab")
    elif LAB_LUA.read_text(encoding="utf-8") != lab_lua(tokens):
        fails.append(f"{LAB_LUA.name} disagrees with render-shelf.md Part 7 — "
                     "run: wowkb.capart export lab")

    # 6 · ⚠ THE REACH GATE. This is the mechanical replacement for the guarantee we gave up when the
    # lab was allowed into the client at all. A lab treatment may be DRAWN (by the gallery, on
    # cap-owned frames) and may never be DECIDED WITH (by the live overlay, on a CDM row). Nothing
    # about `ns.LabStyle` being a table stops Overlay/Treatment/Paint/Sense or a catalog from
    # reading it — only this does. Tests are excluded: they do not run in the client, so a spec
    # naming LabStyle is not a live-path reach.
    offenders = []
    for path in sorted(ADDON_SRC.rglob("*.lua")):
        rel = path.relative_to(ADDON_SRC)
        if rel.parts[0] == "tests":
            continue
        if path.name in LAB_READERS:
            continue
        if "LabStyle" in path.read_text(encoding="utf-8"):
            offenders.append(str(rel))
    if offenders:
        fails.append(
            "ns.LabStyle is referenced by " + ", ".join(offenders) + " — a Part 7 lab treatment is "
            "reaching into the LIVE PATH.\n"
            "    The lab is allowed into the client for exactly one reason: the `/cap style` "
            "gallery draws on cap-owned\n"
            "    frames and shows nobody a CDM row, so a treatment can be judged before it is "
            "adopted. Anything that\n"
            "    can put it on a real row makes an experiment load-bearing without anyone deciding "
            "to promote it, which\n"
            "    is what render-shelf.md Part 7 exists to prevent. Only "
            + " and ".join(LAB_READERS) + " may name it.\n"
            "    A treatment leaves the lab by being MOVED into Parts 1-6 (rule 4), never by being "
            "read from here.")

    # 7 · the lab art is present — the analogue of the badge-texture gate. The gallery can only
    # answer "does this render?" if the real texture is on disk for the client to load.
    lab = tokens.get("lab") or {}
    for key, texture in (("_sheet", LAB_SHEET_TEXTURE),):
        if lab.get(key) and not (LAB_DIR / f"{texture}.tga").exists():
            fails.append(f"lab.{key} declares a texture but {LAB_DIR.relative_to(ROOT)}/"
                         f"{texture}.tga is missing — run: wowkb.capart export lab")
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
    if tokens["badges"].get("tint") != "lane" and (tokens.get("ring") or {}).get("tint") != "lane":
        fails.append("nothing declares tint: \"lane\" any more — the Part 4 tint guard has no "
                     "subject and is guaranteeing nothing. If art really did leave the style, "
                     "delete the guard deliberately rather than letting it pass vacuously.")

    # 0a · V2's cadence is stated three times and must agree. The frame count is what the sheet is
    # generated with, the tick is what the shared ticker runs at, and the duration is what
    # `ShouldSnap` rate-limits on — a disagreement means the border rests mid-arrival or a second
    # snap can start over the first.
    ring, motion = tokens.get("ring"), tokens.get("motion")
    if ring and motion:
        span = ring["frames"] * motion["tick_s"]
        if abs(span - tokens["arrival"]["duration_s"]) > 1e-9:
            fails.append(
                f"tokens.ring.frames ({ring['frames']}) × tokens.motion.tick_s "
                f"({motion['tick_s']}) = {span:g}s, but tokens.arrival.duration_s is "
                f"{tokens['arrival']['duration_s']}s. The frame walk IS the arrival (render-shelf "
                "V2), so the three have to agree.")

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

    # 1b · the reading rule holds, as the ORDERED chain Part 0.5 defines: a row wearing a
    # positive cue is judged by pass 1, every other row by pass 2. Not both on both — that is
    # what made a legitimate pass-1 override unrepresentable.
    fails += reading_gate(doc, tokens)

    # 0c · RETIRED 2026-08-16 with the veil itself. It reconciled each verdict's hand-written
    # `veil` against the polarity of the cues that verdict carried; the veil no longer exists as a
    # primitive, so the gate has no subject. There is nothing to put in its place: a row's skip is
    # now said once, by the badge, and a rule that a badge implies a badge is not a rule.

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
        # 3b · V2's ring sheet, present AND current. Existence alone would keep passing over a
        # sheet nobody regenerated after a token edit, which is the whole failure mode.
        img = ring_image(tokens)
        if img is not None:
            path = MEDIA_DIR / f"{tokens['ring']['texture']}.tga"
            if not path.exists():
                fails.append(f"no {path.relative_to(ROOT)} — run: wowkb.capart export ring")
            else:
                buf = io.BytesIO()
                img.save(buf, "TGA", compression="tga_rle", orientation=1)
                if buf.getvalue() != path.read_bytes():
                    fails.append(f"{path.name} disagrees with tokens.ring — "
                                 "run: wowkb.capart export ring")
        # 3c · V11's hatch sheet, on the same terms as the ring. It is drawn on the live overlay
        # AND borrowed by the gallery, so a stale sheet is wrong in two places at once.
        if tokens.get("hatch"):
            path = MEDIA_DIR / f"{tokens['hatch']['texture']}.tga"
            if not path.exists():
                fails.append(f"no {path.relative_to(ROOT)} — run: wowkb.capart export hatch")
            else:
                buf = io.BytesIO()
                hatch_sheet(tokens["hatch"]).save(buf, "TGA", compression="tga_rle",
                                                  orientation=1)
                if buf.getvalue() != path.read_bytes():
                    fails.append(f"{path.name} disagrees with tokens.hatch — "
                                 "run: wowkb.capart export hatch")
        # 3d · the sheet moved to Media/ when V11 was promoted; a leftover copy under Media/lab/
        # is a second texture that can silently drift from the one that ships.
        stale = LAB_DIR / f"{LAB_SHEET_TEXTURE}.tga"
        if stale.exists() and not (tokens.get("lab") or {}).get("_sheet"):
            fails.append(f"{stale.relative_to(ROOT)} is left over from before V11's promotion — "
                         "the gallery reads Media/stripes.tga now. Delete it.")

    fails += lab_gates(tokens)

    if fails:
        print("FAIL")
        for f in fails:
            print(f"  {f}")
        sys.exit(1)
    print(f"ok · {args.spec}: scenarios.md matches the sidecar, the artifact is current, "
          "shelf.css holds no literal colors,\n"
          "     Style.lua, Media/ring.tga and Media/stripes.tga agree with the shelf and the "
          "arrival's frames × tick match its duration,\n"
          "     the tint guard still has a subject and the positive\n"
          f"     cue owns slot 3, and all {len(doc)} scenarios read correctly under the pass they\n"
          "     actually reach — a row wearing the positive cue presses it, every other row is "
          "reached by elimination.\n"
          "     Part 7: Style.lua carries no lab, Lab.lua and Media/lab/ are current, and "
          "ns.LabStyle is reached\n"
          f"     by {' and '.join(LAB_READERS)} only — the lab is drawable in the gallery and "
          "unreachable from the live overlay")


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

    e = sub.add_parser("export",
                       help="write the shelf into the addon (Style.lua + badge art + Lab.lua)")
    e.add_argument("what", nargs="?", default="all",
                   choices=["lua", "badges", "ring", "hatch", "lab", "all"])
    e.set_defaults(func=cmd_export)

    c = sub.add_parser("check", help="doc-vs-sidecar and artifact-staleness gates")
    c.add_argument("spec", choices=sorted(SPECS_BUILT))
    c.set_defaults(func=cmd_check)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
