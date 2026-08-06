---
title: Ability inventory — mined not written, and the rollout that is not done yet
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/_abilities/README.md  # tier 1 derived, the generated layer's schema
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the 1,578-claim adjudication
  - tools/wowkb/gen_abilities.py  # the generator
confidence: high
---

# Ability inventory — mined, not written

**Status 2026-08-06: the mining is DONE and committed. The prose rollout is BLOCKED
on two small tool changes and one decision from Mike.**

Read this file before touching `knowledge/classes/*/*/abilities.md` or
`tools/wowkb/gen_abilities.py`.

---

## 0. The one-paragraph version

40 hand-written `abilities.md` files restated, per ability, what game data already
knows: name, spellID, cooldown, and a description. Nobody had ever reconciled them
against game data, so they had drifted — dead expansions' abilities, wrong-spec
attributions, 461 `@verify-ingame` markers most of which asked questions that
logging in could never answer. The fix is to **mine the facts and let prose be
prose**. The mining shipped. What has not shipped is stripping the now-redundant
restatement out of the 40 prose files, because two facts still have no generated
home and a rollout today would destroy them.

---

## 1. The target model (Mike's design — this is the north star)

Four bands of decreasing confidence:

1. **Base spell list per class/spec** — mined.
2. **Base talent list** — mined.
3. **Validated but not directly joined** — reachable only indirectly, corroborated
   by a good source. Known accurate.
4. **Un-mined / uncorroborated** — a plain list with provenance and nothing else.

⚠ **Section 4 must not trigger investigation.** It is a catalogue, not a backlog.
An entry is researched when someone **asks**, or when real work needs that specific
ability — the same use-not-age trigger as `projects/addon-lab/docs/lab-process.md`.

**On descriptions** (Mike, 2026-08-06, verbatim): *"I'm ok with it just literally
transcribing the in-game ability description for the spellid, which should be
accessible. Rotation hints, or strategy seems outside the scope of these ability
inventories."* — `rotation.md`, `builds.md` and `gearing.md` already exist as
siblings and own that material.

---

## 2. What is DONE and committed

Seven commits, `b66df73`..`7b03190`, all on `main`.

| commit | what |
|---|---|
| `b66df73` | M2a addon-dev (unrelated workstream, separated out) |
| `1fefcef` | `spec_inventory` — build pin, passive-filter fix, declared class kit line |
| `3f85bcd` | `gen_abilities.py` + 83 generated files + `reconcile-ledger.md` |
| `4a7c437` | sections 3 and 4 (the override walk + the residual probe) |
| `9ecf34b` | the 61 adversarial-verification findings fixed in the 40 prose files |
| `3286a76` | the "not in any data table" correction (Hammer of Light) |
| `7b03190` | descriptions transcribed from game data |

### The generated layer

`tools/wowkb/gen_abilities.py` writes **88 files**, every DB2 read pinned to
`12.0.7.67808`, hard-failing on a miss:

- `knowledge/classes/<class>/<spec>/ability-inventory.{tsv,md}` × 40 — 7,065 rows.
- `knowledge/classes/_abilities/all-abilities.tsv` — grep across all 40 specs.
- `_abilities/pet-family-annex.tsv` — 255 rows, pet skill lines.
- `_abilities/spell-descriptions.tsv` — 3,949 rows, the description join table.
- `_abilities/spell-descriptions.json`, `_abilities/residual-probe.json` — the two
  committed network caches (see §6).
- `_abilities/section-3-corroborated.{tsv,md}` — 36 rows.
- `_abilities/section-4-catalogue.{tsv,md}` — 126 rows.
- `_abilities/README.md` — the schema and the join model.

**`abilities.md` is NEVER generated.** The generated per-spec file is
`ability-inventory.md`.

### Descriptions — two sources, complementary

| | DB2 `Spell.Description_lang` @ 67808 | Blizzard `/data/wow/spell/{id}` |
|---|---|---|
| coverage | **99.6%** (7,039/7,065), pets included | 98.1%, **pets 0/6**, cdm-only 39% |
| readable as-is | **no** — 91% templated | **yes**, resolved English |
| offline / pinned | **yes** | no — cached, see §6 |

