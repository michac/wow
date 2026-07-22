# Verify runbook — one session, four checklists (v0.16.0, 2026-07-21)

> **What this is.** `milestones.md` §7.3 / §7.4 / §7.5 / §7.6 are four *milestone
> exit criteria*, written when each milestone shipped. This is the same content
> **re-ordered into the sequence you'd actually play it**, with the exact
> commands, what you should see, and what it means when you don't.
>
> **Source of truth is still `milestones.md` §7.3–§7.6** — tick the boxes there.
> Each step below names the item it closes, so `→ §7.3.6` means "this closes
> §7.3 item 6". This file is disposable; those checklists are not.

---

## The one thing that changed

Until v0.16.0 the exit criterion of three milestones was `lit now` — **a line you
had to type mid-pull**. It isn't any more. **The HUD records every pull by
itself** and writes it to disk.

So your job during the pull is to **play a real rotation**, not to squint at the
board. Almost everything is read *afterwards*. Steps that genuinely need you to
watch something live are marked **👁 LIVE** — there are only four of them.

---

## Phase 0 — setup (2 min, out of combat, anywhere)

```
/reload                     ← v0.16.0 is deployed but not loaded until you do this
/cdmp                       ← confirms "v0.16.0 loaded"
/cdmp hud                   ← MUST be on: the recorder is gated on the HUD
```

⚠ **`/cdmp hud` off = nothing is recorded.** `/cdmp hud log` says so in its
header if you forget.

Then, so you have a clean baseline:

```
/cdmp probe clear           ← zeroes the passive counters
/cdmp probe                 ← the out-of-combat report
```

Read one line of that output before you go anywhere:

> `seeding (M3d, out-of-combat reads): live — the client answers cooldown reads in this context`

If it says **`unreadable here`**, M3d is dark in this context and §7.4 will fail
for a known reason, not a new one. Note where you were standing.

---

## Phase 1 — the cold start (before you pull anything)

This is the one test that must happen **before** combat, because it's about what
the board knows when it has observed nothing.

1. **Cast Summon Demonic Tyrant** on anything. Let it go on cooldown.
2. **`/reload`** while it is still on cooldown.
3. Look at the Tyrant dot the moment the UI comes back.

**Expect:** a real countdown immediately — `~42.1s (read)`, rendered **solid**.

**Fail looks like:** `NEVER · no edge seen yet`. That is the pre-M3d cold start,
and it means seeding didn't run — check the `seeding` line from Phase 0 first,
because "unreadable here" explains it and "live" doesn't.

→ **§7.4.1** (the headline — if this fails, the rest of §7.4 is moot)

Also note the wording: **`(read)` = the client's own number, `(est)` = our
arithmetic off an observed cast.** They're different confidence and the row says
which.

---

## Phase 2 — standing still (out of combat, ~3 min)

Do all of this in a city or at the dummies *without* attacking anything.

### 2a. Nothing nags you when there's nothing to do 👁 LIVE

Stand there with **3+ shards**. Watch for ~10 seconds.

**Expect:** nothing promotes to **LATE**. Ever. Out of combat, LATE is a nag with
nothing to nag about.

→ **§7.3.4** (B6)

### 2b. PREP is visibly its own thing 👁 LIVE

Look at the rail and the DEMO.SYS terminal chrome.

**Expect:** a calm resting tint that is **visibly not GENERATE**. Read the label
with your eyes unfocused on colour — `[.] PREP 4/5`. The glyph and word alone
must be unambiguous ([X1]: never colour-alone).

→ **§7.5.6**, **§7.5.7**

### 2c. The untracked-ability warning

If you have **not** yet added Shadow Bolt to your Cooldown Manager:

**Expect:** `/cdmp hud` warned that Shadow Bolt is untracked and *said what that
costs you*. Now nudge the CDM a few times in Edit Mode.

**Expect:** the warning does **not** re-spam. It lives in `hud status` instead
(chat scrolls away; the status block is what `probe` captures).

Then add Shadow Bolt manually to the CDM. **Expect:** the warning clears, and
**SB → Infernal Bolt now lights with no code change** — the transform rule
resolves to wherever the override lands.

→ **§7.3.7** (B7)

### 2d. The rail is anchored, not clipped 👁 LIVE

Drag the CDM in Edit Mode; change **Orientation** and **# Rows**.

**Expect:** the rail sits under the `C:\>_` footer at its **own full width**, and
follows. If it comes out ~28 px wide, that's the documented clipping trap
(`notes.md` §9) — one centre anchor, explicit width.

→ **§7.5.1**

---

## Phase 3 — the pull (the main event)

Go to a **target dummy**. You are going to do **three pulls**, and the only thing
you have to do well is **play your actual rotation**. Don't stop to read the HUD.

### Pull 1 — a clean 60–90 seconds

Play normally. Get through at least one full Tyrant window. Make sure that
somewhere in there you:

- let a **Grimoire go on cooldown** (so the button becomes Devour Magic),
- proc a **Demonic Art** (so HoG transforms into Ruination),
- **hit 5 shards** at least once,
- hardcast a **Shadow Bolt / Infernal Bolt** (for the ghost head).

