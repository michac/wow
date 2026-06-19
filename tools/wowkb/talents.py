"""Build a local, greppable talent-tree database for the current patch.

Hybrid source (see knowledge/classes/_talents/README.md):
  * Blizzard Game Data API talent-tree endpoints = primary (Tier-1): nodes
    grouped into class / spec / hero per spec, with spell names resolved.
  * wago.tools Trait* DB2 CSVs = required: cross-check + the two columns the
    Game Data API does not expose (export-string node ordering `serial_order`
    and choice-entry `choice_index`). DB2 also drives the PTR-only path.

Outputs (regenerated each patch day):
  * knowledge/classes/_talents/all-talents.tsv   one row per talent entry
  * knowledge/classes/_talents/trees.tsv         one row per class/spec/hero tree
  * knowledge/classes/<class>/<spec>/talents.md   human-readable per spec
  * knowledge/classes/<class>/<spec>/talents.json graph-shaped, for tooling/app

Usage:
    uv run python -m wowkb.talents fetch                 # live: API + wago @ API build
    uv run python -m wowkb.talents fetch --build 12.0.7.68999   # PTR: DB2-only
    uv run python -m wowkb.talents enrich                # icon URL + desc per spell
    uv run python -m wowkb.talents build
    uv run python -m wowkb.talents verify
"""

import argparse
import csv
import json
import os
import sys
import time
from collections import defaultdict

import requests

from . import blizzard, wago
from ._common import RAW, ROOT, save_raw

# ── paths ────────────────────────────────────────────────────────────────────
CLASSES_DIR = ROOT / "knowledge" / "classes"
TALENTS_DIR = CLASSES_DIR / "_talents"
BLIZZ_RAW = RAW / "blizzard"
MANIFEST = RAW / "talents-manifest.json"
# Stage A enrichment lookup: {spell_id(str): {"icon": url|null, "desc": str}}.
# Produced by `enrich`, consumed by `build` to inline icon+desc onto each entry.
ENRICH_CACHE = RAW / "spell-enrichment.json"

# DB2 tables we need at the pinned build.
WAGO_TABLES = [
    "TraitTree", "TraitNode", "TraitNodeXTraitNodeEntry", "TraitNodeEntry",
    "TraitDefinition", "TraitSubTree", "TraitNodeGroup", "TraitNodeGroupXTraitNode",
    "TraitCond", "TraitNodeXTraitCond", "TraitTreeLoadout", "TraitTreeLoadoutEntry",
    "TraitTreeXTraitCurrency", "TraitCurrencySource", "ChrSpecialization",
    "ChrClasses", "SpellName",
]

# Midnight Season 1 level cap. Budgets (TraitCurrencySource) are resolved at this
# level; bump on the expansion's level-cap patch alongside game-version.md.
LEVEL_CAP = 90

TSV_COLUMNS = [
    "class", "class_id", "spec", "spec_id", "tree", "hero_tree", "node_id",
    "node_type", "entry_id", "talent", "spell_id", "max_ranks", "req_points",
    "row", "col", "choice_group", "prereq_node_ids", "serial_order", "choice_index",
]
TREES_COLUMNS = ["tree_kind", "class", "tree_id", "name", "specs", "node_count"]
TREE_ORDER = {"class": 0, "spec": 1, "hero": 2}


# ── small helpers ──────────────────────────────────────────────────────────────
def slug(name: str) -> str:
    """Directory-style slug: 'Beast Mastery' -> 'beast-mastery', 'Death Knight' -> 'death-knight'."""
    return name.lower().replace("'", "").replace(" ", "-")


def load_wago(table: str, build: str) -> list[dict]:
    path = RAW / "wago" / f"{table}-{build}.csv"
    if not path.exists():
        sys.exit(f"error: missing {path} — run `talents fetch` first")
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def _atomic_write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, path)


def _build_from_namespace(href: str) -> str:
    """'.../?namespace=static-12.0.7_67808-us' -> '12.0.7.67808'."""
    ns = href.split("namespace=", 1)[1].split("&", 1)[0]
    core = ns.split("-", 1)[1].rsplit("-", 1)[0]  # 'static-12.0.7_67808-us' -> '12.0.7_67808'
    return core.replace("_", ".")


# ── fetch ──────────────────────────────────────────────────────────────────────
def _href_segment(href: str, after: str) -> int:
    """Pull the numeric id following `after` in a Game Data API href."""
    parts = href.split("?", 1)[0].rstrip("/").split("/")
    return int(parts[parts.index(after) + 1])