DB2 is the **spine**, the API is the **rendering**. Every row carries
`description_source` so a reader can tell resolved prose from a raw template.
`$@spelldesc<id>` redirects are followed, cycle-guarded, depth 4 (max observed 1).
Result: `api` 6,928 · `db2-template` 57 · `db2-template+redirect` 27 ·
`db2-plain` 20 · `+redirect-unresolved` 7 · `none` 26.

The annex gets the same treatment: 239/255, almost all DB2 template.

---

## 3. ⛔ THE TWO BLOCKERS — do these before any rollout

### B1. `cost` and `cast_time` have no generated home

**This is the hard blocker.** There is no cost column and no cast-time column, and
the API tooltips state only what a spell **generates** ("Generates 3 Holy Power",
"Generates 10 Rage") — **never what it costs**.

So the `Resource` and `Cast / CD` columns of the 40 prose files are the **only**
record of:

- Holy Power / Rage / Energy / mana costs across all 40 specs.
- Cast times. "Flash Heal 1.5s vs Prayer of Healing ~2s vs Divine Hymn 8s channel"
  is a healer's whole decision surface.

A "delete the restated columns" pass destroys both. Sources are already on disk:

- cost → `raw/wago/SpellPower.csv` (⚠ **unversioned** — refetch pinned:
  `uv run python -m wowkb.wago SpellPower --build 12.0.7.67808`)
- cast time → `SpellMisc.CastingTimeIndex` → `SpellCastTimes` (fetch pinned)

### B2. The `## Inventory` heading match is dark for 18 of 40 specs

**`abilities.md` is a MACHINE INPUT and this is not obvious from reading it.**

`gen_abilities._inventory_names()` (~line 1908) harvests the **first column of the
table under a heading whose text `.lower().startswith("inventory")`** and feeds it
to `residual()` → the `prose-only` leg of `section-4-catalogue`.

Measured at `7b03190`: **22 files match, 18 do not.** Most of the misses use
`## Ability inventory`, which starts with "Ability", not "inventory". Some have only
the H1 title.

**Consequence: 10 prose-only rows have never been catalogued.**

```
demon-hunter/devourer    Cull, Demonic Wards, Devour, Pierce the Veil
demon-hunter/vengeance   Reaver's Glaive
evoker/augmentation      Renewing
paladin/protection       Empyrean absorbs, Guardian's, Sacred Weapon
warlock/destruction      Spell Lock
```

⚠ Several of these were described in conversation as "recorded in the catalogue".
They were not. Fix the match (or standardise the 40 headings) **before** rollout, or
you cannot tell a genuinely new catalogue entry from a heading that finally matched.

⚠ Also: **a rollout must keep a table with clean ability names in column 1 under a
matching heading.** The pilot agent replaced the table with prose bullets and
`Templar Slash` silently disappeared from section 4 — a tracked unknown erased by a
docs edit, no marker, no warning.

---

## 4. The pilot — UNCOMMITTED IN THE WORKING TREE

Three files restructured as a shape proposal, awaiting Mike's approve/reject:

```
knowledge/classes/paladin/retribution/abilities.md   (DPS, hero trees)
knowledge/classes/warrior/protection/abilities.md    (tank)
knowledge/classes/priest/holy/abilities.md           (healer)
```

Plus the regenerated `section-4-catalogue.*` and `_meta/verify-in-game.md`.
`git diff` to see it. `git checkout -- <paths>` to discard if the shape is rejected.

### The proposed shape — four sections, nothing else

- **A. Routing header.** States the file carries no per-spell facts and routes:
  *what does X do / spellID / cooldown / tooltip* → `ability-inventory.md`;
  *when do I press X* → `rotation.md`; *do I take X* → `builds.md`;
  *why is X missing* → `section-3` / `section-4`.
