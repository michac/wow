---
id: mplus
name: Mythic+ dungeons
goal: [gearing, rating]
venue: dungeon
group: group
cadence: weekly
time: standing
scope: character
status: invalidated   # PRE-SEASON: no keystones drop until 2026-08-18 — flip back to `active` that reset
gate: { type: mplus_weekly_lt, n: 8 }
breakpoint: { type: vault, track: mplus, thresholds: [1, 4, 8] }
reward: { type: [power], detail: "per-run loot + Season 2 crests + IO; fills the Vault's M+ column" }
time_blocks: 2
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - knowledge/planning/candidates.json
  - knowledge/endgame/mythic-plus/
  - https://worldofwarcraft.blizzard.com/en-us/news/24294369   # Midnight Season 2 overview (Tier 1)
  - https://us.forums.blizzard.com/en/wow/posts/29833350       # S1 ending / S2 pre-season information (Tier 1)
confidence: high
---
⛔ **Not rankable during the 2026-08-11 pre-season week — Mythic+ keystones do not drop
until the weekly reset of 2026-08-18.** Season 1 ended with the Aug 11 maintenance and
Season 2 opens a week later, so there is no key to run and no M+ column to fill. This
file is `status: invalidated` for exactly that reason; **flip it back to `active` (and
re-run `wowkb.gen_candidates`) on 2026-08-18**, when keystones begin dropping and the
Mythic+ difficulties open.

**What dungeons give you this week instead:** the Season 2 pool is already live on
**Heroic and Mythic 0**, and **Mythic 0 is on a weekly lockout for this week only**,
dropping **Champion 1/6 (ilvl 292)**. From Aug 18 M0 returns to a **daily** lockout
(still 292). That pre-season M0 clear is real gearing value but it is *not* this
activity — no keystone, no IO, no vault credit from the M+ column — and the catalog has
no separate M0/Heroic entry yet.

**Season 2 pool (8):** Altar of Fangs (new, 3 bosses, inside the Vaults of Atal'Utek) ·
Murder Row · Den of Nalorakk · The Blinding Vale · Voidscar Arena · Ruby Life Pools
(Dragonflight) · Kings' Rest (BfA) · Temple of Sethraliss (BfA). The three returning
dungeons ship with design/QoL updates. The Season 1 pool (Algeth'ar Academy, Magisters'
Terrace, Maisara Caverns, Nexus-Point Xenas, Pit of Saron, Seat of the Triumvirate,
Skyreach, Windrunner Spire) has rotated out.

**From 2026-08-18, unchanged in shape:** run keys for per-run loot, Season 2 crests
(Mistcrests) and IO score. Running them **also fills the Mythic+ column of the single
Great Vault** (slots at 1/4/8 runs) — that vault contribution is a `breakpoint` here,
**not** a separate activity. `goal` spans `gearing` and `rating`: above ~+10 the loot
flattens but IO keeps climbing, so completionists push past the gear breakpoint.
`breakpoint_R()` boosts the run that crosses the next threshold; R→0 once capped.
