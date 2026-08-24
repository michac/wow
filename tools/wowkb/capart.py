"""Generate the Combat Assist Plus design previews from the docs that own them.

This tool assembles; it never decides. **It holds no color, no rate and no size.** Every
number it draws with is lifted out of `projects/combat-assist/specs/render-shelf.md`
Part 6 — the `render-tokens` JSON block — and every ability, lane and verdict comes from
the spec's own `catalog.md` (and, for Havoc, the `scenarios.md` beside it — Retribution keeps
its walk in the one file). Change the look by editing the shelf and rebuilding; change the walk
by editing the scenario doc and re-importing. If a number appears in this file, that is a bug.

Why it exists. The old Havoc stepper was a stylized diagram: two-letter abbreviations on
CSS gradients, and cue treatments invented on the spot with no relationship to anything
the client can draw. It validated the *logic* of the elimination walk and nothing about
the *look*, which left the eventual `Catalogs/Havoc.lua` a fresh design exercise rather
than a transcription. The preview this builds is a **reproduction**: real Blizzard icon
art at the client's own icon size, real extracted flipbook sheets at their real frame
counts and durations, and cap's treatments composited the way the client composites
them.

The fidelity guard is the point, not a nicety:

* `SetVertexColor` **multiplies**, so a tint is `background-color` +
  `background-blend-mode: multiply`, never `filter: hue-rotate`. A hue rotation looks
  great and can recolor art the client **cannot** recolor — which is exactly the lie that
  makes a preview worthless.
* A primitive asking for `tint: "shelf"` on art whose measured saturation says it carries a
  baked hue is a **hard error**, naming the measurement. The guard is art-agnostic: it began
  on the flipbook emphasis rings and now covers the badge sprites and V11's stripe sheet.
* `tint: "desaturate+shelf"` builds but is stamped ⚠ *open*, because desaturate-then-tint
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
is `spec.md` §3.2's defect), positive cues rank above negative ones so a promotion packs onto the
corner (`render-shelf.md` Part 1), and no row is denser than Part 0.5's hold budget.

Usage:
    uv run python -m wowkb.capart tokens                # resolved tokens + the CSS block
    uv run python -m wowkb.capart assets                # per-asset byte table vs the budget
    uv run python -m wowkb.capart import scenarios <spec>   # seed the sidecar from the doc
    uv run python -m wowkb.capart build havoc           # write one spec's preview
    uv run python -m wowkb.capart build --all           # ...or every registered spec
    uv run python -m wowkb.capart export lua            # the same tokens as CombatAssistPlus/Style.lua
    uv run python -m wowkb.capart export ring           # Part 7's ring flipbook sheet
    uv run python -m wowkb.capart export lab            # Part 7 as Lab.lua + Media/lab/ (gallery only)
    uv run python -m wowkb.capart check havoc [--all]   # doc↔sidecar, staleness, strict CSS

    uv run python -m wowkb.serve projects/combat-assist/previews \\
        --watch projects/combat-assist/specs \\
        --on-change "python -m wowkb.capart build --all"   # edit → rebuild → reload
"""

import argparse
import base64
import contextlib
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
PREVIEWS = PROJECT / "previews"
TEMPLATE = PREVIEWS / "template"
SIDECARS = PREVIEWS / "data"
CACHE = uiart.OUT / "capart-cache"

# Part 7's lab cells are authored once, against this spec's catalog, and drawn on every page.
SHELF_ROSTER_SPEC = "havoc"

BUILT_MARK = "<!-- capart built: {date} -->"
BUILT_RE = re.compile(r"<!-- capart built: (\d{4}-\d{2}-\d{2}) -->")

SPECS_BUILT = {
    "havoc": {
        "catalog": SPECS / "havoc" / "catalog.md",
        "scenarios": SPECS / "havoc" / "scenarios.md",
        "sidecar": SIDECARS / "havoc-scenarios.json",
        "out": PREVIEWS / "havoc-stepper.html",
        "title": "Havoc",
        # One ability per lane, so the primitives gallery can draw a lane swatch on real
        # art even when no scenario happens to exercise that lane. CHARGES is a render-time
        # substitution off a client fact, so its sample is simply an ability the catalog
        # marks as having charges — the lane falls out, it is not assigned here.
        # Sample subjects for the primitives gallery: real art to hang a swatch on. With one
        # treatment these no longer stand for anything — the first is simply the default.
        "scan_samples": ["Metamorphosis", "Blade Dance", "Fel Rush", "Immolation Aura"],
    },
    "demonology": {
        "catalog": SPECS / "demonology" / "catalog.md",
        "scenarios": SPECS / "demonology" / "scenarios.md",
        "sidecar": SIDECARS / "demonology-scenarios.json",
        "out": PREVIEWS / "demonology-stepper.html",
        "title": "Demonology",
        # Sample subjects for the primitives gallery: real art to hang a swatch on. One per
        # role lane plus the spec's own signature button — under one treatment these no longer
        # stand for anything and the first is simply the default.
        "scan_samples": ["Summon Demonic Tyrant", "Hand of Gul'dan", "Shadow Bolt",
                         "Demonbolt"],
    },
    "destruction": {
        "catalog": SPECS / "destruction" / "catalog.md",
        "scenarios": SPECS / "destruction" / "scenarios.md",
        "sidecar": SIDECARS / "destruction-scenarios.json",
        "out": PREVIEWS / "destruction-stepper.html",
        "title": "Destruction",
        # Sample subjects for the primitives gallery: real art to hang a swatch on. One per
        # role lane plus the spec's charge row — under one treatment these no longer stand for
        # anything and the first is simply the default.
        "scan_samples": ["Summon Infernal", "Chaos Bolt", "Incinerate", "Conflagrate"],
    },
    "retribution": {
        "catalog": SPECS / "retribution" / "catalog.md",
        "scenarios": SPECS / "retribution" / "scenarios.md",
        "sidecar": SIDECARS / "retribution-scenarios.json",
        "out": PREVIEWS / "retribution-stepper.html",
        "title": "Retribution",
        # Sample subjects for the primitives gallery: real art to hang a swatch on. Carried
        # over from the per-lane samples this replaced, so the four are still one per role
        # plus a charge candidate — but under one treatment they no longer stand for anything
        # and the first is simply the default.
        "scan_samples": ["Avenging Wrath", "Divine Storm", "Crusader Strike",
                         "Blade of Justice"],
    },
    "devourer": {
        "catalog": SPECS / "devourer" / "catalog.md",
        "scenarios": SPECS / "devourer" / "scenarios.md",
        "sidecar": SIDECARS / "devourer-scenarios.json",
        "out": PREVIEWS / "devourer-stepper.html",
        "title": "Devourer",
        # Sample subjects for the primitives gallery: real art to hang a swatch on. The first is
        # simply the default. Collapsing Star is deliberately among them — it is the first
        # VIRTUAL row any spec has, and the gallery should be able to draw one.
        "scan_samples": ["Void Metamorphosis", "Void Ray", "Reap", "Collapsing Star"],
        # Page-level honesty banners. Devourer is AUTHORED BUT NEVER FLOWN and two of its own
        # premises are recorded as provisional, so the page says so before the reader forms an
        # opinion from it — the per-scenario `⚠ UNSURE` blocks say the rest.
        "notes": [
            "<b>Devourer is authored and has never been built or flown.</b> This page exists to "
            "be reviewed and argued with, not to record a decision. No <code>Catalogs/"
            "Devourer.lua</code> exists; nothing here has run in the client.",
            "<b>Two premises under it are provisional</b> (<code>catalog.md</code> §1): the "
            "hero-tree call (Void-Scarred over Annihilator, contested between sources) and the "
            "branch (<code>!talent.the_hunt</code>). A different call re-authors the roster, not "
            "just the numbers.",
            "<b>The open facts are open</b> (<code>catalog.md</code> §8). The load-bearing one is "
            "item 3: what clears Collapsing Star's gated row is an unmeasured "
            "<code>C_Spell.IsSpellUsable</code> read, and it also carries Void Metamorphosis's "
            "bank hold and Voidblade's rung-1 hold.",
        ],
    },
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
    # Retribution's four override identities — the same lookup, same table.
    427453: 5342121,   # Hammer of Light  (Wake of Ashes's Templar override)
    383328: 461860,    # Final Verdict    (Templar's Verdict's permanent override)
    24275: 7439209,    # Hammer of Wrath  (Judgment's execute-range override)
    407480: 1109508,   # Templar Strike   (Crusader Strike's Templar Strikes override)
    # The two Warlock Diabolist transforms — same lookup, same table. Both are Midnight-new
    # and neither resolves through the media endpoint.
    433891: 841220,    # Infernal Bolt    (Shadow Bolt's / Incinerate's Mother-of-Chaos override)
    433885: 135803,    # Ruination        (Hand of Gul'dan's / Chaos Bolt's Pit-Lord override)
    1276452: 5178162,  # Grimoire: Imp Lord
    1276467: 136217,   # Grimoire: Fel Ravager
    1276672: 615103,   # Summon Doomguard
    # Devourer's six override identities — same lookup, same table (SpellMisc @ 12.1.0.69214).
    1245453: 7554202,  # Cull             (Reap's Void Metamorphosis override)
    1225826: 7554203,  # Eradicate        (Reap's upgraded form)
    1239123: 7554211,  # Hungering Slash  (Voidblade's live form)
    1245483: 1355117,  # Pierce the Veil  (Voidblade's in-Meta Voidsurge cast)
    1245470: 1273724,  # Reaper's Toll    (Voidblade's other in-Meta cast)
    1217610: 7554204,  # Devour           (Consume's Void Metamorphosis override)
}

# --------------------------------------------------------------------------- Blizzard's baseline
#
# ⚠ **THESE ARE NOT DESIGN TOKENS AND THEY MAY NEVER MOVE INTO `render-shelf.md`.**
#
# Everything else this file draws with is an opinion the shelf holds. This block is the opposite:
# it is a *measurement* of what the client already paints on a CDM icon before cap touches it,
# read out of Blizzard's shipped source, and it belongs to the same evidence class as a DB2 row.
# The shelf cannot change these numbers by editing itself, and a rebuild cannot make them
# something we chose. They live here so the preview can draw the row the way the player's client
# would draw it, and so cap's own treatments are judged against that picture rather than against a
# blank icon — which is a different and much easier question.
#
# The consequence that matters: an unaffordable spell is ALREADY marked, in colour, by the client.
# A preview that renders it at full white invites cap to solve a problem the player does not have.
#
# `knowledge/addon-dev/cooldown-manager.md` §3.4 is the claim; this is its transcription.
#   [T1 src @12.1.0: CooldownViewer.lua:1204-1233] — the four-way ladder, in priority order
#   [T1 src @12.1.0: CooldownViewer.lua:14-22]     — the constants
#   [T1 src @12.1.0: CooldownViewer.lua:1195-1202] — desaturation, which means ON COOLDOWN only
#: The sealed-display kinds a scenario may name in a `{sealed: …}` group. The same closed list
#: `Catalog.DISPLAYS` holds on the Lua side, minus the two GRADED kinds — those draw a cue and are
#: stated as one (`hold-sealed`), where these three draw their own art.
SEALED_DISPLAYS = ("count-bands", "count-bar", "pandemic")

CLIENT_PAINT = {
    "_source": "CooldownViewer.lua:1204-1233 + :14-22 @ 12.1.0.69273",
    "_doc": "knowledge/addon-dev/cooldown-manager.md §3.4",
    # SetVertexColor MULTIPLIES, so each of these is a multiply over the icon art — never a
    # hue-rotate, and never something cap can undo by drawing on top.
    "tints": {
        "out-of-range": {
            "rgb": [0.64, 0.15, 0.15], "constant": "ITEM_NOT_IN_RANGE_COLOR",
            "means": "the target is out of range — outranks every other branch",
        },
        "not-enough-power": {
            "rgb": [0.5, 0.5, 1.0], "constant": "ITEM_NOT_ENOUGH_MANA_COLOR",
            "means": "you cannot pay for it — C_Spell.IsSpellUsable's second return",
        },
        "unusable": {
            "rgb": [0.4, 0.4, 0.4], "constant": "ITEM_NOT_USABLE_COLOR",
            "means": "unusable for some other reason",
        },
    },
    # The fourth branch, ITEM_USABLE_COLOR = (1,1,1), is the absence of the other three. It is
    # deliberately not a declarable state: a scenario says nothing and gets the untouched icon.
    "usable_constant": "ITEM_USABLE_COLOR",
    # Not a tint. `cooldownDesaturated = self.isOnActualCooldown` — every assignment, so a grey
    # CDM icon is a statement about COOLDOWN and about nothing else. Driven off the `cd` verdict
    # rather than declared, because `cd` already means exactly that.
    "cooldown_desaturates": True,
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
# `preview` is annotated in the shelf as a viewing aid the addon does not have, and Part 7's
# `lab` is by construction not the style. Neither may reach `ns.Style`.
#
# ⚠ `lab` staying here is not the same claim it used to be. Since 2026-08-16 a lab entry MAY be
# drawn — by the in-game `/cap style` gallery, on cap-owned frames — because you cannot judge a
# treatment without seeing the client draw it. What it may never do is reach the LIVE OVERLAY. So
# the lab crosses into the addon, but through its OWN file and its OWN global (`ns.LabStyle` in
# `Lab.lua`), never through `ns.Style`: every module already reads `ns.Style`, so a `lab` key on it
# would put the guarantee back on everyone remembering. A separate global makes the reach visible
# and greppable, which is exactly what `cmd_check`'s LabStyle reach gate keys off.
NOT_THE_STYLE = ("preview", "lab")
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
    r"\s*(?P<override>[^|]*?)\s*\|\s*(?P<lane>[A-Z]+|—|-)[^|]*\|\s*(?P<charges>[^|]*?)\s*\|",
    re.M,
)
# The override column, in either house style: Havoc writes `Abyssal Gaze ⚠`452497`` (the ⚠
# marking an id we could not resolve an icon slug for), Retribution writes
# `**Hammer of Light `427453`**`. Both are "a display name and the id it resolves to"; the
# bolding and the warning mark are prose, so neither is required.
OVERRIDE_RE = re.compile(r"^\*{0,2}(?P<name>[^⚠`*]+?)\s*\*{0,2}\s*(?:⚠\s*)?`(?P<spell>\d+)`")

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
        # EVERY override in the column, not just the first. A row can wear more than two faces
        # — Devourer's Voidblade has three, one per live form — and a scenario writes whichever
        # one the client would be showing, so binding only the first would leave the others
        # unresolvable names. Split on the `/` the column already uses; a face with no id of its
        # own (Retribution's "Templar Slash") simply does not match and stays unbound, which is
        # the same behaviour it had before.
        for part in m.group("override").split("/"):
            ov = OVERRIDE_RE.match(part.strip())
            if not ov:
                continue
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


# --------------------------------------------------------------------------- scraping


ENTRY_RE = re.compile(r"^(?P<name>.+?)\s+`(?P<verdict>[a-z-]+)`(?P<ann>.*)$")
GROUP_RE = re.compile(r"\{(?P<kind>cues|client|sealed):\s*(?P<body>[^}]*)\}")
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


#: V12's seam. A spec whose press has no Cooldown Manager frame writes its cap-owned panel on
#: either side of the Essential line, and marks the join with `‖`. The composed reading order is
#: the authored left-to-right order (devourer/scenarios.md §7.1), so a virtual entry takes part in
#: elimination exactly like any other — the seam changes how the entry is DRAWN, never its rank.
SEAM = "‖"


def parse_row(raw: str) -> list[dict]:
    """The `- **CDM row.**` bullet's fixed grammar → an ordered list of row entries.

    `·` separates entries. `‖` also separates entries AND marks a surface boundary: everything
    outside the seams is a **virtual row** — a cap-owned icon with no Cooldown Manager frame
    (render-shelf.md V12) — and everything between them is the CDM line.

    ⚠ **Exactly two seams, or none.** The shape this understands is the one §7.1 authorises:
    `[gated panel] ‖ [the Essential line] ‖ [standing panel]`, either panel possibly empty. One
    seam is ambiguous — it cannot say which side is cap's — and three is a geometry nothing has
    authored. Both are refused rather than guessed at.
    """
    row = _flat(raw).rstrip(".")
    seams = row.count(SEAM)
    if seams not in (0, 2):
        _die(f"CDM row has {seams} `{SEAM}` seam(s): {row!r}\n"
             f"       A virtual panel is written `[gated] {SEAM} [the CDM line] {SEAM} "
             "[standing]` — two seams or none.\n"
             "       One seam cannot say which side cap owns, and three is a geometry no spec "
             "has authored.")
    segments = row.split(SEAM) if seams else [row]
    entries = []
    for seg_i, segment in enumerate(segments):
        # With two seams the segments alternate virtual / CDM / virtual, so an even index is
        # cap's own surface. With no seam there is one segment and nothing is virtual.
        virtual = bool(seams) and seg_i % 2 == 0
        entries += _parse_segment(segment, virtual)
    return entries


