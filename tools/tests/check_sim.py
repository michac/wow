"""Offline verification for wowkb.sim (Phase 1: export parsing, profile building, gates).

Stdlib-only:  python3 tools/tests/check_sim.py   (exits non-zero on failure)

The headline case is the last block: `check` on Encomplete's 2026-08-20 export must
report Stormbound Emblem of Dazar firing ZERO times under the upstream APL. That trinket
sat inert through four separate comparisons that day and nothing in simc's output said
so; if this ever passes silently, the firing gate is broken and every DPS number the
tool prints is worth nothing. It needs the local simc build, so it SKIPS loudly rather
than passing quietly when the binary is absent.
"""
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))  # tools/
from wowkb.sim import (  # noqa: E402
    ARMOR_CLOTH, ARMOR_COSMETIC, ARMOR_MAIL, ARMOR_PLATE, BASELINE, CANON_SLOTS,
    ITEM_CLASS_ARMOR, ITEM_CLASS_WEAPON, ITEM_REDUNDANCY_SLOT,
    REDUNDANCY_PAIRED, RESULTS, SE_MEDIAN_FACTOR, SIMC_BIN,
    WEAPON_SLOTS, CrossFrame, Frame, Unsupported, _bonus_step, _exclusion_summary,
    _fmt_row, build_profile, candidates, firing_gate, frame_deltas, gear_variants,
    introduces_effects, is_weapon, item_effects, item_meta, item_names, label,
    leak_gate, parse_export, parse_variant, profileset_lines, resolve_candidate,
    parse_watermarks, resolve_reference, run_simc, set_bonuses, set_counts,
    tier_note, tokenize,
    variant_export,
    wearable,
    # ── Phase 4: tracks, crests, ranks ──
    CREST_COST_DISCOUNTED, CREST_COST_PER_RANK, CREST_CURRENCIES, DAWN_ACHIEVEMENTS,
    LEGACY_CREST_CURRENCIES, MIST_ACHIEVEMENTS, TRACKS, TRACK_STEPS, UPGRADE_ITEMS,
    allocate, crest_balances, discount_state, ilvl_fidelity_gate,
    parse_upgrade_achievements, parse_upgrade_currencies, rank_name, rank_variants,
    redundancy_slot, track_ilvl, upgrade_ranks, watermark_for,
    # ── Phase 5: the cast timeline ──
    LOG_BRAND, LOG_SEED, _log_line, effect_subjects, log_actions, log_options,
    log_windows, parse_log, window_events,
    # ── character overrides ──
    OFF_GCD, load_overrides, override_brand, resolve_apl_append, resolve_overrides,
)

FIX = pathlib.Path(__file__).parent / "fixtures"
EXPORT = FIX / "simc-export-encomplete.simc"
_total = 0
_fails = []


def check(cond, msg):
    global _total
    _total += 1
    if not cond:
        _fails.append(msg)


text = EXPORT.read_text(encoding="utf-8")
export = parse_export(text)

# ── Identity, straight off the `<class>="<name>"` line ───────────────────────
check(export["character"] == "Encomplete", "character name off the class line")
check(export["class"] == "warlock", "class token is the option name, not a `class=` line")
check(export["spec"] == "demonology", "spec parsed")
check(export["race"] == "gnome" and export["level"] == "90", "race + level parsed")
check(export["client_build"] == "12.1.0.69382",
      "client build parsed (it can be AHEAD of game-version.md — that is the point)")
check(export["exported"] == "2026-08-20", "export date off the header comment")
check(export["checksum"] == "f6096dd7", "checksum parsed")
check(export["talents"] and export["talents"].startswith("CoQAMrNP5kak"),
      "the ACTIVE talents line, not one of the commented saved loadouts")
check(len(export["loadouts"]) == 3, f"3 saved loadouts kept aside (got {len(export['loadouts'])})")

# ── Equipped: every slot, with the name/ilvl from its comment line ───────────
check(len(export["equipped"]) == 17, f"17 equipped slots (got {len(export['equipped'])})")
check("off_hand" not in export["equipped"],
      "off_hand genuinely absent — a 2H character, the slot the reference profile leaks")
check(export["equipped"]["shoulders"]["slot"] == "shoulders",
      "the addon's singular `shoulder=` normalizes onto simc's canonical `shoulders`")
check(export["equipped"]["wrists"]["ilvl"] == 295, "`wrist=` → wrists, ilvl off the comment")
check(export["equipped"]["trinket2"]["name"] == "Stormbound Emblem of Dazar",
      "apostrophe-free name parsed intact")
check(export["equipped"]["main_hand"]["item_id"] == 245770, "item id off the item string")

# ── The bag block (failure #8's neighbour) ───────────────────────────────────
check(len(export["bags"]) == 68, f"68 bag candidates (got {len(export['bags'])})")
check(all(r["slot"] in CANON_SLOTS for r in export["bags"]),
      "every bag row carries a canonical slot")
check(any(r["name"] == "Pyrewalker's Gloves" and r["slot"] == "hands"
          for r in export["bags"]), "a named bag row round-trips with its slot")

# ── The vault block: failure #8 itself ──────────────────────────────────────
# Skipped entirely on 2026-08-20; the vault options were missed until the user asked.
check(len(export["vault"]) == 5, f"5 weekly reward choices (got {len(export['vault'])})")
vault_labels = [label(r) for r in export["vault"]]
check(sum(1 for r in export["vault"] if r["slot"] == "hands") == 3,
      "three of the five vault choices are gloves")
# Three of the five ship with NO `# <Name>` comment at all. A row that reads as a bare
# id is unreviewable, so the name comes from simc's own item table instead.
check(any("Handwraps of Blasphemous Rites" in s for s in vault_labels),
      f"unnamed vault rows resolve to real names\n      {vault_labels}")
check(any("Mindpiercer's Sigil" in s for s in vault_labels),
      "the trinket the 2026-08-20 session wrongly recommended is surfaced by name")
check(all("None" not in s and s.strip() for s in vault_labels),
      "no label is blank or a stringified None — a blank cell reads as 'negligible'")

# ── Additional character info ────────────────────────────────────────────────
check(export["catalyst_currencies"] == "2813:8/3269:8/3116:8/3378:8/3465:1",
      "catalyst currencies captured")
check(export["slot_high_watermarks"].count("/") == 16,
      "17 watermark rows captured verbatim (Enum.ItemRedundancySlot — Phase 0 decodes it)")
check(export["upgrade_currencies"].startswith("c:3442:186"), "upgrade currencies captured")

# ── Storing is verbatim ──────────────────────────────────────────────────────
check("### End of Weekly Reward Choices" in text,
      "fixture is the untouched paste, terminator and all")

# ── The reference chain: MID2 → MID1 → simc-apl.md → exit 2 ─────────────────
ref = resolve_reference("warlock", "demonology", None)
check(ref["tier"] == "MID2" and ref["kind"] == "profile",
      f"demonology resolves to a MID2 profile (got {ref['tier']})")
check(ref["warn"] is None, "a MID2 profile carries no caveat")

havoc = resolve_reference("dh", "havoc", None)
check(havoc["tier"] == "MID1", "Havoc has no MID2 profile and falls to MID1")
check(havoc["warn"] and "MID1" in havoc["warn"],
      "the MID1 rung WARNS — MID1_Demon_Hunter_Havoc.simc was measured 151 days stale")

