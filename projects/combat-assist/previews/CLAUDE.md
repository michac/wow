# cap previews — one server, one directory, one file per spec

Everything in this directory is **generated**. `wowkb.capart build <spec>` writes the
`<spec>-stepper.html` pages and `data/<spec>-scenarios.json`; `template/` and `assets/` are the
inputs it assembles from. **Never hand-edit a `*-stepper.html`** — `capart check <spec>` rebuilds
it and fails if the committed file differs, so a hand edit is reverted the next time anyone looks.

## The serving model — do not add a second server

Every spec's preview is a **uniquely named file in this one directory**, so **one** `wowkb.serve`
on **one** port serves all of them, and a new spec needs no new server and no new port. It is
already correct; it just has to be left alone.

```
http://127.0.0.1:8765/                        — the index, listing every spec
http://127.0.0.1:8765/havoc-stepper.html
http://127.0.0.1:8765/retribution-stepper.html
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
