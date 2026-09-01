# Parked work — five items nothing is waiting on

**What this file is for:** ⚠ **it is a REGISTER, not one item's plan**, which is the one way it
deviates from its neighbours in this directory. `backlog/*.md` normally holds the steps for a
single committed item; this holds five unrelated ones that are deliberately *not* committed. They
are written down so they stop being rediscovered, argued about, and parked again.

`backlog.md` → `## Ideas` carries the entry that points here. **Nothing here blocks anything**,
and two of them may correctly never be built. Delete this file when the last one has landed or
been dropped.

Each entry carries the same three things: what it is, **why it is parked**, and the trap that
made it worth writing down.

---

## 1. Destruction — the shipped catalog and its document disagree

**What.** `Catalogs/Destruction.lua` is a **47-line retired pilot** carrying one entry
(`conflagrate`, two abilities). `specs/destruction/catalog.md` carries a fully authored
**10-entry** design that supersedes it. `backlog.md` names this the one place left in the project
where a shipped catalog and its document disagree, and says plainly: **do not read the `.lua` as
the design.**

**Why parked — three independent blockers, any one of which is enough:**

- **`authoring.md` stage 6 refused the transcription.** The scenario↔state gate found five
  scenarios drawing `capped` / `blocked` / `overcap` that the pilot does not declare — and
  declaring them *is* authoring, not transcription.
- **It is the only spec never catalog-reviewed**, which `backlog.md` says must happen **first**.
- **It has neither `catalog.json` nor `scenarios.json`**, so `capart export catalog destruction`
  fails outright. There is no pipeline to run.

**And the row fold has nothing to grab here anyway.** On the real 10-entry design the
press-on-sight abilities sit at positions 1, 3, 5 and 10, so **no cut separates the cooldowns
from the rotation** — which is the constraint every other break satisfies. Destruction may be the
spec that shows the fold is not universal.

⚠ **One correction to land while passing through:** `backlog.md:619` still says *"the old
two-entry proof"*. The pilot has **one entry and two abilities**. (A second stale claim, that
`capart check destruction`'s sidecar self-comparison was broken, was fixed 2026-08-27 and needs
no action.)

---

## 2. Devourer — a line in the setup docs, not code

**What.** `vengeful_retreat` sits in the **Utility** viewer. `Anchor.lua` orders the **Essential**
viewer only, so cap skins and hatches the row but gives it no cell: 6 placed + 1 virtual, 5
actually placed.

**Why parked.** It is not a defect. The drag from Utility into Essential is **legal and is the
player's to make**, so the fix is a sentence in the setup docs and in `Catalogs/Devourer.lua`'s
header. That is the whole item.

⚠ **DO NOT BUILD A `viewer` FIELD.** Essential vs Utility is the *player's layout*, not a
property of the spell — four Tier-1 12.1.0 facts in `knowledge/addon-dev/cooldown-manager.md`
§1.1. A `viewer` field would encode a user setting as authored data. ⚠ And do not re-derive the
placement from `wowkb.spec_inventory`'s `Blizz cat` column: it is the DB2 default and reads
convincingly like an answer.

⚠ **Moving a row between viewers in code means `SetCooldownToCategory`**, which writes the
player's saved layout and is refused by `spec.md` §4.

**The genuinely open part is a different question** and already lives in `discussion.md` →
*Devourer*: *is the hatch alone worth binding a row outside the scanned line?* Havoc declares the
same spell as its entry 1, so it is one question, not two.

---

## 3. Mover-driven resize

**What.** Drop `noResize` from the EllesmereUI element and snap `setWidth` to whole cells, so
dragging the mover's handles picks a grid. The addon half is already done — `Ellesmere.lua`
simply declines resize today, and `ellesmere_spec` asserts it declines *nothing else*.

**Why parked.** Nobody has asked for it. `/cap grid` already sets the grid, per spec and hero
tree, and reads back which tier each number came from.

⚠ **THE TRAP, and it is the one most likely to look tempting for the wrong reason: do not reach
for this to solve overflow.** Deriving the grid from the live roster makes the grid an input cap
has to chase, and makes the panel's rect **roster-dependent** — which destroys *"the rect is
known at login"*. That property is what everything anchored to the row now depends on, including
the EllesmereUI power bars that were the point of the whole exercise. Overflow is answered by
`/cap grid`, and the player is told (`over:<n>`, and the fold-aware capacity line).

---

## 4. `RegisterSkin` for cap's own windows

**What.** EllesmereUI publishes a separate skinning API (`SKINNING_API.md` in the live install).
Applying it to `Window.lua` and `StylePanel.lua` would make cap's own frames match the host's
look.

**Why parked.** Pure cosmetics, and it touches **no Cooldown Manager frame at all** — so it
cannot interact with anything the anchoring work built, and cannot be broken by it. Ships any
time or never.

---

## 5. `norow` conflates three different causes

**What.** `Bind.lua:242` reports `norow` for an authored entry that reached no Cooldown Manager
row. Three unrelated things produce it: the API being absent, the row info being missing *or*
secret, and no readable spell ID. They are one word today, so `/cap anchor rows` and the `bind`
stream can say *that* an entry did not bind but never *why*.

**Why parked.** Nothing is wrong — a `norow` is usually correct and expected (an ability with no
cooldown never gets a row, which `A{miss:n}` counts and the docs call normal). This is a
diagnostic sharpening, not a fix, and it is worth doing the next time somebody is debugging a
binding rather than on its own.

**Where it came from.** Noticed while writing the EllesmereUI anchoring plan and unrelated to it;
carried here so it does not get rediscovered a third time.

---

## What is NOT here

**The folded row's reading model** is a committed item with a live gap behind it, and it lives in
`backlog/fold-reading-model.md`. It is not parked.