Then **stop attacking and drop combat.** Do not type anything.

```
/cdmp hud log
```

**Expect:** the pull is there, with a duration and a histogram. **This is the
milestone.** If you had to toggle or type something first to make it record, M3e
has failed at the one thing it exists to fix.

→ **§7.6.1**

### What to read in that output

**① The histogram line.**

```
lit 0:41% 1:33% 2:19% 3:6% 4:1%
-> never above 3 lit — strictness is holding
```

This is **the answer to the question three milestones have been waiting on.**
Read the *distribution*, not a feeling:

| What you see | What it means | What happens next |
| --- | --- | --- |
| Mass at **1–2** | The rules are right | Board is trusted → M3c-c2 / M4 open |
| A fat **4+** tail (≥10 %) | The rules are too loose | Tighten **`HudScore` RULES** — **do not touch a colour** |
| Mass at **0** | The board is mute, not strict | Different bug: gates falsely closed |

⚠ The verdict line does the arithmetic for you, but **read the buckets anyway** —
a board that's quiet 90 % of the time and lights five dots during every Tyrant
window is exactly what a single number hides, and it's the failure mode
"strictness" is actually about.

→ **§7.3.6** and **§7.4.5** — *the exit criterion of two milestones, in one line*

**② The peak set.**

```
peak: 4 lit at +37.2s
  Ruination (now Ruination · armed · shards 4>=3)
  Summon Demonic Tyrant (up — use on cooldown)
  ...
```

The worst moment in the fight, named **with its reasons**. Argue with it. A dot
you disagree with is a scoring bug you can argue with; **a dot with no reason is
a design failure.**

⚠ Check the **identity**: a transformed Grimoire must appear as **Devour Magic or
not at all**. If "Grimoire: Fel Ravager" appears in a peak set while that button
was a purge, B1 is back.

→ **§7.6.3**, and it's the evidence for **§7.3.1 / §7.3.2**

**③ The event tail.** Timestamped transitions, `dot` / `ready` / `mode` / `cap` /
`cast` / `seed` / `combat`. Four specific things to look for:

- **`ready` lines around an instant cast** — nothing genuinely ready may flip to
  **on-cooldown inside the 1.5 s global**. This is the GCD trap: invisible in a
  snapshot, obvious in two timestamps. → **§7.4.2**
- **`cast` + `mode` lines together** — the `START` line reads `shards 4 ->~1`,
  and the **`mode` flip to SPEND is timestamped *inside* the cast**, not a beat
  after it. That's `projected` doing its job, not `shards`. → **§7.5.4**, **§7.3.5**
- **`cap` lines** — see Pull 2.
- **`dot` lines carrying `~est`** — anything promoted *because of* a projection.
  Cross-check it rendered **hollow** on screen.

### Pull 2 — the cap sequence

Short pull, one job: **get to 5 shards, then HoG, then back to 5 quickly.**

Then read `/cdmp hud log`.

**Expect** in the `cap` events: **two cap edges and exactly one suppression** —

```
+12.30s cap    cap edge (5/5) — glitter
+15.10s cap    cap edge (5/5) — SUPPRESSED by the re-arm
```

If both say `glitter`, the ~2 s throttle isn't wired and we're re-firing a flash
within a couple of GCDs, which [X2] forbids. If suppressions stay 0 through that
sequence, same conclusion.

→ **§7.5.5**

👁 **LIVE, while you do it:** the cap flip reads as **"act or waste"** — a
warning, not a trophy. And the glitter must be **visible even when the board has
receded** (let it go quiet first, then cap). A dim glitter means the fx frame
became a child of the receded rail — the frame-alpha trap. → **§7.5.8**

### Pull 3 — a normal fight, watching two things live 👁 LIVE

- **Mid-cast, watch the dots.** During a Hand of Gul'dan cast the board must
  reflect the **post-cast** shard state, and anything lit *because of* that
  estimate renders **hollow**. ⚠ If the projection reads **low** rather than
  high, that's the documented residual (`atStart` sampled after the client
  already deducted) — the safe direction, and named in
  `HudState.ProjectedShards`'s header. → **§7.3.5** (B4)
- **The ghost head.** During a hardcast, an incoming rail segment appears
  **hollow** and solidifies on landing. Hollow must read **identically** on the
  rail and on the dots — if the two treatments differ, the confidence marker is
  broken, not the rail. → **§7.5.3**
- **Fill honesty.** Segments track shards, and the partial segment moves
  *between* whole shards — **or** `hud status` says fragments are unreadable
  here, which is **an answer, not a failure**. → **§7.5.2**

### While still in combat

```
/cdmp probe
```

That captures the in-combat report. Two things to check in it:

- **Section A** should now read `<secret>` for cooldowns — reads go secret in
  combat, **by design**. The board must **keep** its seeded state rather than
  blanking, and the seeding line must say *unavailable in combat* rather than
  implying the feature is on. → **§7.4.3** (first half)
- **Section C** — if any cast phase reads `ALL SECRET`, note it. `START` going
  secret would take the whole spend-side projection dark.