def _parse_segment(segment: str, virtual: bool) -> list[dict]:
    entries = []
    for chunk in segment.split(" · "):
        chunk = chunk.strip().strip("·").strip()
        if not chunk:
            continue
        if DEAD_GROUP_RE.search(chunk):
            _die(f"CDM row entry still carries a retired `{{dots: …}}` group: {chunk!r}\n"
                 "       The green/red dependency dots were retired 2026-08-13 with "
                 "render-shelf V6.\n"
                 "       A SATISFIED dependency now draws nothing — delete the group. A "
                 "BLOCKED one is\n"
                 "       the `hold-readable` verdict itself, which already IMPLIES `blocked` — "
                 "do not also\n"
                 "       declare `{cues: blocked}`, which is a second mention of one cue.")
        groups = {m.group("kind"): m.group("body") for m in GROUP_RE.finditer(chunk)}
        bare = GROUP_RE.sub("", chunk).strip()
        m = ENTRY_RE.match(bare)
        if not m:
            _die(f"CDM row entry does not parse: {chunk!r}\n"
                 "       expected: <Ability> `<verdict>` [{cues: …}]")
        entry = {"name": m.group("name").strip(), "verdict": m.group("verdict")}
        if "cues" in groups:
            entry["cues"] = [c.strip() for c in groups["cues"].split(",") if c.strip()]
        if "sealed" in groups:
            # A SEALED DISPLAY on this row: art the CLIENT draws from a rule cap authored and
            # never reads back. Its own channel rather than a cue, because a cue is a badge cap
            # shows and this is not one — and its own channel rather than part of the verdict,
            # because a display that ELIMINATES (`ruled-sealed`) and one that merely informs are
            # the same machinery pointed at different facts.
            entry["sealed"] = [c.strip() for c in groups["sealed"].split(",") if c.strip()]
        if "client" in groups:
            # What BLIZZARD paints on this icon in this state, independent of anything cap
            # concluded. Authored separately from the verdict on purpose: if it were derived
            # from `starved` the two could never disagree, and "does cap's badge add anything
            # to the client's own mark?" would be unanswerable by construction.
            entry["client"] = groups["client"].strip()
        if virtual:
            entry["virtual"] = True
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


# Each spec names its own scenario prefix — Havoc walks `ST-n` / `AoE-n`, Retribution `RET-n`,
# Devourer `B-n` / `M-n`. The prefix carries no meaning here beyond ordering the stepper, so it is
# matched by shape. ⚠ A ONE-LETTER prefix is allowed: the bound used to be two and Devourer's
# build/window split is `B`/`M`, which would have forced a spec to rename its scenarios — and the
# ids are cited by section number across three files.
HEADING_RE = re.compile(r"^###\s+(?P<id>[A-Z][A-Za-z]{0,4}-\d+)\s+·\s+(?P<title>.+?)\s*$", re.M)


def scrape_scenarios(path: Path) -> list[dict]:
    """scenarios.md → the ordered scenario list. The doc leads; this reads it."""
    text = path.read_text(encoding="utf-8")
    marks = list(HEADING_RE.finditer(text))
    if not marks:
        _die(f"no `### ST-n · …` scenario headings in {path.relative_to(ROOT)}")

    # ⚠ A scenario's body ends at the next scenario OR at the next level-2 heading, whichever
    # comes first. Without the second terminator the LAST scenario absorbs everything below it:
    # in a spec that keeps its walk inside `catalog.md` that is the whole rest of the document —
    # measured 2026-08-19, RET-13 had swallowed 19 blocks including the changelog and rendered
    # them on the page. A spec with a separate `scenarios.md` only escapes this by luck of
    # formatting (whatever follows the last scenario happening to contain no `- **Bold.**`
    # bullets), so this is not a single-file problem and the fix is not a second file.
    section = [mm.start() for mm in re.finditer(r"(?m)^##\s+", text)]

    out = []
    for i, m in enumerate(marks):
        stop = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        nxt = next((pos for pos in section if pos > m.end()), None)
        if nxt is not None:
            stop = min(stop, nxt)
        body = text[m.end(): stop]
        bullets = {}
        order = []
        for part in re.split(r"(?m)^- \*\*", "\n" + body)[1:]:
            label, _, rest = part.partition("**")
            label = label.split("(")[0].strip().rstrip(".")
            bullets[label] = rest.strip()
            order.append(label)

        if "CDM row" not in bullets:
            _die(f"{m.group('id')} has no `- **CDM row.**` bullet — the preview cannot render it")
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
            for kind in e.get("sealed", []):
                if kind not in SEALED_DISPLAYS:
                    _die(f"{sc['id']}: sealed display {kind!r} on {e['name']!r} is not one of "
                         f"cap's display kinds ({', '.join(sorted(SEALED_DISPLAYS))}).\n"
                         "       A scenario names the SINK, never the picture — the picture is "
                         "render-shelf.md's.")
            if e["verdict"] == "ruled-sealed" and not e.get("sealed"):
                _die(f"{sc['id']}: {e['name']!r} is `ruled-sealed` but names no {{sealed: …}} "
                     "display.\n"
                     "       That verdict says a CLIENT-drawn band ruled the row out; without a "
                     "display there is\n"
                     "       nothing drawing it, and the row would be silently un-eliminated in "
                     "the client.")
            cl = e.get("client")
            if cl is not None and cl not in CLIENT_PAINT["tints"]:
                _die(f"{sc['id']}: client state {cl!r} on {e['name']!r} is not one of Blizzard's "
                     f"branches ({', '.join(sorted(CLIENT_PAINT['tints']))}).\n"
                     "       The fourth branch — usable — is the absence of a declaration, not a "
                     "name you may write.")
            if cl and e["verdict"] == "cd":
                # The client paints ONE of these per icon and the cooldown path does not reach
                # RefreshIconColor's ladder in a way a scenario can meaningfully state. A row
                # that claims both is claiming a picture the client does not produce.
                _die(f"{sc['id']}: {e['name']!r} is `cd` and also declares client state {cl!r}. "
                     "A swiped row is already ruled out natively; stating a second client mark on "
                     "it asserts a composite the source does not describe.")


# --------------------------------------------------------------------------- assets


#: Encoded-asset cache, keyed by image CONTENT plus encode settings. Gitignored (`raw/`).
#:
#: ⚠ This exists because the encode is genuinely expensive and almost always redundant. Measured
#: 2026-08-19: `webp method=6` costs 2.94s for one 512x256 VFX sheet against 0.03s at method=4 —
#: a hundredfold, for 15% of file size. With six sheets, encoded once per spec, `build --all`
#: spent ~30s re-encoding art that had not changed, and `check` paid it a second time because it
#: re-renders both pages to compare. So a one-line colour edit cost a minute of pure recompute.
#:
#: Keyed on the decoded pixels rather than the source path, so it stays correct when a generator
#: rewrites a sheet byte-for-byte identically, and misses when the pixels actually move.
_URI_CACHE = ROOT / "raw" / "capart-uri"


def _data_uri(img: Image.Image, tokens: dict) -> tuple[str, int]:
    fmt = tokens["assets"].get("encode", "webp")
    quality = tokens["assets"].get("quality", 90)
    key = hashlib.sha256(
        img.tobytes() + f"|{img.mode}|{img.size}|{fmt}|{quality}|m6".encode()
    ).hexdigest()
    cached = _URI_CACHE / f"{key}.txt"
    try:
        uri = cached.read_text(encoding="ascii")
        return uri, len(uri)
    except OSError:
        pass

    buf = io.BytesIO()
    if fmt == "webp":
        img.save(buf, "WEBP", quality=quality, method=6)
        mime = "image/webp"
    else:
        img.save(buf, "PNG", optimize=True)
        mime = "image/png"
    uri = f"data:{mime};base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    try:
        _URI_CACHE.mkdir(parents=True, exist_ok=True)
        cached.write_text(uri, encoding="ascii")
    except OSError:
        pass          # a cache that cannot be written is a slow build, never a wrong one
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
    the badge sprites and V11's stripe sheet. The claim was never about rings — it is *art the shelf
    recolors must be art `SetVertexColor` can actually recolor*. `tint: "shelf"` is the token
    spelling of that claim (the colour comes from the shelf, not from the art).

    Losing this silently would be the worst possible outcome of retiring a primitive, so
    `cmd_check` separately asserts that every art-bearing primitive still declares it — a guard whose
    subject set quietly emptied keeps passing while guaranteeing nothing.
    """
    if tint == "shelf" and tintable is False:
        _die(
            f"{what} declares tint: \"shelf\" but {source} measured mean saturation {sat} — it "
            "carries a BAKED HUE.\n"
            "       SetVertexColor multiplies, so that art can only be darkened toward its own "
            "hue; the authored colour is not drawable on it, and a preview that showed one "
            "would be a lie.\n"
            "       Fix it one of three ways: pick neutral art (the vendored Kenney frames "
            "measure 0.000); declare tint: \"none\" and accept the art's own hue; or declare "
            "tint: \"desaturate+shelf\", which builds but stamps a visible ⚠ because "
            "desaturate-then-tint is unverified in client."
        )
    return tint == "desaturate+shelf"


#: Token groups OUTSIDE the cue vocabulary that draw a sprite off the badge sheet, as
#: (group, key-holding-the-frame-name). V16's banded mark and V19's refresh badge both point at a
#: name they do not ship, on the stated grounds that "every name here is already on the cue
#: vocabulary's sheet list" (`addon_style`).
#:
#: ⚠ THAT WAS A COINCIDENCE, NOT A GUARANTEE, AND IT BROKE. On 2026-08-23 the negative cues were
#: made still (V5.1), which dropped `timer_CW_75` off `blocked`'s frame list — and `timer_CW_75` is
#: the sprite V19's pandemic badge draws. Nothing named the dependency, so the failure would have
#: been a badge that silently stopped shipping: no missing file, no failing gate, just a corner of
#: the overlay that went blank. Declaring the borrow here means a frame list can be edited without
#: reading every other token group first, and a borrowed name that no longer exists on disk dies in
#: `badge_assets` like any other.
BORROWED_FRAMES: tuple[tuple[str, str], ...] = (
    ("count", "mark"),
    ("pandemic", "frame"),
)


def borrowed_frames(tokens: dict) -> list[tuple[str, str]]:
    """Every badge-sheet sprite named by a non-cue token group, as (frame, who-named-it)."""
    out = []
    for group, key in BORROWED_FRAMES:
        name = (tokens.get(group) or {}).get(key)
        if name:
            out.append((name, f"tokens.{group}.{key}"))
    return out


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
    wanted = [(f, f"cue {key!r}") for key, cue in tokens["cues"].items() for f in cue["frames"]]
    wanted += borrowed_frames(tokens)
    for frame, who in wanted:
        if frame in out:
            continue
        if frame in GENERATED_FRAMES:
            img, where = GENERATED_FRAMES[frame](), f"generated ({frame})"
        else:
            path = root / f"{frame}.png"
            if not path.exists():
                _die(f"{who} names frame {frame!r}, not found at "
                     f"{(root / f'{frame}.png').relative_to(ROOT)} and not in "
                     f"GENERATED_FRAMES — tokens.badges.asset_root is "
                     f"{badges['asset_root']!r}")
            img, where = Image.open(path).convert("RGBA"), str(path.relative_to(ROOT))
        measure = uiart.tintability(img)
        open_flag = assert_tintable(
            f"badge sprite {frame!r} ({who})", where,
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
    # V14's promotion ring, same reason and the same directory. It ships to `Media/` rather than
    # `Media/lab/` because it is the STYLE now — promotion moved the art with the treatment,
    # exactly as V11's stripe sheet moved on 2026-08-16.
    if "promotion" in out:
        out["promotion"] = dict(out["promotion"], texture_root=MEDIA_TEXTURE_ROOT)
    # V16/V17 and V19 name BADGE art — the mark, the plate, the window's sprite — so their root is
    # the badge directory rather than Media/. They ship no file of their own; they BORROW off the
    # cue vocabulary's sheet, and that borrow is declared in `BORROWED_FRAMES` rather than left to
    # coincide with some cue's frame list (see the ⚠ there — the coincidence broke on 2026-08-23).
    for key in ("count", "pandemic"):
        if key in out:
            out[key] = dict(out[key], texture_root=BADGE_TEXTURE_ROOT)
    # V16/V17's band builder needs three FILE NAMES it must not restate: the plate is the shape
    # `shape_images` generates, and the hatch is V11's own sheet under a different root. Injected
    # here rather than declared in the shelf, so a rename in one place cannot leave the band
    # naming a texture that no longer ships.
    if "count" in out:
        # ⚠ The names the BAND actually points at are the PRE-TINTED crops, not the neutral
        # source art. A band cannot recolour what it names (`|c` tints text and not an inline
        # texture, measured 2026-08-22), so the hue is in the file. `_pos` / `_neg` are the
        # polarity pair; the plate is `_ink` and has no polarity, because contrast is not
        # polarity (V5.1).
        out["count"] = dict(out["count"], plate=PLATE_TEXTURE + "_ink",
                            hatch=tokens["hatch"]["texture"], hatch_root=MEDIA_TEXTURE_ROOT)
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
    # Where the gallery finds art the LAB owns. Its own root, so `Media/lab/` stays legible from
    # `ls` and an entry's art can be deleted with the entry when the experiment loses.
    # TWO roots, because a lab entry now draws from both. Its SPRITE is `fire`, which the style
    # owns since `priority` took it as a glyph; its SHEET is VFX art the lab still owns. Pointing
    # both at one directory is what would put a second copy of `fire` on disk.
    if any(isinstance(v, dict) and v.get("sprite")
           for k, v in out.items() if not k.startswith("_")):
        out["_sprites"] = {"texture_root": BADGE_TEXTURE_ROOT}
    if any(isinstance(v, dict) and v.get("sheet")
           for k, v in out.items() if not k.startswith("_")):
        out["_sheets"] = {"texture_root": LAB_TEXTURE_ROOT}

    # A flipbook's texcoord step is `cell / sheet`, NOT `1 / cols` — the sheet is padded to a
    # power of two, so an 8x3 grid of 64px cells lives in a 512x256 texture with a quarter of the
    # height unused. Dividing by `rows` would stretch every frame and walk into the padding.
    # Computed here, from the file on disk, so neither the gallery nor the preview can assume it.
    for key, entry in out.items():
        if key.startswith("_") or not isinstance(entry, dict) or not entry.get("sheet"):
            continue
        path = VFX_DIR / f"{entry['sheet']}.png"
        if not path.exists():
            _die(f"lab entry {key!r} names sheet {entry['sheet']!r}, missing at "
                 f"{path.relative_to(ROOT)}")
        w, h = Image.open(path).size
        cell = entry.get("cell")
        if not cell:
            _die(f"lab entry {key!r} declares no `cell` — the sheet is padded, so the frame "
                 "size cannot be inferred from its dimensions")
        entry["du"] = round(cell / w, 6)
        entry["dv"] = round(cell / h, 6)
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
    """Every sprite frame the badge sheet ships, in declaration order, deduplicated.

    The cue vocabulary first, then the groups that BORROW off the same sheet — see
    `BORROWED_FRAMES` for why the borrow is declared instead of inferred.
    """
    out = []
    for cue in tokens["cues"].values():
        for frame in cue["frames"]:
            if frame not in out:
                out.append(frame)
    for frame, _who in borrowed_frames(tokens):
        if frame not in out:
            out.append(frame)
    return out


# A badge glyph draws at roughly a quarter of the shelf's icon, so 128px source art reaches the
# client as a heavy minification. Downsampling here (Pillow, LANCZOS) beats doing it at draw time.
SPRITE_PX = 64
SHAPE_PX = 64          # texture resolution for the generated shapes — plumbing, not a look
SHAPE_SS = 4           # supersampling factor for the disc's edge
PLATE_TEXTURE, HALO_TEXTURE = "plate", "halo"


#: Frames cap authors itself, by name. Consulted BEFORE the vendored asset directory, so a
#: generated frame needs no file on disk and cannot go stale against one.
#: Empty since 2026-08-19. `chevron_*` was authored as the `priority` glyph and retired the same
#: day the flame replaced it — probe art dies in the edit that settles the question it asked.
#: The mechanism stays: a cue frame named here needs no file on disk and cannot go stale.
GENERATED_FRAMES: dict = {}


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
    """V2's ring sheet as the preview draws it: a `data:` URI plus its measurement.

    The preview uses it as a `mask-image` over the lane hue and steps `mask-position` at
    `tokens.motion.tick_s`, which is the same art, the same walk and the same rate as the client.
    """
    img = ring_image(tokens)
    if img is None:
        return None
    ring = tokens["ring"]
    measure = uiart.tintability(img)
    assert_tintable("ring flipbook sheet (Part 7)", "capart.ring_flipbook (generated)",
                    ring.get("tint", "none"), measure["mean_saturation"], measure["tintable"])
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    uri = "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode("ascii")
    return {"uri": uri, "bytes": len(uri), "size": list(img.size),
            "mean_saturation": measure["mean_saturation"], "tintable": measure["tintable"],
            "frames": ring["frames"], "grid": ring["grid"], "tile_px": ring["tile_px"],
            "thickness_px": ring["thickness_px"], "travel_px": ring.get("travel_px", 0),
            "tint": ring.get("tint", "none")}


# Every glyph a keybind can contain — digits, letters in both cases (a lowercase-modifier
# notation like `sF` needs them), the punctuation a keyboard binds, and the four arrows a mouse
# wheel or a direction key can produce. A font subset to this is 5-15 KB instead of 100-500 KB,
# which is what makes both the preview page and a SHIPPED font affordable.
KEY_GLYPHS = ("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
              "-+=[]\\;\',./`~!@#$%^&*()<> \u2191\u2193\u2190\u2192")

_FONT_CACHE = ROOT / "raw" / "fonts"


FONT_NOTICE = """\
{ship_as}.ttf — third-party font shipped with Combat Assist Plus.

