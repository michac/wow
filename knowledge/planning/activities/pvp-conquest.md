---
id: pvp-conquest
name: Weekly Conquest (rated PvP)
goal: [gearing, rating]
venue: pvp
group: group
cadence: weekly
time: standing
scope: character
status: active
gate: { type: manual }
breakpoint: { type: vault, track: pvp, thresholds: [1, 4, 8] }
reward: { type: [power, currency], detail: "Conquest → Champion/Galactic Gladiator gear + tier; fills the Vault's PvP column" }
time_blocks: 2
patch: 12.0.7
fetched: 2026-07-07
reviewed: 2026-07-07
sources: ["yt:6OkVWEdttZ0", "https://www.icy-veins.com/wow/midnight-pvp-gearing-guide", "https://conquestcapped.com/guides/wow/pvp-gearing/", "https://news.blizzard.com/en-us/article/24276957/hotfixes-june-12-2026"]
confidence: medium
---
Rated PvP — 2v2/3v3 Arena, **Solo Shuffle**, and **BG Blitz** — for **Conquest**. The
weekly Conquest **cap was removed** for the rest of Season 1 (hotfix 2026-06-12), so it no
longer gates a fixed weekly amount — grind as much as you want. Conquest buys Champion-track gear and converts into tier
pieces (rush the 4-set); PvP gear gets a **+9 ilvl bump in rated instances** (12.0.7), and
rated wins **fill the PvP column of the single Great Vault** — a `breakpoint`, not a
separate row. `goal:rating` too: Galactic Gladiator (Gore Drake mount) at 2300, elite set
at 1800, weapon illusion at 1950 — score-chasing above the gear payoff.

Vendors cluster in **southwest Silvermoon** (near Falconwing Square). `venue:pvp` default E
(0.4) keeps it deprioritized for this PvE-leaning roster; the per-char rating goal is what
surfaces it for a dedicated pusher. `gate: manual` — no clean conquest-cap signal in the
dump yet (surfaces + self-report).