havoc_kb = resolve_reference("dh", "havoc", None, "kb")
check(havoc_kb["kind"] == "kb-apl" and havoc_kb["actions"],
      "`--apl-source kb` reaches the generated simc-apl.md (36 specs) — the reuse")
check("no consumables" in (havoc_kb["warn"] or "").lower()
      or "NO consumables" in (havoc_kb["warn"] or ""),
      "the KB rung says what it does NOT carry")

for cls, spec in (("shaman", "restoration"), ("monk", "mistweaver"),
                  ("evoker", "preservation"), ("paladin", "holy")):
    try:
        resolve_reference(cls, spec, None)
        check(False, f"{cls}/{spec} must be unsupported, not silently simmed")
    except Unsupported as exc:
        check("built-in APL" in str(exc),
              f"{cls}/{spec} refuses simc's built-in APL by name (failure #1)")

# ── Profile building: slot hygiene (invariant 3) ─────────────────────────────
# ⚠ use_overrides=False, and that is the whole point of this block. The headline
# regression below asserts what UPSTREAM does unaided — Stormbound Emblem of Dazar
# sitting inert through a 300s fight. Encomplete now carries an `apl_append` override
# that fixes it in real runs, so without this flag the test would go green for the right
# reason in the wrong place, and the firing gate itself would stop being tested.
profile, built = build_profile(export, ref, use_overrides=False)
check(profile.startswith('warlock="Encomplete"'),
      "our player line is first — a second `<class>=` would create a SECOND actor")
assigned_lines = [ln for ln in profile.splitlines() if ln.split("=", 1)[0] in CANON_SLOTS]
check(len(assigned_lines) == len(CANON_SLOTS),
      f"all {len(CANON_SLOTS)} slots emitted, assigned or cleared (got {len(assigned_lines)})")
check("off_hand=" in profile and "off_hand=alnhara_lantern" not in profile,
      "off_hand is explicitly CLEARED — the reference profile ships one and a 2H "
      "character inherited it for real on 2026-08-20")
check(built["cleared"] == ["off_hand"], f"exactly one cleared slot (got {built['cleared']})")
check("race=Orc" not in profile and "race=gnome" in profile,
      "the reference profile's identity is dropped, ours re-emitted")
check("MID2_Warlock_Demonology_Soulharvester" not in profile,
      "the reference's own player name does not survive")
check("actions.items=use_item" in profile,
      "the maintained APL DOES survive — including its trinket-priority logic")
check(sum(1 for ln in profile.splitlines() if ln.startswith("talents=")) == 1,
      "exactly one talents hash (count by line — `omnium_talents=` contains the "
      "substring and a naive count double-counts it)")

# An override lands on the slot and nothing else moves.
swapped, _ = build_profile(export, ref, overrides={"hands": ",id=275500,bonus_id=40"})
check("hands=,id=275500,bonus_id=40" in swapped, "an override replaces just that slot")
check(swapped.count("trinket2=") == 1 and export["equipped"]["trinket2"]["item_string"]
      in swapped, "every other slot is untouched by an override")

# ── simc's item-effect table ────────────────────────────────────────────────
effects = item_effects()
check(effects, "item_effect.inc parsed")
check(any(e["type"] == 0 for e in effects.get(273649, [])),
      "Stormbound Emblem of Dazar (273649) carries an ON-USE effect in simc's own data")
check(any(e["name"] == "The King's Unyielding Wind" for e in effects.get(273649, [])),
      "its effect is named differently from the ITEM — which is why matching is "
      "by effect name and spell id, not by item name alone")
check(tokenize("The King's Unyielding Wind") == "the_kings_unyielding_wind",
      "tokenize matches simc's util::tokenize (apostrophes dropped)")
check(tokenize("Freightrunner's Flask") == "freightrunners_flask", "tokenize round-trip")

# ══ Phase 2: variants, frames, deltas ═══════════════════════════════════════

def raises(fn, needle, msg):
    try:
        fn()
    except Unsupported as exc:
        check(needle.lower() in str(exc).lower(),
              f"{msg}\n      wanted {needle!r} in: {exc}")
    else:
        check(False, f"{msg} — nothing raised")


name, ovr = parse_variant("0pc = shoulders=@Poisoner's Pauldrons; legs=", export)
check(name == "0pc", "variant name off the first `=`")
check(ovr["shoulders"].startswith(",id=251227"),
      "`@<Item Name>` resolves to the EXPORT's own item string — bonus ids and all, "
      "which is why nobody should be typing one by hand")
check(ovr["legs"] == "", "a bare `<slot>=` strips the slot")

# The baseline is not a variant you may redefine: it IS the current gear, emitted as a
# profileset so it ranks in the same median table (failure #6).
raises(lambda: parse_variant("_baseline=hands=", export), "reserved",
       "`_baseline` is refused as a variant name")
raises(lambda: parse_variant("0pc", export), "no `=`", "a variant with no `=` explains the form")
raises(lambda: parse_variant("A=helmet=,id=1", export), "not a gear slot",
       "a non-slot key names the slot list")
raises(lambda: parse_variant("A=", export), "changes nothing", "an empty variant is refused")
raises(lambda: parse_variant('Bad"Name=hands=', export), "must match",
       "a name that would break the profileset quoting is refused")

# Same item, two upgrade levels, sitting in the export at once. Picking one silently is
# picking a different answer.
raises(lambda: resolve_candidate(export, "shoulders", "Abyssal Immolator's Fury"),
       "matches 2 different", "an ambiguous name lists the ilvls instead of guessing")
check(resolve_candidate(export, "shoulders", "Abyssal Immolator's Fury (263)")[0]
      .startswith(",id=250040,bonus_id=13340"),
      "`@Name (ilvl)` disambiguates to the bag copy, not the equipped one")
raises(lambda: resolve_candidate(export, "hands", "Nonexistent Gloves"),
       "no hands candidate", "an unknown name lists what IS available")

# Paired slots: the addon files every trinket under `trinket1`, but the index is not
# cosmetic — trinket1 wins upstream's damage_trinket_priority tie-break, which is the
# mechanism behind the whole 2026-08-20 disaster.
sigil, row = resolve_candidate(export, "trinket2", "Mindpiercer's Sigil")
check(row["slot"] == "trinket1" and sigil.startswith(",id=250224"),
      "a vault trinket filed under trinket1 is reachable as a trinket2 candidate")
notes = []
parse_variant("Sigil=trinket2=@Mindpiercer's Sigil", export, notes)
check(notes and "trinket1" in notes[0] and "tie-break" in notes[0],
      f"and the move across the pair is REPORTED, not made quietly ({notes})")
check(any(r["slot"] == "finger1" for r in candidates(export, "finger2")),
      "rings pair the same way")

# Profileset emission: the baseline is a profileset like any other.
lines = profileset_lines({"A": {"hands": ",id=1"}})
check(lines[2] == "profileset_metric=dps", "the metric is pinned to dps")
check(f'profileset."{BASELINE}"+=level=' in lines[3],
      "the baseline re-asserts the character's own level — a provable no-op that still "
      "puts it in the median-ranked table rather than on a separate mean line")
check('profileset."A"+=hands=,id=1' in lines, "a variant emits one option per slot")

