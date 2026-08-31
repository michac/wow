# Combat Assist Plus — reading a flight

**What this file is for:** the current capture fields and the mechanical checks they can
support. It is not a visual oracle or a history log. SavedVariables flush only on `/reload`.

Read the live addon version first. Captures store changes, not periodic samples, so line counts
are not duty cycles.

⚠ **Accepted is not drawn** — `authoring.md` states it once, and it applies to every
field below without being repeated per field: a sink accepting a duration or a paint call never
proves a pixel appeared. The player's report is the authority for brightness, contrast, placement
and usefulness.

## Streams

| Command | Carries |
| --- | --- |
| `wowkb.capture cap bind` | resolved CDM rows and binding health, plus the row-order note |
| `wowkb.capture cap tier` | the readable signal; the stream NAME stays `tier` for reader compatibility — the body vocabulary is generational (see the Draw-surface ⚠) |
| `wowkb.capture cap edge` | accepted and refused CDM alert edges, proc-glow edges, and identity flips |
| `wowkb.capture cap draw` | the static overlay and Tyrant-bar paths cap attempted |
| `wowkb.capture cap anchor` | **probe** — CDM frame re-anchoring: drawn position against the authored order |

Combat start/end are marked with a full body. A `# listener-error` in `tier` invalidates the
downstream draw evidence for that interval.

A `# row-order <a> is laid out after <b>` note in `bind` is the **structural** finding, not a
per-ability one: it says this player's Cooldown Manager lays the row out in an order the
catalog's left-to-right reading model does not hold for, which makes elimination point at the
wrong button everywhere at once. It is written once per change of finding and echoed to chat.
**Its ABSENCE on a flight that bound a full roster is the positive result** — that is the check
that the whole reading model rests on.

### ⚠ A reload IN COMBAT produces a blank cap, and it is not a regression

Observed 2026-08-23 and it cost a false alarm: cap came back from `/reload` drawing nothing at
all, and came right by itself after zoning broke combat. Binding is fenced behind
`InCombatLockdown()`, so a reload taken in a pull has nothing to bind against and the roster stays
empty until the fence lifts.

The trap is that Demonology holds combat for a long time on a training dummy — the player reported
staying flagged halfway across the map — so "I was not fighting anything" is not evidence of being
out of combat. **Check `# combat start` / `# combat end` in the `bind` stream before reading a
blank session as a defect.**

⚠ And a session's lines reach disk only on the NEXT `/reload` or logout. A stream whose newest
session names the PREVIOUS build is the normal state right after a deploy, not a failed install —
`wowkb.addon list` says what is installed; the capture cannot.

### The free-Hammer probe, on the `edge` stream (2026-08-22)

Two line kinds were added to answer one question, and **only** that question: can cap tell a
FREE Hammer of Light from an ordinary one? `specs/retribution/catalog.md` *Open facts* 3 owns
the question; this says how to read the answer.

```
t412.6 glow:on  spell:427453
t412.6 identity wake_of_ashes base/255937->transformed/427453 cd:true
```

- **`glow:on|off spell:<id>`** — every `SPELL_ACTIVATION_OVERLAY_GLOW_*` event, carrying the
  **empowered** spell's id. Not filtered to the catalog: an id cap has no row for is exactly the
  interesting case, so filtering would discard the evidence.
- **`identity <ability> <was>-><now> cd:<bool>`** — a row's resolved identity changed, with what
  it became and **whether that row's own cooldown was already running when it happened**. The
  `cd:` term is the point: it is what a timing separator would be built on.

**How to read it.** Find the `glow:on spell:427453` lines. For each, look at the nearest
preceding `identity wake_of_ashes` flip:

- flip and glow **at the same instant, `cd:` turning true together** → an ordinary Hammer,
  arriving with the Wake of Ashes press.
- flip arriving **seconds later, with `cd:true` already standing** → a free Hammer, and the gap
  is a separator cap can author on. This is the outcome that reopens the defeat.