def fetch(build: str | None, patch: str | None) -> None:
    """Acquire raw inputs. With --build => DB2-only (PTR). Else API live + wago @ API build."""
    db2_only = build is not None
    specs_meta = []
    api_build = None

    if not db2_only:
        BLIZZ_RAW.mkdir(parents=True, exist_ok=True)
        index = blizzard.get("/data/wow/playable-specialization/index")
        api_build = _build_from_namespace(index["_links"]["self"]["href"])
        spec_ids = sorted(s["id"] for s in index["character_specializations"])
        print(f"API build {api_build}; {len(spec_ids)} specs")
        for sid in spec_ids:
            spec = blizzard.get(f"/data/wow/playable-specialization/{sid}")
            save_raw("blizzard", f"spec-{sid}.json", json.dumps(spec, indent=2))
            tree_ref = spec.get("spec_talent_tree")
            if not tree_ref:
                continue  # pet / initial specs without a talent tree
            tree_id = _href_segment(tree_ref["key"]["href"], "talent-tree")
            tree = blizzard.get(
                f"/data/wow/talent-tree/{tree_id}/playable-specialization/{sid}"
            )
            save_raw("blizzard", f"talent-tree-{tree_id}-{sid}.json", json.dumps(tree, indent=2))
            specs_meta.append({
                "spec_id": sid,
                "tree_id": tree_id,
                "class_id": spec["playable_class"]["id"],
                "class": slug(spec["playable_class"]["name"]),
                "class_name": spec["playable_class"]["name"],
                "spec": slug(spec["name"]),
                "spec_name": spec["name"],
            })
            print(f"  {specs_meta[-1]['class']:13} {specs_meta[-1]['spec']:16} tree {tree_id}")

    wago_build = build or api_build
    print(f"downloading {len(WAGO_TABLES)} DB2 tables @ {wago_build} ...")
    for table in WAGO_TABLES:
        wago.download(table, wago_build)

    patch = patch or (wago_build.rsplit(".", 1)[0] if wago_build else "")
    manifest = {
        "mode": "db2" if db2_only else "api",
        "patch": patch,
        "api_build": api_build,
        "wago_build": wago_build,
        "specs": specs_meta,
    }
    _atomic_write(MANIFEST, json.dumps(manifest, indent=2))
    print(f"wrote {MANIFEST}")


