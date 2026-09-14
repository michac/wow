"""Generate the Smart Glo profile viewer — a static site built from `rules/*.sg`.

    uv --directory ../../tools run python ../projects/smart-glo/tool/gen_site.py
    uv run python -m wowkb.serve ../projects/smart-glo/site \
        --watch ../projects/smart-glo/rules \
        --on-change 'uv --directory ../../tools run python ../projects/smart-glo/tool/gen_site.py'

⚠ **Generated — never hand-edit `site/`.** Edit a `.sg` file, or this script.

Three things the site shows, and one rule about each:

* **The table.** Subject / when / bind / urgent, from `wowkb.smartglo.parse` — the same
  parser the checker runs, so a page that renders is a profile that checks.
* **The commentary.** The `--` block above each glow, which the parser drops on the floor
  and which is most of what a profile is worth. Lifted out of the source text by position:
  a comment block touching a `glow` line belongs to it, one separated by a blank line is a
  section note, and one written as `-- ---- title ----` is a section heading.
* **The glow prototype.** A simulation of the mark on a Cooldown Manager icon.
  ⚠ Every number in it is READ OUT OF `Look.lua` at build time — the spin period, the
  cycle, the hold/cross wave, the pulse scale, the palette. Nothing here is a taste
  decision, and nothing may be hardcoded: if the addon is retuned this page follows, and
  if a constant is renamed this script fails loudly rather than drawing a stale picture.
"""

import html
import json
import math
import re
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter

from wowkb import smartglo as sg

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "rules"
ADDON = ROOT / "addon" / "SmartGlo"
OUT = ROOT / "site"
REPO = ROOT.parents[1]
ICON_CACHE = REPO / "raw" / "uiart" / "icons"

# --------------------------------------------------------------------------- Look.lua

def read_look() -> dict:
    """The drawing constants, out of the addon rather than out of this file.

    Each one is REQUIRED: a rename upstream must break the build, because the alternative
    is a prototype that keeps drawing last month's glow and looks fine doing it."""
    text = (ADDON / "Look.lua").read_text()

    def number(name):
        m = re.search(rf"^Look\.{name}\s*=\s*([\d.]+)", text, re.M)
        if m is None:
            raise SystemExit(f"Look.lua no longer defines Look.{name} — gen_site.py is stale")
        return float(m.group(1))

    def string(name):
        m = re.search(rf'^Look\.{name}\s*=\s*"([^"]+)"', text, re.M)
        if m is None:
            raise SystemExit(f"Look.lua no longer defines Look.{name} — gen_site.py is stale")
        return m.group(1)

    def rgb(name):
        m = re.search(rf"^Look\.{name}\s*=\s*\{{\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\s*\}}",
                      text, re.M)
        if m is None:
            raise SystemExit(f"Look.lua no longer defines Look.{name} — gen_site.py is stale")
        return [float(v) for v in m.groups()]

    palette = {}
    block = re.search(r"^local PALETTE = \{(.*?)^\}", text, re.M | re.S)
    for name, r, g, b in re.findall(
            r"(\w+)\s*=\s*\{\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)\s*\}", block.group(1)):
        palette[name] = [float(r), float(g), float(b)]

    cycles = {}
    block = re.search(r"^local CYCLES = \{(.*?)^\}", text, re.M | re.S)
    for name, pair in re.findall(r'(\w+)\s*=\s*\{([^}]*)\}', block.group(1)):
        cycles[name] = re.findall(r'"(\w+)"', pair)

    # `Look.Spin` turns -360 degrees; the sign is the direction and the page needs it.
    degrees = re.search(r"rotation:SetDegrees\((-?\d+)\)", text)

    return {
        "default": string("DEFAULT"),
        "fraction": number("FRACTION"),
        "spinSeconds": number("SPIN_SECONDS"),
        "spinDegrees": float(degrees.group(1)) if degrees else -360.0,
        "cycleSeconds": number("CYCLE_SECONDS"),
        "cycleCross": number("CYCLE_CROSS"),
        "pulseSeconds": number("PULSE_SECONDS"),
        "pulseScale": number("PULSE_SCALE"),
        "occlude": number("OCCLUDE"),
        "plateScale": number("PLATE_SCALE"),
        "plateAlpha": number("PLATE_ALPHA"),
        "plateRgb": rgb("PLATE_RGB"),
        "palette": palette,
        "cycles": cycles,
    }


# ⚠ THE NUMBERS ON THESE PAGES THAT ARE NOT READ OUT OF `Look.lua`, and the only ones — the
# geometry and motion of candidates the addon does not draw. `Look.lua` cannot carry them: it
# states what the addon does now, and a constant kept there for a prototype is a constant that
# reads as shipped. Nothing on `prototype.html` touches any of these; that page is the shipping
# look and every number in it comes from the addon.
#
# * plate — the RETIRED black scrim's geometry. `markScale`/`plateScale` are fractions of
#   FRACTION, and ⚠ the footprint they are fractions OF is the lab's, not the addon's: these
#   candidates were drawn against FRACTION 0.72. The shipping plate is purple and comes out of
#   `Look.lua` like everything else on `current`; these numbers only draw the old black one.
# * bounce — urgent as a drop rather than a size pulse. Built and flown; see `## Unproven` in
#   backlog.md for what that flight settled.
LAB = {
    "footprint": 0.72,
    "markScale": 0.74, "plateScale": 1.04, "plateAlpha": 0.55,
    "urgentRate": 1.18,
    "bounceSeconds": 1.8, "bounceHeight": 0.26, "bounceE": 0.42,
    "bounceHops": 4, "bounceRest": 0.26,
}


def page_look() -> dict:
    """What the pages are built from: the addon's constants, plus the lab-only candidate ones.

    ⚠ The lab keys are namespaced under `lab` so nothing on a page can read one by accident and
    present it as the addon's."""
    look = read_look()
    look["lab"] = LAB
    return look


LOOK = page_look()


# ------------------------------------------------------------------ style candidates
#
# ⚠ **`current` is what the addon draws; everything after it is a PROTOTYPE.** The rest exist
# to be looked at, and several are the steps this look was arrived at through — they are kept
# because "why not the simpler one" is a question the page should be able to answer.
#
# A layer is (mask, fill, scale, spin). `scale` multiplies `Look.FRACTION`; `spin` is a
# multiplier on the rotation, so -1 counter-turns. Fills: `tint` is the live cycle, `a`/`b`
# are the cycle's two hues held STATIC, and a literal is drawn as written.
#
# A candidate that swings dark to bright needs no `cycle` of its own — `tint` IS that swing
# now, straight out of `Look.lua`'s `alarm`. What carries explicit endpoints is the candidates
# that PREDATE it, so the page can still draw the purple↔yellow cycle it replaced; `purple` is
# still in the palette, but the cycle that used it is gone and HUE is the only record of it.
HUE = [[0.77, 0.52, 1.00], [1.00, 0.82, 0.25]]
# The lab's own geometry, as multiples of the SHIPPING FRACTION, so a candidate drawn here is
# the size it was drawn at when it was judged even though the shipping mark has since shrunk.
_F = LOOK["lab"]["footprint"] / LOOK["fraction"]
PLATE = f'rgba(0,0,0,{LOOK["lab"]["plateAlpha"]:g})'
# ...and the SHIPPING plate, straight out of `Look.lua`: `PLATE_RGB` at `PLATE_ALPHA`, sized as
# a multiple of the mark rather than of the icon.
_P = LOOK["plateRgb"]
SHIP_PLATE = "rgba(%d,%d,%d,%g)" % (round(_P[0] * 255), round(_P[1] * 255), round(_P[2] * 255),
                                    LOOK["plateAlpha"])
MARK = LOOK["lab"]["markScale"] * _F
PLATE_AT = LOOK["lab"]["plateScale"] * _F