- **no flip at all beside the glow** → the row never transformed, which the player's own
  2026-08-22 observation says should not happen. If it does, both earlier readings are wrong.

⚠ **These lines feed nothing.** No predicate reads them, `readProc` still polls the base id, and
no verdict changes because of them. They may not grow a branch until they have been read.

⚠ **The stack count behind the free cast is not here and cannot be.** Light's Deliverance banks
60 stacks and an aura's application count is sealed in combat. Add it to **Tracked Buffs** before
flying: the player watches the counter climb, which is what makes an empty log mean *"it never
fired"* rather than *"the recorder is broken."*

## Readable signal

```
S{n:2 on:2 mark:2 blind:0}
E{demonbolt:scan tyrant:scan+dreadstalkers,grimoire}
R{ready:2/2 proc:1/1 identity:1/1 capped:1/1 affordable:2/2 resource:1/1}
W{tyrant:dreadstalkers:on(!ready:dreadstalkers=T) tyrant:grimoire:off(identity:grimoire:transformed=F)}
Q{-}
S{settled/spells-changed}
```

- `on:` is the number of enhanced entries assigned scan membership by readable facts.
- `mark:` is the number of readable context markers offered.
- `blind:` counts conditions withheld because a read was unknown.
- `E{}` names each enhanced entry, its membership (`id:scan` — pre-2026-08-25 captures say `id:ROTATION` etc. here, which reads as the same fact plus a tier the model no longer holds), and any marker facts.
- `R{known/total}` distinguishes a false answer from a refused read. The predicates are
  `ready proc identity capped affordable resource talent aoe`, always in that order — `capped` is
  the charge-state read (`GetSpellCharges().isActive`), `affordable` the power one
  (`IsSpellUsable`'s second return), `talent` the trait-config read (`Talents.lua`, and the one
  whose exact call is still marked `[gap]`), and `aoe` cap's **own** `/cap aoe` toggle rather than
  a game read at all — it has no subject, so it is the one predicate that can never be refused by
  the client. A spec that uses none of them reports `0/0` for it, which is not a failure.
  ⚠ `talent` and `aoe` were added on 2026-08-17 and the group grew from six fields to eight, so a
  capture taken before that date has a shorter `R{}` — grep by predicate name, never by position.
- `W{}` is the **reason** each readable marker drew or was withheld — `E{}` and `R{}` say
  *what* and *how healthy*, `W{}` says *why*, so a flight answers "why is this marker firing"
  without back-deriving term values from the catalog. One `entry:marker:STATE(terms)` per
  readable marker, in row order: `STATE` is `on` (drew), `off` (a term read false — the
  eliminating case, and the term shown is the fact that ruled it out), or `blind` (a term was
  unknown, so it was withheld). `terms` lists every `when` term as `predicate:subject=T|F|?`
  (`!` prefixes a negated term; an identity term reads `identity:subject:wanted=T|F`). It is in
  the dedup body, so a change of *justification* emits a line even when the drawn set does not —
  which is how a readiness latch reading `true` is told apart from one reading unknown. Sealed
  (graded) markers never appear here; they are Channel's, reported in `C{}`.
  ⚠ **And a sealed marker's readable GATE does not appear either — this is a blind spot, not a
  design.** Since 2026-08-17 a sealed marker may carry `when` terms that decide whether the client
  is allowed to paint it at all (`spec.md` §3.6, *one secret, many readable gates*). Those land in
  `verdict.gates`, which nothing emits. So when a gated sealed badge does not draw, no stream says
  whether the gate refused it, the curve read below its band, or the arm failed — `C{}` reports
  `gated` for the first, but not which term did it. A gated hold that behaves oddly in play cannot
  currently be diagnosed from a capture.
- `Q{conflagrate:live|napkin|unknown}` records only charge provenance: `live` is an exact
  unrestricted seed; `napkin` is the bounded cast/alert estimate maintained after that seed.
