---
title: Destruction Warlock — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Warlock_Destruction.simc  # tier 1, simc midnight APL, 2026-07-11
  - raw/wago/SpellName.csv @ 12.0.7  # tier 1 game-data name reconciliation, 2026-07-11
  - https://www.method.gg/guides/destruction-warlock  # tier 3, upd. 2026-06-16, 2026-07-11
  - https://www.method.gg/guides/destruction-warlock/playstyle-and-rotation  # tier 3, 2026-07-11
confidence: high
---

# Destruction Warlock — Abilities (Midnight S1)

## Overview

- **Resource:** **Soul Shards** (0–5, tracked internally in tenths / "fragments").
  Builders — Incinerate, Conflagrate, Soul Fire, Immolate ticks — generate
  fragments; spenders — **Chaos Bolt** (2 shards), **Rain of Fire** (3),
  **Shadowburn** (1) — consume whole shards. The whole spec is a shard economy:
  never overcap, always be casting.
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

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| Incinerate | Rotational-builder | — | 2s cast | Core filler; generates a Soul Shard fragment (more with Diabolic Embers / Fire and Brimstone in AoE). |
| Conflagrate | Rotational-builder | — | Instant · 2 charges, ~13s recharge | Instant fire nuke, generates a fragment, grants **Backdraft** (faster Incinerate/Chaos Bolt casts). Mobile filler. |
| Immolate | Rotational-builder (DoT) | — | 1.5s cast · DoT | Fire DoT you keep up; its ticks generate shard fragments and can proc Conflagrate resets. Diabolist maintenance DoT. |
| Wither | Rotational-builder (DoT) | — | 1.5s cast · DoT | **Hellcaller** replacement for Immolate — stacking fire/shadow DoT that Malevolence detonates/empowers. Midnight-new hero DoT. @verify-ingame |
| Chaos Bolt | Rotational-spender | 2 Soul Shards | ~2.5s cast | Primary spender and the bulk of single-target damage; benefits from crit scaling (Chaos Incarnate / Ruin). |
| Rain of Fire | Rotational-spender (AoE) | 3 Soul Shards | Channeled AoE | Ground-target AoE spender; the shard dump at high target counts (Hellcaller sooner, Diabolist only at ~8+). |
| Shadowburn | Rotational-spender / Execute | 1 Soul Shard | Instant · 2 charges, ~12s recharge | Instant spender, extra value sub-20% (execute) and with Fiendish Cruelty; refunds resources / shard on a kill. |
| Soul Fire | Rotational-builder | — | ~4s cast · ~45s CD (charge-like) | Hard-cast that applies/refreshes Immolate and generates multiple shard fragments; best consumed with Backdraft. |
| Cataclysm | Rotational-builder (AoE) | — | Instant · ~30s CD | Ground AoE that applies Immolate to all targets hit and deals burst damage; strong opener + AoE setup. |
| Channel Demonfire | Rotational-spender | — | Channeled · ~25s CD | Launches bolts at all targets with Immolate/Wither; choice-node vs Demonfire Infusion. Talent. |
| Infernal Bolt | Rotational-builder | — | ~2s cast | **Diabolist** Incinerate replacement that generates **more** shards; appears in the APL as a shard-refill button when low. Midnight-new. @verify-ingame |
| Ruination | Rotational-spender (proc) | — | Instant (granted) | **Diabolist** free empowered nuke granted by cycling Diabolic Ritual → Demonic Art; press on proc. Midnight-new. @verify-ingame |
| Embers of Nihilam | Rotational-spender / Apex | — | Active (talent) | Spec apex active (talent tree row 12). Situational burst button when talented. @verify-ingame |
| Havoc | Utility (cleave) | — | Instant · ~30s CD | Marks a second target; single-target spells (Chaos Bolt, Shadowburn, etc.) are duplicated onto it. The 2-target cleave button. |
| Summon Infernal | Major cooldown | — | Instant · 90s CD (60s w/ Inferno), 30s duration | Meteor + persistent infernal; the primary DPS burst window everything (potion/trinkets/racials) syncs to. |
| Malevolence | Major cooldown | — | ~60s CD | **Hellcaller** burst CD — grants haste and empowers/extends active Withers. Hellcaller-exclusive. Midnight-new. @verify-ingame |
| Curse of Exhaustion | Utility (slow) | — | Instant | Reduces target movement speed. Curse. |
| Curse of Tongues | Utility (slow-cast) | — | Instant | Slows enemy cast speed. Curse. |
| Curse of Weakness | Utility (debuff) | — | Instant | Reduces target physical damage. Curse. |
| Blight of Weakness | Utility (debuff) | — | Instant (talent) | **Hellcaller** curse upgrade (choice with Blight of Tongues) — the spreading/empowered version of Curse of Weakness. |
| Drain Life | Defensive (self-heal) | — | Channeled | Channel that damages and heals you; the core sustain filler when low. |
| Mortal Coil | CC / Defensive | — | Instant · 45s CD | Horrifies the target (~3s) and heals you 20–25% max HP. Talent. |
| Shadowfury | CC (AoE stun) | — | Instant · ~30s CD | AoE stun at a ground location. Choice node with Howl of Terror. |
| Fear | CC | — | 1.5s cast | Single-target fear; breaks on damage. |
| Howl of Terror | CC (AoE) | — | Instant · CD (talent) | AoE fear around you; choice node with Shadowfury. |
| Banish | CC | — | 1.5s cast | Incapacitates a Demon or Elemental. Talent. |
| Spell Lock | Interrupt | — | Pet ability · 24s CD | **Felhunter** pet interrupt + purge; Destruction's interrupt comes from the pet, not the player. |
| Subjugate Demon | Utility (enslave) | — | 3s cast | Takes control of a target demon. |
| Fel Domination | Pet | — | Instant · long CD | Next pet summon is instant + free — emergency re-summon. |
| Summon Pet (Imp / Voidwalker / Felhunter / Sayaad) | Pet | — | Cast | Your permanent pet; pick by utility (Felhunter interrupt/purge, Voidwalker tank, Imp dispel, Sayaad CC). Felguard is Demonology-only — not available to Destruction. |
| Health Funnel | Pet (utility) | — | Channeled | Heals your pet from your health. |
| Soulstone | Utility (battle rez) | — | 3s cast · long CD | Combat resurrection; can be pre-applied for a self-rez. |
| Healthstone / Create Healthstone | Defensive (item) | — | Instant use | Instant heal (~25–30% HP); create out of combat, or reusable in combat with Pact of Gluttony. |
| Create Soulwell | Utility | — | Cast | Places a well for the group to grab Healthstones. |
| Soulburn | Utility (empower) | 1 Soul Shard | Instant · ~30s CD | Empowers your next specific spell (e.g. Soul Fire / Demonic Circle / Healthstone). Talent. |
| Dark Pact | Defensive (absorb) | — | Instant · ~60s CD | Sacrifices health for a large shield; usable while CC'd. Talent. |
| Unending Resolve | Defensive | — | Instant · ~3min CD | −25% damage taken (−40% with Strength of Will) + interrupt/silence immunity, 8s. |
| Burning Rush | Movement | — | Toggle | +50% run speed at the cost of health-over-time; the main mobility toggle. |
| Demonic Circle | Movement (utility) | — | Cast to place | Drops a portal; **Demonic Circle: Teleport** returns you to it. Talent. |
| Demonic Circle: Teleport | Movement | — | Instant | Teleport to your placed Demonic Circle (also breaks roots). |
| Demonic Gateway | Movement (utility) | — | Cast · ~10s | Places a linked portal pair; players click to travel between them. Talent. |
| Grimoire of Sacrifice | Utility (passive buff) | — | Instant (talent) | Sacrifices your pet for a personal damage buff + a proc (choice with Summoner's Embrace). |
| Command Demon / pet-specific | Utility | — | Instant | Contextual pet command (Spell Lock, Seduction, Shadow Bulwark, etc. depending on active pet). |

> **Interrupt note:** Destruction has **no baseline personal interrupt**. Kicks
> come from the **Felhunter's Spell Lock** (or CC via Sayaad's Seduction /
> Shadowfury / Howl of Terror / Mortal Coil). This matters for interrupt
> assignments.

> **Seed reconciliation:** the spec seed listed **Summon Felguard** — that is a
> **Demonology** pet and is **not** available to Destruction; corrected above.
> **Curse of Weakness** exists baseline; the Hellcaller talent line is
> **Blight of Weakness / Blight of Tongues** (choice). Names verified vs
> `raw/wago/SpellName.csv` @ 12.0.7.