- **B. `## Resource model`.** The spec's engine in prose, plus a kit-shaped
  hero-tree note (which buttons each tree adds/removes) deferring the pick to
  `builds.md`.
- **C. `## Inventory`.** A **two-column `Ability | Role` table.** No spellID, no
  cooldown, no cast time, no mechanics. Role answers only *"what is this for, in
  this spec"* — the judgement game data cannot make. **This is also the machine
  contract from B2; do not rename the heading or drop the table.**
- **D. `## Reconciliation notes — Tier 1 @ <build>`.** The adjudications with no
  generated home, above all **negative claims** (see §5.1).

Markers in the three files: **18 harvested → 4**. Repo-wide 329 → 315.

### Honest headline: the files got LONGER

131 → 164 lines (Ret), 115 → 146 (Prot), 134 → 154 (Holy). Deleting five columns of
restatement was outweighed by writing down judgement that used to be implicit.

**If the goal is volume, the win is elsewhere and it is free** — see §7.

---

## 5. What a mechanical rollout would DESTROY

Beyond B1. A rollout script will not recognise these as worth keeping.

### 5.1 Negative claims — the highest-value lines in the hand-written layer

"X is not acquirable at 12.0.7." "Seeing Red is in no Warrior inventory." "Holy has
no interrupt and no battle rez." "Defensive Stance is a talent, not baseline."

**A generated inventory is structurally incapable of stating an absence.** It lists
what *is*. It can never say what stopped being.

### 5.2 Charge counts and recharge times

Known as ledger gap **G6**: `SpellCooldowns` returns the **GCD** for charge
abilities, so **194 rows across the 40 files** read 0 or sub-10s. The `~` prose
values are the only record — and they are exactly what a "delete restated cooldowns"
pass deletes. **For Holy Priest this is fatal**: Holy Word charge cadence *is* the
rotation and both Holy Words read `cooldown=0`.

### 5.3 The class-line over-report

Retribution's inventory carries **44 `class-baseline` rows = the entire Paladin
skill line** — 11 mounts, 8 Holy spells, 2 Protection spells, Sense Undead. The
generator is right (`SkillLineAbility:800` is a class attachment) but nothing
generated says which are Retribution's. **This is the load-bearing argument for
keeping the curated §C table**: it is the human filter over 187 rows.

### 5.4 Name history / aliases

"Berserker Shout, formerly Berserker Rage." "Shackle Horror, formerly Shackle
Undead." The tsv has an `aliases` column but it is sparsely populated. Partial loss.

### 5.5 Prose currently shields readers from generated-layer warts

See §8.1.

---

## 6. How the generator works — the parts that bite

```bash
cd ~/code/fun/wow/tools
uv run python -m wowkb.gen_abilities --fetched 2026-08-06            # write
uv run python -m wowkb.gen_abilities --fetched 2026-08-06 --check    # drift gate, exit 1 on drift
uv run python -m wowkb.gen_abilities --fetched 2026-08-06 --residual # section-4 candidates
uv run python -m wowkb.gen_abilities --fetched 2026-08-06 --probe        # NETWORK: residual probe
uv run python -m wowkb.gen_abilities --fetched 2026-08-06 --descriptions # NETWORK: ~3,952 GETs, ~4 min
```

- **`--fetched` is REQUIRED** and is stamped as both `fetched:` and `reviewed:`.
  `gen_abilities` emits `reviewed:` itself, deliberately — `talents.py` does not, and
  all 40 committed `talents.md` carry a hand-stamped one, which is a permanent
  `--check` trap for that generator (recorded in `kb-inbox.md`).
- **The two network legs cache to committed KB artifacts.** Ordinary runs and
  `--check` read the cache and never call out, so generation stays offline and
  deterministic. Refresh on patch day.
- `--check` is a **manual/pre-commit gate. There is no CI in this repo.**

### Legs

Legs 1–6 build sections 1+2 (talents, class kit, spec baseline, PvP, pets, CDM).
Two more build 3+4, and **neither may write into `ability-inventory.tsv`** — neither
produces an acquisition row, and BucketBinds reads that file as the spec's real kit.

