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

- [x] Log `SetRenderMode`'s result in `buildDial` (`Channel.lua`).
- [x] Read `GetRenderMode` back **after** `SetTimerDuration` in `baseCooldownSink` and mark a
      mismatch, since that moment is the one `/cap style` never reaches.
- [x] Replace `Enum.StatusBarRenderMode and …Radial or 1` with an explicit refusal.
- [x] **Established, and the line did NOT cover it.** Both `[client 2026-08-21]` Radial
      measurements were taken on a bar the AuraContainer BUTTON claimed, through
      `SetApplicationBar` / `SetDurationBar`. `baseCooldownSink` is cap's own StatusBar, driven
      by cap calling `SetTimerDuration` on it directly — a different path with a different owner,
      never read back. `security-taint-and-restricted-data.md` §4.8.1 now excludes it by name and
      carries the `@verify-ingame`.

**The collision — a source read before any re-anchor.** cap's hotkey wins a fight it should not
have entered; the fix needs to know what the client owns first.

- [x] Read Blizzard's own `ChargeCount` and cooldown-text anchors off the 12.1 source — done, and
      it is `cooldown-manager.md` §1.5.
- [x] **Re-anchor cap's hotkey — NOT DONE, and the read is why.** §1.5's answer is that the
      **top-left quadrant carries no Blizzard text or number and the bottom-right carries all of
      it**, so cap's hotkey is already in the free corner and moving it would walk it into
      `ChargeCount`. The collision had a different author: cap's own V21 numeral, formatted as a
      sentence and centred in a 24 px badge, reached across the icon into the hotkey. Fixed at
      the formatter (`security-taint-and-restricted-data.md` §4.8.1 finding 2) and by bounding
      the FontString to its badge. ⚠ **The giant centred `1:36` is Blizzard's** — the `Cooldown`
      widget's own C-side text at `GameFontHighlightHugeOutline` on a 50 px icon, with no region
      to reparent (§1.5, point 3). **cap CAN suppress it**, per row, by the same route
      `Glow.lua` dims the proc glow; that is a product decision and it is the entry
      *`1:36` is Blizzard's number, and cap draws the same number* in `backlog.md`.

**The feature.**

- [ ] Point V18's segmented bar at a readable charge count, so the number leaves the icon face
      entirely. ⚠ Charges are **readable** (`Sense.readCapped` already calls
      `C_Spell.GetSpellCharges` every tick), so this needs no sealed sink and no lab question —
      it is a shelf primitive plus a catalog key.

## Then test

- [ ] Whether the hold dial draws as an arc or a rectangle, with the log now naming which of the
      three causes it was. Read it with `wowkb.capture cap bind` and grep `baseCooldownSink`.
      ⚠ A **silent** log is itself an answer: it means the mode was accepted AND survived the
      client's takeover, and the rectangle is coming from somewhere else — the likeliest
      remaining candidate being `Paint.BarFill`'s `SetColorTexture` fill, since Radial drives
      *"the managed texture's radial progress fill percent"* and an untextured swatch may have no
      such percent to drive.
- [ ] Whether the keybind hint still collides with anything, and whether the shortened numeral
      (`2m`, `57s`) is legible at 13 px inside the badge.
- [ ] Whether a charge bar reads better than the small number it replaces.
- [ ] Which two bound abilities wear no hint — `Binds.lua` cannot be diagnosed without their names.
- [ ] Whether position 1 draws Sentinel, and that cue A is now **silent** over it. ⚠ Silence is
      the whole of the fix: the row is not given a Sentinel treatment, because authoring
      `identity` on it still waits on the exhaustive every-set DB2 absence check below.

---

## Deliberately NOT in this round

Each is real, each is owned elsewhere, and each is bigger than one sitting.

- **The hatch losing to bright icon art** — a shelf change (Part 5 question 7, now answered in the
  direction the shelf feared). The fix is area or a different treatment and explicitly **not** a
  hue; the blend has no headroom left. ⚠ **It has since been PROMOTED out of this flight** —
  `backlog.md` → *The hatch is paid on every scan* is its one home, because the 2026-09-01 fold
  decision makes the hatched top line the first thing walked on every scan, on all four folding
  specs. It is no longer Protection's bright icon; do not re-argue it here.
- **Reversing one swipe so a running buff and a running cooldown differ in SHAPE** — the
  highest-value unbuilt item in `backlog.md`, and it needs a `render-shelf.md` V7 amendment first
  because V7 currently declares the opposite.
- **Authoring `identity` for Sentinel on position 1** — blocked on an exhaustive every-set DB2
  absence check; the current evidence is Protection's own inventory file, one tier weaker than the
  Sacred Weapon claim it would copy.
- **The Consecration presence band** — needs a Blessed Assurance build, and the flown one carried
  Divine Guidance.
