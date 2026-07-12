---
title: Demonology Warlock — ability inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://us.api.blizzard.com/data/wow/talent-tree/720/playable-specialization/266  # tier 1, Blizzard Game Data API talent/spell names, static-12.0.7
  - raw/wago/SpellName.csv  # tier 1, wago.tools SpellName DB2 @ 12.0.7.67808 — name canonicalization
  - https://www.icy-veins.com/wow/demonology-warlock-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7 (upd. 2026-05-19), ability roles + cast/CD corroboration
  - https://www.wowhead.com/spell=264178/demonbolt  # tier 4, Demonbolt effect corroboration
  - ./talents.md  # local, spec talent tree (12.0.7.67808)
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

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Shadow Bolt** | Rotational-builder | Generates 1 Soul Shard | ~2s cast | Baseline single-target filler / shard builder. Chance to grant a Demonic Core. **Replaced by Infernal Bolt** when *Demoniac* is talented (the S1 build). |
| **Infernal Bolt** | Rotational-builder | Generates 2 Soul Shards | ~2.3s cast | *Demoniac* talent replacement for Shadow Bolt — builds shards twice as fast; cast when at ≤2 shards. |
| **Demonbolt** | Rotational-spender (core) | Consumes 1 Demonic Core; generates 2 Soul Shards | Instant with a Demonic Core (else ~4.5s cast) | Demonic-Core spender — hits hard and refunds 2 shards. Applies **Doom** if talented. Dump cores so they don't overcap. |
| **Hand of Gul'dan** | Rotational-spender (imp generator) | 1–3 Soul Shards | ~1.5s cast | Spend 1–3 shards to summon that many **Wild Imps**. The single most-maximized cast inside the Tyrant window; cast at 4–5 shards, never overcap. |
| **Call Dreadstalkers** | Rotational-summon | 2 Soul Shards (free/instant with *Demonic Calling*) | ~20s CD | Summons **two Dreadstalkers** for ~12s. Refresh just before Tyrant so they're fresh when it empowers them. |
| **Summon Demonic Tyrant** | Major cooldown | 1 Soul Shard | ~1s cast · 1-min CD | The spec's centerpiece. Empowers and **extends the duration of every active demon** for ~15s and pumps damage. Enter with a full board (Wild Imps + fresh Dreadstalkers + Grimoire demon). |
| **Dominion of Argus** | Major cooldown (apex) | — | active, aligns w/ Tyrant | Apex talent; a large Summon Demonic Tyrant enhancement — the S1 build is built around it (see `builds.md`). @verify-ingame |
| **Implosion** | Rotational-spender (AoE) | — (consumes Wild Imps) | Instant | Sacrifices **all Wild Imps**, each flying to the target and exploding for AoE. Press at ~6 imps for cleave; on pure ST only Implode if talented into *To Hell and Back*. Choice-node vs Power Siphon. |
| **Power Siphon** | Utility (core generator) | — (consumes up to 2 Wild Imps) | ~30s CD | Choice-node vs Implosion. Sacrifices up to 2 Wild Imps to grant **2 Demonic Cores** — fuels the next Demonbolt / Hand of Gul'dan chain. |
| **Grimoire: Fel Ravager** | Rotational-summon | Soul Shards | active (choice node) | Choice-node vs *Grimoire: Imp Lord*. Summons a **Fel Ravager** demon added to the Tyrant board. |
| **Summon Vilefiend** | Passive summon | — | passive/talent | Talent that summons a **Vilefiend** demon for the rotation/Tyrant board (passive node in the S1 tree). |
| **Summon Doomguard** | Rotational-summon / cooldown | Soul Shards | active talent | Summons a **Doomguard** demon (deep spec-tree talent). @verify-ingame |
| **Summon Felguard** | Pet | 1 Soul Shard | ~cast, out of combat | Summons the **Felguard**, Demonology's permanent pet (universal in group content). Provides **Axe Toss** interrupt via Command Demon. |
| **Command Demon / Axe Toss** | Interrupt | — | ~30s CD (Felguard) | *Command Demon* fires the active pet's special. With the Felguard that's **Axe Toss** — a ranged interrupt + brief stun. |
| **Spell Lock** | Interrupt / Dispel | — | ~24s CD (Felhunter) | Felhunter's Command Demon ability — interrupt + a purge. Available when running the Felhunter instead of the Felguard. |
| **Doom** | Passive | — | passive talent | Demonbolt applies **Doom**, a delayed detonation on the target. Build-defining passive, not a pressed button. |
| **Fel Domination** | Utility (pet) | — | ~3-min CD | Your next pet summon within 15s is **instant and free** — the emergency re-summon after a pet dies. |
| **Subjugate Demon** | CC (utility) | — | ~1.5s cast | Enslaves a target demon to fight for you (leveling / niche PvE utility). |
| **Drain Life** | Defensive (self-heal) | — | channel | Channels damage that **heals you** — the low-cost sustain heal; often macro'd with `/cancelaura Burning Rush`. |
| **Mortal Coil** | Defensive / CC | — | ~45s CD | Horrifies the target (~3s) and **heals ~20–25% max HP**. A defensive + single-target peel. |
| **Dark Pact** | Defensive (absorb) | Sacrifices current HP | ~1-min CD (−15s w/ *Frequent Donor*) | Sacrifices health for a large **absorb shield**; usable while CC'd. |
| **Unending Resolve** | Defensive (major) | — | ~3-min CD | **−25% damage taken** for 8s (−40% with *Strength of Will*) + interrupt/silence immunity — the big personal defensive. |
| **Healthstone** | Defensive (item) | — | instant, 1/combat (reusable w/ *Pact of Gluttony*) | Instant **~25–30% HP** heal; conjured pre-combat. |
| **Soulstone** | Utility (battle-rez) | — | ~2.5s cast · 10-min CD | Combat resurrection on an ally (self-rez out of combat) — the warlock brez. |
| **Soulburn** | Utility (empower) | 1 Soul Shard | instant | Empowers the **next** spell (e.g. Healthstone/Drain Life/Demonic Circle) with a bonus effect. |
| **Demonic Circle** | Movement (utility) | — | ~0.5s cast | Places a portal on the ground. |
| **Demonic Circle: Teleport** | Movement | — | instant | Teleports back to your placed Demonic Circle (kiting / mechanic dodge). |
| **Demonic Gateway** | Movement (utility) | — | ~2s cast | Places a two-way gateway allies can use to skip terrain — group mobility/skips. |
| **Burning Rush** | Movement | Drains health over time | toggle | +50% run speed at the cost of health-per-second; toggle off with `/cancelaura`. |
| **Shadowfury** | CC (AoE) | — | ~30s CD | Ground-targeted **AoE stun** — the spec's main trash-pack stun. Choice-node vs *Howl of Terror*. |
| **Howl of Terror** | CC (AoE) | — | ~40s CD | AoE **fear** around you (choice-node vs Shadowfury); Diabolist can grant a stronger 10-target version. |
| **Fear** | CC (single) | — | ~1.5s cast | Single-target fear. |
| **Banish** | CC (single) | — | ~1.5s cast | Banishes a Demon/Elemental, removing it from combat temporarily. |
| **Curse of Tongues** | Utility (debuff) | — | ~1.5s cast | Slows the target's cast speed. |
| **Curse of Weakness** | Utility (debuff) | — | instant | Reduces the target's physical damage. |
| **Curse of Exhaustion** | Utility (slow) | — | instant | Reduces the target's movement speed (kite tool). |
| **Blight of Weakness** | Utility (debuff) | — | instant | Talent upgrade to Curse of Weakness (choice-node vs *Blight of Tongues*); adds a lingering effect. |
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
- Not on the current Midnight Demo spec tree (present in older builds, omitted
  here): **Bilescourge Bombers, Nether Portal, Demonic Strength, Guillotine** —
  none appear in the 12.0.7.67808 talent tree (`talents.md`). @verify-ingame