# ── DB2 indexes (serial_order, choice_index, entry ids, cross-check) ────────────
class Db2Index:
    def __init__(self, build: str):
        self.build = build
        defn = {r["ID"]: r["SpellID"] for r in load_wago("TraitDefinition", build)}
        entry = {
            r["ID"]: (r["TraitDefinitionID"], r["MaxRanks"], r["TraitSubTreeID"])
            for r in load_wago("TraitNodeEntry", build)
        }
        # entry_id -> hero subtree id (0 outside hero trees). Drives the export
        # string's hero-selector (type-3) node, whose choice index picks a subtree.
        self.entry_subtree: dict[str, str] = {eid: e[2] for eid, e in entry.items()}
        # node_id -> [(entry_id, choice_index, spell_id, max_ranks), ...]
        # _Index is a position key (0/100/200…), not 0/1 — the export-string choice
        # index is the entry's ordinal once sorted by _Index, so we enumerate.
        raw: dict[str, list] = defaultdict(list)
        for r in load_wago("TraitNodeXTraitNodeEntry", build):
            eid = r["TraitNodeEntryID"]
            def_id, max_ranks, _ = entry.get(eid, ("", "", ""))
            raw[r["TraitNodeID"]].append((int(r["_Index"]), eid, defn.get(def_id, ""), max_ranks))
        self.node_entries: dict[str, list] = {}
        for nid, entries in raw.items():
            entries.sort(key=lambda e: e[0])
            self.node_entries[nid] = [
                (eid, ordinal, spell, mr) for ordinal, (_, eid, spell, mr) in enumerate(entries)
            ]
        # tree_id -> {node_id: serial_order} (ascending node id == export-string walk).
        # The serial walk is class-wide: every node in the tree (all specs, every
        # hero sub-tree, the type-3 selector/grant nodes the API omits) gets a slot.
        tree_nodes: dict[str, list[int]] = defaultdict(list)
        self.node_tree: dict[int, str] = {}
        self.node_type: dict[int, str] = {}
        for r in load_wago("TraitNode", build):
            nid = int(r["ID"])
            tree_nodes[r["TraitTreeID"]].append(nid)
            self.node_tree[nid] = r["TraitTreeID"]
            self.node_type[nid] = r["Type"]
        self.serial: dict[str, dict[int, int]] = {}
        self.tree_node_count: dict[str, int] = {}
        for tid, nids in tree_nodes.items():
            nids.sort()
            self.serial[tid] = {nid: i for i, nid in enumerate(nids)}
            self.tree_node_count[tid] = len(nids)

        # hero sub-tree names (id -> name) and per-tree name->id, for the selector.
        self.subtree_name: dict[str, str] = {}
        self.subtree_by_tree: dict[str, dict[str, str]] = defaultdict(dict)
        for r in load_wago("TraitSubTree", build):
            self.subtree_name[r["ID"]] = r["Name_lang"]
            self.subtree_by_tree[r["TraitTreeID"]][r["Name_lang"]] = r["ID"]

        # Auto-granted node ids: CondType==2 (granted), >=1 free rank, all-spec
        # (SpecSetID==0). Covers class-tree free talents (e.g. Soul Leech). The
        # export string marks these selected-but-not-purchased. Spec-set-scoped
        # grants are skipped (SpecSetMember is not fetched at this build); hero
        # sub-tree keystone grants are derived separately (see _codec_meta).
        cond_by_id = {r["ID"]: r for r in load_wago("TraitCond", build)}
        self.granted_cond: set[int] = set()
        for r in load_wago("TraitNodeXTraitCond", build):
            c = cond_by_id.get(r["TraitCondID"])
            if not c:
                continue
            if (c["CondType"] == "2" and int(c.get("GrantedRanks") or 0) >= 1
                    and c.get("SpecSetID") == "0"):
                self.granted_cond.add(int(r["TraitNodeID"]))

        # ── point budgets (Stage A′) ────────────────────────────────────────
        # tree_id -> [currency_id ...] ordered by _Index. The class talent tree
        # carries one currency per tree-kind: index 1 = class, 2 = spec, 3+ =
        # the (global, equal) hero currencies. The currencies are shared across
        # all classes — every tree maps to the same set.
        tree_cur: dict[str, list[tuple[int, str]]] = defaultdict(list)
        for r in load_wago("TraitTreeXTraitCurrency", build):
            tree_cur[r["TraitTreeID"]].append((int(r["_Index"]), r["TraitCurrencyID"]))
        self.tree_currencies: dict[str, list[str]] = {
            t: [c for _, c in sorted(v)] for t, v in tree_cur.items()
        }
        # currency_id -> [(minLevel, amount) ...]; budget at a level = sum of the
        # amounts granted at or below it. (Quest/achievement rows carry amount 0.)
        self.currency_grants: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for r in load_wago("TraitCurrencySource", build):
            self.currency_grants[r["TraitCurrencyID"]].append(
                (int(r["PlayerLevel"] or 0), int(r["Amount"] or 0))
            )

        # starter-loadout point totals per tree, for the budget cross-check.
        loadout_tree = {r["ID"]: r["TraitTreeID"] for r in load_wago("TraitTreeLoadout", build)}
        loadout_pts: dict[str, int] = defaultdict(int)
        for r in load_wago("TraitTreeLoadoutEntry", build):
            loadout_pts[r["TraitTreeLoadoutID"]] += int(r["NumPoints"] or 0)
        self.loadout_max: dict[str, int] = defaultdict(int)
        for lid, pts in loadout_pts.items():
            t = loadout_tree.get(lid)
            if t:
                self.loadout_max[t] = max(self.loadout_max[t], pts)

    def currency_points(self, currency_id: str, level: int) -> int:
        """Points a currency grants by `level` = sum of its at-or-below grants."""
        return sum(a for lvl, a in self.currency_grants.get(currency_id, []) if lvl <= level)

    def budgets(self, tree_id: int, level: int = LEVEL_CAP) -> dict:
        """Per-tree-kind point budget at `level` from TraitCurrencySource.

        Returns {class, spec, hero}. Hero currencies are equal across the spec's
        usable hero trees, so the first is representative.
        """
        curs = self.tree_currencies.get(str(tree_id), [])
        pts = [self.currency_points(c, level) for c in curs]
        return {
            "class": pts[0] if len(pts) > 0 else 0,
            "spec": pts[1] if len(pts) > 1 else 0,
            "hero": pts[2] if len(pts) > 2 else 0,
        }

    def serial_order(self, tree_id: int, node_id: int):
        return self.serial.get(str(tree_id), {}).get(node_id, "")

    def entry_lookup(self, node_id: int):
        return self.node_entries.get(str(node_id), [])

    def selector_node(self, tree_id: int, subtree_ids: set[str]):
        """The type-3 hero-selector node whose choice subtrees == `subtree_ids`.

        Returns (node_id, [subtree_id ...] ordered by choice index) or (None, []).
        Each spec has its own selector listing exactly its two usable hero trees.
        """
        tid = str(tree_id)
        for nid, ntype in self.node_type.items():
            if ntype != "3" or self.node_tree.get(nid) != tid:
                continue
            ents = self.node_entries.get(str(nid), [])  # (eid, ordinal, spell, mr)
            subs = [self.entry_subtree.get(eid, "0") for eid, *_ in ents]
            if len(subs) == len(subtree_ids) and set(subs) == subtree_ids:
                return nid, subs
        return None, []


# ── API parse -> model ──────────────────────────────────────────────────────────
def _entries_from_api_node(node: dict, db2: Db2Index):
    """Return list of entry dicts for an API node, attaching DB2 entry_id/choice_index."""
    db2_entries = db2.entry_lookup(node["id"])
    by_spell = {sp: (eid, idx, mr) for (eid, idx, sp, mr) in db2_entries}

    options = []  # (talent_name, spell_id, max_ranks)
    ranks = node.get("ranks", [])
    if node["node_type"]["type"] == "CHOICE":
        tips = next((r["choice_of_tooltips"] for r in ranks if "choice_of_tooltips" in r), [])
        for t in tips:
            options.append((t["talent"]["name"], t["spell_tooltip"]["spell"]["id"], 1))
    else:
        tip = next((r["tooltip"] for r in ranks if "tooltip" in r), None)
        if tip:
            options.append(
                (tip["talent"]["name"], tip["spell_tooltip"]["spell"]["id"], len(ranks))
            )

    out = []
    for order, (talent, spell_id, max_ranks) in enumerate(options):
        eid, idx, db2_mr = by_spell.get(str(spell_id), ("", order, None))
        out.append({
            "entry_id": eid,
            "talent": talent,
            "spell_id": spell_id,
            "max_ranks": db2_mr or max_ranks,
            "choice_index": idx,
        })
    return out