Source        {family}
Upstream      {url}
Licence       {license} (see OFL.txt beside this file)

RENAMED ON PURPOSE. The upstream family carries the Reserved Font Name {rfn!r}, and the file here
is a SUBSET — about 45 glyphs, the alphabet a keybind can contain — which OFL 1.1 counts as a
Modified Version. Clause 3 forbids a Modified Version from using the Reserved Font Name, so it
ships as {ship_as}. The copyright and licence records inside the file are untouched, because the
same licence requires those to travel with it.

Generated by `wowkb.capart export lua` from render-shelf.md Part 6. Do not edit by hand.
"""


def _font_text(url: str) -> bytes:
    """A licence file fetched and cached beside the fonts it governs."""
    _FONT_CACHE.mkdir(parents=True, exist_ok=True)
    cached = _FONT_CACHE / (hashlib.sha256(url.encode()).hexdigest()[:16] + ".txt")
    if not cached.exists():
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": uiart._BROWSER_UA["User-Agent"]})
        with urllib.request.urlopen(req, timeout=180) as r:
            cached.write_bytes(r.read())
    return cached.read_bytes()


def _font_source(spec: dict) -> bytes:
    """The raw TTF named by a font spec: `{fdid}` reads CASC, `{url}` reads the web, once."""
    if spec.get("fdid"):
        return uiart.fetch_blp(int(spec["fdid"]))
    url = spec.get("url")
    if not url:
        _die(f"font spec {spec!r} names neither `fdid` nor `url`")
    _FONT_CACHE.mkdir(parents=True, exist_ok=True)
    cached = _FONT_CACHE / (hashlib.sha256(url.encode()).hexdigest()[:16] + ".ttf")
    if not cached.exists():
        import urllib.request
        req = urllib.request.Request(url, headers={"User-Agent": uiart._BROWSER_UA["User-Agent"]})
        with urllib.request.urlopen(req, timeout=180) as r:
            cached.write_bytes(r.read())
    return cached.read_bytes()


def _rename_font(font, name: str) -> None:
    """Rewrite a font's identity, which OFL 1.1 clause 3 REQUIRES for a Reserved Font Name.

    Share Tech Mono ships "with Reserved Font Name 'Share'", and a subset is a Modified Version —
    so the shipped file may not carry the original name. Only the IDENTITY records change: the
    copyright (0), licence (13) and licence URL (14) are left exactly as they are, because the
    same licence requires those to travel with the file.
    """
    ident = {1: name, 3: name, 4: name, 6: name, 16: name}
    for record in font["name"].names:
        if record.nameID in ident:
            record.string = ident[record.nameID].encode("utf-16-be" if record.platformID == 3
                                                        else "latin-1")


def _subset_font(data: bytes, label: str, ship_as: str | None = None) -> bytes:
    """Cut a font down to `KEY_GLYPHS`.

    ⚠ A TrueType file opens `\x00\x01\x00\x00` (or `true`/`ttcf`/`OTTO`). Checked before
    anything else because wago.tools answers a bad FileDataID with a 34-byte JSON error, and a
    JSON blob base64'd into an `@font-face` fails SILENTLY — the page falls through to the next
    family and nothing anywhere says the fidelity was lost.
    """
    if data[:4] not in (b"\x00\x01\x00\x00", b"true", b"ttcf", b"OTTO"):
        _die(f"{label} is not a font file (opens {data[:4]!r}) — the fdid or url is wrong, "
             "or the fetch was refused")
    from fontTools import subset as ftsubset
    font = ftsubset.load_font(io.BytesIO(data), ftsubset.Options())
    # `hinting=False` is most of the saving — measured on ARIALN, 37 KB with the hinting tables
    # and 9 KB without. It costs nothing either side of this: a browser rasterises small text with
    # its own hinter, and the WoW client converts a TTF to a signed-distance-field slug (the
    # install's `Fonts/615960.slug` is FRIZQT's) where the original hints play no part.
    # `layout_features=[]` drops shaping tables a keybind alphabet has no use for.
    subsetter = ftsubset.Subsetter(options=ftsubset.Options(
        layout_features=[], hinting=False, desubroutinize=True, notdef_outline=True))
    subsetter.populate(text=KEY_GLYPHS)
    subsetter.subset(font)
    if ship_as:
        _rename_font(font, ship_as)
    out = io.BytesIO()
    font.save(out)
    font.close()
    return out.getvalue()


def font_asset(spec: dict, label: str) -> dict:
    """One `@font-face`-ready font: fetched, subset to the keybind alphabet, base64'd."""
    raw = _font_source(spec)
    data = _subset_font(raw, label, spec.get("ship_as"))
    uri = "data:font/ttf;base64," + base64.b64encode(data).decode("ascii")
    return {"uri": uri, "bytes": len(uri), "family": spec.get("ship_as") or spec["family"],
            "source_bytes": len(raw), "subset_bytes": len(data),
            "origin": f"CASC {spec['fdid']}" if spec.get("fdid") else spec.get("url", ""),
            "license": spec.get("license", ""), "shippable": bool(spec.get("shippable"))}


def lab_font_assets(tokens: dict) -> dict:
    """Every font a Part 7 hotkey entry asks for. Lab only — nothing here is the style."""
    out = {}
    for key, entry in (tokens.get("lab") or {}).items():
        if key.startswith("_") or not isinstance(entry, dict):
            continue
        if entry.get("draws") != "hotkey" or not entry.get("font"):
            continue
        out[key] = font_asset(entry["font"], f"lab.{key}")
    return out


def hotkey_font_asset(tokens: dict) -> dict | None:
    """V15's font, pulled out of CASC by FileDataID and embedded as a `data:` URI.

    ⚠ WHY THIS IS ALLOWED HERE AND NOWHERE ELSE. `render-shelf.md` Part 3 says extracted Blizzard
    art is *"for measuring and for the preview, never for the addon's `Media/` folder"* — the rule
    is about what cap **redistributes**, and the preview redistributes nothing: it is a local
    workflow artifact in this repo, exactly like the spell icons it has always embedded. Nothing
    on this path reaches `Style.lua` or `Media/`, and `export` has no idea it exists.

    It matters because the alternative was a guessed CSS family, and a substitute font gets
    ADVANCE WIDTH wrong — which is precisely the question the preview is asked ("does `C-S-F1` fit
    the corner"). A near-enough letterform that lies about width answers it backwards.
    """
    spec = (tokens.get("preview") or {}).get("hotkey_font")
    if not spec:
        return None
    return font_asset(spec, "tokens.preview.hotkey_font")


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
    reach the client through a path the preview never rendered.
    """
    badges = tokens["badges"]
    src = ROOT / "projects" / "combat-assist" / badges["asset_root"]
    tint = badges.get("tint", "none")
    BADGE_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for frame in badge_frames(tokens):
        if frame in GENERATED_FRAMES:
            img, where = GENERATED_FRAMES[frame](), f"generated ({frame})"
        else:
            path = src / f"{frame}.png"
            if not path.exists():
                _die(f"cue frame {frame!r} not found at {path.relative_to(ROOT)} "
                     "and not in GENERATED_FRAMES")
            img, where = Image.open(path).convert("RGBA"), str(path.relative_to(ROOT))
        measure = uiart.tintability(img)
        assert_tintable(f"badge sprite {frame!r}", where,
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
    written += _prune_badges(tokens)
    return written


def _prune_badges(tokens: dict) -> list[tuple[str, tuple[int, int]]]:
    """Delete badge TGAs the shelf no longer names, and say which.

    ⚠ THE EXPORT IS THE ONE DOOR, SO IT OWNS DELETION TOO. A frame dropped from the vocabulary
    used to keep shipping forever — `chevron_1`/`chevron_2` were retired with the `priority` glyph
    on 2026-08-19 and were still in the addon four days later, and making the negatives still
    (V5.1, 2026-08-23) orphaned four more. None of them draws anything; they are payload in a
    released addon that no code can reach, which is the same defect as a stale generated file and
    is invisible for the same reason: nothing looks at what is NOT named.

    ⚠ THE KEEP SET COMES FROM THE TOKENS, NOT FROM WHAT THIS RUN WROTE. `export badges` and
    `export lua` write into the same directory from different generators, so pruning against one
    run's output deletes the other's — measured immediately, the first draft of this took out
    V16's three pre-tinted crops. What is legal in `Media/badges/` is a property of the shelf, and
    only the shelf gets to answer it.
    """
    keep = set(badge_frames(tokens)) | set(shape_images(tokens))
    keep |= {name for name in count_frames(tokens) if not name.startswith(tokens["hatch"]["texture"])}
    gone = []
    for path in sorted(BADGE_DIR.glob("*.tga")):
        if path.stem not in keep:
            path.unlink()
            gone.append((path.stem + " (pruned)", (0, 0)))
    return gone


#: V16/V17's pre-tinted crops. One file per (art, hue), because a band's art CANNOT be recoloured
#: at draw time: measured `[client 2026-08-22]`, a `|cAARRGGBB…|r` escape tints the band's TEXT and
#: leaves an inline `|T…|t` at full white. `SetVertexColor` is not available either — the sink owns
#: a FontString, and the art inside it is named by a path rather than held as a texture object.
#:
#: So the hue has to be BAKED, which render-shelf L5 predicted before any of it shipped: "a
#: pre-composited crop is no longer neutral white-in-alpha art… the hue has to be baked, which
#: means capart export generates one crop per hue, exactly as it already generates the badge TGAs.
#: That is a token change and a generator change, not a new art channel."
COUNT_HUES = ("pos", "neg")


def count_tinted(img: Image.Image, rgb: list, alpha: float = 1.0) -> Image.Image:
    """Neutral white-in-alpha art multiplied by one authored colour — what `SetVertexColor` does,
    done at export time because the draw-time channel is not there.

    ⚠ `alpha` is baked for the same reason the colour is: the art reaches the client as an inline
    `|T…|t` escape inside a FontString, and an escape carries neither a vertex colour nor an alpha
    — a colour escape does not reach art at all `[client 2026-08-22]`. So a translucent hatch has
    to BE translucent in the file. It defaults to 1.0, which leaves the mark and the plate exactly
    as they were.
    """
    r, g, b = (max(0.0, min(1.0, c)) for c in rgb[:3])
    a = max(0.0, min(1.0, alpha))
    out = img.convert("RGBA")
    src = out.split()
    return Image.merge("RGBA", (
        src[0].point(lambda v, k=r: round(v * k)),
        src[1].point(lambda v, k=g: round(v * k)),
        src[2].point(lambda v, k=b: round(v * k)),
        src[3] if a >= 1.0 else src[3].point(lambda v, k=a: round(v * k)),
    ))


def band_hatch(tokens: dict) -> Image.Image:
    """V17's hatch as a SINGLE CROP, pre-rendered at the size it will be drawn.

    ⚠ An inline `|T…|t` escape **cannot tile — it stretches** `[client 2026-08-22]`. `Paint.Hatch`
    draws V11's sheet with `SetTexCoord` past 1 so the stripes keep their authored pitch at any
    icon size; an escape has no such control and crams the whole 128px sheet into whatever box it
    is given, so the same file came out coarse and squashed two icons from a correct one.

    So the band gets its own crop, generated at `tokens.count.hatch_px` with the pitch chosen so
    the ON-SCREEN result matches V11's. It is not tileable and does not need to be: it is drawn
    exactly once, at one size, and seaming is a property of repetition.
    """
    cnt, h = tokens["count"], tokens["hatch"]
    px = cnt["hatch_px"]
    # The file is power-of-two (the client wants it); the pitch is scaled so that squeezing the
    # file into `hatch_px` lands the stripes on V11's own pitch.
    size = 1 << (px - 1).bit_length()
    # The pitch that would land exactly on V11's on-screen spacing once the file is squeezed into
    # `hatch_px` — then snapped to a divisor of the tile, because `hatch_sheet` refuses a pitch
    # that would seam. Seaming cannot happen here (the crop is drawn once, never repeated), but
    # the guard is worth keeping honest rather than bypassing, and the nearest divisor is within
    # a couple of pixels at icon scale.
    target = h["pitch_px"] * size / px
    divisors = [d for d in range(2, size + 1) if size % d == 0]
    pitch = min(divisors, key=lambda d: abs(d - target))
    return hatch_sheet(dict(h, tile_px=size, pitch_px=pitch))


def count_frames(tokens: dict) -> dict:
    """`{ filename: Image }` for every pre-tinted crop V16/V17 names, or `{}` if `count` is absent.

    The plate is deliberately NOT hue-varied: its job is contrast, not polarity (V5.1 — hue
    carries polarity and only polarity), so it is baked once at the badge plate's own colour.
    """
    cnt = tokens.get("count")
    if not cnt:
        return {}
    shapes = shape_images(tokens)
    badges = tokens["badges"]
    src = ROOT / "projects" / "combat-assist" / badges["asset_root"]

    def load(name: str) -> Image.Image:
        if name in shapes:
            return shapes[name]
        path = src / f"{name}.png"
        if not path.exists():
            _die(f"tokens.count names art {name!r}, missing at {path.relative_to(ROOT)}")
        img = Image.open(path).convert("RGBA")
        return img.resize((SPRITE_PX, SPRITE_PX), Image.LANCZOS) if img.size[0] > SPRITE_PX else img

    # ⚠ The source names are the SHELF's, not `Style.lua`'s. `addon_style` injects `plate` and
    # `hatch` onto the count group for the addon's benefit; here we are upstream of that, so the
    # neutral art is named from where it is actually declared.
    sheet = tokens["hatch"]["texture"]
    out = {}
    for hue, rgb in (("pos", cnt["rgb"]), ("neg", cnt["low_rgb"])):
        out[f"{cnt['mark']}_{hue}"] = count_tinted(load(cnt["mark"]), rgb)
        # The hatch alone is translucent: it covers the whole icon face, and an opaque one hides
        # the ability art the row is identified by.
        out[f"{sheet}_{hue}"] = count_tinted(band_hatch(tokens), rgb,
                                             cnt.get("hatch_alpha", 1.0))
    # One plate, no hue: contrast is not polarity.
    out[f"{PLATE_TEXTURE}_ink"] = count_tinted(shapes[PLATE_TEXTURE],
                                               badges["plate"]["rgb"])
    return out


def export_count(tokens: dict) -> list[tuple[str, tuple[int, int]]]:
    """Ship V16/V17's pre-tinted crops beside the neutral badge art they are derived from."""
    written = []
    for name, img in count_frames(tokens).items():
        dest = MEDIA_DIR if name.startswith(tokens["hatch"]["texture"]) else BADGE_DIR
        written.append((name, _write_tga(img, name, dest)))
    return written


