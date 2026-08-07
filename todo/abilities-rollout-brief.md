# Brief — rewriting `abilities.md` into the two-section shape

**Read this fully before editing anything. Then read the template:
`knowledge/classes/warlock/demonology/abilities.md`.** That file is already done and
is the shape you are reproducing. Do not edit it.

---

## What you are doing, and why

Each `knowledge/classes/<class>/<spec>/abilities.md` is hand-written prose that
restates, per ability, what the **generated** sibling `ability-inventory.md` already
carries — spellID, cooldown, cast time, origin, talent/hero placement and the full
in-game tooltip, DB2-pinned to `12.0.7.67808` and regenerated on patch day.

The restatement is worse than redundant. It was authored from **Tier-3 guides**, its
numbers were guesses, and each guess got an `@verify-ingame` marker. Those markers
are landmines: the workspace rule is *"a marked claim you are about to build on is a
STOP: ask"*, so an agent researching a spec halts on a marker whose question game
data could have answered in a minute. That has already cost a real session.

You are replacing the prose with **only the two things the generated file
structurally cannot say.** It is a *join* — a row exists there because a Tier-1
acquisition table says the spec **learns** the spell — so it can only ever list what
**is**.

---

## The output: four sections, nothing else

Copy the structure from the Demonology template exactly.

1. **Front matter** — `title`, `patch: 12.0.7`, `fetched: 2026-08-06`,
   `reviewed: 2026-08-06`, `sources:` (only sources you actually used), `confidence`.
2. **A short intro + a ⛔ stop block** routing the reader: facts →
   `ability-inventory.md`; rotation → `rotation.md`; talents/hero pick →
   `builds.md`. State the spec's row count. Say both sections here are **closed
   lists, not backlogs**.
3. **`## §A — Real buttons the inventory cannot see`** — table
   `| spellID | name | how we know, and why the join misses it |`
4. **`## §B — Encountered, and we believe not valid`** — table
   `| name | verdict | evidence |`

Optionally, only if you have something real for them:

5. `## Corrections this file has already made` — keep a correction **only** where
   re-asserting the wrong thing is a likely failure mode.
6. `## Open in-game questions` — see the marker rules below. Usually **None**.

Target **60–110 lines**. If you are over, you are keeping restatement.

---

## ⛔ HARD RULES

### R1. §A is prescribed. Reproduce your mandatory rows VERBATIM.

Your prompt lists the mandatory `name` values for each of your specs. These are that
spec's current `prose-only` rows in `knowledge/classes/_abilities/section-4-catalogue.tsv`
— machine-tracked unknowns whose **only** record anywhere is the prose you are
replacing.

- Every mandatory name **must** appear in §A's `name` column, **spelled exactly** as
  given. Not reworded, not split, not merged, not "corrected".
- Some are obvious harvest artifacts (`Guardian's`, `Call Pet 1 … Call Pet 5`).
  **Keep them anyway.** Say in the note that it looks like an artifact. Do not fix it
  — a separate deliberate pass handles that. Not losing data and improving data are
  different jobs, and mixing them is how things vanish.
- If your spec has **no** mandatory rows, §A may be empty — write
  `_None known for this spec._` and keep the heading.
- You may **add** a row to §A if you find a real button in the old prose that the
  generated inventory lacks. Verify absence first (see R4).

### R2. §A's heading and table are a MACHINE INPUT.

`wowkb.gen_abilities._inventory_names()` harvests §A's `name` column and feeds it to
the `prose-only` leg of `section-4-catalogue`. The heading is matched on the word
**`inventory`** — which is why the template's heading is
`## §A — Real buttons the inventory cannot see`.

- **Use that exact heading text.** Rename it and every row silently vanishes from the
  catalogue, with no marker and no warning.
- Keep the `| spellID | name | ... |` header row — the harvester finds the column
  named `name`. Lead with `spellID` as the template does.
