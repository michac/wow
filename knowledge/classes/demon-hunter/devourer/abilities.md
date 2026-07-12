---
title: Demon Hunter Devourer — Abilities (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - https://www.method.gg/guides/devourer-demon-hunter/playstyle-and-rotation  # tier 3, upd. 2026-06-17, 2026-07-11
  - https://www.icy-veins.com/wow/devourer-demon-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - https://conquestcapped.com/guides/wow/devourer-demon-hunter-overview/  # tier 4 corroboration, 2026-07-11
  - https://github.com/simulationcraft/simc/tree/midnight/profiles/MID1  # tier 1, MID1_Demon_Hunter_Devourer.simc, 2026-07-11
  - raw/wago/SpellName.csv @ 12.0.7.67808  # tier 1, name canonicalization, 2026-07-11
confidence: medium
---

# Demon Hunter Devourer — Abilities (Midnight S1)

Devourer is the **Midnight-new 4th Demon Hunter specialization** — a **mid-range
(~25 yd, Evoker-like) Void caster** that keeps the class's mobility toolkit but
"plants" for its key casts. It is a DPS spec, not a tank.

**Resource system — two interlocking resources:**
- **Fury** — the standard DH primary resource. **Consume** and other builders
  generate it; **Void Ray** (the main spender) costs **100 Fury** outside
  transform.
- **Soul Fragments ("Souls")** — a secondary economy unique to how Devourer
  plays. Abilities generate Souls; Souls in turn generate Fury (Consume: +4 Fury
  per Soul), boost damage via **Feast of Souls**, and — most importantly —
  accumulate to **50** (35 with *Soul Glutton*) to unlock **Void Metamorphosis**.

**Playstyle in one line:** build Fury + Souls outside of transform, bank to
**50 Souls**, pop **Void Metamorphosis**, then dump Souls into **Collapsing
Star** and empowered casts before Fury drains and the form ends. The whole spec
is built around maximizing damage inside those Void Metamorphosis windows.

**Hero trees:** **Annihilator** (the S1 default everywhere — a caster-leaning
build that ramps *Voidfall* stacks to call down Void Meteors and barely does
damage outside Meta) and **Void-Scarred** (Void Metamorphosis-centric; a
single-target-competitive caster variant and a melee-hybrid variant using The
Hunt / Hungering Slash). See `builds.md`.

> ⚠ Brand-new spec with no Warcraft Logs history distilled yet; several exact
> numbers (charges, cooldowns, Fury/Soul values) come from Tier-3 guides and are
> marked `@verify-ingame`. Names are canonicalized against Tier-1 game data
> (`SpellName.csv` / the talent tree in `talents.md`).

## Ability inventory

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Consume** | Rotational-builder | Generates Fury + 1 Soul (+4 Fury/Soul) | ~2s cast, castable while moving | Primary filler outside transform. Becomes **Devour** inside Void Metamorphosis (collectible while moving). @verify-ingame exact Fury/Soul yield |
| **Void Ray** | Rotational-spender | 100 Fury (free inside Meta) | 3s channel (haste-reduced), roots you | The main spender and a huge chunk of Devourer's damage + Soul generation. Outside Meta: no CD, costs 100 Fury. Inside Meta: no Fury cost but ~16s CD (14s talented). Fully channeling it resets **Reap** and can turn Reap into **Eradicate**. @verify-ingame CD inside Meta |
| **Reap** | Rotational-builder | Pulls up to 4 Souls; generates Fury (*Scythe's Embrace*) | Instant, 8s CD | Instant ranged Cosmic damage; collects up to 4 Soul Fragments. CD resets on a full Void Ray channel. Becomes **Cull** inside Void Metamorphosis. *Eradicate* talent makes it an AoE frontal cone (primary AoE tool). |
| **Soul Immolation** | Rotational-builder / maintenance | Generates 3 Souls + 30 Fury over 5s | ~1 min CD | On-demand Soul/Fury bump aura; also has a heal/dispel use. Maintain it (kept up outside Meta; refreshed as a resource pump). @verify-ingame CD/values |
| **Void Metamorphosis** | Major cooldown | Requires 50 Souls (35 w/ *Soul Glutton*); Fury drains while active | Fragment-gated (no fixed timer) | The defining transform and burst window. Consumes banked Souls to activate, sharply raises damage, unlocks **Collapsing Star**, and upgrades core abilities (Reap→Cull, Consume→Devour, Voidblade→Pierce the Veil). Fury drains rapidly until it ends. |
| **Collapsing Star** | Rotational-spender (Meta only) | 30 Souls | Meta-only | Massive Cosmic-damage Soul spender available only inside Void Metamorphosis; **always crits** (via the *Midnight* capstone) and each cast within the window hits harder. The core in-Meta payoff button. |
| **Midnight** | Passive/empowerment capstone | — | — | Spec capstone (spell 1242486) that enables/empowers **Collapsing Star** (first rank = always crits). @verify-ingame exact effect |
| **Cull** | Rotational-builder (Meta form of Reap) | Up to 4 Souls | Meta-only; CD reduced per Devour cast | Enhanced Reap while transformed; buffed by *Student of Suffering*. Consumes/collects Souls for damage. |
| **Devour** | Rotational-builder (Meta form of Consume) | Fury + Souls | Meta-only, castable while moving | Consume's transformed version — soul-collecting filler used inside Void Metamorphosis. |
| **Eradicate** | Rotational-spender / AoE | Souls + Fury | Talent; replaces Reap after a full Void Ray channel | AoE frontal cone; a large portion of Devourer's multi-target damage (*Eradicate* talent). |
| **Voidblade** | Rotational-builder / Movement | Generates Fury | 30s CD, charges to target | Melee charge that generates Fury; enables melee-hybrid builds. Follows into **Hungering Slash** (talent) or **Pierce the Veil** (Void-Scarred, inside Meta). *Devourer's Bite* makes it a 12%/stack damage amp. |
| **Hungering Slash** | Rotational-builder (talent) | Generates Fury; shatters up to 2 Soul Fragments | Talent | Converts Voidblade/The Hunt into melee slashes; core of the Void-Scarred melee hybrid. |
| **Pierce the Veil** | Rotational-spender (Void-Scarred, Meta) | — | Meta-only | Void-Scarred's empowered Voidblade; first cast per window triggers **Voidsurge**. @verify-ingame |
| **The Hunt** | Major cooldown / Movement | — | 90s CD | Class charge that dashes to a target and applies a DoT; opener + burst tool, heavier in Void-Scarred melee builds. |
| **Void Nova** | CC | — | 45s CD, 30 yd, AoE | Midnight-new class talent (spell 1234195): stuns your target and nearby enemies for 3s. @verify-ingame |
| **Disrupt** | Interrupt | — | 15s CD, 30 yd | Baseline ranged interrupt. |
| **Consume Magic** | Dispel / Utility | — | class talent | Offensive dispel — removes a beneficial magic effect from an enemy (and can generate resources per DH design). |
| **Imprison** | CC | — | class talent | Incapacitate a target (demon/beast/humanoid/dragonkin) — long-duration crowd control. |
| **Sigil of Misery** | CC | — | class talent | Places a sigil that disorients/fears enemies in the area after a short delay. |
| **Torment** | Utility (taunt) | — | — | Single-target taunt (DH baseline) — off-tank/soak utility for DPS. |
| **Spectral Sight** | Utility | — | — | Reveals hidden/stealthed enemies; see through walls briefly (DH baseline). |
| **Throw Glaive** | Utility / ranged | — | short CD/charges | Ranged thrown glaive — minor damage + range/utility (e.g. bouncing with *Bouncing Glaives*). |
| **Vengeful Retreat** | Movement / Defensive | — | ~25s CD | Backward evasive leap; primarily a safety reposition, buffed by *Voidstep* in melee builds. |
| **Shift** | Movement | — | 20s CD, 30 yd (to cursor) | **Midnight-new Devourer movement** — near-instant teleport toward your cursor within 30 yd (Devourer's replacement for Fel Rush). Baseline 1 charge; some guides cite up to 3 charges via talents. @verify-ingame charge count |
| **Blur** | Defensive | — | 1 min CD, 10s | 25% damage reduction + dodge; a second charge is available via talent. Core personal defensive. |
| **Darkness** | Defensive (raid/group) | — | class talent | Places a zone granting allies a chance to avoid incoming damage; proc-based value (stronger vs repeated damage events). |
| **Soul Rending** | Passive (defensive) | — | passive | Leech/self-healing, boosted while transformed and when consuming Souls. |
| **Demonic Wards** | Passive (defensive) | — | passive | Always-on magic damage reduction (Devourer's baseline mitigation). |
| **Feast of Souls** | Passive (offensive) | — | passive | Soul Fragments increase your damage done — part of why banking Souls matters. |
| **Voidfall** | Passive (mechanic) | — | passive | Annihilator mechanic: consuming stacks with Reap/Eradicate calls down Void Meteors (via *Meteoric Fall*). Build to 3 stacks then spend. |
