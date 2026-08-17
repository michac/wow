"""Fetch a SimulationCraft MID1 default profile (APL) → digest markdown, for the KB.

The `knowledge/classes/<class>/<spec>/rotation.md` files distill their priority
lists from SimulationCraft's **default APLs** — the Tier-1, deterministic source
that keeps the curated rotations honest. Those APLs live one-per-spec in the simc
`midnight` branch at:

    https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_<Class>_<Spec>.simc

This tool standardizes that fetch: it pulls the raw `.simc`, **pins provenance**
to the current commit SHA + date via the GitHub commits API (so a citation names
a commit, not a moving branch), and emits a distillation-ready **digest** — the
`talents=` hash(es), any hero-tree/profileset variant names, and the `actions.*`
priority sublists grouped by list.

**Caveat (baked into every digest header):** the simc `midnight` binary/branch
can lag the live patch — `sims.md` already warns the 12.0.5 binary trailed the
12.0.7 game. The commit date stamps *when* the APL was generated so its staleness
is visible; this fetcher does **not** run a sim or produce DPS numbers (that's the
separate docker recipe in `sims.md`).

**`--kb` is the one that matters for the KB.** `raw/` is gitignored and CLAUDE.md
forbids citing it, so a rotation.md could never point at a fetched APL — it had to
hand-copy the priority list, and a hand-copied list drifts. Measured 2026-08-17:
Havoc's rotation.md quoted APL variables (`use_blade_dance`, `eb_aligned`) that the
12.1 rewrite had deleted outright. `--kb` writes the list into the KB **once**, as a
generated artifact, so `rotation.md` augments it instead of restating it.

Upstream does not lay these files out consistently, and all four shapes are handled:
`apl_<class>.cpp` with `//<spec>_apl_start` markers (most), `<class>.cpp` (mage,
warlock), `<class>/<spec>_apl.inc` (druid), C++ `namespace <spec>` blocks (monk), and
the generated `profiles/MID1` profile as a last resort (enhancement). The action-list
NAME is read from each `get_action_priority_list("...")` declaration rather than from
the C++ variable holding it — monk opens `pre`/`def`/`ite` for
"precombat"/"default"/"item_actions", so guessing mislabels every list.

Usage:
    uv run python -m wowkb.simc --list                       # enumerate all MID1 profiles (discover variants)
    uv run python -m wowkb.simc warlock demonology           # base profile → raw/simc/<file>.simc + .digest.md
    uv run python -m wowkb.simc dh vengeance --variant Aldrachi_Reaver   # a hero-tree variant profile
    uv run python -m wowkb.simc warlock affliction --no-sha   # skip the commits API (raw only)
    uv run python -m wowkb.simc --kb --all                    # every spec → knowledge/classes/<class>/<spec>/simc-apl.md
    uv run python -m wowkb.simc --kb dh havoc                 # one spec
    uv run python -m wowkb.simc --kb --check                  # CI gate: exit 1 on drift or a stale APL source

Outputs (both printed):
    raw/simc/<file>.simc         # verbatim fetch cache (gitignored, like maxroll/youtube)
    raw/simc/<file>.digest.md    # provenance header + talents + grouped actions.*
    knowledge/classes/<class>/<spec>/simc-apl.md   # --kb: the citable generated artifact
"""

import argparse
import datetime
import pathlib
import re
import sys

import requests

from ._common import save_raw

# A real browser UA — raw.githubusercontent.com is fine with anything, but the
# GitHub API is friendlier to a named client; keep it consistent with maxroll.
UA = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"
)

RAW_BASE = "https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1"
API_CONTENTS = "https://api.github.com/repos/simulationcraft/simc/contents/profiles/MID1?ref=midnight"
API_COMMITS = (
    "https://api.github.com/repos/simulationcraft/simc/commits"
    "?sha=midnight&path=profiles/MID1/{file}&per_page=1"
)

# The APL SOURCE, which the profiles are generated FROM. It is updated per patch
# while a generated profile may simply never be regenerated — measured 2026-08-16,
# when every Warlock MID1 profile carried a 12.1 launch-day commit and
# MID1_Demon_Hunter_Havoc.simc was still pinned to 2026-03-13, five months stale.
APL_DIR = "engine/class_modules/apl"
APL_MODULE = (
    "https://raw.githubusercontent.com/simulationcraft/simc/midnight/"
    + APL_DIR + "/apl_{class_lower}.cpp"
)
# Paths below are repo-relative from simc's root, so one raw URL and one commits URL
# serve the APL modules, druid's .inc files and the generated MID1 profiles alike.
RAW_ROOT = "https://raw.githubusercontent.com/simulationcraft/simc/midnight/"
API_MODULE_COMMITS = (
    "https://api.github.com/repos/simulationcraft/simc/commits"
    "?sha=midnight&path={path}&per_page=1"
)
APL_RAW = RAW_ROOT + "{path}"

