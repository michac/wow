---
title: Hunter Beast Mastery — ability inventory (Midnight S1)
patch: 12.0.7
fetched: 2026-08-06
reviewed: 2026-08-06
sources:
  - knowledge/classes/hunter/beast-mastery/ability-inventory.tsv  # tier 1 — wago DB2 pinned @ build 12.0.7.67808; the name/spellID/origin/cooldown floor, 2026-08-06
  - knowledge/classes/_abilities/reconcile-ledger.md  # tier 1 derived — the per-row verdicts applied to this file, 2026-08-06
  - knowledge/classes/_abilities/section-3-corroborated.tsv  # tier 1 — Primal Rage 264667, GET /data/wow/spell/264667 → 200, 2026-08-06
  - simc midnight branch profiles/MID1/MID1_Hunter_Beast_Mastery.simc  # tier 1 APL + talent string, WoW 12.0.x
  - https://www.method.gg/guides/beast-mastery-hunter/playstyle-and-rotation  # tier 3, 12.0.7
  - https://www.icy-veins.com/wow/beast-mastery-hunter-pve-dps-rotation-cooldowns-abilities  # tier 3, 12.0.7
  - raw/wago/SpellName.csv  # tier 1, name reconcile @ 12.0.7.67808
confidence: medium
---

# Beast Mastery Hunter — abilities (Midnight S1, 12.0.7)

## Overview

Beast Mastery is a **ranged physical** spec whose damage is delivered mostly
by the **pet(s)**, which means every ability is instant and castable while
moving — the spec's signature. Resource is **Focus** (0–100, passive regen),
generated chiefly by **Barbed Shot** (instant chunk via Pack Tactics) and
spent on **Kill Command** and the **Cobra Shot** filler. The core loop is a
two-charge juggle: never cap **Kill Command** or **Barbed Shot** charges, keep
the pet's **Frenzy** stacks rolling with Barbed Shot, and pour everything else
into Cobra Shot, all funnelled into the **Bestial Wrath** burst window every
30s.

Two hero trees in S1:
- **Pack Leader** — builds and spends **Howl of the Pack Leader** to summon a
  rotating cast of empowered beasts (Wyvern / Boar / Bear) plus a **Stampede**
  line on the first Kill Command inside Bestial Wrath. The default / recommended
  tree for both single-target and AoE.
- **Dark Ranger** — adds **Black Arrow** (a Deathblow-triggering shadow
  attack) and **Wailing Arrow**, with a **Withering Fire** burst window. An
  alternative single-target line.

> **Interrupt note (settled).** The seed listed *Muzzle*. Muzzle is gated to
> **Survival** and is not on the Beast Mastery tree at all; BM's interrupt is
> **Counter Shot**, and it is the only one. See "Not on the Midnight Beast Mastery
> tree" below. *[Tier 1: `ability-inventory.tsv` / DB2 @ 12.0.7.67808.]*

## Inventory