def _req_points(row: int, is_class: bool, restriction_lines: list) -> int:
    pts = [
        int(rl["required_points"])
        for rl in restriction_lines
        if bool(rl.get("is_for_class")) == is_class and row > rl.get("restricted_row", 1e9)
    ]
    return max(pts) if pts else 0


def _api_node(node: dict, db2: Db2Index, tree_id: int, kind: str, restriction_lines):
    return {
        "node_id": node["id"],
        "node_type": node["node_type"]["type"],
        "row": node.get("display_row", ""),
        "col": node.get("display_col", ""),
        "x": node.get("raw_position_x", ""),
        "y": node.get("raw_position_y", ""),
        "serial_order": db2.serial_order(tree_id, node["id"]),
        # Hero trees have no points-spent gate (they gate by level 71 + prereq
        # edges only). restriction_lines only describe class/spec gates; matching
        # hero nodes against them is wrong — they'd inherit the spec tree's lines
        # (is_for_class False) and pick up spurious 8/20 reqs that exceed the
        # ~11-point hero budget and deadlock the entry node.
        "req_points": 0 if kind == "hero" else _req_points(
            node.get("display_row", 0), kind == "class", restriction_lines
        ),
        "prereq_node_ids": node.get("locked_by", []),
        "entries": _entries_from_api_node(node, db2),
    }


def parse_api(manifest: dict, db2: Db2Index) -> list[dict]:
    specs = []
    for m in manifest["specs"]:
        path = BLIZZ_RAW / f"talent-tree-{m['tree_id']}-{m['spec_id']}.json"
        tree = json.loads(path.read_text())
        rl = tree.get("restriction_lines", [])
        tid = m["tree_id"]
        # The tree endpoint lists every class hero tree and duplicates their nodes
        # into spec_talent_nodes. The *spec* endpoint names the 2 trees this spec
        # may use — but can include unreleased "[DNT]" placeholders, so we also
        # require the tree to be populated (its nodes overlap spec_talent_nodes).
        spec_doc = json.loads((BLIZZ_RAW / f"spec-{m['spec_id']}.json").read_text())
        usable_names = {h["name"] for h in spec_doc.get("hero_talent_trees", [])}
        spec_ids = {n["id"] for n in tree["spec_talent_nodes"]}
        all_hero_ids = {n["id"] for h in tree.get("hero_talent_trees", []) for n in h["hero_talent_nodes"]}
        usable_heroes = [
            h for h in tree.get("hero_talent_trees", [])
            if h["name"] in usable_names and {n["id"] for n in h["hero_talent_nodes"]} & spec_ids
        ]
        def build_nodes(api_nodes, kind, exclude=frozenset()):
            # Drop nodes that yield no real talent entry (placeholder/selector
            # CHOICE nodes the API and DB2 both leave empty).
            out = [_api_node(n, db2, tid, kind, rl) for n in api_nodes if n["id"] not in exclude]
            return [n for n in out if n["entries"]]

        sections = {
            "class": build_nodes(tree["class_talent_nodes"], "class", all_hero_ids | spec_ids),
            "spec": build_nodes(tree["spec_talent_nodes"], "spec", all_hero_ids),
            "hero": [(h["name"], build_nodes(h["hero_talent_nodes"], "hero")) for h in usable_heroes],
        }
        specs.append({**m, "sections": sections})
    return specs


# ── emit: TSV ────────────────────────────────────────────────────────────────
def _rows_for_spec(s: dict):
    for kind in ("class", "spec", "hero"):
        groups = [("", s["sections"][kind])] if kind != "hero" else s["sections"]["hero"]
        for hero_name, nodes in groups:
            for node in nodes:
                choice_group = node["node_id"] if node["node_type"] == "CHOICE" else ""
                for e in node["entries"]:
                    yield {
                        "class": s["class"], "class_id": s["class_id"],
                        "spec": s["spec"], "spec_id": s["spec_id"],
                        "tree": kind, "hero_tree": hero_name,
                        "node_id": node["node_id"], "node_type": node["node_type"],
                        "entry_id": e["entry_id"], "talent": e["talent"],
                        "spell_id": e["spell_id"], "max_ranks": e["max_ranks"],
                        "req_points": node["req_points"] or "",
                        "row": node["row"], "col": node["col"],
                        "choice_group": choice_group,
                        "prereq_node_ids": ",".join(str(p) for p in node["prereq_node_ids"]),
                        "serial_order": node["serial_order"],
                        "choice_index": e["choice_index"],
                    }


