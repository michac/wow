---
title: Active characters — the planner's roster
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/encomplete?namespace=profile-us
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/hallick?namespace=profile-us
  - https://us.api.blizzard.com/profile/wow/character/kiljaeden/uncomplete?namespace=profile-us
  - knowledge/characters/encomplete-kiljaeden.md
  - knowledge/characters/hallick-kiljaeden.md
  - knowledge/characters/uncomplete-kiljaeden.md
confidence: high
---

# Active characters

> **Editable by hand.** This is the roster the planner scores across. Add/remove
> rows as your rotation of "characters I actually play" changes — the planner reads
> `active: true` rows only. Snapshots (ilvl, renown) are volatile; re-sync with
> `/sync-characters` and treat the numbers here as last-known, not live.

## Roster

| active | name | realm | class / spec | role | stage | focus (goals) |
|---|---|---|---|---|---|---|
| ✅ | Encomplete | Kil'jaeden | Warlock / Demonology | DPS | **main — geared** | gearing, rating |
| ✅ | Hallick | Kil'jaeden | Druid / Feral | DPS | gearing alt | gearing, collectibles |
| ✅ | Uncomplete | Kil'jaeden | Demon Hunter / Devourer | DPS | gearing alt | gearing |

`focus` biases which goals matter for that character — a leveling alt weights
`goal:leveling` activities up; a geared main weights `gearing` down once its
breakpoints are capped. (The scorer can use this to break cross-character ties.)

## Why the roster is a first-class input (the v2 payoff)

With one hour in the 12.1 pre-season week (Aug 11–17: no Mythic+ keys until Aug 18),
a per-character weekly like `lair-tidebound-grotto` scored **per character** can put
"run the Grotto on Uncomplete" above a grindy capped weekly on Encomplete — because
the alt is `stage: gearing` and the lair's weekly lockout is per character and still
unclaimed there. `scope: account` activities
(Trading Post) are scored **once** for the whole roster; `scope: character` activities
are scored for **each** active row and compete in one global ranking.

## Maintenance

- Seeded 2026-07-06 from the three `knowledge/characters/*.md` snapshots.
- Re-checked 2026-08-11 (12.1 sweep): Uncomplete hit the level cap (90) and is
  gearing on **Devourer** (Annihilator), so his row moved `leveling → gearing alt`;
  Hallick is also 90 (cap) but still at fresh-90 ilvl, so he stays a gearing alt.
- Re-verify class/spec/stage after a spec change or when an alt graduates from
  leveling to gearing (move its `stage`, re-weight `focus`).
- ilvl/renown intentionally omitted here — they're volatile; the planner pulls live
  state from the PlannerState dump + profile API at run time.