# Deltas, and the structural refusal of a cross-invocation comparison (failure #4).
def fake_frame(ident, base_median, base_se, var_median, var_se):
    return Frame(ident, 1, 300, {"sim": {"options": {"iterations": 1000},
        "profilesets": {"results": [
            {"name": BASELINE, "median": base_median, "mean_stddev": base_se,
             "iterations": 1000},
            {"name": "V", "median": var_median, "mean_stddev": var_se,
             "iterations": 1000}]}}}, "", pathlib.Path("x"), {})


rows = {r["name"]: r for r in frame_deltas(fake_frame("f1", 100000.0, 10.0, 105000.0, 10.0))}
check(rows[BASELINE]["verdict"] == "baseline", "the baseline is labelled, not deltaed")
check(abs(rows["V"]["delta_pct"] - 5.0) < 1e-9, "Δ% is against the baseline MEDIAN")
expected_err = 100.0 * 1.96 * (2 * (SE_MEDIAN_FACTOR * 10.0) ** 2) ** 0.5 / 100000.0
check(abs(rows["V"]["err_pct"] - expected_err) < 1e-9,
      "the band is 95% on the MEDIAN (simc's mean SE scaled), baseline and variant "
      "errors added in quadrature — quoting simc's mean error on a median comparison "
      "is exactly the mixing that cost a day on 2026-08-20")
check(rows["V"]["verdict"] == "significant", "5000 DPS over a ~35 DPS band is significant")
noise = {r["name"]: r for r in frame_deltas(fake_frame("f2", 100000.0, 500.0, 100100.0, 500.0))}
check(noise["V"]["verdict"] == "NOISE", "100 DPS inside the band reads NOISE, not a win")
check([r["name"] for r in frame_deltas(fake_frame("f3", 100.0, 1.0, 200.0, 1.0))]
      == ["V", BASELINE], "rows rank by median, baseline included")

mixed = fake_frame("f4", 100000.0, 10.0, 105000.0, 10.0)
mixed.results["V"]["frame"] = "some-other-invocation"
try:
    frame_deltas(mixed)
    check(False, "a cross-invocation delta must be refused, not warned about")
except CrossFrame as exc:
    check("failure #4" in str(exc), "the refusal names the failure it prevents")

# No ambiguous blanks (failure #7): a dash read as "negligible" once already.
check(_fmt_row(None) == ("not simulated",) * 3,
      "a variant missing from a frame reads `not simulated`, never blank or `—`")

# The variant firing gate's trigger: only a variant that brings in an item with an
# effect is worth a validation run.
check(introduces_effects(export, {"trinket2": sigil}),
      "swapping in a trinket with a registered effect triggers a validation run")
check(not introduces_effects(export, {"legs": ""}),
      "stripping a slot with no special effect does not")
check(not introduces_effects(
    export, {"trinket2": export["equipped"]["trinket2"]["item_string"]}),
    "re-asserting the item already worn is not an introduction")
sub = variant_export(export, {"trinket2": sigil, "legs": ""})
check(sub["equipped"]["trinket2"]["item_id"] == 250224 and "legs" not in sub["equipped"],
      "the gate inspects the VARIANT's items, not the baseline's")
check(export["equipped"]["trinket2"]["item_id"] == 273649,
      "and the real export is not mutated on the way")


# ══ Phase 0: the ItemRedundancySlot enum (no ClientLab run needed) ═══════════

check(len(ITEM_REDUNDANCY_SLOT) == 17 and set(ITEM_REDUNDANCY_SLOT) == set(range(17)),
      "the enum covers exactly 0..16, which is the range core.lua loops over")
check(ITEM_REDUNDANCY_SLOT[12] == "Twohand" and ITEM_REDUNDANCY_SLOT[9] == "Finger",
      "…and is NOT a permuted INVSLOT: index 12 is Twohand, 9 is a single Finger row")
check(REDUNDANCY_PAIRED == {"Finger", "Trinket"},
      "exactly two enum rows cover two worn items each")

marks = {r["slot"]: r for r in parse_watermarks(export)}
check(len(marks) == 17, f"all 17 watermark rows resolve to named slots (got {len(marks)})")

# The fingerprint that confirms the mapping without the client: eight slots whose
# watermark equals the ilvl actually worn there. A wrong mapping does not survive this.
FINGERPRINT = {"Head": "head", "Waist": "waist", "Feet": "feet", "Wrist": "wrists",
               "Hand": "hands", "Cloak": "back", "Twohand": "main_hand"}
for mark_slot, inv_slot in FINGERPRINT.items():
    check(marks[mark_slot]["character"] == export["equipped"][inv_slot]["ilvl"],
          f"{mark_slot} watermark == the ilvl worn in {inv_slot} "
          f"({marks[mark_slot]['character']} vs "
          f"{export['equipped'][inv_slot]['ilvl']}) — the mapping's fingerprint")
check(marks["Trinket"]["character"] == 305 and marks["Head"]["index"] == 0,
      "Trinket resolves at index 10, Head at 0")

# ⚠ The live subject of the paired-slot caveat. If someone ever 'fixes' `crests` to read
# a paired row as "highest ever worn", THIS is what catches it: a 305 ring is equipped
# and the Finger row says 295.
worn_rings = sorted(export["equipped"][s]["ilvl"] for s in ("finger1", "finger2"))
check(worn_rings == [295, 305], "Encomplete wears a 295 and a 305 ring")
check(marks["Finger"]["character"] == 295,
      "the Finger watermark is 295 — the SECOND-highest ring, not the highest. A paired "
      "row is not 'best ever worn here', and Phase 4 may not assume it is")
check(marks["Finger"]["paired"] and marks["Trinket"]["paired"]
      and not marks["Head"]["paired"], "paired rows are flagged as such")
# The same shape in the one-hand weapon rows, which DO get two indices: 246 and 62.
check(marks["OnehandWeapon"]["character"] > marks["OnehandWeaponSecond"]["character"],
      "OnehandWeapon > OnehandWeaponSecond — the enum tracks a pair's second mark "
      "separately for weapons, which is the same redundancy shape")

check(parse_watermarks({"slot_high_watermarks": "99:1:2"})[0]["slot"]
      == "index 99 (unknown to this build)",
      "an index a future build adds survives as a number rather than vanishing")
check(parse_watermarks({"slot_high_watermarks": None}) == [], "no watermarks → no rows")


# ══ Phase 3: item metadata, the usability filter, the tier-set confound ══════
#
# All offline — no simc binary needed. `item_data.inc` and `item_set_bonus.inc` are
# files on disk in the local checkout.

# The column indices, asserted against three known rows. This is the off-by-one that
# already bit once (`type_flags` is easy to drop) and silently reported EVERY bag row
# as unwearable — a filter that excludes everything looks exactly like a filter that
# excludes nothing until you read the count.
GRASPS = item_meta()[250043]      # Abyssal Immolator's Grasps — Warlock tier hands
CANE = item_meta()[245770]        # Aln'hara Cane — a staff
GLADIATOR = item_meta()[100013]   # Tyrannical Gladiator's Scaled Gauntlets — plate
check(GRASPS["name"] == "Abyssal Immolator's Grasps", "item name column")
check(GRASPS["item_class"] == ITEM_CLASS_ARMOR and GRASPS["item_subclass"] == ARMOR_CLOTH,
      f"250043 is cloth armor (got class {GRASPS['item_class']}/"
      f"{GRASPS['item_subclass']})")
