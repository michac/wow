# Devourer — get it into the preview

> ⛔ **SUPERSEDED 2026-08-27. Every blocker in this file is closed and two of its load-bearing
> claims are false.** It is kept only until the migration artifacts are closed out
> (`backlog.md` → *Close out the migration artifacts*); read `devourer/catalog.md` and
> `devourer/scenarios.md` for the current state, and nothing here in the present tense.
>
> The two false claims, named so a reader who skips to §3 is not misled:
>
> 1. **There is ONE virtual row, not two** (§3, and the "author decision" below). Collapsing Star
>    was measured in game on 2026-08-27 to be a spell **override** on the Void Metamorphosis row —
>    an override borrows the row of the spell it replaces, so R7 draws it and it is not cap-owned.
>    **Consume is the only virtual row and it is `standing`.**
> 2. **Virtual rows do NOT draw inline.** V12 shipped as `Panel.lua`, a separate strip of
>    cap-owned icons. The 2026-08-19 decision below was reversed by the build.
>
> The preview is registered, carries **11** scenarios, and Devourer is migrated to `catalog.json`.

**Temporary migration artifact**, like `simplification-plan.md` beside it. Not a product
authority. Delete it when Devourer's preview is registered and reviewed.

**Goal.** `http://127.0.0.1:8765/devourer-stepper.html` renders Devourer's ten scenarios so the
author can review the rotation **visually** and give feedback. Correctness of the walk is *not*
the goal — scenarios nobody can stand behind get an in-render warning and ship anyway.

⛔ ~~**Author decision already taken (2026-08-19), do not re-open:** the two virtual rows draw
**inline in the row, styled as ordinary row icons, with a marker calling them out.** Not a
separate strip, not omitted.~~ **Reversed by the build** — V12 shipped as `Panel.lua`, a separate
strip, and there is one virtual row rather than two. See the banner above.

---

## 0. What you need to know before touching anything

**A preview needs no addon Lua.** `SPECS_BUILT` builds from two markdown files. There is no
`Catalogs/Devourer.lua` and this task does not create one. Nothing here ships to the game.

**Devourer is authored but never built or flown** (`backlog.md` → *Status* → *The specs*). Three
files exist and are good: `devourer/catalog.md` (526 lines), `scenarios.md` (262),
`fact-classification.md` (133).

**Every spell id already exists in the docs.** Nothing needs looking up in game or on the web.

**The loop.** One server serves every spec from one directory (`previews/CLAUDE.md`). It should
already be running; if not:

```bash
cd ~/code/fun/wow/tools
uv run python -m wowkb.serve ../projects/combat-assist/previews \
    --watch ../projects/combat-assist/specs \
    --on-change "uv run python -m wowkb.capart build --all"
```

Then `capart build --all`, `capart check --all`. Both are sub-second now (a content-hash cache
on the asset encode landed 2026-08-19); a *cold* build after new art is ~15s.

---

## 1. Blocker: no parseable roster table

`load_roster` (`tools/wowkb/capart.py`) reads **one** table shape and Devourer has none:

```python
ROSTER_RE = r"^\|\s*`(?P<key>[a-z_]+)`\s*\|\s*(?P<name>[^|]+?)\s*\|\s*`(?P<spell>\d+)`\s*\|"
            r"\s*(?P<override>[^|]*?)\s*\|\s*(?P<lane>[A-Z]+|—|-)[^|]*\|\s*(?P<charges>[^|]*?)\s*\|"
```

So: `| \`key\` | Name | \`spell\` | override | LANE | charges |`. A row whose **lane** column is
`—` is skipped as "an open fact, not a drawable button". Both the base name **and** the override
name become keys, because a scenario row writes whatever the client would *display*.

**Do:** add a *Bound abilities* table to `devourer/catalog.md` built from what §5.1 / §5.2 / §6.1
already say. Roughly seven rows:

| ability | spell | overrides to | note |
| --- | --- | --- | --- |
| Void Metamorphosis | `1217605` | — | position 1 |
| Reap | `1226019` | Cull `1245453` / Eradicate `1225826` | |
| Void Ray | `473728` | — | |
| Soul Immolation | `1241937` | — | |
| Voidblade | `1245412` | Hungering Slash `1239123` / Pierce the Veil `1245483` / Reaper's Toll `1245470` | placed last deliberately (§7.1) |
| Collapsing Star | `1221167` | cast id `1221150` | **virtual, gated** |
| Consume | `473662` | Devour `1217610` | **virtual, standing** |
| Vengeful Retreat | `198793` | — | Utility row (§5.2) |

