---
title: Demonology Warlock — ability inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06  # reconciled against the generated DB2 ability inventory (Summon Doomguard, Spell Lock origin, Create Healthstone). Earlier: the four not-on-the-tree names re-confirmed against the API tree itself; Summon Demonic Tyrant costs 0 shards, not 1 (Tier-1 C_Spell.GetSpellPowerCost + DB2); Infernal Bolt yield 2→3 was corrected 2026-07-25
sources:
  - knowledge/classes/warlock/demonology/ability-inventory.tsv  # tier 1, generated DB2 inventory @ 12.0.7.67808 — the name/spellID/origin/cooldown floor, 2026-08-06
  - knowledge/classes/_abilities/pet-family-annex.tsv  # tier 1, pet skill lines @ 12.0.7.67808, 2026-08-06
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived, the verdicts applied here, 2026-08-06
  - https://us.api.blizzard.com/data/wow/talent-tree/720/playable-specialization/266  # tier 1, Blizzard Game Data API talent/spell names, static-12.0.7
  - raw/wago/SpellName.csv  # tier 1, wago.tools SpellName DB2 @ 12.0.7.67808 — name canonicalization
  - https://www.icy-veins.com/wow/demonology-warlock-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7 (upd. 2026-05-19), ability roles + cast/CD corroboration
  - https://www.wowhead.com/spell=264178/demonbolt  # tier 4, Demonbolt effect corroboration
  - ./talents.md  # local, spec talent tree (12.0.7.67808)
  - knowledge/classes/_talents/all-talents.tsv  # tier 1, every spec's tree — the four not-on-the-tree names checked across all of them
confidence: medium
---

# Demonology Warlock — ability inventory (Midnight S1)

> Companion to `rotation.md` (priority/CDM), `builds.md` (talents/gear), and
> `talents.md` (raw tree). This is the raw ability catalog with game roles —
> not a rotation and not a keybind sheet.

## Overview

- **Hero trees:** **Diabolist** (M+ default — burst via Demonic Ritual →
  Overlord / Pit Lord summons inside the Tyrant window) and **Soul Harvester**
  (ST/raid + solo-survivability alternative). See `builds.md`.
- **Resources:** **Soul Shards** (0–5; builders generate, spent on Hand of
  Gul'dan / Call Dreadstalkers / summons) and **Demonic Core** (a proc/charge
  system, up to 4 stacks, consumed to make **Demonbolt** instant + hard-hitting).
  Mana is effectively a non-constraint.
- **Playstyle:** a builder/spender **pet-army** spec. You bank shards and imps,
  then funnel everything into the 1-minute **Summon Demonic Tyrant** window,
  which empowers and extends every active demon. Most of your damage comes from
  the demons, not your own casts.

## Inventory

