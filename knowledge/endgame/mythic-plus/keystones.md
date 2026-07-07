---
title: How Keystones Work — Midnight Season 1
patch: 12.0.7
fetched: 2026-06-21
reviewed: 2026-07-07
sources:
  - https://conquestcapped.com/guides/wow/midnight-mythic-plus-season-1/
  - https://www.icy-veins.com/wow/midnight-mythic-season-1-guide
  - https://boostmatch.gg/blog/wow/articles/wow-midnight-mythic-plus-season-1-guide
  - https://wowvendor.com/media/wow/mythic-plus-guide/
confidence: medium   # core rules high (multi-source); "only used key changes" + reset = standard mechanic, verify in-game
---

# How Keystones Work (Midnight Season 1)

You never "farm" keys. **You always hold exactly one keystone, and finishing a
run hands you the next one.** It's a self-perpetuating loop — the only way to
run out is to delete it or never start.

## Getting your first key

- Clear a **Mythic 0** dungeon (Mythic difficulty, no keystone — queue/walk in
  like Heroic). The **final boss drops your first Mythic Keystone.**
- It starts at **+2**, for a **random dungeon** in the Season 1 pool.
- **No key right now?** (new character, deleted it, etc.) → just run any
  **Mythic 0** again to get a fresh **+2**. That's the reset valve.

## Running a key

- The keystone is an **item in your bags** ("Mythic Keystone"). Activate it at
  the **Font of Power** pedestal just inside the dungeon entrance.
- **Only one key is used per run.** In a 5-player group, one person slots their
  key; **the other four keep theirs untouched.** So five people can chain five
  keys back-to-back, and running a friend's key does **not** burn yours — handy
  for pushing one key while others bank theirs. *(Standard M+ mechanic —
  flagged for in-game confirm in S1.)*

## What happens at the end — upgrade / downgrade

The key **transforms in place** (new level, **new random dungeon**) based on
the timer:

| Result | Time remaining | Key change |
|--------|----------------|------------|
| Timed, barely | under 20% left | **+1 level** |
| Timed, comfortably | 20–40% left | **+2 levels** |
| Timed, blown out | over 40% left | **+3 levels** |
| **Over time** (still completed) | — | **−1 level** (depleted), keeps going |

- This is why a fresh **+2 became your +4** — you timed it with 20–40% to
  spare, so it jumped **two** levels. Time the next one well and +4 → +6 (and
  +6 is the [Hero-track loot breakpoint](loot.md)).
- Missing the timer **no longer bricks the key** — you still finish the dungeon
  and the key just drops one level. You always get *a* key back.

## Resilient Keystones — the safety floor

Once you **time every dungeon in the S1 pool at a given level**, your key
**can't drop below that level** afterward, even on a deplete:

- Time the **full pool at +12** → floor = **+12**.
- Time the full pool at +13 → floor = 13, at +14 → 14, and so on.

Below that threshold there's no floor — a depleted +4 becomes a +3.

## How this connects to rewards

- The key level you **complete** sets your end-of-run loot track and your
  vault ilvl — see [`loot.md`](loot.md). **+6 = Hero track**, **+10 = vault
  cap (272)**.
- Every completion (timed or not) also **counts toward the vault's 1/4/8
  dungeon row** and pays crests + voidcore shards — so a depleted run is never
  wasted.

## TODO

- [ ] **Verify in-game (Encomplete):** confirm only the *used* keystone
      transforms and party members keep theirs in S1 (long-standing mechanic,
      but unconfirmed against a Midnight source here).
- [ ] Confirm **weekly-reset behavior**: does your held key persist across the
      Tuesday reset at its current level, or rescale? (Not covered by the
      sources consulted — check after a reset.)
