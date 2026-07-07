---
title: How Mythic+ Loot Works — Midnight Season 1
patch: 12.0.7
fetched: 2026-06-21
reviewed: 2026-07-07
sources:
  - https://conquestcapped.com/guides/wow/midnight-mythic-plus-season-1/
  - https://www.icy-veins.com/wow/midnight-mythic-season-1-guide
  - https://www.wowhead.com/guide/midnight/season-1-mythic-rewards-loot-drops-mounts-achievements
  - knowledge/endgame/great-vault.md
  - knowledge/endgame/dawncrests.md
  - knowledge/systems/void-forge.md
confidence: medium   # track breakpoints high; timed-vs-depleted drop count needs in-game confirm
---

# How Mythic+ Loot Works (Midnight Season 1)

There are **two completely separate loot channels** in M+, and confusing them
is the #1 source of "why did I get nothing?" frustration:

1. **End-of-dungeon drop** — RNG, immediate, *most runs you get no gear*.
2. **The Great Vault** — guaranteed, weekly, the *reliable* reward. This is
   why you run keys.

Plus a third thing that is **not loot but always pays out**: currency
(Dawncrests + Ascendant Voidshards), every run, win or lose.

## 1. End-of-dungeon drop (the lottery)

When the group **completes** a key, the dungeon drops **2 pieces of gear for
the whole party of 5** — distributed as personal loot. It is **2 items total,
not 2 per player.**

> So on any given run, **0 pieces is the most common outcome for you
> personally.** 2 items split across 5 people ≈ a ~40% chance you win
> *anything* on a run. Three runs in a row with no gear is normal variance,
> not bad luck or a bug.

- Sources agree the count is **2 on a timed clear**. Whether **depleting**
  (over-time) drops fewer (older systems gave 1) is **unconfirmed for S1** —
  see TODO. Either way it is a small, fixed number split 5 ways.
- **Item track is set by key level, not by who you are** (see table below).
- The drop's item level **caps at +10**. Running +11, +15, +20 gives the
  **same end-of-run ilvl** as +10 — higher keys only improve your *vault* and
  your *crest income*, not the end-of-run piece.

### Track / ilvl by key level

| Key level | End-of-run track | End-of-run ilvl | Vault ilvl |
|-----------|------------------|-----------------|------------|
| +2 to +3 | Champion | 250 | 259 |
| +4 to +5 | **Champion** | 253–256 | 263 |
| **+6 to +9** | **Hero** | 259–263 | 266–269 |
| **+10 and up** | Hero | **266 (cap)** | **272 (cap)** |

→ **+6 is the breakpoint that matters.** Below +6 the best the dungeon can
hand you is a **Champion** piece — that is the ceiling for that key, *not* a
bad roll. A "disappointing Champion piece from a +4" is the system working as
designed; the only way to make the drop better is to run a **higher key**.

→ **Myth-track gear does not drop from the end of a key at all.** M+ Myth
gear comes only from (a) the **+10 vault** (272) or (b) a **Nebulous Void
Core bonus roll on a +10 or higher run** (`../../systems/void-forge.md`).

## 2. The Great Vault (the guaranteed reward)

This is the actual reason to grind keys. Each M+ run **counts toward your
weekly vault**; the dungeon row unlocks **1 / 4 / 8** M+ completions →
**up to 3 item choices** next reset. Vault ilvl is set by your **best keys of
the week** (table above), capped at **+10 → 272**.

- Run **8× +10** for the maximum-quality M+ vault row.
- The vault is *picked*, not random-dropped — you choose one piece from what
  it offers. That is the dependable upgrade path; the end-of-dungeon lottery
  is just a bonus on top.
- Full mechanics: `../great-vault.md`.

## 3. The currency you *always* get (not a consolation prize)

Every run pays these **regardless of whether you won gear** — this is what you
saw on your +5s ("nothing but voidcore shards and crests"). It is the steady,
non-RNG progression, and it is arguably more valuable than the gear lottery:

- **Dawncrests** — upgrade currency. +6 and up pays **Hero Dawncrests**; +9
  and up also pays **Myth Dawncrests** every run. 150 Hero crests fully
  upgrades a Hero piece (259→276). Totals are **uncapped** since the May-19
  hotfix — M+ is the best raw crest farm in the game. (`../dawncrests.md`)
- **Voidcore shards** — the M+ final chest drops **two** different void
  currencies; check the tooltip:
  - **Elementary Voidcore Shards** → **build the Voidforge** (3 → 1 Elemental
    Voidcore; 18 shards unlocks it). If you have **not** unlocked the forge
    yet, these are almost certainly what you're seeing.
  - **Ascendant Voidshards** → **upgrade** a maxed weapon/trinket past cap
    (5 → 1 Ascendant Voidcore; e.g. 6/6 Myth 289 → 298), gated behind a
    separate late questline.
  - Both detailed in `../../systems/void-forge.md`.

> Mindset fix: the crests and shards **are** the reward. A run that drops no
> gear still advanced two upgrade tracks and a vault slot. The end-of-dungeon
> piece is the only RNG part — everything else is guaranteed accrual.

## What happened on your runs (worked example)

- **+4, got a Champion piece** → correct ceiling. +4 is below the +6 Hero
  breakpoint, so Champion (253–256) is the *best possible* end-of-run drop
  there. To see Hero-track drops, run **+6 or higher**.
- **Two +5s, no gear, just shards + crests** → you lost both personal-loot
  rolls (2 items ÷ 5 players). Completely normal. You still banked the
  guaranteed crests + Voidshards on each, **and both runs fed your vault** —
  do 1/4/8 keys this week and pick a guaranteed piece at reset.

**Net advice:** push your key to **+6+** so the lottery can give Hero gear,
keep running to fill the **8-dungeon vault** row (the real upgrades), and stop
treating crests/shards as a let-down — they're the dependable half of M+
gearing.

## TODO

- [ ] **Confirm in-game (Encomplete):** does an **over-time / depleted** @verify-ingame
      completion drop **2** items or fewer? Sources state "2 on a timed
      clear" but are silent on depletion.
- [ ] Confirm exact **Hero/Myth Dawncrest counts per key level** at the
      end-of-run chest (Conquest Capped lists per-level crest amounts; e.g.
      +6 ≈ 18 Hero — pull the full table).
- [ ] Confirm **Ascendant Voidshard drop count** per M+ run (and whether it
      scales with key level).
