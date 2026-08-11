---
title: How Mythic+ Loot Works — Midnight Season 2
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://us.forums.blizzard.com/en/wow/posts/29833350        # Tier 1 — S1 ending / S2 pre-season rules (M0 Champion 1/6 weekly lockout, keys Aug 18)
  - https://worldofwarcraft.blizzard.com/en-us/news/24294369     # Tier 1 — Midnight Season 2 overview (M0 292, S2 dungeon pool)
  - https://worldofwarcraft.blizzard.com/en-us/news/24295085     # Tier 1 — Lairs preview (the S2 track-step ilvl + Mistcrest anchors)
  - https://worldofwarcraft.blizzard.com/en-us/news/24293281     # Tier 1 — Curse of Ula'tek content update notes
  - wago.tools CurrencyTypes DB2 @ 12.1.0.69214                  # Tier 1 — Mistcrest currency IDs 3437–3441 + per-track ilvl bands
  - https://conquestcapped.com/guides/wow/midnight-mythic-plus-season-2/   # Tier 4 — provisional per-key numbers only
  - knowledge/endgame/great-vault.md
  - knowledge/endgame/dawncrests.md
  - knowledge/systems/void-forge.md
confidence: medium   # M0/crest/track anchors are Tier-1 high; the per-key M+ table is UNVERIFIED until keys go live 2026-08-18
---

# How Mythic+ Loot Works (Midnight Season 2)

> ## ⚠ Read this first: there are no keystones this week
>
> **12.1 went live 2026-08-11 in a pre-season state. Mythic Keystones do not
> drop and Mythic+ difficulties do not exist until maintenance the week of
> **2026-08-18**.** Everything below about key levels, the M+ vault row and
> per-key crest income describes the **Aug 18** game, not today's.
>
> **What Mythic dungeons pay right now (week of Aug 11):**
>
> - The **Season 2 pool of 8 dungeons** is live on **Heroic and Mythic 0** only,
>   including the new **Altar of Fangs**.
> - **Mythic 0 drops Champion 1/6 — item level 292** — on a **weekly lockout,
>   for this week only**. From Aug 18 M0 returns to a **daily** lockout and
>   still drops 292.
> - Your Great Vault this reset pays out on your **final Season 1 week**.
>   Season 2 vault credit starts accruing now and is claimable **Aug 18**.
>
> So the honest pre-season plan is: **clear all 8 dungeons on M0 once** (that is
> the whole weekly M0 allowance), bank the 292s, and bank vault credit.

There are **two completely separate loot channels** in M+, and confusing them
is the #1 source of "why did I get nothing?" frustration:

1. **End-of-dungeon drop** — RNG, immediate, *most runs you get no gear*.
2. **The Great Vault** — guaranteed, weekly, the *reliable* reward. This is
   why you run keys.

Plus a third thing that is **not loot but always pays out**: currency
(**Mistcrests** + void shards), every run, win or lose.

## 1. End-of-dungeon drop (the lottery)

When the group **completes** a key, the dungeon drops **2 pieces of gear for
the whole party of 5** — distributed as personal loot. It is **2 items total,
not 2 per player.**

> So on any given run, **0 pieces is the most common outcome for you
> personally.** 2 items split across 5 people ≈ a ~40% chance you win
> *anything* on a run. Three runs in a row with no gear is normal variance,
> not bad luck or a bug.

- The count is **2 on a timed clear**. Whether **depleting** (over-time) drops
  fewer (older systems gave 1) remains **unconfirmed** — see TODO. Either way
  it is a small, fixed number split 5 ways.
- **Item track is set by key level, not by who you are.**
- The drop's item level **caps out around +10**. Running +11, +15, +20 gives
  the **same end-of-run ilvl** as +10 — higher keys only improve your *vault*
  and your *crest income*, not the end-of-run piece.
- **Myth-track gear does not drop from the end of a key at all.** M+ Myth gear
  comes only from the **+10 vault** or a **Voidcore bonus roll**.

### The Season 2 gear ladder (Tier-1 confirmed anchors)

These are the numbers that are actually nailed down for S2 — the **first step**
of each track, from the Tier-1 Lairs reward table, and the ilvl **band each
Mistcrest upgrades through**, from `CurrencyTypes` DB2 at build 12.1.0.69214:

| Track | 1/6 ilvl | Upgraded by | Crest band (1/6 → 6/6 top) |
|---|---|---|---|
| Adventurer | — | Adventurer Mistcrest (3437) | 269 → 282 |
| Veteran | **279** | Veteran Mistcrest (3438) | 282 → 295 |
| **Champion** | **292** | Champion Mistcrest (3439) | 295 → 308 |
| **Hero** | **305** | Hero Mistcrest (3440) | 308 → 321 |
| Myth | **318** | Myth Mistcrest (3441) | 321 → 334 |

As in Season 1, a track's **first step or two sits below its own crest band** —
you pay the *lower* tier's crests to climb into the band (Champion 1/6 = 292 is
below the 295 Champion floor, exactly like S1's Champion 1/6 = 246 vs a 250-263
Champion Dawncrest band). Season 2 is a **flat +46 ilvl shift** off Season 1 at
every track step.

### Track / ilvl by key level — ⚠ NOT YET LIVE

**Keys do not exist until 2026-08-18 and Blizzard has published no per-key
reward table.** The figures below are **provisional**, reconstructed from the
confirmed track anchors above plus Tier-4 guide sites, and **must be
re-verified in game once keys drop**. Do not quote them as fact.