- `settled/...` names the bind-settle arm; `DARK` means combat began before a safe roster
  settled and the addon intentionally drew nothing for that fight.

The stream can show that the authored mechanism fired. It cannot show that the Demonbolt
membership or either Tyrant fact was helpful.

## Draw surface

```
D{n:2 rows:2 anch:2 conf:2 off:0 nf:0 bar:tex/fmt/font stock:coexist}
P{demonbolt:scan tyrant:scan immolation_aura:scan+blocked}
M{tyrant:dreadstalkers tyrant:grimoire}
B{tyrant:armed}
C{-}
```

- `anch:` / `conf:` say the addon found and confirmed CDM item frames.
- `off:` is a real but hidden item frame; `nf:` means no frame was found.
- `P{}` records the composed treatment attempted for each enhanced entry, as
  `id:scan[+cue,cue]` — or `id:off` where the row drew nothing, `id:hidden` where its
  CDM item is real but not shown, `id:noframe` where no item was found. **`scan` is the whole of
  the drawn treatment**: a row is in the scan or it is not (shelf V13).
  ⚠ **The ROLE TIER is not here, and since 2026-08-25 it exists nowhere** (it left the paint
  2026-08-19 and the model 2026-08-25). The body vocabulary has three generations: the oldest
  captures say `id:COOLDOWN` (with `CHARGES` substituted in on a charge read) — a tier that
  stopped being a fact about pixels when the four hues collapsed; every capture since, and the
  format going forward, says `id:scan`. Reading an OLD capture, `id:ROTATION` means the same as
  today's `id:scan` and carries a tier as a bonus — a model fact nothing current records; the
  reverse translation does not exist.
  ⚠ **Only READABLE cues appear here.** A graded (sealed) cue's visibility is the client's, so
  it is reported in `C{}` as armed and never in `P{}` — a row wearing only a graded cue reads
  as bare here while its badge fades on screen, and that is correct, not a discrepancy.
  ⚠ **The row string changed when the veil was retired, and a capture is a one-way door.** A row
  in an OLDER capture may carry a `/veil` segment (`id:TIER[/veil][+cue,cue]`) — that segment
  described a dim the addon no longer draws, and its absence in a newer capture is the change,
  not a row that stopped skipping. Lines are stored pre-rendered, so no reader can reconcile the
  two formats; read a `/veil` capture as evidence about the build that wrote it and nothing else.
- `M{}` records which readable context markers the engine asserted. ⚠ Since 2026-08-14 **nothing
  is drawn for them** — the shelf's cue vocabulary has no form for the two Warlock ones — so this
  field reports a decision, never a pixel.
- `stock:coexist` records the deliberate baseline: cap did not try to suppress Blizzard's
  proc glow.
- `B{tyrant:ready|armed|refused|unarmed|nobind}` records the bar path. `armed` means the
  client accepted a duration object.
- `bar:` is the bar's build-time texture/formatter/font probe.
- `C{conflagrate:backdraft:offered|armed|refused}` reports only sealed-channel acquisition. The
  **graded** cues report here too (`felblade:felblade_overcap:armed`,
  `essence_break:essence_break_awaits_eye_beam:armed`): `armed` means the client accepted a
  curve and evaluated it, and `refused` means a feature gate or an evaluation failed. **Never a
  value** — the whole point of a curve is that cap does not learn the number.

A moving `P{}` with a blank screen points first to anchoring or treatment. Healthy `anch:` and
`conf:` with no visible pixels is a treatment failure. A marker in `M{}` at the wrong gameplay
moment is a product failure even when every mechanical field is healthy — and while nothing draws
for it, that failure is invisible in play and readable only here.

## Anchor order

Written by `Anchor.lua`, which draws the Essential viewer's rows in the catalog's authored order.
**This is shipped behaviour and on by default** — it arms itself a second after
`PLAYER_ENTERING_WORLD`, so unlike every other stream here you do not arm it and the stream is
never silent for want of a command. `/cap anchor [on|off|retry|rows]` toggles it,
rebuilds it and reports the plan; the setting persists at `ns.db.anchor`.

