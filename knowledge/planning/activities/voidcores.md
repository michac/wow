---
id: voidcores
name: Buy + spend 2 Nebulous Voidcores
goal: [gearing]
venue: meta
group: solo
cadence: weekly
time: standing
scope: character
status: active
gate: { type: manual }
reward: { type: [power], detail: "bonus-roll hero gear from delves/prey" }
reward_ilvl_max: 276   # Hero bonus-roll (Hero ceiling 276) — worthless once every slot is Hero-capped
time_blocks: 0.5
patch: 12.0.7
fetched: 2026-07-07
reviewed: 2026-07-07
sources:
  - knowledge/planning/candidates.json
  - https://www.wowhead.com/guide/midnight/the-voidforge-patch-12-0-5-bonus-loot-rolls-upgrades
confidence: medium
---
Buy 2 Nebulous Voidcores and spend them on bonus rolls for hero-track gear off delve/prey
content. `gate: manual` — no clean weekly signal yet, so it stays surfaced (self-report
until the addon can track the purchase). Candidate for slot-targeting (v2b).

**No `yields.currencies` (needs-first Phase 1).** A voidcore bonus-roll *spends* the
currency and yields a Hero-track **gear** piece — already valued by `reward_ilvl_max: 276`
via `slot_target_R` (→ 0 for a Hero-capped main). There's no crest/accolade currency to
declare here; the deterministic-vs-RNG treatment of the roll is a Phase-3 concern.
