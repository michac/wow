# cap previews — one server, one directory, one file per spec

Everything in this directory is **generated**. `wowkb.capart build <spec>` writes the
`<spec>-stepper.html` pages and `data/<spec>-scenarios.json`; `build --all` additionally writes
`lab.html` and `index.html`; `template/` and `assets/` are the inputs it assembles from.
**Never hand-edit a generated page** — `capart check` rebuilds each one and fails if the committed
file differs, so a hand edit is reverted the next time anyone looks.

## Three kinds of page, and only one of them is per-spec

- **`<spec>-stepper.html`** — the scenario walk for one spec. One per registered spec.
- **`lab.html`** — Part 7, on its own page since 2026-08-19. It is **not a spec**: its cells
  resolve against the shelf's reference roster (`SHELF_ROSTER_SPEC`), so a lab cell is never a
  claim about a spec's rotation. It used to be appended to *every* spec page, which made that
  claim look spec-shaped and duplicated the larger half of the page into all of them — an
  experiment could add half a megabyte to every spec at once.
- **`index.html`** — the front door, listing every registered spec plus the lab. Deliberately
  minimal.

⚠ **`lab_stripes` and `promotion` in a spec page's data are LEGACY NAMES, not lab payloads.** They
are V11's hatch sheet and V14's ring, both of which the lab owned until they were promoted. What
actually left the spec pages with the lab are the lab-only assets: sprites, VFX sheets and font
candidates.

⚠ **The two non-spec pages are gated outside the per-spec loop** (`_check_shared`), because the
staleness gate that covers a spec page runs *inside* it. `index.html` had no gate at all until
2026-08-19 — a newly registered spec could have been missing from the front door indefinitely with
the run still reading green.

## The serving model — do not add a second server

Every spec's preview is a **uniquely named file in this one directory**, so **one** `wowkb.serve`
on **one** port serves all of them, and a new spec needs no new server and no new port. It is
already correct; it just has to be left alone.

```
http://127.0.0.1:8765/                        — the index: every spec, plus the lab
http://127.0.0.1:8765/havoc-stepper.html
http://127.0.0.1:8765/retribution-stepper.html
http://127.0.0.1:8765/devourer-stepper.html   — the first page drawing a virtual row (V12)
http://127.0.0.1:8765/demonology-stepper.html
http://127.0.0.1:8765/lab.html                — Part 7, one page for every spec
```

⚠ **Running a second server on another port to "give a spec its own preview" is a mistake, and it
is an appealing one.** Both servers end up serving *this same directory*, so the second one buys no
isolation whatsoever — the two ports are two doors into one folder. What it does buy is two
watchers with two different `--on-change` commands writing into that folder, which is a real way to
end up looking at a page one of them rebuilt while reading the other one's URL. Add a spec by
adding a file, not a port.

## The command

Run from `tools/`, one shell, left running:

```bash
uv run python -m wowkb.serve ../projects/combat-assist/previews \
    --watch ../projects/combat-assist/specs \
    --on-change "python -m wowkb.capart build --all"
```

⚠ **`--all`, not a spec name.** The watcher fires on an edit to *any* spec but runs exactly the
command it was given, so a server started with `build havoc` will rebuild Havoc when you edit
`specs/retribution/catalog.md`, serve you the *stale* Retribution page, and report a successful
rebuild while doing it — nothing about that looks wrong on screen. `--all` reads `SPECS_BUILT` in
`tools/wowkb/capart.py`, which is the spec registry, so a newly registered spec is covered without
anyone remembering to extend a command string. `capart check --all` is the same argument for CI.

⚠ **`--watch` points at all of `specs/`, deliberately** — not at one spec's folder. A
`render-shelf.md` edit changes *every* preview, since the shelf is where all the pixels live, and a
watcher scoped to `specs/<spec>/` would silently miss it: you would edit a colour, watch one page
update, and conclude the other spec was unaffected.

⚠ **A preview the watcher rebuilt is a preview you must still commit.** `--on-change` writes the
real file in this directory, not a temporary copy, so a look-and-tweak session leaves real edits
behind. That is intended — but it means `capart check <spec>` passing depends on the last rebuild
having been the one you meant.
