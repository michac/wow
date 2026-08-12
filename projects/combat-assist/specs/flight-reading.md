# Combat Assist Plus — reading a flight

**What this file is for:** the current capture fields and the mechanical checks they can
support. It is not a visual oracle or a history log. SavedVariables flush only on `/reload`.

Read the live addon version first. Captures store changes, not periodic samples, so line counts
are not duty cycles. A sink accepting a duration or a paint call never proves a pixel appeared;
the player's report is the authority for brightness, contrast, placement and usefulness.

## Streams

| Command | Carries |
| --- | --- |
| `wowkb.capture cap bind` | resolved CDM rows and binding health |
| `wowkb.capture cap tier` | the readable signal; the legacy stream name remains during migration |
| `wowkb.capture cap edge` | accepted and refused CDM alert edges |
| `wowkb.capture cap draw` | the static overlay and Tyrant-bar paths cap attempted |

Combat start/end are marked with a full body. A `# listener-error` in `tier` invalidates the
downstream draw evidence for that interval.

## Readable signal

```
S{n:2 on:2 mark:2 blind:0}
E{demonbolt:SOON tyrant:SOON+dreadstalkers,grimoire}
R{ready:2/2 proc:1/1 identity:1/1 resource:1/1}
Q{-}
S{settled/spells-changed}
```

- `on:` is the number of enhanced entries assigned a tier by readable facts.
- `mark:` is the number of readable context markers offered.
- `blind:` counts conditions withheld because a read was unknown.
- `E{}` names each enhanced entry, its emphasis, and any marker facts.
- `R{known/total}` distinguishes a false answer from a refused read.
- `Q{conflagrate:live|napkin|unknown}` records only charge provenance: `live` is an exact
  unrestricted seed; `napkin` is the bounded cast/alert estimate maintained after that seed.
- `settled/...` names the bind-settle arm; `DARK` means combat began before a safe roster
  settled and the addon intentionally drew nothing for that fight.

The stream can show that the authored mechanism fired. It cannot show that the Demonbolt tier
or either Tyrant fact was helpful.

## Draw surface

```
D{n:2 rows:2 anch:2 conf:2 off:0 nf:0 bar:tex/fmt/font stock:coexist}
P{demonbolt:SOON tyrant:SOON}
M{tyrant:dreadstalkers tyrant:grimoire}
B{tyrant:armed}
C{-}
```

- `anch:` / `conf:` say the addon found and confirmed CDM item frames.
- `off:` is a real but hidden item frame; `nf:` means no frame was found.
- `P{}` records the static tier treatment attempted for each enhanced entry.
- `M{}` records which fixed context dots cap showed.
- `stock:coexist` records the deliberate baseline: cap did not try to suppress Blizzard's
  proc glow.
- `B{tyrant:ready|armed|refused|unarmed|nobind}` records the bar path. `armed` means the
  client accepted a duration object, never that the fill or number was visible.
- `bar:` is the bar's build-time texture/formatter/font probe.
- `C{conflagrate:backdraft:offered|armed|refused}` reports only sealed-channel acquisition.
  It never reports whether Blizzard wrote a glyph or what that glyph contained.

A moving `P{}` with a blank screen points first to anchoring or treatment. Healthy `anch:` and
`conf:` with no visible pixels is a treatment failure. A marker in `M{}` at the wrong gameplay
moment is a product failure even when every mechanical field is healthy.

## Combined Phase 9 checkpoint flight

After installing the approved combined test build, record judgments in game before extracting
captures.

For Demonology, play a short pull containing a Demonbolt proc and Tyrant setup:

- Can ASAP, SOON and FALLBACK be identified categorically without comparing subtle brightness?
- Are the static borders bright and distinct without flicker?
- Can it coexist with Blizzard's Demonbolt proc glow, or is one drowned out?
- Are the left blue Dreadstalkers dot and right purple Grimoire dot identifiable during setup?
- Do the dots' honest but longer-lived commitment facts feel useful or misleading?
- Is the independent Tyrant countdown legible and worth its screen space?

For Destruction / Diabolist, begin from an exact 2/2 Conflagrate seed and play through 1/2,
0/2, and natural recharge:

- Does Conflagrate visibly move between SOON, FALLBACK, and off at the authored shard/charge
  states without implying an exact in-combat count?
- Is Backdraft text absent below two applications and visibly `2` at two during restricted
  combat? Does that context help without reading as a press/hold verdict?

The captures then check only that the expected rows bound, reads answered, overlays anchored,
charge provenance changed from `live` to `napkin`, duplicate gains were filtered, sealed
channels armed or refused, readable markers were offered, and the bar path armed. No occupancy
target is an acceptance criterion. If the Tyrant bar is not useful, remove it. If the sealed
channel arms but is not visible or useful, keep Phase 9 open and iterate.