def write_tsv(specs: list[dict]) -> None:
    rows = [r for s in specs for r in _rows_for_spec(s)]
    rows.sort(key=lambda r: (
        r["class"], r["spec"], TREE_ORDER[r["tree"]], r["hero_tree"],
        int(r["row"] or 0), int(r["col"] or 0), int(r["node_id"]), int(r["choice_index"] or 0),
    ))
    lines = ["\t".join(TSV_COLUMNS)]
    lines += ["\t".join(str(r[c]) for c in TSV_COLUMNS) for r in rows]
    _atomic_write(TALENTS_DIR / "all-talents.tsv", "\n".join(lines) + "\n")
    print(f"wrote all-talents.tsv ({len(rows)} rows)")


def write_trees_tsv(specs: list[dict]) -> None:
    rows = []
    by_class: dict[str, list[dict]] = defaultdict(list)
    for s in specs:
        by_class[s["class"]].append(s)
    for cls, members in sorted(by_class.items()):
        members.sort(key=lambda s: s["spec"])
        tid = members[0]["tree_id"]
        spec_slugs = ",".join(m["spec"] for m in members)
        # class tree (shared): distinct class node count from first member
        rows.append(["class", cls, tid, cls, spec_slugs, len(members[0]["sections"]["class"])])
        for m in members:
            rows.append(["spec", cls, tid, m["spec"], m["spec"], len(m["sections"]["spec"])])
        hero_specs: dict[str, list[str]] = defaultdict(list)
        hero_count: dict[str, int] = {}
        for m in members:
            for hero_name, nodes in m["sections"]["hero"]:
                hero_specs[hero_name].append(m["spec"])
                hero_count[hero_name] = len(nodes)
        for hero_name in sorted(hero_specs):
            rows.append(["hero", cls, tid, hero_name,
                         ",".join(hero_specs[hero_name]), hero_count[hero_name]])
    lines = ["\t".join(TREES_COLUMNS)]
    lines += ["\t".join(str(c) for c in r) for r in rows]
    _atomic_write(TALENTS_DIR / "trees.tsv", "\n".join(lines) + "\n")
    print(f"wrote trees.tsv ({len(rows)} rows)")


# ── emit: per-spec markdown + json ──────────────────────────────────────────────
def _md_table(nodes: list[dict]) -> str:
    head = "| Talent | Spell ID | Ranks | Type | Row,Col | Req pts | Prereqs |\n"
    head += "|---|---|---|---|---|---|---|\n"
    body = []
    for n in sorted(nodes, key=lambda n: (int(n["row"] or 0), int(n["col"] or 0))):
        talents = " / ".join(e["talent"] for e in n["entries"])
        spells = " / ".join(str(e["spell_id"]) for e in n["entries"])
        ranks = "/".join(str(e["max_ranks"]) for e in n["entries"])
        prereqs = ",".join(str(p) for p in n["prereq_node_ids"]) or "—"
        body.append(f"| {talents} | {spells} | {ranks} | {n['node_type']} | "
                    f"{n['row']},{n['col']} | {n['req_points'] or '—'} | {prereqs} |")
    return head + "\n".join(body) + "\n"


def write_markdown(s: dict, manifest: dict, confidence: str, note: str) -> None:
    sources = (
        "  - https://us.api.blizzard.com/data/wow/talent-tree (Blizzard Game Data API, Tier 1)\n"
        f"  - https://wago.tools/db2 Trait* @ {manifest['wago_build']} (Tier 1)"
        if manifest["mode"] == "api"
        else f"  - https://wago.tools/db2 Trait* @ {manifest['wago_build']} (Tier 1, DB2-derived)"
    )
    fm = (
        "---\n"
        f"title: {s['class_name']} {s['spec_name']} — talent tree ({manifest['patch']})\n"
        f"patch: {manifest['patch']}\n"
        f"build: {manifest['wago_build']}\n"
        f"fetched: {manifest.get('fetched', '')}\n"
        "sources:\n" + sources + "\n"
        f"confidence: {confidence}\n"
        "---\n\n"
    )
    parts = [fm, f"# {s['class_name']} {s['spec_name']} — talents ({manifest['patch']})\n"]
    if note:
        parts.append(f"\n> {note}\n")
    parts.append(
        "\n> Generated from `knowledge/classes/_talents/all-talents.tsv`. "
        "Spell IDs are the talent's granted spell. Choice nodes show both "
        "options as `A / B`. See `_talents/README.md` for the schema.\n\n"
    )
    parts.append("## Class tree\n\n" + _md_table(s["sections"]["class"]))
    parts.append("\n## Spec tree\n\n" + _md_table(s["sections"]["spec"]))
    for hero_name, nodes in s["sections"]["hero"]:
        parts.append(f"\n## Hero: {hero_name}\n\n" + _md_table(nodes))
    out = CLASSES_DIR / s["class"] / s["spec"] / "talents.md"
    _atomic_write(out, "".join(parts))