*(This section described a hand-armed probe, `probes/AnchorOrder.lua` with a `/capanchor` verb,
until that probe was promoted into `Anchor.lua` on 2026-08-16. The stream format below is
unchanged by the promotion.)*

```
t120.4 # armed
A{n:8 named:6 extra:2 miss:1 parked:0} P{31,12,44,9,17,3,52,28} D{31,12,44,9,17,3,52,28} X{ok} S{stomp:0 icombat:0 disp:0 cont:0 reassert:0 park:0 stale:0 strike:0}
t131.7 # stomp RefreshLayout destructive=1 combat=1
```

- `A{}` is the plan: `n` frames placed, `named` of them in the catalog's authored order,
  `extra` rows the catalog does not name (they keep client order behind the named ones),
  `miss` authored entries with no live row on this build, and `parked` icons cap has moved OFF
  the row and is holding offscreen.
- ⚠ **`miss` and `parked` are different failures and only one is a fault.** A `miss` is an
  authored entry the Cooldown Manager never made a row for — normal, and usually an ability
  with no cooldown. A `parked` icon is one cap moved and then lost its place for: it exists,
  the player configured it, and cap is deliberately holding it out of the row rather than
  letting it read as part of a priority scan it is no longer ordered by. **A steady non-zero
  `parked` is worth chasing**; it means the plan keeps losing a row it once held.
- `P{}` is the **authored** order as cooldownIDs; `D{}` is the **drawn** order, read off each
  frame's measured position. `X{ok}` means they agree; `X{MISMATCH}` means they do not, including
  when a frame's position could not be read.
- ⚠ **`D{}` is read in TWO dimensions, top row first and then left to right** — it used to be
  `GetLeft()` alone, which was right only while the row was one row. A higher `GetTop()` is
  higher on the screen, so the first row to read is the one with the *larger* top.
- **`|` marks the row break**, in both orders: `P{a,b,c|d,e}` is two rows intended,
  `D{a,b,c|d,e}` is two rows drawn. No `|` means everything landed on one row.
  ⚠ **This is the instrument for the second row, and reading the two beside each other is the
  whole point.** The id sequence cannot show a row split by itself: a pass that collapsed every
  icon onto one row produces the *identical* sequence to the correct two-row draw. So
  `P{a,b,c|d,e} D{a,b,c,d,e}` is a real failure — the right order, on the wrong number of rows —
  and it reads `X{MISMATCH}` because the split is part of the verdict, not a decoration beside
  it. A count in `A{}` would have restated the plan's own number and could never have disagreed
  with itself.
- **`X{STALE:<n>}` outranks both** and is read first. It is a live `GetCooldownID()` read
  against the id cap recorded when it took each frame, and `n` frames now answer with a
  different one — the pool re-issued them. `P{}`/`D{}` are then describing icons the plan no
  longer owns, so neither `ok` nor `MISMATCH` would mean what it says.
- `S{}` counts, for the session: `stomp` layout passes seen through `Anchor.lua`'s own hooks,
  `icombat` how many of those landed inside a pull, `park` how many icons have been taken off
  the row across the session (a total; `A{parked}` is how many are off it right now),
  `reassert` frames put back inside the
  `SetPoint` call that moved them, `disp` displacements the sampler still saw within the window
  after one of cap's own re-asserts, `cont` displacements the sampler saw with no recent
  re-assert of cap's, `stale` re-pool episodes, and `strike` the contention run standing right
  now (it decays, so it is a level, not a total).
- **`reassert` is the healthy counter and it climbs.** Every layout pass moves the frames and
  every move is answered inside the same call, so a busy pull produces many re-asserts and no
  `# displaced`. What is worth reading is the ratio: `disp` and `cont` are the moves that
  reached the screen.

