---
title: Outlaw Rogue — Builds & Talents (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Rogue_Outlaw.simc  # tier 1 talent string (Fatebound), 2026-07-11
  - https://www.method.gg/guides/outlaw-rogue/talents  # tier 3, updated 2026-06-16, 12.0.7
  - https://www.method.gg/guides/outlaw-rogue  # tier 3, 12.0.7 (Trickster recommendation)
  - knowledge/classes/rogue/outlaw/talents.md  # tier 1 full tree (Blizzard API + wago)
confidence: high
---

> ⚠ **NOT RE-VERIFIED FOR 12.1 (as of 2026-08-11).** This file still describes
> **Midnight Season 1 / patch 12.0.7** and its `patch:`/`reviewed:` stamps are
> deliberately left at that, because nobody checked its claims against 12.1.
> Patch **12.1 "Curse of Ula'tek"** went live 2026-08-11 and changed things that
> affect **every** spec:
>
> - **Player health and creature damage +25%** at max level, health consumables
>   rescaled, and some DPS/Tank healing + absorb spells retuned. Any absolute
>   HP / healing / consumable number below is now wrong.
> - **Major DPS cooldowns lowered and steady-state damage raised** for several
>   specs — so a spec's burst/sustained split may have moved.
> - **Interrupts** now show a "missed" visual + sound when the target was not casting.
> - **Diminishing-return categories reset after 20s** (was 16s).
> - A game-wide **PvP snare tier-down** (70%→50%, 50%→30%, …). PvP only.
>
> Per-spec 12.1 changes for this spec, if any, are in
> `knowledge/_meta/patch-notes/12.1.md` under the **CLASSES** section — read that
> before trusting anything here. The **regenerated** siblings in this directory
> (`talents.md`, `talents.json`, `ability-inventory.md`) *are* current: they were
> rebuilt on 2026-08-11 from live 12.1 game data and are Tier 1. Where this file
> and they disagree about whether a talent exists, **they win**.


# Outlaw Rogue — Builds & Talents (Midnight S1)

Layer this on top of `talents.md` / `talents.json` (the full Tier-1 tree). This
file is the narrative: which hero tree, which core talents, and why.

## Hero tree: Trickster (recommended)

**Trickster is the go-to for all Season 1 content** per method.gg — Midnight
smoothed out its previously invasive playstyle. Its payoff is **Coup de Grace**
(capstone, via **Unseen Blade**): an empowered strike woven into the builder and
finisher loop, with **Disorienting Strikes** guaranteeing Unseen Blade after
Killing Spree. Supporting picks: **Flawless Form**, **Nimble Flurry** (feeds Blade
Flurry), **No Scruples / Cloud Cover** (Cloud Cover was nerfed ~2% on the May 5
hotfix but the tree still wins). @verify-ingame (current Cloud Cover vs No
Scruples pick)

**Fatebound** is the viable, lower-effort alternative and is what the default
**SimulationCraft profile ships** (its talent string below). Its
**Hand of Fate → Lucky Coin** chain is a passive coin-flip that grants a Lucky
Coin buff every ~7 flips with **no rotational interference** — pick it if you
prefer set-and-forget over Coup de Grace weaving.

## Spec-tree core

Outlaw runs **nearly one build for both single-target and AoE** because its
damage model leans on **Blade Flurry** cleave rather than a separate multi-target
setup. The non-negotiable core:

- **Roll the Bones** (staged 1–4 rework) + **Loaded Dice** — Loaded Dice
  guarantees a higher roll; the whole engine is climbing to and banking a strong
  stage. **Keep It Rolling** locks in a stage-3+ roll for +30s.
- **Restless Blades** + **Ruthlessness** — the cooldown-refund + free-combo-point
  backbone; spending finishers *is* your cooldown reduction.
- **Adrenaline Rush** + **Improved Adrenaline Rush** + **Supercharger** — main DPS
  cooldown; Improved AR adds Slice and Dice upkeep and low-CP usage.
- **Blade Rush**, **Killing Spree**, **Preparation** — cooldown shell (Preparation
  resets AR / BtE / Blade Rush / Killing Spree).
- **Ace Up Your Sleeve** + **Between the Eyes** support (**Improved Between the
  Eyes**, **Zero In**) — Between the Eyes is a core finisher and buff source.
- **Fan the Hammer** + **Opportunity** + **Quick Draw** — the Pistol Shot builder
  package (extra shots, extra combo points per proc).
- **Gravedigger** (apex, row 12) — Between the Eyes double-stack chance, a Dispatch
  proc at high CP, and a bullet-stack system granting free high-impact Between the
  Eyes. Strong single-target apex.

### Two builder identities

Outlaw has two supported builder cores; pick one, don't mix:

- **Fan the Hammer / Ace Up Your Sleeve (pistol) build** — leans on Opportunity +
  Fan the Hammer for combo points via Pistol Shot; the mainstream setup and what
  the simc default profile uses.
- **Hidden Opportunity / Audacity (ambush) build** — **Hidden Opportunity** makes
  **Ambush** usable outside stealth on **Audacity** procs; **Vanish / Shadowmeld**
  are pressed for extra Ambushes between procs. More button-active; the APL fully
  supports it (the `build` list front-loads Ambush when Audacity is up).

### Dungeon / AoE swaps

Keep the core; swap in **Dancing Steel** (Blade Flurry duration) and **Grand
Melee** (target cap), and **Deft Maneuvers** so Blade Flurry itself builds combo
points at 3+ targets. Single-target-focused apex/support points shift toward the
cleave enablers.

## Class-tree staples

Utility/survival picks that matter: **Thistle Tea** (energy/mastery panic),
**Cloak of Shadows**, **Evasion**, **Elusiveness vs Cheat Death** (choice —
Cheat Death for progression), **Tricks of the Trade vs Blackjack**, **Alacrity**
and **Deeper Stratagem / Deeper combo point** for throughput, **Without a Trace**
(extra Vanish charge — key for Hidden Opportunity builds), **Subterfuge** and
**Fleet Footed / Shadowrunner** for movement.

## Talent import strings

- **Fatebound (simc default profile, Tier 1):**
  `CQQAAAAAAAAAAAAAAAAAAAAAAAgx2MGjZmZmtZmZmZMmFGmZZaZw2MAAAAAgZbbmZGmZmZGzMzyAAAAwAYgNYGjGzGgtJswAgZmBG`
- **Trickster (recommended):** method.gg publishes the current Trickster loadout
  string on its Talents page (not machine-scraped here — grab it live). @verify-ingame

## Notes / gaps

- The **SimulationCraft default profile is Fatebound**, while method.gg and Icy
  Veins recommend **Trickster** for live play — both are viable; Trickster is the
  performance pick, Fatebound the low-maintenance one. Re-check when simc ships a
  Trickster default.
- Exact talent-point placement per content type shifts with tuning; treat the
  core list above as stable and confirm the fine points against a live method.gg /
  Wowhead loadout string. @verify-ingame