STYLES = [
    {
        "key": "current",
        "name": "Current",
        "blurb": "One hexagon, tinted by the black\u2194yellow cycle, over a translucent purple "
                 "plate of the same shape that turns with it; <strong>urgent</strong> pops the "
                 "mark 1.35\u00d7 and back on a 0.45s loop. The mark is 0.53 of the icon \u2014 it "
                 "was 0.72, and small reads better: a hexagon that nearly fills the icon "
                 "competes with the art it is marking.",
        "cost": "Shipping. Two Textures, two Rotations started in one call, one shared colour "
                "ticker, one Scale animation. Only the mark cycles and only the mark pops.",
        "layers": [
            {"mask": "hex-fill", "fill": SHIP_PLATE, "scale": LOOK["plateScale"]},
            {"mask": "hex-white", "fill": "tint", "scale": 1.0},
        ],
    },
    {
        "key": "scrim",
        "name": "Purple\u2194yellow on a scrim",
        "blurb": "The RETIRED hue cycle, shrunk over a translucent black plate the same shape. "
                 "The plate supplies the contrast, so the mark no longer has to win against "
                 "the icon underneath it.",
        "cost": "Two Textures, and only the mark joins the colour ticker.",
        "layers": [
            {"mask": "hex-fill", "fill": PLATE, "scale": PLATE_AT},
            {"mask": "hex-white", "fill": "tint", "scale": MARK, "cycle": HUE},
        ],
    },
    {
        "key": "triangle",
        "name": "Purple\u2194yellow, triangle on a scrim",
        "blurb": "Three-fold symmetry instead of six, so the same rotation changes the "
                 "silhouette twice as much. A regular polygon approaches a circle as its "
                 "sides multiply \u2014 the hexagon's inscribed-to-circumscribed radius ratio is "
                 "0.866, already nearly a disc before any blur, where the triangle's is 0.5.",
        "cost": "Two Textures and a new master file; the plate and rim derivations follow it "
                "automatically.",
        "layers": [{"mask": "hex-fill", "fill": PLATE, "scale": PLATE_AT},
                   {"mask": "tri-white", "fill": "tint", "scale": 0.84 * _F,
                    "cycle": HUE}],
    },
    {
        "key": "tri-lumen",
        "name": "Dark \u2194 bright, triangle on a scrim",
        "blurb": "The brightness cycle on the three-fold mark. The two changes are aimed at "
                 "different things and do not overlap: the cycle buys luminance modulation, "
                 "which is what survives the acuity loss, and the triangle buys a silhouette "
                 "whose rotation is still legible once blurred.",
        "cost": "Two Textures and the ticker the scrim already needs, plus the new triangle "
                "master.",
        "axes": "Plain does two things on two channels \u2014 brightness swings, silhouette turns. "
                "\u26a0 Doing two things is not free: a busier plain state has more to lose to a "
                "crowded screen.",
        "layers": [
            {"mask": "hex-fill", "fill": PLATE, "scale": PLATE_AT},
            {"mask": "tri-white", "fill": "tint", "scale": 0.84 * _F},
        ],
    },
    {
        "key": "scrim-lumen",
        "name": "Dark \u2194 bright, urgent pulses",
        "blurb": "The shipping plate and brightness cycle, with urgent still on the SIZE "
                 "channel. The step before the bounce, and the one that shows what moving "
                 "urgent off size bought.",
        "cost": "The plate's two Textures and the ticker. No new animation.",
        "axes": "Plain modulates brightness against a fixed dark ground; urgent scales the "
                "mark. Different channels \u2014 but both read as <em>more of the same thing, "
                "here</em>.",
        "layers": [
            {"mask": "hex-fill", "fill": PLATE, "scale": PLATE_AT, "still": True},
            {"mask": "hex-white", "fill": "tint", "scale": MARK},
        ],
    },
    {
        "key": "scrim-lumen-bob",
        "name": "Dark \u2194 bright, urgent bounces at plain\u2019s rate",
        "blurb": "The shipping look minus the 18% rate: urgent bounces, but its cycle and "
                 "spin stay locked to every plain glow on the bar. Kept to show what the rate "
                 "alone is worth.",
        "cost": "The shipping cost minus one multiplier on the phase.",
        "layers": [
            {"mask": "hex-fill", "fill": PLATE, "scale": PLATE_AT, "still": True},
            {"mask": "hex-white", "fill": "tint", "scale": MARK},
        ],
        "urgentMotion": "bob",
    },
    {
        "key": "scrim-lumen-bob-fast",
        "name": "Dark \u2194 bright, urgent bounces and runs fast",
        "blurb": "The bounce, plus <strong>urgent</strong> running its spin and its brightness "
                 "cycle 18% quicker than plain \u2014 not fast enough to read as a speed, fast "
                 "enough that an urgent glow drifts out of phase with every plain one beside it.",
        "cost": "\u26a0 <strong>Built and flown, then reverted</strong> (v0.3.65\u201368). Everything "
                "here is drawable, and cheaply: the plate is a second Texture, the rate is one "
                "multiplier on a phase that stays a pure function of <code>GetTime()</code>, and "
                "the drop is a chain of ordered Translations whose offsets accumulate. Three "
                "things the flight taught, all of them now in the KB or the addon: a "
                "<code>SetVertexColor</code> fourth argument is the same channel "
                "<code>SetAlpha</code> writes; a plate must be owned by whoever owns the mark\u2019s "
                "alpha, or a sealed bind lights it with no mark on it; and a dark end at 30% of "
                "the bright one reads grey rather than absent.",
        "axes": "Plain modulates BRIGHTNESS in place, urgent modulates POSITION \u2014 the widest "
                "separation on this page, and it is still not what came back. Measured motion is "
                "not the same as read-at-a-glance, which is the warning under the blur slider.",
        "urgentRate": LOOK["lab"]["urgentRate"],
        "urgentMotion": "bob",
        "layers": [
            {"mask": "hex-fill", "fill": PLATE, "scale": PLATE_AT, "still": True},
            {"mask": "hex-white", "fill": "tint", "scale": MARK},
        ],
    },
]

# The backgrounds each candidate is judged against. ⚠ Chosen to DISAGREE with the palette:
# Avenger's Shield is the gold that swallows the BRIGHT half of the cycle and Blessed Hammer
# is the dark art that swallows the dark half, so a style that survives both is not merely
# surviving one accident of art. Shield of the Righteous is kept for the retired purple cycle.
BACKDROPS = [
    (31935, "Avenger's Shield", "gold — eats the yellow phase"),
    (53600, "Shield of the Righteous", "violet — ate the retired purple phase"),
    (26573, "Consecration", "orange fire, high luminance"),
    (204019, "Blessed Hammer", "dark — eats the dark phase"),
    (633, "Lay on Hands", "pale, busy"),
]

# The icon the prototype draws under the mark. Any spell works; this one is in every
# profile's subject list and its art is the yellow-heavy Paladin palette the `alarm` cycle
# exists to survive (`Look.lua`, CYCLES).
PROTOTYPE_SPELL = 31935


# ----------------------------------------------------------------------- source text

GLOW_RE = re.compile(r'^glow\s+"(.*)"\s*$')
ON_RE = re.compile(r"^\s+on\s+(\S+)\s*$")


def split_source(text: str):
    """Walk the file once and hand back (intro, items).

    A comment block is attached by ADJACENCY, which is the only signal the source carries:
    touching a `glow` line it is that glow's note, separated by a blank it is prose in its
    own right, and matching `-- ---- title ----` it is a section heading. Everything before
    `spec` is the profile's intro."""
    lines = text.splitlines()
    intro, items, block, i = [], [], [], 0

    # The header: comment lines up to the `spec` declaration.
    while i < len(lines) and not lines[i].startswith("spec "):
        if lines[i].startswith("--"):
            intro.append(strip_comment(lines[i]))
        i += 1
    i += 1

    while i < len(lines):
        line = lines[i]
        if line.startswith("--"):
            block.append(line)
        elif (m := GLOW_RE.match(line)) is not None:
            # The `on` word as WRITTEN. A subject can answer to more than one name — the rule
            # says `holy_bulwark` and the symbol table's canonical slug for 432459 is
            # `holy_armaments` — and a page that renamed it would be describing a button the
            # profile never mentions.
            spelling = None
            for ahead in lines[i + 1:i + 6]:
                if (o := ON_RE.match(ahead)) is not None:
                    spelling = o.group(1)
                    break
            items.append({"kind": "glow", "name": m.group(1), "on": spelling,
                          "note": render_block(block)})
            block = []
        elif line.strip() == "":
            if block:
                items.append(classify(block))
                block = []
        i += 1
    if block:
        items.append(classify(block))
    return "\n".join(intro).strip(), items


def classify(block):
    head = strip_comment(block[0]).strip()
    m = re.fullmatch(r"-{4,}\s*(.+?)\s*-*", head)
    if m is not None:
        return {"kind": "section", "title": m.group(1),
                "note": render_block(block[1:])}
    return {"kind": "note", "note": render_block(block)}


def strip_comment(line: str) -> str:
    return re.sub(r"^--\s?", "", line)


def render_block(block) -> str:
    """Comment lines to paragraphs. A bare `--` is the author's paragraph break, and the
    `⚠` blocks are visually distinct in the source so they stay distinct here.

    ⚠ An INDENTED comment line is a shell command, not prose. Wrapping one into a paragraph
    runs two `uv run` invocations together into a single unusable line, which is what the
    first cut of this did — so indentation switches the renderer into a code block."""
    paras, cur, code = [], [], []

    def flush():
        if cur:
            paras.append(("p", " ".join(cur)))
            cur.clear()
        if code:
            paras.append(("pre", "\n".join(code)))
            code.clear()

    for line in block:
        text = strip_comment(line).rstrip()
        if text.strip() == "":
            flush()
        elif text.startswith("  "):
            if cur:
                paras.append(("p", " ".join(cur)))
                cur.clear()
            code.append(text.strip())
        else:
            if code:
                paras.append(("pre", "\n".join(code)))
                code.clear()
            cur.append(text.strip())
    flush()

    out = []
    for kind, text in paras:
        if kind == "pre":
            out.append(f"<pre>{html.escape(text)}</pre>")
        else:
            cls = "warn" if text.startswith("⚠") else ""
            out.append(f'<p class="{cls}">{inline(text)}</p>')
    return "\n".join(out)


