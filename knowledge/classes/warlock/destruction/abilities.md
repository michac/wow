---
title: Destruction Warlock — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/warlock/destruction/ability-inventory.tsv  # tier 1, generated DB2 inventory @ 12.0.7.67808 — the name/spellID/origin/cooldown floor, 2026-08-06
  - knowledge/classes/_abilities/pet-family-annex.tsv  # tier 1, pet skill lines @ 12.0.7.67808, 2026-08-06
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied here, 2026-08-06
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Warlock_Destruction.simc  # tier 1, simc midnight APL, 2026-07-11
  - raw/wago/SpellName.csv @ 12.0.7  # tier 1 game-data name reconciliation, 2026-07-11
  - https://www.method.gg/guides/destruction-warlock  # tier 3, upd. 2026-06-16, 2026-07-11
  - https://www.method.gg/guides/destruction-warlock/playstyle-and-rotation  # tier 3, 2026-07-11
  - raw/wago/SpellEffect.csv @ 12.0.7  # tier 1, energize effects -> the fragment yields, 2026-08-01
  - raw/addon-research/simc @ ab7b0b8  # tier 1, local simc checkout (branch midnight, DBC 12.0.7.68887), 2026-08-01 — ⚠ OFF-PIN: this is build 68887, the ability-inventory floor above is 67808. Do not join numbers across the two; on a conflict the 67808 inventory wins for name/ID/origin/cooldown and simc wins for APL ordering
confidence: high
---

# Destruction Warlock — Abilities (Midnight S1)

## Overview