check(GRASPS["class_mask"] == 0x0100,
      f"250043 class_mask is Warlock-only 0x0100 (got {GRASPS['class_mask']:#06x})")
check(GRASPS["inventory_type"] == 10, "250043 inventory_type is hands (10)")
check(GRASPS["level"] == 197,
      "250043 `level` is the BASE ilvl 197, not the 276 it is worn at — which is why "
      "row labels come from the export's comment, never from this column")
check(CANE["item_class"] == ITEM_CLASS_WEAPON and CANE["item_subclass"] == 10,
      f"245770 is a staff — weapon class 2, subclass 10 (got {CANE['item_class']}/"
      f"{CANE['item_subclass']})")
check(CANE["class_mask"] == 0xffff, "245770 is unrestricted (0xffff)")
check(GLADIATOR["item_subclass"] == ARMOR_PLATE and GLADIATOR["class_mask"] == 0x0002,
      f"100013 is plate, Paladin-only (got subclass {GLADIATOR['item_subclass']}, "
      f"mask {GLADIATOR['class_mask']:#06x})")
check(GLADIATOR["race_mask"] == 0xaa2aaaaa4e0ab3b2,
      "race_mask is the last field before socket_color[3] — if THIS is right, every "
      "index before it is right too")

# item_names() is now a view over item_meta(); the vault rows the export leaves
# unnamed must still resolve.
check(item_names()[273773] == "Handwraps of Blasphemous Rites",
      "an unnamed vault row still resolves to a name")

# ── The three tests, on a Warlock ───────────────────────────────────────────
check(wearable(250043, "warlock", "hands") is None, "own-class cloth tier is wearable")
check(wearable(272233, "warlock", "hands") is None,
      "a 0xffff cloth item is kept (Pyrewalker's Gloves)")
check(wearable(100013, "warlock", "hands") == "other-class",
      "class_mask is tested FIRST — Paladin plate reads as other-class, not as plate")
check(wearable(188845, "warlock", "hands") == "other-class",
      "another class's tier is excluded by class_mask ALONE — 188845 is cloth, so the "
      "armor test would happily pass it")
check(wearable(100013, "paladin", "hands") is None,
      "the same plate glove is wearable by the class it is masked to")
check(wearable(100013, "warrior", "hands") == "other-class",
      "…and not by a different plate class")

# Armor type mirrors `item_t::is_valid_type`: matching_armor_type >= subclass, so a
# plate class may wear cloth and never the reverse.
check(wearable(272233, "warrior", "hands") is None,
      "a plate class MAY wear cloth (is_valid_type is >=, not ==)")


def _first(pred):
    for item_id, m in item_meta().items():
        if pred(m):
            return item_id
    return None


mail_body = _first(lambda m: m["item_class"] == ITEM_CLASS_ARMOR
                   and m["item_subclass"] == ARMOR_MAIL
                   and m["inventory_type"] == 1 and m["class_mask"] == 0xffff)
plate_body = _first(lambda m: m["item_class"] == ITEM_CLASS_ARMOR
                    and m["item_subclass"] == ARMOR_PLATE
                    and m["inventory_type"] == 1 and m["class_mask"] == 0xffff)
check(wearable(mail_body, "warlock", "head") == "mail",
      "an unrestricted MAIL body item is excluded for a Warlock, by armor type")
check(wearable(plate_body, "warlock", "head") == "plate",
      "an unrestricted PLATE body item is excluded for a Warlock, by armor type")
check(wearable(mail_body, "warlock", "back") is None,
      "…but only on the 8 slots util::is_match_slot covers — back carries no armor type")

# Cosmetic armor is exempt (engine/item/item.cpp:1640), which is why the cosmetic
# shoulder in Encomplete's bags survives instead of reading as an exclusion bug.
cosmetic = _first(lambda m: m["item_class"] == ITEM_CLASS_ARMOR
                  and m["item_subclass"] == ARMOR_COSMETIC
                  and m["inventory_type"] == 3)
check(wearable(cosmetic, "warlock", "shoulders") is None, "COSMETIC armor is exempt")

# Weapons: flagged, never filtered. simc carries no weapon usability data, so a
# filter here would be invented rather than transcribed.
check(wearable(245770, "warlock", "main_hand") is None, "the worn staff passes")
sword = [r for r in export["bags"]
         if r["slot"] == "main_hand" and is_weapon(r["item_id"])
         and item_meta()[r["item_id"]]["item_subclass"] == 7]
check(sword, "the export really does carry a one-handed sword a Warlock cannot use")
if sword:
    check(wearable(sword[0]["item_id"], "warlock", "main_hand") is None,
          "and it is NOT filtered — it is ranked under the NOT-usability-checked "
          "banner instead, because simc has no data to filter it with")
check("main_hand" in WEAPON_SLOTS and "off_hand" in WEAPON_SLOTS,
      "both weapon slots trigger the banner")

# ── The exclusions are REPORTED, with counts and reasons ────────────────────
head = gear_variants(export, "head")
check(len(head["excluded"]) == 1, f"head excludes exactly 1 row (got {len(head['excluded'])})")
check(head["excluded"] and head["excluded"][0][1] == "mail",
      "…the mail helm, named by its armor type")
check("Tarnished Dawnlit Sentinel's Cover" in label(head["excluded"][0][0]),
      "…and the excluded row is reported by name, not as a count alone")
check("1 mail" == _exclusion_summary(head["excluded"]),
      f"the summary line tallies reasons (got {_exclusion_summary(head['excluded'])!r})")
chest = gear_variants(export, "chest")
check([r for _, r in chest["excluded"]] == ["leather"],
      "chest excludes the leather jerkin")
feet = gear_variants(export, "feet")
check([r for _, r in feet["excluded"]] == ["mail"], "feet excludes the mail boots")
check(sum(len(gear_variants(export, s)["excluded"]) for s in CANON_SLOTS) == 3,
      "3 unwearable rows across the whole export — the bag block is NOT pre-filtered, "
      "which Phase 1 established against the plan's assumption")
shoulders = gear_variants(export, "shoulders")
check(any("Bladed Twilight Spaulder" in label(r) for r in shoulders["rows"].values()),
      "the cosmetic shoulder is KEPT, not excluded")

# ── The acceptance shape for `gear --slot hands` ────────────────────────────
hands = gear_variants(export, "hands")
check(len(hands["variants"]) == 5,
      f"5 hands candidates + the baseline = 6 (got {len(hands['variants'])})")
check(not hands["excluded"], "no hands row is unwearable — every one is cloth")
check(any("Handwraps of Blasphemous Rites" in n for n in hands["variants"]),
      "the vault glove is a candidate under its resolved name, not an item id")
check(all(re.match(r"^[A-Za-z0-9][A-Za-z0-9 _.+/-]*$", n) for n in hands["variants"]),
      "every candidate name is a legal simc profileset name (apostrophes and "
      "parentheses scrubbed)")
check(len(set(hands["variants"])) == len(hands["variants"]), "names are unique")

# ── The tier-set confound ───────────────────────────────────────────────────
check(set_bonuses()[250043][0]["set_name"] == "Reign of the Abyssal Immolator"
      and set_bonuses()[250043][0]["class_id"] == 9,
      "250043 belongs to the Warlock S1 set")