# Upstream does not name these files consistently: most classes are `apl_<class>.cpp`,
# mage and warlock dropped the prefix, and druid keeps its module in a subdirectory
# beside per-spec `.inc` files. Tried in order; the first that returns 200 wins.
MODULE_CANDIDATES = (APL_DIR + "/apl_{c}.cpp", APL_DIR + "/{c}.cpp",
                     APL_DIR + "/{c}/{c}.cpp")

# Druid's specs are not in its .cpp at all — each is an `.inc` the .cpp includes, and
# the whole file IS the block. `restoration` needs the class name appended upstream.
INC_CANDIDATES = (APL_DIR + "/{c}/{s}_apl.inc", APL_DIR + "/{c}/{s}_{c}_apl.inc")

# `knowledge/_meta/game-version.md` is the single source of truth for what is live.
REPO = pathlib.Path(__file__).resolve().parents[2]
GAME_VERSION = REPO / "knowledge" / "_meta" / "game-version.md"
KB_CLASSES = REPO / "knowledge" / "classes"

# The generated block markers, matching `wowkb.gen_verify`'s convention. `--check`
# compares ONLY what sits between them, so a re-stamped `fetched:` is not drift.
GEN_BEGIN = "<!-- gen_simc:begin -->"
GEN_END = "<!-- gen_simc:end -->"


def live_patch_date() -> tuple[str, str] | None:
    """(patch, YYYY-MM-DD it went live), read from game-version.md. None if unreadable."""
    try:
        text = GAME_VERSION.read_text(encoding="utf-8")
    except OSError:
        return None
    patch = re.search(r"^patch:\s*([0-9.]+)", text, re.M)
    live = re.search(r"live (\d{4}-\d{2}-\d{2})", text)
    if not (patch and live):
        return None
    return patch.group(1), live.group(1)


def staleness(commit: dict | None) -> tuple[int, str, str] | None:
    """Days the pinned APL predates the live patch, or None when it does not.

    This is the check that would have caught a five-month-old Havoc APL being cited
    as current. A profile is not "the current rotation" because it is the newest file
    that exists — it is current only if it postdates the patch it claims to describe.
    """
    if not commit or not commit.get("date"):
        return None
    live = live_patch_date()
    if not live:
        return None
    patch, live_date = live
    try:
        d0 = datetime.date.fromisoformat(commit["date"][:10])
        d1 = datetime.date.fromisoformat(live_date)
    except ValueError:
        return None
    if d0 >= d1:
        return None
    return (d1 - d0).days, patch, live_date

# Class-token aliases → the exact filename segment (underscored, TitleCase).
CLASS_ALIASES = {
    "dk": "Death_Knight", "deathknight": "Death_Knight", "death_knight": "Death_Knight",
    "dh": "Demon_Hunter", "demonhunter": "Demon_Hunter", "demon_hunter": "Demon_Hunter",
    "druid": "Druid", "evoker": "Evoker", "hunter": "Hunter", "mage": "Mage",
    "monk": "Monk", "paladin": "Paladin", "pally": "Paladin", "priest": "Priest",
    "rogue": "Rogue", "shaman": "Shaman", "sham": "Shaman",
    "warlock": "Warlock", "lock": "Warlock", "warrior": "Warrior", "warr": "Warrior",
}
# Spec-token aliases → the exact filename segment. Unlisted specs are TitleCased
# verbatim (e.g. "havoc" → "Havoc"), so only the shortenings need entries.
SPEC_ALIASES = {
    "aff": "Affliction", "afflic": "Affliction", "affli": "Affliction",
    "demo": "Demonology", "destro": "Destruction", "destruct": "Destruction",
    "dev": "Devourer", "veng": "Vengeance", "prot": "Protection", "ret": "Retribution",
    "disc": "Discipline", "resto": "Restoration", "guardian": "Guardian",
    "feral": "Feral", "balance": "Balance", "boomkin": "Balance",
    "surv": "Survival", "bm": "Beast_Mastery", "mm": "Marksmanship",
    "unholy": "Unholy", "arms": "Arms", "fury": "Fury", "sub": "Subtlety",
    "sin": "Assassination", "assa": "Assassination", "outlaw": "Outlaw",
    "ele": "Elemental", "enh": "Enhancement", "ww": "Windwalker", "brew": "Brewmaster",
    "mw": "Mistweaver", "holy": "Holy", "shadow": "Shadow", "arcane": "Arcane",
    "fire": "Fire", "frost": "Frost", "aug": "Augmentation", "dev_evoker": "Devastation",
}


