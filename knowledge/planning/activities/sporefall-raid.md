---
id: sporefall-raid
name: Sporefall raid (Rotmire) — previous-tier weekly kill
goal: [collectibles]
venue: raid
group: group
cadence: weekly
time: standing
scope: character
status: active
gate: { type: raid_weekly, boss: rotmire, name_contains: Sporefall }
reward: { type: [collectible], detail: "Luminous Sporeglider mount (4× Delicious Sporesnacks, one per account per week) + Luminous Rotshroom housing decor; Sporefused gear (259–298) is Season 1 loot and a dead end — not current-tier progression" }
reward_ilvl_max: 285   # realistic pug ceiling (Heroic); Mythic 298 needs a guild. S1 items — see below
time_blocks: 2
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - "yt:0asUDe1lUPE"
  - "yt:bCgLtZrd5gQ"
  - https://www.wowhead.com/guide/midnight/raids/sporefall-overview-location-rewards-boss
  - https://us.forums.blizzard.com/en/wow/posts/29833350   # S1 ending / S2 information (Tier 1)
  - https://worldofwarcraft.com/en-us/news/24293281        # Curse of Ula'tek update notes (Tier 1)
  - https://news.blizzard.com/en-us/article/24295090       # Curse of Ula'tek pre-season details (Tier 1)
  - knowledge/endgame/raids/sporefall.md
confidence: medium
---
**⚠ Previous tier as of 12.1 (2026-08-11).** Season 1 ended with the week of Aug 11
maintenance; the Season 2 raid is **The Venomous Abyss** (8 bosses, Coiled Isle), which
opens **2026-08-18** on Normal/Heroic/Mythic + LFR Wing 1. Sporefall is still open and
still killable — it is simply **no longer current-tier progression**, so this row is
demoted from a `gearing` weekly to a `collectibles` weekly.

The 12.0.7 raid: a **single-boss** encounter vs **Rotmire**, in Harandar near the Grudge
Pit delve (/way 73.7, 66.5). RF → Mythic, ilvl **259–298** (RF 259 · Normal 272 · Heroic
285 · Mythic 298). Notable as WoW's first **Mythic Flex** raid — Mythic scales for 15–25
players.

**Why you'd still go: the collectibles.** The **Luminous Sporeglider** mount costs 4×
**Delicious Sporesnacks**, earned **once per week, per account**, by killing Rotmire on
*any* difficulty — so LFR is enough, and a second character's kill adds nothing to it.
The **Luminous Rotshroom** housing decor drops here too. That per-account weekly cadence
is the real shape of this activity now; the `character`-scoped raid lockout only still
matters if you are chasing the loot.

**The gear is a dead end.** Sporefused pieces are **Season 1 items**. Season 2 crests are
**Mistcrests** and Season 1 Nebulous Voidcores were **converted to gold at the end of
Season 1 and can no longer be used in Season 1 content** — so there is no bonus roll here
and no visible path to keep upgrading what drops. Blizzard stated the freeze explicitly
only for Val/Naigtal World Boss drops and the "Knocking off the Top (Heroic)" rewards;
whether a Sporefused drop can still take an upgrade at all is unconfirmed — treat every
piece as terminal at its drop ilvl until proven otherwise. @verify-ingame

Narrow exception, **pre-season week only (Aug 11–17)**: Season 2's ceiling this week is
low — Mythic 0 at Champion 1/6 (**292**), Delves capped at Adventurer 3/6, lairs/Hard
Prey/Pinnacle Caches at Season 2 Veteran — so a Heroic (285) or Mythic (298) Rotmire kill
can still be a raw-ilvl upgrade for an undergeared character. That is what `reward_ilvl_max`
still expresses, and it self-cancels once the slot is above it. From **Aug 18** the
Venomous Abyss supersedes it outright.

**The vault breakpoint is removed.** This row used to carry
`breakpoint: {type: vault, track: raid, thresholds: [2,4,6]}` — two Rotmire kills across
difficulties filling the Great Vault's raid column. With Season 1 over, the raid row is
expected to track the **Season 2** raid, and pre-season week has **no raid at all** in the
Aug-11 content set; Season 2 vault credit accrues now for rewards claimable Aug 18. Rather
than keep ranking Sporefall as a vault-slot filler that may award nothing, the breakpoint
is dropped. Blizzard never stated this either way — **confirm at the first Season 2 vault
(week of Aug 18) whether previous-tier kills still tick the raid row**, and restore the
breakpoint (pointed at the Venomous Abyss) if they do. @verify-ingame

Also note the 12.1 raid-vault retier when the Venomous Abyss row is authored: LFR/Normal/
Heroic vault rewards now arrive at **the first step of the next harder difficulty's track**
(every Heroic-raid vault reward is Myth 1/6), Mythic raid vault rewards at **Myth 6/6**,
and Very Rare items plus the penultimate/final boss loot at **Myth 9** whether from the
boss or the vault. The Voidcore raid re-roll cost also dropped to **1** (was 2) — for
Season 2 content, not here.

The fight itself is unchanged: one repeating phase (add-cleave → Fungal Bloom →
bursting-shroom soak); see `endgame/raids/sporefall.md` for the mechanics distilled from
the RCP/Tactyks guides. `group`-gated (E 0.7), which now sits it below solo weeklies at
essentially all times.

**Gate resolution (Phase 0).** `raid_weekly` resolves from the dump's raid lockouts
(`GetSavedInstanceInfo`) — "done" once Sporefall shows as a saved raid with ≥1 boss
defeated, instead of falling through to `unknown`. The match keys on the instance name
containing **"Sporefall"**; confirm the live lockout string is exactly that (localized
name) so the gate fires. @verify-ingame

**Difficulty is a within-activity axis, not a facet.** This catalog is one row per activity
(like `mplus`, which spans key levels), so difficulty stays *inside* the row — the front
matter carries only the ilvl *span* (259–298), and the per-difficulty reward map lives in
the reference file (`endgame/raids/sporefall.md`).