counts = set_counts(export["equipped"], "warlock")
check(counts.get(1989) == 4,
      f"Encomplete wears 4 pieces of set 1989 (got {counts.get(1989)})")
for name, overrides in hands["variants"].items():
    note = tier_note(export, overrides)
    check(note and "4 → 3 pieces" in note and "losing the 4pc" in note,
          f"{name}: every non-tier glove is annotated `tier 4 → 3 … losing the 4pc` "
          f"(got {note!r}) — otherwise the row reads as 'this glove is bad' when it "
          "means 'this glove costs you the 4pc'")
check(tier_note(export, {"neck": export["equipped"]["neck"]["item_string"]}) is None,
      "a swap that touches no set piece is not annotated")
check(_bonus_step(4, 3) == "losing the 4pc" and _bonus_step(1, 2) == "gaining the 2pc"
      and _bonus_step(1, 0) is None,
      "only crossing a 2pc/4pc threshold is called out")

# ── Family handling survives Phase 2's finding 3 ────────────────────────────
t1 = gear_variants(export, "trinket1")
check(len(t1["skipped"]) == 1 and "already worn in trinket2" in t1["skipped"][0][1],
      "the trinket worn in the OTHER index is not offered as a swap into this one — "
      "that would sim two copies of an item the character owns one of")
check(all(r["slot"] == "trinket1" for r in t1["rows"].values()),
      "the addon files every trinket under trinket1, so every candidate reads that way")
check(len(t1["variants"]) == 13, f"13 trinket candidates (got {len(t1['variants'])})")


# ══ The regression test this whole tool exists for ══════════════════════════
if not SIMC_BIN.is_file():
    print(f"SKIP: no simc binary at {SIMC_BIN} — the firing-gate regression did NOT run. "
          "This is the one test that matters; build simc and re-run.")
else:
    data, _ = run_simc(profile,
                       {"iterations": 200, "fight_style": "Patchwerk",
                        "max_time": 300, "desired_targets": 1},
                       RESULTS, "regression")  # raw/, gitignored
    findings = firing_gate(export, ref, data)
    fails = [f for f in findings if f["level"] == "FAIL"]

    storm = [f for f in findings if "Stormbound" in f["item"]]
    check(storm, "Stormbound Emblem of Dazar produces a finding at all")
    if storm:
        f = storm[0]
        check(f["level"] == "FAIL",
              f"Stormbound is a FAIL, not a warning (got {f['level']})")
        check(f["observed"] == 0.0,
              f"Stormbound fired ZERO times under the upstream APL (got {f['observed']})")
        check(f["forced"] and f["forced"] > 0,
              "and the forced probe proves it is NOT an engine gap — simc models the "
              "effect fine, the APL simply never presses it")
        check(f["expected"] and f["expected"] > 2,
              "expected uses derived from the effect spell's 120s cooldown")

    flask = [f for f in findings if "Freightrunner" in f["item"]]
    check(flask and flask[0]["level"] == "WARN",
          "Freightrunner's Flask under-fires (1 of ~3.3) — a WARN, not a FAIL")

    check(fails, "the run FAILS the gate — `check` must exit non-zero on this export")
    check(not leak_gate(export, built, data),
          "no reference-profile gear leaked into the run")


# ══ Phase 4 — upgrade tracks, crests and the rank ladder ═════════════════════
#
# All offline: no simc binary, no /ps dump, no network. Tracks are injected by hand so
# the enumeration, watermark and budget logic is testable on a fixture that carries no
# track data of its own (which is itself the point — the export never does).

# ── The transcribed tables, checked against the fixture's own lines ──────────
cur = parse_upgrade_currencies(export)
by_id = {r["id"]: r for r in cur}
check(len(cur) == 7, f"all 7 upgrade_currencies entries parsed (got {len(cur)})")
check(by_id[3444]["count"] == 140 and by_id[3444]["track"] == "Champion",
      "140 Champion Mistcrests — the acceptance case, off c:3444")
check(by_id[3444]["name"] == "Champion Mistcrest", "crest names come from extras.lua's own map")
check(crest_balances(export) == {"Adventurer": 186, "Veteran": 169, "Champion": 140,
                                 "Hero": 28, "Myth": 20},
      "every Mistcrest balance, and ONLY the crest rows")
check(by_id[268552]["name"] == "Ascendant Voidcore" and by_id[268552]["kind"] == "i",
      "the `i:` rows are upgrade ITEMS, named from extras.lua — simc's item table has none of them")
check(not any(r["track"] for r in cur if r["kind"] == "i"),
      "an upgrade item is never mistaken for a crest track")
check(all(item_names().get(i) is None for i in UPGRADE_ITEMS),
      "UPGRADE_ITEMS exists BECAUSE simc's own item table carries none of these ids")
check(set(CREST_CURRENCIES) == {3442, 3443, 3444, 3445, 3446},
      "the five S2 Mistcrest currency ids")
check(not (set(CREST_CURRENCIES) & set(LEGACY_CREST_CURRENCIES)),
      "S1 Dawncrest ids are a DISJOINT set — that separation is the season-drift gate")
check(not any(r["legacy"] for r in cur),
      "this export carries no S1 Dawncrest row, so no season-drift warning")

legacy = parse_upgrade_currencies({"upgrade_currencies": "c:3343:99/c:3444:5"})
check(legacy[0]["legacy"] and legacy[0]["name"] == "Champion Dawncrest",
      "an S1 Dawncrest id in an export IS flagged — the silent zero that broke goalboard.py")

ach = parse_upgrade_achievements(export)
check(ach == [42767, 42768, 42769, 61809], f"upgrade_achievements parsed (got {ach})")
check(all(i in DAWN_ACHIEVEMENTS for i in ach),
      "every achievement this character holds is a Season 1 \"…of the Dawn\"")
disc = discount_state(export)
check(not any(d["earned"] for d in disc.values()),
      "NO \"…of the Mist\" achievement → no 50% discount, derived from the export")
check(disc["Champion"]["s1_only"] and disc["Champion"]["mist_id"] == 62412,
      "Champion of the Dawn is held and grants nothing against Mistcrests; the S2 id is 62412")
check(disc["Myth"]["s1_only"] is False,
      "Myth of the Dawn was NOT earned, so it is not reported as an inert S1 credit")
check(set(MIST_ACHIEVEMENTS) == {62410, 62411, 62412, 62414, 62416},
      "the five \"…of the Mist\" ids (extras.lua:438-447 ∩ dawncrests.md:195-205)")

# ── The track table: endpoints are Tier-1, intermediates are flagged ─────────
check(TRACKS["Champion"] == (292, 308) and TRACKS["Myth"] == (318, 334),
      "S2 track endpoints, verbatim from dawncrests.md:53-64")
check(len(TRACKS) == 5 and TRACK_STEPS == 6, "five tracks, six steps")
for track, (base, cap) in TRACKS.items():
    lo, lo_i = track_ilvl(track, 1)
    hi, hi_i = track_ilvl(track, TRACK_STEPS)
    check((lo, hi) == (base, cap), f"{track} 1/6 and 6/6 are the table's own endpoints")
    check(not lo_i and not hi_i, f"{track} endpoints are NOT flagged as interpolated")
    check(all(track_ilvl(track, s)[1] for s in range(2, TRACK_STEPS)),
          f"{track} intermediate steps ARE flagged ~interp")
    check([track_ilvl(track, s)[0] for s in range(1, TRACK_STEPS + 1)]
          == sorted(track_ilvl(track, s)[0] for s in range(1, TRACK_STEPS + 1)),
          f"{track} ilvls increase monotonically with step")
