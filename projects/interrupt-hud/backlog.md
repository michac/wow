# Interrupt HUD — backlog

**What this file is for:** the current implementation status and the ordered work list.
`README.md` owns the design and why the frame is shaped the way it is.

The live addon version comes from `wowkb.addon list`, never from prose here.

**Measurements do not live here.** A fact the prototype established about the client belongs in
`knowledge/addon-dev/`, where the KB's gates apply and the next reader will actually find it. A
status line may say a thing works; the evidence that it works is a claim in a topic file.

**An item here has to keep earning its place.** If its premise stopped being true, rewrite it or
delete it — never leave it standing with a note underneath.

## Status

**It records what is BUILT.** Three stacked rows: the player's own interrupts and stops dimmed
when on cooldown, the target's cast bar, the focus's cast bar. Commands are
`show | hide | drag | reset | status | probe`.

- **The two cast bars draw off sealed duration objects and nothing is read.** `CastBar:Arm`
  distinguishes idle from failed — cast presence cannot be read for a non-player unit, so an
  `expecting` flag is tracked off `UNIT_SPELLCAST_START` / `_STOP` and a cast that is up with no
  duration object renders the reason instead of an empty bar.
- **Interruptibility is a red/grey split**, `SetVertexColorFromBoolean` on a flat fill. Red is the
  cast the player can kick.
- **Casts fill, channels drain.**
- **Both bar hosts are mouseover-casting surfaces** — protected frames carrying a `unit`
  attribute, so with the client's mouseover casting on, a normal action-bar press lands on
  whichever bar the cursor is over. No macros, no rebinding. `/ihud status` reports whether the
  client setting is on, because when it is off the bars draw and nothing is pressable.
- **The readiness row is seeded per class** from `Kit.lua`'s `SEED`, all 47 ids verified against
  12.1 `SpellName` DB2, and filtered to what the character has actually learned — player bank
  then pet bank, overrides included. It rebuilds on `SPELLS_CHANGED`,
  `PLAYER_SPECIALIZATION_CHANGED` and `UNIT_PET`. An empty row says which of the three ways it
  got there; `/ihud status` prints resolved versus known.
- **The frame anchor is saved per character**, and `/ihud reset` returns it to centre. Both it
  and `drag` refuse in combat, because the bar hosts are protected.

Flown on Protection Paladin, in an instance. What the flight settled is recorded in
`knowledge/addon-dev/` — OBS-082/083/084, all drained.

## Now

### Is the seed the RIGHT set of stops, now that every id in it is real?

All 47 ids verify against 12.1 `SpellName` DB2 and only what the character knows draws, so the
row no longer lies. What has never been checked is whether the *set* is complete: it was written
from memory, not derived. The systematic pass is `SpellMechanic` / `SpellCategories.Mechanic` for
the stop mechanics — stunned 12, fleeing 5, disoriented 2, incapacitated 14, asleep 10,
horrified 24, silenced 9, knockbacked 6, sapped 30, polymorphed 17, banished 18, frozen 13 —
**not** rooted 7 or slowed 8. A missing stop is invisible; nothing in the addon can flag it.

⚠ **Three Warlock ids share names with variants** — `19647`/`119910`/`132409` are all *Spell Lock*,
`89766`/`119914` both *Axe Toss*. The spellbook filter picks whichever the character actually has,
so this is handled rather than fixed, and a Warlock pull should confirm a cell appears with a
Felhunter out.

### Is red-means-kickable the right polarity?

It inverts what the original design specified (opaque = cannot be kicked). The current reading
puts the loud colour on the actionable state, which is why it reads — but that was changed at the
same time as the channel, so it has never been tested on its own. Only worth revisiting if the
split stops reading in a busier pull.

### The alpha treatment was never fairly tested

Alpha and polarity moved in one edit, so *alpha vs colour* is confounded and the KB claim is
deliberately narrow. One build settles it — the alpha treatment at correct polarity with a harder
split. Worth doing only if there is a reason to want the bar a single colour.

### A Warlock or Druid pull to exercise the spellbook filter

Protection Paladin is the only class flown, and all four of its stops are unconditional — so the
filter has never had to drop anything. The cases that would prove it are a Warlock (pet-bank ids,
a talented Shadowfury) and a Druid (`Solar Beam` is Balance-only). Watch that the row rebuilds on
summon and on a talent swap rather than only on `/reload`.
