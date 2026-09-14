---
name: optimize-gear
description: >-
  Decide what a character should equip, take from the Great Vault, or spend crests on —
  by simming it, never by eyeballing item level. Use for "which vault item should I take",
  "is this an upgrade", "what should I equip", "which trinket/weapon is better", "should I
  upgrade X or Y", "help me optimize <char>'s gear". Requires a fresh `/simc` export and
  refuses without one. NOT for "what should I do this session" (that's /plan-character) and
  not for rotation/talent questions.
---

# Optimizing gear — sim it, don't eyeball it

**The rule this skill exists to enforce: item level does not decide gear questions.**
Track, tier-set membership, weapon layout, unmodelled procs and crest economics all
routinely outweigh a double-digit ilvl gap, and they point in different directions. On
2026-09-09 a session recommended a vault item from a "+46 ilvl" reading that was wrong on
four independent counts. That session is the reason this file exists; its post-mortem is
`tools/docs/wowkb-sim.md` → Field log, 2026-09-10.

Read `tools/docs/wowkb-sim.md`'s **Field log before designing a comparison, and append to
it after** — that is a standing obligation of `wowkb.sim`, not optional politeness.

---

## Gate 0 — REFUSE without a fresh `/simc` export

The export is the **single input door** and it is the only source for three things
nothing else carries:

- **`### Weekly Reward Choices`** — the vault options. Not in the Blizzard API, not in the
  PlannerState dump. (Field-log failure #8 was skipping this block entirely.)
- **Bag item levels** — they exist nowhere on disk; the Syndicator/DBC path was tried on
  2026-08-20 and dead-ends.
- **`bonus_id` per item** — which is what track resolution needs (see Step 2).

If the user has not pasted one, **stop and ask for it**: in game, `/simc`, copy, paste.
Do not substitute `wowkb.character`, the API, or a previous export. Then:

```bash
cd tools && uv run python -m wowkb.sim import <path|->     # stores under raw/simc-exports/
cd tools && uv run python -m wowkb.sim check <char>        # harness health, NO DPS, run it every time
```

**Check the export's own date line** against today. It is a snapshot: a user who has
looted, swapped or upgraded since is asking about a character that no longer exists.

⚠ **The export outranks the PlannerState dump on conflict.** On 2026-09-09 the dump was
*newer* than the export and still disagreed on three slots; the export was the internally
self-consistent one. Use the dump for reset-state, not for item facts.

---

## Step 1 — Resolve the TRACK of every candidate, before ranking anything

**Never compare two items by item level.** The bands overlap by design: a capped
Champion 6/6 (308) and a fresh Hero 1/6 (305) are three ilvl apart today and *sixteen*
apart at their ceilings. That gap is usually the whole answer.

Track and step are recoverable from `bonus_id` — this is a **join, not arithmetic**:

```
bonus_id → ItemBonusListGroupEntry.(ItemBonusListGroupID, SequenceValue)
           SequenceValue IS the step;  the group IS the track
           ItemBonusListGroup.ItemGroupIlvlScalingID = the SEASON (11 = S1, 12 = S2)
```

Season 2 (12.1) groups, verified against build 12.1.0.69214 — see
`knowledge/endgame/dawncrests.md` for the sourced claim and the endpoints:

| group | track | bonus ids | 1/6 → 6/6 |
|---|---|---|---|
| 614 | Adventurer | 12817-12824 | 266 → 282 |
| 615 | Veteran | 12825-12832 | 279 → 295 |
| 616 | Champion | 12833-12840 | 292 → 308 |
| 617 | Hero | 12841-12848 | 305 → 321 |
| 618 | Myth | 12849-12856 | 318 → 334 |

Steps 7/8 in each block carry `Flags = 3` and are disabled placeholders — the `/6`
denominator is real. **Do not hardcode these bases in code**; regenerate per build from
`raw/wago/ItemBonusListGroupEntry-<build>.csv` + `ItemBonus-<build>.csv`
(`uv run python -m wowkb.wago ItemBonusListGroupEntry`). An id outside the S2 groups is
usually a *previous season's* track — S1 group 611 = Hero, and an S1 leftover in a slot is
itself a finding worth surfacing.

Report every candidate as **`<track> <step>/6 (<ilvl>), ceiling <n>`**. Never bare ilvl.

---

## Step 2 — Filter to what the character can LEGALLY equip

`wowkb.sim` does **not** do this for you, and simc will sim an impossible loadout to a
confident, plausible, wrong number. `gear` prints a `⚠ WEAPON SLOT — NOT usability-checked`
banner; `compare` prints nothing at all. Until the pre-flight layout gate is built
(field log 2026-09-10, gate #1), **this step is manual and it is not optional**:

```bash
# inv_type / class / subclass / speed for any candidate id
grep --no-ignore-files -n '"<Item Name>"' raw/addon-research/simc/engine/dbc/generated/item_data.inc
# fields after the flags: ... quality, INV_TYPE, item_class, item_subclass, bind, delay ...
```

- `inv_type 17` = **INVTYPE_2HWEAPON**. A shield user (Prot Paladin/Warrior, Guardian in
  some forms) cannot use it. simc will still equip it *alongside* the shield and pay out
  roughly double weapon damage — this is exactly how the 2026-09-09 run ranked a 295
  two-hander above a 321 one-hander and looked reasonable doing it.
- `inv_type 13` = 1H either hand · `21` = main-hand only · `22`/`23` = off-hand/held.
- simc carries **no class weapon-usability data at all** (`class_mask` is never read for
  equip validation), so plate/str-vs-agi and class restrictions are on you.
- The addon files **every** ring under `finger1` and **every** trinket under `trinket1`
  regardless of destination — and the indices are not interchangeable, because upstream's
  `damage_trinket_priority` tie-breaks to `trinket1`.

**A candidate that fails this step is struck from the table entirely — not ranked with a
caveat.** A wrong row that wins is worse than no row.

---

## Step 3 — One question, ONE invocation

Deltas across separate simc runs are meaningless (field-log failure #4 recommended the
wrong vault item on exactly this). The tool structurally refuses to print one.

- **Same slot, several candidates** → `wowkb.sim gear <char> --slot <slot>`.
- **Cross-slot** ("the helm or the sword?") → `wowkb.sim compare`, every option as a
  named variant in a **single** call. `gear --slot` cannot answer a cross-slot question,
  because two `gear` runs are two frames.

Hold everything not under test **identical across variants**. If the realistic main hand
in the "take the helm" world is a bag item, then that bag item must be in the helm variant
too — otherwise you are measuring the weapon, not the helm.

```bash
uv run python -m wowkb.sim compare <char> \
  "TAKE_SWORD=main_hand=@Abyss Sabre (305)" \
  "TAKE_HELM=head=@Warhelm (305); main_hand=@Swordsman's Emanation (295)" \
  "TAKE_NOTHING=main_hand=@Swordsman's Emanation (295)"
```

`@<Item Name>` pulls the item string from the export's own equipped/bag/vault rows; add
`(<ilvl>)` when a name appears twice. Names must match the export **exactly**, apostrophes
included. **Always include a do-nothing arm** — "the best thing I already own" is the real
baseline, and without it every option looks like a win against a slot the user was never
going to leave as-is.

---

## Step 4 — Sim BOTH the current track level AND the track ceiling

These routinely disagree, and both are decision-relevant: current answers *today*, capped
answers *what to spend crests on*. A fresh Hero piece that loses today may win at cap.

A rank is expressed by appending `,ilevel=<target>` to the item's own line (simc models no
part of the upgrade system). A profileset line **replaces the slot wholesale**, so restate
the full item string:

```
"TAKE_SWORD_cap321=main_hand=,id=251884,bonus_id=12841/6652,ilevel=321"
```

Label the aspirational rows clearly and cost them in Step 6 — a capped row the user cannot
afford for a month is not a recommendation.

---

## Step 5 — Read the firing gate, and read it precisely

`check`/`gear`/`compare` assert that every equipped effect actually fired. A silent no-op
is the characteristic failure of gear sims and is invisible without this.

Three outcomes, and they mean different things:

| gate says | means | what to do |
|---|---|---|
| effect fired ~expected | modelled and working | trust the number |
| **0 uses, no action exists** | simc has no implementation | number is **stats-only**; say so |
| **0 uses, action exists at 0 executes** | implemented but never triggered | number is a **FLOOR** — the item may be better |

⚠ The gate currently prints "produced no buff and no action" for **both** of the last two
(field log 2026-09-10). Confirm which you have by reading the JSON directly:

```bash
python3 -c "
import json; d=json.load(open('raw/sim-results/<tag>.json'))
for a in d['sim']['players'][0]['stats']:
    print(a['name'], a.get('num_executes',{}).get('mean'))"
```

An item whose proc never fires is **understated**, and if the margin against it is smaller
than the proc could plausibly be worth, the honest answer is "these are within the sim's
resolution", not a ranking.

---

## Step 6 — Cost it: crests, achievements, watermark

DPS-per-rank is only half the decision; the other half is whether they can pay.

Read straight from the export — never from the user's memory of another character:

- **`upgrade_currencies=c:3442:N/...`** → 3442 Adventurer · 3443 Veteran · 3444 Champion ·
  3445 Hero · 3446 Myth. **A track absent from the line is a zero balance.**
- **`upgrade_achievements=`** → the "…of the Mist" ids are **62410** Adventurer ·
  **62411** Veteran · **62412** Champion · **62414** Hero · **62416** Myth, and they are
  **warband-wide**: earning one on any character halves that track's cost for all of them.
  Season 1's Dawn ids (42767-42770, 61809) grant **nothing** against Mistcrests.
- **~20 crests per rank, 10 with the discount** (Tier-3; `dawncrests.md` flags it). Because
  the cost is uniform across ranks, ranking by DPS-per-crest is identical to ranking by
  DPS-per-rank — a wrong constant moves how many they can afford, not the order.
- **`slot_high_watermarks=`** is `Enum.ItemRedundancySlot : character : account`, **not**
  inventory slots and **not** (current, max). Same-character re-upgrade to the slot
  watermark is free; it does not cross to alts. `Finger` and `Trinket` are one row for two
  worn items and the rule there is unconfirmed — say so rather than costing it.

State plainly when a capped recommendation is unaffordable, and name the gap.

---

## Step 7 — Check the tier set before recommending any tier slot

On 2026-09-09, swapping the tier helm for a **higher-track** non-tier helm cost **~8.5
points of relative DPS** — the 4pc dwarfed the entire ilvl-and-track question. Head,
shoulder, hands, legs, chest are the usual set slots.

Before ranking a candidate in a set slot, state the resulting **set-piece count** for each
variant. Two items at identical ilvl and track are not comparable if one breaks 4pc. The
Catalyst is the escape hatch and in 12.1 conversion **inherits secondaries, tertiaries and
certain cantrips** (`knowledge/endgame/catalyst.md`), so catalyse the best-*stat* piece,
not the highest ilvl.

---

## Step 8 — Report

Give the ranked table with **both** fight styles (1T/300s and 5T/120s — they disagree on
ordering often enough that a single-style answer is never printed alone), medians with the
± band and the significance verdict, and then:

- the **recommendation in one line**, and what it beats and by how much *against the
  do-nothing arm*, not against a slot the user had already abandoned;
- every candidate **struck as unusable**, and why — that is often the actual finding;
- **track and ceiling** for each live option, not just ilvl;
- what the sim **could not model** (unfired procs, unmodelled trinkets, tank survivability
  — this ranks on DPS, which is a partial view for a tank);
- the **staleness stamp**: simc SHA + date, export date, and whether the client build is
  ahead of `knowledge/_meta/game-version.md`.

A sim result is **evidence for an answer, never a sourced claim** — results live in
`raw/sim-results/` (gitignored) and must not be written into `knowledge/**`.

---

## Then: append to the field log

`tools/docs/wowkb-sim.md` → Field log. The question asked, what the harness could not
express, what went wrong, and any new **GATE** the session earned. A session that revealed
nothing gets one line saying so. **When a sim gives a wrong answer the fix is a new gate —
never a hand-edited profile or APL.**
