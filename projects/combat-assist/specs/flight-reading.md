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
E{demonbolt:on tyrant:on+dreadstalkers,grimoire}
R{ready:2/2 proc:1/1 identity:1/1 resource:1/1}
S{settled/spells-changed}
```

- `on:` is the number of enhanced entries emphasized by readable facts.
- `mark:` is the number of readable context markers offered.
- `blind:` counts conditions withheld because a read was unknown.
- `E{}` names each enhanced entry, its emphasis, and any marker facts.
- `R{known/total}` distinguishes a false answer from a refused read.
- `settled/...` names the bind-settle arm; `DARK` means combat began before a safe roster
  settled and the addon intentionally drew nothing for that fight.

The stream can show that the authored mechanism fired. It cannot show that the Demonbolt
strength or either Tyrant fact was helpful.

## Draw surface

```
D{n:2 rows:2 anch:2 conf:2 off:0 nf:0 bar:tex/fmt/font stock:coexist}
P{demonbolt:on tyrant:on}
M{tyrant:dreadstalkers tyrant:grimoire}
B{tyrant:armed}
```

- `anch:` / `conf:` say the addon found and confirmed CDM item frames.
- `off:` is a real but hidden item frame; `nf:` means no frame was found.
- `P{}` records the static emphasis state attempted for each enhanced entry.
- `M{}` records which fixed context dots cap showed.
- `stock:coexist` records the deliberate baseline: cap did not try to suppress Blizzard's
  proc glow.
- `B{tyrant:ready|armed|refused|unarmed|nobind}` records the bar path. `armed` means the
  client accepted a duration object, never that the fill or number was visible.
- `bar:` is the bar's build-time texture/formatter/font probe.

A moving `P{}` with a blank screen points first to anchoring or treatment. Healthy `anch:` and
`conf:` with no visible pixels is a treatment failure. A marker in `M{}` at the wrong gameplay
moment is a product failure even when every mechanical field is healthy.

## Phase 5 checkpoint flight

After installing a test build, play a short Demonology pull containing a Demonbolt proc and a
Tyrant setup, then `/reload` and extract all four streams. Judge these directly in game:

- Is the static gold border bright and distinct without flicker?
- Can it coexist with Blizzard's Demonbolt proc glow, or is one drowned out?
- Are the left blue Dreadstalkers dot and right purple Grimoire dot identifiable during setup?
- Do the dots' honest but longer-lived commitment facts feel useful or misleading?
- Is the independent Tyrant countdown legible and worth its screen space?

The captures then check only that the expected rows bound, reads answered, overlays anchored,
markers were offered and the bar path armed. No occupancy target is an acceptance criterion.
