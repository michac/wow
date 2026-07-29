# Demonology — spec facts

> The Demonology-specific instantiation of the general design (`docs/design.md`) and
> pipeline (`docs/architecture.md`). The rotation itself is `rotation.md` (the flat
> priority list the Coach implements); this file is the surrounding facts — the
> tracked set, the burst window, the resource/proc mechanics, the colour members, and
> the blind spots. v1 profile: **Diabolist**.

## Tracked set

Confirmed off `/cdmp hud status` (M3a, live 12.0.7, Diabolist profile), which
enumerates the bound items with their cooldownIDs:

- **Essential (cooldowns) — 6:** Hand of Gul'dan `105174`, Call Dreadstalkers
  `104316`, Summon Demonic Tyrant `265187`, Grimoire: Fel Ravager `1276467`,
  Implosion `196277`, Demonbolt `264178`
- **Utility — 7:** Unending Resolve `104773`, Dark Pact `108416` (defensives);
  Shadowfury `30283`, **Command Demon `119898`**, Mortal Coil `6789`, Blight of
  Tongues `1271802` (CC); Demonic Circle: Teleport `48020` (mobility)
- **Buff bars — 4:** Demonic Core `264173`, Dominion of Argus `1276166`, Unending
  Resolve `104773`, Call Dreadstalkers `104316`
- **Buff icons — 3:** Wild Imp `296553`, Diabolic Ritual `428514` **×2**

Two facts this settled:

- **Utility is 7 spells, not 13**, and it carries the *wrapper* spell **Command
  Demon `119898`**, not the pet ability Axe Toss `119914`. So "the noisy Utility
  default" cited as the trigger for a curated layer-① override (`status.md`) is a
  smaller problem than once assumed — 7 icons, not 13.
- **`428514` (Diabolic Ritual) is tracked TWICE**, as two distinct cooldownIDs
  (`9426`, `9472`) sharing one spellID — direct validation of keying the registry on
  **`cooldownID`, not `spellID`** (`architecture.md`): a spellID-keyed table would
  silently collapse the two and drop a live item. Both entries are the container; the
  per-stage ritual auras a predictive tracker would need are not tracked today (they'd
  need a curated layout override — see `status.md`).

## Rotation shape

Distilled from `knowledge/classes/warlock/demonology/rotation.md` (Diabolist,
12.0.7). Demo is a builder/spender pet-army spec: build Soul Shards → spend on **Hand
of Gul'dan** (summons Wild Imps) → funnel everything into the **Summon Demonic
Tyrant** window (60 s CD, empowers/extends every demon). The single biggest lever is
**how many Hand of Gul'dan casts fit inside the Tyrant window.** The castable-order
logic is `rotation.md`.

### The burst window = the horizontal grouping

Tyrant lines up with the demon-summon cooldowns fired just before it — the canonical
"line Tyrant up with what it buffs" the whole HUD concept is about.

- **The go-gate is Tyrant + Call Dreadstalkers only** — Dreadstalkers is the last
  cast before Tyrant; those two brighten together (common-fate) to mean "go."
- **The tracked Grimoire summon brightens if it's up but is NEVER part of the gate** —
  it's a ~2-min cooldown, absent from roughly half the windows (≈21 Grimoire casts
  vs 48 Tyrant across the top parses), so gating on it would suppress the cue for
  half the burst windows.
- **Summon Doomguard is neither tracked nor cast** in the modern build.

Naming note: the live profile tracks **Grimoire: Fel Ravager**; top parses cast
**Grimoire: Imp Lord** — bind to whatever's tracked, don't hard-code the name.

## Resource & proc mechanics

- **Soul Shards** are readable *and branchable* in instanced combat (the rail's
  cap-flip is a live `if n >= MAX`). Cap = 5, read as **"spend or waste"** at max.
  An in-flight builder shows a **ghost segment** (+1 SB / +3 Infernal Bolt / +2
  Demonbolt).
- **Demonic Core** proc drives the Demonbolt proc-glow; **softens at ≥4 shards** (its
  +2 would overcap). Presence comes off the buff-item `IsActive` / the glow edge, not
  a secret aura read (`architecture.md`).
- **Demonic Art transforms** are directly observable via
  `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED`, which names *which* button transformed:

  | base | override | note |
  | --- | --- | --- |
  | `105174` Hand of Gul'dan | `434635` Ruination | glow the HoG button |
  | `686` Shadow Bolt | `434506` Infernal Bolt | SB isn't tracked → no icon to glow (blind spot) |
  | `1276467` Grimoire: Fel Ravager | `388215` Devour Magic | "becomes a purge on cooldown" |
  | `119898` Command Demon | `119914` Axe Toss | set at pet-summon, before our recorder listens |

  Identity keyed on *ability* (keybinds, proc registry) resolves off the **base**
  spellID, falling back to the override — never the other way round (a transformed
  button otherwise blanks its keybind mid-rotation).

## Colour members (reference — v1 does not colour by group)

v1 colours a cue by **urgency (`emphasis`), not ability group** (`docs/design.md`).
This grouping is retained only as reference for a possible future group-colour mode:

| Group | Members |
| --- | --- |
| Summon-demon (burst) | Tyrant, Dreadstalkers, the tracked Grimoire summon |
| Core shadow damage | Hand of Gul'dan, Demonbolt, Shadow/Infernal Bolt |
| Fel explosion | Implosion |
| Proc / resource | Demonic Core, Soul Shard rail accent |
| Defensive | Unending Resolve, Dark Pact |
| CC | Shadowfury, Axe Toss, Mortal Coil |
| Mobility | Demonic Circle |

## Blind spots — what we cannot assist for Demo

Beyond the general Secret-Values wall (`architecture.md` → Blind spots):

- **Wild Imp count (≥6 Implosion gate):** the `Applications` count is displayed but
  secret. Surface imp *presence* + enlarge Blizzard's stack text with a static "/6";
  **cannot compute "≥6"** ourselves.
- **Demonic Core count (near-cap-4 overcap gate):** displayed but secret. Surface Core
  *presence* only; **cannot signal "near cap 4"**.
- **Demonic Art on the Shadow Bolt half** (SB → Infernal Bolt): *not* secret — Shadow
  Bolt simply isn't in the tracked set, so there's no icon to glow. Glow the
  **HoG → Ruination half only**; the SB half re-opens only with a curated layout that
  adds SB.
