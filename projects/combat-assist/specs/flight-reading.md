# Combat Assist Plus — reading a flight

**What this file is for:** how to read a `wowkb.capture cap <stream>` dump. Every field cap
emits, what it means, and what a rung's flight has to show before it passes. It is an
**instrument**, not a record: present tense, no dates, no history. What we did is
`notes.md`; where the code is is `backlog.md` → `## Status`; what the addon should do is
`spec.md`.

⚠ **SavedVariables only flush on `/reload`.** Make the `/reload` part of the flight, not a
step after it — a pull that ends without one leaves the capture describing the *previous*
build, and every number in it is then a lie about the build you just flew.

⚠ **A capture is interpreted once, and thereafter the docs cite the finding, not the log.**
Reading one is a piece of work with an output: the finding goes to `notes.md` and into whichever
of `discussion.md` / `backlog.md` it bears on, stated as a finding, with the raw fields kept only
as its evidence. **A document that tells you to go and read a capture is a document that has not
been finished** — and the next reader re-derives an interpretation, differently.

⚠ **The stream stores *changes*, not samples, so a count of lines is not a duty cycle.** A state
that changed twice and held for ten minutes occupies the same two lines as one that flickered
twice in a second. Anything stated as a proportion of a pull is **time-weighted against the
`# combat start` → `# combat end` window** or it is wrong, and the two readings differ by a lot.

⚠ **The ceiling on all of it: cap reports what it *offered*, never what appeared.** Every
sealed sink — `SetText`, `SetAlpha`, a duration object — takes a value and hands nothing
back. `armed` means cap handed the client the comparison and nothing more. **An eyeball is
the only oracle for a pixel**, and several rows below say so individually because it is the
mistake this file exists to stop.

## The four streams

| Stream | Carries |
| --- | --- |
| `wowkb.capture cap bind` | the CDM binding — which rows resolved, to what, per resolve |
| `wowkb.capture cap tier` | the tier verdicts and gate health, one line per change |
| `wowkb.capture cap edge` | every alert edge that landed (`Available` / `OnCooldown` / aura) |
| `wowkb.capture cap draw` | what the surfaces painted, and whether they found a frame to anchor to |

Combat start and end are `#`-marked carrying the **full body**, so a pull whose drawn set
never changes still emits its numbers at both edges. `:Meta` carries the catalog, cap's
version and the line count — **read the version first**, because a capture from an older
build is the commonest way a flight reads as a null result.

## The `draw` line

```
D{n: rows: anch: conf: off: nf: cue: arm: glow: nosize: ring: mark: bar:}
P{E1:HIGH/a91p2.5* E7:LOW/a43p0.5*}
C{E8:+stacks:armed E2:-cooldownRemaining:refused}
B{E1:armed E8:ready}
```

One deduped line per change of the drawn set. `rows:` is the bound row count the other
counters are read against.

### `D{}` — the counters

| Token | Means |
| --- | --- |
| `anch:` | rows whose overlay found an item frame and anchored to it |
| `conf:` | of those, rows anchored to a **confirmed** frame |
| `off:` | the item frame is not visible; the overlay is correctly hidden |
| `nf:` | ⚠ **no item frame at all** — anchoring failed. `nf:` = `rows:` is a total failure, not a quiet overlay |
| `nosize:` | rows that wanted a ring and got none for want of a size (see below) |
| `cue:` / `arm:` | cues offered / cues cap actually reached the client with |
| `glow:` | `<frames>/live` or `<frames>/off` — the proc-glow suppression (below) |
| `ring:` `mark:` `bar:` | **build-time probe results** (below). None of them says a pixel moved |

⚠ **`nosize:` is the number that stops a blank screen reading as a healthy pull.** The ring
is sized off `item:GetWidth()`, which is `SecretWhenAnchoringSecret`; a refused read leaves
it unsized and cap **hides it rather than guessing an icon size** — and a tiered row draws no
veil either, because the veil is 0 wherever a ring exists. Without this counter a pull where
every width read refused prints `anch:21 conf:21 nf:0 off:0` with full `P{}` cells:
**identical to a working one.**

