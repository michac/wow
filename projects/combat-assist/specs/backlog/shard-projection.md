# Shard projection — anticipate the post-cast Soul Shard count

**What this file is for:** the plan for one committed backlog item. `backlog.md` → `## Now`
carries the one-line entry that points here; this file holds the steps and the traps. It is
deleted when the work lands and `notes.md` records the round.

## What it does

Demonology, three abilities, one number. While a Shadow Bolt, Infernal Bolt or Hand of Gul'dan
is in flight, `world.resource` reads the count the cast will *leave* you at rather than the one
you have — so every shard cue already in the catalog (the five-shard Tyrant hold **A**,
Demonbolt's overcap **B**, Hand of Gul'dan's starved **E** and banking **F**, the Demonbolt /
Infernal-Bolt yield **D**) becomes anticipatory with no catalog edit.

Shards do not move until the cast finishes, so the whole window between `START` and `SUCCEEDED`
is one cap can speak into. All three abilities have a real cast time (~2s / ~2.3s / ~1.5s); an
instant has nothing to anticipate, which is why the roster is these three.

**Nothing here is sealed.** Soul Shards are one of the seven never-secret power types
(`security-taint-and-restricted-data.md` §4.12), so this is ordinary readable arithmetic: no
sealed sink, no curve, no new vocabulary, no shelf or `render-tokens.json` edit.

**The projection REPLACES the core value rather than sitting beside it.** A second term would
double the grammar and make every future marker author choose; one value means the anticipation
is uniform and there is nothing to keep in sync. The flight judges whether that is too eager.

## The steps

1. Add a shard-delta table to `Catalogs/Demonology.lua` — Shadow Bolt `+1`, Infernal Bolt `+3`,
   Hand of Gul'dan `−3` (`knowledge/classes/warlock/demonology/abilities.md:115-118`).
2. Register the six player cast events in `Sense.lua`: `UNIT_SPELLCAST_START` arms that spell's
   delta; `SUCCEEDED`, `STOP`, `INTERRUPTED`, `FAILED` and `FAILED_QUIET` clear it.
3. Change `readResource()` (`Sense.lua:120-126`) to return `clamp(live + Σ pending, 0, max)`,
   falling back to the live value if any pending spellID reads secret.
4. Cut a release, fly it, and tweak the numbers and the clear-conditions against what is seen.
5. Once it is right: the `spec.md` line, the `notes.md` round, and the
   `cdm-rider-patterns.md` §9.2 rewrite (below).

## What this rests on, and the KB claim it contradicts

`cdm-rider-patterns.md` §9.2 says a player cast's `spellID` is sealed under restriction and that
*"the one in-client reading on record was taken unrestricted."* Both halves are wrong: CDMProbe
measured **readable spellIDs in all four phases, 0 secret across 178 events, in a delve, in
combat** (`projects/cooldown-hud/docs/notes.md:32`). §9.2 is reasoning from the Tier-1
`SecretWhen*` annotation over a measurement that contradicts it.

⚠ The measurement is **12.0.x (2026-07-21)** and 12.1 reworked secret plumbing, so it is not
re-confirmed on the live build. That is not a gate on this work: if the id reads secret, step 3's
fallback means the projection never arms and cap behaves exactly as it does today — the failure
is visible on the first flight. **The §9.2 rewrite waits for that flight** and then deletes the
claim rather than appending a note.

## Traps, all of them recorded by the prior art

CDMProbe shipped the incoming half of this (`roster-state-plan.md:1205-1260`); the spend half was
its unbuilt item 7 (`docs/archive/milestones.md:1932`).

- **Do not build a double-deduction guard.** CDMProbe had one — a `UnitPower` snapshot at `START`,
  suppressing the spend once the live value fell below it — and deleted it deliberately: it leaked
  (a secret terminal event left the entry alive into the next cast, silently under-projecting for
  a whole flight window) and it was already wrong for a multi-power spec. The accepted cost is a
  stale −N for at most one tick, because `SUCCEEDED` supersedes on the very next pulse.
- **`STOP` is load-bearing** and reads like a dead registration from inside the module — it is the
  only thing that cancels a mid-flight spender.
- **A pending delta that cannot be resolved is UNKNOWN, never 0.** A zero-coerced resource inverts
  every comparison at once: every spender affordable, every generator pointless. This is
  `absent-is-never-zero` on a rail (§4.3).
- **The casting row projects against itself** — Infernal Bolt cast at 1 shard makes the projection
  4, so an overcap marker on that row can light while the cast is still in the air. Honest, or
  noise; the flight decides.