- **The override walk** (`EffectWalk`). `SpellEffect` one hop out from the spec's own
  talent spells, on exactly two edges: `EffectTriggerSpell`, and `EffectMiscValue_0`
  **only under `EffectAura == 332`**. Anchors include **rank siblings** (same
  normalised name AND same `SpellClassOptions.SpellClassSet`).
  `override` → section 3, `trigger` → section 4.
- **The residual probe** (`--probe`). Candidate IDs from `SpellName`, then
  `GET /data/wow/spell/{id}`. A 200 promotes to section 3.

`spec_scope` on section-3 override rows: `spec-exclusive` (5 rows) when the
anchor→target pair fires for one spec of the class, `class-shared` (27) when several.
A class-shared row proves the **ability** is reachable from that class's talent, not
that this spec presses it. Scope is counted **before** the already-have filter.

---

## 7. The cheap, separate win — take it regardless

The volume in these files was never the restated facts. It is:

1. **A 16-line `[T1]`-vs-`~` boilerplate blockquote duplicated verbatim across all
   40 files.** (I wrote it this session; it is longer than it needs to be.)
2. **Hero-tree sections that duplicate `builds.md`,** which covers them better.

Deleting those shrinks 40 files by **~25 lines each with zero loss and zero tool
work.** Entirely independent of the rollout decision.

---

## 8. Open quality caveats — known, not fixed

### 8.1 Some tooltips render the wrong spec's branch

Blizzard's API resolves `$?spec[…]` conditionals **without spec context**, so a
shared hero-tree passive can render another spec's text. Confirmed:

- Protection Warrior · `Burst of Power` 437118 → *"your next 2 **Bloodthirsts**"*.
  Bloodthirst is Fury's.
- Protection Warrior · `Thunder Blast` 435607 → *"Shield Slam and **Bloodthirst**"*.

A loose scan (description names an ability existing only in a sibling spec) flags
**~445 rows**, but that is an upper bound with heavy false positives — a class-tree
talent legitimately names abilities the spec does not take. **2 confirmed.** Every
class-shared hero-tree passive is a candidate. Needs a real discriminator, not this
heuristic.

### 8.2 `description_source: none` is a lead on a stub row

26 rows / 12 spellIDs have no text in either source. **Not all junk.** Six are
**stub twins** — a real ability name whose spellID is a hollow shell (cooldown 0,
no text, `NameSubtext_lang` "Passive") sitting in specs that do **not** have the
ability, while the real button is a different spellID:

| name | hollow | carried by | real button |
|---|---|---|---|
| Force of Nature | `37846` cd 0 | Feral, Guardian, Restoration | `205636` cd 60, **Balance** |
| Incarnation: Tree of Life | `81098` cd 0 | Balance, Feral, Guardian | `33891` cd 180, **Restoration** |

⚠ **Weak signal, measured**: 11 names have that stub *shape* and only **2** are
`none`. A free lead, not a census. Full note in `_meta/kb-inbox.md`.
**Do not "fix" by dropping rows** — that changes the union BucketBinds consumes.

### 8.3 A stale sibling found in passing

`priest/holy/rotation.md` still says "pre-apply Prayer of Mending and **Renew**" and
lists **Circle of Healing** "(if talented)" — both contradict the Tier-1 finding in
`abilities.md`. Means **"check the sibling covers it" is not sufficient** — the
sibling can be wrong.

### 8.4 Ledger gaps G1–G7

Routed to `knowledge/_meta/kb-inbox.md` § *Ability inventory — the seven tool gaps*.
**G6 is B1's cousin** (charge recharge, one `wago` fetch away). **G7 is unblocked** —
its stated blocker (unversioned `SpellEffect.csv`) is gone.

---

## 9. TRAPS — each of these cost real time

- **Never use "newest build wins" resolution.** Pin to `12.0.7.67808`. `raw/wago/`
  holds tables at several builds; mixing manufactures spellIDs that exist in one
  table and not another.
