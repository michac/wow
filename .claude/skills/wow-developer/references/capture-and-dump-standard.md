# The capture & dump standard

How every addon in this workspace gets data out of the game client.

This is a **house standard**, not a WoW fact — it says what we do, not what the client
does. The API facts it rests on live in `knowledge/addon-dev/`; this file cites them.

Applies to CDMProbe (`cdmp`), BucketBinds (`bb`), PlannerState (`ps`) and ClientLab (`clab`).
⚠ The capture registry is about **who writes captures**, not who gets released — ClientLab
is deliberately not a release target and still belongs here.

---

## 1. The seam: hard format, soft implementation

Three separate addon repos with no package manager between them. WoW has no dependency
mechanism that isn't either "the user must install a second addon" or embedding — and
embedding *is* vendoring. So we vendor, and we draw the contract at the only place where
divergence actually costs something.

| Layer | Contract | Why |
|---|---|---|
| **The SavedVariables shape** (§2) | **HARD.** Byte-identical semantics across all three addons | One Python reader consumes all of it. Divergence here is what produced four near-identical loaders in `cdmp.py` |
| `Capture.lua` internals, function names, ergonomics | **SOFT.** Copy and adapt | Nothing outside the addon can observe them |
| Dump panel UI, layout, which buttons exist | **SOFT.** Whatever fits the addon | Ditto |

**Enforcement is free and needs no lint.** `wowkb.capture` is the *only* reader. An addon
that writes the wrong shape fails loudly the first time anyone reads a capture. The
consuming tool is the test.

So: "a slightly different implementation that keeps the spirit" is correct for the Lua and
wrong for the format.

---

## 2. The wire format — HARD CONTRACT

Every capture in every addon lands in exactly one place:

```lua
<AddonDB>.captures = {
  ["<stream>"] = {              -- ring, oldest first, newest LAST
    {
      started = "2026-08-05 14:02:11",   -- date("%Y-%m-%d %H:%M:%S") at session open
      version = "0.32.118",              -- ns.version, so a capture names its build
      meta    = { … },                   -- OPTIONAL, per-stream, flat string/number map
      lines   = { "…", "…" },            -- pre-rendered strings; present iff :Line/:Mark used
      rows    = { {…}, {…} },            -- flat tables; present iff :Row used
    },
    …
  },
}
```

**Rules, each of which cost this workspace something:**

1. **One top-level key per addon: `captures`.** Never a new sibling store. Seven top-level
   stores with four retention policies is the state this standard exists to end.
2. **Every stream is bounded.** `sessions` and `cap` are required at `Open`; there is no
   default and no unbounded ring. Drop oldest first.
3. **A session is one addon load.** Every `/reload` opens a new one — so a verification pass
   that respecs between hero trees burns 4–5 slots. Size `sessions` for that: CDMProbe's
   `decisionlog` uses 6 because at 3 the earliest pull silently rolled off before it could
   be extracted.
4. **`lines` are pre-rendered strings, and that is a one-way door.** The string *is* the
   record. No extractor change can add a field to a capture already on disk.
   **Therefore anything you might later want to slice by — combat state, spec, hero tree —
   must be stamped at capture time**, as a `:Mark`. This is not a style preference; it cost
   a re-fly (`DecisionLog.lua:483` records the incident).
5. **No game value reaches a line except through `Capture.Safe()`.** It returns a
   readability *class*, never the value: a Secret Value renders `<secret>`. Formatting or
   indexing a Secret Value taints — see `knowledge/addon-dev/security-taint-and-restricted-data.md`.
6. **No colour escapes inside a line.** Strip at capture time, not at read time. The panel
   colours its *list rows*; it never colours the payload.
7. **`meta` is flat** — strings and numbers only. It is session-scoped context, not a place
   to nest a state dump.

### Choosing `lines` vs `rows`

- **`lines`** — a human or a `grep` is the consumer. Decision traces, event tapes, anything
  you scan. Cheap, greppable, unstructured, permanently frozen once written.
- **`rows`** — a *grader* is the consumer. Acceptance runs, matrix labs, anything a Python
  function turns into PASS/FAIL. Structured, so the grader can evolve; still bounded.

A stream may use both. `flight` is the model: rows for the grader, lines for the human
reading why a criterion failed.

---

## 3. `Capture.lua` — the Lua side

Vendored. Copy it into the addon, adapt freely, keep §2 exact.

```lua
-- One call per stream, at file scope.
local log = ns.Capture.Open("decision", { sessions = 6, cap = 5000, dedup = true })

log:Line(fmt, ...)   -- one pre-rendered line. Skipped if byte-identical to the previous
                     -- line and the stream was opened with dedup = true.
log:Mark(fmt, ...)   -- an edge marker: ALWAYS written, NEVER deduped, stamped ABOVE the
                     -- dedup check. For transitions the log exists to record.
log:Row(tbl)         -- a structured row for a grader.
log:Wipe()           -- discard this session's content and restart it (a flight is one run).
log:Meta(k, v)       -- set/replace a session meta field. Late-binding is fine and expected:
                     -- a spec swap 15 s in should re-stamp, not mislabel the session.

ns.Capture.Safe(v)   -- the ONLY way a game value reaches a line.
```