def _codec_meta(s: dict, db2: Db2Index) -> dict:
    """Loadout-codec facts the per-spec graph needs to (de)serialize export strings.

    The game walks every node in the class-wide tree (serial 0..serial_count-1),
    not just this spec's slice. To round-trip a string byte-for-byte the encoder
    must also reproduce the slots the game fills automatically:
      * granted_serials — selected-but-not-purchased nodes (free talents): the
        class/spec CondType==2 grants plus each usable hero tree's keystone
        (its prereq-less root, auto-granted to the spec).
      * hero_selector   — the type-3 node whose choice index picks the active
        hero tree; {serial, choices:[heroName ordered by choice index]}.
    """
    tid = s["tree_id"]
    serial_count = db2.tree_node_count.get(str(tid), 0)

    def ser(node_id: int):
        v = db2.serial_order(tid, node_id)
        return v if v != "" else None

    granted: set[int] = set()
    for kind in ("class", "spec"):
        for n in s["sections"][kind]:
            if n["node_id"] in db2.granted_cond:
                granted.add(n["node_id"])
    for _hero_name, nodes in s["sections"]["hero"]:
        ids = {n["node_id"] for n in nodes}
        for n in nodes:
            if not [p for p in n["prereq_node_ids"] if p in ids]:
                granted.add(n["node_id"])  # keystone root of an accessible hero tree
    granted_serials = sorted(
        x for x in (ser(nid) for nid in granted) if x is not None
    )

    name_to_sub = db2.subtree_by_tree.get(str(tid), {})
    sub_ids = {name_to_sub[name] for name, _ in s["sections"]["hero"] if name in name_to_sub}
    sel_node, sel_subs = db2.selector_node(tid, sub_ids)
    hero_selector = None
    if sel_node is not None and ser(sel_node) is not None:
        hero_selector = {
            "serial": ser(sel_node),
            "choices": [db2.subtree_name.get(sid, "") for sid in sel_subs],
        }

    return {
        "serial_count": serial_count,
        "granted_serials": granted_serials,
        "hero_selector": hero_selector,
    }


def write_json(s: dict, manifest: dict, db2: Db2Index, enrich_map: dict) -> None:
    def entry_json(e):
        # Stage A enrichment is inlined per entry so the per-spec file stays
        # self-contained (icon is a full Blizzard media URL; desc is rich text).
        meta = enrich_map.get(str(e["spell_id"]), {})
        return {**e, "icon": meta.get("icon"), "desc": meta.get("desc", "")}

    def node_json(n):
        return {
            "node_id": n["node_id"], "type": n["node_type"],
            "row": n["row"], "col": n["col"], "x": n["x"], "y": n["y"],
            "serial_order": n["serial_order"], "req_points": n["req_points"],
            "prereq_node_ids": n["prereq_node_ids"],
            "entries": [entry_json(e) for e in n["entries"]],
        }
    codec = _codec_meta(s, db2)
    doc = {
        "class": s["class"], "class_id": s["class_id"],
        "spec": s["spec"], "spec_id": s["spec_id"],
        "tree_id": s["tree_id"],
        "patch": manifest["patch"], "build": manifest["wago_build"],
        "source": manifest["mode"],
        "serial_count": codec["serial_count"],
        "granted_serials": codec["granted_serials"],
        "hero_selector": codec["hero_selector"],
        # Stage A′: per-tree-kind point budget at the level cap (Tier-1, from
        # TraitCurrencySource). Identical across specs (global currencies).
        "level_cap": LEVEL_CAP,
        "budgets": db2.budgets(s["tree_id"]),
        "trees": {
            "class": [node_json(n) for n in s["sections"]["class"]],
            "spec": [node_json(n) for n in s["sections"]["spec"]],
            "hero": {name: [node_json(n) for n in nodes]
                     for name, nodes in s["sections"]["hero"]},
        },
    }
    out = CLASSES_DIR / s["class"] / s["spec"] / "talents.json"
    _atomic_write(out, json.dumps(doc, indent=2) + "\n")


# ── cross-check ──────────────────────────────────────────────────────────────
def cross_check(specs: list[dict], db2: Db2Index) -> dict[int, list[str]]:
    """Return {spec_id: [warnings]} where API node ids are absent from DB2 at this build."""
    warnings = defaultdict(list)
    for s in specs:
        missing = 0
        for kind in ("class", "spec"):
            for n in s["sections"][kind]:
                if db2.serial_order(s["tree_id"], n["node_id"]) == "":
                    missing += 1
        for _, nodes in s["sections"]["hero"]:
            for n in nodes:
                if db2.serial_order(s["tree_id"], n["node_id"]) == "":
                    missing += 1
        if missing:
            warnings[s["spec_id"]].append(
                f"{missing} API node(s) absent from DB2 tree {s['tree_id']} "
                f"@ {db2.build} (build skew)"
            )
    return warnings