| `nosize:` reading | Means |
| --- | --- |
| `0` | every drawn row had a size. Says nothing about whether art appeared |
| = `rows:` | ⚠ **total** — the width read is refused everywhere and the tier signal is invisible, whatever the rest of the line says |
| `0 <` … `< rows:` | some rows only. Most likely a repool mid-pull, where the fresh frame's width is secret until the next quiet moment |

### `P{}` — one cell per entry, the graded register

`E1:HIGH/a91p2.5*` — the tier, the ring alpha, the pulse rate cap armed, and the `*`.
`E1:HIGH/a91t3p2.5*` when the four-quad fallback ring is live: `t` prints **only** then,
because it describes the fallback's geometry and nothing on screen when the flipbook is up.

| Cell mark | Means |
| --- | --- |
| `*` | this entry is the one drawn on its row |
| no `*` | the entry LOST its row to a **higher-tier** sibling — its treatment is on no icon. ⚠ The comparison is tier order first, emphasis only *inside* one tier, so a **dimmer** cell can be the one carrying the `*` |
| `!` | `Bind.ItemFrame` refused; a rebind is already scheduled |
| `?` | anchored to an **unconfirmed** frame — drawn anyway, possibly on the wrong row |

⚠ **`p` is the rate cap *asked for*, not necessarily the rate on screen.** The per-row phase
is a `SetStartDelay` under a `BOUNCE` loop, and whether that delay re-pays each iteration is
unmeasured (`armPulse`'s `--@unverified`). If it does, the true period is `cycle + delay` and
no two rows in a tier share it. A stalled animation and a slow one are still different
readings, which is what the token is for.

### `C{}` — one cell per offered cue

`E8:+stacks:armed` — the entry, the polarity, the channel, the state.

| State | Means |
| --- | --- |
| `armed` | cap resolved the inputs and handed the client the comparison. **Not** "it appeared" |
| `refused` | cap tried and could not — no live `auraInstanceID`, no duration, no curve, no ink |
| `nodraw` | the cue's (polarity, channel) pair has no marker in the renderer; cap never asked the client |
| `taken` | a second cue wanted a slot another entry already holds on that row |

⚠ **`arm: = cue:`** says the mechanism is wired end to end. `arm:` short of `cue:` with `C{}`
naming `refused` says cap never reached the client. **Neither says a pixel moved.**

⚠ **E8's cue flapping `armed` ↔ `refused` through a pull is the PASS case.** Its
`auraInstanceID` comes off the Wild Imp row, which binds no aura when no imps are out — so
`refused` there means *there are no imps*, which is the same thing the quantiser would have
drawn (nothing) had it been asked. **The failure that looks similar** is `refused` for a
whole pull with imps visibly out: that is the row lookup or the two-viewer tie-break being
wrong.

⚠ **Out of combat the quantiser returns a PLAIN string.** A desk check in a city reads the
count as ordinary text and proves nothing about the sealed path.

### `B{}` — one cell per declared bar, in roster order

| State | Means |
| --- | --- |
| `armed` | cap resolved a duration and handed it to the bar. **Not** "it drew" |
| `ready` | the client returned no duration for `ignoreGCD = true` — nothing remaining. A deliberate state: the bar draws **full and unnumbered** |
| `refused` | the **read** failed — `GetSpellCooldownDuration` was absent or threw, so there was nothing to hand over |
| `unarmed` | cap had a duration and the **sinks** refused it — `SetMinMaxValues` / `SetTimerDuration` raised |
| `nobind` | the roster names it and no CDM row binds it. The row is not drawn at all, so the panel has no hole |
| suffix `!` | the fill is armed and cap could put **no number** on it — the bar carries `--` |

⚠ **`refused` and `unarmed` are two cells and one set of pixels.** Both draw an empty track
carrying `--`; the split is in the log, because "the client would not tell cap" and "the
client would not take it" are different faults and a flight that cannot name which learns
nothing.

⚠ **Zero, expired and broken are three different sets of pixels and only two are cap's to
tell apart.** The formatted string is secret, so cap cannot know whether the client drew a
number or nothing. What separates them is the fill: `ready` is full with no text, `armed` is
the client's fill and the client's string, `refused` is an empty track carrying cap's own
`--`. **`--` never stands for zero.**

⚠ **A bar with no tier is the normal case, not a fault.** Every band on E1/E2/E3 needs
`ready(this)`, so the roster is tier-less for exactly the stretch its bar has something to
show — the fill recedes to the resting slate and counts down anyway. `B{E1:armed E2:armed …}`
with grey fills is that, and it is correct.

### The build-time probes — `ring:`, `mark:`, `bar:`, `glow:`

Settled once, when the first row is built. **None of them says a pixel moved.**

| Token | Means |
| --- | --- |
| `ring:flip` | the atlas resolved, the `FlipBook` animation took all three setters, and the flipbook is the live geometry |
| `ring:quad:<method>` | that setter is **absent** at runtime; cap fell back to the four-quad ring |
| `ring:quad:atlas` | `SetAtlas` did not leave the region atlas-backed — the name did not resolve |
| `ring:quad:flipbook` | `CreateAnimation("FlipBook")` refused |
| `mark:font/pulse` | the count marker took its font *and* its scale animation |
| `mark:nofont/…` | `SetFont` returned false — the marker is on the template's font, not cap's |
| `mark:…/nopulse` | `SetScaleAnimationMode` or the `Scale` animation was unavailable; the number is drawn, unpulsed |
| `bar:-` | no row has been built, so the probe has never been settled — an empty roster, or no verdict pass yet |
| `bar:tex` / `notex` | `SetStatusBarTexture` returned true / did not. ⚠ **Reported, not acted on** — standing down leaves the player nothing, carrying on still leaves them a track and a number |
| `bar:fmt` / `nofmt` | `C_StringUtil.CreateSecondsFormatter` resolved / did not. `nofmt` means **every** bar carries `--`; the fills are unaffected |
| `bar:font` / `nofont` | `SetFont` returned true / did not — `nofont` leaves both strings on the template's font |

**The four-quad ring is the fallback and covers three failures, not one** — a setter name
that is not there, an atlas name that does not resolve, and a `FlipBook` animation type the
client refuses. It needs no size (it is anchored, not sized), so it is also the geometry that
still draws when `GetWidth` never answers.

**`glow:`** is `<frames>/live` or `<frames>/off` — how many item frames cap has hooked **ever
this session**, and whether the dim is armed on this pass.

| Reading | Means |
| --- | --- |
| `glow:0/…` | cap never found a frame to hook |
| `glow:N/off` | the frames are hooked and cap is deliberately dark |
| `glow:N/live` | hooked and armed — the healthy reading |

⚠ **`SetAlpha` hands nothing back, so `glow:` can never say the glow got dimmer.** An eyeball
on a proc'd icon is the only oracle. ⚠ **The count is cumulative and deliberately inflated
in two ways** — it never decrements (`hooked` is weak-keyed and may shrink under it) and it
accumulates across spec swaps within a session; tab-2 rows are armed too, though only tab-1
viewers ever hear the glow event. It is an upper bound on the frames that could ever dim.

## Reading a blank screen

The commonest flight outcome worth diagnosing, and the reason the `draw` stream exists at
all: a flight that sees nothing must be able to tell a treatment bug from an anchoring one.

| Reading | Means |
| --- | --- |
| `P{}` cells move, screen blank | **anchoring** — check `anch:`/`conf:` and the `!`/`?` suffixes |
| `anch:` = `rows:`, `conf:` = `rows:`, screen blank | **treatment** — the paint ran on a real frame and produced nothing visible |
| `nosize:` = `rows:` | the ring never sized; the tier signal is invisible for that reason alone |
| `anch:` = `rows:`, an overlay visibly **on the wrong icon** after a repool | ⚠ **not a treatment bug** — the secret-anchor gap (`knowledge/addon-dev/security-taint-and-restricted-data.md` §1.1; the lab question is `secret-anchor-dependent-geometry` in `projects/addon-lab/questions.json`). `anchor()` calls `SetPoint` mid-pull when the item-frame pool hands a cooldownID a new frame, and a CDM item frame in combat carries a *secret* anchor; whether a dependent of one still moves is **unmeasured**. A silent no-op leaves the overlay on its previous position while everything in `D{}` reads healthy |
| no `draw` lines at all | the paint path never ran — check `tier` for a `# listener-error` mark |

⚠ **What must not read as a pass.** A **`# listener-error`** mark on `tier` means a listener
threw and was reported once; the `draw` stream after it is not evidence of anything. And a
`P{}` cell says nothing about whether a **marker** was drawn on that icon — cues are read out
of `C{}` and nowhere else.

## Acceptance criteria

### The binding — `bind`

| Read | Passes when |
| --- | --- |
| row set across a pull | byte-identical; the generation moves exactly once per real change |
| `u:` (unreadable) | `0` out of combat. ⚠ A `PARTIAL` out of combat is a KB finding, not a cap bug |
| identity rows | every display override resolves to the ability actually on the row |
| `n:` against `set:` | ⚠ **they never agree, and must not be asserted to.** The category set is the spec's full candidate set. The invariant is `rows ≤ set` |

### The gates — `tier` and `edge`

| Read | Passes when |
| --- | --- |
| `edge`, `hooks:` | > 0, matching the bound row set |
| `edge`, `Available` / `OnCooldown` | both appear in a pull, on the cooldown entries and only those |
| `edge`, `refused:` | ⚠ **not checkable as a bare count.** The hook is on every row, most of which are silences, so refusals are the expected case. Restate it as *every refused cid is a declared silence* — which needs the cid logged on refusal, and it is not yet |
| `G{ready:…}` | reaches `n/n` within a pull |
| `G{affordable} {proc} {identity} {resource}` | each `n/n` **in combat** |
| `# settle by:` | fires once, naming which arm fired. ⚠ `by:quiet` is correct for a login and leaves the **event** arm untested — that needs a real spec or hero swap |
| `# combat start` while unsettled | `S{… DARK}` — the dark-for-the-fight rule. Needs a `/reload` mid-combat or a swap immediately before a pull |
| `S{mode:…}` | follows `/cap aoe` |
| `# dropped` marks | exactly the entries whose ability the build does not carry |

⚠ **A criterion nobody exercised must never read as a pass.** Three of the above are only
exercised by a deliberate setup (a spec swap, a mid-combat `/reload`, a `/cap aoe` toggle);
a flight that did none of them has not tested them, and the report must say so rather than
count them.

**And one measurement, which is not a criterion:** the distribution of **how many entries are
HIGH at once** through a pull. It is **reported, never pass/fail** — the instrument for
explaining *why* a moment felt wrong in play, read next to what you actually felt.

### The surfaces — `draw`

Everything in `D{}`/`P{}`/`C{}`/`B{}` above is the mechanical half, and it tops out at
*offered*. The other half has no log entry and must be flown deliberately:

- does the count appear when the imps cross six, and vanish when they fall below;
- does the hold glyph appear **only** in the last stretch before a Tyrant window;
- does a ready bar (full, unnumbered) read as *ready* rather than as *stuck*, and is the
  countdown legible in combat;
- does a resting bar read as *counting down, no opinion* rather than as a dim LOW;
- does cap's ring read as distinct from the stock proc glow on a proc'd icon;
- does an un-opinionated icon under the *none* veil stay readable as a timer.

⚠ **A threshold that fires at the wrong moment reads exactly like one that fires correctly
in every instrument cap owns.** That is why these are on the list and why none of them can be
moved onto it.