⚠ Do not invent lanes. Take them from §5's roster prose.

---

## 2. Blocker: the scenarios are in the older prose grammar

The scraper wants, per scenario:

```
### B-1 · The clean build global

- **State.** …
- **CDM row.** Ability `verdict` · Ability `verdict` {cues: x} · …
- **Walk.**
  1. …
- **Anything else.** …        ← becomes an `extras` line, rendered under the row
```

- `HEADING_RE` = `^###\s+([A-Z][A-Za-z]{1,4}-\d+)\s+·\s+(.+)$` — so `### B-1 · Title` and
  `### M-3 · Title` both parse as-is. **Ids are fine; only the shape is wrong.**
- `ENTRY_RE` = `^(?P<name>.+?)\s+\`(?P<verdict>[a-z-]+)\`(?P<ann>.*)$` — the name must **not** be
  wrapped in `**bold**`.
- `GROUP_RE` = `\{(cues|client):\s*([^}]*)\}`.
- Bullets are split on `^- \*\*Label.\*\*`; `State`, `CDM row` and `Walk` are special, everything
  else lands in `extras`.
- A scenario section ends at the next `###` **or the next `##`**, whichever comes first.

**Devourer's current form** (`scenarios.md` §7.3 / §7.4) differs in exactly four ways:

1. `**B-1 · The clean build global.** *State:* …` inline → split into a `### B-1 · …` heading and
   a `- **State.**` bullet.
2. `- **Row.**` → `- **CDM row.**`
3. the press is written `**Void Ray \`press\`**` → strip the bold.
4. `‖` seams — see §3.

Ten scenarios: **B-1…B-5** (build phase, §7.3) and **M-1…M-5** (window phase, §7.4).

**Measured 2026-08-19, so you know what you are walking into:**

| check | today |
| --- | --- |
| scenarios in the old prose form | 10 |
| `###` headings that would parse | **0** |
| `- **Row.**` bullets | **9** — see M-3 below |
| redundant `{cues: blocked}` to strip (§6) | **4** |
| `ROSTER_RE` matches in `catalog.md` | **0** |

⚠ **M-3 IS NOT TRANSCRIBABLE — it has to be authored.** It is written as a prose delta,
*"As M-2 with `/cap aoe` off"*, with no row of its own and only a bullet naming Misordering 1. Its
nine entries must be **derived** from M-2 by turning the AoE toggle off, which is a judgement about
the rotation and not a reformatting. Derive it, then flag the whole scenario with `⚠ UNSURE` (§5)
and say plainly in the note that this row was derived rather than authored — the elimination gate
will confirm it is self-consistent, and nothing will confirm it is *right*.

⚠ **Keep §7.1, §7.2 and §7.5 as prose.** They are the argument, not scenarios, and they sit under
`## 7`, so the section-boundary rule already stops the scraper swallowing them — provided the
first `### B-1` heading comes *after* them.

---

## 3. Blocker: the virtual rows (the only new engineering)

Devourer's row uses `‖` **19 times** to mark two cap-owned icons that have no Cooldown Manager
frame at all:

```
Collapsing Star `cd` ‖ Void Metamorphosis `cd` · Reap `cd` · Void Ray `press` · … ‖ Consume `below`
```

This is V12 (*virtual row*) and Devourer is the first spec to need it — Consume is the
most-pressed button in the branch and Blizzard gives it no frame in any category (`catalog.md`
§3). The composed reading order is already written in §7.1:

```
[a cleared GATED row] → [the Essential line, left to right] → [the STANDING row]
```

**Build it as:** the row grammar accepts `‖` as a separator alongside `·`, and an entry that
followed a `‖` is flagged virtual (e.g. `entry["virtual"] = true`). The renderer draws it as an
ordinary icon plus a marker. Suggested marker — the author has *not* seen it yet and expects to
react to it on screen, so pick something and iterate: a corner tick in a distinct hue, plus a
`title` reading "cap-owned icon — this ability has no Cooldown Manager frame".

**Touch points:** `scrape_scenarios` (split on `·` today), the sidecar shape, `stepper.js`'s row
builder, `shelf.css`. Any pixel decision belongs in `render-shelf.md` as tokens, **never as a
literal in `shelf.css`** — a gate fails on literal colour outside the chrome block.

⚠ The **elimination gate needs no change**: the composed order *is* the authored left-to-right
order, so a virtual entry participates in the scan exactly like any other.