def inline(text: str) -> str:
    """`code` and **bold**, the only two markups the profiles actually use."""
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    # The profiles write an em-dash as `--`, because a .sg file is ASCII by habit.
    text = re.sub(r"(?<=\s)--(?=\s)", "—", text)
    return text


# ----------------------------------------------------------------------------- names

def display_names() -> dict:
    """id → the name the game shows, harvested from every `ability-inventory.md` in the KB.

    The symbol table only carries slugs, and a slug reads badly in a table — `avengers_shield`
    against `Avenger's Shield`. The inventories are generated from the API, so the apostrophes
    and casing are the client's own rather than a de-slugging guess."""
    names = {}
    row = re.compile(r"^\|\s*\d+\s*\|\s*([^|]+?)\s*\|\s*`(\d+)`")
    for path in (REPO / "knowledge" / "classes").rglob("ability-inventory.md"):
        for line in path.read_text().splitlines():
            m = row.match(line)
            if m is not None:
                names.setdefault(int(m.group(2)), m.group(1).strip())
    return names


SMALL = {"of", "the", "and", "in", "on", "to", "a", "an", "for"}


def deslug(slug: str) -> str:
    """`word_of_glory` → `Word of Glory`. The id suffix a scoped name may carry is dropped;
    the table prints the id separately where it matters."""
    words = re.sub(r"_\d+$", "", slug).split("_")
    return " ".join(w.capitalize() if i == 0 or w not in SMALL else w
                    for i, w in enumerate(words))


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", text.lower())


def by_norm(names: dict) -> dict:
    """normalised name → the name as the client spells it, so a SLUG can borrow its
    punctuation. `avengers_shield` and `Avenger's Shield` normalise alike."""
    return {_norm(v): v for v in names.values()}


def pretty_slug(slug: str, index: dict) -> str:
    """The rule's own word, with the apostrophes put back. Falls through to plain
    de-slugging for anything the inventory does not carry."""
    return index.get(_norm(re.sub(r"_\d+$", "", slug))) or deslug(slug)


def pretty(spell_id: int, spec_key: str, kind: str, names: dict) -> str:
    """The name to print, and the tie-break matters.

    ⚠ **The rule's own word wins.** The inventory name is used only to fix punctuation and
    casing the slug cannot carry — `avengers_shield` → `Avenger's Shield`. Where the two
    genuinely DISAGREE the slug is kept, because an id can be one thing in the rule language
    and another in the inventory: 432459 is `holy_bulwark` to a rule and "Holy Armaments" to
    the ability table, and a page that printed the second would name a button the profile
    never mentions."""
    slug = sg._name_in(spec_key, spell_id, kind)
    shown = names.get(spell_id)
    if slug is None:
        return shown or str(spell_id)
    if shown and _norm(shown) == _norm(slug):
        return shown
    return pretty_slug(slug, by_norm(names))


# ------------------------------------------------------------------------- rendering

def term_html(node, spec_key, names) -> str:
    """The `when` expression, rendered as the source spells it but with real spell names.

    Rendering from the AST rather than scraping the line is deliberate: what the page shows
    is then what the CHECKER read, so a page cannot agree with a comment while disagreeing
    with the rule."""
    t = node.get("t")
    if t == "and":
        return " <span class=op>and</span> ".join(
            term_html(x, spec_key, names) for x in node["terms"])
    if t == "or":
        return " <span class=op>or</span> ".join(
            term_html(x, spec_key, names) for x in node["terms"])
    if t == "not":
        return "<span class=op>not</span> " + term_html(node["term"], spec_key, names)
    if t == "resource":
        return (f'<span class=res>{html.escape(node["power"].replace("_", " "))}</span> '
                f'{html.escape(node["cmp"])} {node["value"]}')
    kind = "aura" if t == "aura" else "ability"
    name = pretty(node["spell"], spec_key, kind, names)
    return f'<span class=fn>{t}</span>(<span class=sp>{html.escape(name)}</span>)'


def bind_html(bind, spec_key, names) -> str:
    fam = bind.get("family")
    if fam == "health":
        return f'<span class=sealed>health {html.escape(bind["cmp"])} {bind["percent"]:g}%</span>'
    if fam == "count":
        name = pretty(bind["aura"], spec_key, "aura", names)
        return (f'<span class=sealed><span class=sp>{html.escape(name)}</span> '
                f'stacks ≥ {bind["threshold"]}</span>')
    if fam == "presence":
        # `unit` and `filter` are what the parser resolved the surface's optional
        # `on <unit>` / `mine` into, so the page shows the resolution rather than the
        # shorthand — which is the half an author gets wrong.
        name = pretty(bind["aura"], spec_key, "aura", names)
        extra = f' on <span class=res>{html.escape(bind.get("unit", "player"))}</span>'
        if bind.get("filter"):
            extra += f' <span class=id>{html.escape(bind["filter"])}</span>'
        return f'<span class=sealed><span class=sp>{html.escape(name)}</span> is up{extra}</span>'
    if fam == "duration":
        name = pretty(bind["spell"], spec_key, "ability", names)
        if bind.get("cmp") == "outside":
            body = f'cooldown outside {bind["lo"]:g}–{bind["hi"]:g}s'
        else:
            body = f'cooldown {html.escape(bind["cmp"])} {bind["seconds"]:g}s'
        if bind.get("absent"):
            body += f' <span class=id>absent {html.escape(bind["absent"])}</span>'
        return f'<span class=sealed><span class=sp>{html.escape(name)}</span> {body}</span>'
    return f"<span class=sealed>{html.escape(json.dumps(bind))}</span>"


def icon_name(spell_id: int) -> str:
    return f"icons/{spell_id}.png"


# ------------------------------------------------------------------------------ page

def profile_page(path: Path, look: dict, names: dict) -> dict:
    text = path.read_text()
    glows = sg.parse(text)
    spec_key = sg._spec_key(text) if hasattr(sg, "_spec_key") else spec_of(text)
    intro, items = split_source(text)

    norm_index = by_norm(names)
    by_name = {g["name"]: g for g in glows}
    subjects = []

    rows, cards = [], []
    for item in items:
        if item["kind"] == "section":
            cards.append(f'<h2 class=sect>{inline(item["title"])}</h2>\n{item["note"]}')
            rows.append(f'<tr class=sectrow><td colspan=5>{inline(item["title"])}</td></tr>')
            continue
        if item["kind"] == "note":
            cards.append(f'<div class=aside>{item["note"]}</div>')
            continue
        g = by_name.get(item["name"])
        if g is None:
            continue
        subj = g["subject"]
        subjects.append(subj)
        subj_name = (pretty_slug(item["on"], norm_index) if item.get("on")
                     else pretty(subj, spec_key, "ability", names))
        when = term_html(g["when"], spec_key, names) if g.get("when") else "<span class=none>—</span>"
        bind = bind_html(g["bind"], spec_key, names) if g.get("bind") else "<span class=none>—</span>"
        urgent = '<span class=urg>urgent</span>' if g.get("urgent") else ""
        icon = (f'<img class=ic src="{icon_name(subj)}" alt="" '
                f'title="{html.escape(subj_name)} · {subj}">')

        rows.append(
            f"<tr><td class=icd>{icon}</td>"
            f"<td class=nm>{html.escape(g['name'])} {urgent}</td>"
            f"<td class=sj>{html.escape(subj_name)}</td>"
            f"<td class=cond>{when}</td><td class=cond>{bind}</td></tr>")

        cards.append(
            f'<article class="card{" u" if g.get("urgent") else ""}">'
            f'<header>{icon}<div><h3>{html.escape(g["name"])} {urgent}</h3>'
            f'<div class=subj>on <span class=sp>{html.escape(subj_name)}</span> '
            f'<span class=id>{subj}</span></div></div></header>'
            f'<div class=terms><div><span class=lbl>when</span> {when}</div>'
            + (f'<div><span class=lbl title="the one sealed leaf a glow may spend">bind</span>'
               f' {bind}</div>' if g.get("bind") else "")
            + f'</div>{item["note"]}</article>')

    title = path.stem.replace("-", " ")
    body = f"""
<p class=crumb><a href="index.html">← all profiles</a> ·
<a href="prototype.html">glow prototype</a> · <a href="styles.html">style lab</a></p>
<h1>{html.escape(title)}</h1>
<p class=meta>{len(glows)} glows · <code>rules/{path.name}</code></p>
<section class=intro>{intro and render_block(["-- " + l for l in intro.splitlines()]) or ""}</section>
<h2>At a glance</h2>
<div class=tablewrap><table>
<thead><tr><th></th><th>glow</th><th>subject</th><th>when <small>readable</small></th>
<th>bind <small>sealed</small></th></tr></thead>
<tbody>{"".join(rows)}</tbody></table></div>
<h2>Every rung, with its reasoning</h2>
{"".join(cards)}
"""
    write(OUT / f"{path.stem}.html", shell(title, body, look))
    return {"stem": path.stem, "title": title, "count": len(glows), "subjects": subjects}


