---
title: Reconcile ledger — hand-written abilities.md vs generated ability-inventory.tsv (12.0.7)
patch: 12.0.7
build: 12.0.7.67808
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - https://wago.tools/db2  # Tier 1, DB2 pinned @ 12.0.7.67808 (SpellName, SpellMisc, SpellCooldowns, TraitDefinition/NodeEntry/Node/NodeXCond/Cond, SpecSetMember, SkillLineAbility, SkillLine, SkillLineXTraitTree, SpecializationSpells, PvpTalent, CooldownSetSpell, TraitSubTree, ChrSpecialization)
  - knowledge/classes/_abilities/all-abilities.tsv  # Tier 1 derived, generated inventory (FROZEN)
  - knowledge/classes/_abilities/pet-family-annex.tsv  # Tier 1 derived, pet skill lines
  - knowledge/classes/*/*/abilities.md  # the hand-written claims under adjudication
confidence: high
---

# Reconcile ledger — `abilities.md` vs `ability-inventory.tsv`

One verdict per hand-written claim row, keyed **class → spec → ability** so a reconcile
agent handling a single class can work from its own section alone.

**Every DB2 read behind this ledger is pinned to build `12.0.7.67808`.** No unversioned or
`68256` table was consulted. Where a join could not answer, the row says so.

## 1. Verdict vocabulary

| Verdict | What the reconcile agent does |
|---|---|
| `CONFIRMED` | Name + spec match Tier 1. Drop the `@verify-ingame` marker; restate the row with its Tier-1 cooldown/origin. |
| `ORIGIN-SHIFT` | Present, but the KB mislabels **how** it is obtained. Fix the label; keep the row. |
| `WRONG-SPEC` | Tier 1 attributes it to a **different** spec. Delete from this file; the real owner is named. |
| `NAME-DRIFT` | Resolves under a different current name. Rename (both names given). |
| `REMOVED` | Resolves in `SpellName` but attaches to **no** acquisition table at 12.0.7.67808. **Delete the claim** — do not leave it under a marker. |
| `TOOL-GAP` | Genuinely castable, generator still cannot see it. **Keep** the marker and file it to `knowledge/_meta/kb-inbox.md`. |

### The discriminator between REMOVED and TOOL-GAP

Both look identical in the diff — the name is absent from the generated tsv. They were
separated by asking a second Tier-1 question: **does the thing that would grant it still exist?**

- `TOOL-GAP` requires a *named, measured* parent that is live on the acquisition graph —
  the talent node, hero subtree, or base ability the button overrides — and usually a
  Midnight-range spell ID (`>= 1200000`) minted for 12.0.