---

## 4. Blocker: registration

Add to `SPECS_BUILT` in `tools/wowkb/capart.py`, mirroring `retribution`:

```python
"devourer": {
    "catalog":   SPECS / "devourer" / "catalog.md",
    "scenarios": SPECS / "devourer" / "scenarios.md",
    "sidecar":   SIDECARS / "devourer-scenarios.json",
    "out":       PREVIEWS / "devourer-stepper.html",
    "title":     "Devourer",
    "scan_samples": [ …four ability display names… ],
},
```

Icons resolve from spell id. Devourer is new, so expect misses on the override ids (Cull,
Eradicate, Pierce the Veil, Reaper's Toll, Devour). For each miss add an `ICON_FDID` entry — the
FileDataID is read off `raw/wago/SpellMisc-*.csv`, column `SpellIconFileDataID`, keyed by
`SpellID`. **Look it up, never guess it**; that table is what the client itself reads.

---

## 5. The annotation — the actual point of the exercise

The author wants to review this **visually**, with everything uncertain flagged **in the render**.

**Mechanism already exists and is free:** any bullet that is not `State` / `CDM row` / `Walk`
becomes an `extras` entry and renders under the row as `<b>Label.</b> html`. So:

```
- **⚠ UNSURE.** The APL spends this global on Voidblade (rung 1); cap never reaches it.
```

Make these **loud** — an amber block, not a grey footnote. That is a style addition, so its
colours are tokens in `render-shelf.md`.

**Flag at minimum these, which the docs themselves already doubt:**

| where | what is uncertain |
| --- | --- |
| §7.1, and therefore **every** scenario | Position 1 assumes a below-bank Void Metamorphosis reads as ruled out **by Blizzard's own desaturation**, and it is written `cd` on that assumption. Unconfirmed in client. If it is wrong, the first icon in the row is wrong. |
| **B-4** | Misordering 2 — the APL spends that global on Voidblade (rung 1) to land *Devourer's Bite* on the window; Voidblade sits at position 5 and the walk never reaches it. |
| **B-5** | Cue D is "a sound slice, not the literal condition" — cap draws `!proc & talent(eradicate) & aoe` where the APL holds on `!eradicate.up & talent.eradicate & !single_target`. It can *miss* a hold, which is the safe direction. |
| `catalog.md` §1 | Two provisional premises, dated. |
| `catalog.md` §8 | Open facts — check each against the scenarios it touches. |

⚠ **Do not annotate around a GATE failure.** "I am unsure this is how the rotation works" and
"this row contradicts itself" are different problems. If `check` rejects a scenario, bring it to
the author. Expect two or three; that is the point of running them.

---

## 6. The gates you will meet

Run `uv run python -m wowkb.capart check --all`. Relevant ones:

- **reading gate** — each scenario judged by exactly one pass. Devourer declares **no positive
  cue**, so every scenario answers to `elimination_gate`: the leftmost entry that is neither
  swiped nor wearing a negative cue must be the one the doc calls the press.
- **density gate** — more than **2** `budgeted` cues before the press fails. Only `blocked` is
  budgeted. Fix by promoting the press, never by raising the number.
- **cue implied by verdict** — an entry may not declare `{cues: blocked}` on a `hold-readable` /
  `hold-sealed` verdict. Devourer's `scenarios.md` **already does this** in B-5 and likely
  elsewhere; strip them. (Havoc had 8, all following advice this tool used to print.)
- **every declared cue is worn** — a cue in the shelf that no scenario wears fails.
- **doc ↔ sidecar** — the whole scenario is compared, so a prose-only edit fails until you re-run
  `capart import scenarios devourer`.

---

## 7. Order of work

1. Roster table into `catalog.md` (§1).
2. Transcribe the ten scenarios (§2) — no `‖` handling yet, just get them parsing.
3. Register in `SPECS_BUILT`, resolve icons (§4). Build. Look at it.
4. Add `‖` / virtual-row support and its marker (§3).
5. Add the loud `⚠ UNSURE` treatment and write the annotations (§5).
6. `check --all` green, then hand the URL to the author.

**Do not** cut a release, and do not write `Catalogs/Devourer.lua` — neither is on this path.

---

## 8. Concurrency warning

Another agent was editing this project on 2026-08-19 (it added **V15 · Hotkey text** and its
shipped font). Before starting, re-read `render-shelf.md` Part 6's token block and
`projects/combat-assist/CLAUDE.md` rather than trusting any summary — including this file's.
