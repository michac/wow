---
title: Macros (Midnight)
patch: 12.0.7
fetched: 2026-06-27
reviewed: 2026-07-07
sources:
  - https://warcraft.wiki.gg/wiki/Macro_commands
  - https://warcraft.wiki.gg/wiki/Macro_conditionals
  - https://warcraft.wiki.gg/wiki/MACRO_targetmarker
  - https://www.wowhead.com/news/new-interrupt-macro-prevents-overwriting-of-target-markers-in-patch-12-0-7-381742
  - https://us.forums.blizzard.com/en/wow/t/macro-changes-now-live-target-markers-and-chat-messages/2261956
confidence: high
---

# Macros (Midnight)

The macro system is one of the most stable parts of WoW — the slash commands
and conditional syntax below have been unchanged for years and are current on
**live 12.0.7**. The only Midnight-era deltas are at the bottom under
[12.0.x changes](#12-0-x-macro-changes). When in doubt, the engine behavior is
authoritative on the Warcraft Wiki (tier ~1–2 for API facts).

> A macro is just a list of slash commands, one per line, run top-to-bottom in a
> single button press. Edit them at **Esc → Macros** (or `/macro`). You get
> ~18 general + 18 character-specific slots; each macro is capped at
> **255 characters** and can use any icon (`?` = auto-pick the icon of the first
> spell).

## The big rule: one action per press

A single keypress may trigger **at most one** spell/item cast. You can stack as
many *non-casting* commands as you like (target, mark, stop, yell), but
`/cast SpellA` then `/cast SpellB` on the same press will only fire SpellA
(unless A is off-GCD/free, e.g. a racial + a real spell). To fire abilities in
order across multiple presses, use `/castsequence`.

Macros also **cannot** make combat decisions for you (no "cast X if boss is
below 20%"). Conditionals only see *static* state (your form, modifiers, target
type, etc.), not health, cooldowns, or buffs on others. That restriction is
deliberate and unchanged in Midnight.

## Core slash commands

| Command | Does |
|---------|------|
| `/cast` | Cast a spell (or use an item; name conflicts resolve to the spell) |
| `/use` | Use an item or spell (name conflicts resolve to the item) |
| `/castsequence` | Step through a list of spells, one per press: `reset=N/target/combat/shift` |
| `/cast !Spell` | The `!` prefix *keeps a toggle on* (won't cancel a stance/aura if already up) |
| `/stopcasting` | Cancel the current cast/channel (put on its own line *above* a burst cast) |
| `/stopmacro` | Abort the rest of the macro; takes conditionals: `/stopmacro [noexists]` |
| `/cancelaura` | Remove one of your own buffs by name (e.g. block, immunity, a stance) |
| `/cancelform` | Drop your current shapeshift/stance |
| `/target`, `/targetenemy`, `/targetlasttarget` | Targeting helpers |
| `/focus`, `/clearfocus` | Set / clear your focus unit |
| `/cleartarget` | Drop the current target |
| `/petattack`, `/petfollow`, `/petstay` | Pet control |
| `/targetmarker` (`/tm`) | Set/clear a raid target marker — see [below](#target-markers-tm) |
| `/click ButtonName` | Press another UI/action button (chains macros, triggers addons) |
| `/run` (`/script`) | Run a line of Lua — blocked from *protected* actions in combat |

`/cast` and `/use` accept the same `[conditional]` brackets and `@unit` syntax
as everything else, so most of a macro's power is in the conditionals, not the
command.

## Conditionals

Conditionals go in `[square brackets]` immediately after the command. Multiple
options inside one bracket are **AND**; semicolons between bracket-sets are
**else/else-if**, evaluated left to right; an empty `[]` (or no bracket) is the
fallback. Prefix any condition with `no` to negate it (`[nocombat]`,
`[nomod]`).

```
/cast [@mouseover,help,nodead][@target,help,nodead][@player] Rejuvenation
```
*Cast on my mouseover if it's a living friendly unit; else my target if
friendly; else myself.*

### Target redirection (`@unit`)

Override who the command affects for that one line:
`@target @focus @mouseover @player @pet @cursor @none`, plus party/raid slots
`@party1..4`, `@raid1..40`, `@arena1..3`, `@boss1..5`.

### Most-used conditionals

| Conditional | True when |
|-------------|-----------|
| `help` / `harm` | Unit can receive a friendly / hostile spell |
| `exists` / `dead` / `nodead` | Unit exists / is dead / is alive |
| `mod` / `mod:shift,ctrl,alt` / `nomod` | A modifier key (or specific one) is held |
| `combat` / `nocombat` | You are in combat |
| `harm,nodead` | Standard "real attackable enemy" guard |
| `form:N` / `stance:N` | In shapeshift/stance index N (`form:0` = caster/no form) |
| `stealth` | Stealthed |
| `mounted` / `flying` / `flyable` | Mount state / can mount / zone allows flying |
| `advflyable` | Zone supports **skyriding** (dynamic flight) |
| `swimming` / `indoors` / `outdoors` | Environment |
| `spec:N` | Active spec is index N (1 = first spec tab) |
| `talent:R/C` | Talent at row R column C is selected (classic tree position) |
| `known:Spell` | You currently know that spell/ability |
| `pet` / `pet:Name` / `pet:Family` | Pet is out (optionally a specific one) |
| `channeling` / `channeling:Spell` | You are channeling (that spell) |
| `equipped:Type` / `worn:Type` | Item type equipped (e.g. `equipped:Shields`, `worn:Cloth`) |
| `bar:N` / `actionbar:N` / `bonusbar:N` | Action bar page state |
| `group` / `group:party` / `group:raid` | In a group / specifically party or raid |
| `resting` | In a rested (inn/city) area |
| `vehicleui` | The vehicle UI is showing |
| `pvptalent:N` | A PvP talent is slotted |
| `house` | **You are inside player housing** (added 11.2.7 — relevant to Midnight housing) |

## Common patterns

**Modifier overload** — three spells on one key:
```
/cast [mod:shift] Spell B; [mod:alt] Spell C; Spell A
```

**Mouseover heal with self-cast fallback** (the healer workhorse):
```
/cast [@mouseover,help,nodead][@target,help,nodead][@player] Flash Heal
```

**Focus interrupt that never steals your target:**
```
/cast [@focus,harm,nodead][harm,nodead] Counterspell
```

**Cast-sequence with reset** (e.g. an opener that resets after 6s out of combat
or on target change):
```
/castsequence reset=6/target/combat A, B, C
```

**Stopcasting burst** (force an instant on top of a hardcast):
```
/stopcasting
/cast Combustion
```

**One-button trinket + cooldown** (both off-GCD, so both fire):
```
/use 13
/cast Some On-Use Cooldown
```
*`13`/`14` are the trinket slots; you can `/use` any equipment slot number.*

## Target markers (`/tm`)

`/tm N` (or `/targetmarker N`) sets a raid marker on your current target;
`/tm 0` clears it. Indices: **1** Star, **2** Circle, **3** Diamond,
**4** Triangle, **5** Moon, **6** Square, **7** Cross (X), **8** Skull.
It accepts the same `[conditional]` and `@unit` options as `/cast`:
```
/tm [@focus] 8
```

## 12.0.x macro changes

These are the only macro deltas specific to **Midnight (12.0)** — everything
above is evergreen.

- **`~` prefix preserves existing markers (12.0.7).** Prefixing the index with
  a tilde tells `/tm` to **skip** the unit if it already carries *any* marker,
  so coordinated interrupt/kill macros no longer stomp the tank's skull:
  ```
  /cast [@mouseover,harm,nodead][harm,nodead] Kick
  /tm ~8
  ```
  *Interrupt, then mark Skull only if the target is currently unmarked.*
- **Marker throttle (12.0.x).** A macro may not set markers on **more than 3
  units in a very short window** — chained `/tm` mass-marking macros are now
  rate-limited. Normal one-target-per-press use is unaffected.
- **Chat-message restrictions during encounters (deployed ~Mar 2026).** While
  in an active boss encounter, macros **cannot** post to non-group channels
  (guild/community/custom). Group channels (`/raid`, `/party`, `/rw`) and
  whispers to people *in the instance* still work but are throttled. Don't build
  raid macros that announce to guild/say chat — they'll be silently dropped in
  combat.
- **`[house]` conditional (11.2.7, carried into Midnight).** True when you're
  inside player housing — useful for housing/decor utility macros (see
  `systems/housing.md`).
- **`[advflyable]`** distinguishes **skyriding**-enabled zones from static-flight
  zones, handy for mount macros now that most Midnight zones use dynamic flight.

## Limits & gotchas

- **255 characters** per macro, hard cap. Long chains → split across `/click`ed
  macros, or use an addon (Macro Toolkit) for in-edit length; the *executed*
  macro still obeys 255.
- **Protected actions can't be triggered by `/run` in combat** — casting,
  targeting, and moving via Lua are blocked once you're in combat (anti-botting).
  Use the real slash commands (`/cast`, `/target`) inside conditionals instead.
- **No reactive logic** — conditionals can't read health %, cooldown readiness,
  or others' buffs. That's an addon (WeakAuras) / `/castsequence` job.
- **Ability *names* drift between patches.** A macro that worked last season can
  silently no-op if a talent renamed the spell — verify spell names against the
  live spellbook after class changes, not against old guides.
