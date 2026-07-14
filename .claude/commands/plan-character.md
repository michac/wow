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

## Step 2 — Pull the goal BOARD (the deterministic facts) + the other views
From `tools/`:

```bash
uv run python -m wowkb.plan --board --character $1 --json       # ← the goal board (per-slot candidates + warband gates/cross-char facts)
uv run python -m wowkb.character $1 --realm ${2:-kiljaeden}     # snapshot incl. "This reset" section
uv run python -m wowkb.plan --gear --character $1               # per-slot cache/crest chart + accolade heuristic
uv run python -m wowkb.plan --minutes 60 --character $1         # ranked session activities (what to DO this reset)
```

- **`--board` is the primary input for gearing goals.** It emits, per slot, the
  enumerated **upgrade candidates** (crest-up / craft / catalyst / Maren / renown)
  with **affordability from the live mat pool**, plus the warband **gate states**
  (Champion 50% discount live? M+ unlocked?) and **cross-char facts** (each toon's
  sub-263 count + pooled mats). It reports **facts only** — it does not rank or
  sequence. Add `--json` for the full structured board (drop it for a human view).
- `--gear` is the older per-band chart; `--board` supersedes it for goal planning
  but the accolade heuristic is still handy colour.
- the session view gates activities by what's already done this reset.
- Add `--no-enrich` for a fast offline run (dump only — spark/voidshard counts
  degrade to absent, flagged); drop it for the full union. `wowkb.plan` also
  auto-logs any weekly it sees in the `/ps` quest log that the addon doesn't track
  yet → `knowledge/planning/discovered-weeklies.json` (verify + promote per that
  file's note).

## Step 2b — Reason over the board (the agent's job, per goal-model.md)
Read `knowledge/planning/goal-model.md` — it is the **rubric**. The board is the
deterministic facts; **you** supply the judgment the tool deliberately doesn't:

1. **Pare** each slot to its one best actionable goal (one slot → one goal).
2. **Cluster** same-path slots into a single goal (e.g. "cap Champion across the
   dozen 246 slots" is one goal, not twelve); a slot earns its own goal only with a
   *distinctive* path (tier slot needing catalyst; a Maren/craft jump).
3. **Rank** goals coarsely by **value ÷ steps** (the board's `affordability` = steps).
4. **Sequence around the two gates** — the economic Champion-discount gate (hold alt
   Champion *spends* until an enabler earns *Champion of the Dawn*; the board names the
   cheapest character) and the hard M+ gate.
5. **Decompose** the selected goals into deduped session TODOs (one step often serves
   several goals — that's where the efficiency lives).

Produce: the ranked goal list, the cross-char plays (who enables whom — the board's
`cheapest_to_gate_champion` + pooled mats are your evidence), and the session TODOs.

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
