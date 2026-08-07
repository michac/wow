---
title: Frost Mage — Ability Inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/mage/frost/ability-inventory.tsv  # tier 1 — wago DB2 pinned @ build 12.0.7.67808; the name/spellID/origin/cooldown floor, 2026-08-06
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived — the per-row verdicts applied to this file, 2026-08-06
  - knowledge/classes/_abilities/pet-family-annex.tsv  # tier 1 derived — pet skill lines (Water Elemental Freeze), 2026-08-06
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Mage_Frost.simc  # tier 1 APL, 2026-07-11
  - https://www.method.gg/guides/frost-mage/playstyle-and-rotation  # tier 3, 12.0.7, 2026-07-11
  - https://www.icy-veins.com/wow/frost-mage-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - raw/wago/SpellName.csv  # tier 1 game-data name reconcile, 2026-07-11
confidence: high
---

# Frost Mage — Ability Inventory (Midnight S1)

## Overview

- **Hero trees:** `builds.md` owns the pick. In kit terms: **Spellslinger** adds
  **Splinter** procs and **Splinterstorm**, plus Frozen Orb / Ray of Frost
  cooldown reduction; **Frostfire** turns Frostbolt and Flurry into Frostfire
  spells and makes **Glacial Spike!** explode on impact.
- **Resource:** **Mana** (rarely a constraint), plus four rotational
  proc/charge systems: **Freezing stacks** (the Midnight replacement for the old
  Winter's Chill debuff — applied to the target by Flurry/Ice Lance/Frozen Orb/
  Ray of Frost/Glacial Spike, capped at 20, consumed by Ice Lance & Comet Storm to
  trigger **Shatter** AoE damage scaled to stacks consumed), **Fingers of Frost**
  (proc → instant, max-Shatter Ice Lance), **Brain Freeze** (proc → instant Flurry),
  and **Icicles** (Frostbolt builds them; 5 Icicles enable/empower Glacial Spike).
- **Playstyle:** smash cooldowns (Frozen Orb, Ray of Frost / Comet Storm, Glacial
  Spike!) on cooldown, then spend Freezing stacks with Ice Lance and rebuild with
  Frostbolt. A proc-reactive caster, not a fixed loop.

> **Midnight rework note:** the old **Winter's Chill** debuff is now **Freezing**
> (stacking to 20). **Glacial Spike!** and **Comet Storm** are now core-build
> buttons. **Frostfire Bolt** (Frostfire hero) and **Splinterstorm** (Spellslinger
> hero) are new hero-tree spells. **Icy Veins is gone** — see "Not on the Midnight
> Frost tree" below; a Midnight Frost bar has no Icy Veins button on it.
>
> ⚠ A previous revision of this file justified several rows by "the name resolves in
> `SpellName.csv`". That is not evidence a spec can cast something — `SpellName` keeps
> retired spells indefinitely. Only an **acquisition** table (trait node,
> SkillLineAbility, SpecializationSpells, PvpTalent) settles it, which is what
> `ability-inventory.tsv` is built from.

## Inventory

> **Tier-1 floor.** `ability-inventory.tsv` beside this file is authoritative for
> name, spellID, origin and cooldown; where it and the prose below disagree, it
> wins. What is here is the judgement layer — function, role, rotational context.
> Notation (`[T1]` vs `~`), the charge-cooldown caveat and the section-3/4
> pointers: **`../../_abilities/prose-conventions.md`**.