> **Tier-1 floor.** `ability-inventory.tsv` in this folder — generated from wago DB2
> pinned to build `12.0.7.67808` — is authoritative for **name, spellID, origin and
> cooldown**, and wins wherever it and the prose below disagree. Cooldowns tagged
> `[T1]` were read off it this pass; a `~` value is prose that has **not** been
> measured. Spell IDs are deliberately *not* restated row-by-row here — the tsv
> carries them and will not drift. This table is for **function, role and rotational
> context**.

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
| Barbed Shot | Rotational-builder | Generates ~25 Focus (Pack Tactics) | Instant · 2 charges, ~12s recharge | Applies/refreshes a bleed and stacks the pet's **Frenzy** (attack-speed buff). The spec's Focus engine and Frenzy-uptime button; never let charges cap. In Midnight it functions as a rolling DoT that stacks rather than resetting. @verify-ingame (recharge/Focus exact) |
| Kill Command | Rotational-spender | 30 Focus | Instant · 2 charges (Alpha Predator), ~7.5s recharge | Commands the pet to savage the target — the primary spender and hardest hit. Empowered when **Nature's Ally** or **Howl of the Pack Leader** is up. Killer Cobra / Killer Instinct interactions in-tree. |
| Cobra Shot | Rotational-builder/filler | 35 Focus | Instant | Focus-dump filler between Kill Command and Barbed Shot; reduces Kill Command's cooldown (strongly with **Killer Cobra** during Bestial Wrath). Decrements the Howl of the Pack Leader timer. @verify-ingame (Focus cost) |
| Wild Thrash | Rotational-spender (AoE) | Focus @verify-ingame (cost) | Instant · 8s [T1] | Midnight's primary AoE ability — **replaces Multi-Shot**. Enables/maintains **Beast Cleave** so the pet's Kill Commands hit all nearby enemies. At an 8-second cooldown it is a *maintenance* button, not a burst one: press it whenever 2+ targets are up, even briefly. |
| Bestial Wrath | Major cooldown | No cost | Instant / 30s CD / **90s** `[T1]` | The core burst window: **+20% damage** (Midnight redesign, down from 30%) plus an upfront burst on activation. Triggers the capstones of **both** hero trees — Pack Leader's Howl summon + Stampede, Dark Ranger's Withering Fire. Dump Barbed Shot charges before pressing. |
| Bloodshed | Passive | — | — | In the Midnight tree Bloodshed is a **passive** pet-damage talent (not the old active button). |
| Dire Beast | Passive | — | — | Passively summons a short-lived beast to attack (procs off rotation). Pack Leader summons flavoured variants (**Dire Beast: Hawk** etc.). |
| Nature's Ally | Rotational-empower (active) | — | Instant · CD | Spec capstone active that grants the **Nature's Ally** buff, empowering the next Kill Command(s). @verify-ingame (exact effect) |
| Black Arrow | Rotational-spender (Dark Ranger) | Focus | Instant · CD | Dark Ranger shadow attack; low-health execute that can trigger **Deathblow** (free reset) and, in AoE, helps re-apply **Beast Cleave**. Spammable during **Withering Fire**. Dark Ranger only. |
| Wailing Arrow | Rotational-spender (Dark Ranger) | Focus | ~2s cast | Dark Ranger nuke that guarantees a **Deathblow** proc and interrupts/silences targets hit for 1s. Replaces the Bestial Wrath button after activation in the Dark Ranger build. Dark Ranger only. @verify-ingame |
| Hunter's Mark | Utility (buff) | No cost | Instant | Marks the target (bonus damage; reveals if stealthed). Apply pre-pull on the main target. |
| Counter Shot | Interrupt | No cost | Instant · 24s [T1] | Ranged interrupt (3s school lockout). **BM's only kick** — the spec has no melee interrupt. |
| Tranquilizing Shot | Dispel | 10 Focus | Instant · ~10s CD | Removes an Enrage or a Magic buff from the target. |
| Intimidation | CC | No cost | Instant · ~60s CD | Commands the pet to stun the target ~5s. |
| Binding Shot | CC | No cost | Instant · ~45s CD | Ground zone; enemies that move too far are stunned. AoE control. |
| Freezing Trap | CC | No cost | Instant · 30s CD | Incapacitates the first enemy that enters (breaks on damage). |
| Tar Trap | CC / slow | No cost | Instant / **30s** `[T1]` | Ground slow field; **Tar-Coated Bindings** synergy with Binding Shot. Choice-node vs Scare Beast. |
| Scare Beast | CC | Focus | Cast | Fears a beast; choice-node alternative to Tar Trap. |
| Concussive Shot | CC / slow | No cost | Instant · 5s CD | Single-target movement slow. |
| Chimaeral Sting | CC (**PvP talent**) | No cost | Instant · 60s [T1] | Applies a disorienting poison. **PvP talent** — unavailable in raid and Mythic+; do not plan a PvE pull around it. |
| Exhilaration | Defensive (self-heal) | No cost | Instant · 2min CD | Heals a large chunk of your (and your pet's) max health; boosted by **Wilderness Medicine / Natural Mending**. |
| Aspect of the Turtle | Defensive (immunity) | No cost | Instant · 3min CD | ~8s immunity to all damage/CC; you cannot attack while active. The panic button. |
| Survival of the Fittest | Defensive | No cost | Instant · ~3min CD | Reduces damage taken by you and your pet (~30%) for a short window. |
| Roar of Sacrifice | Defensive (external) | No cost | Instant / **120s** `[T1]` | Places a buff on a party member redirecting a share of damage they take to you. Choice-node vs Guardian's Hide. |
| Aspect of the Cheetah | Movement | No cost | Instant · 180s [T1] | Burst movement speed (then a lingering lesser boost); **Improved Aspect of the Cheetah** in tree. Class-baseline — nothing to do with Survival despite the old row label. |
| Disengage | Movement | No cost | Instant · ~20s CD | Leap backwards; disengages from melee. |
| Feign Death | Utility | No cost | Instant · 30s CD | Drops combat / threat; also used to cancel casts and dodge mechanics. |
| Misdirection | Utility (threat) | No cost | Instant · ~30s CD | Redirects your next few seconds of threat to your pet or a target ally. |
| Camouflage | Utility (stealth) | No cost | Instant / **60s** `[T1]` | Stealth + minor heal-over-time; used to skip packs / reset. |
| Flare | Utility | No cost | Instant · ~20s CD | Reveals stealth and removes some tracking/stealth effects in an area. |
| Call Pet 1 … Call Pet 5 | Pet | No cost | Cast | Five separate class-baseline spells, one per stable slot — **not** one spell with an argument. That matters for keybinding and macros: each slot needs its own bind. (Renamed this pass; bare "Call Pet" is not a live spell name.) |
| Revive Pet | Pet | No cost | Cast | Resurrects a dead pet. |
| Mend Pet | Pet (heal) | No cost | Channel · 10s CD | Heals the pet over time. |
| Command Pet | Pet (utility) | — | — | Pet control (attack/follow/passive, special abilities). |
| Wild Kingdom | Pet (utility/heal) (**PvP talent**) | No cost | Instant · 60s [T1] | Instantly heals/revives your pet and briefly calls additional pets to attack. **PvP talent** — not a PvE pet-recovery tool; Revive Pet and Mend Pet are. |
| Primal Rage | Utility (Bloodlust) — **pet ability** | No cost | Instant · 360s [T1] | The party-wide +30% haste (with the usual exhaustion lockout). It belongs to the **pet**, not to you: it comes with the *Ferocity* pet specialisation, so whether you can Lust is a question of which pet is out. Bringing a Ferocity pet is a raid-composition decision, not a talent one. |
| Auto Shot | Passive/auto | No cost | Auto | Automatic ranged attack; ticks in the background (in the APL as `auto_shot`). |

### Not on the Midnight Beast Mastery tree

Both of these were carried in this file as BM rows. Tier 1 hands each to a different
Hunter spec, and the tree gates are hard — no talent path reaches them from BM.

- **Kill Shot** — Hunter / **Marksmanship**. Its node on the live Hunter tree is
  spec-gated to Marksmanship alone. BM has **no execute button**; the execute-window
  pressure comes from Black Arrow and Deathblow procs (Dark Ranger) instead, which is a
  real difference in how the last 20% is played, not a naming quirk.
- **Muzzle** — Hunter / **Survival**. Its node is gated to Survival alone. BM's interrupt
  is **Counter Shot** (listed above), and it is ranged — BM never needs to close to melee
  to kick.

*[Tier 1: DB2 @ 12.0.7.67808 — TraitNode → TraitCond → SpecSetMember; `_abilities/reconcile-ledger.md`.]*

### Rows the generated inventory does not carry

- **Auto Shot** is real and castable; it sits on a shared generic skill line (183,
  "GENERIC (DND)") that the inventory generator's two closed allowlists exclude by design.
  Its absence from `ability-inventory.tsv` is a tool gap, not a removal — recorded as
  ledger gap **G3** in `_meta/kb-inbox.md` and as a `prose-only` row in
  `_abilities/section-4-catalogue.md`. It carries no `@verify-ingame` on purpose: logging
  in cannot answer a question about which DB2 skill line a generator reads.
  *[Tier 1: DB2 @ 12.0.7.67808 — SkillLineAbility on SkillLine 183.]*
- **Primal Rage** is a pet-path ability, so it cannot appear in a per-spec player
  inventory — the pet path carries **no spec granularity at all** (`_abilities/reconcile-ledger.md`
  §5 G5). ⚠ It is **not** in `_abilities/pet-family-annex.tsv` either; the annex covers pet
  *skill lines* (Spell Lock, Axe Toss, Freeze) and Primal Rage rides `SpecializationSpells`
  → the **pet** spec *Ferocity*. It is carried in `_abilities/section-3-corroborated.md`,
  confirmed live by `GET /data/wow/spell/264667` → 200.
- **Ancient Hysteria** was the other half of the old Bloodlust row and has been deleted:
  it attaches to nothing at 12.0.7. Primal Rage is the live pet Lust.