check(track_ilvl("Champion", 5)[0] == 305,
      "Champion 5/6 interpolates to 305 — which is what Encomplete's trinket2 actually "
      "wears at Champion 5/6, so the model is corroborated at that step")
check(track_ilvl("Champion", 4, cap=8)[0] != track_ilvl("Champion", 4)[0],
      "a non-6-step cap stretches the ladder rather than being silently ignored")

# ── Rank enumeration: stops at cap, never infers a track from an ilvl ────────
tracks_none = {}
ranks, unresolved = upgrade_ranks(export, tracks_none)
check(not ranks, "no track data → no ranks at all; nothing is guessed")
check({u["slot"] for u in unresolved} ==
      {s for s in export["equipped"] if s not in ("shirt", "tabard")},
      "every equipped, non-cosmetic slot is reported UNRESOLVED TRACK")
ambiguous = [s for s, e in export["equipped"].items() if e.get("ilvl") in (295, 305)]
check(ambiguous and all(any(u["slot"] == s for u in unresolved) for s in ambiguous),
      "the provably ambiguous ilvls (295 = Veteran 6/6 OR Champion 2/6; 305 = Champion "
      "6/6 OR Hero 1/6) are UNRESOLVED, not inferred")

ranks, unresolved = upgrade_ranks(
    export, {"trinket2": {"track": "Champion", "level": 5, "cap": 6}})
check(len(ranks) == 1 and ranks[0]["step"] == 6 and ranks[0]["ilvl"] == 308,
      "Champion 5/6 leaves exactly one rank, targeting the Tier-1 ceiling 308")
check(not ranks[0]["interpolated"], "…and 6/6 is an endpoint, so it is not ~interp")
check(rank_name(ranks[0]) == "trinket2 Champion 6/6 308", "the rank's profileset name")
ov = rank_variants(ranks)["trinket2 Champion 6/6 308"]["trinket2"]
check(ov.endswith(",ilevel=308") and ov.startswith(export["equipped"]["trinket2"]["item_string"]),
      "a rank restates the FULL item line plus ilevel= — a profileset slot line REPLACES, "
      "it does not merge (option.cpp:188-196)")
check(not introduces_effects(export, {"trinket2": ov}),
      "the same item at a higher ilvl introduces no NEW effect, so a rank needs no "
      "validation run")

capped, _ = upgrade_ranks(export, {"hands": {"track": "Hero", "level": 6, "cap": 6}})
check(not capped, "a slot already at 6/6 yields no ranks")
full, _ = upgrade_ranks(export, {"head": {"track": "Veteran", "level": 1, "cap": 6}})
check(len(full) == 5 and [r["step"] for r in full] == [2, 3, 4, 5, 6],
      "enumeration runs level+1 .. cap and stops there")
bogus, unres = upgrade_ranks(export, {"head": {"track": "Warband", "level": 1, "cap": 6}})
check(not bogus and any("not one of the five" in u["why"] for u in unres),
      "a track name the KB table does not carry is UNRESOLVED, not coerced")

# ── The watermark rule ──────────────────────────────────────────────────────
check(redundancy_slot(None, "hands") == "Hand" and redundancy_slot(None, "back") == "Cloak",
      "canon slot → Enum.ItemRedundancySlot name")
check(redundancy_slot(None, "finger2") == "Finger"
      and redundancy_slot(None, "trinket1") == "Trinket",
      "BOTH indices of a paired slot map to the single Finger/Trinket row")
mh = export["equipped"]["main_hand"]["item_id"]
check(redundancy_slot(mh, "main_hand") == "Twohand",
      "the redundancy enum splits weapons by HAND COUNT: Encomplete's 2H is Twohand, "
      "which is the row reading 318")
mark = watermark_for(export, "trinket2")
check(mark and mark["character"] == 305 and mark["paired"],
      "trinket2's watermark is the Trinket row at 305, flagged paired")
check(watermark_for(export, "main_hand")["character"] == 318,
      "main_hand resolves to Twohand 318, matching the 318 weapon actually worn")

free_case, _ = upgrade_ranks(
    export, {"feet": {"track": "Veteran", "level": 3, "cap": 6}})  # feet worn at 285
check([r["ilvl"] for r in free_case] == [289, 292, 295],
      f"Veteran 4/6..6/6 target 289/292/295 (got {[r['ilvl'] for r in free_case]})")
check([r["free"] for r in free_case] == [False, False, False],
      "…and none is free: the Feet watermark is 285, below every one of them")
wm_case, _ = upgrade_ranks(
    export, {"head": {"track": "Veteran", "level": 1, "cap": 6}})  # Head watermark 295
check([r["free"] for r in wm_case] == [True, True, True, True, True],
      "every Veteran rank on head is free — the Head watermark is already 295, the "
      "track's own ceiling (dawncrests.md:215-232, in-game 2026-08-19)")
paired_case, _ = upgrade_ranks(
    export, {"finger1": {"track": "Champion", "level": 1, "cap": 6}})  # Finger row = 295
check([r["ilvl"] for r in paired_case] == [295, 298, 302, 305, 308],
      f"Champion 2/6..6/6 (got {[r['ilvl'] for r in paired_case]})")
check([r["free"] for r in paired_case] == [True, False, False, False, False],
      "a PAIRED slot rides free only to the single Finger row (295) — the adopted "
      "second-highest rule. Note 305 is NOT free even though a 305 ring is worn in "
      "finger2: that is the whole content of the rule.")
check(all(r["watermark"]["paired"] for r in paired_case),
      "…and every such rank carries the paired flag, so the output can label it UNVERIFIED")

# ── The ilvl-fidelity gate ──────────────────────────────────────────────────
truthful = {"gear": {s: {"ilevel": e["ilvl"]}
                     for s, e in export["equipped"].items() if e.get("ilvl")}}
check(not ilvl_fidelity_gate(export, truthful),
      "a baseline resolving to the export's own ilvls passes the fidelity gate")
lying = {"gear": dict(truthful["gear"], head={"ilevel": 999})}
bad = ilvl_fidelity_gate(export, lying)
check(len(bad) == 1 and bad[0]["slot"] == "head" and bad[0]["resolved"] == 999,
      "a single mis-resolved slot FAILS the gate — proved live on 2026-08-20 against a "
      "doctored export, since it passes on all 15 real slots")
check(not ilvl_fidelity_gate(export, {"gear": {}}),
      "a slot simc did not report is not fabricated into a failure")

# ── Budget + allocation ─────────────────────────────────────────────────────
check(CREST_COST_PER_RANK == 20 and CREST_COST_DISCOUNTED == 10,
      "flat 20 per rank, 10 at the 50% discount (dawncrests.md:84-89, Tier-3)")
check(140 // CREST_COST_PER_RANK == 7,
      "140 Champion Mistcrests ÷ 20 = 7 ranks — the acceptance arithmetic")