def spec_of(text: str) -> str:
    m = re.search(r"^spec\s+(\S+)", text, re.M)
    return m.group(1) if m else ""


# -------------------------------------------------------------------------- chrome

def shell(title: str, body: str, look: dict) -> str:
    return f"""<!doctype html>
<html lang=en><head><meta charset=utf-8>
<meta name=viewport content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Smart Glo</title>
<link rel=stylesheet href="style.css">
</head><body>
<main>{body}</main>
<script>window.LOOK = {json.dumps(look)};</script>
<script src="glow.js"></script>
</body></html>"""


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)


# -------------------------------------------------------------------------- assets

# Ids the media endpoint cannot resolve, and what to ask for instead. ⚠ Each entry is a
# claim that the art is THE SAME PICTURE, not merely a related one — the whole reason a
# missing icon draws a blank tile is that a plausible-but-wrong icon is worse than none.
#
#   432472 Sacred Weapon   — 404s by id and carries SpellIconFileDataID = 0, but the icon
#                            slug the armament actually uses does resolve.
#   1241413 Hammer of Wrath — the Sentinel OVERRIDE. Protection knows the ability by no id
#                            of its own; 24275 is the same spell on the Retribution side and
#                            the client draws one picture for both.
#
# Still unresolved, and left as a blank tile on purpose: 434506 / 433891 Infernal Bolt. Both
# ids 404 at the media endpoint and no icon slug for it has been found; guessing one returns
# HTTP 403, which is indistinguishable from a slug that exists but is unreadable.
ICON_FALLBACK = {
    432472: "inv_ability_lightsmithpaladin_sacredweapon",
    1241413: "24275",
}


