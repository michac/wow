---
description: Plan how to gear up / accomplish goals for a character — pull all 3 sources (PlannerState /ps dump + Blizzard API + Syndicator) via the tools, then synthesize, instead of re-reasoning from the KB
argument-hint: "<name> [realm] — the character to plan for (realm defaults to kiljaeden)"
---

# /plan-character — the front door for "how do I gear up / progress <char>"

**Route character gear/goal questions through the tools first.** They already
union the three sources the KB has on a character — don't re-derive a gearing
chart from `knowledge/` by hand when `wowkb.plan` computes it from live state.

The three sources (see `CLAUDE.md`):
1. **PlannerState `/ps` dump** — reset-state the API can't see (weeklies
   done/not, vault progress, world-boss kills, active events) + an equipment/
   currency mirror. The **offline spine**.
2. **Blizzard profile API** — item names, specs, professions, renown, raid/M+.
3. **Syndicator** — authoritative gold + full currency table.

`wowkb.charstate.load` unions all three (graceful offline fallback); both
`wowkb.character` and `wowkb.plan` consume it.

Character: **$1**  ·  realm: **$2** (default `kiljaeden`).

## Step 1 — Ask the character to `/ps` + `/reload` if they can
The `/ps` dump is what carries this-reset progress. If the user is in-game on
$1, have them type `/ps` then `/reload` so the dump (and Syndicator currencies)
are current. If they can't, the tools still run — the API + a prior dump degrade
gracefully; just flag that reset-state may be stale.

## Step 2 — Pull the unified snapshot + both plan views
From `tools/`:

```bash
uv run python -m wowkb.character $1 --realm ${2:-kiljaeden}     # snapshot incl. "This reset" section
uv run python -m wowkb.plan --gear --character $1               # per-slot cache/crest chart + accolade heuristic
uv run python -m wowkb.plan --minutes 60 --character $1         # ranked session activities (what to DO this reset)
```

- `--gear` emits the gearing chart (BAND 1 sub-Champion / BAND 2 Champion /
  BAND 3 Hero+, plus the accolade-allocation heuristic). **Start here for
  gearing questions.**
- the session view gates activities by what's already done this reset.
- Add `--no-enrich` for a fast offline run (dump only); drop it for the full
  union. `wowkb.plan` also auto-logs any weekly it sees in the `/ps` quest log
  that the addon doesn't track yet → `knowledge/planning/discovered-weeklies.json`
  (verify + promote per that file's note).

## Step 3 — Synthesize, don't reinvent
Take the tool output as the spine and add only what it can't compute:
- **Cross-character / warband** moves (caches are warbound — a geared main can
  farm Field Accolades and mail slot-specific Champion/Hero caches to $1; crests
  are **not** transferable). The `--gear` chart is single-character; the warband
  routing is yours to add.
- **KB colour** — cite the live patch + a source per the staleness doctrine;
  pull specifics (quest names, vendor costs, tier mechanics) from `knowledge/`.
- **Track caveat** — the profile API doesn't expose the numeric upgrade track,
  so the chart infers Champion/Hero from ilvl bands. If the user hovers a piece
  in-game and the real track differs, adjust.

## Step 4 — Offer to persist
If the plan is substantive, offer to write / update `knowledge/characters/<name>-plan.md`
(mirrors `encomplete-plan.md` / `uncomplete-plan.md`) so it's a living checklist.
Don't touch the `*-kiljaeden.md` snapshot here — that's `/sync-characters`' job.