`Function` = game role, not a keybind assignment.

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
| **Shadow Bolt** | Rotational-builder | Generates 1 Soul Shard | ~2s cast | Baseline single-target filler / shard builder. Chance to grant a Demonic Core. **Replaced by Infernal Bolt** when *Demoniac* is talented (the S1 build). |
| **Infernal Bolt** | Rotational-builder | Generates 3 Soul Shards | ~2.3s cast | *Demoniac* talent replacement for Shadow Bolt — builds shards ~3× as fast; cast when at ≤2 shards. |
| **Demonbolt** | Rotational-spender (core) | Consumes 1 Demonic Core; generates 2 Soul Shards | Instant with a Demonic Core (else ~4.5s cast) | Demonic-Core spender — hits hard and refunds 2 shards. Applies **Doom** if talented. Dump cores so they don't overcap. |
| **Hand of Gul'dan** | Rotational-spender (imp generator) | 1–3 Soul Shards | ~1.5s cast | Spend 1–3 shards to summon that many **Wild Imps**. The single most-maximized cast inside the Tyrant window; cast at 4–5 shards, never overcap. |
| **Call Dreadstalkers** | Rotational-summon | 2 Soul Shards (free/instant with *Demonic Calling*) | ~20s CD | Summons **two Dreadstalkers** for ~12s. Refresh just before Tyrant so they're fresh when it empowers them. |
| **Summon Demonic Tyrant** | Major cooldown | **none** | ~1s cast / **60s** `[T1]` | The spec's centerpiece. Empowers and **extends the duration of every active demon** for ~15s and pumps damage. Enter with a full board (Wild Imps + fresh Dreadstalkers + Grimoire demon). |
| **Dominion of Argus** | Major cooldown (apex) | — | active, aligns w/ Tyrant | Apex talent; a large Summon Demonic Tyrant enhancement — the S1 build is built around it (see `builds.md`). @verify-ingame |
| **Implosion** | Rotational-spender (AoE) | — (consumes Wild Imps) | Instant / **15s** `[T1]` | Sacrifices **all Wild Imps**, each flying to the target and exploding for AoE. Press at ~6 imps for cleave; on pure ST only Implode if talented into *To Hell and Back*. Choice-node vs Power Siphon. |
| **Power Siphon** | Utility (core generator) | — (consumes up to 2 Wild Imps) | ~30s CD | Choice-node vs Implosion. Sacrifices up to 2 Wild Imps to grant **2 Demonic Cores** — fuels the next Demonbolt / Hand of Gul'dan chain. |
| **Grimoire: Fel Ravager** | Rotational-summon | Soul Shards | active (choice node) / **120s** `[T1]` | Choice-node vs *Grimoire: Imp Lord*. Summons a **Fel Ravager** demon added to the Tyrant board. |
| **Summon Vilefiend** | Passive summon | — | passive/talent | Talent that summons a **Vilefiend** demon for the rotation/Tyrant board (passive node in the S1 tree). |
| **Summon Doomguard** | Rotational-summon / cooldown | Soul Shards | **120s CD** *[Tier 1]* | Summons a **Doomguard** demon — a genuine active talent on the deep spec tree (not a passive summon like Vilefiend), so it is a pressed button on a 2-minute cycle: line it up with the Tyrant window rather than pressing it on sight. |
| **Summon Felguard** | Pet | 1 Soul Shard | ~cast, out of combat | Summons the **Felguard**, Demonology's permanent pet (universal in group content). Provides **Axe Toss** interrupt via Command Demon. |
| **Command Demon / Axe Toss** | Interrupt | — | ~30s CD (Felguard) | *Command Demon* fires the active pet's special. With the Felguard that's **Axe Toss** — a ranged interrupt + brief stun. |
| **Spell Lock** | Interrupt / Dispel | — | **24s CD** *[Tier 1]* | A **pet ability learned on the Felhunter's own skill line**, not a player spell — which is why it is absent from this spec's `ability-inventory.tsv` (it lives in `_abilities/pet-family-annex.tsv`). Interrupt + a purge, fired via Command Demon, and only available if you give up the Felguard's Axe Toss to run the Felhunter. |
| **Doom** | Passive | — | passive talent | Demonbolt applies **Doom**, a delayed detonation on the target. Build-defining passive, not a pressed button. |
| **Fel Domination** | Utility (pet) | — | **180s** `[T1]` | Your next pet summon within 15s is **instant and free** — the emergency re-summon after a pet dies. |
| **Subjugate Demon** | CC (utility) | — | ~1.5s cast | Enslaves a target demon to fight for you (leveling / niche PvE utility). |
| **Drain Life** | Defensive (self-heal) | — | channel | Channels damage that **heals you** — the low-cost sustain heal; often macro'd with `/cancelaura Burning Rush`. |
| **Mortal Coil** | Defensive / CC | — | ~45s CD | Horrifies the target (~3s) and **heals ~20–25% max HP**. A defensive + single-target peel. |
| **Dark Pact** | Defensive (absorb) | Sacrifices current HP | **60s** `[T1]` / *Frequent Donor*) | Sacrifices health for a large **absorb shield**; usable while CC'd. |
| **Unending Resolve** | Defensive (major) | — | **180s** `[T1]` | **−25% damage taken** for 8s (−40% with *Strength of Will*) + interrupt/silence immunity — the big personal defensive. |
| **Create Healthstone** | Defensive (conjure → item heal) | — | Instant · no CD | The **player ability** is `Create Healthstone`; "Healthstone" alone names the *item* use, which is not a learned spell — renamed here *[Tier 1, 2026-08-06]*. Conjure pre-combat; using the stone is an instant **~25–30% HP** heal, once per combat unless *Pact of Gluttony* is talented. |
| **Soulstone** | Utility (battle-rez) | — | ~2.5s cast / **600s** `[T1]` | Combat resurrection on an ally (self-rez out of combat) — the warlock brez. |
| **Soulburn** | Utility (empower) | 1 Soul Shard | instant | Empowers the **next** spell (e.g. Healthstone/Drain Life/Demonic Circle) with a bonus effect. |
| **Demonic Circle** | Movement (utility) | — | ~0.5s cast | Places a portal on the ground. |
| **Demonic Circle: Teleport** | Movement | — | instant / **30s** `[T1]` | Teleports back to your placed Demonic Circle (kiting / mechanic dodge). |
| **Demonic Gateway** | Movement (utility) | — | ~2s cast / **10s** `[T1]` | Places a two-way gateway allies can use to skip terrain — group mobility/skips. |
| **Burning Rush** | Movement | Drains health over time | toggle | +50% run speed at the cost of health-per-second; toggle off with `/cancelaura`. |
| **Shadowfury** | CC (AoE) | — | **60s** `[T1]` | Ground-targeted **AoE stun** — the spec's main trash-pack stun. Choice-node vs *Howl of Terror*. |
| **Howl of Terror** | CC (AoE) | — | ~40s CD | AoE **fear** around you (choice-node vs Shadowfury); Diabolist can grant a stronger 10-target version. |
| **Fear** | CC (single) | — | ~1.5s cast | Single-target fear. |
| **Banish** | CC (single) | — | ~1.5s cast | Banishes a Demon/Elemental, removing it from combat temporarily. |
| **Curse of Tongues** | Utility (debuff) | — | ~1.5s cast | Slows the target's cast speed. |
| **Curse of Weakness** | Utility (debuff) | — | instant | Reduces the target's physical damage. |
| **Curse of Exhaustion** | Utility (slow) | — | instant | Reduces the target's movement speed (kite tool). |
| **Blight of Weakness** | Utility (debuff) | — | instant / **120s** `[T1]` | Talent upgrade to Curse of Weakness (choice-node vs *Blight of Tongues*); adds a lingering effect. |
| **Fel Armor / Demon Skin / Soul Leech** | Passive (defensive) | — | passive | The passive absorb/mitigation backbone — Soul Leech shields off damage dealt; Demon Skin/Fel Armor enlarge and refill it. |

