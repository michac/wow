# Interrupt HUD

Three stacked rows — your stops, the target's cast, the focus's cast. A prototype, kept
deliberately small: its job was to answer questions only a live pull could answer.

`backlog.md` owns status and the work list. This file owns the design and why it is shaped
this way.

## Why it works at all

Under Midnight's secret-value system an addon may not **read** an enemy's cast, but it may
**show** one. Both bars are driven by sealed `LuaDurationObject`s whose contents are
unreadable and whose *presence* is plain — so nil-testing the object to decide whether to
draw is legal, while looking inside it is not. Nothing in `CastBar` branches on a value read
from a unit other than the player or their pet; secrets are handed to client-owned sinks
(`SetTimerDuration`, `SetVertexColorFromBoolean`, `SetAlphaFromBoolean`) instead.

Both bar hosts are protected frames carrying a `unit` attribute, which makes them
**mouseover surfaces**. With the client's mouseover casting on, a normal action-bar press
lands on whichever bar the cursor is over. No macros, no rebinding, and abilities stay on
the action bar.

## What the flight settled

All four questions the prototype was built for are answered. The measurements are claims in
`knowledge/addon-dev/`, where the KB's gates apply — this table is a pointer, not a record.

| Question | Answer |
|---|---|
| Does `UnitCastingDuration` return an object for a unit whose cast info is sealed? | **Yes** — the bar draws for the cast's real length |
| Does mouseover casting fire on an addon-created protected frame? | **Yes** — hovering the focus bar with nothing targeted casts on focus; the target bar raises *"nothing targeted"* rather than falling through |
| Does the interruptible split read at a glance? | **As colour, yes.** Red is kickable, steel-grey is not. As a 0.45 alpha it did not |
| Is `notInterruptible` readable for a non-player unit? | It is a **secret boolean** — unreadable, but drawable through a `*FromBoolean` sink |

`CastBar:Arm` still distinguishes **idle** from **failed**, and that stays: cast presence
cannot be read, so an `expecting` flag is tracked off `UNIT_SPELLCAST_START` / `_STOP`, and a
cast that is up with no duration object renders the reason instead of an empty bar.

Two things learned the hard way, both cheap to repeat:

- **`SetMinMaxValues(0, 1)` must precede any `SetTimerDuration`** or the bar draws 0% forever.
- **Tint only a flat fill.** `SetVertexColor*` multiplies, so status-bar art carrying its own
  shading returns a soft wash instead of the colour asked for.

## The readiness row

`Kit.lua`'s `SEED` maps each class token to its interrupts and cast-stopping crowd control.
All 47 ids are verified against 12.1 `SpellName` DB2. The table is keyed by the **non-localized**
class token from `UnitClassBase` (`PALADIN`, `DEATHKNIGHT`), never the localized name, which
changes with client language.

Resolving an icon only proves a spell exists, so every id is also checked against the
character's own spellbook — player bank, then pet bank, overrides included — and only what
this character can actually cast draws a cell. The row rebuilds on `SPELLS_CHANGED`,
`PLAYER_SPECIALIZATION_CHANGED` and `UNIT_PET`, so a talent swap or a summoned demon moves it.
An empty row says which of the three ways it got there.

## Deploy

It is a normal addon with its own repo and releases; ghaddons installs from the latest
GitHub release, so a push alone deploys nothing.

    uv run python -m wowkb.addon release ihud --patch

Then `/reload`. Commands: `/ihud show | hide | drag | reset | status | probe`.

- `status` reports whether **mouseover casting** is on — a client setting an addon cannot
  set. With it off the bars draw but nothing is pressable, which reads as a broken design
  when it is merely switched off. It also prints how many stops resolved versus how many
  this character knows.
- `probe` prints each bar's interruptible flag by **type and secrecy**, never its value.
- `drag` toggles the frame movable; the anchor is saved **per character**. `reset` returns it
  to centre, which is the way back if it is dragged somewhere unreachable. Both refuse in
  combat, because the bar hosts are protected.