- `REMOVED` is asserted only when **no** spell of that name attaches to any of
  `TraitNodeEntry` (on the class's **live** tree), `SkillLineAbility` (on an in-scope line),
  `SpecializationSpells` or `PvpTalent` — **and** the tree carries no successor node for it.

### Live vs legacy trait trees (this catches four of the REMOVED verdicts)

`TraitNode` at 67808 contains **duplicate legacy copies** of some class trees. Resolving
every `node_id` in the 40 generated tsvs gives exactly one live tree per class:

| Class | Live tree | Legacy copy also present |
|---|---|---|
| Death Knight | 750 | |
| Demon Hunter | 854 | |
| Druid | 793 | |
| Evoker | 872 | |
| Hunter | 774 | |
| Mage | 658 | |
| Monk | **1000** | **781** — carries Zen Meditation, Dampen Harm |
| Paladin | 790 | |
| Priest | 795 | |
| Rogue | 852 | |
| Shaman | **786** | **1033 / 1034** — carry Fire Elemental, Storm Elemental, Thunderstorm, Icefury, Primordial Wave |
| Warlock | 720 | |
| Warrior | 850 | |

A spell whose *only* trait attachment is a legacy tree is `REMOVED`, not present.

## 2. Corpus tallies

| | |
|---|---|
| Claim rows examined (40 files) | **1578** |
| `CONFIRMED` | 1464 |
| `ORIGIN-SHIFT` | 40 |
| `WRONG-SPEC` | 13 |
| `NAME-DRIFT` | 13 |
| `REMOVED` | 24 |
| `TOOL-GAP` | 24 |

Only the **non-CONFIRMED** rows are enumerated below, plus, per spec, the marked rows the
generated tsv now settles. A row not listed anywhere in §4 is `CONFIRMED` by default.

⚠ **Do not copy a sub-2-second value out of the tsv's `cooldown` column.** That column is
`max(RecoveryTime, CategoryRecoveryTime)` at `DifficultyID 0`, which for charge-based and
GCD-categorised abilities returns the **GCD**, not the recharge — `Celestial Alignment` reads
`1`, `Fire Blast` reads `0.5`, `Purifying Brew` reads `1`. Fifteen otherwise-settleable markers
were **withheld** from the tables below for exactly this reason; charge recharge lives in
`SpellCategory`, whose CSV in `raw/wago/` is unversioned and so cannot be pinned to 67808.
## 3. Cross-spec findings — the errors a per-spec agent cannot see

These are the claims where the KB names an ability that Tier 1 hands to a **different spec**
or a **different class**. Each was resolved by reading the acquisition table itself, not by
trusting the label on the row.

| Claimed by | Ability | Tier-1 owner | Evidence @ 12.0.7.67808 |
|---|---|---|---|
| monk/mistweaver + monk/windwalker | **Double Barrel** | Monk / **Brewmaster** | `PvpTalent` 202335 → SpecID Brewmaster only |
| monk/mistweaver + monk/windwalker | **Nimble Brew** | Monk / **Brewmaster** | `PvpTalent` 354540 → SpecID Brewmaster only |
| monk/mistweaver + monk/windwalker | **Reverse Magic** | **Demon Hunter** / Havoc + Vengeance + Devourer | `PvpTalent` 205604 → those three SpecIDs. Not a Monk ability at all. |
| monk/mistweaver | **Spear Hand Strike** | Monk / **Brewmaster** + **Windwalker** | Live tree 1000, node 101152 gated Brewmaster, node 110098 gated Windwalker. No Mistweaver node. |
| rogue/subtlety | **Grappling Hook** | Rogue / **Outlaw** | `SpecializationSpells` 195457 → Outlaw. **Absent from `PvpTalent` entirely** — a "PvP talent" label here is wrong twice. |
| shaman/enhancement + shaman/restoration | **Thunderstorm** | Shaman / **Elemental** | `SpecializationSpells` 51490 → Elemental. **Absent from `PvpTalent` entirely.** Its only trait attachment is the legacy trees 1033/1034. |
| hunter/beast-mastery | **Kill Shot** | Hunter / **Marksmanship** | Node 109490 on live tree 774; `TraitNodeXTraitCond → TraitCond.SpecSetID → SpecSetMember` = Marksmanship only. |
| hunter/beast-mastery | **Muzzle** | Hunter / **Survival** | Node 79837 gated Survival only. BM's interrupt is `Counter Shot` 147362, node 102292, gated Beast Mastery. |
| mage/frost | **Prismatic Barrier** | Mage / **Arcane** | Node 62121 on live tree 658, gated Arcane only. Frost's barrier is `Ice Barrier`. |

### Corrections to the brief's worked examples

Two of the examples handed to this pass do **not** survive measurement, and the ledger
records what was measured rather than what was expected:

- **`Swoop Up` IS in `PvpTalent`.** Spell 370388 is a PvP talent for **all three** Evoker
  specs (Preservation, Devastation, Augmentation), and it is already present in all three
  generated tsvs with `origin = pvp-talent`. The same holds for `Time Stop` (378441) and
  — as the brief said — `Chrono Loop` (383005). The evoker rows are not wrong about
  *ownership*; they are wrong only in that several omit the PvP-talent label (see §4, Evoker).
- **`Grappling Hook` and `Thunderstorm` are confirmed absent from `PvpTalent`**, exactly as
  the brief said — but their real owners are `SpecializationSpells` rows (Outlaw, Elemental),
  which is what makes the verdict `WRONG-SPEC` rather than a bare label fix.

## 4. The ledger

### Death Knight

#### `death-knight/blood`

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Dark Simulacrum` (L68) | `pvp-talent` | 20s | Tier1 pvp-talent; KB does not say PvP |

**Markers the tsv settles** (4) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Consumption` (L43) | Consumption / 1263824 | `talent-active` | **45s** |
| `Dancing Rune Weapon` (L44) | Dancing Rune Weapon / 49028 | `talent-active` | **120s** |
| `Reaper's Mark` (L45) | Reaper's Mark / 439843 | `talent-active` | **45s** |
| `Raise Dead` (L54) | Raise Dead / 46585 | `talent-active` | **120s** |

#### `death-knight/frost`

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Glacial Advance` (L48) | `class-baseline` | — | KB says talent; Tier1 class-baseline |
| `Dark Simulacrum` (L77) | `pvp-talent` | 20s | Tier1 pvp-talent; KB does not say PvP |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Pillar of Frost` (L50) | Pillar of Frost / 51271 | `talent-active` | **45s** |

#### `death-knight/unholy`

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Dark Simulacrum` (L83) | `pvp-talent` | 20s | Tier1 pvp-talent; KB does not say PvP |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Army of the Dead` (L58) | Army of the Dead / 42650 | `talent-active` | **90s** |

### Demon Hunter

#### `demon-hunter/devourer`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Cull` (L57) | **TOOL-GAP** | `Cull` 1245453/1245455 exist in SpellName@67808 (Midnight-range IDs) but attach to no acquisition table. Parent `Reap` 1226019 = SpecializationSpells/Devourer and `Void Metamorphosis` is live on tree 854 — Cull is Reap's transform-form button. |
| `Devour` (L58) | **TOOL-GAP** | Parent `Consume` 473662 = SpecializationSpells/Devourer, live. Devour is its Void-Metamorphosis form; no acquisition row exists for the override button. README §'What this source cannot answer' already names it. |
| `Pierce the Veil` (L62) ⟨marked⟩ | **TOOL-GAP** | 1245483 (Midnight-range) in SpellName, unattached. Parent `Voidblade` 1245412 is on live tree 854. Transform-form override. |
| `Demonic Wards` (L77) | **TOOL-GAP** | 1277736 IS attached — SpecializationSpells → Devourer — but is passive (SpellMisc.Attributes_0 & 0x40). The generator drops passive SpecializationSpells rows (431 of 458 missing). Same hole as Havoc 278386 / Vengeance 203513. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Reap` (L52) | `class-baseline` | — | KB says talent; Tier1 class-baseline |
| `Blur` (L74) | `class-baseline` | 0.5s ⚠GCD | KB says talent; Tier1 class-baseline |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Void Nova` (L64) | Void Nova / 1234195 | `talent-active` | **45s** |

#### `demon-hunter/havoc`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Annihilation` (L47) | **TOOL-GAP** | `Metamorphosis` 191427 (class-baseline, SkillLine 1848) and `Chaos Strike` 344862 (class-baseline) are both in havoc's tsv. Annihilation is the Meta-form replacement of Chaos Strike; overrides have no acquisition row. |
| `Death Sweep` (L49) | **TOOL-GAP** | `Blade Dance` 188499 class-baseline present; Death Sweep is its Meta-form replacement. |
| `Reaver's Glaive` (L58) | **TOOL-GAP** | `Art of the Glaive` 442290 is live on tree 854 in subtree 35 **Aldrachi Reaver**. Reaver's Glaive 1283344 is a Midnight-range ID with no acquisition row — the proc button Art of the Glaive grants. |
| `Abyssal Gaze` (L59) | **TOOL-GAP** | Subtree 34 **Fel-Scarred** is live on tree 854 with `Demonsurge` + `Demonic Intensity`; `Eye Beam` 198013 is talent-active in havoc's tsv. Abyssal Gaze 452497 is the Demonsurge override of Eye Beam. |
| `Consuming Fire` (L60) | **TOOL-GAP** | Same Fel-Scarred path; `Immolation Aura` 258920 class-baseline present. Consuming Fire 452487/456640 is its Demonsurge override. |
| `Fel Barrage` (L74) ⟨marked⟩ | **REMOVED** | 21 spells named Fel Barrage in SpellName@67808, **none** attaches to any trait node, SkillLineAbility, SpecializationSpells or PvpTalent. Max ID 400185 — no Midnight-range ID was ever minted. Tree 854 has no Fel Barrage node. Delete the row. |

**Markers the tsv settles** (3) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Blade Dance` (L48) | Blade Dance / 188499 | `class-baseline` | **15s** |
| `Eye Beam` (L50) | Eye Beam / 198013 | `talent-active` | **30s** |
| `Consume Magic` (L68) | Consume Magic / 278326 | `talent-active` | **10s** |

#### `demon-hunter/vengeance`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Reaver's Glaive` (L72) | **TOOL-GAP** | Same as Havoc — Art of the Glaive 442290, Aldrachi Reaver subtree 35, live on tree 854. |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Spirit Bomb` (L50) | Spirit Bomb / 247454 | `talent-active` | **25s** |

### Druid

#### `druid/balance`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Lunar Eclipse` (L44) | **TOOL-GAP** | 1233272 (Midnight-range) in SpellName, no acquisition row and — unlike its sibling — no CooldownSetSpell row either. Parent `Eclipse` 1239669 is talent-active in the tsv and `Solar Eclipse` 1233346 IS present as `cdm-only`. The asymmetry is a Blizzard CooldownSet omission, not a dead claim. |
| `Half Moon` (L55) | **TOOL-GAP** | `New Moon` 274281 is on live tree 793. Half Moon 202768/274282/373255 attach nowhere — they are the Moon chain's sequential override buttons. |
| `Full Moon` (L56) | **TOOL-GAP** | Same chain; Full Moon 202771/274283/373258 unattached. |
| `Renewal` (L62) ⟨marked⟩ | **REMOVED** | `Renewal` 37563/108238/283762/292628/408762 — none attaches to anything at 12.0.7.67808, and there is no Renewal node on live tree 793. Delete the row. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Ascendant Eclipses` (L50) | `talent-passive` | — | Tier 1 has **no castable spell of this name at all** — every ID carries SpellMisc Attributes_0 & 0x40. It is a passive, not a pressed ability. |
| `Faerie Swarm` (L79) | `pvp-talent` | 30s | Tier1 pvp-talent; KB does not say PvP |
| `Moonkin Form` (L81) | `talent-active` | — | KB says baseline; Tier1 talent-active |

**Markers the tsv settles** (6) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Force of Nature` (L52) | Force of Nature / 205636 | `talent-active` | **60s** |
| `Fury of Elune` (L53) | Fury of Elune / 202770 | `talent-choice` | **60s** |
| `Solar Beam` (L59) | Solar Beam / 78675 | `talent-active` | **60s** |
| `Heart of the Wild` (L65) | Heart of the Wild / 1261867 | `talent-active` | **120s** |
| `Mighty Bash` (L75) | Mighty Bash / 5211 | `talent-choice` | **60s** |
| `Faerie Swarm` (L79) | Faerie Swarm / 209749 | `pvp-talent` | **30s** |

#### `druid/feral`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Renewal` (L72) ⟨marked⟩ | **REMOVED** | Same measurement as Balance — no acquisition row anywhere, no node on tree 793. Delete the row. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Moonfire` (L64) | `class-baseline` | — | KB says talent; Tier1 class-baseline |

#### `druid/guardian`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Rage of the Sleeper` (L62) ⟨marked⟩ | **REMOVED** | 200851/214844/219432 attach to nothing; no node on tree 793. Delete the row. |

#### `druid/restoration`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Nourish` (L53) ⟨marked⟩ | **REMOVED** | 13 spells named Nourish, none attached; no node on tree 793. Delete the row. |

**Markers the tsv settles** (2) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Incarnation: Tree of Life` (L55) | Incarnation: Tree of Life / 33891 | `talent-choice` | **180s** |
| `Heart of the Wild` (L86) | Heart of the Wild / 1261867 | `talent-active` | **120s** |

### Evoker

#### `evoker/augmentation`

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Draconic Attunements` (L73) | `talent-passive` | — | Tier 1 has **no castable spell of this name at all** — every ID carries SpellMisc Attributes_0 & 0x40. It is a passive, not a pressed ability. |

**Markers the tsv settles** (11) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Breath of Eons` (L51) | Breath of Eons / 403631 | `talent-active` | **120s** |
| `Blistering Scales` (L52) | Blistering Scales / 360827 | `talent-active` | **30s** |
| `Time Skip` (L53) | Time Skip / 404977 | `talent-active` | **180s** |
| `Zephyr` (L60) | Zephyr / 374227 | `talent-active` | **120s** |
| `Cauterizing Flame` (L63) | Cauterizing Flame / 374251 | `talent-active` | **60s** |
| `Expunge` (L64) | Expunge / 365585 | `talent-active` | **8s** |
| `Rescue` (L66) | Rescue / 370665 | `talent-active` | **60s** |
| `Landslide` (L68) | Landslide / 358385 | `talent-active` | **90s** |
| `Oppressing Roar` (L69) | Oppressing Roar / 372048 | `talent-active` | **120s** |
| `Tail Swipe` (L70) | Tail Swipe / 368970 | `class-baseline` | **180s** |
| `Spatial Paradox` (L72) | Spatial Paradox / 406732 | `talent-choice` | **180s** |

#### `evoker/devastation`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Engulf` (L64) ⟨marked⟩ | **REMOVED** | No spell named Engulf at 12.0.7.67808 attaches to anything, and no Midnight-range ID named Engulf exists (max 322174, all unrelated legacy spells). Subtree 37 **Flameshaper** IS live on tree 872 but its actives are `Fire Torrent` 1265992 and `Consume Flame`. Delete the row; do NOT assume Fire Torrent is a rename — that is unmeasured. |

**Markers the tsv settles** (10) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Eternity Surge` (L57) | Eternity Surge / 359073 | `talent-active` | **30s** |
| `Zephyr` (L69) | Zephyr / 374227 | `talent-active` | **120s** |
| `Rescue` (L72) | Rescue / 370665 | `talent-active` | **60s** |
| `Cauterizing Flame` (L73) | Cauterizing Flame / 374251 | `talent-active` | **60s** |
| `Expunge` (L74) | Expunge / 365585 | `talent-active` | **8s** |
| `Oppressing Roar` (L77) | Oppressing Roar / 372048 | `talent-active` | **120s** |
| `Landslide` (L78) | Landslide / 358385 | `talent-active` | **90s** |
| `Tail Swipe` (L79) | Tail Swipe / 368970 | `class-baseline` | **180s** |
| `Spatial Paradox` (L81) | Spatial Paradox / 406732 | `talent-choice` | **180s** |
| `Time Spiral` (L85) | Time Spiral / 374968 | `talent-choice` | **120s** |

#### `evoker/preservation`

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Swoop Up` (L81) | `pvp-talent` | 90s | Tier1 pvp-talent; KB does not say PvP |
| `Chrono Loop` (L82) | `pvp-talent` | 45s | Tier1 pvp-talent; KB does not say PvP |
| `Time Stop` (L83) | `pvp-talent` | 45s | Tier1 pvp-talent; KB does not say PvP |
| `Return` (L88) | `class-baseline` | — | KB says talent; Tier1 class-baseline |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Temporal Anomaly` (L56) | Temporal Anomaly / 373861 | `talent-active` | **15s** |

### Hunter

#### `hunter/beast-mastery`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Kill Shot` (L60) ⟨marked⟩ | **WRONG-SPEC** | Kill Shot 53351 sits on node 109490 / tree 774, and TraitNodeXTraitCond → TraitCond → SpecSet resolves that node to **Hunter/Marksmanship only**. Real owner: Marksmanship (talent-active). Delete from the BM file. |
| `Muzzle` (L70) | **WRONG-SPEC** | Muzzle 187707 is node 79837 / tree 774, gated to **Hunter/Survival only**. Beast Mastery's interrupt is `Counter Shot` 147362 (node 102292, gated Beast Mastery) — already in the BM tsv. Replace the row. |
| `Survival cooldown — Aspect of the Cheetah` (L75) | **CONFIRMED** | `Aspect of the Cheetah` is in the BM tsv — class-baseline, cooldown **180s**. Only the row label ('Survival cooldown — …') is prose; drop the marker and restate the row with the Tier-1 origin/cooldown. |
| `Call Pet (1–5)` (L81) | **NAME-DRIFT** | Current names are **`Call Pet 1` … `Call Pet 5`** (883, …), SkillLineAbility on SkillLine 795 (Hunter). Bare `Call Pet` resolves in SpellName but attaches to nothing. Rename the row. |
| `Ancient Hysteria / Primal Rage` (L86) ⟨marked⟩ | **NAME-DRIFT** | Split the row. `Ancient Hysteria` (19372/90355) attaches to nothing → **delete that half**. `Primal Rage` 264667 IS attached — SpecializationSpells → the **pet** spec `Ferocity`, cd 360s — so keep it but label it a pet(Ferocity) ability, not a player spell. |
| `Auto Shot` (L87) | **TOOL-GAP** | Auto Shot 75 IS attached — SkillLineAbility on SkillLine **183 'GENERIC (DND)'** — which is outside the generator's two closed skill-line allowlists. Genuinely castable; keep the marker. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Chimaeral Sting` (L69) | `pvp-talent` | 60s | Tier1 pvp-talent; KB does not say PvP |
| `Wild Kingdom` (L85) | `pvp-talent` | 60s | Tier1 pvp-talent; KB does not say PvP |

**Markers the tsv settles** (3) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Wild Thrash` (L52) | Wild Thrash / 1264359 | `talent-active` | **8s** |
| `Chimaeral Sting` (L69) | Chimaeral Sting / 356719 | `pvp-talent` | **60s** |
| `Wild Kingdom` (L85) | Wild Kingdom / 356707 | `pvp-talent` | **60s** |

#### `hunter/marksmanship`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Auto Shot` (L89) | **TOOL-GAP** | Same: SkillLineAbility 75 on SkillLine 183 GENERIC (DND), outside the allowlist. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Kill Shot` (L60) | `talent-active` | — | KB says baseline; Tier1 talent-active |
| `Call Pet 1` (L85) | `class-baseline` | — | KB says talent; Tier1 class-baseline |

**Markers the tsv settles** (3) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Counter Shot` (L66) | Counter Shot / 147362 | `talent-active` | **24s** |
| `Binding Shot` (L68) | Binding Shot / 109248 | `talent-active` | **45s** |
| `Harrier's Cry` (L84) | Harrier's Cry / 466904 | `class-baseline` | **360s** |

#### `hunter/survival`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Call Pet` (L74) | **NAME-DRIFT** | Current names are **`Call Pet 1` … `Call Pet 5`** (883, …), SkillLineAbility on SkillLine 795 (Hunter). Bare `Call Pet` resolves in SpellName but attaches to nothing. Rename the row. |
| `Ancient Hysteria` (L78) ⟨marked⟩ | **REMOVED** | 19372 and 90355 attach to nothing at 12.0.7.67808. The live bloodlust-analogue on the pet path is `Primal Rage` 264667 (SpecializationSpells → pet spec **Ferocity**). Delete the Ancient Hysteria row. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Harpoon` (L55) | `class-baseline` | 1s ⚠GCD | KB says talent; Tier1 class-baseline |
| `Chimaeral Sting` (L66) | `pvp-talent` | 60s | Tier1 pvp-talent; KB does not say PvP |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Aspect of the Eagle` (L51) | Aspect of the Eagle / 186289 | `class-baseline` | **90s** |

### Mage

#### `mage/arcane`

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Frost Nova` (L58) | `class-baseline` | — | KB says talent; Tier1 class-baseline |

**Markers the tsv settles** (3) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Presence of Mind` (L50) | Presence of Mind / 205025 | `talent-choice` | **45s** |
| `Supernova` (L51) | Supernova / 157980 | `talent-choice` | **45s** |
| `Alter Time` (L53) | Alter Time / 342245 | `talent-active` | **60s** |

#### `mage/fire`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Mass Barrier` (L78) | **REMOVED** | 414660 attaches to no trait node, SkillLineAbility, SpecializationSpells or PvpTalent. It survives only as a **CooldownSetSpell** row in set 278, which is why it appears as `cdm-only` in mage/frost and nowhere for Fire. CooldownSetSpell is not an acquisition table. Delete the Fire row. |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Meteor` (L55) | Meteor / 153561 | `talent-active` | **45s** |

#### `mage/frost`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Glacial Spike` (L48) | **NAME-DRIFT** | No spell named `Glacial Spike` attaches to anything (27 IDs, all unattached; tree 658 carries only the Glacial* passives). The current name is **`Glacial Spike!`** — spell 1222865, present in mage/frost's own tsv as origin `cdm-only`, castable=true. Rename the row and restate origin as cdm-only. |
| `Icy Veins` (L52) ⟨marked⟩ | **REMOVED** | 12472 / 54792 / 428329 — none attaches to any acquisition table, and there is no Icy Veins node on live tree 658 (Frost's cooldown-band castables are Frozen Orb, Cold Snap, Ray of Frost, Comet Storm, Splinterstorm, Alter Time, Mirror Image). The KB row's own hedge — 'the simc cds list does not explicitly cast it' — was right. Delete the row. |
| `Shifting Power` (L53) ⟨marked⟩ | **REMOVED** | 314791's only attachment at 12.0.7.67808 is SkillLineAbility on SkillLine **2732 'Night Fae'** — a dead Shadowlands covenant line the generator excludes by design (README, 'The Shadowlands Covenant lines stay dead'). No node on tree 658. Delete the row. |
| `Freeze (Water Elemental)` (L64) | **ORIGIN-SHIFT** | `Freeze` 33395 is attached — SkillLineAbility on SkillLine **805 'Pet - Water Elemental'** (and 1777). It is a **pet** ability, not a player spell; `Summon Water Elemental` 31687 is the player-side node on tree 658. Relabel origin as pet. It is absent from the spec tsv by design (only the Hunter pet line 270 is emitted per-spec). |
| `Prismatic Barrier` (L72) | **WRONG-SPEC** | Prismatic Barrier 235450 is node 62121 / tree 658, gated to **Mage/Arcane only**. Frost's barrier is `Ice Barrier`. Delete from the Frost file. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Cone of Cold` (L55) | `class-baseline` | 25s | KB says talent; Tier1 class-baseline |
| `Blink / Shimmer` (L78) | `class-baseline` | 0.5s ⚠GCD | KB says talent; Tier1 class-baseline |

### Monk

#### `monk/brewmaster`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Zen Meditation` (L84) ⟨marked⟩ | **REMOVED** | 115176's only trait attachment is tree **781**, which is the legacy Monk tree — the live Monk tree is **1000** (every node_id in all 3 Monk tsvs resolves to 1000). No Zen Meditation node on 1000. Delete the row. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Crackling Jade Lightning` (L82) | `class-baseline` | — | KB says talent; Tier1 class-baseline |

**Markers the tsv settles** (12) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Breath of Fire` (L51) | Breath of Fire / 115181 | `talent-active` | **15s** |
| `Exploding Keg` (L54) | Exploding Keg / 325153 | `talent-active` | **60s** |
| `Black Ox Brew` (L59) | Black Ox Brew / 115399 | `talent-choice` | **120s** |
| `Fortifying Brew` (L60) | Fortifying Brew / 115203 | `talent-active` | **360s** |
| `Invoke Niuzao, the Black Ox` (L61) | Invoke Niuzao, the Black Ox / 132578 | `talent-active` | **120s** |
| `Touch of Death` (L65) | Touch of Death / 322109 | `class-baseline` | **180s** |
| `Expel Harm` (L66) | Expel Harm / 322101 | `class-baseline` | **15s** |
| `Leg Sweep` (L72) | Leg Sweep / 119381 | `class-baseline` | **60s** |
| `Paralysis` (L73) | Paralysis / 115078 | `talent-active` | **45s** |
| `Ring of Peace` (L74) | Ring of Peace / 116844 | `talent-choice` | **45s** |
| `Tiger's Lust` (L78) | Tiger's Lust / 116841 | `talent-active` | **30s** |
| `Transcendence: Transfer` (L80) | Transcendence: Transfer / 119996 | `cdm-only` | **45s** |

#### `monk/mistweaver`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Spear Hand Strike` (L73) | **WRONG-SPEC** | On live tree 1000, Spear Hand Strike 116705 sits on node 101152 (gated **Brewmaster**) and node 110098 (gated **Windwalker**). There is no Mistweaver node. (Its tree-781 node is ungated but 781 is the legacy tree.) Delete from the Mistweaver file. |
| `Nimble Brew` (L88) | **WRONG-SPEC** | PvpTalent@67808: Nimble Brew 354540 → **Monk/Brewmaster** only. Delete from the Mistweaver file. |
| `Double Barrel` (L89) ⟨marked⟩ | **WRONG-SPEC** | PvpTalent@67808: Double Barrel 202335 → **Monk/Brewmaster** only. Delete from the Mistweaver file. |
| `Reverse Magic` (L90) | **WRONG-SPEC** | PvpTalent@67808: Reverse Magic 205604 → **Demon Hunter** Havoc / Vengeance / Devourer. It is not a Monk ability at all. Delete from the Mistweaver file. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Touch of Death` (L71) | `class-baseline` | 180s | KB says talent; Tier1 class-baseline |
| `Crackling Jade Lightning` (L72) | `class-baseline` | — | KB says talent; Tier1 class-baseline |

**Markers the tsv settles** (2) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Rushing Wind Kick` (L56) | Rushing Wind Kick / 467307 | `talent-choice` | **10s** |
| `Crackling Jade / Expel Harm` (L87) | Expel Harm / 322101 | `class-baseline` | **15s** |

#### `monk/windwalker`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Dampen Harm` (L74) ⟨marked⟩ | **REMOVED** | 122278 attaches only to legacy tree 781 (nodes 80704/95171/95172 for BrM/MW/WW). Nothing on live tree 1000. Delete the row. |
| `Nimble Brew` (L80) ⟨marked⟩ | **WRONG-SPEC** | PvpTalent 354540 → Monk/**Brewmaster**. Delete. |
| `Double Barrel` (L81) ⟨marked⟩ | **WRONG-SPEC** | PvpTalent 202335 → Monk/**Brewmaster**. Delete. |
| `Reverse Magic` (L82) ⟨marked⟩ | **WRONG-SPEC** | PvpTalent 205604 → **Demon Hunter** Havoc/Vengeance/Devourer. Delete. |
| `Combo Strikes (Mastery)` (L83) | **NAME-DRIFT** | Current name is **`Mastery: Combo Strikes`**, spell 115636, SpecializationSpells → Windwalker, passive. Rename the row and mark it passive. (It is absent from the tsv only because the generator drops passive SpecializationSpells rows.) |

**Markers the tsv settles** (4) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Strike of the Windlord` (L48) | Strike of the Windlord / 392983 | `talent-choice` | **35s** |
| `Zenith` (L53) | Zenith / 1249625 | `talent-active` | **16s** |
| `Celestial Conduit` (L55) | Celestial Conduit / 443028 | `talent-active` | **90s** |
| `Touch of Death` (L57) | Touch of Death / 322109 | `class-baseline` | **180s** |

### Paladin

#### `paladin/holy`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Barrier of Faith` (L65) ⟨marked⟩ | **REMOVED** | 148039/388536/395180 attach to nothing; no node on live tree 790 (which carries `Seraphic Barrier`). Delete the row. |
| `Sacred Weapon` (L75) | **NAME-DRIFT** | No spell named Sacred Weapon (432472/432502/432616/432757/441590) attaches to anything. The acquiring talent is **`Holy Armaments`** 1289728, on live tree 790, subtree 49 **Lightsmith** — Sacred Weapon is one of its two armament outputs and has no acquisition row of its own. Rename/re-anchor to Holy Armaments (the tsv already carries the `Holy Bulwark ⇄ Holy Armaments` alias). |
| `Concentration Aura` (L93) | **REMOVED** | 79963/81455/317920/344220 attach to nothing. `Devotion Aura` 465 is still on SkillLine 800 and `Aura Mastery` / `Auras of the Resolute` are on tree 790 — Concentration Aura specifically is gone. Delete the row. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Crusader Strike` (L55) | `class-baseline` | — | KB says talent; Tier1 class-baseline |

**Markers the tsv settles** (5) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Holy Prism` (L64) | Holy Prism / 114165 | `talent-choice` | **45s** |
| `Beacon of Virtue` (L68) | Beacon of Virtue / 200025 | `talent-choice` | **15s** |
| `Avenging Crusader` (L71) | Avenging Crusader / 216331 | `talent-choice` | **60s** |
| `Tyr's Deliverance` (L73) | Tyr's Deliverance / 200652 | `class-baseline` | **90s** |
| `Blessing of Sacrifice` (L81) | Blessing of Sacrifice / 6940 | `talent-active` | **120s** |

#### `paladin/protection`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Sacred Weapon` (L56) | **NAME-DRIFT** | Same as Holy — re-anchor to `Holy Armaments` 1289728 (tree 790, Lightsmith). |
| `Concentration Aura` (L80) | **REMOVED** | Same measurement as Holy. Delete the row. |

#### `paladin/retribution`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Templar Strike / Templar Slash` (L46) ⟨marked⟩ | **TOOL-GAP** | The acquiring talent **`Templar Strikes`** is on live tree 790. Templar Strike 1260091 is a Midnight-range ID; neither Strike nor Slash has an acquisition row because both are sequential replacement buttons. Keep the marker. |
| `Hammer of Light` (L53) | **TOOL-GAP** | 1246643 is in **CooldownSetSpell set 637** (Retribution's) yet on no acquisition table — the signature of a runtime override button. Named in the generator README's known-gap list. Keep the marker. |
| `Concentration Aura` (L81) | **REMOVED** | Same measurement. Delete the row. |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Execution Sentence` (L55) | Execution Sentence / 343527 | `talent-active` | **60s** |

### Priest

#### `priest/discipline`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Void Shield` (L55) ⟨marked⟩ | **TOOL-GAP** | The acquiring talent **`Master the Darkness`** 1253591 IS on live tree 795, and Void Shield has 8 Midnight-range IDs (1213562 … 1293007). It is the Power Word: Shield upgrade button — an override with no acquisition row. Keep the marker. |
| `Premonition` (L66) ⟨marked⟩ | **REMOVED** | 188779/428924/443056/450796 — all TWW-era, none attached. Subtree 20 **Oracle** IS live on tree 795 but now carries `Prophet's Insight`, `Prophet's Will`, `Piety`, `Twinsight` — no Premonition and no `Premonition of *`. Delete the row. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Shadow Word: Pain` (L47) | `class-baseline` | — | KB says talent; Tier1 class-baseline |
| `Shadowfiend` (L63) | `talent-active` | — | KB says baseline; Tier1 talent-active |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Void Torrent` (L51) | Void Torrent / 263165 | `talent-active` | **30s** |

#### `priest/holy`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Heal` (L48) | **REMOVED** | Spell 2060 `Heal` attaches to no trait node, SkillLineAbility, SpecializationSpells or PvpTalent at 12.0.7.67808; none of the other 112 spells named Heal does either. The Priest kit (SkillLine 804) carries Flash Heal, Power Word: Shield, Prayer of Mending, Smite — not Heal. Delete the row. |
| `Renew` (L50) | **REMOVED** | Spell 139 `Renew` attaches to nothing; not on SkillLine 804, not on tree 795 (which has `Renewed Faith` but no Renew). Delete the row. |
| `Circle of Healing` (L51) ⟨marked⟩ | **REMOVED** | 204883 (and the other 5) attach to nothing; no node on tree 795. Delete the row. |
| `Mastery: Echo of Light` (L76) ⟨marked⟩ | **TOOL-GAP** | 77485 IS attached — SpecializationSpells → **Holy** — but is passive, and the generator drops passive SpecializationSpells rows. Not a KB error; keep the row and the marker. |

**Markers the tsv settles** (10) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Holy Word: Chastise` (L45) | Holy Word: Chastise / 88625 | `talent-active` | **60s** |
| `Halo` (L54) | Halo / 120644 | `talent-active` | **60s** |
| `Apotheosis` (L55) | Apotheosis / 200183 | `talent-active` | **120s** |
| `Divine Hymn` (L56) | Divine Hymn / 64843 | `talent-active` | **180s** |
| `Guardian Spirit` (L57) | Guardian Spirit / 47788 | `talent-active` | **180s** |
| `Power Infusion` (L58) | Power Infusion / 10060 | `talent-active` | **120s** |
| `Holy Fire` (L61) | Holy Fire / 14914 | `talent-active` | **10s** |
| `Fade` (L67) | Fade / 586 | `talent-active` | **30s** |
| `Purify` (L72) | Purify / 527 | `class-baseline` | **8s** |
| `Mass Dispel` (L74) | Mass Dispel / 32375 | `talent-active` | **120s** |

#### `priest/shadow`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Void Volley` (L56) ⟨marked⟩ | **TOOL-GAP** | 8 Midnight-range IDs (1230903 … 1269563) exist in SpellName@67808 with no acquisition row. `Void Bolt` — which the KB row says it replaced — is itself gone from tree 795, and subtree 18 **Voidweaver** is live with `Void Blast` / `Entropic Rift`. This is a Midnight-new button the DB2 acquisition tables do not carry. Keep the marker. |
| `Mind Flay: Insanity` (L58) | **TOOL-GAP** | `Surge of Insanity` is on live tree 795 and `Mind Flay` 15407 is SpecializationSpells → Shadow. 391401/391403 are the proc-replacement buttons and have no acquisition row. Keep the marker. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Void Apparitions` (L67) | `talent-passive` | — | Tier 1 has **no castable spell of this name at all** — every ID carries SpellMisc Attributes_0 & 0x40. It is a passive, not a pressed ability. |

**Markers the tsv settles** (3) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Void Torrent` (L61) | Void Torrent / 263165 | `talent-active` | **30s** |
| `Halo` (L63) | Halo / 120644 | `talent-active` | **60s** |
| `Dispersion` (L69) | Dispersion / 47585 | `class-baseline` | **120s** |

### Rogue

#### `rogue/assassination`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Poisons (apply)` (L70) | **NAME-DRIFT** | `Poisons` is not a spell name at 12.0.7.67808. The concrete Tier-1 rows are `Instant Poison` / `Deadly Poison` / `Wound Poison` / `Crippling Poison` (class-baseline) and `Atrophic Poison` / `Numbing Poison` (talent-choice) — all already present in this spec's tsv. Split the row into the real names. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Shiv` (L61) | `talent-active` | — | KB says baseline; Tier1 talent-active |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Mark for Death` (L90) | Mark for Death / 1293340 | `cdm-only` | **20s** |

#### `rogue/outlaw`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Restless Blades` (L66) | **TOOL-GAP** | 79096 IS attached — SpecializationSpells → **Outlaw** — but is passive, and the generator drops passive SpecializationSpells rows. Not a KB error; keep the row (mark it passive) and the marker. |
| `Poisons` (L88) | **NAME-DRIFT** | `Poisons` is not a spell name at 12.0.7.67808. The concrete Tier-1 rows are `Instant Poison` / `Deadly Poison` / `Wound Poison` / `Crippling Poison` (class-baseline) and `Atrophic Poison` / `Numbing Poison` (talent-choice) — all already present in this spec's tsv. Split the row into the real names. |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Killing Spree` (L63) | Killing Spree / 51690 | `talent-active` | **180s** |

#### `rogue/subtlety`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Symbols of Death` (L59) ⟨marked⟩ | **REMOVED** | 212283/227151/247895/319063/328077 attach to nothing; no node on live tree 852. The KB row already suspected this ('appears removed/reworked in Midnight'). Tier 1 confirms — delete the row rather than leaving it marked. |
| `Grappling Hook` (L70) ⟨marked⟩ | **WRONG-SPEC** | Grappling Hook 195457 is **SpecializationSpells → Outlaw** (class-baseline; its tsv `cooldown` of 0.8 is the GCD, not the real cooldown — see §4 preamble), and it is **not in PvpTalent at all** — so any 'PvP talent' framing on this row is wrong twice over. Delete from the Subtlety file. |
| `Poisons` (L81) | **NAME-DRIFT** | `Poisons` is not a spell name at 12.0.7.67808. The concrete Tier-1 rows are `Instant Poison` / `Deadly Poison` / `Wound Poison` / `Crippling Poison` (class-baseline) and `Atrophic Poison` / `Numbing Poison` (talent-choice) — all already present in this spec's tsv. Split the row into the real names. |

**Markers the tsv settles** (3) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Goremaw's Bite` (L51) | Goremaw's Bite / 426591 | `talent-active` | **45s** |
| `Shadow Dance` (L57) | Shadow Dance / 185313 | `class-baseline` | **6s** |
| `Sprint` (L69) | Sprint / 2983 | `class-baseline` | **120s** |

### Shaman

#### `shaman/elemental`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Fire Elemental` (L54) | **REMOVED** | 198067's only trait attachment is trees **1033/1034**, the legacy Shaman trees (they carry Icefury, Primordial Wave, Liquid Magma Totem, Stormstrike — the pre-Midnight set). The live Shaman tree is **786** (every node_id in all 5 Shaman tsvs resolves to 786), which carries `Earth Elemental` 198103 and `Primal Elementalist` but no Fire Elemental. Delete the row. |
| `Storm Elemental` (L55) | **REMOVED** | 192249, same measurement — legacy trees 1033/1034 only, nothing on live tree 786. Delete the row. |

#### `shaman/enhancement`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Thunderstorm` (L109) ⟨marked⟩ | **WRONG-SPEC** | Thunderstorm 51490 is **SpecializationSpells → Elemental** (class-baseline in the Elemental tsv, cd 30s). Its only trait attachment is the legacy trees 1033/1034. It is **not in PvpTalent** — the 'PvP talent' label on this row is wrong. Delete from the Enhancement file. |
| `Capacitor/Earthgrab/Tremor/Wind Rush` (L111) | **CONFIRMED** | All four resolve in the Enhancement tsv: `Capacitor Totem`, `Earthgrab Totem`, `Tremor Totem`, `Wind Rush Totem`. Restate as four named rows with their Tier-1 origins. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Wind Shear` (L104) | `talent-active` | 12s | KB says baseline; Tier1 talent-active |

**Markers the tsv settles** (12) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Lava Lash` (L49) | Lava Lash / 60103 | `talent-active` | **18s** |
| `Sundering` (L58) | Sundering / 197214 | `talent-active` | **30s** |
| `Astral Shift` (L83) | Astral Shift / 108271 | `talent-active` | **120s** |
| `Earth Elemental` (L84) | Earth Elemental / 198103 | `talent-active` | **180s** |
| `Nature's Swiftness` (L89) | Nature's Swiftness / 378081 | `talent-active` | **60s** |
| `Feral Lunge` (L97) | Feral Lunge / 196884 | `class-baseline` | **30s** |
| `Totemic Projection` (L98) | Totemic Projection / 108287 | `talent-active` | **10s** |
| `Wind Shear` (L104) | Wind Shear / 57994 | `talent-active` | **12s** |
| `Hex` (L105) | Hex / 51514 | `talent-active` | **30s** |
| `Earthgrab Totem` (L107) | Earthgrab Totem / 51485 | `talent-active` | **30s** |
| `Wind Rush Totem` (L117) | Wind Rush Totem / 192077 | `talent-active` | **120s** |
| `Cleanse Spirit` (L119) | Cleanse Spirit / 51886 | `talent-active` | **8s** |

#### `shaman/restoration`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Thunderstorm` (L72) ⟨marked⟩ | **WRONG-SPEC** | Same measurement — SpecializationSpells → **Elemental** only, not in PvpTalent. Delete from the Restoration file. |

**Markers the tsv settles** (2) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Surging Totem` (L45) | Surging Totem / 444995 | `talent-active` | **25s** |
| `Totemic Projection` (L67) | Totemic Projection / 108287 | `talent-active` | **10s** |

### Warlock

#### `warlock/affliction`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Healthstone` (L85) | **NAME-DRIFT** | `Healthstone` 6262 is the item-use spell and attaches to nothing. The player ability is **`Create Healthstone`** 6201, SkillLineAbility on SkillLine 849 (Warlock) — already in warlock/destruction's file under that name. Rename. |
| `Spell Lock` (L113) ⟨marked⟩ | **ORIGIN-SHIFT** | `Spell Lock` 19647 IS attached — SkillLineAbility on SkillLine **189 'Pet - Felhunter'** (cd 24s), confirmed in `_abilities/pet-family-annex.tsv`. It is a **pet** ability, not a player spell. Relabel origin as pet; it is absent from the per-spec tsv by design (only the Hunter pet line 270 is emitted per-spec). |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Shadow Bolt` (L56) | `class-baseline` | — | KB says talent; Tier1 class-baseline |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Malevolence` (L66) | Malevolence / 442726 | `talent-active` | **60s** |

#### `warlock/demonology`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Spell Lock` (L56) | **ORIGIN-SHIFT** | `Spell Lock` 19647 IS attached — SkillLineAbility on SkillLine **189 'Pet - Felhunter'** (cd 24s), confirmed in `_abilities/pet-family-annex.tsv`. It is a **pet** ability, not a player spell. Relabel origin as pet; it is absent from the per-spec tsv by design (only the Hunter pet line 270 is emitted per-spec). |
| `Healthstone` (L64) | **NAME-DRIFT** | `Healthstone` 6262 is the item-use spell and attaches to nothing. The player ability is **`Create Healthstone`** 6201, SkillLineAbility on SkillLine 849 (Warlock) — already in warlock/destruction's file under that name. Rename. |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Summon Doomguard` (L53) | Summon Doomguard / 1276672 | `talent-active` | **120s** |

#### `warlock/destruction`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Spell Lock` (L82) | **ORIGIN-SHIFT** | `Spell Lock` 19647 IS attached — SkillLineAbility on SkillLine **189 'Pet - Felhunter'** (cd 24s), confirmed in `_abilities/pet-family-annex.tsv`. It is a **pet** ability, not a player spell. Relabel origin as pet; it is absent from the per-spec tsv by design (only the Hunter pet line 270 is emitted per-spec). |
| `Summon Pet (Imp / Voidwalker / Felhunter / Sayaad)` (L85) | **NAME-DRIFT** | `Summon Pet` attaches to nothing. The real rows are `Summon Imp` 688 etc., SkillLineAbility on SkillLine 849. Split into the concrete summon names. |
| `Health Funnel` (L86) | **REMOVED** | 9 spells named Health Funnel, none attached to any acquisition table at 12.0.7.67808. Delete the row. |

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Embers of Nihilam` (L68) | `talent-passive` | — | Tier 1 has **no castable spell of this name at all** — every ID carries SpellMisc Attributes_0 & 0x40. It is a passive, not a pressed ability. |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Malevolence` (L71) | Malevolence / 442726 | `talent-active` | **60s** |

### Warrior

#### `warrior/arms`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Heroic Strike` (L53) | **TOOL-GAP** | The KB row's own claim is right: `Master of Warfare` IS on live tree 850, and Heroic Strike **1269383** is a Midnight-range ID in SpellName with no acquisition row — the apex override form of `Slam`. Named in the generator README's known-gap list. Keep the marker. |

#### `warrior/fury`

**Claims the generated inventory does not carry**

| Ability (line) | Verdict | Evidence @ 12.0.7.67808 |
|---|---|---|
| `Crushing Blow` (L70) | **TOOL-GAP** | `Raging Blow` 85288 is on live tree 850; Crushing Blow 1215563/1270646 are Midnight-range IDs with no acquisition row — the Enrage-window replacement. Keep the marker. |

**Markers the tsv settles** (5) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Bloodthirst` (L63) | Bloodthirst / 23881 | `talent-active` | **4.5s** |
| `Champion's Spear` (L82) | Champion's Spear / 376079 | `talent-active` | **90s** |
| `Wrecking Throw` (L91) | Wrecking Throw / 384110 | `talent-choice` | **45s** |
| `Berserker Shout` (L94) | Berserker Shout / 384100 | `talent-choice` | **60s** |
| `Enraged Regeneration` (L110) | Enraged Regeneration / 184364 | `talent-active` | **120s** |

#### `warrior/protection`

**Origin mislabels** (row stays, label changes)

| Ability (line) | Tier-1 origin | Tier-1 cd | Fix |
|---|---|---|---|
| `Defensive Stance` (L85) | `talent-active` | 3s | KB says baseline; Tier1 talent-active |

**Markers the tsv settles** (1) — drop the marker, write the Tier-1 cooldown

| Ability (line) | Tier-1 name / spellID | origin | cooldown |
|---|---|---|---|
| `Champion's Spear` (L62) | Champion's Spear / 376079 | `talent-active` | **90s** |
## 5. Tool gaps — file these to `knowledge/_meta/kb-inbox.md`

The inventory is frozen, so these are recorded, not fixed. Each is a **measured** hole, with
the count where one could be measured.

### G1 — Passive `SpecializationSpells` rows are dropped (431 of 458)

`SpecializationSpells` at 67808 has **632** rows for real player specs, **458** of which are
passive (`SpellMisc.Attributes_0 & 0x40`). Only **27** of those 458 appear in
`all-abilities.tsv`. Most of the loss is junk (`Plate Specialization`, `Leather
Specialization`), but it also swallows real spec identity: `Mastery: Echo of Light` 77485
(Holy), `Restless Blades` 79096 (Outlaw), `Mastery: Combo Strikes` 115636 (Windwalker),
`Demonic Wards` 203513 / 278386 / 1277736 (Vengeance / Havoc / Devourer).
**Accounts for 4 `TOOL-GAP` verdicts.**

### G2 — Runtime override / proc-replacement buttons have no acquisition row

Already declared in `_abilities/README.md`; this pass measured its extent. **13 `TOOL-GAP`
verdicts** are of this shape: Annihilation, Death Sweep, Reaver's Glaive (×2 specs), Abyssal
Gaze, Consuming Fire, Cull, Devour, Pierce the Veil, Half Moon, Full Moon, Templar
Strike/Slash, Hammer of Light, Void Shield, Void Volley, Mind Flay: Insanity, Heroic Strike,
Crushing Blow, Lunar Eclipse. Only **one** of them (`Hammer of Light` 1246643, CooldownSet
637) leaves any DB2 trace at all. Closing these needs an in-game spellbook enumeration
(ClientLab), not another DB2 join.

### G3 — `SkillLine 183 "GENERIC (DND)"` is outside both allowlists

`Auto Shot` 75 is a `SkillLineAbility` row on line 183 and is therefore invisible to the
generator for every Hunter spec. **2 `TOOL-GAP` verdicts.** Worth checking what else line 183
carries before widening the allowlist — the allowlists exist to keep the dead covenant lines
out, and that guard must survive.

### G4 — `castable` is computed on the trait entry's visible spell, which is often the aura

45 rows across 23 specs read `castable = false` / `origin = talent-passive` for abilities that
are unmistakably pressed: `Drain Soul`, `Comet Storm`, `Shadow Mend`, `Flourish`, `Summon
Gargoyle`, `Raise Abomination`, `Zenith Stomp`, `Tempest`, `Void Blast`, `Mindbender`, … In
each case the tsv's `spell_id` is a passive aura while a castable sibling exists — e.g.
Windwalker `Zenith Stomp` is recorded as 1272694 (passive) when 1272696 / 1291484 are castable.
**These are NOT counted as KB errors in this ledger** — the KB rows are right and the column is
wrong. The four names that genuinely have *no* castable spell of that name anywhere
(`Ascendant Eclipses`, `Draconic Attunements`, `Void Apparitions`, `Embers of Nihilam`) are the
only ones filed as `ORIGIN-SHIFT`.

### G5 — pet abilities have no spec granularity (already documented, re-confirmed)

`Spell Lock` 19647 (SkillLine 189 Pet - Felhunter), `Axe Toss` 89766 (761/931 Pet - Felguard),
`Freeze` 33395 (805 Pet - Water Elemental) and `Primal Rage` 264667 (`SpecializationSpells` →
the **pet** spec `Ferocity`) are all real and all invisible per-spec. `pet-family-annex.tsv`
carries the first three. **5 `ORIGIN-SHIFT` verdicts** ride on this.

### G6 — charge recharge times are unreachable at a pinned build

`SpellCooldowns` gives the GCD for charge-based abilities (`Fire Blast` 0.5s, `Celestial
Alignment` 1s, `Purifying Brew` 1s, `Prayer of Mending` 1.5s, …). The real recharge is in
`SpellCategory.ChargeRecoveryTime` via `SpellCategories`, and **neither CSV in `raw/wago/`
carries a build suffix** — reading them would break the 67808 pin. 15 markers stay open on
this alone. Fetching `SpellCategory` and `SpellCategories` at 12.0.7.67808 would close them.

### G7 — one claim the data cannot re-anchor

`mage/frost` L61 `Icy Veins (Thermal Void)` is deleted as written because Icy Veins is gone,
but `Thermal Void` 1247729 **is** live on tree 658. What it now extends is not answerable from
`SpellName` / `SpellCooldowns` / `SpellMisc` — the effect tables were not consulted because
`SpellEffect.csv` in `raw/wago/` is **unversioned** and cannot be pinned to 67808. Do not guess.

## 6. Marker accounting

`knowledge/classes/*/*/abilities.md` carries **323** unbackticked `@verify-ingame` markers;
**300** of them sit on an inventory table row.

| | |
|---|---|
| Closed by a Tier-1 cooldown on a `CONFIRMED` row (§4 "Markers the tsv settles") | **118** |
| Closed because the row itself is deleted / reassigned / renamed (`REMOVED` 15, `WRONG-SPEC` 8, `NAME-DRIFT` 1, `ORIGIN-SHIFT` 1) | **25** |
| **Total markers this ledger closes** | **143** |
| Markers that must **stay** (`TOOL-GAP` rows) | 5 |
| Withheld — the tsv's `cooldown` is the GCD, not the recharge (charge abilities) | 15 |
| Markers on cast time, effect magnitude, resource cost or mechanic wording | 160 |

The last row is the honest limit of this pass: the generated tsv has a `cooldown` column and
no cast-time, resource or effect column, so a marker asking "is this really a 2.2s cast?" or
"how much Astral Power?" cannot be settled from Tier-1 DB2 as joined here. Those stay open and
belong in `_meta/verify-in-game.md`.

## 7. What was deliberately not done

- No file under `tools/wowkb/` and no generated file was touched. The inventory is frozen.
- No `abilities.md` was edited. This ledger is the instruction set; the reconcile agents execute it.
- No Tier-3/Tier-4 source was consulted. Every verdict above rests on a pinned DB2 read; where
  a join could not answer (G6), the row says so rather than borrowing a number from a guide.

## 8. Addendum — verdicts the reconcile pass issued for itself *(2026-08-06)*

Adversarial verification of the prose pass found **seven edits made off a second Tier-1
file (`_talents/all-talents.tsv`, and in one case the Blizzard talent-tree API) rather
than off a ledger row**, and reported as if they had not happened. Every one was
independently re-verified and **every one is factually correct** — which is why they are
recorded here rather than reverted. The defect was provenance discipline: §7 says this
ledger is the instruction set, so an agent issuing its own `REMOVED` / `WRONG-SPEC` /
`NAME-DRIFT` verdicts without declaring them removes the audit trail that separates a
measured deletion from a guessed one.

These are now ledger rows. The evidence column is what was actually checked.

| Spec | Ability | Self-issued verdict | Evidence re-verified |
|---|---|---|---|
| demon-hunter/havoc | Sigil of Spite | `WRONG-SPEC` — row deleted | `all-talents.tsv` @ 67808: Sigil of Spite 390163 → demon-hunter/**vengeance** node 90978 only. Havoc's tsv carries Sigil of Misery / Flame / Mastery and no Sigil of Spite. |
| evoker/devastation | Firestorm | `REMOVED` — row deleted | Zero rows named Firestorm across all 40 specs in `all-talents.tsv` @ 67808. |
| evoker/devastation | Shattering Star → **Shattering Stars** | `NAME-DRIFT` + `ORIGIN-SHIFT` — renamed, re-anchored to 1265802, reclassified active → passive | `all-talents.tsv`: devastation node 93316 `node_type=PASSIVE`, entry 115627, "Shattering Stars" 1265802. The spec tsv agrees (`talent-passive`, `castable=false`). ⚠ This is the §5 G4 shape, where 45 rows read passive wrongly — it survives only because `node_type` is an **independent** signal from the `castable` column. State that when citing it. |
| mage/arcane | Ice Barrier | `REMOVED` — row deleted | Arcane's tsv carries only Prismatic Barrier / Improved Prismatic Barrier. |
| mage/frost | Ice Floes | `REMOVED` — row deleted | Zero hits in `all-talents.tsv` and `all-abilities.tsv` @ 67808. |
| mage/frost | Blazing Barrier / Mass Barrier | `REMOVED` — row deleted | The Frost row was separate from the fire/Mass Barrier deletion the pass did declare, and no ledger row covered it. |
| shaman/enhancement | Elemental Blast | `WRONG-SPEC` — row deleted | Elemental Blast 117014 is `talent-choice` on **Elemental** only in `all-talents.tsv` and `all-abilities.tsv`; absent from the Enhancement tsv. (The file's two surviving prose mentions of it have since been reconciled with the deletion.) |
| warlock/demonology | the "not on the current Demo tree" bullet | marker dropped | Blizzard talent-tree API tree 720 / spec 266: 147 unique names, none of Bilescourge Bombers / Nether Portal / Demonic Strength / Guillotine, with Hand of Gul'dan / Implosion / Summon Demonic Tyrant / Doom present as controls; all four absent from `all-talents.tsv` for **every** spec. |

**The cross-check itself is now in play, deliberately.** `_talents/all-talents.tsv` is a
second Tier-1 file and using it is right; what was wrong was using it silently. Any future
pass may cite it — and must say so in the same breath.

### Corrections to this ledger's own rows

- **§4's "markers the tsv settles" entry for fury `Champion's Spear`, fury `Enraged
  Regeneration` and prot `Champion's Spear` is wrong.** Those markers asked about
  Rage-on-cast and heal-%/DR-% — questions §6 itself says the tsv cannot answer. Dropping
  them removed three genuine open unknowns. They have been re-opened as scoped markers in
  the prose files.
- **The Holy Armaments "unresolved Tier-1 vs Tier-1 conflict" is not one.** Tree 790
  subtree 49 carries node 95234 (TraitDefinition 122894 → 432459, *Holy Bulwark*) and node
  110257 (TraitDefinition 141558 → *Holy Armaments* 1289728, whose `VisibleSpellID` **is**
  432459). One entry, two names — exactly what the tsv's `aliases` column encodes.
- **"File TOOL-GAP rows to `_meta/kb-inbox.md`" (§5) is superseded.** Those names now live
  in the generated `section-4-catalogue.md` with their provenance, which cannot rot and
  carries the *catalogue, not backlog* rule. `kb-inbox.md` takes the **tool** gaps G1–G7,
  not the abilities.
- **G2 is partly refuted and G7 is unblocked.** `gen_abilities`' override walk reaches five
  of G2's names from `SpellEffect` alone (Templar Strike 407480, Cull 1245453, Voidblade
  1245412, Condemn 317485, Kill Shot 53351), and `raw/wago/SpellEffect-12.0.7.67808.csv`
  now exists, so G7's stated blocker — an unversioned `SpellEffect.csv` — is gone.