def export_ring(tokens: dict) -> list[tuple[str, tuple[int, int]]]:
    """Vendor V2's ring flipbook into `Media/`, beside `Media/badges/` — declared art, not lab art.

    Lab art lives in `Media/lab/` and style art does not, so `ls Media/` still says which is which.
    The tint guard runs here as well as on the preview path, so a sheet with a hue baked into it
    cannot reach the client through a route the preview never rendered.
    """
    img = ring_image(tokens)
    if img is None:
        return []
    ring = tokens["ring"]
    measure = uiart.tintability(img)
    assert_tintable("ring flipbook sheet (Part 7, ship path)",
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


def promotion_asset(tokens: dict) -> dict:
    """V14's sheet as the preview draws it: a `data:` URI plus its measurement."""
    promo = tokens.get("promotion")
    if not promo:
        return {}
    path = VFX_DIR / f"{promo['texture']}.png"
    if not path.exists():
        _die(f"V14 names {promo['texture']!r}, missing at {path.relative_to(ROOT)}")
    img = Image.open(path).convert("RGBA")
    measure = uiart.tintability(img)
    assert_tintable("promotion ring (V14)", str(path.relative_to(ROOT)),
                    promo.get("tint", "none"), measure["mean_saturation"], measure["tintable"])
    uri, nbytes = _data_uri(img, tokens)
    return {"uri": uri, "bytes": nbytes, "w": img.size[0], "h": img.size[1]}


def export_promotion(tokens: dict) -> list[tuple[str, tuple[int, int]]]:
    """Vendor V14's proc-ring flipbook into `Media/`, beside the ring and the stripe sheet.

    The tint guard has real teeth here: V14's whole advantage over Blizzard's own proc glow is
    that it is NEUTRAL and therefore tintable, so a future edit that bakes a hue into
    `wowkb.procring` must fail loudly rather than silently shipping art `SetVertexColor` cannot
    move.
    """
    promo = tokens.get("promotion")
    if not promo:
        return []
    path = VFX_DIR / f"{promo['texture']}.png"
    if not path.exists():
        _die(f"V14 names {promo['texture']!r}, missing at {path.relative_to(ROOT)} — "
             "regenerate it with `python -m wowkb.procring`")
    img = Image.open(path).convert("RGBA")
    measure = uiart.tintability(img)
    assert_tintable("promotion ring (V14, ship path)", str(path.relative_to(ROOT)),
                    promo.get("tint", "none"), measure["mean_saturation"], measure["tintable"])
    return [(promo["texture"], _write_tga(img, promo["texture"], MEDIA_DIR))]


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


#: Art the LAB owns, by frame name. Kept separate from the cue frames on purpose: a lab sprite
#: is not part of the badge vocabulary, ships to `Media/lab/` rather than `Media/badges/`, and
#: must be deletable with its entry when the experiment loses (Part 7 rule 4).
#: Empty since 2026-08-19: `fire` was promoted to a cue frame when `priority` took it as its
#: glyph, so it now ships to `Media/badges/` as declared art and the lab reads it FROM THERE.
#: Promotion moves art rather than copying it — the same rule that moved V11's stripe sheet.
LAB_SPRITES: tuple[str, ...] = ()


def lab_sprite_assets(tokens: dict) -> dict:
    """The lab's own sprite frames as `data:` URIs, measured by the same tint guard.

    A lab entry may draw art the style does not, but it may not draw art nobody measured — a
    baked-hue sprite would show the gallery a recolour `SetVertexColor` could never produce, and
    the whole point of the in-client gallery is that it does not lie about the client.
    """
    root = ROOT / "projects" / "combat-assist" / tokens["badges"]["asset_root"]
    tint = tokens["badges"].get("tint", "none")
    out: dict[str, dict] = {}
    for frame in LAB_SPRITES:
        path = root / f"{frame}.png"
        if not path.exists():
            _die(f"lab sprite {frame!r} not found at {path.relative_to(ROOT)}")
        img = Image.open(path).convert("RGBA")
        measure = uiart.tintability(img)
        assert_tintable(f"lab sprite {frame!r}", str(path.relative_to(ROOT)),
                        tint, measure["mean_saturation"], measure["tintable"])
        uri, nbytes = _data_uri(img, tokens)
        out[frame] = {"uri": uri, "bytes": nbytes,
                      "mean_saturation": measure["mean_saturation"]}
    return out


VFX_DIR = ROOT / "projects" / "combat-assist" / "previews" / "assets" / "vfx"


def vfx_assets(tokens: dict) -> dict:
    """The lab's FLIPBOOK sheets — VFX art, which the tint guard cannot simply assert on.

    Every other art path in this file demands neutral art, because the shelf's primitives are
    tinted per lane and a baked hue makes `SetVertexColor` a liar. A particle effect is the one
    case where that is the wrong demand: an explosion is not one colour multiplied, it is a fire
    gradient, and desaturating it to make it tintable destroys the thing being evaluated.

    So the guard INVERTS here. The measurement still runs — every sheet's mean saturation is
    reported — but the entry declares what it intends (`tint: "none"` for baked art it will never
    recolour, `tint: "lane"` for neutral art it will), and `check` fails an entry whose art does
    not match its declaration. Baked art is allowed; baked art *claiming* to be tintable is not.
    """
    out: dict[str, dict] = {}
    lab = tokens.get("lab") or {}
    for key, entry in lab.items():
        if key.startswith("_") or not isinstance(entry, dict):
            continue
        name = entry.get("sheet")
        if not name or name in out:
            continue
        path = VFX_DIR / f"{name}.png"
        if not path.exists():
            _die(f"lab entry {key!r} names sheet {name!r}, not found at "
                 f"{path.relative_to(ROOT)} — generate it with wowkb.vfxsheet or wowkb.sparkler")
        img = Image.open(path).convert("RGBA")
        measure = uiart.tintability(img)
        uri, nbytes = _data_uri(img, tokens)
        out[name] = {"uri": uri, "bytes": nbytes, "w": img.size[0], "h": img.size[1],
                     "mean_saturation": measure["mean_saturation"],
                     "tintable": measure["tintable"]}
    return out


FONTS_DIR = MEDIA_DIR / "fonts"


def export_style_font(tokens: dict) -> list[str]:
    """Ship V15's font into the addon, with the licence it travels under.

    This is the ONE piece of third-party art cap redistributes, and the rules that let it are not
    the same rules that govern the preview. The preview may embed anything it can measure, because
    it redistributes nothing; `Media/fonts/` goes out to every player, so what lands here must be
    ours to give away. `tokens.preview.hotkey_font.license` is where that is asserted and
    `shippable` is what turns it on.
    """
    spec = (tokens.get("preview") or {}).get("hotkey_font") or {}
    written: list[str] = []
    FONTS_DIR.mkdir(parents=True, exist_ok=True)
    if not spec.get("shippable"):
        # A client font (`Fonts\\ARIALN.TTF`) needs no file and must never get one.
        for stale in sorted(FONTS_DIR.glob("*")):
            stale.unlink()
        return written
    name = spec.get("ship_as") or spec["family"]
    data = _subset_font(_font_source(spec), "tokens.preview.hotkey_font", spec.get("ship_as"))
    (FONTS_DIR / f"{name}.ttf").write_bytes(data)
    written.append(f"{name}.ttf")
    # ⚠ The licence is not optional cargo. OFL 1.1 requires it to travel with every copy, and
    # clause 3 is why the file above is RENAMED — see `_rename_font`.
    if spec.get("license_url"):
        (FONTS_DIR / "OFL.txt").write_bytes(_font_text(spec["license_url"]))
        written.append("OFL.txt")
    (FONTS_DIR / "NOTICE.txt").write_text(FONT_NOTICE.format(
        ship_as=name, family=spec["family"], rfn=spec.get("rfn", "—"),
        license=spec.get("license", "—"), url=spec.get("url", "—")), encoding="utf-8")
    written.append("NOTICE.txt")
    return written


def export_lab(tokens: dict) -> list[tuple[str, tuple[int, int]]]:
    """Ship the lab's generated art into the addon as 32-bit TGA, under its own directory.

    `Media/lab/` rather than a naming convention inside `Media/badges/`, so "this is lab art" is
    legible from `ls`. The tint guard runs on the ship path exactly as `export_badges` runs it: the
    sheet measures 0.000 by construction, and the point of asserting it anyway is that a future
    edit which bakes a colour into the generator fails here instead of shipping a lie.
    """
    written: list[tuple[str, tuple[int, int]]] = []
    fonts_written: list[tuple[str, int]] = []
    src = ROOT / "projects" / "combat-assist" / tokens["badges"]["asset_root"]
    tint = tokens["badges"].get("tint", "none")
    LAB_DIR.mkdir(parents=True, exist_ok=True)
    for name in sorted({e.get("sheet") for e in (tokens.get("lab") or {}).values()
                        if isinstance(e, dict) and e.get("sheet")}):
        path = VFX_DIR / f"{name}.png"
        if not path.exists():
            _die(f"lab sheet {name!r} not found at {path.relative_to(ROOT)}")
        img = Image.open(path).convert("RGBA")
        # No tint assertion: a VFX sheet is allowed a baked hue (see `vfx_assets`). What is
        # asserted is that its declaration matches, and `check` owns that.
        written.append((name, _write_tga(img, name, LAB_DIR)))
    for frame in LAB_SPRITES:
        path = src / f"{frame}.png"
        if not path.exists():
            _die(f"lab sprite {frame!r} not found at {path.relative_to(ROOT)}")
        img = Image.open(path).convert("RGBA")
        measure = uiart.tintability(img)
        assert_tintable(f"lab sprite {frame!r}", str(path.relative_to(ROOT)),
                        tint, measure["mean_saturation"], measure["tintable"])
        if img.size[0] > SPRITE_PX:
            img = img.resize((SPRITE_PX, SPRITE_PX), Image.LANCZOS)
        written.append((frame, _write_tga(img, frame, LAB_DIR)))
    # Part 7's SHIPPABLE fonts. A font candidate can only be judged where the client draws it
    # (WoW rasterises a TTF into a signed-distance-field slug, which a browser does not do), and
    # the gallery cannot draw a face the install does not have. Blizzard's own candidates need no
    # file — `Fonts\\ARIALN.TTF` is already there — so only the ones we would actually ship get
    # written, subset to the keybind alphabet exactly as the preview embeds them.
    for key, entry in sorted((tokens.get("lab") or {}).items()):
        if key.startswith("_") or not isinstance(entry, dict):
            continue
        spec = entry.get("font") or {}
        if entry.get("draws") != "hotkey" or not spec.get("shippable"):
            continue
        data = _subset_font(_font_source(spec), f"lab.{key}")
        out = LAB_DIR / f"{spec['family']}.ttf"
        out.write_bytes(data)
        fonts_written.append((f"{spec['family']}.ttf", len(data)))

    # PRUNE art the lab no longer owns. Promotion MOVES a file — `fire` went to `Media/badges/`
    # when `priority` took it as a glyph, and `procring` to `Media/` when V14 shipped — and a
    # promoted texture left behind here is the second copy the whole rule exists to prevent. It
    # would also keep drawing: the gallery reads by name, so a stale file silently wins.
    keep = {name for name, _ in written}
    for stale in sorted(LAB_DIR.glob("*.tga")):
        if stale.stem not in keep:
            stale.unlink()
            print(f"  pruned {stale.name:<21} no longer lab art (promoted, or its entry is gone)")
    # A shipped font is not `.tga` and the prune above cannot see it; prune it the same way.
    keep_fonts = {name for name, _ in fonts_written}
    for stale in sorted(LAB_DIR.glob("*.ttf")):
        if stale.name not in keep_fonts:
            stale.unlink()
            print(f"  pruned {stale.name:<21} no longer a lab font candidate")
    for name, size in fonts_written:
        print(f"  {name:<24} {size / 1024:>6.1f} KB subset → {LAB_DIR.relative_to(ROOT)}")
    if written or fonts_written:
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


#: `SetBlendMode` → the CSS compositing operator that reproduces it. Only the two the shelf
#: actually uses are here: an unlisted mode is a KeyError rather than a silently wrong preview.
CSS_BLEND = {"BLEND": "normal", "ADD": "plus-lighter"}


def root_css(tokens: dict) -> str:
    s = tokens["surfaces"]
    b = tokens["badges"]

    def rgba(col, alpha=1.0):
        r, g, b_ = (round(x * 255) for x in col)
        return f"rgba({r},{g},{b_},{alpha})"

    d = b["diameter_pct"] / 100 * s["icon_px"]
    rd = tokens["ready"]
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
        "  /* V13 · in the scan. One hue, no roles, no motion: an icon either participates in",
        "     the read or it does not. Full brightness on a restrained AREA, drawn ON the rect,",
        "     so no row gap can be too small. The blend mode is a token because ADD could not",
        "     carry the hue: see the shelf's V13 ruling. */",
        f"  --ready-rgb: {','.join(str(round(x * 255)) for x in rd['rgb'])};",
        f"  --ready-alpha: {rd['alpha']:.2f};",
        f"  --ready-line: {rd['line_px']}px;",
        f"  --ready-blend: {CSS_BLEND[rd['blend']]};",
    ]

    # The first badge hangs off the top-right corner: its right edge sits `overhang` past the
    # icon's right edge and its top edge `overhang` above the top, so it reads as ON the icon
    # rather than inside it. Every further badge steps one diameter+padding DOWN the right edge.
    # The stack is unbounded, so the page computes each offset from its index rather than
    # matching a fixed slot rule (V5, 2026-08-19).
    lines += [
        "",
        "  /* V5 · corner badges, flowing DOWN. The first overhangs the top-right corner by",
        "     --badge-over; each further badge steps --badge-step down the right edge. */",
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
        # V11's SECOND cause: cap's own "ruled out", in its own red at its own phase, so a row
        # that is somehow both does not moiré into a flat wash.
        skip = sheet.get("skip")
        if skip:
            lines += [
                f"  --hatch-skip-rgb: {rgba(skip['rgb'], skip.get('alpha', 1.0))};",
                f"  --hatch-skip-phase: "
                f"{sheet['pitch_px'] * skip.get('phase_pct', 0) / 100:.2f}px;",
                f"  --hatch-skip-over: {skip.get('overhang_px', 0)}px;",
            ]
            border = skip.get("border")
            if border:
                lines += [
                    f"  --hatch-skip-line: {border['line_px']}px;",
                    f"  --hatch-skip-edge: {rgba(border['rgb'], border.get('alpha', 1.0))};",
                ]
    # V15 · the hotkey hint. `root_css` is hand-written per token group rather than a generic
    # flattener, so a new token group needs a line here or `strict_css` fails the stylesheet that
    # tried to name the value directly. Chrome: no tint, no rank, nothing per-cue.
    hk = tokens.get("hotkey")
    if hk:
        lines += [
            "",
            "  /* V15 · hotkey text — chrome. Names the row; asserts nothing about the press. */",
            f"  --hotkey-size: {hk['size']}px;",
            f"  --hotkey-color: {rgba(hk['rgb'], hk['alpha'])};",
            f"  --hotkey-x: {hk['offset']['x']}px;",
            f"  --hotkey-y: {-hk['offset']['y']}px;",
            # The client's `OUTLINE` flag draws black and cap does not choose that; the preview
            # has to emulate it with four offset shadows, so the colour lives in `preview` —
            # excluded from Style.lua, because the addon has nothing to do with it.
            f"  --hotkey-outline: "
            f"{rgba((tokens.get('preview') or {}).get('hotkey_outline_rgb', [0, 0, 0]))};",
            # ⚠ The client's font is a FILE (`tokens.hotkey.font`) and the browser cannot have
            # it — Part 3 forbids shipping Blizzard art, so the preview names the closest family
            # it can and the shelf owns that choice too. This is the largest remaining fidelity
            # gap in V15's preview and the flight is what closes it.
            f"  --hotkey-font: "
            f"{(tokens.get('preview') or {}).get('hotkey_font_stack', 'inherit')};",
            # The client's `OUTLINE` / `THICKOUTLINE` flag, emulated as an offset ring. The width
            # is the SHELF's, not this file's, and it is a two-value vocabulary on purpose: the
            # preview must not be able to draw a dark edge `SetFont` cannot ask for.
            f"  --hotkey-outline-px: "
            f"{(tokens.get('preview') or {}).get('hotkey_outline_px', 1)}px;",
        ]

    # PREVIEW-ONLY chrome, and both live under `tokens.preview` for the same reason the hotkey
    # outline colour does: `NOT_THE_STYLE` excludes that key from `Style.lua`, so neither of these
    # can reach the addon. The virtual tick compensates for a geometry the PREVIEW loses (V12's
    # panel is a separate surface in the client and one flat row here); the unsure block is a note
    # to the author about the doc, not a mark on a button.
    prev = tokens.get("preview") or {}
    vm = prev.get("virtual_mark")
    if vm:
        lines += [
            "",
            "  /* V12 · virtual-row tick — PREVIEW ONLY. Says 'cap owns this frame; the",
            "     Cooldown Manager has no row for it', which the client says by geometry. */",
            f"  --virtual-rgb: {rgba(vm['rgb'])};",
            f"  --virtual-size: {vm['size_px']}px;",
            f"  --virtual-line: {vm['line_px']}px;",
            # It HANGS OFF the corner, the way a badge overhangs the top-right, because the scan
            # edge already owns the rim: a tick drawn inside the rect competes with a 2px gold
            # line on exactly the pixels it needs, and on bright art it loses.
            f"  --virtual-out: {vm['overhang_px']}px;",
        ]
    uns = prev.get("unsure")
    if uns:
        lines += [
            "",
            "  /* ⚠ UNSURE annotation — PREVIEW ONLY. Loud on purpose: it marks a claim the",
            "     authoring docs themselves doubt, and it must not read as a footnote. */",
            f"  --unsure-rgb: {rgba(uns['rgb'])};",
            f"  --unsure-bg: {rgba(uns['bg_rgb'], uns.get('bg_alpha', 1.0))};",
            f"  --unsure-line: {uns['line_px']}px;",
        ]

    promo = tokens.get("promotion")
    if promo:
        lines += [
            "",
            "  /* V14 · promotion ring */",
            f"  --promo-rgb: {','.join(str(round(x * 255)) for x in promo['rgb'])};",
            f"  --promo-alpha: {promo.get('alpha', 1.0):.2f};",
            f"  --promo-spread: {promo['spread']:.2f};",
            f"  --promo-cols: {promo['cols']};",
            f"  --promo-rows: {promo['rows']};",
        ]
    # V16/V17 · the banded count. The per-band HUE deliberately does not appear as one variable:
    # in the client it lives inside the band's own `format` string (`|cffRRGGBB…|r`), because the
    # count sink adds `Text` and `Shown` and never `VertexColor`, so there is nowhere else to put
    # it. What is emitted is the TYPE plus the two polarity hues the bands are written from.
    cnt = tokens.get("count")
    if cnt:
        lines += [
            "",
            "  /* V16/V17 · banded count — a sealed number as a numeral, a mark, or both */",
            f"  --count-size: {cnt['size']}px;",
            f"  --count-outline: 1px;",
            f"  --count-rgb: {rgba(cnt['rgb'])};",
            f"  --count-low: {rgba(cnt['low_rgb'])};",
            f"  --count-mark: {cnt['mark_px']}px;",
            f"  --count-mark-x: {cnt['mark_offset_px'][0]}px;",
            f"  --count-mark-y: {cnt['mark_offset_px'][1]}px;",
            f"  --count-plate: {cnt['plate_px']}px;",
            f"  --count-hatch: {cnt['hatch_px']}px;",
            f"  --count-hatch-alpha: {cnt.get('hatch_alpha', 1.0)};",
            f"  --count-pulse-dur: {cnt['pulse']['duration_s']}s;",
            f"  --count-pulse-a0: {cnt['pulse']['alpha'][0]};",
            f"  --count-pulse-a1: {cnt['pulse']['alpha'][1]};",
            f"  --count-pulse-scale: {cnt['pulse']['scale']};",
        ]
    # V18 · the sealed radial. A bar has a TRACK as well as a fill, and the track is the half that
    # decides whether an empty one reads as "nothing yet" or as clutter — which is the whole cost
    # of a primitive that has no blank state.
    arc = tokens.get("arc")
    if arc:
        lines += [
            "",
            "  /* V18 · sealed radial — the same secret as a shape */",
            f"  --arc-inset: {arc['inset_px']}px;",
            f"  --arc-rgb: {rgba(arc['rgb'], arc.get('alpha', 1.0))};",
            f"  --arc-track: {rgba(arc['track_rgb'], arc.get('track_alpha', 1.0))};",
            f"  --arc-full: {rgba(arc['full_rgb'])};",
        ]
    # V19 · the pandemic window. Every number here is cap's; the one thing that is not is the only
    # thing that matters — whether the region is shown, which the client owns outright.
    pd = tokens.get("pandemic")
    if pd:
        lines += [
            "",
            "  /* V19 · pandemic window — a badge the client alone shows and hides */",
            f"  --pd-rgb: {rgba(pd['rgb'])};",
            f"  --pd-size: {pd['size_px']}px;",
            f"  --pd-pulse-dur: {pd['pulse']['duration_s']}s;",
            f"  --pd-pulse-a0: {pd['pulse']['alpha'][0]};",
            f"  --pd-pulse-a1: {pd['pulse']['alpha'][1]};",
        ]
    lab = tokens.get("lab") or {}
    if sheet:
        for key, entry in lab.items():
            if key.startswith("_") or not isinstance(entry, dict) or "rgb" not in entry:
                continue
            if entry.get("draws") != "stripes":
                continue   # a phase is meaningless without the sheet, and the rgba() form
                           # would be overwritten by the bare triple emitted below anyway
            phase = sheet["pitch_px"] * entry.get("phase_pct", 0) / 100
            lines.append(f"  --lab-{key}-rgb: {rgba(entry['rgb'], entry.get('alpha', 1.0))};")
            lines.append(f"  --lab-{key}-phase: {phase:.2f}px;")
    # Part 7 · the readiness entries. They share no asset with each other and none with the
    # style, so each emits only the variables its own render reads. `glow_px` is an OUTSET: the
    # halo is drawn outside the icon rect, which is the whole point of the treatment.
    for key, entry in lab.items():
        if key.startswith("_") or not isinstance(entry, dict) or "rest_alpha" not in entry:
            continue
        pre = f"  --lab-{key}-"
        lines.append("")
        lines.append(f"  /* Part 7 · {key} */")
        # A bare `r,g,b` triple, not an `rgba(...)`: the renders compose it with their own
        # alpha (`rgba(var(--…-rgb), var(--…-rest))`), which CSS cannot do to a finished color.
        lines.append(f"{pre}rgb: {','.join(str(round(x * 255)) for x in entry['rgb'])};")
        lines.append(f"{pre}rest: {entry['rest_alpha']:.2f};")
        lines.append(f"{pre}flare: {entry.get('flare_alpha', entry['rest_alpha']):.2f};")
        if "glow_px" in entry:
            lines.append(f"{pre}glow: {entry['glow_px']}px;")
        if "flare_mult" in entry:
            lines.append(f"{pre}flare-glow: {entry['glow_px'] * entry['flare_mult']:.1f}px;")
        if "line_px" in entry:
            lines.append(f"{pre}line: {entry['line_px']}px;")
        # A breathing entry that ALSO flares needs two tops: the cycle's peak and the one-shot's
        # overshoot. Without `peak_alpha` the cycle simply reaches `flare_alpha`, as before.
        if "peak_alpha" in entry:
            lines.append(f"{pre}peak: {entry['peak_alpha']:.2f};")
        for k, css in (("decay_s", "decay"), ("period_s", "period")):
            if k in entry:
                lines.append(f"{pre}{css}: {entry[k]:.2f}s;")
        # Part 7 · blaze. `spread` is a SCALE rather than a pixel outset: the field is a scaled
        # copy of the glyph's own mask (or of the plate's disc), so it has to grow proportionally
        # or the light stops fitting the shape it is supposed to be coming from.
        if "spread" in entry:
            lines.append(f"{pre}spread: {entry['spread']:.2f};")
        # The glyph's own hue, separate from the light's. They cannot be the same value: a
        # sprite tinted with the colour blazing behind it disappears into it.
        if "glyph_rgb" in entry:
            lines.append(f"{pre}glyph: "
                         f"{','.join(str(round(x * 255)) for x in entry['glyph_rgb'])};")
    # Part 7 · the flipbook entries (icon-scale VFX). They carry no `rest_alpha`, so they miss
    # the readiness loop above and emit their own. `scale` is a multiple of the ICON, not of a
    # badge: these surround the button the way Blizzard's proc glow does.
    for key, entry in lab.items():
        if key.startswith("_") or not isinstance(entry, dict):
            continue
        if entry.get("draws") != "flipbook":
            continue
        pre = f"  --lab-{key}-"
        lines.append("")
        lines.append(f"  /* Part 7 · {key} — {entry['frames']} frames @ {entry['fps']}fps */")
        lines.append(f"{pre}scale: {entry.get('scale', 1.0):.2f};")
        lines.append(f"{pre}dur: {entry['frames'] / entry['fps']:.3f}s;"
                     if entry.get("fps") else f"{pre}dur: 0s;")
        lines.append(f"{pre}cols: {entry['cols']};")
        lines.append(f"{pre}rows: {entry['rows']};")
        if "period_s" in entry:
            lines.append(f"{pre}period: {entry['period_s']:.2f}s;")
        if "rgb" in entry:
            lines.append(f"{pre}rgb: "
                         f"{','.join(str(round(x * 255)) for x in entry['rgb'])};")
    # Part 7 · the count entries — a secret aura APPLICATION COUNT reaching a pixel. Two shapes
    # and they are genuinely different mechanisms, so they emit different variables:
    #   `count`     — the NumericRuleFormatter's banded string, drawn as text. Per-band hue lives
    #                 inside the band's own `format` (`|cffRRGGBB…|r`), which is where the client
    #                 reads it from too, so the renderer resolves it per cell rather than from a
    #                 variable here. What IS emitted is the type: size, outline, and the static
    #                 hue that needs no markup at all.
    #   `count-bar` — SetApplicationBar's fill, drawn as art. A bar has a track as well as a
    #                 fill, and the track is the half that decides whether an empty one reads as
    #                 "nothing yet" or as clutter.
    for key, entry in lab.items():
        if key.startswith("_") or not isinstance(entry, dict):
            continue
        if entry.get("draws") == "count":
            pre = f"  --lab-{key}-cn-"
            lines += [
                "",
                f"  /* Part 7 · {key} — banded count text */",
                f"{pre}size: {entry['size_px']}px;",
                f"{pre}outline: {entry['outline_px']}px;",
                f"{pre}rgb: {rgba(entry['rgb'])};",
            ]
        elif entry.get("draws") == "count-bar":
            pre = f"  --lab-{key}-cb-"
            lines += [
                "",
                f"  /* Part 7 · {key} — count-driven fill */",
                f"{pre}h: {entry['height_px']}px;",
                f"{pre}rgb: {rgba(entry['rgb'])};",
                f"{pre}track: {rgba(entry['track_rgb'], entry.get('track_alpha', 1.0))};",
                f"{pre}ring: {entry.get('ring_px', 3)}px;",
            ]
        elif entry.get("draws") in ("count-glyph", "duration"):
            # A band whose `format` carries a texture escape. The MARK is the drawn thing, so
            # the entry declares its size and its hue; the plate, when a cell asks for one, is
            # the badge stack's own and is deliberately not re-declared here.
            pre = f"  --lab-{key}-cg-"
            lines += [
                "",
                f"  /* Part 7 · {key} — a banded texture escape */",
                f"{pre}size: {entry['size_px']}px;",
                f"{pre}rgb: {rgba(entry['rgb'])};",
                f"{pre}alt: {rgba(entry['alt_rgb'])};",
                f"{pre}pulse-dur: {entry['pulse']['duration_s']}s;",
                f"{pre}pulse-a0: {entry['pulse']['alpha'][0]};",
                f"{pre}pulse-a1: {entry['pulse']['alpha'][1]};",
                f"{pre}pulse-scale: {entry['pulse']['scale']};",
            ]
        elif entry.get("draws") == "composite":
            # A composite cell stacks several sinks on one row, so its palette is named rather
            # than positional: a layer says `green`, and which green is the entry's business.
            pre = f"  --lab-{key}-cx-"
            lines += ["", f"  /* Part 7 · {key} — several sinks on one row */"]
            for hue, val in entry["hues"].items():
                lines.append(f"{pre}{hue}: {rgba(val)};")
            lines += [
                f"{pre}arc-track: {rgba(entry['arc_track_rgb'], entry['arc_track_alpha'])};",
                f"{pre}arc-inset: {entry['arc_inset_px']}px;",
                f"{pre}size: {entry['size_px']}px;",
                f"{pre}pulse-dur: {entry['pulse']['duration_s']}s;",
                f"{pre}pulse-a0: {entry['pulse']['alpha'][0]};",
                f"{pre}pulse-a1: {entry['pulse']['alpha'][1]};",
                f"{pre}pulse-scale: {entry['pulse']['scale']};",
            ]
        elif entry.get("draws") == "pandemic":
            # The client owns Shown; every number here is the addon's. `alpha` is the wash's,
            # which is the one treatment that covers icon art rather than sitting beside it.
            pre = f"  --lab-{key}-pd-"
            lines += [
                "",
                f"  /* Part 7 · {key} — art gated by Blizzard's pandemic window */",
                f"{pre}rgb: {rgba(entry['rgb'])};",
                f"{pre}wash: {rgba(entry['rgb'], entry['wash_alpha'])};",
                f"{pre}edge: {entry['edge_px']}px;",
                f"{pre}foot: {entry['foot_px']}px;",
                f"{pre}size: {entry['size_px']}px;",
                f"{pre}pulse-dur: {entry['pulse']['duration_s']}s;",
                f"{pre}pulse-a0: {entry['pulse']['alpha'][0]};",
                f"{pre}pulse-a1: {entry['pulse']['alpha'][1]};",
            ]

    # Part 7 · the font candidates. Each hotkey entry names its own family and its own two
    # dials, so the entries can be read side by side at the same size or at different ones.
    for key, entry in (tokens.get("lab") or {}).items():
        if key.startswith("_") or not isinstance(entry, dict):
            continue
        if entry.get("draws") != "hotkey":
            continue
        pre = f"  --lab-{key}-hk-"
        lines += [
            "",
            f"  /* Part 7 · {key} */",
            f"{pre}font: '{entry['font']['family']}', var(--hotkey-font);",
            f"{pre}size: {entry['size_px']}px;",
            f"{pre}outline: {entry['outline_px']}px;",
        ]
        # The plate, where an entry has one. A candidate without one emits nothing and the
        # stylesheet's own transparent/0 defaults stand, so `background` and `padding` do not
        # have to be conditional in CSS.
        # The title bar. Emitted as ONE `background` value so the flat and the faded variant
        # differ in the token block and nowhere else — CSS takes a gradient wherever it takes a
        # colour, and the client takes `SetGradient` wherever it takes `SetColorTexture`.
        bar = entry.get("bar")
        if bar:
            top = rgba(bar["rgb"], bar.get("alpha", 1.0))
            fill = (f"linear-gradient(to bottom, {top}, {rgba(bar['rgb'], 0.0)})"
                    if bar.get("fade") else top)
            lines += [
                f"{pre}bar: {fill};",
                f"{pre}bar-h: {bar['height_px']}px;",
                f"{pre}bar-align: {'center' if bar.get('align') == 'center' else 'flex-start'};",
            ]
            rule = bar.get("rule")
            lines.append(f"{pre}bar-rule: {rule['px']}px solid {rgba(rule['rgb'], rule['alpha'])};"
                         if rule else f"{pre}bar-rule: 0 solid transparent;")

        plate = entry.get("plate")
        if plate:
            lines += [
                f"{pre}plate: {rgba(plate['rgb'], plate.get('alpha', 1.0))};",
                f"{pre}plate-x: {plate.get('pad_x_px', 0)}px;",
                f"{pre}plate-y: {plate.get('pad_y_px', 0)}px;",
            ]
    lines.append("}")

    # V15's real font, straight out of CASC. Emitted AFTER `:root` because an `@font-face` is a
    # top-level rule and cannot live inside one. The preview is the only consumer; see
    # `hotkey_font_asset` for why embedding it is Part 3-legal.
    font = hotkey_font_asset(tokens)
    if font:
        lines += [
            "",
            f"/* V15 · the SHIPPED font, {font['origin']} — the same subset file the addon "
            "carries, so the preview measures exactly the advance widths the game does. */",
            "@font-face {",
            f"  font-family: '{font['family']}';",
            f"  src: url({font['uri']}) format('truetype');",
            "  font-display: block;",
            "}",
        ]
    # Part 7's candidates, same mechanism. Subset to the keybind alphabet, so three extra
    # families cost a few KB rather than a few hundred.
    #
    # Deduped BY FAMILY: the control entry deliberately names the same face the style does, and
    # two `@font-face` rules for one family is both dead weight and a question about which wins.
    seen_families = {font["family"]} if font else set()
    for key, asset in lab_font_assets(tokens).items():
        if asset["family"] in seen_families:
            continue
        seen_families.add(asset["family"])
        lines += [
            "",
            f"/* Part 7 · {key} — {asset['family']}, {asset['source_bytes'] / 1024:.0f} KB "
            f"subset to {asset['subset_bytes'] / 1024:.1f} KB. {asset['origin']} */",
            "@font-face {",
            f"  font-family: '{asset['family']}';",
            f"  src: url({asset['uri']}) format('truetype');",
            "  font-display: block;",
            "}",
        ]
    return "\n".join(lines)


JS_CLASS_RE = re.compile(r'\bel\(\s*"[a-z]+"\s*,\s*"([a-z0-9][a-z0-9 -]*)"\)')
JS_QUERY_RE = re.compile(r'querySelector(?:All)?\(\s*"(?:[^"]*?)\.([a-z0-9-]+)[^"]*"\)')


def smoke_dom(js: Path, css: Path, root: str) -> list[str]:
    """Every class name stepper.js builds or looks up must exist in the stylesheet.

    ⚠ This gate exists because `check` never renders the page and therefore never noticed that
    the lab's `inner_border: false` was stripping `.edge`, **a class the DOM stopped carrying**
    when the lane border retired — so all four readiness entries were judged with a stray scan
    line composited over them and every gate stayed green. A class the JS names and the CSS does
    not is either dead code or an invisible element; neither is something a look-at-it preview
    can afford to hold silently.
    """
    text = js.read_text(encoding="utf-8")
    sheet = css.read_text(encoding="utf-8") + root
    # An id counts: a node given `el("div", "tip")` and then `.id = "tip"` is styled as `#tip`.
    styled = set(re.findall(r"[.#]([a-z0-9-]+)", sheet))
    bad = []
    built = {c for m in JS_CLASS_RE.findall(text) for c in m.split()}
    for name in sorted(built | set(JS_QUERY_RE.findall(text))):
        if name not in styled:
            bad.append(f"{js.name}: class {name!r} is built or queried but no rule in "
                       f"{css.name} names it — a dead lookup, or an element nobody can see.")
    return bad


SEALED_KIND_RE = re.compile(r'kind\s*===\s*"([a-z-]+)"')
GALLERY_SEALED_RE = re.compile(r'sealed:\s*\[([^\]]*)\]')


def gallery_covers_sealed(js: Path) -> list[str]:
    """Every sealed display `sealedNode` can draw must have a swatch in the primitives gallery.

    ⚠ This is the ONE gate the preview's own seam earned, and it is deliberately narrow. The
    defect it is written against (2026-08-23) is that all four sealed displays were reachable
    ONLY from inside a scenario row — and V16, the count band in its ordinary non-eliminating
    direction, is drawn by no scenario in any catalog at all. So the gallery section, whose own
    copy promises "every primitive the shelf declares, INCLUDING the ones no scenario above
    exercises", quietly did not, and a shelf edit to those tokens landed nowhere anyone looks.

    ⚠ It is NOT a rendering gate, and no rendering gate belongs here. The sibling defect found
    the same day — `.sealed-run` computing to 22x22 because `inset` does not override an
    inherited `width` — is invisible to any static check: the class existed, the rule existed,
    the rule was simply wrong. Catching that means running a browser inside `check`, which is a
    large dependency for a tool whose job is to assemble a page. That measurement stays MANUAL.

    ⚠ Scoped to the sealed kinds and not to "every art-bearing token group", which was the wider
    rule considered first. `tokens.ring` and `tokens.promotion` also carry art and are correctly
    absent from the gallery — ring is retired, promotion is drawn from Part 7 — so the wider gate
    would fail on two primitives that are right, which is worse than not having it.
    """
    text = js.read_text(encoding="utf-8")
    # Scoped to sealedNode's OWN body: `kind === "row"` and `kind === "sheet"` live in the Part 7
    # lab further down the file and are not sealed displays. A gate reporting those as missing
    # swatches would be crying wolf on the two cases it is least qualified to judge.
    fn = text.find("function sealedNode(")
    nxt = text.find("\n  function ", fn + 1)
    if fn < 0:
        return [f"{js.name}: cannot find sealedNode — this gate has lost its subject."]
    kinds = set(SEALED_KIND_RE.findall(text[fn:nxt if nxt > fn else len(text)]))
    # The fall-through: `sealedNode` returns the count-band run when no branch matched, so that
    # kind is named in the sidecar and never in a `kind ===` comparison.
    kinds.add("count-bands")

    start = text.find('var gallery = host("gallery")')
    end = text.find('var framesHost = host("frames")')
    if start < 0 or end < 0 or end < start:
        return [f"{js.name}: cannot find the gallery section — this gate has lost its subject."]
    drawn = {k.strip().strip('"\'')
             for m in GALLERY_SEALED_RE.findall(text[start:end])
             for k in m.split(",") if k.strip()}

    return [f"{js.name}: the sealed display {k!r} is drawn by sealedNode but no gallery swatch "
            f"builds it — the section promises every primitive the shelf declares, and a "
            f"primitive only a scenario reaches is one a shelf edit changes invisibly."
            for k in sorted(kinds - drawn)]


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
    #
    # ⚠ They resolve against the SHELF's reference roster, not this spec's. Part 7 is one gallery
    # belonging to `render-shelf.md`, drawn on whatever page you happen to be looking at; its
    # cells are authored once and are not a claim about any spec's rotation. Holding them to the
    # roster of the spec being built would mean re-authoring the lab per spec, which would make
    # every experiment a spec decision — the opposite of what Part 7 is for.
    lab_roster = roster if spec == SHELF_ROSTER_SPEC else load_roster(
        SPECS_BUILT[SHELF_ROSTER_SPEC]["catalog"])
    lab_icon_roster = dict(lab_roster)
    lab_names = set()
    for key, entry in ((k, e) for k, e in (tokens.get("lab") or {}).items()
                       if not k.startswith("_")):
        for cell in entry.get("cells", []):
            # A `row` cell draws several icons at the true row pitch; every name in it needs an
            # icon fetched exactly as a single-ability cell's does.
            for name in cell.get("abilities", []):
                if name not in lab_roster:
                    _die(f"lab.{key}: {name!r} is not in "
                         f"{SPECS_BUILT[SHELF_ROSTER_SPEC]['catalog'].relative_to(ROOT)}'s "
                         "bound-abilities table (Part 7 draws from the shelf's reference roster)")
                lab_names.add(name)
            name = cell.get("ability")
            if name is None:
                continue
            if name not in lab_roster:
                _die(f"lab.{key}: {name!r} is not in "
                     f"{SPECS_BUILT[SHELF_ROSTER_SPEC]['catalog'].relative_to(ROOT)}'s "
                     "bound-abilities table (Part 7 draws from the shelf's reference roster)")
            if cell.get("verdict") and cell["verdict"] not in tokens["verdicts"]:
                _die(f"lab.{key}: verdict {cell['verdict']!r} is not in the closed vocabulary")
            lab_names.add(name)

    used = sorted({e["name"] for sc in scenarios for e in sc["row"]}
                  | set(cfg["scan_samples"]) | lab_names)
    missing = [n for n in cfg["scan_samples"] if n not in roster]
    if missing:
        _die(f"scan sample {missing} not in the roster")
    # The spec's own roster wins on any name both carry; the shelf roster only fills in the lab.
    lab_icon_roster.update(roster)
    icons = icon_assets(used, lab_icon_roster, tokens)
    frames = badge_assets(tokens)
    stripes = hatch_asset(tokens)
    ring = ring_asset(tokens)

    # The base64 budget is a fact to report, not a gate: an oversized page is still a page
    # you can look at, and `wowkb.capart assets` prints the per-asset table that fixes it.
    # The ring sheet is deliberately NOT in this sum and not in `data`: nothing in the preview
    # renders it since V2 retired, and embedding a 4 KB data URI no CSS names is dead weight the
    # budget would then report as spent. It still ships to the addon and is still measured under
    # the tint guard on `ring_asset`'s path — only the injection stopped.
    total = (sum(a["bytes"] for a in icons.values()) + sum(f["bytes"] for f in frames.values())
             + (stripes["bytes"] if stripes else 0))

    # V15 · SIMULATED keybinds, so the corner can be judged before the feature reaches the game.
    #
    # ⚠ These are fakes and they live in `tokens.preview`, which `NOT_THE_STYLE` excludes from
    # `Style.lua` — a fake key is structurally incapable of reaching the addon. They are NOT in
    # any catalog or sidecar either: a keyboard layout in a gameplay authority document would
    # contradict the chrome ruling, and a `{hotkey: …}` row group would make the fake look
    # authored.
    #
    # Assignment is by ROSTER POSITION and therefore deterministic — gate 2 rebuilds the page and
    # byte-compares, so a random or date-seeded fake would make that gate permanently red. It also
    # means one ability wears the same fake in every scenario on the page, which is what makes the
    # eye able to learn it.
    fakes = (tokens.get("preview") or {}).get("hotkeys") or []
    at = {name: i for i, name in enumerate(lab_icon_roster)}

    abilities = {
        name: {"key": lab_icon_roster[name]["key"], "spell": lab_icon_roster[name]["spell"],
               "hotkey": (fakes[at[name] % len(fakes)] if fakes else ""),
               # The authored role lane still travels because the CATALOGS still record it —
               # it is a fact about the ability. It no longer picks a treatment: an icon either
               # is in the scan or is not, and rank comes from row order plus elimination.
               "lane": lab_icon_roster[name]["lane"],
               "charges": lab_icon_roster[name].get("charges", 0), "icon": icons[name]["uri"]}
        for name in used
    }

    # A spec may carry standing banners of its own — what the page is and is not evidence for.
    # They are page-level because they are true of every scenario on it; a caveat that is true of
    # ONE scenario belongs in that scenario's `⚠ UNSURE` extras bullet, where the row is.
    notes = list(cfg.get("notes") or [])
    open_frames = sorted(n for n, f in frames.items() if f["open"])
    if open_frames:
        notes.append(
            "Badge sprite(s) " + ", ".join(open_frames) + " are drawn through "
            "desaturate-then-tint, which is <b>unverified in client</b>. Whether desaturated "
            "baked-hue art takes a clean authored hue has not been measured, so treat these as a "
            "proposal, not a preview."
        )
    data = {
        "built": when,
        # Deliberately a sibling of `tokens`, never a member. The template reads it as
        # `D.client_paint` and the shelf's own `T.*` namespace cannot see it, which is the
        # mechanical form of "this layer is Blizzard's and cap does not own it".
        "client_paint": CLIENT_PAINT,
        "abilities": abilities,
        "scan_samples": cfg["scan_samples"],
        "scan_sample": cfg["scan_samples"][0],
        "scenarios": scenarios,
        "notes": notes,
        "frames": frames,
        # ⚠ `lab_stripes` is a LEGACY NAME, not a lab payload: it is V11's hatch sheet, which
        # the lab owned until L4 was promoted on 2026-08-16 and took it into `tokens.hatch`.
        # Same for `promotion`, which is V14's. Both are the style's and both stay.
        #
        # What left with the lab page are the genuinely lab-only assets — sprites, VFX sheets and
        # font candidates. A spec page carried all three for as long as the lab was appended to
        # it, which is most of why an experiment could add half a megabyte to every spec at once.
        "lab_stripes": stripes,
        "promotion": promotion_asset(tokens),
        "provenance_html": provenance_html(spec, tokens, icons, frames, stripes, ring, total,
                                           when),
    }

    page = (TEMPLATE / "page.html").read_text(encoding="utf-8")
    # The page is one template for every spec, so its own name has to arrive as data. It used to
    # hardcode "Havoc", which put the Retribution preview under Havoc's title in the tab strip.
    page = page.replace("<!--__SPEC_TITLE__-->", cfg.get("title", spec.title()))
    page = page.replace("<!--__SPEC__-->", spec)
    page = page.replace("<!--__SCENARIO_COUNT__-->", str(len(scenarios)))
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
    rows.append((
        "client baseline",
        "Blizzard's own icon paint, drawn <b>under</b> everything cap adds and read from source, "
        "not chosen: " + " · ".join(
            f"<code>{t['constant']}</code> {tuple(t['rgb'])}"
            for t in CLIENT_PAINT["tints"].values())
        + f" · plus desaturate-on-cooldown. {CLIENT_PAINT['_source']}; "
        f"claim at <code>{CLIENT_PAINT['_doc']}</code>. <b>These are not render tokens</b> — they "
        "are not in the shelf and an edit to the shelf cannot change them."))
    rd = tokens["ready"]
    rows.append((
        "in the scan · V2",
        f"one treatment, no roles, no motion — a {rd['line_px']}px {rd['blend']} edge at "
        f"alpha {rd['alpha']:.2f}, drawn ON the icon rect. The blend mode is declared because "
        "ADD clipped this hue to white on a bright icon; the restrained area is why full "
        "brightness is not loud. It has no falloff, so it cannot bleed into a neighbour at any "
        "row gap. Rank is "
        "carried by row order and elimination, not by hue."
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
            "ring sheet · Part 7 only",
            f"{ring['size'][0]}×{ring['size'][1]} generated by <code>capart.ring_flipbook</code> — "
            f"{ring['frames']} frames in a {ring['grid']}×{ring['grid']} grid of "
            f"{ring['tile_px']}px cells, band {ring['thickness_px']}px, travelling "
            f"{ring['travel_px']}px inward across the arrival · measured mean saturation "
            f"{ring['mean_saturation']}, so <code>SetVertexColor</code> takes it to the shelf's "
            f"colour · declared <code>tint: \"{ring['tint']}\"</code>, which is what puts it under "
            "the tint guard · shipped by <code>export ring</code> to <code>Media/</code> for Part "
            "7's <code>arrival-*</code> entries. <b>Not embedded in this page</b>: V2 retired and "
            "nothing here renders it."
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
    rd = tokens["ready"]
    r, g, b = (round(x * 255) for x in rd["rgb"])
    print("  V2 · the scan edge (ONE binary treatment: in the scan, or not)")
    print(f"    edge     rgb({r:>3},{g:>3},{b:>3}) · {rd['line_px']}px · alpha {rd['alpha']:.2f} · "
          f"{rd['blend']}, drawn ON the icon rect")
    print("    rank     row order plus elimination — there is no hue ladder and no motion")

    ring, a = tokens.get("ring"), tokens["arrival"]
    if ring:
        print(f"\n  Part 7 only · ring flipbook (no live subject; the lab still draws it)")
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

    print("\n  cues (negative BY DEFAULT — a cue draws when a button is RULED OUT. The positives "
          "do not\n        eliminate their own button, and rank above the negatives so they pack "
          "onto the corner)")
    for key, cue in tokens["cues"].items():
        pol = cue.get("polarity", "negative")
        print(f"    {key:<9} {'+' if pol == 'positive' else '-'} rank {cue['rank']} · "
              f"{len(cue['frames'])}f @{cue['duration_s']}s {cue['loop']:<7} {cue['means'][:48]}")

    t = tokens["text"]
    print()
    print(f"  text       max {t['max_hz']} Hz · duty {t['duty']} · alpha floor {t['alpha_floor']} "
          "(MIL-STD-1472F — safety, not taste)")

    outside = [k for k, v in tokens["verdicts"].items() if not v["scan"]]
    badged = [k for k, v in tokens["verdicts"].items() if v.get("cues")]
    print(f"\n  verdicts   {', '.join(tokens['verdicts'])}")
    print(f"    out of scan  {', '.join(outside)}")
    print(f"    badged       {', '.join(badged)}")
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
                  | set(cfg["scan_samples"]))
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
        print(f"{'ring flipbook':<40} {'lab':<6} {ring['bytes'] / 1024:>8.1f}  "
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
    print("\nThe scan edge (V13) needs no art at all — it is four colour strips. The ring "
          "flipbook above ships for Part 7's arrival experiments and nothing live draws it.")
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
            f"SEEDED by `wowkb.capart import scenarios {args.spec}` from "
            f"{cfg['scenarios'].relative_to(ROOT)}, then "
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


def _specs_of(args) -> list[str]:
    """Which specs a command runs over: the named one, or every built spec under `--all`.

    `--all` exists because the alternative is a hand-maintained list of spec names living
    somewhere other than `SPECS_BUILT` — in a `--on-change` string, in a CI line — and a list like
    that goes stale the moment a spec is added. The failure it causes is quiet in exactly the wrong
    way: a watcher told to rebuild only Havoc still fires on a Retribution edit, still rebuilds
    Havoc, still reports success, and still serves the stale Retribution page. `SPECS_BUILT` is the
    registry; this reads it rather than asking anyone to restate it.
    """
    if getattr(args, "all_specs", False):
        if args.spec:
            _die("pass a spec or --all, not both")
        return sorted(SPECS_BUILT)
    if not args.spec:
        _die(f"which spec? one of {', '.join(sorted(SPECS_BUILT))} — or --all for every one")
    return [args.spec]


INDEX_OUT = PREVIEWS / "index.html"
LAB_OUT = PREVIEWS / "lab.html"
PRIMITIVES_OUT = PREVIEWS / "primitives.html"


def build_lab(tokens: dict, when: str) -> str:
    """Part 7 as its own page.

    ⚠ IT IS NOT A SPEC AND MUST NOT BECOME ONE. Lab cells resolve against `SHELF_ROSTER_SPEC`'s
    roster and always did — Part 7 is one gallery belonging to `render-shelf.md`, and its cells
    are not a claim about any spec's rotation. It used to be appended to every spec page, which
    made that claim look spec-shaped and duplicated the larger half of the page into all of them.

    It ships no scenarios, and `stepper.js` renders the stepper only when there are some.
    """
    roster = load_roster(SPECS_BUILT[SHELF_ROSTER_SPEC]["catalog"])
    names = set()
    for key, entry in ((k, e) for k, e in (tokens.get("lab") or {}).items()
                       if not k.startswith("_")):
        for cell in entry.get("cells", []):
            names |= set(cell.get("abilities", []))
            if cell.get("ability"):
                names.add(cell["ability"])
    missing = sorted(n for n in names if n not in roster)
    if missing:
        _die(f"lab cells name {missing}, which are not in "
             f"{SPECS_BUILT[SHELF_ROSTER_SPEC]['catalog'].relative_to(ROOT)}'s bound-abilities "
             "table (Part 7 draws from the shelf's reference roster)")
    # An EMPTY lab embeds nothing. Every asset below exists to be drawn by an entry, so with no
    # entries they are half a megabyte of payload behind a page that says "the lab is empty" —
    # which is also the state the lab is supposed to spend most of its life in.
    used = sorted(names)
    icons = icon_assets(used, roster, tokens) if used else {}
    frames = badge_assets(tokens) if used else {}
    fakes = (tokens.get("preview") or {}).get("hotkeys") or []
    at = {name: i for i, name in enumerate(roster)}
    data = {
        "built": when,
        "client_paint": CLIENT_PAINT,
        "abilities": {
            name: {"key": roster[name]["key"], "spell": roster[name]["spell"],
                   "hotkey": (fakes[at[name] % len(fakes)] if fakes else ""),
                   "lane": roster[name]["lane"],
                   "charges": roster[name].get("charges", 0), "icon": icons[name]["uri"]}
            for name in used},
        # No scenarios and no scan samples: this page has no row to walk and no press to lead the
        # eye to. Both are the shelf's, and the shelf is not what the lab is asking about.
        "scenarios": [], "scan_samples": [], "notes": [],
        "frames": frames,
        "lab_stripes": hatch_asset(tokens) if used else None,
        "lab_sprites": lab_sprite_assets(tokens) if used else {},
        "lab_vfx": vfx_assets(tokens) if used else {},
        "lab_fonts": lab_font_assets(tokens),
        "promotion": promotion_asset(tokens) if used else None,
        "provenance_html": lab_provenance_html(tokens, icons, when),
    }
    page = (TEMPLATE / "lab.html").read_text(encoding="utf-8")
    page = page.replace("/*__ROOT_TOKENS__*/", root_css(tokens))
    page = page.replace("/*__SHELF_CSS__*/", (TEMPLATE / "shelf.css").read_text(encoding="utf-8"))
    page = page.replace("/*__STEPPER_JS__*/", (TEMPLATE / "stepper.js").read_text(encoding="utf-8"))
    page = page.replace("/*__TOKENS_JSON__*/", json.dumps(tokens, separators=(",", ":")))
    page = page.replace("/*__DATA_JSON__*/", json.dumps(data, separators=(",", ":")))
    return BUILT_MARK.format(date=when) + "\n" + page


def build_primitives(tokens: dict, when: str) -> str:
    """Parts 1-6 as their own page: every declared primitive, once.

    ⚠ IT IS ONE PAGE FOR THE SAME REASON THE LAB IS. The style vocabulary is not spec-specific
    — the `cap-tokens` block is byte-identical on all five spec pages — so drawing the gallery
    into each of them duplicated the whole of it five times and quietly implied the primitives
    were a claim about that spec's rotation. They are not. Only the roster a swatch borrows its
    icon art from differs, which is a property of the swatch and not of the primitive.

    It ships no scenarios, so `stepper.js` renders no stepper; the spec pages keep the walk and
    have no `#gallery` to draw into, which is all the gating either page needs.
    """
    cfg = SPECS_BUILT[SHELF_ROSTER_SPEC]
    roster = load_roster(cfg["catalog"])
    used = [n for n in cfg["scan_samples"] if n in roster]
    if not used:
        _die(f"{SHELF_ROSTER_SPEC}'s scan_samples resolve to nothing in "
             f"{cfg['catalog'].relative_to(ROOT)} — the gallery has no art to borrow")
    icons = icon_assets(used, roster, tokens)
    fakes = (tokens.get("preview") or {}).get("hotkeys") or []
    at = {name: i for i, name in enumerate(roster)}
    data = {
        "built": when,
        "client_paint": CLIENT_PAINT,
        "abilities": {
            name: {"key": roster[name]["key"], "spell": roster[name]["spell"],
                   "hotkey": (fakes[at[name] % len(fakes)] if fakes else ""),
                   "lane": roster[name]["lane"],
                   "charges": roster[name].get("charges", 0), "icon": icons[name]["uri"]}
            for name in used},
        "scan_samples": used,
        "scan_sample": used[0],
        # No scenarios: a primitive is drawn as itself, never as a step in somebody's rotation.
        "scenarios": [], "notes": [],
        "frames": badge_assets(tokens),
        "lab_stripes": hatch_asset(tokens),
        "promotion": promotion_asset(tokens),
        "provenance_html": primitives_provenance_html(tokens, icons, when),
    }
    page = (TEMPLATE / "primitives.html").read_text(encoding="utf-8")
    page = page.replace("/*__ROOT_TOKENS__*/", root_css(tokens))
    page = page.replace("/*__SHELF_CSS__*/", (TEMPLATE / "shelf.css").read_text(encoding="utf-8"))
    page = page.replace("/*__STEPPER_JS__*/", (TEMPLATE / "stepper.js").read_text(encoding="utf-8"))
    page = page.replace("/*__TOKENS_JSON__*/", json.dumps(tokens, separators=(",", ":")))
    page = page.replace("/*__DATA_JSON__*/", json.dumps(data, separators=(",", ":")))
    return BUILT_MARK.format(date=when) + "\n" + page


def primitives_provenance_html(tokens: dict, icons: dict, when: str) -> str:
    cues = [k for k in tokens.get("cues", {}) if not k.startswith("_")]
    rows = [
        ("render-shelf.md", f"sha {_sha(SHELF)} · Parts 1–6"),
        ("reference roster", f"{SHELF_ROSTER_SPEC} · {SPECS_BUILT[SHELF_ROSTER_SPEC]['catalog'].name}"
                             " — art only, never a rotation claim"),
        ("cues", f"{len(cues)} declared · {sum(1 for k in cues if tokens['cues'][k].get('open'))}"
                 " unverified in client"),
        ("icons", f"{len(icons)} × {tokens['assets']['icon_size']}px "
                  f"{tokens['assets']['encode']}"),
        ("built", when),
    ]
    return ("<table>" + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows) + "</table>")


def lab_provenance_html(tokens: dict, icons: dict, when: str) -> str:
    entries = [k for k in (tokens.get("lab") or {}) if not k.startswith("_")]
    rows = [
        ("render-shelf.md", f"sha {_sha(SHELF)} · Part 7, {len(entries)} "
                            f"{'entry' if len(entries) == 1 else 'entries'}"),
        ("reference roster", f"{SHELF_ROSTER_SPEC} · "
                             f"{SPECS_BUILT[SHELF_ROSTER_SPEC]['catalog'].name}"),
        ("icons", f"{len(icons)} × {tokens['assets']['icon_size']}px "
                  f"{tokens['assets']['encode']}"),
        ("authority", "<b>none</b> — Part 7 rule 3. A treatment leaves by being MOVED into "
                      "Parts 1–6, never by being cited from here."),
        ("built", when),
    ]
    return ("<table>" + "".join(f"<tr><th>{k}</th><td>{v}</td></tr>" for k, v in rows) + "</table>")


def build_index(when: str) -> str:
    """The directory's front door, listing every registered spec.

    `previews/CLAUDE.md` advertised this URL for weeks while the server answered it with a bare
    directory listing — every template file and asset folder beside the two pages anyone wanted.
    It is generated from `SPECS_BUILT`, so a newly registered spec appears without anyone
    remembering to add a row.
    """
    rows = []
    for spec in sorted(SPECS_BUILT):
        cfg = SPECS_BUILT[spec]
        out = cfg["out"]
        built = "not built yet"
        if out.exists():
            m = re.search(r"capart built: (\d{4}-\d{2}-\d{2})", out.read_text(encoding="utf-8"))
            built = f"built {m.group(1)}" if m else "built"
        rows.append(
            f'    <li><a href="{out.name}">{htmllib.escape(cfg.get("title", spec.title()))}'
            f'</a> <span>{built}</span></li>')
    return (
        BUILT_MARK.format(date=when) + "\n"
        "<title>cap previews</title>\n"
        "<style>\n"
        "  body { margin: 0; padding: 3rem 1.5rem; background: #14161b; color: #e8e6e1;\n"
        "         font: 15px/1.6 system-ui, sans-serif; }\n"
        "  main { max-width: 34rem; margin: 0 auto; }\n"
        "  h1 { font-size: 1.25rem; margin: 0 0 .25rem; }\n"
        "  p { color: #9a9eaa; }\n"
        "  ul { list-style: none; padding: 0; margin: 1.5rem 0 0; }\n"
        "  li { padding: .6rem 0; border-top: 1px solid #2a2e37; display: flex;\n"
        "       justify-content: space-between; gap: 1rem; }\n"
        "  a { color: #ffdb73; text-decoration: none; }\n"
        "  a:hover { text-decoration: underline; }\n"
        "  span { color: #7d8291; font-size: 13px; }\n"
        "</style>\n"
        "<main>\n"
        "  <h1>Combat Assist Plus — scenario steppers</h1>\n"
        "  <p>One page per spec, all generated by <code>wowkb.capart build --all</code> from\n"
        "     <code>specs/render-shelf.md</code> and each spec&rsquo;s <code>scenarios.md</code>.</p>\n"
        "  <ul>\n" + "\n".join(rows) + "\n  </ul>\n"
        # ONE more link, and deliberately below the specs rather than among them: the lab is not
        # a spec and the list above is what this page is for.
        "  <p><a href=\"primitives.html\">The primitives</a> — Parts 1–6, every declared\n"
        "     treatment as a live swatch. One page, because the style vocabulary is the same on\n"
        "     every spec.</p>\n"
        "  <p><a href=\"lab.html\">The lab</a> — Part 7, experiments with no authority.</p>\n"
        "</main>\n")


def cmd_build(args) -> None:
    tokens = load_tokens()
    when = args.date or date.today().isoformat()
    cap = tokens["budget"]["max_base64_kb"]
    for spec in _specs_of(args):
        page = build(spec, tokens, when)
        out = SPECS_BUILT[spec]["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page, encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)} · {len(page) / 1024:.0f} KB · built {when}")
        if len(page) / 1024 > cap:
            _warn(f"{out.name} is over the {cap} KB budget in tokens.budget — "
                  "run `wowkb.capart assets` for the per-asset table")
    prim_page = build_primitives(tokens, when)
    PRIMITIVES_OUT.write_text(prim_page, encoding="utf-8")
    print(f"wrote {PRIMITIVES_OUT.relative_to(ROOT)} · {len(prim_page) / 1024:.0f} KB · "
          f"{len([k for k in tokens.get('cues', {}) if not k.startswith('_')])} cues")
    lab_page = build_lab(tokens, when)
    LAB_OUT.write_text(lab_page, encoding="utf-8")
    entries = [k for k in (tokens.get("lab") or {}) if not k.startswith("_")]
    print(f"wrote {LAB_OUT.relative_to(ROOT)} · {len(lab_page) / 1024:.0f} KB · "
          f"{len(entries)} lab {'entry' if len(entries) == 1 else 'entries'}")
    INDEX_OUT.write_text(build_index(when), encoding="utf-8")
    print(f"wrote {INDEX_OUT.relative_to(ROOT)} · {len(SPECS_BUILT)} specs")


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
        # V15's font rides with Style.lua because Style.lua is what names its path.
        for name in export_style_font(tokens):
            print(f"  {name:<24} → {FONTS_DIR.relative_to(ROOT)}")
    if what in ("badges", "all"):
        for frame, size in export_badges(tokens):
            print(f"  {frame + '.tga':<24} {size[0]}x{size[1]} 32-bit → "
                  f"{BADGE_DIR.relative_to(ROOT)}")
    if what in ("ring", "all"):
        for name, size in export_ring(tokens):
            print(f"  {name + '.tga':<24} {size[0]}x{size[1]} 32-bit → "
                  f"{MEDIA_DIR.relative_to(ROOT)}")
    if what in ("count", "all"):
        for name, size in export_count(tokens):
            print(f"  {name + '.tga':<24} {size[0]}x{size[1]} 32-bit → pre-tinted (V16/V17)")
    if what in ("hatch", "all"):
        for name, size in export_hatch(tokens):
            print(f"  {name + '.tga':<24} {size[0]}x{size[1]} 32-bit → "
                  f"{MEDIA_DIR.relative_to(ROOT)}")
    if what in ("promotion", "all"):
        for name, size in export_promotion(tokens):
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
            if rule.get("eliminates"):
                # ⚠ THE THIRD ELIMINATING SIGNAL, since 2026-08-22. `ruled-sealed` is a band the
                # CLIENT evaluated against a secret: it draws V11's hatch and a negative mark out
                # of one FontString, so the row reads exactly as ruled out and carries no cue at
                # all. The gate has to know that or it walks straight past a hatched row.
                continue
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


def one_positive_per_entry(scenarios: list[dict], tokens: dict) -> list[str]:
    """Pass 1 needs ONE answer, and that is a constraint on a row rather than the vocabulary.

    "Scan left to right for a positive cue; if one is present, press it" is undefined if a single
    button wears two of them. It is perfectly defined when two different buttons in the vocabulary
    can each carry one, which is why the old cap of one positive cue overall was the wrong shape.
    """
    fails = []
    for sc in scenarios:
        for e in sc["row"]:
            worn = [k for k in _cues_of(e, tokens)
                    if tokens["cues"].get(k, {}).get("polarity") == "positive"]
            if len(worn) > 1:
                fails.append(f"{sc['id']}: {e['name']!r} wears {len(worn)} positive cues "
                             f"({', '.join(sorted(worn))}) — pass 1 says 'press the positive cue' "
                             "and says nothing about which of two wins.")
    return fails


#: Part 0.5's density rule. Stepping over one or two holds is a glance; three is counting.
NEGATIVE_BUDGET = 2


def density_gate(scenarios: list[dict], tokens: dict) -> list[str]:
    """THE DENSITY RULE, MECHANISED (render-shelf.md Part 0.5).

    Elimination is not free: every skip the reader steps over costs a badge to interpret. Past
    two, a row reads as "something is wrong" rather than "press the clean one", and the press
    should be PROMOTED instead of the skips being drawn.

    ⚠ Swipes do not count. Blizzard ran those buttons down and cap drew nothing; the reader is
    not paying for them.

    ⚠ Nor does every badge. Only cues flagged `budgeted` in the shelf count, which today is
    `blocked` alone. A hold is cap claiming a castable, affordable button should be skipped
    anyway — the reader cannot check that at a glance, and it is what costs interpretation.
    `starved` and `overcap` restate a resource already on the player's own bar, on buttons that
    were not pressable in that state.

    ⚠ This is the one gate that cannot be evaluated per marker. A hold is true or false on its
    own terms, but whether the row is too dense depends on what every OTHER entry is doing in
    that same state — so it is per scenario, and a catalog satisfies it by choosing which of the
    two shapes to author.
    """
    def negative(e) -> bool:
        rule = tokens["verdicts"][e["verdict"]]
        if rule["swipe"]:
            return False
        keys = list(rule.get("cues") or []) + list(e.get("cues") or [])
        return any(tokens["cues"].get(k, {}).get("polarity", "negative") == "negative"
                   and tokens["cues"].get(k, {}).get("budgeted", False)
                   for k in keys)

    fails = []
    for sc in scenarios:
        if wears_positive(sc, tokens):
            continue                      # promoted rows answer to pass 1, not to elimination
        press = next((i for i, e in enumerate(sc["row"])
                      if e["verdict"].startswith("press")), None)
        if press is None:
            continue                      # reading_gate already reports a row with no press
        skipped = [e["name"] for e in sc["row"][:press] if negative(e)]
        if len(skipped) > NEGATIVE_BUDGET:
            fails.append(
                f"{sc['id']}: {len(skipped)} holds stand between the left edge and the "
                f"press ({', '.join(skipped)}), over the budget of {NEGATIVE_BUDGET}.\n"
                "    Part 0.5: past two skips the reader is counting rather than glancing. Author "
                "`priority` on\n"
                f"    {sc['row'][press]['name']!r} and drop the holds it replaces, rather than "
                "raising this number.")
    return fails


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

    What keeps the chain honest is `one_positive_per_entry`: no single button may wear two
    positive cues, so "scan for a positive cue" always has one answer. That is the real
    invariant — until 2026-08-19 it was enforced as a cap of one positive cue in the whole
    vocabulary, which was the V5 three-slot geometry mistaken for a reading rule.
    """
    # Both passes quietly abstain on a row without exactly one press, so the chain has to assert
    # it itself or a malformed row would be judged by neither.
    fails = [f"{sc['id']}: expected exactly one `press*` entry, found "
             f"{[e['name'] for e in sc['row'] if e['verdict'].startswith('press')] or 'none'}"
             for sc in scenarios
             if len([e for e in sc["row"] if e["verdict"].startswith("press")]) != 1]
    positive = [sc for sc in scenarios if wears_positive(sc, tokens)]
    plain = [sc for sc in scenarios if not wears_positive(sc, tokens)]
    return (fails + one_positive_per_entry(scenarios, tokens)
            + positive_gate(positive, tokens) + elimination_gate(plain, tokens)
            + density_gate(scenarios, tokens))


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


DATA_RE = re.compile(r'<script type="application/json" id="cap-data">(.*?)</script>', re.S)


def _page_data(out: Path) -> dict | None:
    """The `data` blob capart embedded in a built page, read back out of it."""
    m = DATA_RE.search(out.read_text(encoding="utf-8"))
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def _check_shared() -> list[str]:
    """The two pages that belong to no spec: the lab and the index.

    ⚠ THIS GATE EXISTS BECAUSE ONE OF THEM HAD NO GATE AT ALL. `index.html` has been generated by
    `build --all` and checked by nothing since it shipped, so a newly registered spec could be
    missing from the front door indefinitely and the run would still read green. `lab.html` would
    have inherited the same hole the day it was split out — the per-spec staleness gate is inside
    the per-spec loop, and neither of these is a spec.
    """
    tokens = load_tokens()
    fails = []
    for out, rebuild, what in ((PRIMITIVES_OUT, build_primitives, "primitives.html"),
                               (LAB_OUT, build_lab, "lab.html"),
                               (INDEX_OUT, lambda t, w: build_index(w), "index.html")):
        if not out.exists():
            fails.append(f"no {what} at {out.relative_to(ROOT)} — run: wowkb.capart build --all")
            continue
        committed = out.read_text(encoding="utf-8")
        m = BUILT_RE.search(committed)
        if not m:
            fails.append(f"{what} carries no build stamp — rebuild it")
        elif rebuild(tokens, m.group(1)) != committed:
            fails.append(f"{what} is stale — rebuild: wowkb.capart build --all")
    # The index is the front door and a spec missing from it is invisible, which is the one
    # failure a byte-compare of a self-generated file cannot catch on its own.
    if INDEX_OUT.exists():
        listing = INDEX_OUT.read_text(encoding="utf-8")
        for spec, cfg in sorted(SPECS_BUILT.items()):
            if cfg["out"].name not in listing:
                fails.append(f"{spec} is registered in SPECS_BUILT but the index does not link "
                             f"{cfg['out'].name} — run: wowkb.capart build --all")
        for name, why in (("primitives.html", "Parts 1–6"), ("lab.html", "Part 7")):
            if name not in listing:
                fails.append(f"the index does not link {name} — {why} would be unreachable from "
                             "the front door")
    return fails


def cmd_check(args) -> None:
    specs = _specs_of(args)
    if len(specs) > 1:
        # Run each in turn so one spec's failure does not hide the next one's. Exit non-zero if
        # ANY failed — a gate that stops at the first bad spec under-reports on the run where it
        # matters most.
        bad = []
        for spec in specs:
            print(f"── {spec}", flush=True)   # flushed so the per-spec verdicts stay interleaved
                                             # with anything the gates write to stderr
            try:
                _check_one(argparse.Namespace(spec=spec, all_specs=False))
            except SystemExit as exc:
                if exc.code:
                    bad.append(spec)
            sys.stdout.flush()
        shared = _check_shared()
        if shared:
            print("── shared pages")
            print("FAIL")
            for line in shared:
                print(f"  {line}")
            bad.append("shared pages")
        else:
            print("── shared pages")
            print("ok · lab.html and index.html are current, and the index links every "
                  "registered spec plus the lab")
        if bad:
            sys.exit(f"FAILED: {', '.join(bad)}")
        return
    _check_one(argparse.Namespace(spec=specs[0], all_specs=False))


def _check_one(args) -> None:
    tokens = load_tokens()
    cfg = SPECS_BUILT[args.spec]
    fails = []

    for line in strict_css(TEMPLATE / "shelf.css"):
        fails.append(line)
    fails += smoke_dom(TEMPLATE / "stepper.js", TEMPLATE / "shelf.css", root_css(tokens))
    fails += gallery_covers_sealed(TEMPLATE / "stepper.js")

    # 0z · the OTHER subcommands still run. `tokens` and `assets` read the token block on paths
    # `build` does not, and both sat dead behind a KeyError for a week while `check` reported
    # green — because `check` reads the sidecar and the tokens and renders nothing. This is the
    # cheapest possible standing answer to that: run them, discard the output, fail on a raise.
    for name, fn in (("tokens", cmd_tokens), ("assets", cmd_assets)):
        buf = io.StringIO()
        try:
            with contextlib.redirect_stdout(buf):
                fn(argparse.Namespace(spec=args.spec, css=False, all_specs=False))
        except SystemExit as exc:                       # `assets` exits 1 over budget; that is
            if exc.code:                                # a real finding, not a crash
                fails.append(f"capart {name} exited {exc.code}")
        except Exception as exc:                        # noqa: BLE001 — any raise is the finding
            fails.append(f"capart {name} raised {type(exc).__name__}: {exc}")

    # 0 · the tint guard still has EVERY subject. `assert_tintable` is the shelf's one mechanical
    # promise, and a guard whose subject set quietly shrinks keeps passing while guaranteeing less
    # each time — which is exactly what the lane→scan collapse did to it: `tokens.badges.tint`
    # changed value, the guard matched a literal, and the badge sprites went unguarded while this
    # gate stayed green on the ring alone. So it is checked per primitive, not as an any-of.
    # ⚠ `promotion`, `count` and `pandemic` were added 2026-08-22. The first two words of this
    # comment are the finding: V14 shipped declaring `tint: "lane"`, a value from the retired lane
    # vocabulary that `assert_tintable` does not match — so the primitive whose whole advantage
    # over Blizzard's own proc glow is that it is NEUTRAL was the one going unguarded.
    for name in ("badges", "ring", "hatch", "promotion", "count", "pandemic"):
        art = tokens.get(name)
        if art is None:
            continue
        if art.get("tint") not in ("shelf", "desaturate+shelf", "none"):
            fails.append(
                f"tokens.{name}.tint is {art.get('tint')!r}, which the Part 4 tint guard does not "
                "recognise — so that art ships unguarded and a baked hue in it would render as a "
                "recolour SetVertexColor cannot perform. Use \"shelf\", \"desaturate+shelf\" "
                "or a deliberate \"none\".")

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

    # 0b · at most one positive cue PER ENTRY. Pass 1 says "scan for A positive cue and press
    # it", which needs one answer — but that is a constraint on a ROW, not on the vocabulary.
    # Until 2026-08-19 this gate capped the vocabulary at one positive cue, which was the V5
    # three-slot geometry read backwards; the badge stack now flows and there is no ceiling.
    # See render-shelf.md Part 0.5, "There is no positive-cue budget".

    # 1 · the doc leads the sidecar.
    doc = scrape_scenarios(cfg["scenarios"])
    # 1a · the built page carries what it needs to DRAW a row. The shelf is assembled in the
    # browser out of the embedded JSON, so there is no markup to count here — but a blank row
    # has a static cause every time: a scenario entry with no `abilities` record, or one whose
    # icon URI never resolved. ⚠ This is not a render. `check` still cannot tell you the page
    # looks right; only a browser can, which is why the previews are served and looked at.
    if cfg["out"].exists():
        data = _page_data(cfg["out"])
        if data is None:
            fails.append(f"{cfg['out'].name} carries no embedded data block — it is not a build "
                         "this tool produced.")
        else:
            names = {e["name"] for sc in data.get("scenarios", []) for e in sc.get("row", [])}
            names |= set(data.get("scan_samples", []))
            if not names:
                fails.append(f"{cfg['out'].name} embeds no row entries at all — the page renders "
                             "an empty shelf.")
            for name in sorted(names):
                ab = data.get("abilities", {}).get(name)
                if not ab:
                    fails.append(f"{cfg['out'].name}: {name!r} is drawn but has no abilities "
                                 "record — that row renders blank.")
                elif not ab.get("icon"):
                    fails.append(f"{cfg['out'].name}: {name!r} has no icon URI — that row renders "
                                 "as an empty square.")

    if not cfg["sidecar"].exists():
        fails.append(f"no sidecar at {cfg['sidecar'].relative_to(ROOT)}")
    else:
        side = json.loads(cfg["sidecar"].read_text(encoding="utf-8"))["scenarios"]
        d_ids = [s["id"] for s in doc]
        s_ids = [s["id"] for s in side]
        if d_ids != s_ids:
            fails.append(f"scenario ids differ — doc {d_ids} vs sidecar {s_ids}")
        else:
            # ⚠ Compare the WHOLE scenario, not a chosen tuple of fields.
            #
            # This used to compare `(name, verdict, cues)` per row and nothing else, which made
            # the sidecar silently authoritative for everything it did not check: `build` renders
            # scenario PROSE out of the sidecar, so an edit to a `State`/`Walk`/eye-direction
            # bullet never reached the preview and no gate said so. The advice that grew around
            # it — "remember to re-import after editing prose, not only after editing a row" — was
            # a human standing in for a comparison the tool could just do.
            #
            # It also silently swallowed every field added later. `{client: …}`, added 2026-08-18,
            # was outside the tuple from the day it shipped: the client-paint layer could be
            # edited in the doc and never appear on the page. A whitelist of compared fields is
            # wrong by construction here, because the failure mode is always a NEW field nobody
            # remembered to add to it.
            for a, b in zip(doc, side):
                if a == b:
                    continue
                fails.append(f"{a['id']}: {cfg['scenarios'].name} differs from the sidecar — "
                             f"re-run: wowkb.capart import scenarios {args.spec}")
                for key in sorted(set(a) | set(b)):
                    if a.get(key) == b.get(key):
                        continue
                    if key == "row":
                        ra, rb = a.get("row") or [], b.get("row") or []
                        for x, y in zip(ra, rb):
                            if x != y:
                                fails.append(f"    row: doc {x} != sidecar {y}")
                        if len(ra) != len(rb):
                            fails.append(f"    row: doc has {len(ra)} entries, sidecar {len(rb)}")
                    else:
                        fails.append(f"    {key}: doc and sidecar disagree")

    # 1b · the reading rule holds, as the ORDERED chain Part 0.5 defines: a row wearing a
    # positive cue is judged by pass 1, every other row by pass 2. Not both on both — that is
    # what made a legitimate pass-1 override unrepresentable.
    fails += reading_gate(doc, tokens)

    # 0c · RETIRED 2026-08-16 with the veil itself. It reconciled each verdict's hand-written
    # `veil` against the polarity of the cues that verdict carried; the veil no longer exists as a
    # primitive, so the gate has no subject. There is nothing to put in its place: a row's skip is
    # now said once, by the badge, and a rule that a badge implies a badge is not a rule.

    # 0d · every positive cue ranks above every negative one, so a promotion always lands on the
    # corner where the eye arrives first (render-shelf.md Part 1). This replaced the old
    # "slot 3 belongs to the positive cue" assertion when the stack began to flow: absolute
    # positions stopped existing, and the ordering is what actually carried the meaning.
    ranks = {k: c.get("rank") for k, c in tokens["cues"].items()}
    missing = sorted(k for k, r in ranks.items() if not isinstance(r, int))
    if missing:
        fails.append(f"cues with no integer `rank`: {', '.join(missing)} — the badge stack packs "
                     "in rank order, so a cue without one has no defined position.")
    else:
        worst_positive = max((r for k, r in ranks.items()
                              if tokens["cues"][k].get("polarity") == "positive"), default=None)
        best_negative = min((r for k, r in ranks.items()
                             if tokens["cues"][k].get("polarity") != "positive"), default=None)
        if worst_positive is not None and best_negative is not None \
                and worst_positive > best_negative:
            fails.append(
                f"a negative cue ranks above a positive one (best negative rank {best_negative}, "
                f"worst positive {worst_positive}) — Part 1 packs positives onto the corner so a "
                "promotion is the badge the eye reaches first.")
        if len(set(ranks.values())) != len(ranks):
            fails.append("two cues share a `rank` — the stack order would depend on dict order, "
                         "so two rows wearing the same pair could stack them differently.")

    # 0e · A NEGATIVE CUE DOES NOT MOVE. Motion is the third polarity carrier (render-shelf.md
    # V5.1, 2026-08-23), and it is the one the other two cannot cover: hue and glow are read where
    # the eye already is, motion pulls it. A negative is up for as long as its skip is true, which
    # in a pull is most of the fight, so animating one spends the player's attention on precisely
    # the rows that wanted none of it. That was the player's own report on the first Demonology
    # flight — the blinking negatives were "too much" — and it is the kind of ruling that decays
    # back into prose the moment someone adds a cue and copies the two-frame `BOUNCE` off a
    # neighbour, so it is a gate rather than a paragraph.
    for key, cue in sorted(tokens["cues"].items()):
        if cue.get("polarity") == "positive":
            continue
        if len(cue.get("frames") or []) > 1:
            fails.append(
                f"negative cue {key!r} declares {len(cue['frames'])} frames — a negative cue is a "
                "STILL IMAGE (render-shelf.md V5.1). Motion carries polarity: gold + halo + "
                "animation says act, red + still says skip. Pick the one frame that states the "
                "condition on its own and drop the rest.")

    # 0f · the SHIPPED font is the one the shelf declares, byte for byte.
    #
    # Gated exactly as Style.lua is, and for the same reason: generation buys nothing the first
    # time someone edits one and not the other. It also catches the thing that would be worst
    # here — a `Media/fonts/` file with no licence beside it, or one left behind after the style
    # moved to a font the client already has.
    if ADDON_SRC.exists():
        spec = (tokens.get("preview") or {}).get("hotkey_font") or {}
        want = {}
        if spec.get("shippable"):
            name = spec.get("ship_as") or spec["family"]
            want[f"{name}.ttf"] = _subset_font(_font_source(spec), "tokens.preview.hotkey_font",
                                               spec.get("ship_as"))
            if spec.get("license_url"):
                want["OFL.txt"] = _font_text(spec["license_url"])
        have = {f.name for f in FONTS_DIR.glob("*")} if FONTS_DIR.exists() else set()
        for name, data in want.items():
            path = FONTS_DIR / name
            if not path.exists():
                fails.append(f"Media/fonts/{name} is missing — run: wowkb.capart export lua")
            elif path.read_bytes() != data:
                fails.append(f"Media/fonts/{name} disagrees with the shelf — "
                             "run: wowkb.capart export lua")
        for stale in sorted(have - set(want) - {"NOTICE.txt"}):
            fails.append(f"Media/fonts/{stale} is shipped but the shelf does not declare it — "
                         "run: wowkb.capart export lua")
        if want and "OFL.txt" not in want and spec.get("license", "").upper().startswith("OFL"):
            fails.append("tokens.preview.hotkey_font claims an OFL licence but names no "
                         "`license_url`, so the licence would ship with no text beside it.")

    # 0e · CHROME IS NOT A CUE, and this is what makes that mechanical rather than promised.
    #
    # The reading model's gates (`_cues_of`, `reading_gate`, the rank check above, 1c) all iterate
    # `tokens["cues"]` and nothing enumerates top-level token keys, so a sibling key is invisible
    # to them by construction — which is exactly why the ruling needs a gate of its OWN. Nothing
    # would have failed if `hotkey` had quietly grown a polarity and started ranking rows.
    #
    # ⚠ This replaces the plan's "the hint claims no badge slot": the three fixed slots were
    # retired on 2026-08-19 and the stack flows, so there is no slot left to claim. The geometry
    # assertion that still means something is the CORNER — the badges flow from
    # `tokens.badges.flow.anchor` and chrome must not start there.
    hk = tokens.get("hotkey")
    if hk is not None:
        if "hotkey" in tokens["cues"]:
            fails.append("`hotkey` is declared as a cue — it is chrome (spec.md §3.8): it names a "
                         "row and asserts nothing about the press, so it must take no part in "
                         "elimination or the badge vocabulary.")
        for key in ("polarity", "rank"):
            if key in hk:
                fails.append(f"tokens.hotkey declares `{key}` — chrome has no polarity and no "
                             "rank (spec.md §3.8). A label that can be mistaken for a signal is "
                             "the one way V15 breaks the reading model.")
        for name, rule in tokens["verdicts"].items():
            if "hotkey" in (rule.get("cues") or []):
                fails.append(f"verdict {name!r} names `hotkey` in its cues — chrome is not "
                             "authored per verdict and never rules a row in or out.")
        corner = (tokens["badges"].get("flow") or {}).get("anchor", "top-right-corner")
        if corner.replace("-corner", "").replace("-", "") == hk.get("anchor", "").lower():
            fails.append(f"tokens.hotkey.anchor is {hk.get('anchor')!r}, which is the corner the "
                         f"badge stack flows from ({corner}) — the two would negotiate a place, "
                         "and chrome is supposed to hold a corner no cue may claim.")

    # 1b-ii · an entry may not DECLARE a cue its verdict already implies.
    #
    # `{cues: …}` exists to add a cue the verdict does not carry. Naming one it already carries is
    # a second mention of a single cue, and the renderer drew it as a second badge — two identical
    # red discs on one icon, which reads as two different reasons rather than as one. The
    # renderer now dedupes, so this is about the DOC saying what it means: found 2026-08-19 with
    # 8 such entries in Havoc, all of them following advice this file used to print.
    for sc in doc:
        for e in sc["row"]:
            implied = set(tokens["verdicts"].get(e["verdict"], {}).get("cues") or [])
            dup = sorted(implied & set(e.get("cues") or []))
            if dup:
                fails.append(
                    f"{sc['id']}: {e['name']!r} declares {{cues: {', '.join(dup)}}}, which its "
                    f"`{e['verdict']}` verdict already implies.\n"
                    "    Drop the group — a cue named twice is one badge, and the declaration "
                    "adds nothing but noise.")

    # 1c · every declared cue actually draws somewhere. spec.md §3.2 — "a catalog form that
    # loads successfully and then renders nothing is a defect" — and a cue nobody wears is that
    # defect at the shelf level. It matters most for the positive cue, whose whole justification
    # is one scenario: if ST-10 ever stops carrying it, the exception has no subject and should be
    # retired rather than left declared.
    #
    # ⚠ **The subject is EVERY built spec, not the one being checked.** The cue vocabulary is the
    # shelf's and is shared; a catalog is entitled to decline a cue whose fact its rotation does
    # not have. Retribution declines `capped` deliberately (catalog.md, "Why this catalog does not
    # spend the positive cue") — scoped per-spec, this gate would read that considered decision as
    # a defect and the only way to pass would be to invent a scenario for it, which is precisely
    # the pressure spec.md §3.2 exists to resist. Scoped across the union it still catches the
    # thing it was written for: a cue NO catalog anywhere wears.
    worn = set()
    for name, other in SPECS_BUILT.items():
        for sc in (doc if name == args.spec else scrape_scenarios(other["scenarios"])):
            for e in sc["row"]:
                worn |= set(tokens["verdicts"][e["verdict"]].get("cues") or [])
                worn |= set(e.get("cues") or [])
    for key in tokens["cues"]:
        if key not in worn:
            fails.append(f"cue {key!r} is declared in the shelf but no scenario row in any built "
                         f"spec ({', '.join(sorted(SPECS_BUILT))}) wears it — it renders nowhere, "
                         "which spec.md §3.2 calls a defect. Give it a subject or retire it.")

    # 2 · the committed HTML is not stale.
    out = cfg["out"]
    if not out.exists():
        fails.append(f"no preview at {out.relative_to(ROOT)} — run: wowkb.capart build {args.spec}")
    else:
        committed = out.read_text(encoding="utf-8")
        m = BUILT_RE.search(committed)
        if not m:
            fails.append(f"{out.name} carries no build stamp — rebuild it")
        elif build(args.spec, tokens, m.group(1)) != committed:
            fails.append(f"{out.name} is stale — rebuild: wowkb.capart build {args.spec}")

    # 3 · the addon carries the same style as the preview. Generation buys nothing the first
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
    print(f"ok · {args.spec}: scenarios.md matches the sidecar, the preview is current, "
          "shelf.css holds no literal colors,\n"
          "     Style.lua, Media/ring.tga and Media/stripes.tga agree with the shelf and the "
          "arrival's frames × tick match its duration,\n"
          "     every art-bearing primitive still declares the tint guard, tokens/assets both "
          "run, every class\n"
          "     stepper.js names is styled, every drawn row resolves to an icon, and the positive\n"
          f"     cues rank onto the corner, and all {len(doc)} scenarios read correctly under the pass they\n"
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

    b = sub.add_parser("build", help="render the preview")
    b.add_argument("spec", nargs="?", choices=sorted(SPECS_BUILT),
                   help="the spec to render; omit it and pass --all for every one")
    b.add_argument("--all", action="store_true", dest="all_specs",
                   help="render every spec in SPECS_BUILT — what a --on-change watcher wants, "
                        "since it fires on edits to any spec")
    b.add_argument("--date", help="stamp this build date instead of today (used by `check`)")
    b.set_defaults(func=cmd_build)

    e = sub.add_parser("export",
                       help="write the shelf into the addon (Style.lua + badge art + Lab.lua)")
    e.add_argument("what", nargs="?", default="all",
                   choices=["lua", "badges", "ring", "hatch", "promotion", "count", "lab", "all"])
    e.set_defaults(func=cmd_export)

    c = sub.add_parser("check", help="doc-vs-sidecar and preview-staleness gates")
    c.add_argument("spec", nargs="?", choices=sorted(SPECS_BUILT),
                   help="the spec to gate; omit it and pass --all for every one")
    c.add_argument("--all", action="store_true", dest="all_specs",
                   help="gate every spec in SPECS_BUILT — the CI form, so a new spec is covered "
                        "the moment it is registered")
    c.set_defaults(func=cmd_check)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