**Notes / canonicalization (Tier-1 game data is the floor):**
- **Shadow Bolt → Infernal Bolt**: with *Demoniac* (the S1 build) your baseline
  builder is **Infernal Bolt** (spell 433891), not Shadow Bolt. Both names are
  live; the seed's "Shadow Bolt" is correct as the *untalented* builder.
- The seed's **"Grimoire: Fel Ravager"** is confirmed live (spell 1276467), a
  choice-node vs **Grimoire: Imp Lord**. The old **Grimoire: Felguard** (111898)
  still exists in game data but is **not** on the Midnight Demo spec tree.
- **Curse of Weakness** and **Blight of Weakness** are distinct: the curse is
  baseline; Blight is the talent upgrade (choice vs Blight of Tongues).
- **Not on the Midnight Demo spec tree** (present in older builds, omitted here):
  **Bilescourge Bombers, Nether Portal, Demonic Strength, Guillotine**. Confirmed
  against the Blizzard Game Data API tree itself — tree 720 / spec 266, whose 147
  talent names contain none of the four, while Hand of Gul'dan, Implosion, Summon
  Demonic Tyrant and Doom are all present as controls. They are absent from
  `all-talents.tsv` for **every** spec, not just this one, so they are not talents
  anywhere at 12.0.7. *[Tier 1, static-12.0.7_67808 — which is the API's current
  static namespace, not a stale pin.]*
