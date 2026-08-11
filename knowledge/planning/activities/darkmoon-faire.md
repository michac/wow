---
id: darkmoon-faire
name: Darkmoon Faire (monthly)
goal: [collectibles, professions]
venue: world
group: solo
cadence: monthly
time: time-boxed
scope: account
status: active
gate: { type: event_active, match: "Darkmoon Faire" }
reward: { type: [currency, collectible, power], detail: "Darkmoon tokens → mounts/pets/heirlooms/transmog; +5 profession skill; +10% rep/XP WHEE! buff" }
time_blocks: 1
urgency: 1.5
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources: ["yt:rliFXbEHghU", "https://www.wowhead.com/event=479/darkmoon-faire", "https://boostmatch.gg/blog/wow/articles/wow-midnight-darkmoon-faire-complete-guide"]
confidence: medium
---
The monthly Darkmoon Faire on **Darkmoon Island** — runs the **first full week of each month
(starts the first Sunday, ~7 days)**. Unchanged by 12.1. **The live window is volatile — do
not read a hardcoded date out of this file**; `gate: { type: event_active }` is what decides
whether the ranker may surface it, so let the gate answer "is it up?". (For orientation only:
the August 2026 window was Aug 2–9, so the Faire is **down** as of 2026-08-11; the next one
starts Sep 6.) `time: time-boxed` + recurring → **U 1.5** (recurring-FOMO); `scope: account`
(the profession-skill and rep/XP quests are once-per-char but the *reason to go* — the Faire
being up — is a single account-wide window, counted once).

What to grab while it's up:
- **+5 profession skill** quest (per profession) — the `professions` tag and a real skill bump.
- **Pet-battle** quest.
- **WHEE!** ride + the **Darkmoon rep/XP buff** (+10%) — stacks with other XP buffs, so a
  Faire week is the cheap multiplier to stack on top of whatever alt-leveling event is up.
  ⚠ The old "pair it with Turbulent Timeways" advice is **dead**: Turbulent Timeways ended
  **2026-08-11** with the 12.1 patch (see `_meta/moving-values.md`).
- **Darkmoon Prize Tickets** from game/turn-in quests → mounts, pets, heirlooms, transmog at
  the ticket vendors (the `collectibles` payoff, R-floored via the U≥1.5 rule).