**`:Mark` sits above the dedup, and that placement is the entire point.** A combat edge
that does not happen to move the decision — idling at a full bar and pulling, the normal
way a pull starts — would otherwise be swallowed by the change-only early return.

**`Open` before `ADDON_LOADED` is a no-op that returns a live handle.** Callers must never
have to guard. Writes before the DB exists are dropped, not queued.

---

## 4. The dump panel — captures a human takes at a moment

A **dump** is a capture triggered deliberately, mid-pull, at a moment only the player can
recognise. It is a **button**, never a slash subcommand.

```lua
ns.Dumps.Register{
  id      = "coverage",
  label   = "Roster coverage",                                    -- the button face
  blurb   = function() return ("%s · %d blind"):format(spec, n) end,  -- the list-row caption
  capture = function() return { "line 1", "line 2", … } end,      -- PLAIN TEXT, no escapes
}
```

`/<addon> dump` toggles the panel. That is the **only** new slash command this standard
adds anywhere.

- **Top: a button grid**, one per registered dump. Press it mid-pull. No typing, no macro.
- **Bottom: the list**, newest first — `#12  14:02:11  coverage · Havoc · 2 blind  [copy] [×]`
- Pressing a button appends `{ t, id, blurb, lines }` to the `dump` stream and adds a row.
- **`[copy]` reads the in-memory ring** — so no `/reload`, and no picking the right entry
  out of SavedVariables by hand.

**It composes with §2 by simply being a stream named `dump`.** Same ring, same bounds, same
shape — so `wowkb.capture <addon> dump` still flattens it to disk and the agent path is
untouched. The bytes a human copies and the bytes the extractor writes are identical.

**The panel must refuse to create itself in combat** (CDMProbe's `HudVirtual` already does
this correctly), and its copy EditBox must never be a secure frame.

### How `[copy]` actually works

**WoW has no clipboard API.** The only mechanism is a multiline `EditBox`: `SetText(payload)`
→ `HighlightText()` → `SetFocus()`, leaving the text selected so the user's own Ctrl+C does
the work.

Verified against source:

- `SetMultiLine`, `SetMaxBytes`, `SetMaxLetters` are documented `SimpleEditBox` methods —
  `Blizzard_APIDocumentationGenerated/SimpleEditBoxAPIDocumentation.lua:776, :756, :766` **[T1]**
- `HighlightText()` is Blizzard's own select-all idiom, 17 call sites, e.g.
  `Blizzard_SharedXML/Shared/InputBox/InputBoxTemplates.lua:113` **[T1]**
- The shipping copy-out proof is WeakAuras' debug log —
  `WeakAurasOptions/OptionsFrames/DebugLogFrame.lua:36, :52-53`: `OnMouseUp → HighlightText()`
  and `OnTextChanged → SetText(text); HighlightText()`, i.e. it reverts user edits and
  re-selects. Read-only by reselection. **[T3]**

**Constraints, stated honestly:**

- Call `SetMaxLetters(0)` and `SetMaxBytes(0)` unconditionally, so the default cap never
  matters. **The default is not established by anything readable** — `@verify-ingame`.
- Very large payloads stall the client on `SetText`. Cap a copy page at **~30,000
  characters** and page it (`[copy 1/3]`). **30k is a guess pending measurement** — file an
  observation when it gets measured.
- Strip colour escapes at capture time (§2 rule 6), not here.

---

## 5. `wowkb.capture` — the Python side

One reader for all three addons. Replaces the four hand-written loaders in `cdmp.py`.

```python
load(addon: str, wow_path=DEFAULT_WOW) -> Capture | None   # newest <Addon>.lua, parsed once
Capture.streams() -> list[str]
Capture.sessions(stream) -> list[Session]                  # .started .version .meta .lines .rows
Capture.flatten(stream, out: Path) -> int                  # greppable .log, newest-last
```

CLI: `uv run python -m wowkb.capture <bb|cdmp|clab|ps> <stream> [--out PATH] [--list]`

**Graders stay per-addon and per-stream.** `flight`'s PASS/FAIL ladder and `curvelab`'s
five-valued grading are domain logic and must not be generalised — but they consume
`capture.load()` and never glob a path themselves. `wowkb.cdmp` shrinks to *just* graders.

**A grader reports UNREADABLE, never a number, when the capture predates the marker it
needs.** Silently scoring a capture that cannot answer the question hands back a confident
wrong answer, which is the failure this whole standard exists to end.

⚠ **SavedVariables only flush on `/reload` or logout.** Every workflow built on this ends
with a `/reload`. Say so in the addon's chat confirmation, every time.

---

## 6. Checklist for a new capture

- [ ] Does an existing stream already answer this? Add a `:Mark`, not a stream.
- [ ] `sessions` and `cap` chosen deliberately, sized for `/reload` burn.
- [ ] Everything you might slice by later is a `:Mark` *now*.
- [ ] Every game value goes through `Safe()`.
- [ ] A human-triggered capture is a `Dumps.Register` button, not a subcommand.
- [ ] If it's for a probe, it dies with the probe: file, `.toc` line, stream, spec, grader.