def _titleseg(token: str, aliases: dict) -> str:
    key = token.strip().lower().replace("-", "_")
    if key in aliases:
        return aliases[key]
    # TitleCase each underscore-separated word: "beast_mastery" → "Beast_Mastery".
    return "_".join(w.capitalize() for w in key.split("_"))


def profile_filename(class_token: str, spec_token: str, variant: str | None) -> str:
    cls = _titleseg(class_token, CLASS_ALIASES)
    spec = _titleseg(spec_token, SPEC_ALIASES)
    name = f"MID1_{cls}_{spec}"
    if variant:
        # Variant segment is kept as-given (may carry hyphens, e.g. Void-Scarred).
        name += "_" + variant.strip().strip("_")
    return name + ".simc"


def _get(url: str) -> requests.Response:
    return requests.get(url, headers={"User-Agent": UA}, timeout=60)


def list_profiles() -> list[str]:
    resp = _get(API_CONTENTS)
    resp.raise_for_status()
    return sorted(e["name"] for e in resp.json() if e.get("name", "").endswith(".simc"))


def resolve_commit(filename: str) -> dict | None:
    """Latest commit that touched this profile → {sha, short, date}, or None.

    Unauthenticated GitHub API is rate-limited (60/hr); on any failure we fall
    back to raw-only so a fetch still succeeds (SHA-less citation, --no-sha).
    """
    try:
        resp = _get(API_COMMITS.format(file=filename))
        if resp.status_code != 200:
            return None
        data = resp.json()
        if not isinstance(data, list) or not data:
            return None
        commit = data[0]
        sha = commit["sha"]
        date = commit["commit"]["committer"]["date"][:10]  # YYYY-MM-DD
        return {"sha": sha, "short": sha[:7], "date": date}
    except (requests.RequestException, KeyError, ValueError):
        return None


def parse_profile(text: str) -> dict:
    """Pull the digest-ready material out of a .simc profile.

    Returns: profile name, spec/level/race, talents hash(es), profileset variant
    names, and the actions.* lists grouped {list_name: [action, ...]} in order.
    """
    profile_name = None
    meta: dict[str, str] = {}
    talents: list[str] = []
    profilesets: list[str] = []
    action_lists: dict[str, list[str]] = {}

    m = re.match(r'^\s*\w+="([^"]+)"', text)
    if m:
        profile_name = m.group(1)

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        # `key=value` scalar meta lines we want to surface.
        for key in ("spec", "level", "race", "role", "default_pet"):
            m = re.match(rf"^(?:\w+\.)?{key}=(.+)$", line)
            if m:
                meta[key] = m.group(1)

        m = re.match(r"^talents=(\S+)$", line)
        if m:
            talents.append(m.group(1))
            continue

        # profileset."Some Variant Name"+=/talents=HASH (build variants in-file).
        m = re.match(r'^profileset\."([^"]+)"', line)
        if m and m.group(1) not in profilesets:
            profilesets.append(m.group(1))

        # actions[.<list>]=action  /  actions[.<list>]+=/action
        m = re.match(r"^actions(?:\.([\w]+))?(?:\+)?=/?(.*)$", line)
        if m:
            list_name = m.group(1) or "default"
            action = m.group(2).strip()
            if action:
                action_lists.setdefault(list_name, []).append(action)

    return {
        "profile_name": profile_name,
        "meta": meta,
        "talents": talents,
        "profilesets": profilesets,
        "action_lists": action_lists,
    }


def _action_verb(action: str) -> str:
    """The ability/directive at the head of an action line (before the first comma)."""
    return action.split(",", 1)[0]