- **`EffectMiscValue_0` is a spell reference ONLY under aura 332.** Otherwise it is
  a skill line, mechanic or item id — ignoring this yields Dry Pork Ribs and
  Teleport: Goldshire as Paladin abilities.
- **A spell-API 404 is NOT evidence of absence.** Hammer of Light 427441 and 427453
  both 404 and are demonstrably live.
- **"Not in any data table" is almost always wrong.** Said of Hammer of Light this
  session; it has **8** `SpellName` entries, is reached via `SpellEffect` from
  Light's Guidance 427445, and **Protection Paladin already carries it** as
  `1246643 cdm-only` (`CooldownSetSpell` set 637 = spec **66**, not 70). The precise
  claim a section-4 row makes is: **no table says this SPEC LEARNS it.** Before
  calling one unknown, **check a sibling spec of the same class** — a shared hero
  tree makes a one-sided gap likely.
- **`@verify-ingame` inside backticks is ignored by `wowkb.gen_verify`; bare, it is
  harvested.** New boilerplate must backtick it or it inflates the checklist. Ten
  phantom rows came from exactly this.
- **Put each marker on its own physical line.** `gen_verify` truncates to one line,
  so a marker at the end of wrapped prose harvests as an unreadable fragment.
- **Descriptions contain newlines.** 996 inventory rows and 76 annex rows. Every TSV
  cell is escaped on write; without it each would split a row and be read as data.
- **Do NOT let one agent both change the generator and rewrite prose.** It will tune
  the generator until the prose validates. **Generate → freeze → adjudicate → edit.**
  This session ran two agents in sequence for exactly that reason.
- **`kblint` exits 1 at HEAD** — **17 findings** across 13 files in `knowledge/addon-dev/`,
  none from this work, verified identical with changes stashed. Do not chase them.
  (Both agents reported this as "one hit"; it is 17. Recount, don't trust.)

---

## 10. Verification

```bash
cd ~/code/fun/wow/tools
uv run python -m wowkb.gen_abilities --fetched 2026-08-06 --check  # 0 = no drift; run TWICE
uv run python -m wowkb.gen_verify --check
uv run python -m wowkb.obs check
uv run python -m wowkb.gen_candidates --check
uv run python -m wowkb.spec_inventory --unseeded                   # BucketBinds impact
uv run python -m wowkb.kblint                                      # 17 PRE-EXISTING
```

Plus, after any TSV schema change: re-parse every generated `.tsv` tab-delimited and
assert **uniform field count AND line-count == row-count** (the second check is the
one that catches an embedded newline that happens to balance).

**Marker count:** `abilities.md` markers went **332 → 185** across this work
(counting bare, i.e. what `gen_verify` harvests). `_meta/verify-in-game.md` is at
**328 open items** at `7b03190`, **315** with the pilot applied.

**BucketBinds:** the `spec_inventory` fixes moved `--unseeded` from
**1,635 unbound / 2,491** to **1,663 / 2,560** — 69 more abilities visible, 41 of
them already seed-bound. Worth a look before the next placement pass.

---

## 11. NEXT ACTIONS, in order

1. **[BLOCKER] Add `cost` + `cast_time` to `gen_abilities`.** Fetch `SpellPower`,
   `SpellCastTimes` pinned to `12.0.7.67808` first. §3-B1.
2. **[BLOCKER] Fix or standardise the `## Inventory` heading match.** §3-B2. Expect
   `section-4-catalogue` to grow by ~10 rows; that is the backlog surfacing, not new
   drift.
3. **[DECISION — Mike] Approve or reject the pilot shape.** §4. The `Ability | Role`
   two-column table is the part worth arguing about: it is simultaneously the human
   filter over 187 rows and the machine contract from B2.
4. Roll out to the remaining 37 — only after 1–3.
5. **[INDEPENDENT] Delete the duplicated boilerplate + hero-tree sections.** §7.
   Free, needs no tool work, do it whenever.
6. Re-measure markers (`gen_verify`) and BucketBinds coverage after rollout.