def fetch_icons(spell_ids):
    want = sorted(set(spell_ids))
    missing = [str(ICON_FALLBACK.get(i, i)) for i in want
               if not (OUT / icon_name(i)).exists()]
    if missing:
        subprocess.run([sys.executable, "-m", "wowkb.uiart", "icon", *missing],
                       cwd=REPO / "tools", check=False,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # `wowkb.uiart` names files by icon SLUG; the site wants them by spell id, because a
    # page is written before anyone knows which slug an id resolves to.
    slugs = {}
    # One request token can serve SEVERAL subjects — 24275 is both Retribution's own Hammer
    # of Wrath and the art Protection's override borrows — so this is a token → ids fan-out
    # rather than a map. A plain dict silently dropped the self-mapping.
    asked = {}
    for i in want:
        asked.setdefault(str(ICON_FALLBACK.get(i, i)), []).append(i)
    out = subprocess.run([sys.executable, "-m", "wowkb.uiart", "icon", "--size", "56",
                          *asked.keys()], cwd=REPO / "tools",
                         capture_output=True, text=True)
    for line in out.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 3 and parts[0] in asked:
            for i in asked[parts[0]]:
                slugs[i] = REPO / parts[2]
    # ⚠ Some ids have no icon ANYWHERE we can reach: 432472 Sacred Weapon 404s at
    # `/data/wow/media/spell/` and carries `SpellIconFileDataID = 0` in SpellMisc. Borrowing a
    # sibling's art was rejected — the Holy Armaments node resolves to the BULWARK icon, so a
    # Sacred Weapon rung would show the other armament's picture and look correct doing it.
    # A blank tile that says nothing is better than a tile that says the wrong thing.
    missing_art = []
    for spell_id in want:
        src = slugs.get(spell_id)
        dst = OUT / icon_name(spell_id)
        dst.parent.mkdir(parents=True, exist_ok=True)
        if src and src.exists():
            shutil.copyfile(src, dst)
        else:
            missing_art.append(spell_id)
            if not dst.exists():
                Image.new("RGBA", (56, 56), (58, 54, 68, 255)).save(dst)
    if missing_art:
        print("no icon art for: " + ", ".join(map(str, missing_art))
              + "  (placeholder tile drawn)")


# How far the rim grows, in texels of the 64px master. The stroke itself measures 6 texels
# across (scanline through the centre), so 2 either side is a third of the stroke — a rim
# that reads at icon size without swallowing the colour it is meant to separate.
RIM_TEXELS = 2


def export_mark():
    """The mark the site draws is the addon's own shipping file, converted, not redrawn —
    plus the derived masks the style candidates need.

    ⚠ Every derivation here is a MASK — alpha only, at full opacity — because the page tints
    and fades it in CSS. `hex-fill` is the one that also ships, and the shipped `.tga` bakes
    `Look.PLATE_ALPHA` into its alpha (see `tool/gen_media.py` for why it has to). Converting
    that file instead of re-deriving it would apply the translucency twice and draw the lab's
    plate at 0.30 where the client draws 0.55 — so the plate mask is derived from `hex-white`
    here and its alpha comes from the style's own fill.

    ⚠ `hex-rim` and the motion masks are PROTOTYPE art and live here rather than in
    `tool/gen_media.py`, which owns what the addon ships. Promoting a style means moving the
    routine there and emitting a `.tga`, which is the trip the plate has made.

    * `hex-fill` — the outline flood-filled. A scrim plate the shape of the mark, rather
      than a rounded rectangle behind it.
    * `hex-rim`  — the outline dilated. Drawn black underneath the tinted stroke it makes a
      border; in the client this is a second Texture, not a new file. (Baking the rim into
      the master would also survive `SetVertexColor`, since black times any tint is black —
      but it fixes the rim width to the art, which is the thing to be able to tune.)
    """
    master = Image.open(ADDON / "Media" / "hex-white.tga").convert("RGBA")
    master.save(OUT / "hex-white.png")
    alpha = master.split()[3]
    # Flood the interior from the centre, then union with the original to keep the stroke.
    # ⚠ `thresh` is not optional. The stroke's INNER edge is anti-aliased, so an exact-match
    # fill halts on the first partially-opaque pixel and leaves a ring of soft alpha
    # unfilled — a visible seam between plate and stroke. 200 lets the fill cross that edge
    # while still stopping inside the stroke proper.
    inside = alpha.copy()
    ImageDraw.floodfill(inside, (inside.width // 2, inside.height // 2), 255, thresh=200)
    write_mask(ImageChops.lighter(inside, alpha), OUT / "hex-fill.png")

    # MaxFilter of width 2n+1 grows an opaque region by n in every direction.
    write_mask(alpha.filter(ImageFilter.MaxFilter(2 * RIM_TEXELS + 1)), OUT / "hex-rim.png")

    # ⚠ THE MOTION MASKS, and the reason they exist. A regular hexagon ring is uniform all
    # the way round and has six-fold rotational symmetry, so rotating it produces an image
    # nearly identical to the one before — and blur destroys the fine detail that was the
    # only thing distinguishing them. That is why the shipping spin vanishes in the
    # periphery. Every mask below breaks that symmetry ON PURPOSE, so that rotation becomes
    # a change in WHERE the light is rather than a change in nothing.
    write_mask(comet(alpha), OUT / "hex-comet.png")
    write_mask(arc(alpha, 150), OUT / "hex-arc.png")
    write_mask(triangle(master.size[0], stroke_width(alpha)), OUT / "tri-white.png")
    write_mask(triangle_fill(master.size[0]), OUT / "tri-fill.png")
    write_mask(dot(master.size[0]), OUT / "dot-white.png")


def stroke_width(alpha: Image.Image) -> int:
    """The master's stroke, measured rather than assumed — a scanline through the centre
    crosses it twice, so the first run of opaque pixels is the width. Derived art matches
    whatever the master happens to be, and follows it if the master is ever regenerated."""
    mid = alpha.size[1] // 2
    run = 0
    for x in range(alpha.size[0]):
        if alpha.getpixel((x, mid)) > 128:
            run += 1
        elif run:
            return run
    return 6


def _angle(size: int, x: int, y: int) -> float:
    """Position around the ring, 0..1, measured from the +x axis."""
    c = (size - 1) / 2
    return (math.atan2(y - c, x - c) / (2 * math.pi)) % 1.0


def comet(alpha: Image.Image) -> Image.Image:
    """The ring with a bright head fading to nothing around its circumference.

    Spun, this is a luminance PEAK travelling around the icon — a low-spatial-frequency
    moving blob, which is the thing peripheral vision is actually good at. The exponent
    shortens the head and lengthens the tail; a linear ramp reads as a lopsided ring rather
    than as something moving."""
    out = Image.new("L", alpha.size, 0)
    src, dst = alpha.load(), out.load()
    for y in range(alpha.size[1]):
        for x in range(alpha.size[0]):
            v = src[x, y]
            if v:
                dst[x, y] = int(v * max(0.0, 1.0 - _angle(alpha.size[0], x, y)) ** 1.6)
    return out


def arc(alpha: Image.Image, degrees: float) -> Image.Image:
    """A sector of the ring. Two of these counter-rotating cross twice a turn, and a
    crossing is a real luminance event at a fixed point on the icon."""
    span = degrees / 360.0
    out = Image.new("L", alpha.size, 0)
    src, dst = alpha.load(), out.load()
    for y in range(alpha.size[1]):
        for x in range(alpha.size[0]):
            if src[x, y] and _angle(alpha.size[0], x, y) <= span:
                dst[x, y] = src[x, y]
    return out


def triangle(size: int, stroke: int) -> Image.Image:
    """Three-fold symmetry instead of six, so a turn of the same angle changes the picture
    twice as much. The cheapest possible fix, and the one that keeps the current design."""
    out = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(out)
    c, r = (size - 1) / 2, size / 2 - stroke / 2 - 1
    pts = [(c + r * math.cos(math.radians(a)), c + r * math.sin(math.radians(a)))
           for a in (-90, 30, 150)]
    draw.polygon(pts, outline=255, width=stroke)
    return out


def triangle_fill(size: int) -> Image.Image:
    """The plate under a triangle mark. ⚠ A triangle inscribed in the same circle has HALF
    the area of a hexagon, so this plate carries half the low-frequency luminance mass of the
    hexagonal one — which is most of what a scrim is for. It is drawn to the full radius
    rather than inset to recover some of that."""
    out = Image.new("L", (size, size), 0)
    c, r = (size - 1) / 2, size / 2 - 1
    ImageDraw.Draw(out).polygon(
        [(c + r * math.cos(math.radians(a)), c + r * math.sin(math.radians(a)))
         for a in (-90, 30, 150)], fill=255)
    return out


def dot(size: int) -> Image.Image:
    """A filled disc, for the orbit candidate. Small and solid: a compact blob is what a
    blur preserves best, where a thin ring is what it smears away."""
    out = Image.new("L", (size, size), 0)
    c, r = (size - 1) / 2, size * 0.16
    ImageDraw.Draw(out).ellipse([c - r, c - r, c + r, c + r], fill=255)
    return out


def write_mask(alpha: Image.Image, path: Path):
    """A CSS mask reads only the alpha channel, so the colour is irrelevant — white keeps
    the file legible if anyone opens it."""
    out = Image.new("RGBA", alpha.size, (255, 255, 255, 0))
    out.putalpha(alpha)
    out.save(path)


# ---------------------------------------------------------------------------- main

def main() -> int:
    look = LOOK
    names = display_names()
    OUT.mkdir(parents=True, exist_ok=True)

    profiles, subjects = [], [PROTOTYPE_SPELL]
    for path in sorted(RULES.glob("*.sg")):
        info = profile_page(path, look, names)
        profiles.append(info)
        subjects += info["subjects"]

    fetch_icons(subjects)
    export_mark()
    write(OUT / "style.css", STYLE)
    write(OUT / "glow.js", SCRIPT)
    write(OUT / "index.html", index_page(profiles, look))
    write(OUT / "prototype.html", prototype_page(look, names))
    write(OUT / "styles.html", styles_page(look, names))
    print(f"wrote {len(profiles)} profiles + prototype into {OUT}")
    return 0


def index_page(profiles, look) -> str:
    cards = "".join(
        f'<a class=pcard href="{p["stem"]}.html"><h3>{html.escape(p["title"])}</h3>'
        f'<p>{p["count"]} glows</p></a>' for p in profiles)
    body = f"""
<h1>Smart Glo profiles</h1>
<p class=meta>Generated from <code>projects/smart-glo/rules/*.sg</code> by
<code>tool/gen_site.py</code>. Edit the rule file, not this page.</p>
<div class=grid>{cards}</div>
<h2>The mark itself</h2>
<div class=grid><a class=pcard href="prototype.html"><h3>Glow prototype</h3>
<p>What plain and <em>urgent</em> draw on a Cooldown Manager icon</p></a>
<a class=pcard href="styles.html"><h3>Style lab</h3>
<p>Candidate marks, judged against icons chosen to fight them</p></a></div>
"""
    return shell("Smart Glo profiles", body, look)


def tile(style, spell_id: int, urgent: bool) -> str:
    """One Cooldown Manager icon with a candidate drawn on it. Every layer carries its own
    mask, fill, scale and spin as data; `glow.js` reads them and owns no style knowledge."""
    def attrs(l):
        out = (f'data-mask="{l["mask"]}" data-fill="{html.escape(l["fill"])}" '
               f'data-scale="{l.get("scale", 1.0)}" data-spin="{l.get("spin", 1)}"')
        if "breathe" in l:
            out += f' data-breathe="{l["breathe"][0]},{l["breathe"][1]}"'
        if "orbit" in l:
            out += f' data-orbit="{l["orbit"]}"'
        if "fade" in l:
            out += f' data-fade="{l["fade"][0]},{l["fade"][1]}"'
        if l.get("still"):
            out += ' data-still="1"'
        if "cycle" in l:
            out += ' data-cycle="%s"' % ",".join(
                str(v) for rgb in l["cycle"] for v in rgb)
        return out

    layers = "".join(f'<i class=layer {attrs(l)}></i>' for l in style["layers"])
    mode = style.get("urgentMotion", "pulse")
    rate = style.get("urgentRate", 1.0)
    return (f'<div class=cdm data-urgent="{1 if urgent else 0}" data-umode="{mode}" '
            f'data-urate="{rate}">'
            f'<img class=art src="{icon_name(spell_id)}" alt="">{layers}</div>')


def styles_page(look, names) -> str:
    """One section per candidate. ⚠ Deliberately NOT a table: the descriptions are long and
    the tiles are small, and a table column sized for one starves the other — the first cut
    squeezed the prose to a word a line while the tiles floated in whitespace."""
    sections = []
    for style in STYLES:
        tiles = "".join(
            f'<figure><div class=pair>{tile(style, sid, False)}{tile(style, sid, True)}</div>'
            f'<figcaption><strong>{html.escape(name)}</strong><br>'
            f'<small>{html.escape(why)}</small></figcaption></figure>'
            for sid, name, why in BACKDROPS)
        sections.append(
            f'<section class=style><h3>{html.escape(style["name"])}'
            + (' <span class=shipping>shipping</span>' if style["key"] == "current" else "")
            + f'</h3><p>{inline(style["blurb"])}</p>'
            f'<p class=cost><span class=lbl>in the client</span> {inline(style["cost"])}</p>'
            + (f'<p class=cost><span class=lbl>plain vs urgent</span> '
               f'{inline(style["axes"])}</p>' if style.get("axes") else "")
            + f'<div class=strip>{tiles}</div></section>')

    body = f"""
<p class=crumb><a href="index.html">← all profiles</a> ·
<a href="prototype.html">the shipping look</a></p>
<h1>Style lab</h1>
<p class=meta>Candidate marks, none of them built. Each strip runs one style across icons
chosen to fight it; within a cell the left tile is plain and the right is
<strong>urgent</strong>.</p>

<div class=controls>
  <label>icon size <input id=size type=range min=28 max=120 value=64>
    <output id=sizeout>64</output>px</label>
  <label>eccentricity
    <input id=blur type=range min=0 max=35 step=1 value=12>
    <output id=blurout>12</output>&deg; off-axis</label>
  <label><input id=freeze type=checkbox> freeze animation</label>
</div>

{"".join(sections)}

<h2>What the eccentricity slider is, and where to set it</h2>
<p>It was a raw pixel count, which could not be answered — a 5px blur means one thing on a
28px icon and another on a 120px one, and neither corresponds to anything. It now takes an
<strong>angle off the point you are looking at</strong> and derives the blur, so moving the
icon-size slider no longer silently changes the severity of the test.</p>
<p>The model is the standard linear falloff of acuity with eccentricity,
<code>MAR(E) = MAR&#8320;(1 + E/E&#8322;)</code> with <code>MAR&#8320;</code> one arcminute
(20/20) and <code>E&#8322;</code> 2.3&deg;, taking the Gaussian sigma as half the minimum
resolvable angle. Converting that to page pixels needs one assumption, stated here so you can
disagree with it: <strong>a Cooldown Manager icon subtends about 0.9&deg;</strong> — a 40px
icon on a 27" 1440p panel at 60cm, which is roughly 45 pixels per degree.</p>
<p><strong>Set it to 10–15&deg;.</strong> That is where the Essential viewer actually sits
when you are watching your character: the bar is a little above the action bars, and the
centre of a 27" screen at 60cm is about 15&deg; from its bottom edge. 20–25&deg; is a
side-mounted or second-monitor bar. Past 30&deg; you are asking a question about the far
periphery that no icon-sized mark passes, and the slider goes there mainly to show you
that.</p>
<p class=warn>⚠ A blur models low acuity and <em>nothing else</em>. It does not model the
periphery's much better <em>motion</em> sensitivity, nor its near-intact contrast sensitivity
at low spatial frequencies — so it is systematically unfair to anything moving and fair to
anything large. That bias is exactly why the spin measured worse here than it may fly, and
why <code>urgent</code> already reads better than plain. Treat it as a filter that rules
candidates OUT, not one that picks the winner.</p>

<h2>What the purple↔yellow cycle got wrong, and what replaced it</h2>
<p>It solved wash-out in <strong>time</strong>: it crossed to the opposite side of the wheel so
the mark was never the icon's hue for long, and <code>Look.CYCLE_CROSS</code> held each end
because the midpoint of purple and yellow is a pale tan less visible than either. But holding
an end means that for the length of a hold the mark <em>is</em> one specific hue — and on the
icon that shares it, that hold is the mark disappearing. Worse, the two hues differed in
relative luminance by only about 15%, so the whole modulation was landing on
<strong>chroma</strong>, which is most of what peripheral vision discards.</p>
<p>The cycle shipping now swings the same hue from near-black to <code>yellow</code>, which
puts the whole modulation on <strong>luminance</strong> — the channel the periphery keeps —
and takes Michelson contrast from about 0.15 to about 0.9 for the same one
<code>SetVertexColor</code> per tick. No spell art is both very dark and very bright in one
place, so one end of the swing always stands off the icon.</p>

<h2>What was built, flown, and what came back</h2>
<p>The dark↔bright swing arrived as part of a larger look: the mark shrunk over a
<strong>translucent black plate</strong>, and <code>urgent</code> moved off the size channel
onto a <strong>bounce</strong> run 18% faster than a plain glow. The last four candidates above
are its steps. It topped every column of <code>tool/measure_motion.py</code> and survived
backdrops the plain hexagon disappears against.</p>
<p>It was reverted after four releases, and then taken apart. What is shipping now is three of
its four ideas: the <strong>smaller mark</strong>, the <strong>dark end of the swing</strong>,
and the <strong>plate</strong> — in purple rather than black, and <em>turning with the mark</em>
rather than sitting still under it, which is what stops it reading as a hole punched in the row.
What did not come back is the bounce: beside icons that were not moving it read as fidgeting,
and <code>urgent</code> is a pop again.</p>
<p class=warn>⚠ Every offline axis on this page — blur, rate, swing — agreed on the version that
lost, and agreed for the right reasons about the parts that were kept. They rule a candidate
out; they do not pick the winner. A row at the top of the measurement is a reason to go and
look, never a reason to ship.</p>
"""
    return shell("Style lab", body, look)


def prototype_page(look, names) -> str:
    """The SHIPPING look, and every number under it read out of `Look.lua`.

    The tiles are drawn by `tile()` from `STYLES[0]` rather than hand-written here, so this
    page cannot drift from the candidate the style lab marks `shipping`."""
    cyc = look["cycles"].get(look["default"], [])
    pair = " \u2194 ".join(c for c in cyc) or look["default"]
    current = STYLES[0]
    plate_swatch = (f'<span class=swatch style="background:{SHIP_PLATE}"></span> '
                    + ", ".join(f"{v:g}" for v in look["plateRgb"]))
    body = f"""
<p class=crumb><a href="index.html">← all profiles</a> ·
<a href="styles.html">style lab</a></p>
<h1>Glow prototype</h1>
<p class=meta>Every number below is read out of <code>addon/SmartGlo/Look.lua</code> at
build time, and the art is the addon's own <code>Media/hex-white.tga</code> and
<code>Media/hex-fill.tga</code>. This is a simulation of the drawing, not of the client — the
icon behind it is a still.</p>

<div class=stage>
  <figure>{tile(current, PROTOTYPE_SPELL, False)}
    <figcaption><strong>plain</strong><br><small>lit, spinning on its plate,
    cycling</small></figcaption></figure>
  <figure>{tile(current, PROTOTYPE_SPELL, True)}
    <figcaption><strong>urgent</strong><br><small>the same mark, popping</small></figcaption></figure>
  <figure><div class=cdm data-off=1>
      <img class=art src="{icon_name(PROTOTYPE_SPELL)}" alt=""></div>
    <figcaption><strong>dark</strong><br><small>an untouched CDM icon</small></figcaption></figure>
</div>

<div class=controls>
  <label>icon size <input id=size type=range min=28 max=120 value=56>
    <output id=sizeout>56</output>px</label>
  <label><input id=freeze type=checkbox> freeze animation</label>
</div>

<h2>The numbers, and where each comes from</h2>
<div class=tablewrap><table>
<tbody>
<tr><td><code>Look.FRACTION</code></td><td>{look["fraction"]:g}</td>
    <td>the mark's side, as a fraction of the icon. It was 0.72: a hexagon that nearly fills
    the icon competes with the art it is marking, where one with air around it is a mark
    <em>on</em> the icon</td></tr>
<tr><td><code>Look.PLATE_SCALE</code></td><td>×{look["plateScale"]:g}</td>
    <td>the plate's side, as a multiple of the MARK's — so the pair keeps its proportion at
    every icon size. {look["fraction"] * look["plateScale"]:.3g} of the icon, which has to stay
    inside <code>OCCLUDE</code> {look["occlude"]:g}: the plate is the widest thing an element
    draws, and a count's occluder has to cover it</td></tr>
<tr><td><code>Look.PLATE_RGB</code></td><td>{plate_swatch}</td>
    <td><code>purple</code> at 35% of its value. Full <code>purple</code> is a light lavender
    at relative luminance 0.608 against <code>yellow</code>'s 0.817 — a 15% swing, which is the
    mistake the black↔yellow cycle exists to undo, handed back as a background</td></tr>
<tr><td><code>Look.PLATE_ALPHA</code></td><td>{look["plateAlpha"]:g}</td>
    <td>⚠ <strong>baked into <code>Media/hex-fill.tga</code></strong> by
    <code>tool/gen_media.py</code>, which reads it from this line. It cannot be written at
    runtime: <code>SetVertexColor</code>'s fourth argument and <code>SetAlpha</code> are one
    channel, so the write that says whether the plate is drawn would clobber it</td></tr>
<tr><td><code>Look.SPIN_SECONDS</code></td><td>{look["spinSeconds"]:g}s</td>
    <td>one full turn of {look["spinDegrees"]:g}°, armed at build and never started on a
    crossing — mark and plate simply always turn, in step</td></tr>
<tr><td><code>Look.CYCLE_SECONDS</code></td><td>{look["cycleSeconds"]:g}s</td>
    <td>the hue cycle, {html.escape(pair)}. 1.67&nbsp;Hz, under the 3&nbsp;Hz where flashing
    becomes a problem, and fast enough that a GCD-long glance cannot land entirely in one
    phase</td></tr>
<tr><td><code>Look.CYCLE_CROSS</code></td><td>{look["cycleCross"]:g}</td>
    <td>the fraction of the cycle spent crossing rather than holding — the mark is a
    saturated hue ~70% of the time instead of sitting in the pale midpoint</td></tr>
<tr><td><code>Look.PULSE_SECONDS</code></td><td>{look["pulseSeconds"]:g}s</td>
    <td><strong>urgent only.</strong> Out and back, <code>IN_OUT</code> smoothing, looping</td></tr>
<tr><td><code>Look.PULSE_SCALE</code></td><td>×{look["pulseScale"]:g}</td>
    <td>a SCALE rather than a translation, so it is immune to an icon-size change</td></tr>
</tbody></table></div>

<h2>What <code>urgent</code> means</h2>
<p>One level above plain, and it is about the rule rather than the art: <em>this rung
outranks the ordinary reading</em> — a resource actively being wasted, not merely a button
that happens to be available. The keyword names the meaning so the drawing can be retuned
without touching a rule.</p>
<p>The <a href="styles.html">style lab</a> carries the alternatives, including one that was
built and flown: <strong>urgent</strong> as a drop rather than a pop. It measured better on
every offline axis and did not survive being looked at.</p>
"""
    return shell("Glow prototype", body, look)


STYLE = """
:root{
  --bg:#faf9f7; --panel:#fff; --ink:#1b1a19; --dim:#6b6763; --line:#e2ddd6;
  --accent:#8a5cf0; --urg:#c2410c; --seal:#0e7490; --code:#f3f0ec;
}
:root:not([data-theme=light]){ }
@media (prefers-color-scheme:dark){ :root:not([data-theme=light]){
  --bg:#16151a; --panel:#1e1d24; --ink:#eceaf0; --dim:#9c96a6; --line:#332f3c;
  --accent:#b794ff; --urg:#ff9d5c; --seal:#5ed4e0; --code:#26242e;
}}
:root[data-theme=dark]{
  --bg:#16151a; --panel:#1e1d24; --ink:#eceaf0; --dim:#9c96a6; --line:#332f3c;
  --accent:#b794ff; --urg:#ff9d5c; --seal:#5ed4e0; --code:#26242e;
}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--ink);margin:0;
  font:15px/1.6 ui-sans-serif,system-ui,-apple-system,"Segoe UI",sans-serif;}
main{max-width:980px;margin:0 auto;padding-block:32px 80px;padding-left:20px;padding-right:20px}
h1{font-size:1.9rem;letter-spacing:-.02em;margin:.2em 0 .1em}
h2{font-size:1.15rem;letter-spacing:-.01em;margin:2.4em 0 .8em;
  padding-bottom:.4em;border-bottom:1px solid var(--line)}
h2.sect{margin-top:3em;color:var(--accent);border-bottom-style:dashed}
h3{font-size:1rem;margin:0}
a{color:var(--accent)}
code{background:var(--code);border-radius:4px;padding:.1em .35em;
  font:12.5px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace}
.crumb{font-size:.85rem;color:var(--dim);margin:0 0 1.2em}
.meta{color:var(--dim);font-size:.88rem;margin:.2em 0 1.6em}
.intro p,.aside p{color:var(--dim);font-size:.92rem}
.aside{border-left:2px solid var(--line);padding-left:14px;margin:1.6em 0}
p.warn{border-left:2px solid var(--urg);padding-left:12px}

.tablewrap{overflow-x:auto;border:1px solid var(--line);border-radius:10px;background:var(--panel)}
table{border-collapse:collapse;width:100%;font-size:.86rem;min-width:640px}
.swatch{display:inline-block;width:.85em;height:.85em;border-radius:3px;vertical-align:-1px;border:1px solid var(--line)}
th{text-align:left;font-weight:600;color:var(--dim);font-size:.72rem;
  text-transform:uppercase;letter-spacing:.06em;padding:10px 12px;border-bottom:1px solid var(--line)}
th small{text-transform:none;letter-spacing:0;font-weight:400;opacity:.7}
td{padding:9px 12px;border-bottom:1px solid var(--line);vertical-align:top}
tr:last-child td{border-bottom:0}
td.icd{width:34px;padding-right:0}
td.nm{font-weight:600;min-width:190px}
td.sj{color:var(--dim);white-space:nowrap}
td.cond{font:12.5px/1.5 ui-monospace,SFMono-Regular,Menlo,monospace}
td.cond:last-child{min-width:150px}
tr.sectrow td{background:var(--code);color:var(--accent);font-weight:600;
  font-size:.74rem;text-transform:uppercase;letter-spacing:.06em}
img.ic{width:26px;height:26px;border-radius:5px;display:block;
  box-shadow:0 0 0 1px rgba(0,0,0,.25)}

.op{color:var(--dim)} .fn{color:var(--accent)} .sp{color:var(--ink);font-weight:600}
.res{color:var(--seal)} .none{color:var(--dim)}
.sealed{color:var(--seal);border-bottom:1px dotted currentColor}
.urg{display:inline-block;vertical-align:1px;background:var(--urg);color:#fff;
  font:600 9.5px/1 ui-sans-serif,system-ui;letter-spacing:.08em;text-transform:uppercase;
  padding:3px 5px;border-radius:3px}
.id{color:var(--dim);font:11px ui-monospace,monospace}

.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;
  padding:16px 18px;margin:14px 0}
.card.u{border-left:3px solid var(--urg)}
.card header{display:flex;gap:12px;align-items:center;margin-bottom:10px}
.card header img.ic{width:36px;height:36px;border-radius:7px}
.card .subj{color:var(--dim);font-size:.8rem}
.card .terms{background:var(--code);border-radius:8px;padding:10px 12px;margin:10px 0 12px;
  font:12.5px/1.7 ui-monospace,SFMono-Regular,Menlo,monospace}
.card .terms .lbl{display:inline-block;width:40px;color:var(--dim);font-weight:600}
.card p{font-size:.9rem;color:var(--dim)}
.card p:last-child{margin-bottom:0}

.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:12px}
.pcard{display:block;background:var(--panel);border:1px solid var(--line);border-radius:12px;
  padding:16px;text-decoration:none;color:inherit}
.pcard:hover{border-color:var(--accent)}
.pcard p{color:var(--dim);font-size:.85rem;margin:.3em 0 0}

.stage{display:flex;gap:32px;flex-wrap:wrap;margin:24px 0}
.stage figure{margin:0;text-align:center}
.stage figcaption{margin-top:12px;font-size:.85rem;color:var(--dim)}
.cdm{position:relative;width:56px;height:56px;margin:0 auto}
.cdm .art{width:100%;height:100%;border-radius:6px;display:block;
  box-shadow:0 0 0 1px rgba(0,0,0,.4)}
/* `SetVertexColor` multiplies a white master by a tint. A mask over a solid fill is the
   same operation: the file contributes only its alpha, the colour comes from elsewhere.
   A CSS `filter` is NOT the same and was tried first — it renders the mark black.
   Size, mask file and fill all come from glow.js, so a style is data and not a rule here. */
.cdm .layer{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  pointer-events:none;-webkit-mask-size:contain;mask-size:contain;
  -webkit-mask-position:center;mask-position:center;
  -webkit-mask-repeat:no-repeat;mask-repeat:no-repeat}

/* the style lab */
.style{background:var(--panel);border:1px solid var(--line);border-radius:12px;
  padding:18px 20px;margin:16px 0}
.style h3{font-size:1.05rem;margin:0 0 .5em}
.style .shipping{background:var(--code);color:var(--dim);font:600 9.5px/1 ui-sans-serif,
  system-ui;letter-spacing:.08em;text-transform:uppercase;padding:4px 6px;border-radius:3px;
  vertical-align:2px}
.style p{font-size:.88rem;color:var(--dim);margin:0 0 .6em;max-width:66ch}
.style p.cost{border-top:1px solid var(--line);padding-top:.7em;margin-top:.9em}
.style .lbl{color:var(--accent);font-weight:600}
.strip{display:flex;gap:22px;flex-wrap:wrap;margin-top:18px}
.strip figure{margin:0;text-align:center}
.strip figcaption{margin-top:10px;font-size:.78rem;color:var(--dim);max-width:150px}
.strip figcaption small{opacity:.8}
.pair{display:flex;gap:10px;justify-content:center;align-items:center}
.controls{display:flex;gap:24px;flex-wrap:wrap;align-items:center;
  background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:12px 16px}
.controls label{font-size:.85rem;color:var(--dim);display:flex;gap:8px;align-items:center}
@media (max-width:560px){ .stage{gap:20px;justify-content:center} }
"""

SCRIPT = r"""
// The mark's motion, driven from LOOK — which gen_site.py read out of Look.lua. Nothing
// here picks a number, and nothing here knows a style: every layer carries its own mask,
// fill, scale and spin as data attributes, so adding a candidate is a Python-side change.
(function () {
  var L = window.LOOK; if (!L) return;
  var tiles = Array.prototype.slice.call(document.querySelectorAll('.cdm'));
  if (!tiles.length) return;

  var pair = (L.cycles[L.default] || []).map(function (n) { return L.palette[n]; });
  var solo = L.palette[L.default] || [1, 1, 1];
  if (pair.length < 2) pair = [solo, solo];

  function css(rgb) {
    return 'rgb(' + rgb.map(function (v) { return Math.round(v * 255); }).join(',') + ')';
  }
  // Look.lua's `Wave`: hold each end, cross quickly, so the mark is a saturated hue most of
  // the time rather than sitting in the pale midpoint of the two.
  function wave(phase) {
    var cross = L.cycleCross, hold = (1 - 2 * cross) / 2;
    if (phase < hold) return 0;
    if (phase < hold + cross) return (phase - hold) / cross;
    if (phase < 2 * hold + cross) return 1;
    return 1 - (phase - 2 * hold - cross) / cross;
  }
  function lerp(a, b, t) { return a + (b - a) * t; }
  // `IN_OUT` smoothing is a sine ease in the client; the same curve here.
  function easeInOut(t) { return 0.5 - 0.5 * Math.cos(Math.PI * t); }

  // A ball DROPPED and left to settle, not a sine and not a single arc. It begins AT its apex,
  // so an urgent glow differs from a plain one on the first frame rather than after a climb.
  // Two facts do the rest. Under constant gravity a hop's height is a PARABOLA — it leaves
  // fast, hangs near the apex and returns fast, where a sine spends its time evenly and reads
  // as a hover. And a bounce loses energy by a fixed RESTITUTION each time, so each hop is
  // BOB_E of the previous height and, because arc time goes as the square root of height,
  // sqrt(BOB_E) of its duration. The settle therefore accelerates on its own — that quickening
  // is what says "a thing was dropped" rather than "a thing is blinking on a timer".
  //
  // The rest at the end is not padding. An unbroken oscillation in the periphery adapts away
  // (Troxler fading is specifically a peripheral effect); a discrete event that stops and
  // restarts never does. It is also what the macOS Dock's attention bounce actually is.
  // ⚠ Out of LOOK.lab, not Look.lua — the addon does not bounce, so these are the lab's own
  // and gen_site.py says so where they are defined. BOUNCE_HEIGHT 0.26 is not a taste number
  // even here: it is what the count occluder's footprint leaves once the mark is inside it.
  var BOB_SECONDS = L.lab.bounceSeconds,
      BOB_HEIGHT = L.lab.bounceHeight,
      BOB_E = L.lab.bounceE,
      BOB_HOPS = L.lab.bounceHops,
      BOB_REST = L.lab.bounceRest;

  // The chain of HALF-arcs, precomputed once: the drop is one fall, and every bounce after it
  // is a rise and a fall. A half-arc of height h takes sqrt(h)/2, and mirrors Look.lua's
  // ordered Translations exactly — `fall` there is smoothing IN, `rise` is OUT.
  //   fall, local t: h(1 - t²)      rise, local t: h(2t - t²)
  // which are just the second and first halves of the parabola h·4u(1-u), reparametrised.
  var bobSeg = [], bobTotal = 0;
  for (var i = 0; i < BOB_HOPS; i++) {
    var h = Math.pow(BOB_E, i), d = Math.sqrt(h) / 2;
    if (i > 0) { bobSeg.push({ h: h, d: d, up: true }); bobTotal += d; }
    bobSeg.push({ h: h, d: d, up: false }); bobTotal += d;
  }
  function bounce(phase) {
    var span = 1 - BOB_REST;
    if (phase >= span) return 0;                 // sitting on the plate, waiting
    var x = phase / span * bobTotal;             // position along the chain of half-arcs
    for (var i = 0; i < bobSeg.length; i++) {
      var s = bobSeg[i];
      if (x < s.d) {
        var t = x / s.d;
        return s.up ? s.h * (2 * t - t * t) : s.h * (1 - t * t);
      }
      x -= s.d;
    }
    return 0;
  }

  // A layer is a MASK over a solid fill, which is exactly what SetVertexColor does to a
  // white master: the file contributes only its alpha. A CSS `filter` is NOT the same and
  // was tried first — it renders the mark black.
  var layers = [];
  tiles.forEach(function (tile) {
    Array.prototype.forEach.call(tile.querySelectorAll('.layer'), function (el) {
      var scale = parseFloat(el.dataset.scale || '1');
      var side = (L.fraction * scale * 100) + '%';
      el.style.width = el.style.height = side;
      el.style.webkitMaskImage = el.style.maskImage = 'url(' + el.dataset.mask + '.png)';
      function nums(v) { return v ? v.split(',').map(parseFloat) : null; }
      layers.push({
        el: el, scale: scale, spin: parseFloat(el.dataset.spin || '1'),
        fill: el.dataset.fill, urgent: tile.dataset.urgent === '1',
        // A `still` layer sits out the urgent motion — the plate is scenery, not actor.
        umode: el.dataset.still ? 'none' : (tile.dataset.umode || 'pulse'),
        // Urgent may run its own clock. A RATE, not an offset — an offset is a fixed head
        // start that never widens, where a rate keeps sliding, so the difference from a
        // neighbouring plain glow is always arriving rather than already arrived.
        urate: parseFloat(tile.dataset.urate || '1'),
        breathe: nums(el.dataset.breathe),   // [amplitude, seconds]
        fade: nums(el.dataset.fade),         // [minAlpha, seconds]; 0s = static
        // Six floats = two RGB triples this layer cycles between on the SHARED wave,
        // in place of the palette's. Same ticker, same period — different endpoints.
        cycle: nums(el.dataset.cycle),
        orbit: el.dataset.orbit ? parseFloat(el.dataset.orbit) : 0
      });
    });
  });

  var frozen = false, t0 = performance.now();
  function frame(now) {
    if (!frozen) {
      var t = (now - t0) / 1000;
      // Phase is per-layer now, because urgent may run a faster clock than plain.
      function phases(rate) {
        var u = t * rate;
        return { hue: wave((u % L.cycleSeconds) / L.cycleSeconds),
                 spin: (u % L.spinSeconds) / L.spinSeconds * L.spinDegrees };
      }
      var base = phases(1);
      // Out on order 1, back on order 2 — one loop is PULSE_SECONDS end to end.
      var p = (t % L.pulseSeconds) / L.pulseSeconds;
      var pulse = 1 + (L.pulseScale - 1) *
        (p < 0.5 ? easeInOut(p * 2) : easeInOut((1 - p) * 2));

      layers.forEach(function (l) {
        var ph = (l.urgent && l.urate !== 1) ? phases(l.urate) : base;
        var hue = ph.hue, spin = ph.spin;
        var tint = css([0, 1, 2].map(function (i) {
          return lerp(pair[0][i], pair[1][i], hue);
        }));
        var parts = ['translate(-50%,-50%)'];
        // ⚠ ORDER IS LOAD-BEARING. A transform list composes left-to-right as coordinate-
        // system operations, so anything after the rotate travels along the MARK'S axes, not
        // the screen's. A bounce must be screen-space vertical — put it before the spin, or
        // "up" rotates with the mark and the hop becomes a wobble. (The orbit below is the
        // opposite case: it is deliberately after the rotate, because sweeping a circle is
        // exactly "offset along an axis that turns".)
        if (l.urgent && l.umode === 'bob') {
          parts.push('translateY(' +
            (-BOB_HEIGHT * 100 * bounce((t % BOB_SECONDS) / BOB_SECONDS)) + '%)');
        }
        parts.push('rotate(' + (spin * l.spin) + 'deg)');
        // ⚠ An orbit is a TRANSLATION AFTER A ROTATION, expressed as a percentage of the
        // layer's own size — never an absolute offset. That is the whole point: in the
        // client this is an off-centre child of a rotating parent, so only a Rotation is
        // ever animated and an icon-size change cannot strand it (Look.lua PULSE_SECONDS).
        if (l.orbit) parts.push('translateX(' + (l.orbit * 100) + '%)');
        if (l.breathe) {
          parts.push('scale(' + (1 + l.breathe[0] *
            Math.sin(2 * Math.PI * t / l.breathe[1])) + ')');
        }
        // ⚠ A bob is a TRANSLATION, and a translation in percent of the LAYER'S OWN SIZE
        // — never an absolute offset, for the same reason the orbit is not one. |sin| is a
        // ballistic bounce: it touches down once per period rather than easing through the
        // bottom the way the scale pulse eases through its trough.
        if (l.urgent && l.umode === 'pulse') parts.push('scale(' + pulse + ')');
        l.el.style.transform = parts.join(' ');
        // A fade with a period of 0 is a fixed alpha — how a layer is dimmed rather than
        // animated. ⚠ In the client an ANIMATED alpha is contested: a sealed duration or
        // percent bind owns the widget's alpha. The route is nesting, measured 2026-09-08 —
        // a child renders at parent alpha x its own — so an alpha-animated mark has to be a
        // CHILD of the frame the bind drives, never the frame itself.
        if (l.fade) {
          l.el.style.opacity = l.fade[1] > 0
            ? (l.fade[0] + (1 - l.fade[0]) *
               (0.5 + 0.5 * Math.sin(2 * Math.PI * t / l.fade[1])))
            : l.fade[0];
        }
        // `a` and `b` hold the cycle's two hues STATIC; `tint` is the live cycle; anything
        // else is a literal colour the style asked for.
        var own = l.cycle && css([0, 1, 2].map(function (i) {
          return lerp(l.cycle[i], l.cycle[i + 3], hue);
        }));
        l.el.style.background = own ? own
                              : l.fill === 'tint' ? tint
                              : l.fill === 'a' ? css(pair[0])
                              : l.fill === 'b' ? css(pair[1])
                              : l.fill;
      });
    }
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);

  function slider(id, outId, apply) {
    var el = document.getElementById(id), out = document.getElementById(outId);
    if (!el) return;
    el.addEventListener('input', function () { out.textContent = el.value; apply(el.value); });
  }
  slider('size', 'sizeout', function (v) { iconPx = parseFloat(v); applyOptics(); });
  // Peripheral vision is low-acuity. Blurring the WHOLE tile — art and mark together — is
  // the point: a mark that survives only because it is sharp has not survived.
  //
  // The slider is an ANGLE, not a pixel count, because a pixel count is unanswerable: it
  // only means something against an icon size and a viewing distance. MAR(E) = MAR0(1+E/E2)
  // is the standard linear acuity falloff (MAR0 = 1 arcmin, E2 = 2.3 deg); sigma is taken as
  // half the minimum resolvable angle, and ICON_DEGREES converts to page pixels. Because it
  // scales with the icon-size slider, the two controls are finally independent.
  var ICON_DEGREES = 0.9;   // a 40px CDM icon at ~45 px/deg — see the prose on the page
  function blurPx(deg) {
    var mar = (1 + deg / 2.3) / 60;                       // degrees
    return (mar / 2) / ICON_DEGREES * iconPx;             // page pixels
  }
  // The prototype page has a size slider but no eccentricity one; with no blur control on
  // the page there is no blur, or that page would silently inherit this one's 12 degrees.
  var sizeEl = document.getElementById('size'), eccEl = document.getElementById('blur');
  var iconPx = sizeEl ? parseFloat(sizeEl.value) : 64;
  var ecc = eccEl ? parseFloat(eccEl.value) : 0;
  function applyOptics() {
    tiles.forEach(function (c) {
      c.style.width = c.style.height = iconPx + 'px';
      var px = blurPx(ecc);
      c.style.filter = px > 0.15 ? 'blur(' + px.toFixed(2) + 'px)' : '';
    });
  }
  slider('blur', 'blurout', function (v) { ecc = parseFloat(v); applyOptics(); });
  applyOptics();
  var f = document.getElementById('freeze');
  if (f) f.addEventListener('change', function () { frozen = f.checked; });
})();
"""


if __name__ == "__main__":
    raise SystemExit(main())