# ── enrich (Stage A: icon URL + description per spell) ──────────────────────────
def _media_icon_url(media: dict) -> str | None:
    """Full Blizzard media URL for a spell's icon asset. Per the M5 decision we
    keep the whole Tier-1 URL (no third-party CDN, no slug rewrite)."""
    assets = media.get("assets", [])
    for a in assets:
        if a.get("key") == "icon":
            return a.get("value")
    return assets[0].get("value") if assets else None


def _get_json_soft(path: str, retries: int = 3):
    """blizzard.get, tolerating absent/flaky records: None on 404 (choice/aura
    spells with no record) and on a persistent 5xx or connection error after a
    short retry, so one bad spell can't abort a 3000-spell run. Auth/4xx errors
    still raise — those are configuration problems worth stopping for."""
    for attempt in range(retries):
        try:
            return blizzard.get(path)
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            if status == 404:
                return None
            if status is not None and 500 <= status < 600:
                if attempt < retries - 1:
                    time.sleep(0.5 * (attempt + 1))
                    continue
                return None  # persistently failing record → treat as a miss
            raise
        except requests.RequestException:
            if attempt < retries - 1:
                time.sleep(0.5 * (attempt + 1))
                continue
            return None
    return None


def enrich(sleep_s: float = 0.05) -> None:
    """Resolve icon URL + description for every distinct talent spell.

    Caches each raw API response under raw/blizzard/ and the distilled lookup in
    raw/spell-enrichment.json, so re-runs only fetch newly-seen spells (cheap and
    polite). Misses fall back to icon=null / desc="" and are counted in the
    report. `build` reads the lookup and inlines icon+desc onto each entry.
    """
    if not MANIFEST.exists():
        sys.exit("error: no manifest — run `talents fetch` first")
    manifest = json.loads(MANIFEST.read_text())
    if manifest["mode"] != "api":
        sys.exit("error: enrich needs the live API (media + descriptions) — re-fetch without --build")

    db2 = Db2Index(manifest["wago_build"])
    specs = parse_api(manifest, db2)
    spell_ids = sorted({
        e["spell_id"]
        for s in specs
        for kind in ("class", "spec")
        for n in s["sections"][kind]
        for e in n["entries"]
    } | {
        e["spell_id"]
        for s in specs
        for _, nodes in s["sections"]["hero"]
        for n in nodes
        for e in n["entries"]
    })

    cache: dict[str, dict] = {}
    if ENRICH_CACHE.exists():
        cache = json.loads(ENRICH_CACHE.read_text())

    todo = [sid for sid in spell_ids if str(sid) not in cache]
    print(f"enrich: {len(spell_ids)} distinct spells, {len(todo)} to fetch "
          f"({len(spell_ids) - len(todo)} cached)")
    fetched = 0
    for sid in todo:
        media = _get_json_soft(f"/data/wow/media/spell/{sid}")
        if media is not None:
            save_raw("blizzard", f"media-spell-{sid}.json", json.dumps(media, indent=2))
        spell = _get_json_soft(f"/data/wow/spell/{sid}")
        if spell is not None:
            save_raw("blizzard", f"spell-{sid}.json", json.dumps(spell, indent=2))
        icon = _media_icon_url(media) if media else None
        desc = (spell.get("description") or "").strip() if spell else ""
        cache[str(sid)] = {"icon": icon, "desc": desc}
        fetched += 1
        if fetched % 50 == 0:
            print(f"  {fetched}/{len(todo)} fetched")
            _atomic_write(ENRICH_CACHE, json.dumps(cache, indent=2) + "\n")  # checkpoint
        time.sleep(sleep_s)

    _atomic_write(ENRICH_CACHE, json.dumps(cache, indent=2) + "\n")
    icon_miss = sum(1 for sid in spell_ids if not cache.get(str(sid), {}).get("icon"))
    desc_miss = sum(1 for sid in spell_ids if not cache.get(str(sid), {}).get("desc"))
    print(f"wrote {ENRICH_CACHE.name} ({len(cache)} spells)")
    print(f"  misses: icon {icon_miss}/{len(spell_ids)}  desc {desc_miss}/{len(spell_ids)}")
    print("  re-run `talents build` to inline icon+desc into talents.json")