ladder, _ = upgrade_ranks(export, {"head": {"track": "Veteran", "level": 1, "cap": 6}})
# Cumulative Δ vs current gear, i.e. what one frame actually reports. The marginal gain
# of step 4 is deliberately the largest, so a naive sort on Δ would order these wrong.
cum = {"head Veteran 2/6 282": 0.5, "head Veteran 3/6 285": 0.8,
       "head Veteran 4/6 289": 1.9, "head Veteran 5/6 292": 2.1,
       "head Veteran 6/6 295": 2.3}
deltas = {n: {"delta_pct": v, "err_pct": 0.05, "verdict": "significant"}
          for n, v in cum.items()}
picked = allocate(ladder, deltas, {"Veteran": 3})
check([r["step"] for r in picked] == [2, 3, 4],
      "ranks STACK: 4/6 cannot be bought without 2/6 and 3/6, so the ladder is walked "
      "in order however tempting the later rung")
check(abs(picked[2]["marginal_pct"] - 1.1) < 1e-9,
      "the reported gain is MARGINAL (1.9 − 0.8), not the cumulative Δ")
check(len(allocate(ladder, deltas, {"Veteran": 99})) == 5, "a budget larger than the ladder buys it all")
check(allocate(ladder, deltas, {"Veteran": 0}) == [], "a zero budget buys nothing")

flat = {n: {"delta_pct": 0.0, "err_pct": 0.05} for n in cum}
check(allocate(ladder, flat, {"Veteran": 3}) == [],
      "a rank with no positive marginal gain is not bought just because it is affordable")