- **Resource:** **Soul Shards** — displayed 0–5, stored internally as **0–50
  fragments** (10 per shard; confirmed in-client 2026-08-01 via
  `UnitPowerMax("player", SoulShards, true)` = 50 against a displayed 5).
  Builders generate fragments; spenders — **Chaos Bolt** (2 shards / 20 frags),
  **Rain of Fire** (3 / 30), **Shadowburn** (1 / 10) — consume whole shards. The
  whole spec is a shard economy: never overcap, always be casting.

  **Yields, in fragments** (DB2 energize effects + 12.0.7 tooltips):

  | Ability | Base | On crit | Modifiers |
  |---|---|---|---|
  | Incinerate | 2 | +1 | **Diabolic Embers ×2 → 4** |
  | Conflagrate | 5 | — | MID1 4-set **+2** |
  | Immolate / Wither tick | 1 | +1 at 50 % | haste-scaled 3 s period |
  | Soul Fire | **10** (a full shard) | — | Havoc copy doubles |
  | Infernal Bolt | **20** (Destro) / 30 (Demo) | — | see below |
  | Shadowburn kill refund | 10 | — | — |
  | Infernal pet / Overfiend | 1 / sec | — | — |

  ⚠ **Infernal Bolt is 20 or 30 on Destruction and the sources disagree** — one
  reading has the spec aura `137046` (effect #13) applying −10 to Demonology's 30.
  @verify-ingame — cast one as Diabolist and watch the bar move 2 shards or 3.
- **Hero trees (Midnight):** **Diabolist** (default — best single target,
  competitive in stacked cleave; builds shards into Chaos Bolt and cycles
  **Diabolic Ritual → Demonic Art → free Ruination**) and **Hellcaller**
  (replaces Immolate with **Wither**, adds the **Malevolence** burst CD; the
  sustained-AoE / long-fight pick). Choose the tree first — it changes the
  maintenance DoT and one major cooldown.
- **Playstyle:** Chaos Bolt is the payoff button and most of the direct damage;
  a maintained fire DoT (Immolate/Wither) plus a mix of instant Conflagrate and
  Shadowburn keeps Destruction fairly mobile between hard-cast Incinerates.

## Ability inventory

> **Tier-1 floor.** Canonical **name, spellID, acquisition origin and base
> cooldown** live in `ability-inventory.tsv` (generated from wago DB2 @
> 12.0.7.67808) — read them there rather than trusting a restated number here.
> This table is for **role and rotational context**; on any disagreement the tsv wins.

> **What the Tier-1 floor does and does not cover.** A **bold `[T1]`** cooldown
> below was read straight out of `ability-inventory.tsv` (wago DB2 @ 12.0.7.67808).
> A `~` value was **not**: it is a Tier-3 guide number that the tsv could not
> settle, and it is kept on purpose. The tsv's `cooldown` column is
> `SpellCooldowns` at DifficultyID 0 — `max(RecoveryTime, CategoryRecoveryTime)` —
> which is the real cooldown for a normal button and is **wrong for a charge
> ability**, where it returns the GCD (Fire Blast 0.5s, Purifying Brew 1s). The
> recharge lives in `SpellCategory.ChargeRecoveryTime`, unreachable without
> breaking the build pin (`_abilities/reconcile-ledger.md` §5 G6). **So "the tsv
> wins" applies to the values it actually carries, not to every row** — 194 rows
> across the 40 files read 0 or sub-10s there and keep their `~` prose instead.
>
> Names this file asserts that **no** acquisition row reaches are catalogued in
> `../../_abilities/section-4-catalogue.md`; ones game data reaches indirectly are
> in `section-3-corroborated.md`. ⚠ Neither is a backlog — an entry there is
> researched when someone **asks**, never because it has sat there a while.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Incinerate | Rotational-builder | — | 2s cast | Core filler; generates **2** fragments (+1 on crit), **doubled to 4 by Diabolic Embers**. ⚠ **Fire and Brimstone does NOT grant fragments** — its 12.0.7 tooltip is damage-only (cleave); an earlier revision of this line said otherwise. |
| Conflagrate | Rotational-builder | — | Instant · 2 charges, ~13s recharge | Instant fire nuke, generates **5** fragments (**7** with the MID1 4-set), grants **Backdraft** (faster Incinerate/Chaos Bolt casts). Mobile filler. |
| Immolate | Rotational-builder (DoT) | — | 1.5s cast · DoT | Fire DoT you keep up; each tick generates **1** fragment (+1 at 50 % on a crit tick) and can proc Conflagrate resets. Diabolist maintenance DoT. |
| Wither | Rotational-builder (DoT) | — | 1.5s cast · DoT | **Hellcaller** replacement for Immolate — stacking fire/shadow DoT that Malevolence detonates/empowers. Midnight-new hero DoT. @verify-ingame |
| Chaos Bolt | Rotational-spender | 2 Soul Shards | ~2.5s cast | Primary spender and the bulk of single-target damage; benefits from crit scaling (Chaos Incarnate / Ruin). |
| Rain of Fire | Rotational-spender (AoE) | 3 Soul Shards | Channeled AoE | Ground-target AoE spender; the shard dump at high target counts (Hellcaller sooner, Diabolist only at ~8+). |
| Shadowburn | Rotational-spender / Execute | 1 Soul Shard | Instant · ⚠ **charges disputed — see below** | Instant spender, extra value sub-20% (execute) and with Fiendish Cruelty; refunds resources / shard on a kill. |
| Soul Fire | Rotational-builder | — | ~4s cast · ~45s CD (charge-like) | Hard-cast that applies/refreshes Immolate and generates **10 fragments — a full Soul Shard**; best consumed with Backdraft. |
| Cataclysm | Rotational-builder (AoE) | — | Instant · ~30s CD | Ground AoE that applies Immolate to all targets hit and deals burst damage; strong opener + AoE setup. |
| Channel Demonfire | Rotational-spender | — | Channeled · ~25s CD | Launches bolts at all targets with Immolate/Wither; choice-node vs Demonfire Infusion. Talent. |
| Infernal Bolt | Rotational-builder | — | ~2s cast | **Diabolist** Incinerate replacement that generates **more** shards; appears in the APL as a shard-refill button when low. Midnight-new. @verify-ingame |
| Ruination | Rotational-spender (proc) | — | Instant (granted) | **Diabolist** free empowered nuke granted by cycling Diabolic Ritual → Demonic Art; press on proc. Midnight-new. @verify-ingame |
| Embers of Nihilam | **Passive** (spec apex talent) | — | — (nothing to press) | ⚠ **Not a button.** Every spell of this name in Tier-1 game data is flagged passive — there is no castable `Embers of Nihilam` at 12.0.7 *[Tier 1]*. This row previously called it a "situational burst button"; that was wrong, and nothing in the rotation should be waiting on you to press it. Treat it as an apex-row throughput passive. |
| Havoc | Utility (cleave) | — | Instant · ~30s CD | Marks a second target; single-target spells (Chaos Bolt, Shadowburn, etc.) are duplicated onto it. The 2-target cleave button. |
| Summon Infernal | Major cooldown | — | Instant · 120s CD (90s w/ Inferno), 30s duration | Meteor + persistent infernal; the primary DPS burst window everything (potion/trinkets/racials) syncs to. Base CD confirmed 120s via DB2 (SpellCooldowns spell 1122); **Inferno** talent −30s → 90s. |
| Malevolence | Major cooldown | — | **60s CD** *[Tier 1]* | **Hellcaller** burst CD — grants haste and empowers/extends active Withers. Hellcaller-exclusive, and a talent rather than a hero-tree freebie. Midnight-new. |
| Curse of Exhaustion | Utility (slow) | — | Instant | Reduces target movement speed. Curse. |
| Curse of Tongues | Utility (slow-cast) | — | Instant | Slows enemy cast speed. Curse. |
| Curse of Weakness | Utility (debuff) | — | Instant | Reduces target physical damage. Curse. |
| Blight of Weakness | Utility (debuff) | — | Instant (talent) / **120s** `[T1]` | **Hellcaller** curse upgrade (choice with Blight of Tongues) — the spreading/empowered version of Curse of Weakness. |
| Drain Life | Defensive (self-heal) | — | Channeled | Channel that damages and heals you; the core sustain filler when low. |
| Mortal Coil | CC / Defensive | — | Instant · 45s CD | Horrifies the target (~3s) and heals you 20–25% max HP. Talent. |
| Shadowfury | CC (AoE stun) | — | Instant / **60s** `[T1]` | AoE stun at a ground location. Choice node with Howl of Terror. |
| Fear | CC | — | 1.5s cast | Single-target fear; breaks on damage. |
| Howl of Terror | CC (AoE) | — | Instant / **40s** `[T1]` (talent) | AoE fear around you; choice node with Shadowfury. |
| Banish | CC | — | 1.5s cast | Incapacitates a Demon or Elemental. Talent. |
| Spell Lock | Interrupt | — | Instant · **24s CD** *[Tier 1]* | A **pet ability on the Felhunter's own skill line**, not a player spell — so it is absent from this spec's `ability-inventory.tsv` by design and lives in `_abilities/pet-family-annex.tsv`. Interrupt + purge; Destruction's kick comes from the pet, which means no Felhunter, no kick. |
| Subjugate Demon | Utility (enslave) | — | 3s cast | Takes control of a target demon. |
| Fel Domination | Pet | — | Instant / **180s** `[T1]` | Next pet summon is instant + free — emergency re-summon. |
| Summon Imp / Summon Voidwalker / Summon Felhunter / Summon Sayaad | Pet | — | Cast | Four separate class-baseline spells, one per pet — there is no generic "Summon Pet" ability, which is how this row read until *[Tier 1, 2026-08-06]*. Pick by utility: Felhunter interrupt/purge (the group-content default), Voidwalker tank, Imp dispel, Sayaad CC. Felguard is Demonology-only — not available to Destruction. |
| Soulstone | Utility (battle rez) | — | 3s cast / **600s** `[T1]` | Combat resurrection; can be pre-applied for a self-rez. |
| Create Healthstone | Defensive (conjure → item heal) | — | Instant / — | The **player ability** is `Create Healthstone` 6201 *[Tier 1]*; "Healthstone" alone names the *item* use (6262), which is not a learned spell — renamed to match affliction and demonology. Conjure out of combat; using the stone is an instant ~25–30% HP heal, reusable in combat with Pact of Gluttony. |
| Create Soulwell | Utility | — | Cast / **120s** `[T1]` | Places a well for the group to grab Healthstones. |
| Soulburn | Utility (empower) | 1 Soul Shard | Instant · ~30s CD | Empowers your next specific spell (e.g. Soul Fire / Demonic Circle / Healthstone). Talent. |
| Dark Pact | Defensive (absorb) | — | Instant · ~60s CD | Sacrifices health for a large shield; usable while CC'd. Talent. |
| Unending Resolve | Defensive | — | Instant · ~3min CD | −25% damage taken (−40% with Strength of Will) + interrupt/silence immunity, 8s. |
| Burning Rush | Movement | — | Toggle | +50% run speed at the cost of health-over-time; the main mobility toggle. |
| Demonic Circle | Movement (utility) | — | Cast to place | Drops a portal; **Demonic Circle: Teleport** returns you to it. Talent. |
| Demonic Circle: Teleport | Movement | — | Instant / **30s** `[T1]` | Teleport to your placed Demonic Circle (also breaks roots). |
| Demonic Gateway | Movement (utility) | — | Cast · ~10s | Places a linked portal pair; players click to travel between them. Talent. |
| Grimoire of Sacrifice | Utility (passive buff) | — | Instant (talent) / **30s** `[T1]` | Sacrifices your pet for a personal damage buff + a proc (choice with Summoner's Embrace). |
| Command Demon / pet-specific | Utility | — | Instant | Contextual pet command (Spell Lock, Seduction, Shadow Bulwark, etc. depending on active pet). |

> ⚠ **Shadowburn's "2 charges, ~12s recharge" is contradicted by Tier-1 data (2026-07-30).**
> The old row asserted 2 charges. Two independent Tier-1 sources disagree: wago DB2 has
> Shadowburn `17877` with `SpellCategories.ChargeCategory = 0` and
> `SpellCooldowns.RecoveryTime = 0` (against Conflagrate `17962`, which carries
> `ChargeCategory = 672`), and a live in-client capture found Shadowburn raising **no**
> `Available`/`OnCooldown`/`ChargeGained` Cooldown-Manager alerts, i.e. it has no recovery
> event at all — while Conflagrate raised all three. The likely origin of the old claim is
> a pre-Midnight tooltip. **Not yet corrected outright**, because a talent could add charges
> via an aura effect that base DB2 rows would not show. `@verify-ingame` — check
> Shadowburn's tooltip on a live Destruction character and, if it shows 1 charge and no
> recharge, delete this note and fix the row.


> **Interrupt note:** Destruction has **no baseline personal interrupt**. Kicks
> come from the **Felhunter's Spell Lock** (or CC via Sayaad's Seduction /
> Shadowfury / Howl of Terror / Mortal Coil). This matters for interrupt
> assignments.

> **`Health Funnel` is gone.** It had a row here as a pet-sustain channel; it is
> **not acquirable at 12.0.7**. Nine spells carry the name in game data and not one
> of them attaches to any acquisition table — no talent node, no class skill line,
> no spec grant *[Tier 1, 12.0.7.67808]*. Pet healing is now the pet's own
> business; don't plan around funnelling. Row deleted rather than left open, because
> the absence is measured, not merely unconfirmed.

> **Seed reconciliation:** the spec seed listed **Summon Felguard** — that is a
> **Demonology** pet and is **not** available to Destruction; corrected above.
> **Curse of Weakness** exists baseline; the Hellcaller talent line is
> **Blight of Weakness / Blight of Tongues** (choice). Names verified vs
> `raw/wago/SpellName.csv` @ 12.0.7.