| Ability | Function | Resource | Cast / CD | Description |
|---|---|---|---|---|
| **Frostbolt** | Rotational-builder | Mana | ~2s cast | Core filler. Builds Icicles + Fingers of Frost chance; applies a slow. Replaced by **Frostfire Bolt** under the Frostfire hero tree. |
| **Frostfire Bolt** | Rotational-builder | Mana | ~2s cast | Frostfire hero-tree builder (spell 51779) that replaces Frostbolt; deals Frost+Fire and builds Frostfire empowerment. |
| **Ice Lance** | Rotational-spender | Mana | Instant | Primary Freezing spender; instant when Fingers of Frost is up (deals max-Shatter damage regardless of stacks). Consumes Freezing stacks → Shatter. |
| **Flurry** | Rotational-builder | Mana | ~1.5s cast (instant w/ Brain Freeze) | Applies Freezing stacks; instant + off-cooldown when Brain Freeze procs. (Older revisions said "held while the Thermal Void window is active" — Thermal Void is still a live passive but what it now extends is unmeasured; see the note below. Do not hold Flurry on that basis until it is confirmed.) |
| **Glacial Spike!** | Rotational-spender | Mana | ~2.5s cast | Available at 5 Icicles; big nuke that applies Freezing. Explodes on impact / cleaves under the right talents. Press when charged. **The trailing `!` is part of the real spell name** — a plain "Glacial Spike" matches no acquirable spell, which matters for macros, WeakAuras and anything doing a name lookup. Its only DB2 attachment is a Cooldown-Manager set entry, so the tsv lists it `cdm-only`; it is castable. |
| **Frozen Orb** | Major cooldown | Mana | **60s** `[T1]` | Bouncing AoE bolt-storm (~15s), grants Fingers of Frost + Freezing; core burst button pressed on CD. Spellslinger: feeds Splinters and reduces Ray of Frost CD. |
| **Comet Storm** | Major cooldown | Mana | ~30s CD (talent) | Burst AoE that consumes Freezing stacks; Frostfire's primary channel-follow burst and a high-priority button for both hero trees. |
| **Ray of Frost** | Major cooldown | Mana | ~4s channel, 60s CD | Hard-hitting channel that stacks Freezing; **2 charges** with the Hand of Frost apex. Sync with potion/Bloodlust. Frostfire may transform it into Comet Storm. |
| **Blizzard** | Rotational-spender (AoE) | Mana | Channel / ground-target / **12s** `[T1]` | AoE ground effect; strongly favored when the **Freezing Rain** buff is up (instant, buffed). Core AoE button at 3+ targets. |
| **Cone of Cold** | Rotational-spender (AoE) | Mana | Instant, 25s [T1] | Frontal AoE + slow; an AoE filler with the Cone of Frost talent. **Class-baseline**, not a talent. Roughly double the cooldown the older prose claimed — at 25s it is not a filler you weave, it is a button you spend. |
| **Ice Nova** | CC / AoE | Mana | Instant, charges (talent) | AoE nova: damage + root; also an AoE filler with the right talents. |
| **Arcane Explosion** | Rotational-spender (AoE) | Mana | Instant | Baseline PBAoE; largely off-meta for Frost (Blizzard/Cone preferred) but available. |
| **Frozen Orb / Splinters** | Passive (Spellslinger) | — | — | Spellslinger Splinter procs fire off casts, add cleave, and reduce Frozen Orb / Ray of Frost cooldowns. |
| **Splinterstorm** | Passive (Spellslinger) | — | — | Spellslinger capstone (spell 443783): pooled Splinters release as a burst-damage storm. |
| **Hand of Frost** | Rotational-spender / Passive | Mana | (apex spec talent) | Apex talent (spell 102593) granting a **2nd Ray of Frost charge** and triggering damage during its cast — pooling flexibility for burst. |
| **Thermal Void** | Passive | — | — | Live on the Frost tree. **What it extends is unknown** — it used to extend Icy Veins, and Icy Veins no longer exists. Answering this needs the spell-effect tables, which cannot currently be read at a pinned build, so it is deliberately left unstated rather than guessed. @verify-ingame |
| **Counterspell** | Interrupt | Mana | Instant / **25s** `[T1]` | Spell-school lockout interrupt. |
| **Frost Nova** | CC | Mana | Instant, charges | Roots all nearby enemies; a Freezing/Shatter setup and kite tool. |
| **Freeze** | CC — **pet ability** | Mana | Instant, ~25s CD | AoE root for Shatter/kite setup. It belongs to the **Water Elemental**, not to you: it lives on the pet's own skill line, so it exists only while the elemental is out (i.e. with *Summon Water Elemental* over *Lonely Winter*). That is why it does not appear in this spec's inventory tsv — per-spec inventories carry player spells. |
| **Polymorph** | CC | Mana | ~1.5s cast | Single-target sheep; soft CC / crowd control. |
| **Mass Polymorph** | CC | Mana | Cast (talent) / **60s** `[T1]` | AoE Polymorph (spell 29963); talent choice. |
| **Ring of Frost** | CC | Mana | Cast / ground (talent) / **45s** `[T1]` | AoE hold/CC field; talent choice vs Mass Polymorph. |
| **Dragon's Breath / Supernova** | CC | Mana | Instant (class talent choice) | Dragon's Breath = frontal disorient; Supernova = AoE knock-up/damage. Choice node. |
| **Spellsteal** | Dispel / Utility | Mana | ~1.5s cast | Steals a beneficial magic buff from an enemy. |
| **Remove Curse** | Dispel | Mana | Instant | Removes a Curse from a friendly target. |
| **Ice Barrier** | Defensive | Mana | Instant, ~30s CD (25 talented) | Frost damage-absorb shield. |
| **Ice Block** | Defensive | Mana | Instant, ~3min CD | Full immunity + clears most debuffs; **Ice Cold** talent trades immunity for heavy damage reduction while still casting. |
| **Cold Snap** | Defensive / Utility | Mana | ~5min CD | Resets Ice Block / Ice Barrier / Frost Nova (and related defensive) cooldowns. |
| **Greater Invisibility** | Defensive | Mana | Instant, ~2min CD | Invisibility + damage reduction + threat drop. |
| **Mirror Image** | Defensive / Major cooldown | Mana | Instant, ~2min CD | Summons 3 images that cast and split threat; adds damage and a survivability buffer. |
| **Alter Time** | Utility / Defensive | Mana | Instant / **60s** `[T1]` | Snapshots position + health, returns you to them within the window — escape / heal-undo tool. |
| **Blink / Shimmer** | Movement | Mana | Instant, charges | Blink teleport (~20yd). **Blink is class-baseline** — you always have a blink; the **Shimmer** talent is what swaps it for a 2-charge, off-GCD, cast-while-casting version. |
| **Time Warp** | Utility (Bloodlust) | Mana | Instant, ~5min CD | Raid Bloodlust/Heroism-equivalent 30% haste. |
| **Arcane Intellect** | Utility (raid buff) | Mana | Cast | +Intellect raid buff; cast pre-combat. |
| **Mass Invisibility** | Utility | Mana | Cast (talent) / **300s** `[T1]` | Group invisibility (spell 198158); skip/reset utility. |
| **Slow Fall** | Utility | Mana | Instant | Slows a target's fall. |
| **Summon Water Elemental** | Pet | Mana | Instant (talent) / **15s** `[T1]` | Summons the Water Elemental pet (choice vs Lonely Winter); provides **Freeze** and passive damage. |