# ── build ──────────────────────────────────────────────────────────────────────
def build(fetched: str) -> None:
    if not MANIFEST.exists():
        sys.exit("error: no manifest — run `talents fetch` first")
    manifest = json.loads(MANIFEST.read_text())
    manifest["fetched"] = fetched
    db2 = Db2Index(manifest["wago_build"])

    if manifest["mode"] == "api":
        specs = parse_api(manifest, db2)
    else:
        sys.exit("error: DB2-only (PTR) build path not yet wired — re-fetch without --build")

    enrich_map = {}
    if ENRICH_CACHE.exists():
        enrich_map = json.loads(ENRICH_CACHE.read_text())
        print(f"enrichment: {len(enrich_map)} spell(s) with icon/desc from {ENRICH_CACHE.name}")
    else:
        print(f"⚠ no {ENRICH_CACHE.name} — run `talents enrich`; emitting icon=null/desc=\"\"")

    warnings = cross_check(specs, db2)
    write_tsv(specs)
    write_trees_tsv(specs)
    for s in specs:
        confidence = "high" if manifest["mode"] == "api" else "medium"
        note = ""
        if s["spec_id"] in warnings:
            confidence = "low"
            note = "; ".join(warnings[s["spec_id"]])
        elif manifest["mode"] == "db2":
            note = "PTR/DB2-derived — names via SpellName join; not cross-checked against the live API."
        write_markdown(s, manifest, confidence, note)
        write_json(s, manifest, db2, enrich_map)
    print(f"wrote {len(specs)} per-spec talents.md + talents.json")
    if warnings:
        print(f"⚠ {len(warnings)} spec(s) flagged confidence:low (see notes)")

    # Budget cross-check: derived level-cap totals vs the starter loadouts.
    print(f"budgets @ level {LEVEL_CAP} (TraitCurrencySource):")
    for tid in sorted({s["tree_id"] for s in specs}):
        cls = next(s["class"] for s in specs if s["tree_id"] == tid)
        b = db2.budgets(tid)
        total = b["class"] + b["spec"] + b["hero"]
        loadout = db2.loadout_max.get(str(tid), 0)
        flag = "" if loadout <= total else f"  ⚠ starter loadout {loadout} > budget {total}"
        print(f"  {cls:13} class {b['class']} spec {b['spec']} hero {b['hero']} "
              f"= {total}  (starter loadout max {loadout}){flag}")


# ── verify ──────────────────────────────────────────────────────────────────────
def verify() -> None:
    tsv = TALENTS_DIR / "all-talents.tsv"
    if not tsv.exists():
        sys.exit("error: no all-talents.tsv — run `talents build` first")
    with tsv.open(newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    manifest = json.loads(MANIFEST.read_text()) if MANIFEST.exists() else {}
    print(f"build: {manifest.get('wago_build')}  mode: {manifest.get('mode')}  rows: {len(rows)}")

    by_class = defaultdict(set)
    for r in rows:
        by_class[r["class"]].add(r["spec"])
    print(f"classes: {len(by_class)}  specs: {sum(len(v) for v in by_class.values())}")

    # choice-node integrity: each choice_group must have exactly 2 entries
    choice_entries = defaultdict(int)
    for r in rows:
        if r["choice_group"]:
            choice_entries[(r["spec_id"], r["choice_group"])] += 1
    bad = {k: v for k, v in choice_entries.items() if v != 2}
    print(f"CHOICE nodes: {len(choice_entries)}  with != 2 entries: {len(bad)}")
    for k, v in list(bad.items())[:10]:
        print(f"  ⚠ spec {k[0]} node {k[1]}: {v} entries")

    # empty spell ids / names
    empty_names = [r for r in rows if not r["talent"]]
    empty_spells = [r for r in rows if not r["spell_id"] or r["spell_id"] == "0"]
    print(f"rows with empty talent name: {len(empty_names)}  empty spell id: {len(empty_spells)}")

    # export-string readiness: serial_order present, choice_index in {0,1}
    no_serial = [r for r in rows if r["serial_order"] == ""]
    bad_choice = [r for r in rows if r["choice_group"] and r["choice_index"] not in ("0", "1")]
    print(f"rows missing serial_order: {len(no_serial)}  CHOICE rows w/ choice_index not in {{0,1}}: {len(bad_choice)}")

    # serial_order contiguity per tree (shared across a class's specs)
    per_tree = defaultdict(set)
    for r in rows:
        if r["serial_order"] != "":
            per_tree[r["class"]].add(int(r["serial_order"]))
    for cls, orders in sorted(per_tree.items()):
        lo, hi = min(orders), max(orders)
        gap = (hi - lo + 1) - len(orders)
        flag = "" if gap == 0 else f"  ({gap} DB2 type-3 selector/grant nodes carry no talent — API omits them)"
        print(f"  {cls:13} serial_order {lo}..{hi} distinct={len(orders)}{flag}")


# ── cli ──────────────────────────────────────────────────────────────────────
def main() -> None:
    p = argparse.ArgumentParser(prog="wowkb.talents", description=__doc__)
    sub = p.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch", help="acquire API + wago raw inputs")
    f.add_argument("--build", default=None, help="exact wago build => DB2-only (PTR/historical)")
    f.add_argument("--patch", default=None, help="patch label for front matter (default: from build)")
    e = sub.add_parser("enrich", help="resolve per-spell icon URL + description (Stage A)")
    e.add_argument("--sleep", type=float, default=0.05, help="seconds between API fetches")
    b = sub.add_parser("build", help="parse raw -> TSV + markdown + json")
    b.add_argument("--fetched", default="", help="ISO date to stamp in front matter (e.g. 2026-06-18)")
    sub.add_parser("verify", help="read-only sanity report")
    args = p.parse_args()

    if args.cmd == "fetch":
        fetch(args.build, args.patch)
    elif args.cmd == "enrich":
        enrich(args.sleep)
    elif args.cmd == "build":
        build(args.fetched)
    elif args.cmd == "verify":
        verify()


if __name__ == "__main__":
    main()
