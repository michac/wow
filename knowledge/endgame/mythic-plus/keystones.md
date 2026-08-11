---
title: How Keystones Work — Midnight Season 2
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://us.forums.blizzard.com/en/wow/posts/29833350   # S1 ending / S2 information — pre-season week rules (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24294369          # Midnight Season 2 overview / dungeon rotation (Tier 1)
  - https://conquestcapped.com/guides/wow/midnight-mythic-plus-season-2/
  - https://www.icy-veins.com/wow/midnight-mythic-season-1-guide   # carried-over S1 key mechanics
confidence: medium   # pre-season timing + M0 lockout/track are Tier 1 (high); the carried-over transform rules are S1-sourced and not re-confirmed for S2
---

# How Keystones Work (Midnight Season 2)

> ⚠ **Week of 2026-08-11 — there are no keystones.** 12.1 went live Aug 11 in a
> **pre-season** state: Mythic+ difficulties are **closed** and **keys do not
> drop**. Everything below the next section describes the game from **the week
> of 2026-08-18**, when Season 2 opens and keys begin dropping again.

You never "farm" keys. **You always hold exactly one keystone, and finishing a
run hands you the next one.** It's a self-perpetuating loop — the only way to
run out is to delete it or never start.

## Right now: the pre-season week (Aug 11 → Aug 18)

- **Mythic+ is not available and Mythic Keystones do not drop.** Any key you
  were holding is a Season 1 key and does nothing.
- The **Season 2 dungeon pool is already live on Heroic and Mythic 0**,
  including the new **Altar of Fangs**.
- **Mythic 0 is on a WEEKLY lockout this week only** and drops **Champion 1/6
  (ilvl 292)**. One clear per dungeon, then that dungeon is done until reset.
- **With maintenance the week of Aug 18:** Mythic+ difficulties open, players
  begin earning Mythic Keystones, and **Mythic 0 returns to a daily lockout**
  (still ilvl 292).

So the pre-season play is: run each Season 2 dungeon **once** on Mythic 0 for a
292 piece and to learn the pool. There is nothing to push and no key to protect.

## The Season 2 pool (8 dungeons)

**Altar of Fangs** (new) · Murder Row · Den of Nalorakk · The Blinding Vale ·
Voidscar Arena · **Ruby Life Pools** (Dragonflight) · **Kings' Rest** (BfA) ·
**Temple of Sethraliss** (BfA). The three returning dungeons ship with design
and quality-of-life updates.

The eight Season 1 dungeons — Algeth'ar Academy, Magisters' Terrace, Maisara
Caverns, Nexus-Point Xenas, Pit of Saron, Seat of the Triumvirate, Skyreach,
Windrunner Spire — **rotated out** and are no longer keystone dungeons.

## Getting your first key (from Aug 18)

- Clear a **Mythic 0** dungeon (Mythic difficulty, no keystone — queue/walk in
  like Heroic). The **final boss drops your first Mythic Keystone.**
- It starts at **+2**, for a **random dungeon** in the Season 2 pool.
- **No key right now?** (new character, deleted it, etc.) → just run any
  **Mythic 0** again to get a fresh **+2**. That's the reset valve.

## Running a key

- The keystone is an **item in your bags** ("Mythic Keystone"). Activate it at
  the **Font of Power** pedestal just inside the dungeon entrance.
- **Only one key is used per run.** In a 5-player group, one person slots their
  key; **the other four keep theirs untouched.** So five people can chain five
  keys back-to-back, and running a friend's key does **not** burn yours — handy
  for pushing one key while others bank theirs. *(Standard M+ mechanic —
  flagged for in-game confirm.)*

## What happens at the end — upgrade / downgrade

*(Carried over from Season 1; 12.1's notes changed nothing here, but it has not
been re-confirmed in a Season 2 key.)* The key **transforms in place** (new
level, **new random dungeon**) based on the timer:

| Result | Time remaining | Key change |
|--------|----------------|------------|
| Timed, barely | under 20% left | **+1 level** |
| Timed, comfortably | 20–40% left | **+2 levels** |
| Timed, blown out | over 40% left | **+3 levels** |
| **Over time** (still completed) | — | **−1 level** (depleted), keeps going |

- So a fresh **+2 becomes a +4** if you time it with 20–40% to spare — it jumps
  **two** levels. Time the next one well and +4 → +6.
- Missing the timer **does not brick the key** — you still finish the dungeon
  and the key just drops one level. You always get *a* key back.

## Resilient Keystones — the safety floor

Once you **time every dungeon in the Season 2 pool at a given level**, your key
**can't drop below that level** afterward, even on a deplete:

- Time the **full pool of 8 at +12** → floor = **+12**. This is the first
  threshold.
- Time the full pool at +13 → floor = 13, at +14 → 14, and so on.

Below +12 there's no floor — a depleted +4 becomes a +3. The floor is a floor on
*depletion*, not a lock: **Lindormi can still lower a key manually** if you want
a lower level.

## How this connects to rewards

- The key level you **complete** sets your end-of-run loot track and your
  vault ilvl — see [`loot.md`](loot.md) for the Season 2 track/ilvl table and
  the level breakpoints. (The Season 1 numbers — "+6 = Hero, +10 = 272 vault
  cap" — are **historical**; Season 2 rescaled them.)
- Every completion (timed or not) also **counts toward the vault's 1/4/8
  dungeon row** and pays **Season 2 crests (Mistcrests)** + voidcore shards — so
  a depleted run is never wasted.

## TODO

- [ ] **Verify in-game (Encomplete):** confirm only the *used* keystone @verify-ingame
      transforms and party members keep theirs (long-standing mechanic, but
      unconfirmed against a Midnight source here). **Not testable until Aug 18.**
- [ ] Confirm the **upgrade/downgrade table still holds in Season 2** (the
      20% / 20–40% / 40% bands and the −1 on depletion) — carried over from S1,
      not re-sourced for S2.
- [ ] Confirm **weekly-reset behavior**: does your held key persist across the
      Tuesday reset at its current level, or rescale? (Not covered by the
      sources consulted — check after the first S2 reset.)
