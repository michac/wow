---
id: ritual-sites
name: Ritual sites (Hero crests + accolades)
goal: [gearing]
venue: world
group: solo
cadence: repeatable
time: standing
scope: character
status: active
gate: { type: always }
reward: { type: [power, currency], detail: "Hero crests + accolades (T5); T6 pays 5 Myth + 10 Heroic Dawncrests/run — the only repeatable SOLO Myth-crest farm; steady solo engine" }
yields: { currencies: { hero_crest: 10, myth_crest: 5, field_accolade: 100 } }   # T6/run; Myth crest = the needs-first draw (dawncrests.md)
time_blocks: 1
enjoyment: 1.2
urgency: 1
patch: 12.0.7
fetched: 2026-07-06
reviewed: 2026-07-07
sources: [knowledge/planning/candidates.json, knowledge/systems/ritual-sites.md]
confidence: high
---
Farmable solo power engine — no weekly reset (`cadence: repeatable`), always available
(`gate: always`, U=1). Low urgency by design: it never expires, so it fills time after
the expiring weeklies are cleared.

**T6 is the Myth-crest promotion (Phase 0, needs-first redesign).** Tier payout climbs:
T5 ≈ 20 Hero crests + Field Accolades solo; **T6 (UI-recommended ilvl ~274) pays 5 Mythic
+ 10 Heroic Dawncrests per run** — the **only repeatable *solo* source of Myth crests**
(otherwise M+ / raid / gilded stash only). That lifts this out of the "steady Hero filler"
backlog: for a Myth-crest-bottlenecked geared main (Encomplete: 20 Myth, gating the crafted
waist + staff recraft), **T6 ritual sites is the top play** under needs-first scoring — a
deterministic, repeatable Myth-crest engine that beats another random Hero drop. See
`../../systems/ritual-sites.md` (Rewards) and `../../endgame/dawncrests.md`. The pre-needs-first
formula keeps U=1 (it never expires); the promotion is realized when the currency-need
scoring loop lands (Phases 1–2) — this row is a designated Myth-crest yield for it.