## Not on the Midnight Frost tree

### Belongs to another spec

- **Prismatic Barrier** — Mage / **Arcane**. Its node on the live Mage tree is gated to
  Arcane alone. The class barrier node is one node with three spec-specific spells —
  Arcane gets Prismatic Barrier, Fire gets **Blazing Barrier**, Frost gets **Ice
  Barrier** (listed above) — which is exactly what makes the wrong one look plausible in
  a Frost list. Frost has **one** barrier and it is Ice Barrier.

### Not acquirable at 12.0.7

- **Icy Veins** — gone. None of its spell IDs attaches to a trait node,
  SkillLineAbility, SpecializationSpells or PvpTalent entry, and the Mage tree carries no
  Icy Veins node. The old row's own hedge — "the simc `cds` list does not explicitly cast
  it" — was right for the right reason. Frost's cooldown-band castables are Frozen Orb,
  Cold Snap, Ray of Frost, Comet Storm, Splinterstorm, Alter Time and Mirror Image; there
  is no haste burst among them, which is a real change to how the spec ramps.
  **Thermal Void survives the spell it used to extend** — it is still on the tree, and
  what it now does is genuinely unresolved (see its row above). Do not assume it silently
  moved onto Frozen Orb or Ray of Frost; that would be a guess.
- **Shifting Power** — not acquirable by any Mage spec. Its only attachment is a
  SkillLineAbility row on the dead Shadowlands *Night Fae* covenant line, which is not a
  live acquisition path, and there is no node for it on the Mage tree. The Mythic+
  cooldown-cycling tool it used to provide simply is not in the Midnight kit.
- **Ice Floes** and **Mass Barrier** — appear on no class, spec or hero tree for any
  spec. (Mass Barrier still shows up in this spec's inventory tsv as `cdm-only`: that is
  a Cooldown-Manager set entry, **not** an acquisition row, and does not mean Frost can
  cast it.)

*[Tier 1: DB2 @ 12.0.7.67808 — `all-talents.tsv` across all 40 specs, plus
SkillLineAbility / SpecializationSpells / PvpTalent; `_abilities/reconcile-ledger.md`.]*