⚠ **`P{}`/`D{}` are the only evidence here.** The `bind` stream's `# row-order` note and
`Catalog.OrderCheck` both derive order from `layoutIndex`, which a `SetPoint` re-anchor does not
touch — they keep reporting Blizzard's order whether the re-anchor worked or not. **Their silence
is not evidence in this flight.**

Marks:

| Mark | Means |
| --- | --- |
| `# armed` / `# restored n=<n> orphans=<m>` | cap took and gave back the frames — `n` is every frame it had moved, placed and parked alike, since restoring only the placed ones would leave a parked icon offscreen for good. A non-zero `orphans` is a bug: a frame left with no points |
| `# combat start` / `# combat end` | the `PLAYER_REGEN_*` edge, which is where every `combat=` flag comes from |
| `# stomp <source> destructive=<0\|1> combat=<0\|1>` | Blizzard's layout ran. `destructive=1` is `RefreshLayout`, which releases the frame pool, so the frames afterwards are new ones — cap answers it with a rebuild, not a re-place |
| `# displaced n=<count> combat=<0\|1>` | frames left where cap put them and were **still** displaced half a second later, within the window after one of cap's own re-asserts — the layout engine settling around a move cap has already answered |
| `# contended n=<count> strike=<n> combat=<0\|1>` | frames displaced with **no** recent re-assert of cap's, so they moved by a route `SetPoint` does not carry — a scale or parent change, or something re-anchoring them harder than cap. The claim is positional only; cap names no addon. `strike` is the run so far; the third inside 10 s opens the dialog |
| `# stale n=<count> combat=<0\|1>` | `n` tracked frames are serving other rows: the pool re-issued them and the plan is stale. A `# rearmed` follows, in combat as well as out |
| `# rearmed why=<reason>` | cap rebuilt the plan from a fresh bind rather than re-placing frames whose identity it no longer knew |
| `# parked n=<count> combat=<0\|1>` | `n` icons cap had moved dropped out of the plan and were taken off the row (`spec.md` §3.9). Emitted by the apply that MOVED them, never by the plan rebuild that decided to — an adopt followed by a failed apply has parked nothing. Cleared wholesale by a destructive stomp, because the pool re-issues those frames against new rows |
| `# asking` | cap opened the contention dialog. Nothing after it until the player answers — the two answers are `# restored` (turn it off) or `# armed` (keep trying) |
| `# reapply why=<reason>` | cap re-applied its order, in combat as well as out, after that event |

**`# contended` changes what the flight measures.** A run carrying contention is measuring cap
against another addon, not cap against the client, so its persistence result answers a different
question than the one you asked. `status` and the stream `Meta` carry the count.

**cap never stops ordering on its own.** A run of `CONTENTION_STRIKES` inside the window raises
a dialog asking whether to turn ordering off, and both answers are visible in the stream. A
capture that simply goes quiet after a `# contended` is a bug, not a back-off.

**`# stomp … combat=1` is the case to read first.** `RefreshLayout` fires in a pull from the
viewer's full-aura-update path and releases the whole frame pool. Every one of them must be
followed by a `# rearmed` or `# reapply` carrying `X{ok}`. A destructive stomp with nothing after
it until `# combat end` is the failure: the row spent the rest of the pull in Blizzard's order
while still looking like a priority scan. The item frames are unprotected, so nothing about
combat excuses it.

## The Havoc row — one flight for S3–S7

The whole row is built and flies **once**, not per slice. State the question, play, write the
answer down in your own words, and only then read a capture.

**The one player-experience question:** *does the row at rest read as quiet, and when it stops
being quiet, does the change point at one button?*

Play a few pulls on a target dummy and then something real, and record:

- At rest, out of combat and between packs — is the row calm, or is it a wall of borders and
  badges? (Shelf Q1. This one needs time on target; the `/cap style` gallery cannot answer it.)
- The scan edge — can you tell a lit row from an unlit one at a glance, mid-pull, without
  hunting? (Q2. The failure to watch for is a line nobody notices; if it fires, the answer is
  more area or a different blend, **never** a second colour.)
