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

Usage:
    uv run python -m wowkb.simc --list                       # enumerate all MID1 profiles (discover variants)
    uv run python -m wowkb.simc warlock demonology           # base profile → raw/simc/<file>.simc + .digest.md
    uv run python -m wowkb.simc dh vengeance --variant Aldrachi_Reaver   # a hero-tree variant profile
    uv run python -m wowkb.simc warlock affliction --no-sha   # skip the commits API (raw only)

Outputs (both printed):
    raw/simc/<file>.simc         # verbatim fetch cache (gitignored, like maxroll/youtube)
    raw/simc/<file>.digest.md    # provenance header + talents + grouped actions.*
"""

import argparse
import datetime
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


def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.simc", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("class_token", nargs="?", help="class (e.g. warlock, dh, death_knight)")
    p.add_argument("spec_token", nargs="?", help="spec (e.g. demonology, demo, vengeance)")
    p.add_argument("--variant", help="hero-tree/build variant filename segment (e.g. Aldrachi_Reaver, Hellcaller)")
    p.add_argument("--list", action="store_true", help="enumerate all MID1 profiles and exit")
    p.add_argument("--no-sha", action="store_true", help="skip the GitHub commits API (raw fetch only)")
    args = p.parse_args()

    if args.list:
        for name in list_profiles():
            print(name)
        return

    if not args.class_token or not args.spec_token:
        p.error("class and spec are required (or use --list)")
    fetch(args.class_token, args.spec_token, args.variant, want_sha=not args.no_sha)


if __name__ == "__main__":
    main()
