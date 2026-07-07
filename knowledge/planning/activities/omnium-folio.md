---
id: omnium-folio
name: Omnium Folio weekly (Seeking Knowledge)
goal: [gearing, story]
venue: quest
group: solo
cadence: weekly
time: standing
scope: character
status: active
gate: { type: weekly_quest, quest: omnium_seeking_knowledge }
reward: { type: [power], detail: "empower a folio rune — the 12.0.7 player-power track" }
time_blocks: 1
patch: 12.0.7
fetched: 2026-07-07
reviewed: 2026-07-07
sources: ["https://worldofwarcraft.blizzard.com/news/24277442/", "knowledge/systems/omnium-folio.md", "yt:kUP8oqI7Ekc"]
confidence: medium
---
The **Omnium Folio** is 12.0.7's new runic-power progression system. You join **Magister
Umbric** and **Grand Magister Rommath** to restore the **Sunstrider Omnium**; the intro is
the **Magister's Missive** pickup in **Silvermoon City** (beside the Ritual Site vendors).
Once unlocked you're entrusted with the folio — a runic ledger opened from a **minimap
icon** — and empower your first rune. After the one-time unlock it's a **multi-week** track:
each week's *Seeking Knowledge* quest awards a Mote you spend to unlock/empower that week's
row (fully built in **5 weeks**; runes stay relevant the rest of Midnight).

**Account-wide since the 2026-06-25 hotfix:** from **Week 2** the Seeking Knowledge weekly's
quest *prerequisites* are account-wide — an alt no longer has to grind back up through the
earlier weeks to reach the current week's quest. Each character must still complete the
Sunstrider Omnium unlock questline to open the interface and run the weekly, which is why
this stays `scope:character`.

Tagged `goal:[gearing, story]` — it's real player power (`gearing`) delivered through a
weekly story step. **Do it early**: it's the one 12.0.7 addition tied directly to new
player power, so deferring it delays your power ceiling. `gate` is best-effort on the weekly
step ID — read the live log if it doesn't resolve. Full mechanics:
`knowledge/systems/omnium-folio.md`.