- Walking the row left to right and skipping what is swiped or wearing a negative badge: does that land on
  the button you would have pressed anyway? (Q5. Say where it does **not** — that is the finding.)
- Fury: do Chaos Strike and Blade Dance badge when you are short, and do the two generators warn
  before you overflow? Both are cues you should be able to describe **without** looking at a
  number.

Then, and only then, the captures:

- `wowkb.capture cap bind` — **is there a `# row-order` note?** If yes, the reading model does
  not hold for this Cooldown Manager layout and the whole elimination walk is pointed wrong;
  see `backlog.md`'s cap-owned-row fork before touching anything else.
- `wowkb.capture cap edge` — count `Available` edges for Chaos Strike and Demon's Bite. Silence
  is the intended behaviour. Edges arriving at rotational speed mean `ready` is tracking
  affordability, which the border was never meant to say, and which the player will have already
  reported as a blinking row.
- `wowkb.capture cap draw` — `C{}` for the two graded cues, and `P{}` for which rows were in the
  scan. Both say cap took the route it meant to. ⚠ `P{}` no longer carries the charge substitution
  that used to corroborate a `capped` badge; the cue is now the only term that reports it.
- `wowkb.capture cap tier` — `W{}` for **why a readable hold fired**. ⚠ **The Hunt's hold is no
  longer one of them.** It was a readable `ready:metamorphosis` marker until 2026-08-17; it is now
  two sealed bands (Eye Beam far, Metamorphosis near) gated on Eternal Hunt, so
  `the_hunt:hunt_awaits_meta` emits **no `W{}` line at all** and grepping for one finds nothing —
  which reads exactly like a hold that never fired. Judge The Hunt by eye and by `C{}`'s
  arm status; the gate blind spot above is why that is the only route.
  The `W{}` route still works for the readable holds that remain, chiefly Metamorphosis's
  `meta_wastes_eye_beam` and `meta_wastes_death_sweep`.

**Tuning is expected and is a shelf edit.** Too many badges, too loud a badge, too eager a snap —
change the numbers in `render-shelf.md` Part 6 and rebuild. A noisy first render is not a reason
to unpick a slice.

## Combined Phase 9 checkpoint flight

After installing the approved combined test build, record judgments in game before extracting
captures.

For Demonology, play a short pull containing a Demonbolt proc and Tyrant setup:

- Are the scan edges bright and distinct without flicker, and is it obvious which rows carry one?
  ⚠ **This list used to ask whether COOLDOWN, ROTATION and FALLBACK could be told apart
  categorically.** They cannot, by design: V13 draws one treatment, and since 2026-08-25
  membership IS the single bit — the tiers left the model, not just the paint. Rank is row order.
- Can it coexist with Blizzard's Demonbolt proc glow, or is one drowned out?
- ⚠ The Dreadstalkers and Grimoire dots no longer draw, so the two questions this list used to
  ask about them are unanswerable until they are re-authored as cues.
- Is the independent Tyrant countdown legible and worth its screen space?

For Destruction / Diabolist, begin from an exact 2/2 Conflagrate seed and play through 1/2,
0/2, and natural recharge:

- Does Conflagrate hold one steady scan treatment across the authored shard/charge states — its
  membership is the default ready-self, since the old two-band tier flip carried no membership
  information — leaving the scan only when genuinely on cooldown, without implying an exact
  in-combat count?
- Is Backdraft text absent below two applications and visibly `2` at two during restricted
  combat? Does that context help without reading as a press/hold verdict?

The captures then check only that the expected rows bound, reads answered, overlays anchored,
charge provenance changed from `live` to `napkin`, duplicate gains were filtered, sealed
channels armed or refused, readable markers were offered, and the bar path armed. No occupancy
target is an acceptance criterion. If the Tyrant bar is not useful, remove it. If the sealed
channel arms but is not visible or useful, keep Phase 9 open and iterate.