# THE property that makes the Tier-3 cost figure safe to quote: because cost is uniform
# across ranks, it sets the COUNT and nothing else. Halve it and the ORDER is identical.
order_20 = [rank_name(r) for r in allocate(ladder, deltas, {"Veteran": 140 // CREST_COST_PER_RANK})]
order_10 = [rank_name(r) for r in allocate(ladder, deltas, {"Veteran": 140 // CREST_COST_DISCOUNTED})]
check(order_10[:len(order_20)] == order_20,
      "rank ORDER is independent of the per-rank cost constant — which is why the order "
      "is not branded [Tier-3 est] and the counts are")


# ⚠ The regression that a real character found on 2026-08-20: budgets are PER TRACK and
# must never be pooled. Encomplete held 186 Adventurer + 139 Veteran + 20 Myth crests and
# ZERO Champion — and the first version summed those into "16 ranks" and then spent all
# 16 on Champion ranks. Every row was individually true and the plan was unbuyable.
# A slot carries ONE track, so the Champion rungs go on a different slot — modelling
# two tracks on one slot would test something the game cannot produce.
mixed = ladder + [dict(r, track="Champion", slot="chest") for r in ladder]
mixed_deltas = dict(deltas)
for r in mixed:
    mixed_deltas.setdefault(rank_name(r), {"delta_pct": 9.0, "err_pct": 0.05})
broke = allocate(mixed, mixed_deltas, {"Veteran": 2, "Champion": 0})
check(all(r["track"] == "Veteran" for r in broke) and len(broke) == 2,
      "a rank is bought ONLY out of its own track's pool — a track with zero crests "
      "contributes nothing, however large its delta")
check(len(allocate(mixed, mixed_deltas, {"Veteran": 0, "Champion": 0})) == 0,
      "no crests in any track in scope buys nothing at all")


# ══ Phase 5 — the cast timeline ══════════════════════════════════════════════
#
# Offline against a hand-written log fragment in simc's own format. The real acceptance
# (five Tyrant windows, zero on-use presses in any of them) needs the binary and is run
# by hand; everything the PARSER and the WINDOW logic do is checkable here.

SAMPLE_LOG = """0.000 Enemy 'Fluffy_Pillow' arises. Spawn Index=0
0.000 Raid gains Buff 'arcane_intellect' (1459) (stacks=1) (value=0.03)
0.000 Player 'Encomplete' performs Action 'demonbolt' (264178) (262500)
0.000 Player 'Encomplete' consumes 5000 mana for Action 'demonbolt' (264178) (257500)
0.000 Player 'Encomplete' schedules travel (0.857) for Action 'demonbolt' (264178)
1.314 Player 'Encomplete' performs Action 'call_dreadstalkers' (104316) (261295)
1.314 Player 'Encomplete' summons dreadstalker for 15.140s.
3.405 Player 'Encomplete' schedules execute for Action 'summon_demonic_tyrant' (265187)
4.413 Player 'Encomplete' performs Action 'summon_demonic_tyrant' (265187) (260805)
4.413 Player 'Encomplete' summons demonic_tyrant for 20.272s.
4.413 Player 'Encomplete' gains Buff 'tyrant' (0) (stacks=1) (value=-2.2e-308)
4.413 Player 'Encomplete' loses Buff 'casting' (0)
5.319 Player 'Encomplete_demonic_tyrant' performs Action 'burning_cleave' (1264093) (200)
5.401 Player 'Encomplete_demonic_tyrant' refreshes demonic_power_5 (value=0.1)
6.851 Player 'Encomplete' dismisses wild_imp
24.685 Player 'Encomplete' dismisses demonic_tyrant
40.000 Player 'Encomplete' gains Buff 'freightrunners_flask' (1250533) (stacks=1) (value=1)
66.090 Player 'Encomplete' performs Action 'summon_demonic_tyrant' (265187) (260805)
not a log line at all
"""

ev = parse_log(SAMPLE_LOG)
kinds = [e["kind"] for e in ev]
check(len(ev) == 13, f"13 actionable events parsed from 19 lines (got {len(ev)})")
check("schedules travel" not in "".join(e["raw"] for e in ev)
      and not any("schedules execute" in e["raw"] for e in ev)
      and not any("refreshes" in e["raw"] for e in ev),
      "the high-volume bookkeeping verbs (schedules execute/travel, refreshes) are "
      "dropped — they are ~60% of a log and say nothing about ORDER")
check(kinds.count("cast") == 5 and kinds.count("summon") == 2
      and kinds.count("dismiss") == 2 and kinds.count("consume") == 1
      and kinds.count("buff") == 2 and kinds.count("buff_end") == 1,
      f"event kinds tallied (got {ev and kinds})")
check([e["t"] for e in ev] == sorted(e["t"] for e in ev), "events stay in log order")
check(ev[0]["action"] == "demonbolt" and ev[0]["spell"] == "264178",
      "log_spell_id puts a traceable spell id on every cast row")
check(any(e["kind"] == "buff" and e["buff"] == "tyrant" for e in ev),
      "buff gains are parsed even though the default view hides them")
check(not any(e.get("actor") == "" for e in ev),
      "the unquoted `Raid gains Buff` line does not parse as an empty actor")

vocab = log_actions(ev, "Encomplete")
check(vocab == {"demonbolt": 1, "call_dreadstalkers": 1, "summon_demonic_tyrant": 2},
      f"the action vocabulary is the PLAYER's own casts only (got {vocab})")
check("burning_cleave" not in vocab,
      "a pet's cast is not offered as an --around anchor for the player")

# ── Windows ─────────────────────────────────────────────────────────────────
wins = log_windows(ev, "Encomplete", "summon_demonic_tyrant", 5.0, None)
check(len(wins) == 2, f"one window per cast of the anchor (got {len(wins)})")
check(abs(wins[0]["span"] - 20.272) < 1e-6 and "demonic_tyrant" in wins[0]["span_source"],
      "the window length comes from the anchor's OWN summon duration in the log — "
      "hardcoding 20s would be a Demonology special case in a tool that has none")
check(abs(wins[0]["start"] - (4.413 - 5.0)) < 1e-9 and abs(wins[0]["end"] - 24.685) < 1e-3,
      "the window spans --before seconds of lead-in to the end of the summon")
check(wins[1]["span"] == 15.0 and "15s default" in wins[1]["span_source"],
      "a cast that summons nothing falls back to 15s, and SAYS which it used")
check(log_windows(ev, "Encomplete", "summon_demonic_tyrant", 5.0, 3.0)[0]["span"] == 3.0,
      "--after overrides the derived span")
check(log_windows(ev, "Encomplete", "burning_cleave", 5.0, None) == [],
      "an action the player never cast yields no windows rather than a pet's")

rows = window_events(ev, wins[0], "Encomplete", pets=False, buffs=False)
check(all(r["actor"] == "Encomplete" for r in rows),
      "the default view is the character's own events only")
check(not any(r["kind"] in ("buff", "buff_end") for r in rows),
      "…and hides buffs until --buffs asks for them")
check(all(wins[0]["start"] <= r["t"] <= wins[0]["end"] for r in rows),
      "every row is inside the window")
petted = window_events(ev, wins[0], "Encomplete", pets=True, buffs=True)
check(any(r["actor"] == "Encomplete_demonic_tyrant" for r in petted),
      "--pets admits `<char>_<pet>` actors")
check(any(r["kind"] == "buff" for r in petted), "--buffs admits buff rows")
check(len(petted) > len(rows), "both flags only ever ADD rows")

line = _log_line(ev[0], 4.413, "Encomplete")
check("CAST" in line and "-4.413" in line, "a row carries its offset from the anchor")
check("[demonic_tyrant]" in _log_line(
          next(e for e in ev if e["actor"] == "Encomplete_demonic_tyrant"),
          4.413, "Encomplete"),
      "a pet row is labelled with the pet, not the full `<char>_<pet>` actor string")

# ── The structural guarantees ───────────────────────────────────────────────
opts = log_options(LOG_SEED, 1, 300)
check(opts["iterations"] == 1 and opts["threads"] == 1,
      "a timeline is ONE iteration on ONE thread — there is no flag to raise either, "
      "so it cannot quietly become a statistical run")
check(opts["deterministic"] == 1 and opts["seed"] == LOG_SEED,
      "deterministic + a fixed seed, so `reproduce the window` is an instruction "
      "someone can actually follow (verified: two runs, identical md5)")
check(opts["log"] == 1 and opts["log_spell_id"] == 1,
      "logging on, with spell ids")
check("NOT A DPS RESULT" in LOG_BRAND,
      "every timeline row is branded — a row copied out of the table must carry the "
      "warning with it, the same rule the DPS tables follow")

# ── effect_subjects is now SHARED with the firing gate ──────────────────────
subs = effect_subjects(export)
check(len(subs) == 2 and {s["slot"] for s in subs} == {"trinket1", "trinket2"},
      f"Encomplete's two effect-bearing items (got {[s['slot'] for s in subs]})")
storm_sub = next(s for s in subs if "Stormbound" in s["item"])
check(storm_sub["on_use"] and storm_sub["cooldown"] and storm_sub["cooldown"] > 0,
      "Stormbound is an on-use with a real cooldown — one row, not two, even though "
      "it ships an on-use AND an equip effect under the same name")
check(storm_sub["spell_id"] in storm_sub["ids"] and storm_sub["keys"],
      "each subject carries the keys and ids that identify it in a report OR a log — "
      "the same matcher the firing gate uses, so the two cannot disagree")

# ══ Character overrides — the two declared exceptions, and their fences ══════

REF = {"text": "actions.precombat+=/variable,name=trinket_priority,value=1\n"
               "actions+=/demonbolt\n"}

ok, bad = resolve_overrides(REF, {"variables": {
    "trinket_priority": {"value": 2, "why": "w", "measured": "2026-08-20"}}})
check(len(ok) == 1 and ok[0]["value"] == 2.0, "a declared variable is accepted")
_, bad = resolve_overrides(REF, {"variables": {
    "invented_variable": {"value": 2, "why": "w", "measured": "2026-08-20"}}})
check(len(bad) == 1 and "does not declare" in bad[0],
      "a variable the UPSTREAM reference does not declare is REJECTED — an override may "
      "re-point a decision upstream already makes, never invent behaviour")
_, bad = resolve_overrides(REF, {"variables": {"trinket_priority": {"value": 2}}})
check(len(bad) == 1 and "superstition" in bad[0],
      "no `why`/`measured` → rejected; an unmeasured override is a superstition")
_, bad = resolve_overrides(REF, {"variables": {
    "trinket_priority; actions=chaos_bolt": {"value": 1, "why": "w", "measured": "d"}}})
check(len(bad) == 1, "a variable NAME cannot smuggle an action past the parser")

TY = "use_item,use_off_gcd=1,slot=trinket2,if=pet.demonic_tyrant.active"
ok, bad = resolve_apl_append({"apl_append": [
    {"line": TY, "why": "w", "measured": "2026-08-20"}]})
check(len(ok) == 1 and ok[0]["line"] == TY, "a use_item rung with use_off_gcd=1 is accepted")
_, bad = resolve_apl_append({"apl_append": [
    {"line": "use_item,slot=trinket2", "why": "w", "measured": "d"}]})
check(len(bad) == 1 and OFF_GCD in bad[0],
      "use_off_gcd=1 is MANDATORY — failure #2 was exactly this line without it, and it "
      "baked -3.2% into every forced run for a day")
_, bad = resolve_apl_append({"apl_append": [
    {"line": "chaos_bolt,if=1", "why": "w", "measured": "d"}]})
check(len(bad) == 1 and "use_item" in bad[0],
      "only use_item may be appended — this can never become 'rewrite the rotation', "
      "which failure #3 showed swings 3.21% on ordering alone")
_, bad = resolve_apl_append({"apl_append": [
    {"line": "use_item,use_off_gcd=1,slot=trinket1\nactions=chaos_bolt",
     "why": "w", "measured": "d"}]})
check(len(bad) == 1, "a newline cannot smuggle a second action line through")

check(override_brand({"overrides": [{"name": "trinket_priority"}]}).startswith("⚠ OVERRIDE"),
      "a variable override brands every row")
check("APL-APPEND" in override_brand({"apl_append": [{"line": TY}]}),
      "an appended action brands LOUDER — it adds a press upstream would not make")
check(override_brand({}) == "", "no override, no brand")

live = load_overrides("encomplete")
check(live.get("apl_append") and len(live["apl_append"]) == 2,
      "Encomplete's two trinket rungs are installed (this is what took the firing gate "
      "from FAIL to PASS on 2026-08-20)")
check(all(OFF_GCD in a["line"] and a.get("measured") for a in live["apl_append"]),
      "…and both carry use_off_gcd=1 and a measurement date")
check(load_overrides("nobody") == {} and load_overrides(None) == {},
      "an unknown character degrades to 'upstream unaided', never to a crash")


if _fails:
    print(f"FAIL ({len(_fails)}/{_total})")
    for m in _fails:
        print(f"  - {m}")
    sys.exit(1)
print(f"OK ({_total} checks)")