def render_digest(filename: str, url: str, commit: dict | None, parsed: dict) -> str:
    today = datetime.date.today().isoformat()
    meta = parsed["meta"]
    lines: list[str] = []

    # ── Provenance header ─────────────────────────────────────────────
    lines.append(f"# simc APL digest — {parsed['profile_name'] or filename}")
    lines.append("")
    lines.append(f"- profile: `{filename}`")
    lines.append(f"- source: {url}  (SimulationCraft `midnight` branch, Tier 1)")
    if commit:
        lines.append(
            f"- pinned commit: `{commit['short']}` ({commit['sha']}), "
            f"committed {commit['date']}"
        )
        cite = (
            f"simc midnight branch profiles/MID1/{filename}  "
            f"# tier 1 APL, commit {commit['short']} {commit['date']}"
        )
    else:
        lines.append(
            "- pinned commit: **unavailable** (GitHub API rate-limited or --no-sha) "
            "— raw fetch only, no SHA pin"
        )
        cite = (
            f"simc midnight branch profiles/MID1/{filename}  "
            f"# tier 1 APL, fetched {today} (commit SHA unresolved)"
        )
    lines.append(f"- fetched: {today}")
    if meta.get("spec"):
        detail = "  ".join(f"{k}={meta[k]}" for k in ("spec", "level", "race", "default_pet") if k in meta)
        lines.append(f"- profile detail: {detail}")
    lines.append("")
    stale = staleness(commit)
    if stale:
        days, patch, live_date = stale
        lines.append(
            f"> ❌❌ **THIS APL PREDATES THE LIVE PATCH BY {days} DAYS — DO NOT CITE IT AS "
            f"CURRENT.** It was generated {commit['date']}; **{patch}** went live "
            f"{live_date}. Upstream regenerates these profiles per spec and sometimes "
            "never gets to one: on 2026-08-16 every Warlock MID1 profile carried a 12.1 "
            "launch-day commit while this Havoc profile was still on 2026-03-13. **The "
            "newest file that exists is not the same as a current one.**\n>\n"
            "> The APL SOURCE the profiles are generated from is updated per patch — "
            "`engine/class_modules/apl/apl_<class>.cpp` on the `midnight` branch. When a "
            "profile is stale, read that instead and expect the priority list to differ "
            "structurally, not just numerically: the 12.1 Havoc rewrite dropped the whole "
            "`eb_aligned` alignment variable and made `eye_beam` unconditional."
        )
    else:
        lines.append(
            "> ⚠ **Staleness:** the simc `midnight` binary/branch can lag the live "
            "game patch (see `sims.md`). The commit date above is when this APL was "
            "generated — treat it, not the live patch, as the APL's currency. This is "
            "an APL fetcher only; it does not run a sim or produce DPS numbers."
        )
    lines.append("")
    lines.append("**Ready-to-paste `sources:` citation line:**")
    lines.append("```")
    lines.append(f"  - {cite}")
    lines.append("```")
    lines.append("")

    # ── Talents ───────────────────────────────────────────────────────
    lines.append("## Talents")
    lines.append("")
    if parsed["talents"]:
        for hash_ in parsed["talents"]:
            lines.append(f"- default: `{hash_}`")
    else:
        lines.append("- (no `talents=` hash in profile)")
    if parsed["profilesets"]:
        lines.append("")
        lines.append("**Profileset variants (build alternatives in-file):**")
        for name in parsed["profilesets"]:
            lines.append(f"- {name}")
    lines.append("")

    # ── Action lists ──────────────────────────────────────────────────
    lists = parsed["action_lists"]
    lines.append("## Action lists (`actions.*`)")
    lines.append("")
    lines.append(
        f"{len(lists)} list(s): "
        + ", ".join(f"`{n}`" for n in lists)
    )
    lines.append("")
    # Emit `default` and `precombat` first (the entry points), then the rest in
    # file order — these route into the hero-tree/target-count sublists.
    ordered = list(lists)
    for head in ("precombat", "default"):
        if head in ordered:
            ordered.remove(head)
            ordered.insert(0, head)
    for name in ordered:
        lines.append(f"### `actions.{name}`" if name != "default" else "### `actions` (top-level)")
        lines.append("")
        for action in lists[name]:
            lines.append(f"- `{action}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def list_names(text: str) -> dict[str, str]:
    """C++ local variable → the action-list name it was opened with.

    These are NOT the same, and assuming they are silently mislabels lists: monk opens
    `pre`/`def`/`ite` for "precombat"/"default"/"item_actions". The declaration is the
    only place the real name appears, so it is read rather than guessed.
    """
    return {m.group(1): m.group(2) for m in re.finditer(
        r'action_priority_list_t\*\s*(\w+)\s*=\s*\w+->get_action_priority_list\(\s*"([^"]+)"',
        text)}


def unwrap_actions(block: str, names: dict[str, str] | None = None) -> list[str]:
    """C++ `x->add_action("…")` calls → the plain `actions.<list>+=/…` lines they build."""
    names = names if names is not None else list_names(block)
    actions: list[str] = []
    for m in re.finditer(r'(\w+)->add_action\(\s*"((?:[^"\\]|\\.)*)"', block):
        var, action = m.group(1), m.group(2).replace('\\"', '"')
        listname = names.get(var) or ("default" if var in ("default_", "def") else var)
        actions.append(f"actions.{listname}+=/{action}")
    return actions


def module_specs(text: str) -> list[str]:
    """Every spec this class module carries, in file order.

    Two upstream shapes: explicit `//<spec>_apl_start` markers (most classes), and bare
    C++ `namespace <spec>` blocks (monk). PTR variants are excluded — `game-version.md`
    is the authority on what is live, and a `_ptr` block never describes it.
    """
    specs = list(dict.fromkeys(re.findall(r"//(\w+)_apl_start", text)))
    if not specs:
        specs = list(dict.fromkeys(re.findall(r"^namespace (\w+)\s*$", text, re.M)))
    return [s for s in specs if not s.endswith("_ptr")]


def module_actions(text: str, spec: str) -> list[str] | None:
    """One spec's priority list, whichever shape the class module uses."""
    # Declarations usually sit inside the block, but fall back to the file's when a
    # class opens its lists above the marker. Block-local wins on a collision.
    outer = list_names(text)
    block = re.search(rf"//{spec}_apl_start(.*?)//{spec}_apl_end", text, re.S)
    if block:
        body = block.group(1)
        return unwrap_actions(body, {**outer, **list_names(body)})

    # Namespace shape (monk). Prefer `live_apl` over `default_apl`, and never `ptr_apl`:
    # where a class ships both, `default_apl` dispatches and `live_apl` holds the list.
    ns = re.search(rf"^namespace {spec}\s*$(.*?)^}};?\s*//\s*namespace {spec}",
                   text, re.S | re.M)
    if not ns:
        return None
    for fn in ("live_apl", "default_apl"):
        m = re.search(rf"^void {fn}\(.*?$(.*?)(?=^void |\Z)", ns.group(1), re.S | re.M)
        if m:
            actions = unwrap_actions(m.group(1), {**outer, **list_names(m.group(1))})
            if actions:
                return actions
    return None


def pick_versioned(specs: list[str], spec: str) -> str | None:
    """Some specs ship as `<spec>_<major>_<minor>_<build>` blocks (evoker/augmentation
    carries both 12_1_0 and 12_0_5). Prefer the live patch's, else the highest."""
    cands = [s for s in specs if re.fullmatch(rf"{spec}_\d+(_\d+)*", s)]
    if not cands:
        return None
    live = live_patch_date()
    if live:
        want = live[0].replace(".", "_")
        for c in cands:
            if c[len(spec) + 1:].startswith(want):
                return c
    return max(cands, key=lambda s: [int(p) for p in s[len(spec) + 1:].split("_")])


def resolve_module(class_lower: str) -> tuple[str, str] | None:
    """(repo-relative path, text) of this class's APL module, or None if none exists."""
    for pattern in MODULE_CANDIDATES:
        path = pattern.format(c=class_lower)
        resp = _get(APL_RAW.format(path=path))
        if resp.status_code == 200:
            return path, resp.text
    return None


def resolve_inc(class_lower: str, spec_lower: str) -> tuple[str, str] | None:
    """Druid's shape: one `.inc` per spec, where the whole file is the block."""
    for pattern in INC_CANDIDATES:
        path = pattern.format(c=class_lower, s=spec_lower)
        resp = _get(APL_RAW.format(path=path))
        if resp.status_code == 200:
            return path, resp.text
    return None


_COMMIT_CACHE: dict[str, dict | None] = {}


def module_commit(path: str) -> dict | None:
    # One class module serves every spec of that class, so without this a 40-spec run
    # burns 40 calls against an unauthenticated 60/hr limit and starts returning None
    # — which would show up as phantom drift, since the pin is part of the file.
    if path in _COMMIT_CACHE:
        return _COMMIT_CACHE[path]
    _COMMIT_CACHE[path] = _module_commit(path)
    return _COMMIT_CACHE[path]


def _module_commit(path: str) -> dict | None:
    try:
        r = _get(API_MODULE_COMMITS.format(path=path))
        if r.ok and r.json():
            c = r.json()[0]
            return {"sha": c["sha"], "short": c["sha"][:7],
                    "date": c["commit"]["author"]["date"][:10]}
    except (requests.RequestException, KeyError, ValueError):
        pass
    return None


def resolve_profile(class_lower: str, spec_lower: str) -> tuple[str, list[str]] | None:
    """Last resort: the GENERATED MID1 profile. Some specs (enhancement) have a profile
    but no module block at all. Staleness matters most here — this is the shape that
    upstream regenerates per spec and sometimes forgets."""
    filename = profile_filename(class_lower, spec_lower, None)
    resp = _get(f"{RAW_BASE}/{filename}")
    if resp.status_code != 200:
        return None
    lists = parse_profile(resp.text)["action_lists"]
    actions = [f"actions.{name}+=/{a}" for name, acts in lists.items() for a in acts]
    return (f"profiles/MID1/{filename}", actions) if actions else None


def kb_specs(class_lower: str) -> list[str]:
    """The specs the KB has directories for — the authority on what we want to carry."""
    d = KB_CLASSES / class_lower.replace("_", "-")
    if not d.is_dir():
        return []
    return sorted(p.name.replace("-", "_") for p in d.iterdir() if p.is_dir())


def kb_path(class_lower: str, spec_lower: str) -> pathlib.Path:
    """simc uses underscores, the KB tree uses hyphens: `beast_mastery` → `beast-mastery`."""
    return (KB_CLASSES / class_lower.replace("_", "-")
            / spec_lower.replace("_", "-") / "simc-apl.md")


def _gen_block(src: str, spec: str, commit: dict | None, actions: list[str]) -> str:
    """The part `--check` compares. Everything volatile (a fetch date) stays outside it."""
    pin = (f"commit `{commit['short']}` ({commit['date']})" if commit
           else "commit unresolved (`--no-sha`, or the API was rate-limited)")
    return "\n".join([
        GEN_BEGIN,
        f"_Generated by `wowkb.simc --kb` from `{src}` (`{spec}` block), {pin}. "
        f"{len(actions)} actions. Do not hand-edit._",
        "",
        "```",
        *actions,
        "```",
        GEN_END,
    ])


def render_kb(class_lower: str, spec: str, src: str,
              commit: dict | None, actions: list[str]) -> str:
    """The citable KB artifact. `raw/` is gitignored and uncitable, which is exactly why
    the priority list used to get hand-copied into rotation.md — and then drift."""
    today = datetime.date.today().isoformat()
    live = live_patch_date()
    patch = live[0] if live else "unknown"
    url = APL_RAW.format(path=src)
    title_spec = spec.replace("_", " ").title()
    title_class = class_lower.replace("_", " ").title()
    source = f"  - {url}  # tier 1, simc APL source for {spec}"
    if commit:
        source += f", commit {commit['short']} ({commit['date']})"

    return "\n".join([
        "---",
        f"title: {title_spec} {title_class} — simc APL (generated)",
        f"patch: {patch}",
        f"fetched: {today}",
        f"reviewed: {today}",
        "sources:",
        source,
        "verbatim: true",
        "confidence: high",
        "---",
        "",
        f"# {title_spec} {title_class} — the simc priority list",
        "",
        "The Tier-1 action priority list, taken from the **class module** the MID1 profiles",
        "are generated from. Upstream regenerates profiles per spec and sometimes never gets",
        "to one, so the module is what actually tracks the live patch.",
        "",
        "**`rotation.md` augments this file — it does not restate it.** The list lives here so",
        "there is exactly one copy; a hand-transcribed second copy is what drifts.",
        "",
        "It carries no `talents=` string, no consumables and no profileset variants — those",
        "exist only in a generated profile, so a build recommendation still needs one.",
        "",
        _gen_block(src, spec, commit, actions),
        "",
    ])


def gen_actions(block: str | None) -> list[str] | None:
    """The action lines out of a generated block.

    `--check` compares THESE, not the whole block: the provenance line carries a commit
    pin that can fail to resolve when the unauthenticated API rate-limits, and a check
    that fails on an unresolved pin would cry wolf. The priority list is the contract;
    a pin-only change re-stamps on the next write without failing anything.
    """
    if block is None:
        return None
    m = re.search(r"```\n(.*?)```", block, re.S)
    return m.group(1).splitlines() if m else None


def read_gen_block(path: pathlib.Path) -> str | None:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    m = re.search(re.escape(GEN_BEGIN) + r".*?" + re.escape(GEN_END), text, re.S)
    return m.group(0) if m else None


def fetch_module(class_token: str, spec_token: str, want_sha: bool) -> None:
    """The APL SOURCE for a class, sliced to one spec — the fallback when a profile is stale.

    `apl_<class>.cpp` holds every spec's list between `//<spec>_apl_start` and
    `//<spec>_apl_end` markers, as C++ `add_action( "..." )` calls. This extracts the
    named spec's block and unwraps it back into plain APL lines, so the output reads
    like a profile's `actions` section and can be distilled the same way.
    """
    cls = _titleseg(class_token, CLASS_ALIASES).lower()
    spec = _titleseg(spec_token, SPEC_ALIASES).lower()
    url = APL_MODULE.format(class_lower=cls)

    resp = _get(url)
    if resp.status_code == 404:
        sys.exit(f"error: no APL module for {cls!r} at {url} (HTTP 404)")
    resp.raise_for_status()
    text = resp.text

    actions = module_actions(text, spec)
    if actions is None:
        found = ", ".join(module_specs(text)) or "none"
        sys.exit(f"error: no //{spec}_apl_start block in {url}\n  blocks present: {found}")

    commit = module_commit(f"apl_{cls}.cpp") if want_sha else None

    today = datetime.date.today().isoformat()
    name = f"apl_{cls}_{spec}"
    head = [
        f"# simc APL SOURCE — {cls} / {spec}",
        "",
        f"- source: {url}  (SimulationCraft `midnight` branch, Tier 1)",
        f"- extracted block: `//{spec}_apl_start` … `//{spec}_apl_end`",
    ]
    if commit:
        head.append(f"- pinned commit: `{commit['short']}` ({commit['sha']}), "
                    f"committed {commit['date']}")
    head += [
        f"- fetched: {today}",
        f"- actions: {len(actions)}",
        "",
        "> **This is the APL the profiles are GENERATED FROM**, taken directly because the "
        "generated profile for this spec lagged the live patch. It is the same priority list "
        "a regenerated profile would carry, without waiting for upstream to regenerate it. "
        "It carries no `talents=` string, no consumables and no profileset variants — those "
        "live only in a profile, so a build recommendation still needs one.",
        "",
        "```",
    ] + actions + ["```", ""]

    raw_path = save_raw("simc", f"{name}.cpp", text)
    digest_path = save_raw("simc", f"{name}.digest.md", "\n".join(head))
    print(raw_path)
    print(digest_path)
    if commit:
        stale = staleness(commit)
        print(f"  pinned {commit['short']} {commit['date']} — "
              + ("STILL STALE" if stale else "postdates the live patch"))
        # Same contract as `fetch()`: a stale APL must not be consumable by a script
        # in silence. The module is the SOURCE, so if even it predates the patch,
        # nothing upstream describes the live game yet.
        if stale:
            days, patch, live_date = stale
            print(
                f"\n❌ STALE: this APL SOURCE was committed {commit['date']} — {days} days "
                f"BEFORE {patch} went live ({live_date}).\n"
                f"   Upstream has not touched {cls}'s APL for this patch.\n"
                f"   Do not cite it as the {patch} rotation.",
                file=sys.stderr,
            )
            sys.exit(3)


def sync_kb(class_tokens: list[str], spec_token: str | None,
            want_sha: bool, check_only: bool) -> int:
    """Write (or verify) `knowledge/classes/<class>/<spec>/simc-apl.md` per spec.

    One class module holds every spec of that class, so a whole class costs ONE fetch.
    Returns a process exit code: 1 if anything drifted, is missing, or is stale.
    """
    drift: list[str] = []
    stale_srcs: list[str] = []
    missing: list[str] = []
    wrote = checked = 0

    for token in class_tokens:
        cls = _titleseg(token, CLASS_ALIASES).lower()
        resolved = resolve_module(cls)
        text = resolved[1] if resolved else ""
        module_path = resolved[0] if resolved else None

        # Which specs to emit is the KB's call, not upstream's: the KB tree is the set
        # we maintain, and upstream carries PTR and dated variants we do not want.
        wanted = [_titleseg(spec_token, SPEC_ALIASES).lower()] if spec_token else kb_specs(cls)
        in_module = set(module_specs(text))

        for spec in wanted:
            path = kb_path(cls, spec)
            src, actions = None, None

            block = spec if spec in in_module else pick_versioned(sorted(in_module), spec)
            if block:
                src, actions = module_path, module_actions(text, block)
            else:
                # Not in the class module — try the per-spec `.inc` shape (druid),
                # then the generated MID1 profile (enhancement has only that).
                inc = resolve_inc(cls, spec)
                if inc:
                    src, actions = inc[0], unwrap_actions(inc[1])
                else:
                    prof = resolve_profile(cls, spec)
                    if prof:
                        src, actions = prof

            if not actions:
                missing.append(f"{cls}/{spec}")
                continue

            commit = module_commit(src) if want_sha else None
            stale = staleness(commit)
            if stale:
                entry = f"{src} ({commit['date']}, {stale[0]}d before {stale[1]})"
                if entry not in stale_srcs:
                    stale_srcs.append(entry)

            fresh = _gen_block(src, block or spec, commit, actions)
            current = read_gen_block(path)
            checked += 1
            if current == fresh:
                continue
            rel = path.relative_to(REPO)
            if check_only:
                if gen_actions(current) == actions:
                    continue  # pin-only difference: re-stamps on write, not drift
                drift.append(f"{rel} — {'missing' if current is None else 'differs from upstream'}")
                continue
            path.write_text(render_kb(cls, spec, src, commit, actions), encoding="utf-8")
            wrote += 1
            print(f"  wrote {rel} ({len(actions)} actions)")

    if check_only:
        print(f"\nchecked {checked} spec APL file(s)")
        for d in drift:
            print(f"  ❌ {d}")
    else:
        print(f"\n{wrote} written, {checked - wrote} already current")

    if missing:
        # Not a failure: upstream genuinely has no APL for some specs (healers mostly).
        # Reported so "this spec has no simc-apl.md" is a known absence, not a mystery.
        print(f"\nno upstream APL for {len(missing)} spec(s): " + ", ".join(missing))

    if stale_srcs:
        print("\n⚠ APL SOURCE predates the live patch — upstream has not retuned these:",
              file=sys.stderr)
        for s in stale_srcs:
            print(f"  {s}", file=sys.stderr)

    return 1 if (drift or stale_srcs) else 0


def fetch(class_token: str, spec_token: str, variant: str | None, want_sha: bool) -> None:
    filename = profile_filename(class_token, spec_token, variant)
    url = f"{RAW_BASE}/{filename}"

    resp = _get(url)
    if resp.status_code == 404:
        avail = ", ".join(list_profiles())
        sys.exit(
            f"error: no MID1 profile named {filename!r} (HTTP 404).\n"
            f"Available profiles:\n  {avail}\n"
            "Pass --variant for a hero-tree file, or check --list."
        )
    resp.raise_for_status()
    text = resp.text

    raw_path = save_raw("simc", filename, text)
    commit = resolve_commit(filename) if want_sha else None
    parsed = parse_profile(text)
    digest = render_digest(filename, url, commit, parsed)
    digest_path = save_raw("simc", f"{filename}.digest.md", digest)

    print(raw_path)
    print(digest_path)

    # Loud on stdout as well as in the digest: the digest is read later by whoever
    # distills, but the person who ran the fetch is the one who can go get the real
    # source. Non-zero exit so a script cannot consume a stale APL silently.
    stale = staleness(commit)
    if stale:
        days, patch, live_date = stale
        cls = _titleseg(class_token, CLASS_ALIASES).lower()
        print(
            f"\n❌ STALE: this APL was generated {commit['date']} — {days} days BEFORE "
            f"{patch} went live ({live_date}).\n"
            f"   Upstream regenerates profiles per spec and has not regenerated this one.\n"
            f"   The current APL source is:\n"
            f"     {APL_MODULE.format(class_lower=cls)}\n"
            f"   Read that instead, and do not cite this file as the {patch} rotation.",
            file=sys.stderr,
        )
        sys.exit(3)


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.simc", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("class_token", nargs="?", help="class (e.g. warlock, dh, death_knight)")
    p.add_argument("spec_token", nargs="?", help="spec (e.g. demonology, demo, vengeance)")
    p.add_argument("--variant", help="hero-tree/build variant filename segment (e.g. Aldrachi_Reaver, Hellcaller)")
    p.add_argument("--list", action="store_true", help="enumerate all MID1 profiles and exit")
    p.add_argument("--no-sha", action="store_true", help="skip the GitHub commits API (raw fetch only)")
    p.add_argument("--module", action="store_true",
                   help="fetch the APL SOURCE (engine/class_modules/apl/apl_<class>.cpp) instead of "
                        "the generated profile — use when the profile predates the live patch")
    p.add_argument("--kb", action="store_true",
                   help="write the citable artifact knowledge/classes/<class>/<spec>/simc-apl.md "
                        "(from the APL source) instead of the raw/ digest")
    p.add_argument("--all", action="store_true",
                   help="with --kb: every spec of the named class, or every class when none is named")
    p.add_argument("--check", action="store_true",
                   help="with --kb: verify the committed simc-apl.md files against upstream; "
                        "write nothing, exit 1 on drift or a stale APL source")
    args = p.parse_args()

    if args.list:
        for name in list_profiles():
            print(name)
        return

    if args.kb or args.check:
        if args.class_token:
            classes = [args.class_token]
        elif args.all or args.check:
            classes = sorted(set(CLASS_ALIASES.values()))
        else:
            p.error("--kb needs a class, or --all for every class")
        if args.spec_token and args.all:
            p.error("--all takes a class, not a spec")
        sys.exit(sync_kb(classes, args.spec_token,
                         want_sha=not args.no_sha, check_only=args.check))

    if not args.class_token or not args.spec_token:
        p.error("class and spec are required (or use --list)")
    if args.module:
        fetch_module(args.class_token, args.spec_token, want_sha=not args.no_sha)
        return
    fetch(args.class_token, args.spec_token, args.variant, want_sha=not args.no_sha)


if __name__ == "__main__":
    main()