---

## Phase 4 — leaving combat, and the disk

Drop combat and read `/cdmp hud log` one more time.

**Expect:** the pull's **last** events are the combat-exit ones — a `seed` line
saying what re-truthing the board actually found, and a `mode` flip out of SPEND
into PREP. They're inside the pull they belong to, deliberately.

**Expect on screen:** anything sitting at `"should be up, unconfirmed"` has
resolved to a real number. That's the free fix — a drifted estimate replaced by
the client's own figure the instant combat ends.

→ **§7.4.3** (second half)

Then check provenance is legible:

```
/cdmp hud status
```

**Expect:** per-item `ready=yes(seed)` vs `ready=no(edge)`, and a seeding block
with a live/unreadable verdict plus last-pass counts. Both are direct
observations and both render solid — this readout is the **only** place they're
distinguishable, which is what keeps M3c-b and M3d separable inside one release.

→ **§7.4.4**

Also confirm here, once:

**`handler errors (swallowed by the hook's pcall): 0`**

A non-zero count is **a bug, not a curiosity** — it was 47 hiding inside `other`
before the split.

→ **§7.3.3** (B2/B3)

### The disk round-trip

```
/cdmp probe
/reload            ← NOT OPTIONAL
```

Then read:

```
/mnt/c/Program Files (x86)/World of Warcraft/_retail_/WTF/Account/LLOYDCHRISTMAS/SavedVariables/CDMProbe.lua
```

**Expect:** `CDMProbeDB.pulls` holds the last 5 pulls, structured —
`pulls[3].hist` indexes directly, `pulls[3].peakSet` is a plain list of strings.
Plus `CDMProbeDB.reports["probe_ooc"]` and `["probe_combat"]`.

⚠ **Without the `/reload` you are reading the previous session's file, which is
indistinguishable from a recorder that did nothing.** This has cost us a session
before.

→ **§7.6.6**

---

## Phase 5 — the keybind question (5 min, out of combat)

This one has been open since v0.4.0 and is **not diagnosable from source** — it
depends on your actual bars, which is why it needed the report.

1. Find a spell whose keybind the HUD shows **wrong** (or remap one and watch it
   not update).
2. `/cdmp probe` → `/reload` → open the file → find **section E**.

The spell will show **exactly one of four things**, and each is the answer:

| What you see | Diagnosis |
| --- | --- |
| Two slots, the **lower** marked `<-- used` | **First-bound-slot-wins** — bar 1 answers before the bar you remapped |
| A row with `cmd=none` | Slot is in the **unbindable ranges** (13–24, 109–180) — action-bar *pages* with no bindings of their own |
| **No rows at all** | A **macro** `GetMacroSpell` can't resolve (conditional/modifier) |
| A populated **`2nd=…`** | You remapped the **secondary** binding — new in v0.16.0, and previously invisible |

⚠ The fourth was found in source this session: `GetBindingKey(cmd)` returns
**two** keys and the resolver only ever read the first, so remapping the
secondary changed nothing and **no row said why**. v0.16.0 shows both. It does
**not** change which one wins — that decision wants this evidence first.

→ **§7.6.8**, closes **§7.2 item 5**

---

## Phase 6 — cost, and the two context risks

### Cost is invisible

Several pulls with the HUD on and **no stutter**. The sample path is one integer
increment; only *transitions* and a *new peak* pay for building reason strings.
If you feel it, say so — the design has a specific budget and this is where it'd
show.

→ **§7.6.7**

### The two things only real content can answer

Both are **standing risks reported honestly by the addon rather than assumed** —
neither is a failure if it comes back negative, but we need to know.

1. **Napkin readability in a raid.** All probe data is open-world. Cast
   readability is the entire foundation of the spend-side projection and **has
   never been confirmed in a raid.** `/cdmp probe` in a raid → section C: does
   any phase read `ALL SECRET`? This is the **highest-value open check on the
   board**. → **§7.3.8**, §7 item 14
2. **Seeding outside the open world.** Check the `hud status` seeding verdict in
   an **instance lobby** and in a **raid between pulls**. An `unreadable here`
   verdict is **the answer the line exists to give**, not a bug — but it tells us
   where seeding silently does less. → **§7.4.6**

---

## Quick reference

| Command | What it's for |
| --- | --- |
| `/cdmp hud` | toggle the HUD — **required for recording** |
| `/cdmp hud log` | last pull: histogram + peak set + event tail |
| `/cdmp hud log all` | the whole 5-pull ring, summaries only |
| `/cdmp hud status` | live state: edges, seeding verdict, provenance, `lit now` |
| `/cdmp hud binds` | keybind reverse index, live |
| `/cdmp probe` | the full report → SavedVariables (run OOC *and* in combat) |
| `/cdmp probe clear` | zero the passive counters |
| `/reload` | **flushes SavedVariables** — nothing is on disk until you do |

**If you only do one thing:** Phase 3, Pull 1, then read the histogram. That
single line closes the exit criterion of **two** milestones and decides whether
the next milestone is *tuning the rules* or *building the next feature*.
