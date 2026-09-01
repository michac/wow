# Protection — what to add, then test

The work list that came out of the **first Protection flight** (2026-08-31), which is written up in
`backlog.md` → *THE FIRST PROTECTION FLIGHT*. That entry owns the findings and the evidence; this
file owns only what to do about them and in what order.

⚠ **`protection-flight.md` is the other half and is not superseded.** It carries the setup gate,
the one player-experience question and the primer. This file assumes that one has been read; the
tests below are things to add to its section 5, not a second flight.

⚠ **Nothing here is a release.** Cutting one is a separate decision under `../../CLAUDE.md`
§ Releasing, and this list does not make it.

---

## Add

**The dial — instrumentation before any fix.** The shape is the largest open question and three
causes are still live; every step here is a read-back, not a redesign.

- [ ] Log `SetRenderMode`'s result in `buildDial` (`Channel.lua`) — it is the only pcall on that
      bar with no `ns.Log.Mark`, and it is the one deciding arc-versus-rectangle.
- [ ] Read `GetRenderMode` back **after** `SetTimerDuration` in `baseCooldownSink` and mark a
      mismatch, since that moment is the one `/cap style` never reaches.
- [ ] Replace `Enum.StatusBarRenderMode and …Radial or 1` with an explicit refusal, because a nil
      enum currently posts a guessed literal instead of failing.
- [ ] Establish which sink the *"Radial is measured on a SetTimerDuration-driven bar
      [client 2026-08-21]"* line was measured on, as it may never have covered `baseCooldownSink`.

**The collision — a source read before any re-anchor.** cap's hotkey wins a fight it should not
have entered; the fix needs to know what the client owns first.

- [ ] Read Blizzard's own `ChargeCount` and cooldown-text anchors off the 12.1 source into
      `knowledge/addon-dev/cooldown-manager.md`, which records neither today.
- [ ] Re-anchor cap's hotkey off whichever corners that read says the client already owns.

**The feature.**

- [ ] Point V18's segmented bar at a readable charge count, so the number leaves the icon face
      entirely. ⚠ Charges are **readable** (`Sense.readCapped` already calls
      `C_Spell.GetSpellCharges` every tick), so this needs no sealed sink and no lab question —
      it is a shelf primitive plus a catalog key.

## Then test

- [ ] Whether the hold dial draws as an arc or a rectangle, with the log now naming which of the
      three causes it was.
- [ ] Whether the keybind hint still collides with the client's count or its countdown text.
- [ ] Whether a charge bar reads better than the small number it replaces.
- [ ] Which two bound abilities wear no hint — `Binds.lua` cannot be diagnosed without their names.
- [ ] Whether position 1 draws Sentinel, and whether cue A wears its *hold for Divine Toll* badge
      over it.

---

## Deliberately NOT in this round

Each is real, each is owned elsewhere, and each is bigger than one sitting.

- **The hatch losing to bright icon art** — a shelf change (Part 5 question 7, now answered in the
  direction the shelf feared). The fix is area or a different treatment and explicitly **not** a
  hue; the blend has no headroom left.
- **Reversing one swipe so a running buff and a running cooldown differ in SHAPE** — the
  highest-value unbuilt item in `backlog.md`, and it needs a `render-shelf.md` V7 amendment first
  because V7 currently declares the opposite.
- **Authoring `identity` for Sentinel on position 1** — blocked on an exhaustive every-set DB2
  absence check; the current evidence is Protection's own inventory file, one tier weaker than the
  Sacred Weapon claim it would copy.
- **The Consecration presence band** — needs a Blessed Assurance build, and the flown one carried
  Divine Guidance.