- **§B must NOT contain the word `inventory` in its heading.** It asserts the
  opposite; harvesting it would record "not an ability" as "an asserted ability".
- Do not put an ability-name table under any other `inventory`-matching heading.

### R3. `@verify-ingame` — delete almost all of them.

A marker belongs **only** on a question that genuinely cannot be answered from game
data, i.e. you must be logged in and looking at it.

- *"The exact cooldown / cast time / resource cost is uncertain"* is **NOT** such a
  question. `ability-inventory.md` has the Tier-1 number. **Delete the marker and the
  guess together.**
- *"Is X on the tree?"* is **NOT** such a question — `knowledge/classes/_talents/all-talents.tsv`
  answers it. Resolve it and put the result in §B.
- If you keep one, put it on its own physical line (`gen_verify` truncates to one
  line) and state the question precisely.
- ⚠ Backticked `` `@verify-ingame` `` is NOT harvested; bare is. Don't add bare ones
  in explanatory prose.

### R4. Never assert without checking. Three cheap Tier-1 checks:

```bash
# is it in the spec's generated inventory?  (name, spellID, cooldown, cast, tooltip)
grep -i '<name>' knowledge/classes/<class>/<spec>/ability-inventory.tsv

# is it a talent anywhere, for any spec?
grep -i '<name>' knowledge/classes/_talents/all-talents.tsv

# is it reached indirectly, or already catalogued?
grep -i '<name>' knowledge/classes/_abilities/section-3-corroborated.tsv
grep -i '<name>' knowledge/classes/_abilities/section-4-catalogue.tsv
```

- **A `SpellName` hit is not evidence a spec can cast something** — that table keeps
  retired spells indefinitely. Only an acquisition table settles it.
- **A spell-API 404 is not evidence of absence.**
- **"Not in any data table" is almost always wrong.** Before calling something
  absent, check a **sibling spec of the same class** — a shared hero tree makes a
  one-sided gap likely.

### R5. Do not migrate rotational or build judgement.

"Press at 5 shards", "hold this for the burst window", "the S1 meta pick" — all of it
belongs to `rotation.md` / `builds.md`, which already exist and are better sourced.
**Check the sibling actually covers it before dropping it** (`grep` the sibling). If
the sibling is *wrong* or contradicts a Tier-1 finding, do not silently delete —
report it in your ESCALATIONS (below). Siblings have been measured stale before.

### R6. Scope.

- **Edit only the `abilities.md` of the specs named in your prompt.** Nothing else.
  Not the generated files, not `rotation.md`, not `builds.md`, not the tools.
- Do not run any `wowkb` generator. The orchestrator regenerates and verifies once.
- A backup of every original is already at `todo/abilities-pre-rollout-2026-08-06/`.

---

## What §B is for

Names that appear in guides, older builds, or other people's notes, which you have
**checked** and believe are not part of this spec at 12.0.7. Each row needs real
evidence — an `all-talents.tsv` miss across every spec, an API tree enumeration, a
rename. This is the section that stops the next reader re-running your check, so the
evidence column matters more than the verdict.

Good sources for §B rows: the old file's "Not on the Midnight X tree" / "Not
acquirable" / "Name reconciliation" sections, and any claim of the form "X was
removed / renamed / no longer exists".

If the old file has none, write `_None recorded for this spec._`

---

## Report back

Return a short structured report, not prose:

- `SPEC` — one line each: old line count → new line count, markers before → after.
- `SECTION_A` — the names you wrote, and confirmation each mandatory name is present
  verbatim.
- `SECTION_B` — the names you wrote.
- `DROPPED` — anything you removed that you were not fully confident was redundant.
- `ESCALATIONS` — sibling files that contradict a Tier-1 finding, contradictions you
  could not resolve, or anything you were tempted to fix but left alone.

Be honest in `DROPPED` and `ESCALATIONS`. A quiet deletion is the failure mode this
whole exercise exists to prevent.
