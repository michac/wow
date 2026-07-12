---
title: Bellular Keybind Seed — Expert Review Findings (Midnight 12.0.7)
date: 2026-07-12
scope: all 40 specs
method: spec-expert agents primed on per-spec KB (abilities/rotation/builds), adversarial verify pass
source-seed: bellular-keybinds.seed.json (unmodified — this is a findings doc only)
---

# Bellular Keybind Seed — Expert Review Findings

Every spec in `bellular-keybinds.seed.json` was reviewed by a spec-expert agent
grounded in a freshly-authored, name-reconciled per-spec KB set
(`knowledge/classes/<class>/<spec>/{abilities,rotation,builds}.md`, Midnight 12.0.7).
Each placement was judged on **role fit** *and* **press-frequency fit** (is a
constant-use ability on a slow modified key? is a rare cooldown eating a prime
unmodified slot?). Findings then passed an adversarial verify pass; only survivors
appear here, tagged **CONFIRMED** (clearly correct from the kit) or **PLAUSIBLE**
(reasonable, not certain).

**This document does not edit the seed.** The seed's placements are Bellular's
recommendations; these are independent critiques against current game data.

Verdict vocabulary: `wrong` (mis-role / not the spec's ability) · `stale-name`
(renamed/removed in 12.0.7) · `gap` (important ability left unbound or buried) ·
`weak` (defensible but a better slot exists) · `good` (affirmed — press-frequency
and role both fit).

## Systemic findings across all 40 specs

- **669 verified findings** kept across 40 specs (52 wrong · 12 stale-name · 83 gap · 118 weak · 404 good). ~102 weaker findings were dropped by the verify pass.

Recurring cross-spec patterns (the seed's systematic quirks, not one-off slips):

- **The `Class 6 (Dispel)` / `Class 5 (Purge)` buckets are frequently filled with a
  CC or utility ability for classes that have no true friendly dispel/purge** (e.g.
  Demon Hunter `Imprison` in Dispel, Hunter `Flare` in Dispel, Warlock `Banish` in
  Purge). The bucket has no correct owner, so the seed parks overflow there — read
  these as "this key is really an extra CC/utility," not a dispel.
- **The `Slow` bucket often holds a non-snare.** All three Warlocks get
  `Subjugate Demon` (an enslave, i.e. CC) in Slow while the real snare
  (`Curse of Exhaustion`) sits in a Movement/Class bucket — a straight swap fixes it.
- **Choice-node / transform pairs are double-bound.** Abilities that are the same
  button in-game (Warlock `Curse of Weakness`↔`Blight of Weakness`; DK
  `Heart Strike`↔`Vampiric Strike`; Havoc `Chaos Strike`↔`Annihilation`) sometimes
  occupy two buckets — only the talented one needs a key.
- **Some Combat 1–8 (fastest) slots hold long-cooldown or situational buttons** while
  a genuinely constant-press ability is unbound — the core press-frequency mismatch
  this review exists to catch (e.g. Devourer `Soul Immolation` on Combat 4 while the
  in-Meta spender `Collapsing Star` has no bind).
- **Placeholder / uncertain cells shipped verbatim from the source sheet**:
  literal `Free`, `Trinket Macro`, `Damage Potion`, `Racial Ability`, a Druid
  `Efflorescence?` (author's own question mark), and Monk/Priest `Res` in the `Buff`
  slot. These are intended macro/placeholder rows, not real ability bugs — flagged
  where they sit in an ability slot.
- **Midnight-new / renamed abilities the seed predates**: Demon Hunter **Devourer**
  (`Shift`, `Void Nova`, and the transform kit `Collapsing Star`/`Cull`/`Devour`),
  Hunter BM interrupt is **Counter Shot** not `Muzzle`, Demonology's S1 build casts
  **Infernal Bolt** in place of `Shadow Bolt`.

Most-repeated exact (bucket → verdict) issues:

| Bucket | Verdict | # specs |
|---|---|---|
| Class 7 (Raid Defensive) | wrong | 18 |
| (unbound) | gap | 12 |
| Res | wrong | 7 |
| (unbound — no slot) | gap | 7 |
| Buff | wrong | 5 |
| (missing binding) | gap | 5 |
| Slow | wrong | 4 |
| Class 6 (Dispel) | wrong | 3 |
| Interrupt | wrong | 3 |
| Combat 1 | stale-name | 3 |
| Buff | stale-name | 3 |
| Combat 10-12 (unbound) | gap | 3 |
| Personal Defensive 2 | gap | 3 |
| Stance 1 | stale-name | 3 |

---

## Death Knight — Blood

KB confidence: **high** · 16 verified findings (1 actionable, 15 affirmed) · 3 dropped in verify

> **Sourcing note / gaps:** Exact base cooldown/cost numbers for several abilities (Consumption ~45s, Vampiric Blood ~90s, Icebound Fortitude ~180s, Death Grip, Wraith Walk, Asphyxiate, Dark Simulacrum, Death and Decay, Blood Boil recharge) were not directly sourced from Tier-1 tooltips and carry @verify-ingame markers in abilities.md — they are talent-modifiable and approximate. No verified S1 talent import strings were captured (method.gg talents page gave the hero-tree/flex-talent narrative but the raw strings were not extractable from the JS-rendered page); left as a TODO in builds.md. Stat priority / enchant / gem s …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Immune/Spell Immune/Movement | Anti-Magic Shell | weak | PLAUSIBLE | AMS is a reactive defensive that ALSO generates Runic Power (a rotational consideration), yet it sits in the slow utility 'Immune' bucket while a faster single-modifier defensive slot appears unused. It also isn't a true immunity, so the bucket role is a loose fit. → **Move Anti-Magic Shell to a single-modifier reactiv … |

*Affirmed as correct (15):* Combat 1=Heart Strike, Combat 5=Death Strike, Combat 2=Marrowrend, Combat 6=Vampiric Blood, Combat 8=Consumption, Combat 7=Death's Caress, Interrupt=Mind Freeze, Personal Defensive 1=Icebound Fortitude, Combat 9=Dancing Rune Weapon, Combat 10=Reaper's Mark, Class 2 (CC)=Gorefiend's Grasp, Class 1 (Movement)=Death Grip, Class 7 (Raid Defensive)=Anti-Magic Zone, Class 8 (Lust/BRes)=Raise Ally …

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Anti-Magic Shell** — Not missing but buried: it's a frequent reactive defensive AND a Runic Power generator, sitting on the slow ctrl-layer Immune bucket (Ctrl+C) while the faster Personal Defensive 2 (SZ) key is empty. Should live on a single-modifier reactive …

---

## Death Knight — Frost

KB confidence: **high** · 30 verified findings (8 actionable, 22 affirmed) · 5 dropped in verify

> **Sourcing note / gaps:** All three target files pre-existed at patch 12.0.7 with high/medium confidence and were confirmed-existing (not rewritten), so no new web fetches were performed this run — sourcesUsed reflects the URLs the files were originally built from. Open items carried in the files: (1) Pillar of Frost exact cooldown flagged @verify-ingame (guides cite ~45s–1min); (2) Chosen of Frostbrood exact Midnight-era effect flagged @verify-ingame; (3) live top-key/top-parse hero-tree + engine pairing (Deathbringer+Breath vs Rider+Obliteration) not yet log-confirmed for S1; (4) precise per-build stat weights (Breat …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Combat 8 | Frostwyrm's Fury | wrong | CONFIRMED | FWF is a 3min major cooldown pressed only in burst windows, yet it occupies one of the eight fastest unmodified keys (F) while the frequent ~20s Remorseless Winter is buried on a shift slot. Clear rare-CD-in-a-spam-slot mismatch. → **Demote FWF to a Combat 9-12 shift slot and give F to Remorseless Winter (or Reaper's M … |
| Combat 11 | Remorseless Winter | wrong | CONFIRMED | Remorseless Winter is a frequent ~20s AoE cornerstone pressed on CD, but is buried on shift slot S3 while two long cooldowns (FWF 3min, ERW 2min) sit on fast unmodified keys. A frequent rotational button belongs on an unmodified Combat 1-8 key. → **Promote Remorseless Winter to an unmodified Combat slot (swap with FWF  … |
| (unassigned) | Chosen of Frostbrood | gap | CONFIRMED | Chosen of Frostbrood is in the inventory as a Midnight-era capstone Major cooldown (frequency 'cooldown', tied to the FWF burst window) but appears in no seed bucket at all — it is dropped. If it is an active press it needs a home alongside the burst cooldowns (a shift/Combat slot); its exact effect is flagged @verify- … |
| Combat 5 | Pillar of Frost | weak | PLAUSIBLE | Pillar is a ~1min anchor cooldown, not a constant press, occupying prime key Q. As the highest-frequency cooldown it is a reasonable use of a spare unmodified key, but by raw frequency the buried Remorseless Winter (frequent) has a stronger claim. Defensible; the better demotion target is FWF, not Pillar. → **Keep Pill … |
| Combat 7 | Empower Rune Weapon | weak | PLAUSIBLE | ERW is a 2min charge cooldown on prime key R; a higher-frequency cooldown (Reaper's Mark ~45s) or the buried frequent Remorseless Winter out-ranks it for an unmodified slot. Real but mild frequency mismatch. → **Low priority: consider a shift-layer slot for ERW so R can hold a more frequently pressed button.** |
| Combat 10 | Reaper's Mark | weak | PLAUSIBLE | Reaper's Mark is the second-highest-frequency cooldown (~45s, pressed on CD, woven with Pillar) yet sits on shift slot S2 while 2min (ERW) and 3min (FWF) cooldowns hold prime unmodified keys — a genuine frequency inversion. → **Promote Reaper's Mark to an unmodified key ahead of FWF/ERW; e.g. onto F if FWF is demoted.* … |
| Movement Ability | Death's Advance | weak | CONFIRMED | Death's Advance is passive (grounding: 'Passive; no active press'), so binding it to the reachable single-key Movement slot (X) wastes that key while the actual active movement ability (Wraith Walk) is pushed to the shifted SX. → **Put Wraith Walk on the primary Movement key (X); drop passive Death's Advance to a park  … |
| Movement Ability 2 | Wraith Walk | weak | CONFIRMED | Wraith Walk is the only active movement button and should own the faster primary Movement key (X) rather than the shifted SX, since a passive currently occupies X. → **Promote Wraith Walk to X (paired with the Death's Advance finding).** |

*Affirmed as correct (22):* Combat 1=Obliterate, Combat 2=Frost Strike, Combat 3=Howling Blast, Combat 4=Frostscythe, Combat 6=Glacial Advance, Combat 9=Breath of Sindragosa, Combat 12=Raise Dead, Class 1 (Movement)=Death Grip, Self-Heal 1=Death Strike, Self-Heal 2=Lichborne, Self-Heal 3 (Overflow)=Death Coil, Self-Heal 4 (Emergency/Overflow)=Death Pact, Class 7 (Raid Defensive)=Anti-Magic Zone, Class 8 (Lust/BRes)=Raise Ally …

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Chosen of Frostbrood** — Listed in the inventory as a Midnight-era capstone cooldown tied to the FWF burst window, but the seed assigns it to no bucket at all. If it is an active press it needs a home (likely a shift/Combat slot alongside the other burst cooldowns) …
- **Death Grip (as gap-closer) — no gap, noted** — Present and placed; not missing. (No action.)
- **Anti-Magic Zone / Personal Defensive 2** — Personal Defensive 2 (SZ) is left unused by the seed while Frost has multiple defensives competing for the reactive Ctrl layer. Lichborne or Death Pact could be promoted to the reachable SZ single key instead of sitting on C2/C4, improving  …

---

## Death Knight — Unholy

KB confidence: **high** · 20 verified findings (8 actionable, 12 affirmed) · 1 dropped in verify

> **Sourcing note / gaps:** Rotation/abilities are high-confidence (Tier-1 simc APL + Tier-3 method.gg agree; names reconciled against SpellName.csv — Putrefy 1247378, Dread Plague 251966, Necrotic Coil 1242172, Epidemic all confirmed live). builds.md is medium-confidence: (1) method.gg's three named Rider import strings did not render (page is JS-rendered — only build NAMES came through; only the simc Rider string was captured verbatim); (2) no San'layn reference string or Rider-vs-San'layn usage-split data (murlok/WCL) was pulled, so that recommendation leans on method.gg prose; (3) no stat-priority/enchant/gem source  …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| PvP 2 | Zombify | stale-name | CONFIRMED | Confirmed: 'Zombify' does not appear anywhere in the 12.0.7 DK inventory — it is not a real ability for this spec. → **Remove; leave Free or fill with a real PvP tool (e.g. Lichborne anti-CC).** |
| (unbound gap) | Apocalypse Now | gap | PLAUSIBLE | Confirmed gap: Apocalypse Now (Rider capstone burst CD, priority 'cooldown') is in the inventory and is an active on-CD press for Rider builds, but no seed slot binds it. Empty Combat/Free slots exist. → **Bind to an empty Combat (S2/S3) or Free slot for Rider-of-the-Apocalypse builds.** |
| (unbound gap) | Gift of the San'layn | gap | PLAUSIBLE | Confirmed gap: Gift of the San'layn (San'layn burst window, priority 'cooldown') is an active hero cooldown in the inventory but is left unbound in the seed. → **Bind to a free shift/alt slot for San'layn builds.** |
| Combat 12 | Raise Dead | weak | PLAUSIBLE | Raise Dead is a 'rare' pre-combat pet summon (priority 'rare'), so a once-per-pull cast occupying a shift-layer Combat slot is sub-optimal — Alt/Free-layer material. Not egregious (not on an unmodified 1-8 key). → **Move to an Alt/Free slot and free the Combat slot for an unbound hero burst CD.** |
| Class 2 (CC) | Death and Decay | weak | CONFIRMED | Role mislabel confirmed: Death and Decay is a FREQUENT rotational AoE button (priority 'frequent'; leads the AoE list and drives Putrefy CD reduction via Cycle of Death), not a CC. Parking it in the CC bucket is a semantic mismatch. → **Move to a free unmodified/near-unmodified Combat slot and reserve the CC bucket for … |
| Self-Heal 3 (Overflow) | Death Coil | weak | PLAUSIBLE | Factually true: Death Coil is a rotational damage spender and only self-heals while Lichborne is active, so it is a weak 'self-heal' — and it duplicates Combat 3. The genuine RP-overflow defensive (Death Strike) is already at Self-Heal 1. (Note: an RP-dump use is defensible, so this is a soft point.) → **Consider repur … |
| Class 5 (Purge) | Control Undead | weak | PLAUSIBLE | Confirmed placeholder: no offensive purge exists in the inventory; Control Undead is a rare enslave-undead utility, not a purge. → **No purge exists — leave Free, or rebind Control Undead to a Free/Alt utility slot fitting a rare cast.** |
| Class 6 (Dispel) | Path of Frost | weak | PLAUSIBLE | Confirmed placeholder: Unholy has no dispel in the inventory, and Path of Frost is water-walking utility, not a dispel. Harmless but a bucket mismatch. → **Accept the spec has no dispel — leave the slot Free, or move Path of Frost to a true utility/Free bind.** |

*Affirmed as correct (12):* Combat 1=Scourge Strike, Combat 2=Festering Strike, Combat 3=Death Coil, Combat 4=Putrefy, Combat 5=Dark Transformation, Combat 8=Soul Reaper, Combat 9=Army of the Dead, Class 1 (Movement)=Death Grip, Interrupt=Mind Freeze, Class 7 (Raid Defensive)=Anti-Magic Zone, Class 8 (Lust/BRes)=Raise Ally, Personal Defensive 1=Icebound Fortitude

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Apocalypse Now** — Rider of the Apocalypse hero capstone burst CD (summons all four Horsemen) — a real on-cooldown press for Rider builds, but the seed binds no slot for it. Combat 10/11 (S2/S3) and the Free slots (AR/AF) are empty and should hold it.
- **Gift of the San'layn** — San'layn hero burst window layered onto Dark Transformation — an active cooldown for San'layn builds, left unbound. Should take a free shift/alt slot for whichever hero tree is active.
- **Anti-Magic Shell** — Placed only on the 'Immune/Spell Immune/Movement' Ctrl-combo key (CC). AMS is a ~1min reactive defensive AND an active RP generator pressed fairly often; a Ctrl-chorded double-C is awkward for something used this reactively. Consider surfac …

---

## Demon Hunter — Devourer

KB confidence: **medium** · 20 verified findings (5 actionable, 15 affirmed) · 4 dropped in verify

> **Sourcing note / gaps:** Brand-new Midnight spec with no Warcraft Logs / murlok ladder history yet, so no top-log opener or usage-split sanity check was possible. Wowhead's Devourer guide pages are JS-rendered and returned only nav shells (fetch failed) — rotation/abilities came from method.gg + Icy Veins (Tier 3) plus the Tier-1 simc APL, whose sub-list conditions (reaps/melee_combo/math_for_wizards) were summarized rather than reproduced line-for-line. Several exact numbers are Tier-3-sourced and flagged @verify-ingame: Consume Fury/Soul yield, Void Ray in-Meta CD (14 vs 16s), Collapsing Star Soul cost, Soul Immolat …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| (unbound) | Collapsing Star | gap | CONFIRMED | The in-Meta payoff spender (30 Souls, always crits, ramps per cast; priority: frequent during burst) has NO bucket. Unlike Cull/Devour/Eradicate it is a genuinely NEW button unlocked only inside Void Metamorphosis, not an overlay of a base ability, so it needs its own key — the Meta rotation is otherwise unbindable. Bi … |
| (unbound) | Hungering Slash | gap | PLAUSIBLE | Core builder of the Void-Scarred melee-hybrid build (converts Voidblade/The Hunt into slashes; priority: frequent in that build) — absent from the seed, so melee-hybrid players have no bind. Build-conditional: only relevant when that talent build is chosen. → **Assign a free fast/shift key (S1-S4) when running the Void … |
| Combat 4 | Soul Immolation | weak | CONFIRMED | Soul Immolation is a ~1min Soul/Fury maintenance pump (priority: cooldown) occupying Combat 4, a prime unmodified digit meant for constantly-pressed rotational buttons — while the genuinely-frequent in-Meta Collapsing Star has no bind at all. Frequency mismatch is directly backed by the priority list. → **Move Soul Imm … |
| Combat 8 | Vengeful Retreat | weak | PLAUSIBLE | Vengeful Retreat is a situational evasive reposition (~25s, priority: situational) on unmodified F — a fastest-tier key better reserved for a rotational press, while frequent Meta buttons are unbound. (Note: some DH builds do keep VR on a fast key offensively, so this is debatable.) → **Move Vengeful Retreat to Movemen … |
| Class 6 (Dispel) | Imprison | weak | PLAUSIBLE | The Dispel bucket (CE) holds Imprison, which is CC (incapacitate), not a friendly dispel. DH/Devourer has no friendly dispel in the inventory, so the bucket has no true owner; parking overflow CC here is defensible but the ability under a 'Dispel' key is actually a CC. → **Leave Imprison as extra CC (label mismatch onl … |

*Affirmed as correct (15):* Combat 1=Consume, Combat 2=Reap, Combat 3=Void Ray, Combat 5=Void Metamorphosis, Combat 7=Voidblade, Interrupt=Disrupt, Movement Ability=Shift, Personal Defensive 1=Blur, CC=Void Nova, CC 2=Sigil of Misery, Class 5 (Purge)=Consume Magic, Class 7 (Raid Defensive)=Darkness, Class 3 (Tag)=Throw Glaive, Class 4 (Special)=Spectral Sight …

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Collapsing Star** — The in-Meta payoff spender (30 Souls, always crits, ramps per cast; priority: frequent during the burst window) has NO bucket in the seed. Unlike Cull/Devour/Eradicate which overlay their base-form keys inside Meta, Collapsing Star is a gen …
- **Eradicate** — The AoE frontal-cone multi-target backbone (replaces Reap after a full Void Ray channel; priority: frequent). It replaces Reap so it can inherit the Reap key (Combat 2/2), likely needing no separate bind — but the seed never acknowledges it …
- **Cull / Devour** — Meta-form upgrades of Reap/Consume. They auto-replace their base abilities on the same buttons (Combat 2 and Combat 1), so no new key is required — worth confirming the overlay assumption so in-Meta builders stay pressable.
- **Hungering Slash** — Core builder of the Void-Scarred melee-hybrid build (converts Voidblade/The Hunt into slashes; priority: frequent in that build). Not in the seed at all; melee-hybrid players have no bind — needs a fast/shift key when that talent build is c …
- **Pierce the Veil** — Void-Scarred's Meta-only empowered Voidblade (triggers Voidsurge). Build-specific; overlays Voidblade (Combat 7/R) in Meta so likely no separate bind, but entirely unmentioned by the seed for melee-hybrid players.

---

## Demon Hunter — Havoc

KB confidence: **high** · 22 verified findings (4 actionable, 18 affirmed) · 0 dropped in verify

> **Sourcing note / gaps:** Exact Fury costs (Chaos Strike 40 / Blade Dance 35 / Eye Beam 30) and several ability cooldowns (Consume Magic, Chaos Nova, Essence Break) are from historical/guide values, not scraped live from 12.0.7 spell data — flagged @verify-ingame in abilities.md. Talent import strings (simc Tier-1 + method.gg) are captured but not verified to load as Fel-Scarred in-game (@verify-ingame in builds.md). No gearing/stat-priority/enchant section was authored (out of the 3-file scope; noted as a TODO in builds.md). method.gg is JS-rendered — used the /playstyle-and-rotation and /talents sub-URLs plus Icy Vei …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Combat 10-12 (open) | Fel Barrage | gap | PLAUSIBLE | Talent-gated AoE-burst major cooldown (~60s channel) in the inventory with no seed bind. Not in the default S1 build so low priority, but if specced it is an on-CD burst button with no home. → **If Fel Barrage is talented, assign it to an open shift-Combat slot (Combat 10-12).** |
| Combat 10-12 (open) | Sigil of Spite | gap | PLAUSIBLE | Talent-gated rotational sigil (damage + soul fragments) in the inventory with no seed bind. Niche Havoc uptake, but if run it becomes an on-CD rotational button with no home. → **If Sigil of Spite is talented, assign it to an open shift-Combat slot.** |
| Class 3 (Tag) | Throw Glaive | weak | PLAUSIBLE | Fine as a ranged tag for Fel-Scarred/non-AR. But under Aldrachi Reaver this becomes Reaver's Glaive after 6 fragments and enters the core rotation (empowers next Chaos Strike + Blade Dance per inventory) — a semi-rotational button on a slow shift/class key. Conditional on hero-talent choice. → **Fine for Fel-Scarred /  … |
| Class 6 (Dispel) | Imprison | weak | CONFIRMED | Imprison is single-target CC (inventory: 'Incapacitates'), not a dispel. Havoc has no friendly/defensive dispel, so the Dispel bucket is genuinely repurposed as a third CC key (the two CC buckets already hold Chaos Nova + Sigil of Misery). Real role/label mismatch, though best available use. → **Acceptable overflow giv … |

*Affirmed as correct (18):* Combat 1=Chaos Strike, Combat 2=Blade Dance, Combat 3=Eye Beam, Combat 4=Immolation Aura, Combat 5=Essence Break, Combat 6=The Hunt, Combat 7=Felblade, Combat 8=Vengeful Retreat, Combat 9=Metamorphosis, Class 5 (Purge)=Consume Magic, Interrupt=Disrupt, Movement Ability=Fel Rush, CC=Chaos Nova, CC 2=Sigil of Misery …

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Fel Barrage** — Talent-gated AoE-burst major cooldown (~60s channel). If specced, it's an on-CD burst button with no bind in the seed. Low priority since it's not in the default S1 build, but note there's an open Combat 10-12 (S2-S4) slot it could take whe …
- **Sigil of Spite** — Talent-gated rotational sigil (damage + soul fragments). Niche Havoc uptake, but if run it becomes an on-CD rotational button with no bind. Same open shift-Combat slots are available.
- **Sigil of Flame / second personal defensive** — Not a real gap — Havoc has no baseline self-heal button (Soul Fragment healing is passive), so the empty Self-Heal 1-4 buckets are correct, and there's no baseline second personal defensive (Netherwalk is a talent) to fill Personal Defensiv …

---

## Demon Hunter — Vengeance

KB confidence: **medium** · 3 verified findings (3 actionable, 0 affirmed) · 3 dropped in verify

> **Sourcing note / gaps:** Rotation.md is high-confidence (full Tier-1 simc APL captured verbatim). Gaps/flags: (1) Exact Fury values and several cooldowns in abilities.md come from Tier-3 guides (Icy Veins/method.gg/Wowhead) rather than a Tier-1 tooltip pull — marked @verify-ingame. (2) Spirit Bomb appears to now have a ~25s haste-reduced cooldown in Midnight (the APL references cooldown.spirit_bomb) — a real change worth confirming in-game. (3) Metamorphosis 2min CD + Fracture +15 Fury confirmed via web but not a Tier-1 tooltip. (4) Only the Annihilator Tier-1 simc talent string was available on the midnight branch; n …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 6 (Dispel) | Imprison | wrong | CONFIRMED | Imprison is a single-target CC/incapacitate (grounding function: 'CC (incapacitate)'), not a dispel. Vengeance DH has no friendly PvE dispel in the inventory: Consume Magic is an offensive purge (already correctly placed in Class 5 Purge) and Reverse Magic is PvP-only. So the Dispel bucket has no legitimate occupant an … |
| (unassigned — no seed slot) | Untethered Rage | gap | CONFIRMED | Untethered Rage is in the inventory as an activated Apex/Annihilator cooldown ('Instant (activates a granted charge)', the Annihilator burst trigger, ~1/min+) and in the priority list at freq 'cooldown', but it is assigned to none of the 35 seed slots. An Annihilator DH would have no key to activate the granted Metamor … |
| (unassigned — no seed slot) | Reaver's Glaive | gap | CONFIRMED | Reaver's Glaive is the Aldrachi Reaver rotational spender/empower (priority freq 'frequent') that starts the AR damage cycle (Rending Strike + Glaive Flurry), but it has no bucket in the seed. An Aldrachi Reaver DH would have no key for it. Note: a DH runs exactly one hero tree, so exactly one of Untethered Rage / Reav … |

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Untethered Rage** — Apex/Annihilator cooldown — activates the granted special Metamorphosis charge on proc (~1/min+), the core Annihilator burst trigger. It is not assigned to any bucket in the seed, so the Annihilator burst window has no key. Should occupy a  …
- **Reaver's Glaive** — Aldrachi Reaver rotational-spender/empower that starts the AR damage cycle (Rending Strike + Glaive Flurry). Marked 'frequent' in the priority list yet has no bucket. AR players would have no key for it. Needs a fast/shift-layer slot if pla …

---

## Druid — Balance

KB confidence: **high** · 15 verified findings (3 actionable, 12 affirmed) · 3 dropped in verify

> **Sourcing note / gaps:** Rotation/builds are high-confidence (Tier-1 simc midnight APL, distilled directly). Ability cast-time/cooldown numbers in abilities.md were NOT pulled from the live Blizzard spell API this pass — they are experience/tooltip estimates and carry @verify-ingame markers (Eclipse charge count + recharge, Celestial Alignment/Incarnation CD + charges, Starfire cast, Solar Beam CD, Renewal/Mighty Bash/Faerie Swarm/Heart of the Wild CDs, Ascendant Eclipses CD). Name reconciliation done vs raw/wago/SpellName.csv: 'Eclipse' is now an activated button in Midnight (Lunar Eclipse spell 1233272 / Solar Eclip …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Combat 7 | Lunar Eclipse | gap | CONFIRMED | Inventory lists a generic 'Eclipse' toggle ('frequent' press, enters the side armed by the last builder) plus separate Solar Eclipse and Lunar Eclipse states. The seed binds ONLY Lunar Eclipse, leaving no key to enter the Solar side (Wrath-empowered, used for Solar filler / <=3 targets) — a real core-loop gap. → **Bind … |
| (unbound) | Ascendant Eclipses | gap | PLAUSIBLE | The Midnight capstone active burst (spell 1261564, 'cooldown' frequency) is not bound anywhere. If this capstone is talented it needs a Shift/Combat key; build-dependent, so flag on talent swaps. → **If running the Ascendant Eclipses capstone, give it a cooldown-layer key.** |
| Self-Heal 4 (Emergency/Overflow) | Heart of the Wild | weak | CONFIRMED | Heart of the Wild is a ~5-min off-role empowerment cooldown, not an emergency self-heal — a role mismatch for this bucket. Meanwhile Renewal (the spec's genuine instant self-heal, a reactive defensive) is left unbound entirely. → **Bind Renewal in a Self-Heal slot; move Heart of the Wild to an Overflow/utility-CD slot  … |

*Affirmed as correct (12):* Combat 1=Wrath, Combat 2=Starfire, Combat 3=Moonfire, Combat 4=Sunfire, Combat 5=Starsurge, Combat 6=Starfall, Combat 8=Fury of Elune, Combat 9=Celestial Alignment, Combat 11=Force of Nature, Combat 12=Wild Mushroom, Interrupt=Solar Beam, Personal Defensive 1=Barkskin

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Solar Eclipse** — Post-rework, Solar and Lunar Eclipse are separate activated states. The seed binds only Lunar Eclipse (Combat 7), so the Solar side (Wrath-empowered, used ≤3 targets) cannot be entered — a core-loop gap. Bind the 'Eclipse' toggle or add a S …
- **Ascendant Eclipses** — The new Midnight capstone active burst (spell 1261564) is not bound anywhere. If talented it's a cooldown-frequency press that needs a Shift/Combat slot.
- **Renewal** — The spec's instant self-heal (reactive defensive) is unbound while Self-Heal 2 (C2) sits empty and a 5-min utility CD occupies the emergency-heal slot. Should own a Self-Heal key.
- **Incarnation: Chosen of Elune** — Preferred M+/council burst; only Celestial Alignment (its base form) is bound. If the Incarnation node is talented, the Combat 9 bind should be Incarnation, not CA.
- **New Moon / Half Moon / Full Moon** — The Moon-chain builders are unbound. Acceptable given the seed assumes the Force of Nature build (Combat 11), but if the player runs the Moon-chain talent these 'frequent' generators have no keys — build-dependent gap to flag on talent swap …

---

## Druid — Feral

KB confidence: **high** · 13 verified findings (5 actionable, 8 affirmed) · 2 dropped in verify

> **Sourcing note / gaps:** Exact Energy/CP costs and several cooldown durations in abilities.md were not pulled from a Tier-1 tooltip dump this pass (Blizzard spell API / wago SpellEffect not queried) — they are standard Feral values and carry @verify-ingame where Midnight may have retuned. Midnight-new interactions flagged for in-game verification: Unseen Predator buff mechanics, Panther's Guile double-Bite proc, Ravage/Claw Rampage proc conditions, and the reported removal of Brutal Slash/Thrash from the Feral kit. Ferocious Bite vs Ravage naming: talents.md marks Unseen Predator (spell 1263657) as ACTIVE while it rea …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| (unbound) | Ravage | gap | CONFIRMED | Ravage — Druid of the Claw proc spender marked 'frequent — reactive, press ASAP' in the priority — appears in no seed bucket. A proc-driven spender that must fire immediately is a live, unbound damage button. → **Bind Ravage to a fast/reactive key (it can overlap Ferocious Bite's slot conceptually, but needs a real hom … |
| Self-Heal | Renewal | gap | CONFIRMED | Renewal — instant self-heal (~1.5min class talent), a genuine on-demand defensive — is absent from the seed entirely, while Innervate (mana support) and Heart of the Wild (5-min empower) fill the self-heal overflow slots. Renewal is the stronger self-heal-bucket candidate. → **Place Renewal in a Self-Heal slot, displac … |
| Combat 11 | Moonfire | weak | PLAUSIBLE | Priority marks Moonfire (Lunar Inspiration) 'frequent' — a maintained DoT — yet it sits on the slower shift-layer. Real but mild frequency/key tension; talent-conditional and slow pandemic cadence, and the unmodified Combat slots are all occupied by higher-priority abilities. → **Acceptable as-is; an unmodified slot wo … |
| Self-Heal 3 (Overflow) | Innervate | weak | CONFIRMED | Innervate is ally mana-support Utility ('grants an ally free spellcasting'), not a self-heal. It occupies a self-heal slot while Renewal — an actual instant self-heal (~1.5min) — is off the bar entirely. Clear role mismatch. → **Swap Innervate for Renewal so the self-heal bucket holds a real self-heal; park Innervate o … |
| Self-Heal 4 (Emergency/Overflow) | Heart of the Wild | weak | PLAUSIBLE | Heart of the Wild is a 'rare' 5-min hybrid empower with minor Feral use — not an emergency self-heal despite the bucket name. Fine as overflow filler only. → **Consider Renewal for one of the two overflow self-heal slots.** |

*Affirmed as correct (8):* Combat 1=Shred, Combat 3=Rip, Combat 5=Tiger's Fury, Combat 10=Convoke the Spirits, Interrupt=Skull Bash, Personal Defensive 2=Survival Instincts, Stance 2=Cat Form, Taunt/Quick Access=Prowl

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Ravage** — Druid of the Claw proc spender, marked 'frequent — reactive, press ASAP' in the priority, but it appears in no bucket. A proc-driven spender you must fire immediately needs a fast/reactive key; omitting it leaves a live damage button unboun …
- **Renewal** — Instant self-heal (~1.5min class talent) — a genuine on-demand defensive — is left off entirely, while Innervate (mana support) and Heart of the Wild (5-min empower) occupy the self-heal overflow slots. Renewal is the stronger self-heal-buc …
- **Incarnation: Avatar of Ashamane** — The choice-node alternative to Convoke; if the player talents Incarnation instead, it has no bucket. Not a hard gap (shares Convoke's node) but should occupy Combat 10 when chosen.

---

## Druid — Guardian

KB confidence: **high** · 13 verified findings (3 actionable, 10 affirmed) · 3 dropped in verify

> **Sourcing note / gaps:** Exact Rage costs are uncertain: sources disagree (method/Icy Veins list Ironfur ~30 Rage, historical value ~40; Frenzied Regeneration listed by Icy Veins as "10 rage per tick" vs the historical charge-based no-cost) — flagged @verify-ingame in abilities.md, functions are solid. Method.gg /abilities and /rotation sub-URLs 404; content pulled from /playstyle-and-rotation + /talents instead. Wowhead rotation page returned only a nav shell. Rage of the Sleeper appears superseded by Wild Guardian (spell 1269614) in the Midnight Guardian tree per talents.md — flagged @verify-ingame. builds.md intent …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 7 (Raid Defensive) | Prowl | wrong | CONFIRMED | Prowl is cat-form stealth, not a defensive of any kind. Guardian has no raid-wide defensive in its kit, so labeling stealth as a Raid Defensive is a pure role mismatch. Verified: Prowl's inventory function is 'Utility (stealth)'. → **Leave the Raid Defensive bucket Free (Guardian lacks a true one) or move Prowl to an A … |
| Combat 7 | Swipe | weak | PLAUSIBLE | Swipe is the lowest-priority filler in the priority list ('situational', Druid of the Claw) yet sits on a prime unmodified rotational key, while the burst capstone Wild Guardian is left entirely unbound. Verified against priority frequencies. → **Demote Swipe to a shift/overflow slot and promote Wild Guardian to a fast … |
| Combat 12 | Bristling Fur | weak | PLAUSIBLE | Bristling Fur is a situational rage-refill (priority: 'situational') parked on a shift-layer combat-cooldown slot, while the spec's signature Midnight burst capstone Wild Guardian (in inventory, priority 'cooldown', fired at max Thrash / during Ravage or Lunar Beam) has no slot anywhere in the seed. This is the seed's  … |

*Affirmed as correct (10):* Combat 1=Mangle, Combat 2=Thrash, Combat 5=Ironfur, Combat 4=Frenzied Regeneration, Combat 8=Lunar Beam, Interrupt=Skull Bash, Taunt/Quick Access=Growl, Personal Defensive 1=Barkskin, Stance 1=Bear Form, Class 5 (Purge)=Soothe

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Wild Guardian** — The Midnight-new burst capstone active (spell 1269614, replacing Rage of the Sleeper) is completely absent from the seed. It is a core cooldown fired at max Thrash / during Ravage or Lunar Beam — it must own a shift-cooldown slot (e.g. swap …
- **Incarnation: Guardian of Ursoc** — The standard tank capstone major CD is unbound. Defensible IF the build took Berserk + Convoke instead (choice node), which the seed appears to assume — but if Incarnation is talented it has no slot. Verify against the actual talent build.

---

## Druid — Restoration

KB confidence: **medium** · 20 verified findings (7 actionable, 13 affirmed) · 6 dropped in verify

> **Sourcing note / gaps:** No Tier-1 SimulationCraft APL/profile exists for Restoration (SimC's midnight branch ships only Druid Balance/Feral/Guardian DPS/tank profiles — confirmed no MID1_Druid_Restoration.simc), so rotation ordering and builds are guide-consensus (Tier 3 method.gg + Icy Veins + Wowhead + Maxroll), not sim-optimized — hence medium confidence. HERO-TREE ASSIGNMENT IS CONTESTED: method.gg's talents page (2026-06-16) says Wildstalker=raid / Keeper of the Grove=M+, while wowlazymacros and method's own Playstyle-page framing say the reverse (Keeper=raid / Wildstalker=M+) — flagged @verify-ingame in builds. …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Self-Heal 2 | Starsurge | wrong | CONFIRMED | Starsurge is an instant Astral DPS nuke ('downtime DPS' in grounding), not a self-heal or emergency button. Parked in a Self-Heal bucket purely to give it a home — role mismatch. → **Move to Free/Alt if kept at all; reserve Self-Heal buckets for actual survivability.** |
| Class 7 (Raid Defensive) | Efflorescence? | wrong | CONFIRMED | Two confirmed problems: (1) Efflorescence is a ground-targeted AoE healing zone per grounding, not a raid defensive; Resto's closest raid-CD is Tranquility (already Combat 9). (2) It is 'frequent' (keep the zone down) yet buried on a slow reactive Ctrl key — hidden from the fast rotation. The trailing '?' confirms the  … |
| Flourish (unplaced) | (none) | gap | PLAUSIBLE | Flourish appears in the grounding priority list as an active 'cooldown' press (stretch HoTs after a ramp) but has no key. Its choice-node alternative is a passive (Inner Peace), so when talented it is a standalone button with no home. Real conditional gap; a Free slot is available. → **Assign Flourish to a Free/Alt coo … |
| Frenzied Regeneration (unplaced) | (none) | gap | PLAUSIBLE | Bear-form self-heal is in the grounding priority ('reactive') for bear-weave survivability but unplaced. Niche for Resto, but a valid gap. Caveat: the 'Personal Defensive 2 (SZ)' slot the reviewer cites is not present in the given seed slice. → **Place on a personal-defensive/Alt key if bear-weaving; low priority other … |
| Combat 1 | Wrath | weak | CONFIRMED | Real press-frequency inversion: Wrath is 'situational' downtime-DPS/mana filler in the grounding priority, yet holds an unmodified combat key while genuinely 'frequent' heals (Wild Growth, Efflorescence) sit on the slower Shift/Ctrl layers. The reviewer's 'single fastest key' phrasing is ergonomically imprecise, but th … |
| Combat 2 | Starfire | weak | CONFIRMED | Clearest inversion: Starfire does not appear anywhere in the priority/frequency list (lowest-value filler) yet occupies a fast unmodified combat key while frequent heals are on modifier layers. → **Move a frequent heal (Efflorescence/Wild Growth) here; push Starfire to a modifier slot or Free.** |
| Combat 11 | Wild Growth | weak | CONFIRMED | Wild Growth is 'frequent' (on ~8s CD, triggers Symbiotic Blooms/Grove Guardians) but sits on the Shift layer while situational/absent DPS filler (Wrath/Starfire) holds unmodified keys. Under-prioritized for key speed. (Also covers the reviewer's Wild Growth gap note — same issue.) → **Promote to an unmodified Combat 1- … |

*Affirmed as correct (13):* Combat 5=Rejuvenation, Combat 6=Regrowth, Combat 7=Lifebloom, Combat 8=Swiftmend, Class 6 (Dispel)=Nature's Cure, Combat 3=Moonfire, Combat 4=Sunfire, Self-Heal 3 (Overflow)=Innervate, Combat 12=Ironbark, Personal Defensive 1=Barkskin, Class 5 (Purge)=Soothe, Class 8 (Lust/BRes)=Rebirth, Stance 1=Bear Form

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Convoke the Spirits** — A major cooldown and the Wildstalker default (~1min with Cenarius' Guidance) is unplaced. It is a choice-node vs Incarnation (which the seed did place on Combat 10), so this is defensible if the player runs Keeper — but if Wildstalker is ch …
- **Flourish** — HoT-extend cooldown (~90s, huge throughput after a ramp) has no bucket. It is a choice-node vs Inner Peace so may be untalented, but when talented it is an active press with no home.
- **Efflorescence** — Technically placed, but mis-bucketed as a 'Raid Defensive' and buried on a slow Ctrl key despite being a 'frequent' maintained heal — effectively hidden from the fast rotation.
- **Wild Growth** — Placed on the Shift layer while situational DPS filler (Wrath/Starfire) holds unmodified keys 1-2 — a 'frequent' on-cooldown heal is under-prioritized for key speed.
- **Frenzied Regeneration** — Bear-form self-heal (emergency personal survivability while bear-weaving) is omitted; with an empty Personal Defensive 2 (SZ) slot available, it could reasonably occupy it.

---

## Evoker — Augmentation

KB confidence: **medium** · 15 verified findings (6 actionable, 9 affirmed)

> **Sourcing note / gaps:** No MID1_Evoker_Augmentation.simc profile exists in the simc midnight branch — only the augmentation_12_0_5 APL function in apl_evoker.cpp (already the basis for rotation.md). Talent import strings in builds.md are therefore Tier-3 (method.gg), not cross-checked against a Tier-1 loadout; verify hero tree on import. Several ability cooldowns/charge counts carry @verify-ingame markers (Prescience charges, Breath of Eons CD, Blistering Scales, Time Skip amount, Spatial Paradox values, PvP-talent details). Scalecommander-vs-Chronowarden ST gap cited inconsistently across guides (~2% method vs ~3% o …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 7 (Raid Defensive) | Source of Magic | wrong |  | Source of Magic is a mana-battery utility assigned once to a healer, not a defensive at all — it does not belong in the Raid Defensive bucket. Meanwhile Zephyr, the spec's actual group damage-reduction cooldown, is filed under Class 1 (Movement). → **Move Zephyr into Class 7 (Raid Defensive); relocate Source of Magic t … |
| Res | Return | stale-name |  | Return is an out-of-combat teleport-to-portal, not a battle res (Augmentation has no combat res). It is only parked in the Res bucket as a placeholder. → **Harmless park; no action needed — just don't mistake it for a brez in-combat.** |
| Class 1 (Movement) | Zephyr | weak |  | Zephyr is primarily a group raid-DR cooldown (its movement-speed is incidental), so it is misfiled in the movement slot. The real movement abilities (Hover, Deep Breath, Verdant Embrace, Rescue) belong here or are elsewhere. → **Swap Zephyr into Class 7 (Raid Defensive) — see the Source of Magic finding — and put a gen … |
| Class 3 (Tag) | Landslide | weak |  | Landslide is a ~1.5-min line root (real CC), not a tag ability. The empty Slow (SV) bucket is a cleaner home for a root/slow than the Tag slot. → **Move Landslide to Slow (SV); a DPS Aug rarely needs a dedicated Tag bind.** |
| Self-Heal 3 (Overflow) | Tip the Scales | weak |  | Tip the Scales is a 2-min offensive empower-enabler (instant + max-rank Fire Breath), not a self-heal. Parking it in an overflow bucket is tolerable and Ctrl-layer speed is fine for a 2-min cadence, but the bucket role is semantically wrong. → **Acceptable as overflow parking given the Combat slots are full; if a Comba … |
| Class 5 (Purge) | Rescue | weak |  | Augmentation has no purge, so the bucket has no correct occupant; Rescue is an ally-save mobility cooldown parked here. Fine as a park, but it is not a purge and the empty Movement Ability 2 (SX) slot would fit its role better. → **Consider moving Rescue to Movement Ability 2 (SX); leave Purge empty since the spec lack … |

*Affirmed as correct (9):* Combat 5=Ebon Might, Combat 3=Eruption, Combat 7=Prescience, Combat 4=Fire Breath, Combat 8=Blistering Scales, Combat 9=Breath of Eons, Personal Defensive 1=Obsidian Scales, Interrupt=Quell, Class 8 (Lust/BRes)=Fury of the Aspects

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Renewing Blaze** — A real personal defensive (heals back damage taken over 8s, ~90s CD) is left off entirely while the Personal Defensive 2 slot (SZ) sits empty — it should own SZ alongside Obsidian Scales on Z.
- **Deep Breath** — Movement/damage cooldown that also extends Ebon Might and is woven into the Scalecommander kit; omitted while Movement Ability 2 (SX) is open — a natural second movement bind.

---

## Evoker — Devastation

KB confidence: **medium** · 15 verified findings (8 actionable, 7 affirmed) · 2 dropped in verify

> **Sourcing note / gaps:** abilities.md and rotation.md already existed at patch 12.0.7 (fetched 2026-07-11) and were confirmed-existing, not rewritten — their many @verify-ingame markers (exact CDs/cast times for Fire Breath, Eternity Surge, Obsidian Scales, Hover, most CC/utility) remain unresolved and downstream should confirm in-game. builds.md was authored fresh but at medium confidence: the SpellName.csv in raw/wago is an old-era dump (spell IDs read like MoP/Cata), so it only confirmed the existence of core names (Fire Breath, Firestorm, Deep Breath, Time Stop, Blessing of the Bronze Dragonflight, Living Flame) — …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 7 (Raid Defensive) | Source of Magic | wrong | CONFIRMED | Grounding tags Source of Magic as Utility (assign-once mana-return buff, frequency 'rare') — not a raid defensive. The spec's actual raid defensive (dmg reduction + speed) is Zephyr, which the seed misfiled under Class 1 (Movement). → **Put Zephyr in Class 7 (Raid Defensive); move Source of Magic to a utility/Free slot … |
| Combat 8 (F) / Combat 10-12 (empty) | (unbound — not in seed) | gap | CONFIRMED | Shattering Star (Rotational-builder: ~20s/2-charge, grants Essence Burst + damage-amp debuff when specced) is bound nowhere, while fast slots Combat 8 (F) and Combat 10-12 (S2-S4) are empty. → **Bind Shattering Star to a fast Combat slot (e.g. F) when specced.** |
| Personal Defensive 2 (SZ, empty) | (unbound — not in seed) | gap | CONFIRMED | Renewing Blaze (~90s self-heal-over-time defensive, listed unconditionally in the priority) is left off, and its natural home Personal Defensive 2 (Shift+Z) is unassigned. → **Bind Renewing Blaze to Personal Defensive 2 (SZ).** |
| Combat 8/10-12 (empty, Flameshaper) | (unbound — not in seed) | gap | PLAUSIBLE | Engulf (Flameshaper hero rotational burst that consumes the Fire Breath DoT, short CD) is unbound. The seed bound the Scalecommander button (Deep Breath) but not the Flameshaper one, so a Flameshaper build has no bind for its key button. → **Bind Engulf to a fast Combat slot when running Flameshaper.** |
| Combat 10-12 (empty Shift slot) | (unbound — not in seed) | gap | PLAUSIBLE | Firestorm (~20s ground AoE spender, AoE-lean talent) has no bind; when specced it is an active rotational press and empty Shift-layer Combat slots are available. → **Bind Firestorm to an open Combat/Shift slot when specced.** |
| Combat 9 | Deep Breath | weak | CONFIRMED | Priority lists Deep Breath as 'frequent' (Scalecommander rotational button, ~2x per window) yet it sits on the Shift-layer S1 while unmodified fastest-tier Combat 8 (F) is confirmed empty for this spec. → **Promote Deep Breath to the empty Combat 8 (F) so a frequent rotational press lands on an unmodified key; leave S1 … |
| Class 1 (Movement) | Zephyr | weak | CONFIRMED | Grounding explicitly describes Zephyr as a raid damage-reduction defensive; its movement-speed is secondary. Miscategorized as the class Movement button. → **Move Zephyr to Class 7 (Raid Defensive); pairs with the Source-of-Magic fix.** |
| Self-Heal 3 (Overflow) | Tip the Scales | weak | PLAUSIBLE | Tip the Scales is a 120s offensive empower cooldown fired mid-Dragonrage (Major cooldown, not a heal). Parking is tolerated by the 'Overflow' label, but on Ctrl-layer C3 it is a slow reach for a burst-synced instant while faster Shift-layer Combat 10-12 slots sit empty. → **Consider moving to an empty Shift-layer Comba … |

*Affirmed as correct (7):* Combat 3=Disintegrate, Combat 1=Living Flame, Personal Defensive 1=Obsidian Scales, Movement Ability=Hover, Interrupt=Quell, Class 8 (Lust/BRes)=Fury of the Aspects, Combat 5=Dragonrage

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Shattering Star** — ~20s / 2-charge builder granting Essence Burst plus a damage-amp debuff — a core rotational button (frequency: cooldown, but woven often) when specced. The seed binds it nowhere, while fast slots Combat 8 (F) and Combat 10-12 (S2-S4) sit em …
- **Renewing Blaze** — Standard ~90s self-heal-over-time defensive, simply left off. Personal Defensive 2 (SZ) — its natural home — is unassigned.
- **Firestorm** — ~20s ground AoE spender talent; when specced it is an active rotational press with no bind. Belongs on an open Combat/Shift slot.
- **Engulf** — Flameshaper hero rotational burst button (consumes the Fire Breath DoT, short CD). Unbound; needs a fast slot whenever the Flameshaper build is run.

---

## Evoker — Preservation

KB confidence: **medium** · 26 verified findings (12 actionable, 14 affirmed) · 2 dropped in verify

> **Sourcing note / gaps:** All three target files already existed at patch 12.0.7 (fetched/reviewed 2026-07-11) and are complete, so per the cheap re-run guard they were confirmed-existing, not rewritten; no fresh web fetches were needed. Inherited gaps flagged inside those files: (1) No Tier-1 rotation source — SimulationCraft does not model healers, so no MID1_Evoker_Preservation.simc APL exists; rotation priority is built from agreeing Tier-3 guides (method.gg primary, Icy Veins, maxroll) at medium confidence. (2) Midnight removal of Spiritbloom, Emerald Communion, and Engulf from Preservation is flagged @verify-inga …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Combat 3 | Disintegrate | wrong | CONFIRMED | Disintegrate is 'situational' (Energy Loop mana build only) yet occupies the prime unmodified '3' key. A build-specific niche button should not sit on a fastest-tier slot on a healer. → **Demote Disintegrate to a modified/Alt slot (or leave unbound outside Energy Loop) and promote a frequent heal onto '3' — the unbound … |
| Class 1 (Movement) | Zephyr | wrong | CONFIRMED | Zephyr is a party-wide ~20% DR + HoT raid defensive, not a movement ability; it is mis-slotted into the Movement bucket while the actual Raid-Defensive bucket holds a set-once utility (Source of Magic). → **Move Zephyr to Class 7 (Raid Defensive); put a real movement/utility (Rescue or Deep Breath) in the Movement clas … |
| Class 7 (Raid Defensive) | Source of Magic | wrong | CONFIRMED | Source of Magic is a 'rare' set-once mana-return utility, not a raid defensive; the genuine raid defensive (Zephyr) is mis-parked in the Movement bucket instead. → **Put Zephyr here and move Source of Magic to an Alt/utility slot (it is applied once pre-combat).** |
| (unbound) | Merithra's Blessing | gap | CONFIRMED | Merithra's Blessing is 'frequent' — the apex Echo finisher and strongest heal, pressed whenever available — yet it is bound to NO bucket anywhere in the seed. This is the single biggest omission. → **Bind it to a fast unmodified Combat key freed from the situational damage on 2/3.** |
| (unbound) | Renewing Blaze | gap | PLAUSIBLE | Renewing Blaze is a 'reactive' self-heal-over-time defensive in the inventory but is bound to no bucket. Minor (Obsidian Scales already covers personal DR), but it is a genuinely unbound defensive. → **Bind Renewing Blaze to a secondary personal-defensive slot.** |
| (grounding gap) | Quell (interrupt) | gap | PLAUSIBLE | The inventory contains no interrupt at all, but Preservation Evoker has Quell in-game (Midnight 12.0.7). This is a grounding gap: an interrupt exists for the spec and is missing from the ability list, so any Interrupt bucket cannot be filled from the given data. → **Flag the grounding gap — verify/add Quell to the inve … |
| Combat 2 | Azure Strike | weak | CONFIRMED | Azure Strike is 'situational' off-heal-time filler damage but occupies the prime unmodified '2' key while the 'frequent' apex heal Merithra's Blessing is unbound entirely and Emerald Blossom sits on the Ctrl layer. → **Move Azure Strike to a slower slot and put a frequent spender (Merithra's Blessing / Emerald Blossom) … |
| Combat 7 | Time Dilation | weak | PLAUSIBLE | Time Dilation is a 'reactive' external ally defensive, not a rotational press; consuming the prime unmodified 'R' key that a constant/frequent heal would value is a priority mismatch. → **Relocate Time Dilation to a reactive Ctrl/single-key slot and give R to a frequent rotational heal.** |
| Combat 12 | Dream Breath | weak | PLAUSIBLE | Dream Breath is pressed on cooldown (~30s) for the guaranteed Merithra's proc — a core rotational spender — yet it is buried on shift-layer Combat 12 while situational damage (Azure Strike, Disintegrate) sits on unmodified 2/3. → **Swap Dream Breath onto a fast unmodified Combat key freed from Azure Strike/Disintegrate … |
| Class 5 (Purge) | Rescue | weak | PLAUSIBLE | Rescue is a reactive movement/reposition ability, not a purge; Preservation has no purge in the inventory, so the bucket has no true occupant and Rescue also duplicates the movement role. → **Acceptable filler given no purge exists, but Rescue fits a Movement slot better (and is the reviewer's suggested Movement replac … |
| Res | Return | weak | PLAUSIBLE | Return is a teleport-to-placed-point (portal talent), not a resurrection; Evoker has no combat res in the inventory, so the Res bucket has no real occupant — Return is only a placeholder. → **Fine as a placeholder; recognize it is not a battle-res. Nothing to correct in rotation terms.** |
| PvP | Time Stop | weak | PLAUSIBLE | Time Stop is a legitimate PvE 'reactive' external save (brief invuln on a dying ally) but is buried on the slow Alt-layer PvP key, where it is not reachable as a reactive save. → **Move Time Stop to a reactive Ctrl/single-key slot with the other externals; use the PvP alt slot for a PvP-only tool.** |

*Affirmed as correct (14):* Combat 6=Reversion, Combat 5=Echo, Combat 8=Temporal Anomaly, Combat 1=Living Flame, Combat 4=Fire Breath, Combat 11=Rewind, Self-Heal 1=Verdant Embrace, Class 6 (Dispel)=Naturalize, Class 8 (Lust/BRes)=Fury of the Aspects, Personal Defensive 1=Obsidian Scales, Movement Ability=Hover, Class 2 (CC)=Sleep Walk, PvP 3=Chrono Loop, Buff=Blessing of the Bronze

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Merithra's Blessing** — Biggest gap: it is a 'frequent' apex Echo finisher and the strongest heal, pressed whenever available, yet it is not bound to any bucket. It should own a fast unmodified Combat key (freed from Azure Strike/Disintegrate).
- **Renewing Blaze** — A 'reactive' self-heal-over-time defensive with no binding; Personal Defensive 2 (SZ) is left empty and is its natural home.
- **Interrupt (bucket empty)** — The Interrupt bucket (V) has no occupant. The provided kit contains no interrupt (Evoker's Quell is absent from the grounding), so this is a grounding gap to flag — verify whether an interrupt exists for the spec before leaving V unbound.
- **Stasis / Time Spiral** — Choice-node options (Stasis vs Dream Flight; Time Spiral vs Spatial Paradox) are unbound. Lower priority since their alternatives are placed, but a Stasis-based build has no key for its planned-burst tool.

---

## Hunter — Beast Mastery

KB confidence: **medium** · 17 verified findings (6 actionable, 11 affirmed) · 4 dropped in verify

> **Sourcing note / gaps:** Interrupt reconciliation: the seed listed "Muzzle" but that is Survival's melee interrupt — Beast Mastery uses Counter Shot (147362, class tree); flagged in-file. Bloodshed is a PASSIVE in the Midnight tree (not the old active pet CD), so it is not a rotational button. Kill Shot does not appear in the Midnight BM tree — execute pressure comes from Black Arrow/Deathblow (Dark Ranger); flagged @verify-ingame. Exact Focus costs/cooldowns for Cobra Shot (35), Wild Thrash, and Kill Command recharge are from stable-retail knowledge + one search snippet, not a live Tier-1 tooltip pull (Icy Veins spel …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 6 (Dispel) | Flare | wrong | CONFIRMED | Flare is an anti-stealth/reveal utility, not a dispel. BM has no friendly dispel; its only removal effect (Tranquilizing Shot) is already correctly in the Purge bucket. Flare is mis-slotted into a dispel role. → **Leave the Dispel bucket Free (BM lacks a dispel); relocate Flare to a situational utility/PvP slot.** |
| Class 7 (Raid Defensive) | Command Pet | wrong | CONFIRMED | Command Pet is the pet control bar (attack/follow/passive), not a raid defensive. It fills the raid-defensive slot with a non-defensive; BM's only external/raid-facing defensive is Roar of Sacrifice, which is currently misplaced on Combat 12. → **Move Roar of Sacrifice here; unbind Command Pet (it lives on the pet bar) … |
| Interrupt | Muzzle | wrong | CONFIRMED | Muzzle is Survival's melee interrupt; BM's interrupt is Counter Shot (ranged, 24s, 3s lockout) per the grounding note. The dedicated single-key interrupt slot holds a non-BM ability and BM is left with no kick bound at all — a reactive must-press with no home. → **Bind Counter Shot to the Interrupt bucket.** |
| PvP 2 | Dire Beast: Hawk | wrong | CONFIRMED | Dire Beast is a passive in the Midnight BM tree (it passively summons short-lived beasts); it is not an activatable button. Binding 'Dire Beast: Hawk' to a key does nothing. → **Leave PvP 2 Free or place a real niche control (e.g. Scare Beast).** |
| Combat 7 | (unassigned / Free) | gap | CONFIRMED | Nature's Ally — an active spec capstone (Instant · CD) that empowers Kill Command and is pressed on cooldown in the core rotation — is not placed anywhere in the seed map. A rotational active with no binding is a real gap. → **Assign Nature's Ally to a fast unmodified combat slot (e.g. Combat 7).** |
| Combat 12 | Roar of Sacrifice | weak | CONFIRMED | Roar of Sacrifice is a reactive external defensive, not a rotational press, yet it occupies a combat/rotational slot while the actual raid-defensive bucket holds junk (Command Pet). Real role mismatch, though the slot is a shift-layer key so impact is moderate. → **Swap Roar into Class 7 (Raid Defensive) and free Comba … |

*Affirmed as correct (11):* Combat 1=Cobra Shot, Combat 2=Barbed Shot, Combat 3=Kill Command, Combat 4=Wild Thrash, Combat 5=Black Arrow, Combat 6=Bestial Wrath, Slow=Concussive Shot, CC=Intimidation, Class 8 (Lust/BRes)=Ancient Hysteria, Immune/Spell Immune/Movement=Aspect of the Turtle, Personal Defensive 1=Survival of the Fittest

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Counter Shot** — BM's actual interrupt — entirely absent because the Interrupt bucket holds Survival's Muzzle instead. A reactive must-press with no binding is a critical gap.
- **Nature's Ally** — Capstone active that empowers Kill Command, pressed on cooldown in the core rotation, but not placed anywhere. Prime fast keys Combat 7/8 sit empty.
- **Wailing Arrow** — Dark Ranger rotational cooldown (guaranteed Deathblow, overlays the Bestial Wrath button after activation) — missing from the map despite being a frequent-tier press in that build.

---

## Hunter — Marksmanship

KB confidence: **high** · 13 verified findings (7 actionable, 6 affirmed) · 3 dropped in verify

> **Sourcing note / gaps:** Seed list name error: it listed "Muzzle" as MM's interrupt — that is Survival's melee interrupt. MM's interrupt is Counter Shot (spell 147362, confirmed in talents.md class tree + SpellName.csv); authored as Counter Shot. Chimaeral Sting (356719) is a PvP talent, not a PvE rotational button. method.gg /rotation and /abilities subpages 404 — used the /playstyle-and-rotation subpage instead (12.0.7, upd 2026-06-16). Wowhead rotation page returned only nav shell (JS-rendered), not used. Exact cooldown/cast values for several utility/defensive abilities (Binding Shot, Survival of the Fittest, Harr …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 7 (Raid Defensive) | Command Pet | wrong | CONFIRMED | Command Pet is pet behavior control (confirmed in inventory), not any external/raid defensive — it is junk in a defensive bucket. Roar of Sacrifice, MM's only external DR, is instead parked on Combat 12. → **Move Roar of Sacrifice into Class 7 (Raid Defensive); drop Command Pet from a bound prime bucket.** |
| Interrupt | Muzzle | wrong | CONFIRMED | Muzzle is Survival's melee interrupt and is not in the MM inventory at all; the grounding explicitly names Counter Shot as MM's interrupt ('the class-tree Counter Shot node, NOT Survival's Muzzle'). The Interrupt bucket itself is correct, but the placed ability does not exist for this spec. → **Replace Muzzle with Coun … |
| Combat 5 | Black Arrow | gap | PLAUSIBLE | The baseline/Sentinel execute Kill Shot is unbound; only its Dark Ranger replacement Black Arrow is placed. These are mutually exclusive (Black Arrow replaces Kill Shot), so this is a build-coverage caveat, not a free-slot gap: Sentinel/baseline players need Kill Shot in this slot instead. → **For Sentinel/baseline bui … |
| Combat 10 | (empty) | gap | CONFIRMED | Explosive Shot is listed 'frequent' (~20s filler, procs Lock and Load → instant Aimed Shot) but is unbound, while empty Combat shift slots exist. It fits a Dark Ranger build (the seed's Black Arrow choice), so this is a genuine unbound frequent filler. → **Bind Explosive Shot to an open Combat shift slot.** |
| Combat 11 | (empty) | gap | PLAUSIBLE | Moonlight Chakram is 'frequent' and unbound with an open Combat slot. Caveat: it is Sentinel-hero-tree-only, which conflicts with the seed's Dark Ranger commitment (Black Arrow) — so it is a gap for a Sentinel layout, not the layout the seed actually implies. → **Bind Moonlight Chakram to an open Combat slot on Sentine … |
| Combat 12 | Roar of Sacrifice | weak | CONFIRMED | A reactive external defensive occupies a Combat (rotational) bucket while frequent rotational fillers go unbound. Roar belongs on the defensive layer; this pairs with the Command Pet finding as a single swap. → **Move Roar of Sacrifice to Class 7 (Raid Defensive) and free Combat 12 for a rotational filler (e.g. Explosi … |
| Taunt/Quick Access | Disengage | weak | PLAUSIBLE | Disengage (~20s CD core repositioning) sits in a Quick-Access bucket while the 3-min Aspect of the Cheetah holds the Movement Ability bucket — a plausible frequency inversion between two movement tools. Note the priority list marks BOTH 'situational,' and the exact key layers aren't in the grounding, so the magnitude i … |

*Affirmed as correct (6):* Combat 5=Black Arrow, Combat 3=Aimed Shot, Combat 4=Rapid Fire, Combat 8=Trueshot, Class 8 (Lust/BRes)=Harrier's Cry, Immune/Spell Immune/Movement=Aspect of the Turtle

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Explosive Shot** — A 'frequent' rotational filler (~20s CD, procs Lock and Load → instant Aimed Shot) is not bound anywhere. Combat 10 (S2) is empty and is the natural shift-layer home for it.
- **Moonlight Chakram** — Sentinel's frequent recastable mini-Trueshot (grants free Lock and Load) is unbound. Combat 11 (S3) is empty — ideal for a frequent-but-secondary rotational button on the shift layer.
- **Kill Shot** — The baseline/Sentinel execute is left unbound; only Black Arrow (its Dark Ranger replacement) is placed. Build-dependent, but Sentinel/baseline players need Kill Shot bound in the Combat 5 (Q) slot instead of Black Arrow.
- **Disengage** — Not truly missing but buried on a Ctrl slot (Taunt/Quick Access, CV); the core ~20s repositioning tool should occupy a fast movement key (Movement Ability 2 / SX is open).

---

## Hunter — Survival

KB confidence: **medium** · 18 verified findings (6 actionable, 12 affirmed) · 2 dropped in verify

> **Sourcing note / gaps:** Survival got a substantial Midnight rework, so several exact numbers are unconfirmed and flagged @verify-ingame: Kill Command exact Focus gen / charge behavior; Raptor Strike Focus cost (35 vs 40); Flamefang Pitch base CD (HackMD says 30s, method.gg says 60s — conflicting); Aspect of the Eagle duration/CD; Ancient Hysteria pet family; and the Method.gg curated import strings (page is JS-rendered — only the Tier-1 simc default string was captured). NAME RECONCILE: HackMD claims 'Tip of the Spear removed as active buff, now passive only' but the live Tier-1 simc APL heavily tracks buff.tip_of_th …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 7 (Raid Defensive) | Command Pet | wrong | CONFIRMED | Command Pet is pet-control (grounding: 'Pet management'), not a defensive — the Raid/External-Defensive bucket holds a non-defensive filler while the spec's actual external, Roar of Sacrifice, is buried in the Combat 12 damage bucket. → **Move Roar of Sacrifice into Class 7 (a reactive/ctrl key is the right tier for a  … |
| (unplaced) | Moonlight Chakram | gap | PLAUSIBLE | Sentinel hero-tree rotational button flagged 'frequent' in the priority (thrown inside Tip of the Spear windows) is assigned to no bucket at all. On Sentinel builds the player has no key for a frequently-pressed rotational ability. → **For Sentinel, claim a fast key (e.g. Combat 7 in place of the situational Hatchet To … |
| Combat 7 | Hatchet Toss | weak | PLAUSIBLE | A situational ranged filler occupies a prime unmodified key while Moonlight Chakram — flagged 'frequent' in the priority for Sentinel — is placed nowhere. For Sentinel builds the key is better spent on the frequent rotational button. Build-conditional: Hatchet is correct for Pack Leader (Hogstrider) builds. → **For Sen … |
| Combat 12 | Roar of Sacrifice | weak | CONFIRMED | The spec's real external defensive (grounding: 'Defensive (external)') sits in a damage-combat bucket while the semantically-correct Raid-Defensive bucket (Class 7) holds the non-defensive Command Pet — both a role and a tier mismatch. → **Swap with Class 7: Roar of Sacrifice -> Class 7, freeing Combat 12.** |
| Class 1 (Movement) | Tar Trap | weak | PLAUSIBLE | Tar Trap is a ground slow/CC (grounding: 'CC / Utility (slow)'), not a movement ability — miscategorized against the Movement bucket. The spec's only true movement (Aspect of the Cheetah) is in Movement Ability and Harpoon is in Combat 8, so no better occupant exists. → **Acceptable filler; treat as utility not movemen … |
| Class 6 (Dispel) | Flare | weak | PLAUSIBLE | Flare is stealth-detection / ground-effect clear (grounding: 'Utility (detect)'), not a dispel. Survival has no dispel in kit, so this bucket has no true occupant — it is placeholder filler, not a functional dispel. (True enemy-purge, Tranq Shot, is already correctly in Class 5.) → **Acceptable as unavoidable filler, b … |

*Affirmed as correct (12):* Combat 2=Kill Command, Combat 1=Raptor Strike, Combat 3=Wildfire Bomb, Interrupt=Muzzle, Class 5 (Purge)=Tranquilizing Shot, Class 8 (Lust/BRes)=Ancient Hysteria, Personal Defensive 1=Survival of the Fittest, Immune/Spell Immune/Movement=Aspect of the Turtle, CC=Intimidation, Combat 4=Takedown, Combat 5=Boomstick, Combat 6=Flamefang Pitch

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Moonlight Chakram** — Sentinel hero-tree rotational button flagged 'frequent' in the priority (thrown inside Tip of the Spear windows) but assigned to no bucket at all. Sentinel players have no key for a frequently-pressed rotational ability; it should claim a f …
- **Roar of Sacrifice** — Present in the seed but buried in Combat 12 (a damage bucket) rather than the Raid Defensive bucket, which instead holds the non-defensive Command Pet. Effectively missing from its correct home.

---

## Mage — Arcane

KB confidence: **high** · 2 verified findings (2 actionable, 0 affirmed) · 4 dropped in verify

> **Sourcing note / gaps:** method.gg /abilities and /rotation subpages 404'd (JS-rendered); used the /playstyle-and-rotation page + main guide + simc APL instead. Nether Precision confirmed REMOVED in Midnight (base Arcane Missiles buffed to compensate) — flagged @verify-ingame. Exact cooldowns/charges for Arcane Orb, Arcane Pulse, Touch of the Archmage, Presence of Mind, Supernova, and Alter Time carry small uncertainty (marked @verify-ingame in abilities.md). Spellslinger-vs-Sunfury usage/win-rate split not sourced from murlok/Archon — both presented as viable, so builds.md is medium confidence on the hero-tree recomm …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Res | Arcane Intellect | wrong | PLAUSIBLE | The Res slot holds Arcane Intellect, a raid Intellect buff, not a resurrection. Mage has no combat res (none in the inventory), so the slot has no true occupant and a must-maintain raid buff was parked in a semantically wrong home — a genuine category mismatch. → **Move Arcane Intellect to a dedicated Buff/utility slot … |
| Free / spare Combat slot | (unbound) | gap | CONFIRMED | Touch of the Archmage — a spec capstone active (row 11, frequency 'cooldown') tied to the Touch of the Magi burst window — is not assigned to any bucket in the seed. Confirmed absent: it is a real, bindable major cooldown left with no key, while all nine Combat slots are spent on rotational buttons and situational Evoc … |

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Touch of the Archmage** — Spec capstone active (row 11) tied to the burst window, frequency 'cooldown', but it is not assigned to any bucket in the seed. It should occupy one of the free Combat 10-12 shift slots (S2-S4) so it can be pressed inside the Touch of the M …
- **Arcane Explosion** — Situational 4+-target Sunfury filler (when not talented into Impetus) is left unbound. Minor, but a bindable rotational AoE with no home — could go in a spare Combat 10-12 slot for AoE-heavy content.

---

## Mage — Fire

KB confidence: **high** · 26 verified findings (5 actionable, 21 affirmed) · 1 dropped in verify

> **Sourcing note / gaps:** Seed-list correction: the seed listed "Prismatic Barrier" (that is Arcane's baseline barrier) — Fire's absorb is "Blazing Barrier" (confirmed in the existing talents.md class tree); authored as Blazing Barrier. Prior-expansion staples Phoenix Flames and Shifting Power are REMOVED in Midnight (method.gg), and Sun King's Blessing is folded into Pyroclasm — none authored as live buttons. "Fired Up" (talent 1257343 / buff 1257349): the existing talents.md marks the row-11 capstone ACTIVE, but every guide describes it as a passive apex proc — flagged @verify-ingame whether a pressable component exi …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Personal Defensive 1 | Prismatic Barrier | stale-name | CONFIRMED | Prismatic Barrier is ARCANE's baseline barrier. Fire's absorb shield is Blazing Barrier (grounding explicitly flags this). Wrong-spec ability in the primary personal defensive slot; Fire's actual mitigation is unbound. → **Replace with Blazing Barrier — Fire's actual damage-absorb defensive.** |
| Combat 12 | Arcane Explosion | weak | PLAUSIBLE | Arcane Explosion is off-spec/'rare' for Fire (Flamestrike is the AoE spender); it near-never gets cast, so it occupies a Combat slot vestigially. → **Acceptable as a low-priority filler, but Blazing Barrier (Fire's unbound defensive) or Frost Nova would be more useful here.** |
| Class 1 (Movement) | Mass Polymorph | weak | PLAUSIBLE | Bucket is labeled 'Movement' but holds Mass Polymorph, a 'rare' AoE CC choice node — a genuine role-label mismatch. → **Fire has no extra movement ability beyond Blink/Shimmer; leaving CC overflow here is fine, but the label doesn't match the pick.** |
| Class 7 (Raid Defensive) | Slow Fall | weak | PLAUSIBLE | Slow Fall is a fall utility, not a raid defensive; the role label is mismatched. Mage has no true raid-defensive cooldown, so the slot is inherently hard to fill. → **Consider Mass Invisibility as a closer 'raid defensive' proxy and move Slow Fall to a Free/Alt slot.** |
| Res | Arcane Intellect | weak | PLAUSIBLE | The 'Res' bucket holds Arcane Intellect (a raid Intellect buff), not a resurrection. Mage has no combat res, so the slot is repurposed, but the role label is a mismatch. → **Reasonable as a buff parking spot given no res exists; a dedicated 'Buff' slot would be the more honest home if one exists.** |

*Affirmed as correct (21):* Combat 1=Fireball, Combat 2=Fire Blast, Combat 3=Pyroblast, Combat 4=Scorch, Combat 5=Combustion, Combat 6=Flamestrike, Combat 7=Meteor, Class 2 (CC)=Cone of Cold, Class 3 (Tag)=Polymorph, Class 4 (Special)=Mass Invisibility, Self-Heal 1=Alter Time, Self-Heal 2=Mirror Image, Class 5 (Purge)=Spellsteal, Class 6 (Dispel)=Remove Curse …

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Blazing Barrier** — Fire's core damage-absorb defensive is entirely absent from the seed — the Personal Defensive 1 slot was filled with Arcane's Prismatic Barrier by mistake. This is the most important omission: Fire's actual pre-cast mitigation button is not …
- **Dragon's Breath** — The other half of the CC 2 choice node (frontal disorient + fire damage) — a common Fire pick for AoE CC and a Combustion setup. Only Supernova is represented; if the build runs Dragon's Breath it has no home.
- **Frostfire Bolt** — Not needed for the S1 Sunfury build (it's the Frostfire hero-tree filler replacing Fireball), so its absence is correct — noting only that it's intentionally omitted, not a gap.

---

## Mage — Frost

KB confidence: **high** · 22 verified findings (8 actionable, 14 affirmed) · 2 dropped in verify

> **Sourcing note / gaps:** Two source-level conflicts and several verify flags: (1) The Icy Veins ROTATION page summary said "Frostfire recommended for most content," but the Icy Veins BUILDS page and method.gg both say Spellslinger is the go-to for all content ("Frostfire is significantly behind"). Resolved in favor of Spellslinger (2 tier-3 sources + it is the meta pick); authored as Spellslinger-primary, Frostfire-alternative. (2) Icy Veins (spell 12472) as a pressed burst cooldown: the simc `cds` action list does NOT explicitly cast icy_veins, yet Thermal Void (which historically gates the Icy Veins window) is refer …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Combat 12 | Arcane Explosion | wrong | CONFIRMED | Grounding explicitly marks Arcane Explosion off-meta for Frost (Blizzard/Cone preferred), yet it occupies a combat slot while the high-priority ~30s burst Comet Storm — Frostfire's lead burst, frequency 'cooldown' — is unbound entirely. → **Replace with Comet Storm; drop Arcane Explosion or push it to Free/Alt.** |
| Class 7 (Raid Defensive) | Slow Fall | wrong | CONFIRMED | Slow Fall is a fall-speed utility (function 'Utility'), not any kind of defensive. A Raid Defensive slot should hold real mitigation. → **Put a genuine defensive here (Ice Barrier, or Greater Invisibility if not used elsewhere) and move Slow Fall to an Alt/utility bind.** |
| (unbound) — Combat/Shift cooldown slot | Icy Veins | gap | PLAUSIBLE | Icy Veins, the primary ~3min burst / Thermal Void cooldown, is not bound anywhere in the seed. Note the grounding flags @verify-ingame whether it is still a manual press vs auto in the Midnight build, so this is not fully certain. → **Bind Icy Veins to a Shift/Alt cooldown slot so the burst window can be triggered — pe … |
| (unbound) — Shift/Alt cooldown slot | Shifting Power | gap | PLAUSIBLE | Shifting Power, the M+ cooldown-cycling channel, has no bind. A core dungeon tool left off the bars. → **Give Shifting Power a Shift/Alt cooldown slot for M+ play.** |
| (unbound) — second personal-defensive slot | Ice Barrier | gap | PLAUSIBLE | Ice Barrier, the Frost damage-absorb barrier, is unbound. Prismatic Barrier is bound as a personal defensive, so this is a secondary defensive gap rather than a critical one. → **Bind Ice Barrier to a second personal-defensive slot so both barriers are reachable.** |
| Combat 5 | Ray of Frost | weak | CONFIRMED | Ray of Frost is a 60s banked channel (frequency 'cooldown') occupying a prime unmodified combat key, while the frequent spender Glacial Spike (frequency 'frequent', on CD / at 5 Icicles) is unbound anywhere in the seed. Real press-frequency mismatch. → **Bind Glacial Spike to this unmodified slot and demote Ray of Fros … |
| Class 1 (Movement) | Mass Polymorph | weak | PLAUSIBLE | A rare AoE-CC talent (function CC, frequency 'rare') parked in a Movement-labeled class slot — role mismatch, and a low-frequency ability on a fast Shift slot. → **Move Mass Polymorph to a rare-CC/Alt slot; use the movement slot for a movement enabler (Ice Floes if present in tree — needs verify).** |
| Class 2 (CC) | Cone of Cold | weak | PLAUSIBLE | Grounding classifies Cone of Cold as a Rotational-spender / AoE filler (with Cone of Frost), not a crowd-control tool; filing it under a CC slot mislabels its role and separates it from the other AoE buttons. (It does slow, so the mismatch is soft.) → **Treat Cone of Cold as an AoE filler on an open combat slot and res … |

*Affirmed as correct (14):* Combat 1=Frostbolt, Combat 2=Ice Lance, Combat 3=Flurry, Combat 4=Frozen Orb, Combat 6=Blizzard, Class 3 (Tag)=Polymorph, Class 8 (Lust/BRes)=Time Warp, Personal Defensive 1=Prismatic Barrier, Movement Ability=Blink, Interrupt=Counterspell, Immune/Spell Immune/Movement=Ice Block, CC=Frost Nova, Self-Heal 2=Mirror Image, Taunt/Quick Access=Greater Invisibility

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Comet Storm** — Major ~30s AoE burst, high priority for both Spellslinger and Frostfire trees, and Frostfire's lead burst. Completely unbound — should own the Combat 12 slot currently wasted on off-meta Arcane Explosion, or an open Combat 7/8.
- **Glacial Spike** — Frequent rotational spender (on CD / at 5 Icicles) — a core damage button left entirely unbound while a 60s Ray of Frost sits on the prime Q key. Needs a fast unmodified slot.
- **Icy Veins** — Primary ~3min burst/Thermal Void cooldown (verify manual-press status). Not bound anywhere; belongs on a Shift or Alt cooldown slot so the burst window can be triggered.
- **Shifting Power** — Core M+ cooldown-cycling channel with no bind. Should occupy a Shift/Alt cooldown slot for dungeon play.
- **Ice Barrier** — The Frost damage-absorb barrier — a primary personal defensive left unbound while Personal Defensive 2 (SZ) is empty.
- **Ice Floes** — Cast-while-moving enabler (verify presence in tree). Movement Ability 2 (SX) is unused and would be its natural home; important for a heavy-cast spec.

---

## Monk — Brewmaster

KB confidence: **medium** · 13 verified findings (7 actionable, 6 affirmed) · 2 dropped in verify

> **Sourcing note / gaps:** Tier-1 MID1 simc APL was available and is the rotation backbone (high confidence on priority ORDER). Lower-confidence items, all marked @verify-ingame in the files: (1) exact Brew charge counts, recharge times, and cooldowns for Purifying/Celestial/Black Ox/Fortifying/Niuzao/Touch of Death/Exploding Keg — approximated from guides, not pulled from the Blizzard spell API; (2) precise Bring Me Another apex mechanics (Empty Barrel proc %, Keg Smash cost reduction per rank, Refreshing Drink) — sourced only from method.gg/Icy Veins prose, numbers unconfirmed; (3) Energy costs for Tiger Palm/Keg Smas …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 7 (Raid Defensive) | Zen Flight | wrong | CONFIRMED | Zen Flight is an out-of-combat slow-fall/travel cantrip with zero defensive value (per grounding) — it does not belong in a raid-defensive bucket, while the spec's actual defensives Diffuse Magic (90s magic DR + reflect) and Zen Meditation (5min emergency DR) are unslotted entirely. → **Bind Diffuse Magic or Zen Medita … |
| Buff | Res | stale-name | CONFIRMED | 'Res' is not in the Brewmaster ability inventory — Monk (non-healer) has no unique combat/OOC resurrect and no self-buff to slot in a Buff bucket. This is a seed/template placeholder, not a real bind. → **Leave as Free, or move an under-slotted defensive/utility here; don't treat 'Res' as a Brewmaster bind.** |
| Personal Defensive 2 | — | gap | PLAUSIBLE | A second personal-defensive slot appears unassigned while two real defensives — Diffuse Magic and Zen Meditation — are slotted nowhere in the seed. (The exact bucket isn't in the provided slice, inferred from 'Personal Defensive 1', but the unslotted-defensives gap is confirmed.) → **Bind Diffuse Magic or Zen Meditatio … |
| Combat 7 | Spinning Crane Kick | weak | PLAUSIBLE | SCK is explicitly situational (AoE gather / Charred-Passions cleave, no mitigation, not on strict priority) yet sits on a prime fast Combat slot, while Chi Burst ('frequent') is on the shift layer. Real press-frequency vs key-tier mismatch, though exact key mapping isn't given. → **Acceptable if AoE-heavy; otherwise co … |
| Combat 8 | Rushing Jade Wind | weak | PLAUSIBLE | Situational maintenance buff (choice vs Special Delivery; refreshed on a timer, not spammed) on a prime fast Combat slot. Lower-value use of a fast key if RJW isn't the talented/maintained choice. → **Fine when RJW is talented and maintained; otherwise demote to a modifier layer.** |
| Combat 12 | Chi Burst | weak | PLAUSIBLE | Chi Burst is a real 'frequent' core-loop button in Master of Harmony but is parked on the shift layer; for a MoH main the modifier costs speed. For Shado-Pan it's low-priority filler and shift is fine — so this is build-dependent, not a clear error. → **Leave if MoH isn't the main build; if it is, move it one slot clos … |
| Self-Heal 4 (Emergency/Overflow) | Black Ox Brew | weak | PLAUSIBLE | Black Ox Brew is a ~2min off-GCD mitigation/energy reset cooldown (refills Purifying charges + Energy), not a self-heal — a role mismatch to a heal bucket. Softened by the 'Overflow' label and off-GCD (speed tier barely matters), which is why it's mild rather than wrong. → **Consider slotting a real defensive (Diffuse  … |

*Affirmed as correct (6):* Combat 3=Keg Smash, Combat 1=Tiger Palm, Combat 6=Purifying Brew, Interrupt=Spear Hand Strike, Taunt/Quick Access=Provoke, Personal Defensive 1=Fortifying Brew

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Diffuse Magic** — Real ~90s magic-damage panic button with a reflect — a core Brewmaster defensive, and it appears nowhere in the seed. The Class 7 Raid Defensive and Personal Defensive 2 buckets are the natural homes (one is misfilled with Zen Flight, the o …
- **Zen Meditation** — ~5min emergency channel with massive damage reduction — a genuine 'oh no' mitigation button, left unslotted. Belongs in a defensive bucket (Personal Defensive 2 or Class 7).
- **Empty the Cellar** — Grounding notes it 'appears as its own action in the APL' (Brew CDR value), but the seed gives it no bucket. Minor/optional — mostly passive-adjacent — but worth a slot if it's an active press in the current APL.

---

## Monk — Mistweaver

KB confidence: **medium** · 17 verified findings (8 actionable, 9 affirmed) · 1 dropped in verify

> **Sourcing note / gaps:** No Tier-1 SimulationCraft APL or talent string exists for Mistweaver — simc does not model healers, and the midnight branch ships only Brewmaster and Windwalker Monk profiles (confirmed via the profiles/MID1 listing). rotation.md and builds.md therefore rest on Tier-3 guides (method.gg 12.0.7 upd. 2026-06-16 + Icy Veins 12.0.7), confidence medium. Wowhead's rotation page (Swirl, 2026/05/28) is JS-rendered and returned only a nav shell — not usable for corroboration. Seed omitted Vivify (core heal, spell 116670) — added. 'Awakened Jadefire' surfaced in the Icy Veins DPS guide but did not match  …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 7 (Raid Defensive) | Zen Flight | wrong | CONFIRMED | Zen Flight is an out-of-combat levitate/travel channel (inventory: Movement, 'out of combat') — it does nothing as a raid defensive and can't be pressed in combat. The slot is dead weight. → **Bind Diffuse Magic here (MW's ~90s magic-damage defensive, currently unbound) or leave blank; move Zen Flight to a travel key i … |
| Combat 5 / Self-Heal (unbound) | Vivify | gap | CONFIRMED | CRITICAL omission: Vivify (spell 116670) — the core spot heal AND the Renewing Mist cleave payoff, rated 'frequent' — is bound to no bucket at all. The seed ships a Mistweaver sheet with no primary spot heal on it. → **Bind Vivify to a fast heal key (contend Q with Sheilun's Gift, or a free Self-Heal slot). Highest-pri … |
| Class 7 (Raid Defensive) / Personal Defensive | Diffuse Magic | gap | CONFIRMED | Diffuse Magic (~90s magic-damage-reduction defensive, in inventory as a talent) is unbound. Since Class 7 is currently wasted on Zen Flight, this is a clean swap into a real defensive. → **Bind Diffuse Magic into the Raid Defensive slot in place of Zen Flight.** |
| Self-Heal (empty) | Expel Harm | gap | PLAUSIBLE | Expel Harm (instant personal self-heal, ~15s, in inventory) is unbound. It is the exact ability the Self-Heal category exists for; the seed leaves that role empty. → **Bind Expel Harm to a free Self-Heal slot.** |
| Self-Heal 1 | Thunder Focus Tea | weak | PLAUSIBLE | Category mismatch: TFT is a 'frequent' ~30s off-GCD loop empower (feeds Renewing Mist/RSK/Enveloping/Vivify + Secret Infusion), not a self-heal. Parking it in a Self-Heal bucket a modifier away is the wrong mental slot, though off-GCD makes it survivable — as the reviewer concedes. → **Treat as a rotational empower; a  … |
| Class 5 (Purge) | Transcendence | weak | PLAUSIBLE | MW has no purge in the inventory, so the bucket has no true owner; Transcendence (spirit placement) is movement setup, not a purge. An acceptable park, but arbitrary pairing. → **Fine as a park; grouping it near Transcendence: Transfer keeps both halves of the mechanic together.** |
| Class 8 (Lust/BRes) | Summon Jade Serpent Statue | weak | PLAUSIBLE | MW has neither Bloodlust nor a battle rez, so this bucket has no true owner. The statue is a rare set-and-forget pet — a reasonable park, not a Lust/BRes. → **Fine to leave as a park; nothing better contends for the slot.** |
| Buff | Res | weak | PLAUSIBLE | 'Res' is loose shorthand for Resuscitate (an out-of-combat rez, per inventory), not a buff, and MW has no single-target raid buff to fill this bucket. Harmless park with a placeholder-ish name. → **Rename to Resuscitate for clarity. (Reviewer's 'move to the Res bucket (CX)' references a bucket not present in this seed  … |

*Affirmed as correct (9):* Combat 5=Sheilun's Gift, Combat 6=Renewing Mist, Combat 1=Tiger Palm, Combat 9=Invoke Chi-Ji, the Red Crane, Class 1 (Movement)=Transcendence: Transfer, Class 6 (Dispel)=Detox, Interrupt=Spear Hand Strike, Personal Defensive 1=Fortifying Brew, Class 3 (Tag)=Crackling Jade Lightning

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Vivify** — CRITICAL omission — Vivify (spell 116670) is the core spot heal AND the Renewing Mist cleave-heal payoff, rated 'frequent' in the priority list, yet it is bound to no bucket at all. The seed shipped a Mistweaver sheet with no primary heal o …
- **Diffuse Magic** — Reactive ~90s magic-damage defensive (talent) is unbound. Personal Defensive 2 (SZ) is free and is its natural home — and the Raid Defensive slot is currently wasted on Zen Flight, so this is a clean swap.
- **Expel Harm** — Instant personal self-heal (~15s) is unbound while two Self-Heal buckets (C2, C3) sit empty — the exact category it belongs to.
- **Invoke Yu'lon, the Jade Serpent** — Only the Chi-Ji side of the Celestial choice node is bound. Fine if speccing Chi-Ji, but if the raid build (Yu'lon) is chosen there is no bound button for it — worth a note since the two share the S1 slot by talent choice.

---

## Monk — Windwalker

KB confidence: **high** · 10 verified findings (10 actionable, 0 affirmed) · 4 dropped in verify

> **Sourcing note / gaps:** Rotation/abilities are high-confidence (Tier-1 simc APL fetched successfully with full action lists, corroborated by Method 12.0.7). Gaps/flags: (1) Exact cooldowns and resource costs for several abilities (Zenith ~90s, Celestial Conduit CD, Touch of Death CD, Strike of the Windlord Chi/CD, Tigereye Brew mechanics) are approximate — marked @verify-ingame in abilities.md. (2) Rushing Wind Kick and Zenith Stomp precise mechanics inferred from APL usage, not a tooltip — flagged. (3) builds.md is confidence:medium — Method import strings (Tier 3) captured for both hero trees + ST/M+, but NOT yet r …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 7 (Raid Defensive) | Zen Flight | wrong | CONFIRMED | Grounding lists Zen Flight as an out-of-combat slow-fall/travel spell — it provides zero mitigation, so it does not belong in a Raid Defensive slot. Meanwhile Diffuse Magic (magic mitigation, returns debuffs) and Dampen Harm (big-hit mitigation) are both unbound. → **Put Diffuse Magic in Class 7; drop Zen Flight to a F … |
| Buff | Res | stale-name | PLAUSIBLE | 'Res' is a literal placeholder string sitting in the Buff bucket, and Windwalker has no group/raid buff in the inventory. If it means Resuscitate, that is a rez, not a buff. The specific claim about a dedicated 'Res bucket (CX)' cannot be confirmed from the provided seed slice, but the placeholder-in-Buff mismatch is r … |
| (unbound — no slot) | Rushing Wind Kick | gap | CONFIRMED | Priority-list frequency is 'frequent' (talent strike woven high), yet it has no bucket. The strongest gap. Caveat: its desc carries a 'Mechanic to verify in-game' hedge, so certainty it is a discrete active button is imperfect. → **Bind to a freed fast key (e.g. the F slot Zenith holds, or an empty shift-combat slot).* … |
| (unbound — no slot) | Tigereye Brew | gap | CONFIRMED | Spec capstone burst cooldown (stacks from Chi spent, consumed for a crit window) — a real damage cooldown left entirely unbound while shift-combat slots sit empty. → **Bind to an open shift-combat slot alongside the other burst CDs.** |
| (unbound — no slot) | Diffuse Magic | gap | CONFIRMED | Windwalker's magic-damage mitigation (returns debuffs) is unbound; it is the natural occupant of the Class 7 Raid Defensive slot currently wasted on Zen Flight. → **Bind to Class 7 (Raid Defensive), replacing Zen Flight.** |
| (unbound — no slot) | Celestial Conduit | gap | PLAUSIBLE | Conduit-of-the-Celestials hero cooldown (channeled nuke pressed in the Zenith window). Unbound. Build-dependent — only needed on the Conduit hero tree — so not universal, but a missing damage CD for that build. → **Park on a free shift-combat slot if running the Conduit hero tree.** |
| (unbound — no slot) | Zenith Stomp | gap | PLAUSIBLE | Situational Chi dump used inside a Zenith window — a rotational damage button with no key. Lower priority (situational), but still an active with no home. → **Give it a shift-combat or overflow slot if talented.** |
| (unbound — no slot) | Dampen Harm | gap | PLAUSIBLE | Big-hit percent mitigation defensive is unbound; only Fortifying Brew and Touch of Karma received defensive slots. Talent-dependent (if picked), so conditional. → **Share the Ctrl/defensive layer if talented.** |
| (unbound — no slot) | Resuscitate | gap | PLAUSIBLE | The out-of-combat rez has no clean home; the seed used a literal 'Res' placeholder in the Buff bucket instead of binding Resuscitate to a rez slot. Overlaps with the Buff/'Res' stale-name finding. → **Bind Resuscitate to the intended rez/utility slot.** |
| Combat 8 | Zenith | weak | PLAUSIBLE | The load-bearing part is true and material: Rushing Wind Kick is listed 'frequent' in the priority yet has no bucket at all, while a ~90s major cooldown (Zenith) occupies a prime single-key slot. Whether Zenith specifically must yield the key is preference, but the unbound frequent rotational is a genuine gap. → **Give … |

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Rushing Wind Kick** — Priority-list frequency is 'frequent' (talent strike woven high in the rotation), yet it has no bucket at all. A frequent rotational button unbound is the biggest gap — two shift combat slots (Combat 10/S2, Combat 11/S3) are empty and Zenit …
- **Tigereye Brew** — Spec capstone burst cooldown (stacks from Chi spent, consumed for a crit window) — a real damage cooldown left entirely unbound. Belongs on an open shift slot (Combat 10/11) with the other burst CDs.
- **Celestial Conduit** — Conduit-of-the-Celestials hero cooldown, a channeled nuke pressed in the Zenith window when Heart of the Jade Serpent is down. Unbound; needed for the Conduit build (asserted S1 primary hero tree). Park on a free shift combat slot.
- **Diffuse Magic** — Windwalker's magic-damage mitigation (returns debuffs) is unbound. It is the natural occupant of the Class 7 Raid Defensive slot currently wasted on Zen Flight.
- **Zenith Stomp** — Situational Chi dump used inside a Zenith window — no bucket. Lower priority than the above but still a rotational spender with no key.
- **Dampen Harm** — Big-hit percent mitigation defensive (if talented) is unbound; only Fortifying Brew and Touch of Karma got defensive slots. Could share the Ctrl defensive layer.
- **Resuscitate** — The out-of-combat rez has no clean home — the seed put a literal 'Res' placeholder in the Buff bucket instead of assigning Resuscitate to the dedicated Res bucket (CX), which is left blank.
- **Slicing Winds** — Talent AoE dash / secondary gap-closer is unbound. Minor (situational movement), but worth a slot if talented since it doubles as a filler-spender.

---

## Paladin — Holy

KB confidence: **medium** · 17 verified findings (6 actionable, 11 affirmed) · 2 dropped in verify

> **Sourcing note / gaps:** Cheap re-run: all three target files already existed with patch 12.0.7 front-matter and were confirmed, not rewritten (no new web fetches this pass; sourcesUsed reflects the provenance recorded in those files from the prior authoring run). Standing gaps carried in the files: (1) No Tier-1 SimulationCraft APL exists for any healer spec (SimC does not model healer throughput), so the rotation priority is distilled from three agreeing Tier-3 guides — medium confidence, exact press-order between near-equal builders (Judgment vs Crusader Strike vs Hammer of Wrath) is not numerically pinned. (2) Whe …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Combat 8 | Holy Bulwark | wrong | CONFIRMED | Holy Bulwark is not independently castable — inventory lists its resource as '(via Holy Armaments)' and Holy Armaments alternates Sacred Weapon/Holy Bulwark each cast. The pressable button is Holy Armaments, and it is Lightsmith-only (not the default Herald build), so this fast key is dead on the recommended spec. → ** … |
| unbound (belongs on a Shift-Combat / cooldown slot) | Divine Toll | gap | CONFIRMED | Divine Toll is completely absent from the seed placements despite being the Herald's key ~1-min button (fires Holy Shock at up to 5 targets, big HP+healing burst, seeds Dawnlight) with priority note 'keep on cooldown'. The single most important omission. → **Bind Divine Toll on a Shift-Combat / cooldown slot; it should … |
| Combat 4 | Holy Light | weak | CONFIRMED | Holy Light is frequency 'situational' (slow mana top-up) yet occupies a prime unmodified fast key, while 'frequent' builders Hammer of Wrath and Crusader Strike are entirely unbound. → **Move Hammer of Wrath (frequent builder+damage) onto this fast slot and demote Holy Light to a modifier slot.** |
| Combat 7 | Word of Glory | weak | CONFIRMED | Grounding states Eternal Flame replaces Word of Glory and is the default Herald single-target spender ('frequent'); WoG is the non-Herald fallback. Seed binds only the fallback and Eternal Flame appears nowhere in the placements. → **Bind Eternal Flame on this fast key (it swaps onto the same button when talented Heral … |
| Class 2 (CC) | Blessing of Protection | weak | PLAUSIBLE | Inventory function for Blessing of Protection is 'Defensive' (external physical immunity), not crowd control; the bucket is explicitly labeled (CC) and the actual CC (stun/disorient) sit in the dedicated CC/CC2 slots. Real label mismatch (though it reads as intentional blessing-family grouping across Class 1-3). → **Tr … |
| Class 5 (Purge) | Turn Evil | weak | CONFIRMED | The inventory contains no purge/offensive-dispel ability for this spec; Turn Evil is a Fear CC (function 'CC'). It fills the Purge bucket but is not a purge. → **Leave the Purge bucket empty or relabel — no real purge exists for Holy Paladin; Turn Evil is CC filler at best.** |

*Affirmed as correct (11):* Combat 1=Holy Shock, Combat 5=Shield of the Righteous, Combat 6=Light of Dawn, Combat 9=Avenging Wrath, Class 1 (Movement)=Blessing of Freedom, Class 6 (Dispel)=Cleanse, Class 8 (Lust/BRes)=Intercession, Self-Heal 4 (Emergency/Overflow)=Lay on Hands, Immune/Spell Immune/Movement=Divine Shield, CC=Hammer of Justice, Taunt/Quick Access=Hand of Reckoning

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Divine Toll** — The single most important omission. It is the Herald's key ~1-min button (fires Holy Shock at up to 5 targets, huge HP+healing burst, seeds Dawnlight), flagged 'keep on cooldown' in the priority. Entirely unbound despite Combat 11/12 (S3/S4 …
- **Hammer of Wrath** — Listed 'frequent' — a recurring builder+damage button in execute range and during Avenging Wrath. Completely unbound; belongs on a fast unmodified key (e.g. reclaim Combat 4 from Holy Light).
- **Crusader Strike** — Listed 'frequent' when talented (Crusader's Might) — a melee builder that also shaves Holy Shock / Light of Dawn cooldowns. Unbound; needs a fast or Shift-Combat slot when speccing it.
- **Eternal Flame** — The default Herald single-target Holy-Power spender that REPLACES Word of Glory. The seed binds only WoG (the fallback), so on the recommended build the actual button pressed is unlabeled. Should own Combat 7 (R).
- **Holy Prism** — ~20s-cooldown spender/Dawnlight seed, priority 'on cooldown'. Unbound; a Shift-Combat slot (S3/S4) fits.
- **Tyr's Deliverance** — ~90s rolling group-HoT / heal-amp cooldown, priority 'roll on cooldown'. Unbound despite empty Shift and Ctrl slots.
- **Beacon of Virtue** — ~15s burst-AoE beacon spender when talented — pressed on a short cadence right after AoE ticks. Unbound; a Shift or fast slot is warranted when speccing it.
- **Barrier of Faith** — Situational pre-cast absorb + heal-empower on a known incoming hit. Unbound; fits an empty Ctrl/Class slot.
- **Avenging Crusader** — Choice-node alternative to Avenging Wrath. Not strictly missing (shares Combat 9 with AW as a choice node) but should be noted as the same-slot swap so the S1 binding covers whichever is talented.

---

## Paladin — Protection

KB confidence: **high** · 21 verified findings (7 actionable, 14 affirmed) · 2 dropped in verify

> **Sourcing note / gaps:** All three target files already existed at patch 12.0.7 with complete, well-sourced content, so nothing was re-authored (re-run guard). Extraction confidence is high; content confidence carries the files' own flags. Open items inherited from the existing files: (1) No distilled Tier-1 SimC APL for Protection — the MID1_Paladin_Protection.simc profile carries only the talent/gear loadout; the actual action priority lives in the SimC engine (class_modules/sc_paladin.cpp, apl_protection) and was NOT distilled, so the rotation ordering is guide-shaped (Tier 3, method.gg/Icy Veins) over the Tier-1 t …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Buff | Rite Of Sanctification | stale-name | CONFIRMED | Inventory canonical spelling is 'Rite of Sanctification' (lowercase 'of'); the seed writes 'Rite Of Sanctification'. Placement as the pre-pull Lightsmith raid buff is correct. → **Rename to 'Rite of Sanctification'.** |
| Combat 10-12 (unbound) | Avenging Wrath | gap | CONFIRMED | Avenging Wrath — the default major offensive CD ('Wings', +20% dmg/healing on a ~1-min cadence, converts Judgment to Hammer of Wrath) — is not bound anywhere. The seed bound only its choice-node sibling Sentinel; if AW is the talented pick it has no key. → **Bind Avenging Wrath into an open Combat slot, or make the Com … |
| Combat 10-12 (unbound) | Sacred Weapon | gap | CONFIRMED | Sacred Weapon — Lightsmith armament (weapon buff) that shares the Holy Armaments charge pool with the bound Holy Bulwark and must be refreshed when the buff wanes — is left out entirely despite being a real rotational-cadence button. → **Bind Sacred Weapon into an open Combat slot alongside Holy Bulwark.** |
| Combat 8 | Holy Bulwark | weak | PLAUSIBLE | Holy Bulwark is a charge-based Lightsmith absorb the priority list rates 'cooldown', not a constant rotational button, yet it occupies a fastest-tier unmodified key. Meanwhile its charge-pool partner Sacred Weapon and the major CD Avenging Wrath are bound nowhere. → **Consider moving Holy Bulwark to a shift Combat slot … |
| Combat 9 | Sentinel | weak | PLAUSIBLE | Sentinel and Avenging Wrath are the two halves of one choice node — only one is talented. The seed binds Sentinel only; if the player runs Avenging Wrath (the cadence the rotation is tuned around) this slot holds a talent they don't have. → **Treat this bucket as 'major burst CD (AW/Sentinel)' and bind whichever is act … |
| Class 2 (CC) | Blessing of Protection | weak | PLAUSIBLE | BoP is an external physical-immunity (with a threat drop), not CC. It fills a generically-labeled Class slot; the 'CC' label shouldn't be read literally. Real CC (Hammer of Justice / Blinding Light) is correctly in the dedicated CC buckets. → **Fine to keep on the shift-Class layer as part of the Blessing suite; recogn … |
| Class 5 (Purge) | Turn Evil | weak | CONFIRMED | Paladin has no purge; the inventory confirms Turn Evil is a fear vs Undead/Demon/Aberration. It fills the Purge slot as best-available filler, not an actual dispel/purge. → **Leave as-is (nothing better fits Purge for Prot); recognize it as a situational fear.** |

*Affirmed as correct (14):* Combat 5=Shield of the Righteous, Combat 2=Judgment, Combat 4=Consecration, Combat 3=Avenger's Shield, Combat 7=Word of Glory, Combat 6=Divine Toll, Self-Heal 4 (Emergency/Overflow)=Lay on Hands, Personal Defensive 1=Ardent Defender, Interrupt=Rebuke, Immune/Spell Immune/Movement=Divine Shield, Taunt/Quick Access=Hand of Reckoning, Class 6 (Dispel)=Cleanse Toxins, Class 8 (Lust/BRes)=Intercession, Stance 2=Devotion Aura

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Avenging Wrath** — The default major offensive CD ('Wings'), +20% dmg/healing on a ~1-min cadence the whole rotation is tuned around, and it converts Judgment to Hammer of Wrath. The seed bound only its choice-node sibling Sentinel; if AW is the talented pick …
- **Sacred Weapon** — Lightsmith armament (weapon buff, Holy dmg/healing) that shares the Holy Armaments charge pool with the bound Holy Bulwark and must be refreshed when the buff wanes — a real rotational-cadence button left out entirely. Bind it in an open Co …
- **Hammer of Light** — Templar top-priority spender for 12s after every Divine Toll. Not separately mapped, but it REPLACES Divine Toll on the same button, so it is effectively covered by Combat 6 (E) — noting so a reviewer doesn't add a redundant bind. Only a co …

---

## Paladin — Retribution

KB confidence: **medium** · 15 verified findings (7 actionable, 8 affirmed) · 1 dropped in verify

> **Sourcing note / gaps:** All three target files already existed with front-matter patch 12.0.7 (fetched/reviewed 2026-07-11), so per the cheap re-run guard they were confirmed, not rewritten; the inventory/priority above are extracted from their existing content. Flagged uncertainties already carry @verify-ingame markers in the files: (1) Templar Strike/Slash builder naming and shared-recharge behavior; (2) Execution Sentence exact detonation delay and cost; (3) Shield of Vengeance and Divine Protection cooldown/percent values; (4) Wake of Ashes and Divine Toll base cooldowns (talent-modified). Name reconciliation not …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Combat 1 | Crusader Strike | stale-name | CONFIRMED | The priority list leads with 'Templar Strike / Templar Slash' as the constant filler builder, and the grounding states Crusader Strike is the baseline that gets replaced by the Templar Strikes / Crusading Strikes choice node in the live 12.0.7 Templar build. So the fast key-1 filler is stale. → **Bind Templar Strike /  … |
| Personal Defensive 2 | Shield of Vengeance | gap | PLAUSIBLE | Shield of Vengeance (~1.5-2min absorb + holy reflect) is a real Ret defensive that is unbound. Note: the cited 'Personal Defensive 2' bucket does not appear in the provided seed slice (only 'Personal Defensive 1'), so the specific slot claim is unverified — but the underlying gap (a real defensive with no home) is genu … |
| Combat (unbound) | Hammer of Wrath | gap | CONFIRMED | Hammer of Wrath is a 'frequent'-tier builder (~7.5s; any-health during wings, else sub-20%) and has no binding anywhere in the seed. A core rotational button is homeless. → **Bind Hammer of Wrath to a fast or shift-Combat key.** |
| Combat (unbound) | Hammer of Light | gap | CONFIRMED | Hammer of Light is a 'frequent'-tier Templar spender and the top spend priority during the 20s Wake-of-Ashes window (fuels Shake the Heavens / Empyrean Hammer / Light's Deliverance). It is completely unbound — one of the two highest-damage buttons in the S1 Templar rotation. → **Bind Hammer of Light to a Combat / shift … |
| Combat 6 | Divine Toll | weak | CONFIRMED | Divine Toll is a ~60s cooldown occupying a prime unmodified key while two 'frequent'-tier rotational buttons (Hammer of Wrath ~7.5s, Hammer of Light — top spend priority in the WoA window) are unbound entirely. Real press-frequency misallocation. → **Keep Divine Toll here only after Hammer of Wrath and Hammer of Light  … |
| Class 2 (CC) | Blessing of Protection | weak | CONFIRMED | Blessing of Protection is an external defensive (physical immunity on an ally), not crowd control, yet it sits in the 'CC' bucket. Role/label mismatch. → **Workable as a home for an external, but note it is not CC.** |
| Class 5 (Purge) | Turn Evil | weak | CONFIRMED | Turn Evil is a situational fear (CC vs Undead/Demon/Aberration), not a purge; Retribution has no offensive purge. The slot's implied role does not match the ability. → **Acceptable as a niche-CC parking spot, but relabel expectations — this is a fear, not a dispel/purge.** |

*Affirmed as correct (8):* Combat 4=Final Verdict, Combat 5=Divine Storm, Combat 2=Judgment, Combat 3=Blade of Justice, Combat 9=Avenging Wrath, Interrupt=Rebuke, Personal Defensive 1=Divine Protection, Immune/Spell Immune/Movement=Divine Shield

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Hammer of Wrath** — 'Frequent' priority builder (~7.5s): usable sub-20% and on ANY-health target during wings (free/priority with Walk Into Light). A core rotational button that is omitted entirely — belongs on a fast or shift Combat key (S2/S3 are free).
- **Hammer of Light** — 'Frequent' Templar signature spender: replaces Wake of Ashes for 20s after WoA, a 5-HP nuke that is the TOP spend priority when available (fuels Shake the Heavens / Empyrean Hammer / Light's Deliverance). Completely unbound — one of the two …
- **Shield of Vengeance** — A real personal defensive (absorb + holy-damage reflect) with the Personal Defensive 2 (SZ) slot sitting empty — should be bound there.

---

## Priest — Discipline

KB confidence: **medium** · 22 verified findings (15 actionable, 7 affirmed) · 2 dropped in verify

> **Sourcing note / gaps:** No Tier-1 SimulationCraft APL or talent profile exists for Discipline — SimC ships only MID1_Priest_Shadow profiles (healers have no default action list), so rotation.md and builds.md rely on Tier-3 method.gg + Icy Veins consensus (they agree with each other) rather than a sim, and the damage priority is a soft ordering. method.gg /abilities and /rotation subpages 404; used /playstyle-and-rotation and /talents instead. Cast/CD/resource numbers in abilities.md are approximate (guides give few exact figures) — tuning-sensitive ones (Void Torrent CD, Pain Suppression % , Shadow Mend, Plea baselin …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 2 (CC) | Shadow Word: Death | wrong | CONFIRMED | Shadow Word: Death is a 'frequent' rotational execute/spender, not a CC — role-mismatched for the CC bucket and demoted off the fast-key tier it warrants. → **Move Shadow Word: Death to a fast unmodified Combat slot (swap with Plea on Combat 8).** |
| Class 7 (Raid Defensive) | Levitate | wrong | CONFIRMED | Levitate is a rare slow-fall movement utility, not a raid defensive — a role mismatch parking a 'rare' ability on the Raid-Defensive key, while the real raid defensive (Power Word: Barrier) sits in Combat 10. → **Put a genuine raid defensive (Power Word: Barrier) here; park Levitate on an overflow slot.** |
| Buff | Res | wrong | CONFIRMED | The Buff bucket holds 'Res' while the actual raid buff, Power Word: Fortitude, is in the Res bucket — the two are inverted. → **Put Power Word: Fortitude in the Buff bucket and Resurrection in the Res bucket.** |
| Res | Power Word: Fortitude | wrong | CONFIRMED | Res bucket holds the raid Stamina buff instead of Resurrection — the inverse of the Buff-bucket error. → **Place Resurrection here; move Power Word: Fortitude to the Buff bucket.** |
| (unbound) | Shadowfiend / Mindbender | gap | CONFIRMED | Major pet cooldown (Mindbender ~1min / Shadowfiend ~3min) — a build-agnostic core damage/mana cooldown pressed every window — is given no bind anywhere in the seed. → **Bind to a shift/Alt cooldown slot.** |
| (unbound) | Shadow Mend | gap | PLAUSIBLE | Reactive emergency spot-heal (Oracle proc) has no bind while the Self-Heal 2/3/4 overflow slots sit empty — an obvious home for it. → **Bind to an empty Self-Heal overflow slot.** |
| (unbound) | Premonition | gap | PLAUSIBLE | Oracle hero-talent active on ~60s CD (throughput/defensive) is unbound — an important button for the Oracle build the seed otherwise targets. → **Bind for Oracle builds on a cooldown slot.** |
| (unbound) | Void Torrent | gap | PLAUSIBLE | Voidweaver major channel cooldown driving the Entropic Rift window is unbound; needed for Voidweaver builds (does not override another button). → **Bind on a cooldown slot for Voidweaver builds.** |
| (unbound) | Ultimate Penitence | gap | PLAUSIBLE | 4-min offensive major cooldown is unbound. It is the choice-node alternative to Power Word: Barrier (which IS bound at Combat 10), so this only bites when running the Ult Penitence build. → **Bind on a cooldown slot if running Ultimate Penitence over Barrier.** |
| Combat 8 | Plea | weak | CONFIRMED | Plea is a 'situational' cheap Atonement top-up yet sits on a prime unmodified fastest-tier key, while the 'frequent' Shadow Word: Death (pressed on CD, feeds the pet) is buried on a shift key. A fast key is being spent on a low-frequency filler. → **Swap: put Shadow Word: Death on Combat 8 and move Plea to a shift/over … |
| Class 1 (Movement) | Holy Nova | weak | PLAUSIBLE | Holy Nova is situational PBAoE damage/Atonement, not a movement ability; the real movement button (Angelic Feather) is correctly elsewhere. Acceptable overflow use, role-label mismatch. → **Acceptable overflow park; note the label mismatch.** |
| Class 3 (Tag) | Mass Dispel | weak | PLAUSIBLE | Mass Dispel is an AoE magic dispel / immunity strip, not a tag ability; Disc has no dedicated tag button. Works as an overflow park but conceptually belongs with the dispels. → **Acceptable; could relocate to a utility slot and leave Tag free.** |
| Class 8 (Lust/BRes) | Mind Soothe | weak | PLAUSIBLE | Priest/Discipline has neither Bloodlust nor a battle-res, so this bucket has no real occupant; Mind Soothe just fills the slot. Harmless non-fit. → **Fine as a park; no true Lust/BRes exists for this spec.** |
| Slow | Mind Control | weak | PLAUSIBLE | Mind Control is an enemy-control CC, not a slow; Discipline has no true slow, so the bucket has no natural occupant. Harmless park but a role-label mismatch. → **Acceptable park; conceptually Mind Control belongs with CC. Leaving Slow free is also fine.** |
| Immune/Spell Immune/Movement | Leap of Faith | weak | PLAUSIBLE | Priest has no immunity; Leap of Faith is an ally save/reposition that fits the 'Movement' portion of this bucket. An acceptable park rather than a clean match. |

*Affirmed as correct (7):* Combat 5=Penance, Combat 7=Power Word: Shield, Combat 6=Power Word: Radiance, Combat 9=Evangelism, Class 4 (Special)=Power Infusion, Combat 1=Smite, Interrupt=

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Shadowfiend / Mindbender** — Major pet cooldown (Mindbender ~1min, Shadowfiend ~3min) — a core damage/mana cooldown pressed every window, yet the seed gives it no bind at all. Belongs on a shift/Alt cooldown slot.
- **Ultimate Penitence** — 4-min offensive major cooldown (big Atonement-healing burst, choice vs Power Word: Barrier) — completely unbound in the seed.
- **Premonition** — Oracle hero-talent active on ~60s CD (throughput/defensive) — a frequent, important button for the Oracle build with no bind.
- **Void Blast** — Voidweaver's constant filler while Entropic Rift is open (replaces Smite). For Voidweaver builds this is a spam button; the seed provides no explicit slot.
- **Void Torrent** — Voidweaver major channel cooldown driving the Entropic Rift window — unbound; needed for that build.
- **Shadow Mend** — Reactive emergency spot-heal (Oracle proc) has no bind, and all Self-Heal 2/3/4 overflow slots sit empty — an obvious home for it.
- **Master the Darkness** — Apex talent active empowering Atonement / upgrading to Void Shield — listed as an active cooldown but given no bind.

---

## Priest — Holy

KB confidence: **medium** · 20 verified findings (12 actionable, 8 affirmed) · 1 dropped in verify

> **Sourcing note / gaps:** No Tier-1 SimulationCraft APL exists for Holy Priest — the simc midnight branch profiles/MID1 directory ships only Shadow and Shadow_Archon for Priest, no MID1_Priest_Holy.simc. Rotation/priority is therefore distilled from Tier-3 guides (method.gg + Icy Veins), not a Tier-1 APL, and no numeric talent import strings were captured (no simc string; method.gg talents subpage 404'd and Wowhead is JS-nav-shell only). Exact cast times, cooldowns, Holy Word CD-reduction values, Halo/Apotheosis/Divine Hymn timers, Mastery: Echo of Light %, and the precise Benediction mechanic (empowered Flash Heal vs  …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 7 (Raid Defensive) | Levitate | wrong | CONFIRMED | Levitate is a slow-fall movement utility, not a raid defensive. Holy's raid-wide amp (Divine Hymn) is already on Combat 10; this is filler in the wrong bucket. → **Move Levitate to a rare-utility/Free slot; leave Raid Defensive empty (spec has no dedicated one).** |
| Slow | Mind Control | wrong | CONFIRMED | Mind Control is a channeled enemy-control CC, not a snare/slow. Holy Priest has no dedicated slow, so the Slow bucket has no valid occupant and Mind Control is a role mismatch here. → **Leave Slow empty/Free (spec has no snare); park Mind Control on a spare rare-utility slot if desired.** |
| Buff | Res | wrong | CONFIRMED | The Buff bucket holds the bare placeholder 'Res' instead of the raid buff Power Word: Fortitude. Buff and Res are inverted (PW:Fortitude is sitting in the Res bucket). → **Set Buff = Power Word: Fortitude.** |
| Res | Power Word: Fortitude | wrong | CONFIRMED | The Res bucket holds Power Word: Fortitude instead of Resurrection. Inverted with the Buff bucket, and the actual Resurrection ability is left unbound. → **Set Res = Resurrection.** |
| Combat 11 | Renew | gap | CONFIRMED | Renew is a 'frequent' instant HoT that feeds Holy Word: Sanctify's CD and Mastery: Echo of Light top-off, yet it is entirely unbound. Combat 11 (S3) is empty in the seed. → **Bind Renew to the empty Combat 11, or let it displace a situational park (SW:D/Mass Dispel) / even claim Combat 8 over the 40s Halo.** |
| Res | Resurrection | gap | CONFIRMED | The out-of-combat revive (Resurrection) is not bound as itself — it survives only as the bare 'Res' placeholder mislodged in the Buff bucket. Should occupy the Res bucket. → **Set Res = Resurrection (resolves alongside the Buff/Res swap).** |
| Combat 8 | Halo | weak | PLAUSIBLE | Halo is a ~40s cooldown occupying a prime unmodified key while the 'frequent' HoT Renew is left unbound. Defensible for Archon (pressed ~every 40s for Surge of Light), but a frequent builder has a stronger claim to a fast key. → **Consider F for Renew and move Halo to the empty Combat 11 (S3), or keep Halo but bind Ren … |
| Class 1 (Movement) | Holy Nova | weak | PLAUSIBLE | Holy Nova is an instant PBAoE heal/damage filler, not a movement ability — the real movement tool (Angelic Feather) is bound elsewhere. Reasonable park of an instant on a shift key, but the bucket label mismatches. |
| Class 2 (CC) | Shadow Word: Death | weak | PLAUSIBLE | SW:D is instant Shadow damage / execute, not CC; the actual CC (Psychic Scream, Shackle Horror) sits on the C/SC keys. Reasonable to keep SW:D on a quick shift key for damage, but the bucket label is a mismatch. |
| Class 8 (Lust/BRes) | Mind Soothe | weak | PLAUSIBLE | Priest has neither Bloodlust nor a Battle Res, so this bucket is dead for the spec; parking the skip-pull utility Mind Soothe on the otherwise-unused key is an acceptable repurpose. |
| Interrupt | Holy Word: Chastise | weak | PLAUSIBLE | Holy Priest has no true kick; Chastise interrupts only via its stun/incapacitate and doubles as a ~60s rotational DPS/CC button (Empyreal Blaze resets Holy Fire). It is the best available occupant but not a dedicated interrupt. → **Acceptable as-is; note it functions as pseudo-interrupt + DPS/CC, not a real kick.** |
| Immune/Spell Immune/Movement | Leap of Faith | weak | PLAUSIBLE | Leap of Faith is an ally-yank utility, not an immunity. Holy has no immunity to bind, so parking it against the 'Movement' half of this dead bucket is a fine repurpose. |

*Affirmed as correct (8):* Combat 4=Flash Heal, Combat 3=Prayer of Mending, Combat 5=Holy Word: Serenity, Self-Heal 1=Desperate Prayer, Personal Defensive 1=Fade, Combat 12=Guardian Spirit, Class 5 (Purge)=Dispel Magic, Class 6 (Dispel)=Purify

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Renew** — Frequent instant HoT that feeds Holy Word: Sanctify's cooldown and provides Mastery: Echo of Light top-off — a 'frequent' priority ability left entirely unbound. Combat 11 (S3) is empty, or it should displace a situational park (SW:D/Mass D …
- **Resurrection** — The actual revive is not bound as itself — it survives only as the bare placeholder 'Res' sitting in the wrong (Buff) bucket. Should occupy the Res bucket (CX).
- **Heal** — The slow mana-efficient single-target heal (also reduces Serenity CD) is unbound. Minor — many Holy priests keep it for downtime efficiency; could take a spare Combat/shift slot.

---

## Priest — Shadow

KB confidence: **medium** · 11 verified findings (4 actionable, 7 affirmed) · 7 dropped in verify

> **Sourcing note / gaps:** Tier-1 simc APL exists (Voidweaver default profile only) and drove rotation.md; no Archon simc profile published, so the Archon priority is from method.gg (Tier 3). Exact numbers — Shadow Word: Madness Insanity cost, generator Insanity values, and the Void Volley / Void Torrent / Voidform / Dispersion / Halo cooldowns — are Tier-3 approximations only and are marked @verify-ingame; the SpellName.csv (Tier 1) confirmed spell IDs/names (Shadow Word: Madness 335467 = renamed Devouring Plague, Tentacle Slam 1227280 = reworked Shadow Crash, Void Volley replaced Void Bolt, Shackle Horror 9484 = renam …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 7 (Raid Defensive) | Levitate | wrong | PLAUSIBLE | Seed matches. Levitate is definitionally a slow-fall/water-walk travel utility (per grounding), not a defensive. A Raid Defensive slot is the one dead-role slot (Shadow has no raid-wide defensive) where a reflexive press during a damage spike is an actual trap — pressing it yields zero mitigation. → **Leave empty or pa … |
| Buff | Res | wrong | CONFIRMED | Seed has 'Buff':'Res' and 'Res':'Power Word: Fortitude' — the two are swapped. Resurrection (a battle/out-of-combat res) sits in the Buff bucket while the raid Stamina BUFF sits in the Res bucket. → **Swap them: Power Word: Fortitude -> Buff, Resurrection -> Res.** |
| Res | Power Word: Fortitude | wrong | CONFIRMED | Inverse of the Buff-bucket error: the raid Stamina buff (Power Word: Fortitude) occupies the Res slot. Resurrection belongs here. → **Move Resurrection to Res and Power Word: Fortitude to Buff.** |
| Combat 10 | Free | gap | CONFIRMED | Void Volley (replaced Void Bolt) is in the inventory with priority 'frequent' and is explicitly high-priority to avoid losing charges, yet it appears in zero seed values — it is completely unbound. This is the most impactful omission. → **Bind Void Volley to an empty shift-layer slot (e.g. Combat 10 / the 'Free' slot); … |

*Affirmed as correct (7):* Combat 5=Shadow Word: Madness, Combat 1=Mind Flay, Interrupt=Silence, Combat 2=Mind Blast, Combat 8=Void Torrent/Halo, Class 4 (Special)=Power Infusion, Combat 9=Voidform

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Void Volley** — Frequent short-CD Insanity generator (replaced Void Bolt), HIGH priority to not lose charges — completely unbound in the seed despite three empty shift slots (Combat 10-12). This is the most impactful omission.
- **Resurrection** — Present only as the label 'Res' mislocated in the Buff bucket; needs to actually live in the Res slot after un-swapping with Power Word: Fortitude.
- **Shadowform** — The DPS stance kept up at all times (precombat recast if dropped). Not bound anywhere; Stance slots F1-F4 are all empty and are its natural home.

---

## Rogue — Assassination

KB confidence: **high** · 23 verified findings (10 actionable, 13 affirmed) · 1 dropped in verify

> **Sourcing note / gaps:** Hero-tree meta is a genuine split, not settled: the simc default profile (Tier 1) is built around Deathstalker and sims ahead, while Method (Tier 3) recommends Fatebound for far better QoL. Both trees are documented; which leads on live 12.0.7 logs is flagged @verify-ingame. Midnight reworks (baseline Shiv removed / returns via Toxic Stiletto; Crimson Tempest reworked into a bleed-spreading generator; Master Assassin stealth effects removed) are sourced from Method's intro but exact reworked behaviour is @verify-ingame. Exact ability energy costs / cooldowns are approximate baseline values (ta …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Combat 8 | Ambush | gap | CONFIRMED | Ambush is absent from the seed entirely, yet it is a builder used from Stealth/Vanish openers and on Blindside procs (higher damage than Mutilate). Combat 8 is unassigned and is its natural fast-key home. → **Bind Ambush to the open Combat 8 slot.** |
| Combat shift/Alt slot | Slice and Dice | gap | PLAUSIBLE | Omitted from the seed. Minor (mostly a precombat pre-cast) but a real finisher/self-buff some builds refresh mid-fight; it should have a low-priority home rather than being absent. → **Bind to a low-priority shift/Alt slot.** |
| Combat shift slot | Mark for Death | gap | PLAUSIBLE | Omitted. In Deathstalker it is the target-swap mark-mover (reset CP + relocate Deathstalker's Mark before a Darkest Night proc). Situational and build-conditional, but real if running Deathstalker. → **If running Deathstalker, bind to a shift/Combat slot; skippable otherwise.** |
| Class 1 (Movement) | Sap | weak | CONFIRMED | Sap is a stealth incapacitate (CC), not a movement ability — a role mismatch. Harmless as filler since it's rarely pressed and rogue movement (Sprint/Shadowstep/Vanish) is already placed elsewhere. → **Acceptable filler; no better rogue candidate competes for this slot.** |
| Self-Heal 2 | Thistle Tea | weak | PLAUSIBLE | Thistle Tea is an energy/Mastery sustain cooldown pressed inside the Kingsbane/Deathmark burst window, not a heal; parking it in a self-heal slot is a role mismatch. Grounding notes it auto-procs/near-auto in S1, which softens the access concern but not the label mismatch. → **Move to an open Combat shift slot so it's  … |
| Class 6 (Dispel) | Distract | weak | CONFIRMED | Distract is pull manipulation, not a dispel. Rogues have no true dispel (Cloak self-dispels only), so the bucket has no correct occupant. → **Fine as filler; no rogue ability truly fits Dispel.** |
| Class 7 (Raid Defensive) | Tricks of the Trade | weak | CONFIRMED | Tricks is a threat/damage redirect, not a raid defensive. Assassination has no raid-wide defensive, so this is unavoidable filler. → **Acceptable filler; no better rogue candidate exists.** |
| Class 8 (Lust/BRes) | Shroud of Concealment | weak | CONFIRMED | Shroud is a group-stealth skip tool, not Lust or Battle-Res; rogues provide neither, so the mismatch is unavoidable. → **Fine as filler placement.** |
| Slow | Gouge | weak | CONFIRMED | Gouge is an incapacitate (breaks on damage), not a slow. Rogue slows come from passive weapon poisons, so there is no active slow button; Gouge is a role-mismatched stand-in. → **Acceptable given no dedicated slow ability; treat it as a second short-CC key.** |
| Res | Poisons | weak | CONFIRMED | 'Poisons (apply)' is a once-an-hour precombat weapon buff, not a resurrect. Rogues have no combat res, so the bucket has no correct occupant. → **Fine as filler; could equally sit on an Alt/consumable-tier key since it's rarely pressed.** |

*Affirmed as correct (13):* Combat 1=Mutilate, Combat 4=Envenom, Combat 2=Garrote, Combat 3=Rupture, Combat 5=Kingsbane, Combat 6=Fan of Knives, Combat 7=Crimson Tempest, Combat 9=Deathmark, Class 4 (Special)=Vanish, Self-Heal 4 (Emergency/Overflow)=Cloak of Shadows, Immune/Spell Immune/Movement=Shadowstep, Interrupt=Kick, CC=Kidney Shot

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Ambush** — Left out of the seed entirely, yet it is a rotational builder (used from Stealth/Vanish openers and on every Blindside proc — frequent, not rare). Combat 8 (F) is unassigned in the seed and is the natural fast-key home for it.
- **Slice and Dice** — Omitted. Minor (mostly a precombat pre-cast) but a real finisher button that some builds refresh mid-fight; belongs on a low-priority Alt/shift slot rather than being absent.
- **Mark for Death** — Omitted. In Deathstalker it's the target-swap mark-mover (reset CP + relocate Deathstalker's Mark before a Darkest Night proc). Situational but real; if running Deathstalker it should occupy a shift/Combat slot.

---

## Rogue — Outlaw

KB confidence: **high** · 6 verified findings (2 actionable, 4 affirmed) · 7 dropped in verify

> **Sourcing note / gaps:** Rotation/build structure is high-confidence (Tier-1 simc APL + two corroborating Tier-3 guides all 12.0.7/2026-06-16). Flagged uncertainties: (1) Exact energy costs and several cooldowns are approximate — the Tier-3 summarizers gave conflicting numbers (e.g. Sinister Strike cited as 35 vs historical 45 energy) and Restless Blades/haste shorten cooldowns dynamically; marked @verify-ingame. (2) Whether Killing Spree now consumes combo points (APL/method.gg treat it as a high-CP finisher, a Midnight change from a standalone channel) — @verify-ingame. (3) Roll the Bones staged 1-4 rework details a …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| (unbound) | Slice and Dice | gap | PLAUSIBLE | Slice and Dice — the self-haste buff maintained/refreshed in Improved Adrenaline Rush builds (priority frequency 'cooldown') — is not bound to any bucket in the seed. Build-dependent, but in that common build it is a real maintenance spender with no key. → **Bind Slice and Dice to an open Combat/overflow slot for Impro … |
| Combat 8 | Killing Spree | weak | CONFIRMED | Killing Spree (~60s-CD burst, priority frequency 'cooldown') occupies the last fast key while Ambush — inventoried as a rotational builder and flagged 'frequent' / 'constant' in Hidden Opportunity builds — is bound to NO bucket anywhere in the seed. On press-frequency grounds a proc-driven builder outranks a 60s cooldo … |

*Affirmed as correct (4):* Combat 1=Sinister Strike, Combat 4=Dispatch, Self-Heal 4 (Emergency/Overflow)=Cloak of Shadows, Personal Defensive 1=Evasion

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Ambush** — A rotational builder — the guaranteed stealth/Vanish opener and, in Hidden Opportunity/Audacity builds, a CONSTANT proc-driven builder (priority list flags it 'frequent', 'constant there'). The seed binds it to no bucket at all, despite Com …
- **Slice and Dice** — The self-haste buff maintained in Improved Adrenaline Rush builds ('cooldown' frequency, refreshed periodically). Not bound anywhere; a build-dependent but real maintenance spender that needs a key — the unused Combat 12 (S4) slot is the na …
- **Coup de Grace** — Trickster capstone woven into builder and finisher windows ('frequent') — unbound. It may fire as an automatic empowerment rather than a manual press in the current implementation, so lower priority than Ambush/SnD, but if it requires a key …

---

## Rogue — Subtlety

KB confidence: **medium** · 16 verified findings (9 actionable, 7 affirmed) · 1 dropped in verify

> **Sourcing note / gaps:** Exact cast/CD/cost numbers for several abilities are unverified and flagged @verify-ingame — Blizzard spell API not queried this pass. Specifics: Shadow Dance recharge (Icy Veins claims 20s/charge vs the long-standing 60s — big discrepancy, left as 'recharge, 2 charges'); Goremaw's Bite CD/cost; Secret Technique CD; Sprint and Grappling Hook CDs and Grappling Hook spec access. Notable Midnight change flagged for downstream review: the Tier-1 S1 simc APL casts NO Rupture and NO Symbols of Death, and Slice and Dice appears only as a maintained buff (read via buff.slice_and_dice.up), not an activ …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 6 (Dispel) | Distract | wrong | CONFIRMED | Inventory defines Distract as a pull/pathing tool (draws mob attention) — it does not dispel anything. The Dispel bucket is filled by a non-dispel. Rogue's only dispel-adjacent effects are Cloak of Shadows (self magic-dispel) and Shiv (enrage dispel). → **Leave the bucket empty (Sub has no friendly dispel) and move Dis … |
| Class 7 (Raid Defensive) | Tricks of the Trade | wrong | CONFIRMED | Inventory defines Tricks of the Trade as a threat-redirect utility — it mitigates no damage, so it is not a raid defensive. Sub has no true raid-wide defensive; Feint (personal AoE mitigation) is closest and already on Personal Defensive 2. → **Treat this as an empty/filler bucket and put Tricks in a plain utility slot … |
| Combat 1 | Backstab | stale-name | CONFIRMED | Seed places Backstab on Combat 1. Inventory states Backstab is REPLACED by Gloomblade when talented (a common Sub build), so the label is wrong on a Gloomblade build. The slot/role is right; only the name is build-dependent. → **Bind key 1 to Gloomblade when talented (same constant single-target builder, no positional  … |
| Combat 10-12 (unbound) | Coup de Grace | gap | CONFIRMED | Coup de Grace is in the inventory at 'frequent' and prioritized OVER Eviscerate when up, yet is bound to no bucket. On a Trickster build it is a core spammed finisher needing a fastest-tier Combat slot. → **Bind Coup de Grace to a free fast Combat slot (10-12), or share/replace Eviscerate's key 4 on Trickster builds.** |
| Combat 1 (unbound alt) | Gloomblade | gap | CONFIRMED | Gloomblade, the talent replacement for Backstab (constant single-target builder), is unbound; the seed only placed Backstab. On a Gloomblade build key 1 must point at Gloomblade instead. → **Ensure key 1 resolves to Gloomblade when talented (see the Combat 1 stale-name finding); this is the same slot, not an additional … |
| Movement (unbound) | Grappling Hook | gap | PLAUSIBLE | Grappling Hook, a baseline Rogue mobility tool in the inventory, is bound to no bucket. Genuinely useful in M+/PvP, though situational and its spec access is marked unverified. → **Bind Grappling Hook to a free movement/utility slot if the spec has access; low priority. Verify spec access before committing the slot.** |
| Class 8 (Lust/BRes) | Shroud of Concealment | weak | CONFIRMED | Rogue has neither Bloodlust nor a battle-res, so this bucket has no legitimate occupant. Shroud (rare group-stealth skip tool) is defensible filler — just not a lust or brez. → **Acceptable filler; no action needed beyond knowing this key provides no lust/brez.** |
| Slow | Gouge | weak | CONFIRMED | Inventory defines Gouge as a frontal incapacitate that breaks on damage — not a slow. Sub has no active slow keybind (Crippling/Numbing are passive poisons), so the Slow bucket has no real occupant; Gouge is filler better read as CC. → **Acceptable as filler given no active slow exists, but note it fires an incap, not  … |
| Res | Poisons | weak | CONFIRMED | Rogue has no resurrect; Poisons is a pre-combat prep action, not a res. Harmless as filler in a low-priority slot, and Poisons needs no fast key. → **Acceptable filler; consider a Poisons re-apply macro so the key is at least functional out of combat.** |

*Affirmed as correct (7):* Combat 2=Shadowstrike, Combat 3=Secret Technique, Combat 4=Eviscerate, Combat 5=Shadow Dance, Combat 9=Shadow Blades, Self-Heal 4 (Emergency/Overflow)=Cloak of Shadows, Class 4 (Special)=Vanish

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Coup de Grace** — Trickster capstone finisher, listed at 'frequent' and prioritized OVER Eviscerate when up, is not bound to any bucket. On a Trickster build it is a core spammed finisher and needs a fastest-tier Combat slot. Combat 10-12 (S2-S4) are free, o …
- **Gloomblade** — Talent replacement for Backstab (constant single-target builder) is unbound; the seed only placed Backstab on Combat 1. If Gloomblade is talented — common for Sub — key 1 must point at it instead.
- **Grappling Hook** — Baseline Rogue mobility is unbound while Movement Ability 2 (SX) sits empty. Situational but genuinely useful in M+/PvP; the free shift-layer movement slot is the natural home (competing with Shadowstep for it).

---

## Shaman — Elemental

KB confidence: **high** · 25 verified findings (10 actionable, 15 affirmed) · 0 dropped in verify

> **Sourcing note / gaps:** Name canonicalization all clean — every seed ability confirmed in SpellName.csv; Midnight-new/renamed rotational abilities added and verified: Tempest (454009, Stormbringer hero passive that grants a castable nuke), Voltaic Blaze (470057, spec active), Ancestral Swiftness (443454, Farseer active that replaces Nature's Swiftness), Skyfury (462854, the group raid buff). Primordial Wave (326059) exists as a spell but is NOT in the Midnight 12.0.7 Elemental talent tree (absent from talents.md and the simc APL) — deliberately omitted. Flagged / lower-confidence items: (1) exact Maelstrom generation …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Buff | Ancestral Spirit | wrong | CONFIRMED | Ancestral Spirit is the combat resurrection, not a buff. It is swapped with the Res bucket, which holds the actual raid buff (Skyfury). → **Put Skyfury in Buff and Ancestral Spirit in Res — the two are swapped.** |
| Res | Skyfury | wrong | CONFIRMED | Skyfury is the group raid buff (pre-pull attack/spell power), not a resurrection. The actual battle rez (Ancestral Spirit) is parked in Buff — the two buckets are swapped. → **Swap: Ancestral Spirit -> Res, Skyfury -> Buff.** |
| Combat 10/11 (open) | Tempest | gap | CONFIRMED | Frequent Stormbringer proc-spender (charges from spending Maelstrom, supercharges the next Bolt/CL, applies Lightning Rod) is completely unbound. A 'frequent'-tier rotational button with no key. → **Bind Tempest to a fast Combat/shift key (open Combat 10/11), or have it displace the situational Nature's Swiftness on th … |
| Combat 10/11 (open) | Fire Elemental (or Storm Elemental) | gap | CONFIRMED | ~2.5min burst-pet DPS cooldown, alongside Stormkeeper/Ascendance, is unbound entirely. → **Bind Fire Elemental (or Storm Elemental) to an open shift slot (Combat 10/11).** |
| Combat 5 / spender slot | Elemental Blast | gap | CONFIRMED | Primary ST Maelstrom spender ('usually the pick' of the Earth Shock choice node) is unbound; only the alternative Earth Shock was placed, so the common build has no spender key. → **Bind Elemental Blast in the Combat 5 spender slot for the usual build (or an open Combat slot to cover both choice options).** |
| Combat 8 / cooldown slot | Ancestral Swiftness | gap | PLAUSIBLE | Farseer DPS cooldown (~1.5min, instant + haste + summons an ancestor) is unbound; the seed bound the mutually-exclusive Nature's Swiftness instead, leaving Farseer builds without this button. → **For Farseer, bind Ancestral Swiftness to the fast/shift key currently holding Nature's Swiftness.** |
| AoE spender slot (open) | Voltaic Blaze | gap | PLAUSIBLE | Frequent AoE Flame Shock spreader (core in Farseer/M+ when talented) is unbound — a 'frequent'-tier rotational button with no key at all. → **Bind Voltaic Blaze to a fast Combat/shift key in builds that talent it.** |
| Combat 5 | Earth Shock | weak | CONFIRMED | Earth Shock is the losing half of a choice node; grounding says Elemental Blast is 'usually the pick' as the primary ST spender, and Elemental Blast is bound nowhere. The common build ends up with no spender key. → **Bind whichever spender is talented here (Elemental Blast for the usual build), or add Elemental Blast t … |
| Combat 8 | Nature's Swiftness | weak | CONFIRMED | Prime unmodified key spent on a situational utility. Nature's Swiftness is replaced by Ancestral Swiftness in Farseer (mutually exclusive), so the key is dead in that build, while the frequent proc-spender Tempest is unbound entirely. Press-frequency mismatch on a top-tier key. → **Give this key to a frequent rotationa … |
| Class 7 (Raid Defensive) | Totemic Projection | weak | PLAUSIBLE | Totemic Projection is a rare totem-repositioning utility, not a raid defensive. Elemental has no true raid-wide external, so this is filler occupying the slot rather than a real match. → **Acceptable as a placeholder; consider a group-value totem (Wind Rush / Healing Stream) if a defensive-flavored button is wanted, an … |

*Affirmed as correct (15):* Combat 1=Lightning Bolt, Combat 2=Lava Burst, Combat 3=Flame Shock, Combat 4=Chain Lightning, Combat 6=Earthquake, Combat 7=Stormkeeper, Combat 9=Ascendance, Combat 12=Frost Shock, Class 4 (Special)=Spiritwalker's Grace, Class 8 (Lust/BRes)=Heroism, Interrupt=Wind Shear, Personal Defensive 1=Astral Shift, Personal Defensive 2=Earth Elemental, CC 2=Thunderstorm …

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Tempest** — Frequent Stormbringer rotational proc-spender (charges from spending Maelstrom, supercharges the next Bolt/CL) — it is completely unbound. A 'frequent'-tier button belongs on a fast Combat key; open slots Combat 10/11 (S2/S3) exist, or it s …
- **Fire Elemental (or Storm Elemental)** — ~2.5min burst-pet cooldown, a core DPS CD alongside Stormkeeper/Ascendance — unbound entirely. Should take an open shift slot (Combat 10/11 = S2/S3).
- **Ancestral Swiftness** — Farseer DPS cooldown (~1.5min, instant + haste + summons an ancestor) — unbound; the seed bound the mutually-exclusive Nature's Swiftness instead. Farseer builds want this on a fast/shift key, not the class-talent alternative.
- **Elemental Blast** — Primary ST Maelstrom spender ('usually the pick' of the Earth Shock choice node) — unbound. The common build has no spender key because only Earth Shock was placed.
- **Voltaic Blaze** — Frequent AoE Flame Shock spreader (core in Farseer/M+) — unbound. A 'frequent'-tier rotational button with no key at all.

---

## Shaman — Enhancement

KB confidence: **high** · 21 verified findings (11 actionable, 10 affirmed) · 3 dropped in verify

> **Sourcing note / gaps:** All 32 seed ability names canonicalize cleanly against raw/wago/SpellName.csv (12.0.7) — no renames. Added talent-granted actives present in the tier-1 APL that were not in the seed list: Voltaic Blaze (470057, Midnight-relevant Flame Shock refresh), Tempest (Stormbringer spender), Primordial Storm (Totemic spender), Ascendance/Windstrike, Elemental Blast, Windfury/Flametongue Weapon imbues, Lightning Shield. Exact cast/CD numbers could NOT be sourced for several abilities (Wowhead overview page returned only a nav shell) and are flagged @verify-ingame in abilities.md: Stormstrike charges/rech …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Buff | Ancestral Spirit | wrong | CONFIRMED | Ancestral Spirit is the out-of-combat resurrection, NOT a buff — mis-slotted in the Buff bucket. Mirror of the Skyfury error. → **Swap: Ancestral Spirit -> Res bucket, Skyfury -> Buff bucket.** |
| Res | Skyfury | wrong | CONFIRMED | Skyfury is the Shaman group buff (Mastery / melee-ranged bonus, function 'Utility (group buff)'), NOT a resurrection — mis-slotted in the Res bucket. It is swapped with Ancestral Spirit. → **Swap: Skyfury -> Buff bucket, Ancestral Spirit -> Res bucket.** |
| (missing binding) | Voltaic Blaze (unbound) | gap | CONFIRMED | Voltaic Blaze (spell 470057) is a 'frequent' builder / Flame Shock refresher — the ability that actually maintains the Flame Shock parked on prime key 3 — yet it has no binding anywhere in the seed. → **Bind Voltaic Blaze to a fast/frequent slot (Combat 10 is unassigned).** |
| (missing binding) | Tempest (unbound) | gap | CONFIRMED | Tempest is the 'frequent' Stormbringer hero-tree spender (massive nuke at 10 stacks) and is unbound. In the Stormbringer build it is a core spender with no key while 40-60s CDs occupy prime slots. → **Give Tempest a fast or shift spender key in the Stormbringer build.** |
| (missing binding) | Primordial Storm (unbound) | gap | CONFIRMED | Primordial Storm is the 'frequent' Totemic hero-tree spender (replaces the lightning nuke in the Totemic loop) and is unbound — central to the Totemic build with no key. → **Bind Primordial Storm to a spender key in the Totemic build.** |
| (missing binding) | Ascendance (unbound) | gap | PLAUSIBLE | Ascendance is a ~2-min major burst CD that REPLACES Doom Winds and enables Windstrike/Thorim's Invocation in that build, yet is entirely unbound. Build-conditional (Ascendance/DRE build). → **For Ascendance builds, bind it at Combat 9 (in place of Doom Winds) or the empty Combat 10.** |
| (missing binding) | Windfury / Flametongue / Lightning Shield (unbound) | gap | PLAUSIBLE | The maintained weapon imbues and self-buff have no binding in the shown seed. They are low mid-combat priority but must be re-applicable on expiry. Caveat: the seed slice shows no Alt layer, so these may live on an unshown layer. → **Place on an Alt/precombat layer or a Free slot for re-application.** |
| Combat 3 | Flame Shock | weak | CONFIRMED | Flame Shock is 'frequent' DoT upkeep, hard-cast only as filler and 'mostly kept up via Voltaic Blaze' per its own note — yet it holds a prime unmodified combat key while its actual refresher (Voltaic Blaze) and the frequent hero-tree spenders are unbound. A filler on a prime slot is a real cost. → **Bind Voltaic Blaze  … |
| Combat 5 | Sundering | weak | CONFIRMED | Sundering is a ~40s-CD burst button (priority frequency 'cooldown') on a prime fast combat key, while 'frequent' spenders Tempest / Primordial Storm are entirely unbound. A 40s CD is a low-value occupant of an unmodified slot. → **Relocate Sundering to a shift-layer cooldown slot (Combat 10 is free) and give the fast k … |
| Combat 11 | Nature's Swiftness | weak | PLAUSIBLE | Nature's Swiftness is a 'reactive' emergency heal-enabler sitting on a shift-combat slot intended for proactive cooldowns — a genuine role/tier mismatch, though low-impact. → **Move to a reactive (Ctrl) layer and free the shift slot for a burst CD (Ascendance/Feral Spirit). Low priority.** |
| Class 7 (Raid Defensive) | Totemic Projection | weak | PLAUSIBLE | Totemic Projection is a totem-relocate utility, not a raid defensive; Enhancement has no true raid-external, so the bucket's intended role is structurally unmet and this is a repurposed placeholder. → **Acceptable given the spec lacks a raid defensive; note the bucket is effectively repurposed for utility.** |

*Affirmed as correct (10):* Combat 1=Stormstrike, Combat 2=Lava Lash, Combat 4=Crash Lightning, Combat 6=Lightning Bolt, Combat 7=Chain Lightning, Combat 9=Doom Winds, Interrupt=Wind Shear, Personal Defensive 1=Astral Shift, Slow=Earthgrab Totem, Class 4 (Special)=Feral Lunge

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Voltaic Blaze** — 'Frequent' builder/Flame Shock refresh (spell 470057) present in the tier-1 APL — the ability that actually maintains the Flame Shock the seed parks on prime key 3, yet it has no binding. Combat 10 (S2) is unassigned and free for it.
- **Tempest** — 'Frequent' Stormbringer hero-tree spender (massive nuke replacing a Lightning/Chain cast at 10 stacks). A core spender in the Stormbringer build with no key at all; deserves a fast/shift slot over the 40-60s CDs currently occupying Q/F.
- **Primordial Storm** — 'Frequent' Totemic hero-tree spender (replaces the lightning nuke in the Totemic loop) — unbound. Central to the raid-preferred Totemic build and needs a real key.
- **Ascendance** — ~2-min major burst cooldown (or DRE proc) that REPLACES Doom Winds in that build and enables Windstrike/Thorim's Invocation. Entirely unbound; Combat 10 (S2) is empty and ideal.
- **Feral Spirit** — Major burst-loop cooldown (spirit wolves). Unbound — may be passively granted in the Midnight tree (flagged @verify-ingame); if it remains an active button it needs a shift/Combat slot.
- **Elemental Blast** — Optional hard-hitting Maelstrom spender; only if talented, but if run it competes for a spender key and currently has no home.
- **Windfury Weapon / Flametongue Weapon / Lightning Shield** — Maintained precombat imbues/self-buff — low mid-combat press priority, but none are bound anywhere; belong on Alt-layer or a Free slot for re-application on expiry.

---

## Shaman — Restoration

KB confidence: **medium** · 17 verified findings (5 actionable, 12 affirmed) · 3 dropped in verify

> **Sourcing note / gaps:** No Tier-1 simc APL exists for Restoration Shaman — simc MID1 ships only Elemental and Enhancement profiles (verified 2026-07-11 via GitHub contents API on the midnight branch), so rotation.md and builds.md rest on Tier-3 Method/Icy Veins/Maxroll and are marked medium confidence. method.gg pages are JS-rendered; the /rotation subpath 404s (the live page is /playstyle-and-rotation) — content pulled from that page plus Icy Veins. Several cooldown/cast values are approximate and carry @verify-ingame markers: Healing Surge cast, Surging Totem CD, Downpour CD, Totemic Projection CD, Thunderstorm CD, …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 7 (Raid Defensive) | Totemic Projection | wrong | CONFIRMED | Role mismatch confirmed. Totemic Projection is a totem-relocation utility (grounding: 'Relocates active totems'), not a raid defensive/DR cooldown. Resto's actual raid-DR button is Spirit Link Totem (~10-15% DR + health equalize) — parked at Combat 12 — or Healing Tide Totem. The Raid Defensive slot holds a low-value u … |
| Res | Skyfury | wrong | CONFIRMED | Role mismatch confirmed. Grounding lists Skyfury as 'Applies the Shaman raid buff (Skyfury)' — it is the once-per-fight raid buff, not a resurrect. Shaman has no battle-res; the out-of-combat rez is Ancestral Spirit (absent from the inventory). Filing the raid buff under Res is wrong. → **Move Skyfury to the Buff bucke … |
| — | Healing Surge (unbound) | gap | CONFIRMED | Most material omission, confirmed. Healing Surge — the spec's fast, expensive emergency single-target heal that consumes Tidal Waves for a big crit (priority: reactive) — appears nowhere in the seed. A reactive top-up like this needs a reachable key. → **Bind Healing Surge to an empty Self-Heal slot (1 or 2).** |
| Self-Heal 4 (Emergency/Overflow) | Earth Shield | weak | CONFIRMED | Real role/frequency mismatch. Earth Shield is a tank/target maintenance shield refreshed when charges run low (grounding frequency: situational), not an emergency top-up. The spec's actual fast emergency heal, Healing Surge, is bound nowhere in the seed, and the reactive Self-Heal slots are exactly where it belongs. →  … |
| Buff | Ancestral Vision | weak | CONFIRMED | Mirror of the Skyfury misfile. The Buff slot should carry the spec's real raid buff (Skyfury), which is instead sitting in Res. Ancestral Vision is a situational utility whose 12.0.7 behavior is explicitly unverified in the grounding ('confirm current behavior in-game'), so it is a poor occupant of the dedicated raid-b … |

*Affirmed as correct (12):* Combat 5=Riptide, Combat 6=Healing Wave, Combat 7=Chain Heal, Combat 2=Lava Burst, Combat 9=Ascendance, Combat 11=Unleash Life, Interrupt=Wind Shear, Class 6 (Dispel)=Purify Spirit, Class 5 (Purge)=Purge, Class 8 (Lust/BRes)=Heroism, Personal Defensive 1=Astral Shift, Class 4 (Special)=Spiritwalker's Grace

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Healing Surge** — The spec's fast emergency single-target heal (consumes Tidal Waves for a big crit) is bound nowhere, yet Self-Heal 1 (C1) and Self-Heal 2 (C2) sit empty. A reactive top-up like this must have a reachable key — this is the most impactful omi …
- **Healing Tide Totem** — Totemic's primary raid cooldown is unbound. It is a choice node vs Ascendance, so this is build-conditional — but if you run Totemic instead of Farseer/Ascendance, HTT (not Ascendance at Combat 9) needs the raid-CD slot, and it is the natur …
- **Surging Totem** — Under the Totemic hero build, Surging Totem replaces Healing Rain as the AoE anchor (keep active, reposition via Totemic Projection). The seed binds Healing Rain (Combat 10) but not Surging Totem, so a Totemic build has no bind for its core …
- **Stormstream Totem** — The apex talent's empowered-HST proc spend (banked by Riptide / Nature's/Ancestral Swiftness) has no key. If specced into the apex, this is an active button pressed when banked and should not be unbound.
- **Downpour** — In the Downpour build this is a frequent burst-AoE spender used before the puddle expires; unbound. Build-conditional, but needed a key if talented.

---

## Warlock — Affliction

KB confidence: **high** · 18 verified findings (6 actionable, 12 affirmed) · 3 dropped in verify

> **Sourcing note / gaps:** method.gg /abilities and /rotation subpages returned HTTP 404 (JS-rendered guide split changed); corroborated instead from the existing sibling rotation.md/builds.md (which cite the simc APL + method.gg talents) and Icy Veins 12.0.7. A few resource/CD values are marked @verify-ingame in abilities.md: Spell Lock's exact 12.0.7 cooldown, Shadow of Nathreza's precise cost/effect, Malevolence details (Hellcaller-only), and whether Curse of Weakness is baseline vs talent in 12.0.7. Haunt/Darkglare/Dark Harvest cast+CD were confirmed from Wowhead (Haunt: 1.5s/15s/no shard; Darkglare: instant/2min; D …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Class 5 (Purge) | Banish | wrong | CONFIRMED | Banish is single-target demon/elemental CC (inventory function: CC), not a purge/dispel. Affliction has no personal purge in the inventory (only the pet's Devour Magic), so the bucket holds an off-role ability. → **Leave the Purge bucket empty or macro the pet's Devour Magic; move Banish to a CC/overflow slot.** |
| Slow | Subjugate Demon | wrong | CONFIRMED | Subjugate Demon is demon-enslave control (inventory function: CC), not a snare. The spec's real movement slow, Curse of Exhaustion, is instead parked in Class 1 (Movement). → **Put Curse of Exhaustion in the Slow bucket; demote Subjugate Demon to overflow.** |
| Combat 8 | — | gap | CONFIRMED | Combat 8 is unassigned in the seed while the meta apex cooldown Shadow of Nathreza (priority: cooldown, part of the Darkglare burst) has no bind at all — a free fast slot next to an unbound rotational CD. → **Bind Shadow of Nathreza to the open Combat 8 slot (or the shift-cooldown slot freed from Malevolence).** |
| Combat 10 | Malevolence | weak | CONFIRMED | Inventory confirms Malevolence is Hellcaller-only (priority: rare, near-dead build in S1) yet it occupies a prime shift-cooldown slot, while the meta build's apex burst CD Shadow of Nathreza is bound nowhere in the seed. → **Replace with Shadow of Nathreza (folded into the Darkglare window); demote Malevolence to overf … |
| Class 4 (Special) | Blight of Weakness | weak | CONFIRMED | Inventory confirms Blight of Weakness is the choice-talent transform OF Curse of Weakness — the same button, and only one exists at a time. Curse of Weakness is already bound in Class 3 (Tag), so this is a duplicate binding. → **Bind only whichever is talented (Curse of Weakness OR Blight of Weakness), freeing Class 4  … |
| Immune/Spell Immune/Movement | Demonic Circle | weak | PLAUSIBLE | The bucket's role (immune/movement escape) is served by Demonic Circle: Teleport (breaks snares/roots), which sits on Taunt/Quick Access instead; this bucket holds only the anchor-placement setup half. → **Swap: Demonic Circle: Teleport (the reactive escape) on the Immune/Movement key, placement on Quick Access.** |

*Affirmed as correct (12):* Combat 1=Drain Soul, Combat 4=Unstable Affliction, Combat 3=Agony, Combat 5=Haunt, Combat 6=Seed of Corruption, Combat 7=Dark Harvest, Combat 9=Summon Darkglare, Interrupt=Spell Lock, Class 8 (Lust/BRes)=Soulstone, Personal Defensive 1=Dark Pact, Personal Defensive 2=Unending Resolve, Movement Ability=Burning Rush

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Shadow of Nathreza** — The apex spec active and a real part of the meta Darkglare burst (priority: cooldown), but it is bound to no bucket at all. Malevolence (near-dead Hellcaller build) sits on the shift-cooldown slot it should own.
- **Malefic Grasp** — Listed as a frequent filler channel during every Darkglare window. It transforms from Shadow Bolt in the Darkglare window, but this seed uses Drain Soul as the filler and binds no Shadow Bolt — so on a Drain Soul build the Darkglare-window  …
- **Shadow Bolt** — The alternative Nightfall-proc filler; not bound. Correct to omit IF the Drain Soul filler talent is taken (they are a choice node), but flagged so the build assumption is explicit.

---

## Warlock — Demonology

KB confidence: **medium** · 11 verified findings (4 actionable, 7 affirmed) · 3 dropped in verify

> **Sourcing note / gaps:** rotation.md and builds.md already existed at patch 12.0.7 and were left untouched (confirmed-existing) per the cheap re-run guard; only abilities.md was authored. No SimulationCraft MID1 Demonology APL was fetched this run — rotation.md's existing priority is sourced from Icy Veins (Tier 3) + method.gg, not a Tier-1 simc APL (the Affliction set has a simc APL but Demo's rotation.md does not cite one; a Tier-1 APL re-distill is still pending). method.gg's /abilities and /rotation subpages 404 or return JS shells, so exact cast times / cooldowns / shard costs in abilities.md are approximate (mar …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Interrupt | Spell Lock | wrong | CONFIRMED | Interrupt slot holds Spell Lock, which is the Felhunter's Command Demon ability. Demonology universally runs the Felguard in group content (grounding: 'universal in group content'), whose Command Demon is Axe Toss. With a Felguard summoned, Spell Lock does nothing — the load-bearing kick slot holds an ability the stand … |
| Slow | Subjugate Demon | wrong | CONFIRMED | Slow bucket holds Subjugate Demon, which grounding lists as CC (demon enslave), not a slow. The spec's actual slow — Curse of Exhaustion ('Reduces movement speed; kite tool') — is filed under Class 1 (Movement) instead, so the dedicated Slow key holds a niche enslave that rarely fires. → **Move Curse of Exhaustion into … |
| Combat 1 | Shadow Bolt | stale-name | CONFIRMED | The S1 build talents Demoniac, which replaces Shadow Bolt with Infernal Bolt (2 shards/cast). Grounding confirms the replacement and that Demoniac is 'the S1 build'. Infernal Bolt auto-overrides the same button, so the placement is functionally fine — but the label is the pre-replacement name. → **Relabel to 'Infernal  … |
| Combat 7 / Combat 8 | Summon Doomguard / Grimoire: Fel Ravager | gap | PLAUSIBLE | The Combat 7/8 placements themselves are defensible as a burst-window cluster next to Tyrant. The real issue is a gap: Dominion of Argus — the apex major cooldown the S1 build is built around, listed active/cooldown-frequency and aligned with Tyrant — is bound nowhere in the seed, while empty Combat slots exist. The fu … |

*Affirmed as correct (7):* Combat 3=Hand of Gul'dan, Combat 2 / Combat 4=Call Dreadstalkers / Demonbolt, Combat 5=Implosion/Power Siphon, Combat 6=Summon Demonic Tyrant, Personal Defensive 1 / Personal Defensive 2=Dark Pact / Unending Resolve, Class 8 (Lust/BRes)=Soulstone, Self-Heal 3 / Self-Heal 4=Fel Domination / Summon Felguard

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Dominion of Argus** — Apex major cooldown that the entire S1 build is constructed around, fired aligned with Summon Demonic Tyrant. The seed binds it nowhere, yet Combat 9-12 (S1-S4) are all empty. It should take Combat 9 (S1) beside Tyrant so the burst package  …
- **Command Demon / Axe Toss** — The actual interrupt for the Felguard build that Demonology universally runs in group content. It is unbound because the Interrupt bucket instead holds Spell Lock (the Felhunter's version, which won't fire with a Felguard out). This is the  …

---

## Warlock — Destruction

KB confidence: **high** · 17 verified findings (9 actionable, 8 affirmed) · 3 dropped in verify

> **Sourcing note / gaps:** Hero-tree default is a genuine, contested S1 split: method.gg /talents recommends Hellcaller for most content incl. M+ (Diabolist "equal in ST"), while method.gg /playstyle and the simc midnight profile's default APL/talent string lean Diabolist. Flagged medium-confidence in builds.md with a @verify-ingame TODO. method.gg/rotation returned 404 and the Wowhead rotation page returned only a nav shell — rotation.md is sourced from the Tier-1 simc APL + method.gg /playstyle instead. Seed correction: the seed's 'Summon Felguard' is a Demonology-only pet, NOT a Destruction ability (corrected in abil …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Self-Heal 4 (Emergency/Overflow) | Summon Felguard | wrong | CONFIRMED | Seed binds 'Summon Felguard' here, but grounding states Felguard is Demonology-only and NOT available to Destruction — the bucket holds a non-existent button for the spec, and it is not a self-heal. → **Bind a real emergency/overflow button (e.g. Fel Domination for instant re-summon) or leave Free. Destruction pets are … |
| Class 5 (Purge) | Banish | wrong | CONFIRMED | Seed binds Banish in the Purge bucket, but grounding defines it as Demon/Elemental CC, not a dispel/purge. Destruction has no player purge (the only dispel-adjacent effect rides on the Felhunter's Spell Lock). → **Leave the purge bucket empty (no player purge exists) and bind Banish on a rare CC/utility key.** |
| Class 7 (Raid Defensive) | Soulburn | wrong | CONFIRMED | Seed binds Soulburn as a raid defensive, but grounding defines it as a spell-empower utility (empowers Soul Fire/Healthstone/Demonic Circle). Role mismatch — it is not a defensive at all. → **No true raid-wide defensive exists for Destruction; move Soulburn to a utility/Free slot and leave this empty.** |
| Slow | Subjugate Demon | wrong | CONFIRMED | Seed binds Subjugate Demon in the Slow bucket, but grounding defines it as an enslave-demon utility, not a movement slow. The real slows (Curse of Exhaustion, Curse of Tongues) are bound elsewhere. → **Put a real slow here (e.g. Curse of Exhaustion) and bind Subjugate Demon on a rare/Free utility key.** |
| Combat 3 (DoT / core-maintenance) | Wither (missing) | gap | CONFIRMED | Wither is absent from the seed. Grounding + priority list mark it a 'constant' maintenance DoT and the Hellcaller replacement for Immolate. The seed already binds Hellcaller-exclusive Malevolence (Combat 10) and Blight of Weakness (Class 4) but not Wither — a Hellcaller build is left without its core DoT button. → **Bi … |
| Combat 1 (filler) | Ruination (missing) | gap | CONFIRMED | Ruination is bound nowhere. Grounding + priority list mark it 'frequent' — a Diabolist free empowered-nuke proc/spender that needs a fast reactive key. Diabolist players have no bind for their proc payoff. → **Bind Ruination on a fast unmodified/reactive key for Diabolist builds.** |
| Combat 1 (filler) | Infernal Bolt (missing) | gap | PLAUSIBLE | Infernal Bolt is bound nowhere. Grounding: Diabolist Incinerate replacement and APL shard-refill builder ('frequent'). A Diabolist build's filler/shard-refill button has no home (mutually exclusive with Incinerate). → **For Diabolist builds bind Infernal Bolt on the Combat 1 filler slot (replacing/alongside the Inciner … |
| Combat CD slot (shift-layer) | Embers of Nihilam (missing) | gap | PLAUSIBLE | Embers of Nihilam is absent. Grounding: spec apex active (tree row 12) triggering Echo of Sargeras, a cooldown-frequency burst button when talented. When talented it has no bind alongside Summon Infernal/Malevolence. → **When talented, bind Embers of Nihilam on a shift/combat-CD key next to the other burst cooldowns.** |
| Class 4 (Special) | Blight of Weakness | weak | PLAUSIBLE | Blight of Weakness is a Hellcaller choice-node upgrade to Curse of Weakness (grounding: 'spreading/empowered Curse of Weakness'), yet Curse of Weakness is also bound on Class 3. Since the seed already commits to Hellcaller (Malevolence bound), only the upgraded curse is active — binding both is redundant. → **Bind whic … |

*Affirmed as correct (8):* Combat 1=Incinerate, Combat 4=Chaos Bolt, Combat 5=Shadowburn, Combat 6=Rain of Fire, Combat 8=Soul Fire, Combat 9=Summon Infernal, Interrupt=Spell Lock, Class 8 (Lust/BRes)=Soulstone

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Wither** — Constant-maintenance DoT and the Hellcaller REPLACEMENT for Immolate — a Hellcaller build needs it on the constant-press key (Combat 3, where Immolate currently sits). Not bound anywhere; a Hellcaller player is left without their core DoT b …
- **Infernal Bolt** — Diabolist Incinerate replacement and the APL shard-refill builder — a 'frequent'/constant press. If playing Diabolist it should own the Combat 1 filler slot; it is bound nowhere, so the Diabolist filler is missing.
- **Ruination** — Diabolist free empowered-nuke proc, listed 'frequent' — a reactive spender that needs a fast unmodified key. Completely absent from the seed; Diabolist players would have no bind for their proc payoff.
- **Embers of Nihilam** — Spec apex active (tree row 12) triggering Echo of Sargeras haste/crit — a cooldown-frequency burst button when talented. Not bound; belongs on a shift/combat-CD key alongside Summon Infernal/Malevolence.

---

## Warrior — Arms

KB confidence: **high** · 13 verified findings (5 actionable, 8 affirmed) · 1 dropped in verify

> **Sourcing note / gaps:** All three target files already existed at patch 12.0.7 (abilities.md/rotation.md high confidence, builds.md medium), so per the cheap re-run guard none were rewritten — no new web fetches were needed. Name reconciliation confirmed against raw/wago/SpellName.csv: 'Demolish' (34625/436358), 'Colossus Smash' (108126/167105), 'Overpower' (7384), 'Bladestorm' (9632/227847), 'Ravager' (143872/228920), 'Master of Warfare' (1269314) all present under current names — no stale/renamed seed names. Note: SpellName.csv lists 'Mortal Strike' under spell 9347 (generic) while the Arms talent grants spell 1229 …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Stance 1 | Protection Stance | stale-name | CONFIRMED | Arms has no Protection Stance (that is the Protection tank stance). The inventory's non-offensive stance is Defensive Stance (damage-reduction toggle). The placeholder name is wrong for this spec. → **Rename to Defensive Stance — the actual Arms toggled mitigation stance.** |
| (unbound rotational) | Whirlwind | gap | CONFIRMED | Whirlwind is a 'frequent' AoE spender (consumes Collateral Damage at 3 stacks; lands a Slam-equivalent on the primary target in the Fervor of Battle build) yet appears in no seed placement. The AoE kit only has Cleave and Thunder Clap — a frequently-pressed rotational button has no home. → **Bind Whirlwind to a fast ke … |
| (unbound defensive) | Berserker Rage | gap | PLAUSIBLE | Berserker Rage — self fear/sap/incap break (~60s) that also generates Rage — is unbound; only the ally-only Berserker Shout is placed. A DPS's reactive anti-CC button has no key. → **Bind Berserker Rage to an empty reactive/personal-defensive slot (or the Self-Heal overflow slot in place of Berserker Shout).** |
| Combat 7 | Thunder Clap/Rend | weak | PLAUSIBLE | Two separately-maintained 'frequent' builders share one key. Rend is the single-target bleed refreshed <5s; Thunder Clap is the AoE builder. They are only mode-exclusive (TC spreads Rend in AoE), so single-target Rend upkeep competes with the AoE button on the same bucket. → **Acceptable if the build leans on Thunder C … |
| Self-Heal 3 (Overflow) | Berserker Shout | weak | CONFIRMED | Per the grounding, Berserker Shout removes fear from nearby ALLIES (choice vs Fearless) — it is ally support, not a self-defensive/heal. The self version, Berserker Rage (breaks fear/sap/incap on you, ~60s, generates Rage), is the broadly-useful reactive button for a DPS and is unbound anywhere in the seed. → **Prefer  … |

*Affirmed as correct (8):* Combat 2=Mortal Strike, Combat 1=Slam, Combat 4=Overpower, Combat 5=Execute, Combat 6=Cleave, Combat 3=Colossus Smash, Interrupt=Pummel, Self-Heal 2=Ignore Pain

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Whirlwind** — A 'frequent' AoE spender that consumes Collateral Damage at 3 stacks (and lands a Slam-equivalent on the primary target in the Fervor of Battle build). It is completely unbound — the AoE kit only has Cleave (E) and Thunder Clap (R). A frequ …
- **Berserker Rage** — Self fear/sap/incap break (~60s) that also generates Rage — the reactive defensive/anti-CC button for a DPS. Only the ally-only Berserker Shout is bound. Personal Defensive 2 (SZ) is left empty and would fit it perfectly.

---

## Warrior — Fury

KB confidence: **high** · 21 verified findings (5 actionable, 16 affirmed) · 1 dropped in verify

> **Sourcing note / gaps:** abilities.md and rotation.md already existed at patch 12.0.7 (confirmed-existing, not rewritten). Only builds.md was authored. Unresolved / flagged @verify-ingame: exact S1 2pc/4pc tier-set wording + the Odyn's Fury cooldown reduction; exact base CDs for Odyn's Fury and Champion's Spear rage-on-cast in 12.0.7; Enraged Regeneration / Berserker Shout exact heal/DR/CD values; Rampaging Berserker active-vs-passive breakdown; and the live 12.0.7 stat order (guides give only a flat Crit/Haste-ish consensus). Import strings should be confirmed to load on the correct hero tree in-game. No dedicated re …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Stance 1 | Protection Stance | stale-name | CONFIRMED | 'Protection Stance' is a mislabel — that is the Protection tank stance, which Fury cannot use. Fury's damage-reduction stance is Defensive Stance (grounding flags this explicitly). → **Rename this slot to Defensive Stance (the DR toggle Fury actually uses).** |
| Combat 7 | Thunder Clap/Rend | weak | CONFIRMED | Bundling Thunder Clap (frequent MT filler) with Rend (situational bleed) is reasonable, but the empowered Thunder Blast — a frequent MT press (fire at 2 stacks / during Avatar; extends Avatar + triggers Lightning Strike) — is absent from the entire seed and has no fast-key home. → **Fold Thunder Blast onto this bucket  … |
| Self-Heal 3 (Overflow) | Berserker Shout | weak | PLAUSIBLE | Berserker Shout is a fear/incapacitate break (+Enrage), not a self-heal. It is reactive so an overflow layer is tolerable, but the Self-Heal role label mismatches the ability. → **Keep on a reactive overflow key but treat as CC-break utility, not a heal.** |
| Self-Heal 4 (Emergency/Overflow) | Spell Reflection | weak | PLAUSIBLE | Spell Reflection is a magic-damage defensive, not a heal; reactive so the overflow layer works, but it would group more naturally with the real defensives. → **Consider moving to the unused Personal Defensive 2 slot to group it with the other defensives.** |
| Class 5 (Purge) | Intervene | weak | CONFIRMED | Fury has no purge/dispel in its inventory, so the nominal Purge role cannot be filled; Intervene is a mobility hop / ally damage-intercept. Functional use of an otherwise-dead bucket, but the role label mismatches the ability. → **Acceptable as filler; alternatively move Intervene to a movement/defensive slot and leave … |

*Affirmed as correct (16):* Combat 1=Bloodthirst, Combat 2=Raging Blow, Combat 3=Rampage, Combat 4=Whirlwind, Combat 5=Execute, Combat 6=Odyn's Fury, Combat 8=Recklessness, Combat 9=Avatar/Bladestorm, Combat 12=Champion's Spear, Interrupt=Pummel, Personal Defensive 1=Enraged Regeneration, Class 7 (Raid Defensive)=Rallying Cry, Stance 2=Berserker Stance, Slow=Hamstring …

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Thunder Blast** — Frequent Mountain Thane press (fire at 2 stacks / during Avatar; extends Avatar and always triggers Lightning Strike). The empowered Thunder Clap has no bucket at all — it should live on Combat 7 alongside Thunder Clap so the MT rotation ha …
- **Defensive Stance** — The spec's real DR stance is absent by name — the seed labels Stance 1 'Protection Stance', a tank stance Fury cannot use. The correct ability (Defensive Stance) needs to occupy that slot.

---

## Warrior — Protection

KB confidence: **high** · 9 verified findings (6 actionable, 3 affirmed) · 4 dropped in verify

> **Sourcing note / gaps:** All three files already existed at patch 12.0.7 (fetched/reviewed 2026-07-11) and were confirmed, not rewritten. Open items carried in the existing files: (1) Champion's Spear CD/mechanics flagged @verify-ingame; (2) the simc talent string is @verify-ingame (import strings are tree-version-sensitive - confirm it loads as Mountain Thane); (3) builds.md lacks a gearing/stat-priority/enchant section (deferred to general tank-gearing flow) and a confirmed per-scenario M+ vs raid Mountain Thane string; (4) rotation.md opener not yet WCL-log-verified and awaits a retuned 12.0.7 simc APL if published …

| Bucket | Seed ability | Verdict | Conf | Issue → suggestion |
|---|---|---|---|---|
| Stance 1 | Protection Stance | stale-name | CONFIRMED | The grounding is explicit: no 'Protection Stance' exists in 12.0.7 game data; the Protection tanking stance is Defensive Stance (386208). The seed's Stance 1 label is a stale/nonexistent name. → **Rename Stance 1 to Defensive Stance.** |
| Personal Defensive 2 | Last Stand | gap | CONFIRMED | Last Stand (Defensive, ~180s, +30% max HP emergency EHP) is in the inventory but appears in none of the 40 seed values. Only Shield Wall is on a personal-defensive slot; the second personal-defensive slot is empty. → **Bind Last Stand to the empty second personal-defensive slot (Personal Defensive 2).** |
| Self-Heal 3 (Overflow) | Berserker Shout | weak | CONFIRMED | Berserker Shout is a reactive fear/sleep/incap break (anti-CC), not a self-heal or rage-overflow tool. Role mismatch for a Self-Heal bucket, though the Ctrl reactive tier fits its press pattern. Name is correctly reconciled from the stale 'Berserker Rage'. → **Acceptable as an overflow parking spot, but it is anti-CC,  … |
| Self-Heal 4 (Emergency/Overflow) | Spell Reflection | weak | CONFIRMED | Spell Reflection is a reactive magic mitigation/reflect defensive (~25s), not a self-heal. Parked in an overflow self-heal bucket; the reactive Ctrl tier fits its press pattern but the bucket role is a mismatch. → **Fine as an overflow home for a short-CD reactive defensive; just note it is not a heal.** |
| Class 5 (Purge) | Intervene | weak | CONFIRMED | The inventory has no purge for Protection Warrior. Intervene (ally-jump / damage-intercept movement+defensive) is parked in the Purge slot as overflow — sensible reuse of a dead bucket, but role-mismatched. → **Acceptable overflow placement — no true purge exists for Protection.** |
| Class 6 (Dispel) | Challenging Shout | weak | CONFIRMED | The inventory has no dispel for Protection Warrior. Challenging Shout (AoE taunt, ~90s) is parked in the Dispel slot — reasonable reuse of a dead bucket, but role-mismatched (it's a mass-pickup taunt). → **Acceptable overflow — no dispel exists; AoE taunt is a fine tenant for the dead slot.** |

*Affirmed as correct (3):* Class 2 (CC)=Piercing Howl, Interrupt=Pummel, Taunt/Quick Access=Taunt

**Missing / mis-slotted (important abilities the seed omits or buries):**

- **Last Stand** — Major emergency defensive (+30% max HP, ~3min). The seed binds only Shield Wall (Personal Defensive 1) and leaves Personal Defensive 2 (SZ) empty — Last Stand should go there. Currently unbound entirely.
- **Spell Reflection** — Bound only as overflow filler in the Self-Heal 4 bucket, not in a true defensive slot. It's a real ~25s reactive magic defensive that a tank presses often in M+; buried under a 'self-heal' label it's easy to forget it exists.
- **Intervene** — Real co-tank positioning + damage-intercept movement/defensive tool, but parked in the dead 'Purge' bucket rather than a Movement 2 slot (SX is empty). Movement Ability 2 would be a more discoverable, role-appropriate home.
- **Intimidating Shout** — AoE fear — the choice-node alternative to Piercing Howl. Only Piercing Howl is bound; if the player runs the fear instead there is no slot mapped to it.
- **Devastate** — Rare last-resort filler builder — minor, but it has no bucket at all. Acceptable to omit given it's usually replaced by the Devastator passive, but worth noting it's absent.

---
