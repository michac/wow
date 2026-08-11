---
title: Ruby Life Pools — Midnight S2 M+ dungeon (STUB)
patch: 12.1
build: 12.1.0.69214
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.com/en-us/news/24294369   # "Midnight Season 2" overview — S2 dungeon pool + returning-dungeon callout (tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281   # 12.1 "Curse of Ula'tek" Content Update Notes (tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350  # S1 ending / S2 pre-season schedule (tier 1)
  - https://us.api.blizzard.com/data/wow/journal-instance/1202  # journal-instance 1202 — expansion, map, encounter list (tier 1 game data)
confidence: low
---

# Ruby Life Pools — Midnight Season 2 Mythic+

> ⚠ **STUB, written on patch day (2026-08-11).** Everything below is Tier-1 only:
> official notes plus the Blizzard journal API. There is **no route, no trash
> table, no boss-ability table and no loot list here yet** — see `## TODO`. The
> sibling files in this directory (e.g. `skyreach.md`) show the shape this file
> should grow into.

Dragonflight dungeon in **The Waking Shores**, returning to the Mythic+ rotation
for **Midnight Season 2**. Three bosses. Journal instance **1202**, map **2521**,
expansion **Dragonflight** (Blizzard journal API, static namespace at 12.1).

## What is confirmed (Tier 1)

- **In the Season 2 Mythic+ pool** — one of eight: Altar of Fangs (new) · Murder
  Row · Den of Nalorakk · The Blinding Vale · Voidscar Arena · **Ruby Life
  Pools** · Kings' Rest · Temple of Sethraliss.
- Blizzard lists it under **"Returning dungeons with design and quality of life
  updates"** and **does not enumerate the updates** in the content-update notes.
  That callout is the whole of the official statement.
- **Availability is dated** (see `season-2-overview.md` for the full split):
  - **Week of 2026-08-11 (pre-season, live now)** — Heroic and **Mythic 0 only**.
    M0 is on a **weekly** lockout this week only and drops **Champion 1/6 (292)**.
    **No keystones drop**, so there is no Mythic+ Ruby Life Pools yet.
  - **Week of 2026-08-18** — Mythic+ opens, keystones begin dropping, M0 returns
    to a **daily** lockout.
- Timed **Mythic 10+** grants the dungeon teleport, as for all eight S2 dungeons.

## Bosses (names only)

Corroborated against Blizzard journal-instance 1202. **Abilities are deliberately
not listed** — they are exactly what the "design and quality of life updates"
may have changed.

| # | Boss | Journal encounter |
|---|---|---|
| 1 | **Melidrussa Chillworn** | 2488 |
| 2 | **Kokia Blazehoof** | 2485 |
| 3 | **Kyrakka and Erkhart Stormvein** | 2503 |

## Why pre-12.1 guides are suspect here

Two independent reasons, both Tier-1:

1. Blizzard explicitly re-worked this dungeon for its return but published no
   list of changes, so any Dragonflight-era or Season-1-era route/trash/boss
   guide is unverified against the shipped version.
2. 12.1 raised **max-level player health and enemy damage by 25%** game-wide
   ("Curse of Ula'tek" developers' note) with encounter abilities hand-tuned
   alongside. Every absolute damage number in an older guide is wrong.

## TODO

Fill this file to the shape of `skyreach.md` (Route → Trash → Bosses → DPS
notes, with the archetype/tier/role columns that feed
`systems/mechanic-archetypes.md` and `projects/mplus_memory/`). Intended
sources, in trust order:

- **Tier 1** — `wowkb.blizzard journal-encounter 2488 / 2485 / 2503` for the
  shipped 12.1 ability lists per boss (this is the one source that reflects the
  rework rather than describing the old dungeon). Also `wowkb.wago` for the
  dungeon's `MapChallengeMode` timer, which is **not** stated in the notes and
  must not be taken from editorial prose.
- **Tier 1** — the 12.1 verbatim archive `_meta/patch-notes/12.1.md`; re-grep it
  for a "Dungeons and Raids" per-dungeon section if one is added by hotfix.
- **Tier 3** — `method.gg` and `icy-veins.com` Ruby Life Pools guides, once they
  are re-authored for Midnight S2. ⚠ On 2026-08-11 these are **not yet updated**;
  a page that still reads as a Dragonflight guide must not be distilled here.
  Require a "Midnight" / "Season 2" / 12.1 signal before using one.
- **Tier 3/4, corroborate only** — Wowhead's PTR write-ups
  (`wowhead.com/news/quality-of-life-changes-for-ruby-life-pools-and-temple-of-sethraliss-in-midnight-382252`,
  `.../first-look-at-new-ruby-life-pools-in-mythic-season-2-382213`) describe the
  **PTR** build, not necessarily what shipped. Use them to know what to go look
  for in the journal data — never as the claim itself.
- Once M+ opens on **2026-08-18**, a run of the dungeon plus a `wowkb.youtube`
  transcript of a S2 walkthrough (the S1 files used Dalaran Gaming's) is the
  practical way to get the route.

Until then: **do not** assert a route, a pull order, an affix interaction, a
timer, or a loot table for this dungeon.
