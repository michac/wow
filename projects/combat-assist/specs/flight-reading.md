# Combat Assist Plus — reading a flight

**What this file is for:** the current capture fields and the mechanical checks they can
support. It is not a visual oracle or a history log. SavedVariables flush only on `/reload`.

Read the live addon version first. Captures store changes, not periodic samples, so line counts
are not duty cycles.

⚠ **Accepted is not drawn** — `pattern-shelf.md` Part 2 states it once, and it applies to every
field below without being repeated per field: a sink accepting a duration or a paint call never
proves a pixel appeared. The player's report is the authority for brightness, contrast, placement
and usefulness.

## Streams

| Command | Carries |
| --- | --- |
| `wowkb.capture cap bind` | resolved CDM rows and binding health, plus the row-order note |
| `wowkb.capture cap tier` | the readable signal; the legacy stream name remains during migration |
| `wowkb.capture cap edge` | accepted and refused CDM alert edges |
| `wowkb.capture cap draw` | the static overlay and Tyrant-bar paths cap attempted |

Combat start/end are marked with a full body. A `# listener-error` in `tier` invalidates the
downstream draw evidence for that interval.

A `# row-order <a> is laid out after <b>` note in `bind` is the **structural** finding, not a
per-ability one: it says this player's Cooldown Manager lays the row out in an order the
catalog's left-to-right reading model does not hold for, which makes elimination point at the
wrong button everywhere at once. It is written once per change of finding and echoed to chat.
**Its ABSENCE on a flight that bound a full roster is the positive result** — that is the check
that the whole reading model rests on.

## Readable signal

```
S{n:2 on:2 mark:2 blind:0}
E{demonbolt:ROTATION tyrant:ROTATION+dreadstalkers,grimoire}
R{ready:2/2 proc:1/1 identity:1/1 capped:1/1 affordable:2/2 resource:1/1}
W{tyrant:dreadstalkers:on(!ready:dreadstalkers=T) tyrant:grimoire:off(identity:grimoire:transformed=F)}
Q{-}
S{settled/spells-changed}
```

- `on:` is the number of enhanced entries assigned a tier by readable facts.
- `mark:` is the number of readable context markers offered.
- `blind:` counts conditions withheld because a read was unknown.
- `E{}` names each enhanced entry, its emphasis, and any marker facts.
- `R{known/total}` distinguishes a false answer from a refused read. The predicates are
  `ready proc identity capped affordable resource`, always in that order — `capped` is the
  charge-state read (`GetSpellCharges().isActive`) and `affordable` the power one
  (`IsSpellUsable`'s second return). A spec that uses neither reports `0/0` for it, which is
  not a failure.
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
- `Q{conflagrate:live|napkin|unknown}` records only charge provenance: `live` is an exact
  unrestricted seed; `napkin` is the bounded cast/alert estimate maintained after that seed.
- `settled/...` names the bind-settle arm; `DARK` means combat began before a safe roster
  settled and the addon intentionally drew nothing for that fight.

The stream can show that the authored mechanism fired. It cannot show that the Demonbolt tier
or either Tyrant fact was helpful.

## Draw surface

```
D{n:2 rows:2 anch:2 conf:2 off:0 nf:0 bar:tex/fmt/font stock:coexist}
P{demonbolt:ROTATION tyrant:ROTATION immolation_aura:CHARGES/veil+blocked}
M{tyrant:dreadstalkers tyrant:grimoire}
B{tyrant:armed}
C{-}
```

- `anch:` / `conf:` say the addon found and confirmed CDM item frames.
- `off:` is a real but hidden item frame; `nf:` means no frame was found.
- `P{}` records the composed treatment attempted for each enhanced entry, as
  `id:LANE[/veil][+cue,cue]` — or `id:off` where the row drew nothing, `id:hidden` where its
  CDM item is real but not shown, `id:noframe` where no item was found. The lane is the drawn
  one, so a charge ability at rest reads `CHARGES`, not the role lane its catalog authored.
  The veil is **derived**, never authored: it is present iff a negative cue is.
  ⚠ **Only READABLE cues appear here.** A graded (sealed) cue's visibility is the client's, so
  it is reported in `C{}` as armed and never in `P{}` — a row wearing only a graded cue reads
  as un-veiled here while dimming on screen, and that is correct, not a discrepancy.
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

## The Havoc row — one flight for S3–S7

The whole row is built and flies **once**, not per slice. State the question, play, write the
answer down in your own words, and only then read a capture.

**The one player-experience question:** *does the row at rest read as quiet, and when it stops
being quiet, does the change point at one button?*

Play a few pulls on a target dummy and then something real, and record:

- At rest, out of combat and between packs — is the row calm, or is it a wall of borders and
  badges? (Shelf Q1. This one needs time on target; the `/cap style` gallery cannot answer it.)
- Immolation Aura's purple CHARGES border — does it read as a different **kind** of statement
  than the blue rotation borders around it, or just as another colour? (Q3.)
- Walking the row left to right and skipping what is swiped, veiled or badged: does that land on
  the button you would have pressed anyway? (Q6. Say where it does **not** — that is the finding.)
- The arrival snap: too frequent, too subtle, or about right?
- Fury: do Chaos Strike and Blade Dance dim when you are short, and do the two generators warn
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
- `wowkb.capture cap draw` — `C{}` for the two graded cues and the CHARGES lane in `P{}`. Both
  say cap took the route it meant to.
- `wowkb.capture cap tier` — `W{}` for **why a hold fired**. For The Hunt, grep
  `the_hunt:hunt_awaits_meta`: an `on(...)` line names the readiness that held it (e.g.
  `ready:the_hunt=T,ready:metamorphosis=T`); an `off(ready:metamorphosis=F)` line is Meta
  reading on-cooldown, i.e. the hold correctly standing down. If the hold sits `on` with
  `ready:metamorphosis=T` across the whole fight while Meta was being pressed on cooldown, the
  readiness latch is stuck, not the gameplay rule — a bug, not a tuning question.

**Tuning is expected and is a shelf edit.** Too many badges, too heavy a dim, too eager a snap —
change the numbers in `render-shelf.md` Part 6 and rebuild. A noisy first render is not a reason
to unpick a slice.

## Combined Phase 9 checkpoint flight

After installing the approved combined test build, record judgments in game before extracting
captures.

For Demonology, play a short pull containing a Demonbolt proc and Tyrant setup:

- Can COOLDOWN, ROTATION and FALLBACK be identified categorically without comparing subtle
  brightness?
- Are the static borders bright and distinct without flicker?
- Can it coexist with Blizzard's Demonbolt proc glow, or is one drowned out?
- ⚠ The Dreadstalkers and Grimoire dots no longer draw, so the two questions this list used to
  ask about them are unanswerable until they are re-authored as cues.
- Is the independent Tyrant countdown legible and worth its screen space?

For Destruction / Diabolist, begin from an exact 2/2 Conflagrate seed and play through 1/2,
0/2, and natural recharge:

- Does Conflagrate visibly move between ROTATION, FALLBACK, and off at the authored shard/charge
  states without implying an exact in-combat count?
- Is Backdraft text absent below two applications and visibly `2` at two during restricted
  combat? Does that context help without reading as a press/hold verdict?

The captures then check only that the expected rows bound, reads answered, overlays anchored,
charge provenance changed from `live` to `napkin`, duplicate gains were filtered, sealed
channels armed or refused, readable markers were offered, and the bar path armed. No occupancy
target is an acceptance criterion. If the Tyrant bar is not useful, remove it. If the sealed
channel arms but is not visible or useful, keep Phase 9 open and iterate.
