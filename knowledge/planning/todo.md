---
title: Session TODO — manual check-off (this reset)
patch: 12.0.7
fetched: 2026-07-06
sources:
  - knowledge/planning/activities/
confidence: high
---

# Session TODO

> **How this works (for now).** The planner populates this list each reset from the
> ranked shortlist; you tick boxes by hand as you go. It's the **self-report** tier
> for activities the game/API/addon can't detect as done (`gate: manual`, unresolved
> quest IDs, account-wide chores).
>
> **Eventual goal:** extend the **PlannerState** addon so you can check these off
> **in-game** (an FTA-style checklist UI), and the planner reads that state back
> instead of you editing markdown. Until then, this file is the ledger.

## Legend
`- [ ]` todo · `- [x]` done this reset · `~` low-confidence / needs in-game verify

---

## Account-wide (do once across the roster)
- [ ] Trading Post monthly — punch card → Trader's Tender

## Encomplete (main — geared)
- [ ] _populated by `wowkb.plan` — run the planner to fill this_

## Hallick (gearing alt)
- [ ] _populated by `wowkb.plan`_

## Uncomplete (leveling)
- [ ] _populated by `wowkb.plan`_

---

_Reset: markdown checkboxes are cleared/regenerated when the planner runs after a
weekly reset (Tuesday). Manual entries you add above the generated block survive._
