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
APL_MODULE = (
    "https://raw.githubusercontent.com/simulationcraft/simc/midnight/"
    "engine/class_modules/apl/apl_{class_lower}.cpp"
)
API_MODULE_COMMITS = (
    "https://api.github.com/repos/simulationcraft/simc/commits"
    "?sha=midnight&path=engine/class_modules/apl/apl_{class_lower}.cpp&per_page=1"
)

# `knowledge/_meta/game-version.md` is the single source of truth for what is live.
GAME_VERSION = pathlib.Path(__file__).resolve().parents[2] / "knowledge" / "_meta" / "game-version.md"


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

    block = re.search(rf"//{spec}_apl_start(.*?)//{spec}_apl_end", text, re.S)
    if not block:
        found = ", ".join(sorted(set(re.findall(r"//(\w+)_apl_start", text)))) or "none"
        sys.exit(f"error: no //{spec}_apl_start block in {url}\n  blocks present: {found}")

    actions: list[str] = []
    for m in re.finditer(r'(\w+)->add_action\(\s*"((?:[^"\\]|\\.)*)"', block.group(1)):
        listname, action = m.group(1), m.group(2).replace('\\"', '"')
        listname = "precombat" if listname == "precombat" else (
            "default" if listname in ("default_", "default") else listname)
        actions.append(f"actions.{listname}+=/{action}")

    commit = None
    if want_sha:
        try:
            r = _get(API_MODULE_COMMITS.format(class_lower=cls))
            if r.ok and r.json():
                c = r.json()[0]
                commit = {"sha": c["sha"], "short": c["sha"][:7],
                          "date": c["commit"]["author"]["date"][:10]}
        except Exception:
            commit = None

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
    args = p.parse_args()

    if args.list:
        for name in list_profiles():
            print(name)
        return

    if not args.class_token or not args.spec_token:
        p.error("class and spec are required (or use --list)")
    if args.module:
        fetch_module(args.class_token, args.spec_token, want_sha=not args.no_sha)
        return
    fetch(args.class_token, args.spec_token, args.variant, want_sha=not args.no_sha)


if __name__ == "__main__":
    main()