| Key level | End-of-run track | End-of-run ilvl | Vault ilvl |
|-----------|------------------|-----------------|------------|
| Mythic 0 | **Champion 1/6** | **292** *(Tier-1 confirmed)* | — |
| +2 to +3 | Champion | ~295–296 | ~305 |
| +4 to +5 | Champion | ~299–302 | ~309 |
| **+6 to +9** | **Hero** | ~305–309 | ~312–315 |
| **+10 and up** | Hero | **~311 (Hero 3/6, cap)** | **~318 (Myth 1/6, cap)** |

→ **+6 is the breakpoint that matters** (assuming S1's shape carries). Below
+6 the best the dungeon can hand you is a **Champion** piece — that is the
ceiling for that key, *not* a bad roll. The only way to make the drop better is
to run a **higher key**.

→ **+10 is where Myth-track enters your life at all**, and only via the vault.

## 2. The Great Vault (the guaranteed reward)

This is the actual reason to grind keys. Each M+ run **counts toward your
weekly vault**; the dungeon row unlocks **1 / 4 / 8** M+ completions →
**up to 3 item choices** next reset. Vault ilvl is set by your **best keys of
the week**, capped at **+10**.

- Run **8× +10** for the maximum-quality M+ vault row.
- The vault is *picked*, not random-dropped — you choose one piece from what
  it offers. That is the dependable upgrade path; the end-of-dungeon lottery
  is just a bonus on top.
- **Season 2 timing:** the vault you open the week of Aug 11 is built from your
  **final Season 1 week**. S2 credit accrues from now and pays out **Aug 18**.
  **Voidcore bonus rolls are absent from that first S2 vault** — they arrive the
  **week of Aug 25** and need at least **3 panes unlocked**.
- Full mechanics: `../great-vault.md`.

## 3. The currency you *always* get (not a consolation prize)

Every run pays these **regardless of whether you won gear**. It is the steady,
non-RNG progression, and it is arguably more valuable than the gear lottery:

- **Mistcrests** — the **Season 2 upgrade currency**, replacing Season 1's
  **Dawncrests**. Same five tiers (Adventurer / Veteran / Champion / Hero /
  Myth), same job. As in S1, high keys pay **Hero Mistcrests**, and the top
  keys also pay **Myth Mistcrests**. **Which key levels pay which tier, and how
  many per run, is not published for S2 — verify at launch** (see TODO).
  (`../dawncrests.md` covers the crest system itself.)
  - ⚠ **Season 1 Dawncrests are dead currency for gearing** — they only upgrade
    Season 1 items, and Season 1 world-boss / "Knocking off the Top (Heroic)"
    gear **can no longer be upgraded at all**.
- **Voidcore shards** — the M+ final chest drops **two** different void
  currencies; check the tooltip:
  - **Elementary Voidcore Shards** → **build the Voidforge** (3 → 1 Elemental
    Voidcore; 18 shards unlocks it). If you have **not** unlocked the forge
    yet, these are almost certainly what you're seeing.
  - **Ascendant Voidshards** → **upgrade** a maxed weapon/trinket past cap
    (5 → 1 Ascendant Voidcore), gated behind a separate late questline.
  - Both detailed in `../../systems/void-forge.md`.
  - ⚠ **Nebulous Voidcores changed in 12.1:** Season 1 Voidcores **converted to
    gold** at season end. From S2 they are a **Great Vault reward**, the **raid
    re-roll costs 1** (was 2), and Orin Straylight (relocated next to the
    Catalyst in Silvermoon) hands out **one extra per week from week 8**.

> Mindset fix: the crests and shards **are** the reward. A run that drops no
> gear still advanced two upgrade tracks and a vault slot. The end-of-dungeon
> piece is the only RNG part — everything else is guaranteed accrual.

## Worked example (the pattern, from a Season 1 session)

The ilvls below are Season 1 numbers — kept because the *shape* of the lesson
is what carries into Season 2, not the values.

- **+4, got a Champion piece** → correct ceiling. +4 was below the +6 Hero
  breakpoint, so Champion was the *best possible* end-of-run drop there. To see
  Hero-track drops, run **+6 or higher**.
- **Two +5s, no gear, just shards + crests** → both personal-loot rolls lost
  (2 items ÷ 5 players). Completely normal. The guaranteed crests + Voidshards
  still banked on each, **and both runs fed the vault**.

**Net advice (from Aug 18):** push your key to **+6+** so the lottery can give
Hero gear, keep running to fill the **8-dungeon vault** row (the real
upgrades), and stop treating crests/shards as a let-down — they're the
dependable half of M+ gearing. **Until then (week of Aug 11): one M0 clear of
each of the 8 dungeons, 292 apiece, weekly lockout.**

## TODO

- [ ] **Verify the whole per-key table in game from 2026-08-18** @verify-ingame
      — end-of-run ilvl and vault ilvl at +2 / +5 / +6 / +10. The table above
      is reconstructed, not sourced from Blizzard.
- [ ] **Confirm which key levels pay Hero vs Myth Mistcrests, and the count
      per run** @verify-ingame — no S2 table has been published; any guide
      still quoting S1 Dawncrest amounts is carrying dead data.
- [ ] **Confirm in-game:** does an **over-time / depleted** completion drop @verify-ingame
      **2** items or fewer? Sources state "2 on a timed clear" but are silent
      on depletion. (Carried over from S1 — still unanswered.)
- [ ] Confirm **Ascendant Voidshard drop count** per M+ run in S2 (and whether
      it scales with key level).
