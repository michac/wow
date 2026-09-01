# Protection Paladin — the flight

The plan file for `backlog.md` → `## Now` → *Devourer drew nothing, and Protection has still not
been seen*. Delete it when the flight lands and `notes.md` records the round.

Protection is the **only** spec carrying a `sealed-pandemic` besides Demonology, and Demonology has
no catalog Lua of the current design — so **V19 has never been on a screen anywhere**, and this
flight is the only route to it. It also carries two `@verify-ingame` markers that a few minutes of
play settle, one of which **two specs are resting on**.

---

## 0. Setup — do this before you pull, or the flight cannot fail honestly

**This is a LIGHTSMITH flight, and that is a hard gate.** Holy Armaments is a Lightsmith hero
talent, and so are **both** halves of the build split below — Blessed Assurance and Divine Guidance
are two entries on the same node (`95235`) *[T1: `ability-inventory.tsv` @ 12.1.0]*. On **Templar**
there is no Holy Armaments row at all, so the V19 badge — the headline of this flight — cannot
appear, and its absence would mean nothing.

**Decide what to do about SENTINEL first — it replaces the Avenging Wrath button.** Both are
talentable (separate nodes, one point each), but the live client prints *"Replaced by Sentinel"* on
the Avenging Wrath tooltip, so with Sentinel talented **position 1 displays Sentinel** and the
catalog does not know. Two ways to fly, and they answer different questions:

- **Untalent Sentinel** → positions 1 and 2 test the catalog **as authored**, which is what the
  flight below is written against. ⚠ On Lightsmith, Avenging Wrath also feeds the flight's own
  headline: *Blessing of the Forge* has it summon an additional Sacred Weapon.
- **Keep Sentinel** → position 1 answers the **new** question instead (`## Now`): does the row
  display Sentinel, and does cue A wear its *hold for Divine Toll* badge over it? A **yes** to both
  is the finding, because that badge argues an offensive window over a defensive button.

⚠ **Either way, spend thirty seconds looking at position 1 before changing talents** — with Sentinel
still on, that observation is free and nothing else in the flight produces it.

⚠ If you take **Righteous Protector**, cue B is withheld by the talent gate (H) and position 2
wearing nothing is CORRECT.

**Six auras must be in your Tracked Buffs viewer.** Three are read as latches, three are the
subjects sealed displays drive off. A subject that does not resolve draws **nothing**, and nothing
looks exactly like a correct dark marker — which is the failure mode this whole flight is aimed at,
so it must not be self-inflicted.

| Aura | ID | Why it is needed |
| --- | ---: | --- |
| Sacred Weapon | `432502` | subject of the **V19 pandemic badge** — the headline |
| Consecration (standing in) | `188370` | subject of the **presence band** |
| Divine Guidance | `433106` | subject of the count bands on Avenger's Shield + Consecration |
| Vanguard | `1267203` | latch — gates two Avenger's Shield markers |
| Blessed Assurance | `433015` | latch — gates the Judgment hold |
| Shining Light | `321136` | latch — gates the Word of Glory hold |

**Then pick your build and know which half you are flying.** The catalog splits on a choice node
and the two halves light different markers:

- **Blessed Assurance** → `cons_field_up` (the Consecration presence band) and the Judgment hold
  are live; the Divine Guidance count bands are dead, because that count can never reach five.
- **Divine Guidance** → the two count bands are live; `cons_field_up` is dark.

⚠ **You cannot fly both in one sitting and you should not try.** Fly the one you actually tank on.

Also worth knowing: **Divine Toll's hold only exists without Righteous Protector** (`dt_awaits_wrath`
carries `!talent(righteous_protector)`). If you are talented into it, that badge is *correctly*
absent.

---

## 1. The one player-experience question

State it before you play, answer it in your own words afterwards, and read no capture until you have.

> **This catalog spends no positive cue at all. With nothing on the row saying *press this*, does
> elimination alone land you on the button you would have pressed — while tanking, where the row is
> not the only thing you are watching?**

That is `render-shelf.md` Part 5 question 5, sharpened to the one spec that has to answer it
without help. Protection is the honest test of it: Havoc and Retribution both carry promotions, and
`catalog.md` → *Why this catalog does not spend a positive cue* is an argument that has never been
in front of an eye.

**The finding is where it does NOT land on your button.** Say so specifically — which pull, which
button you pressed, which one the walk pointed at. A walk that works is one line; a walk that fails
is the whole value of the flight.

---

## 2. Play, and record these in your own terms

A few pulls on a dummy to see the row at rest, then real packs — Protection's reading happens under
pressure and a dummy cannot produce that.

- **The V19 badge on Holy Armaments.** Inside the Sacred Weapon window, does a gold dial appear on
  the row and drain? This is the headline: cap hands the widget to the client and reads nothing, so
  either the client drives it or it sits at zero forever. **A dial frozen at 0% is a failure and it
  is a specific one** — `ApplyDurationBar` never calls `SetMinMaxValues`, and the addon setting the
  range itself is the guard against exactly that.
- **Does it appear only near the end of the window?** It rides `AddPandemicRegion`, so the whole
  badge — halo, plate, dial — should show up in the refresh window and vanish outside it, not sit
  there all buff. If it is visible for the full 20 s the wrapper is not doing its job.
- **The Consecration presence band** (Blessed Assurance builds). Standing in your own Consecration,
  does the band mark? Step out — does it stop? This aura has `Duration = -1`, so presence is the
  only shape it can ever draw; there is no clock to expect.
- **The Divine Guidance count bands** (Divine Guidance builds). Do Avenger's Shield and Consecration
  band as the stacks climb toward five?
- **The row at rest.** Between packs, is it calm, or a wall of red? Protection has seven negative
  markers and one shared red. If they under-differentiate, the fix is different **shapes**, not a
  second hue.
- **The `blocked` dials.** Avenging Wrath, Divine Toll and Holy Armaments hold with a V21 dial that
  says *how long*. Does the dial read better than a still glyph would — and can you tell it apart
  from the badge in the next corner?

---

## 3. Two marked facts, settled by looking — do these deliberately

Both are `@verify-ingame` on `catalog.md` and both are cheap. Neither needs a capture.

- [ ] **Which way round the Sacred Weapon transform reads.** Game data proves Sacred Weapon `432472`
      has no Cooldown-Manager row anywhere, so it can only reach the CDM as an override on Holy
      Bulwark `432459`. **What is unproven is the direction**: whether `base` is Holy Bulwark and
      `transformed` is Sacred Weapon, or whether the row simply displays whichever armament is next
      with no override at all. Watch the Holy Armaments row across a full alternation and write down
      **which icon it wears when**. `ha_banks_bulwark` fires on `identity(base)` and the V19 badge on
      `identity(transformed)` — if the badge appears on the *bank* half, the direction is backwards
      and the catalog needs correcting, not the code.
- [ ] **Whether Hammer of Wrath rides the Judgment row.** This is Tier 2, sourced from a 12.0.7 file
      that carries its own `@verify-ingame`, and **Retribution's catalog rests on the same claim**.
      Get a target under execute range and watch the Judgment row: does the icon become Hammer of
      Wrath? ⚠ Measuring it once here closes it for both specs.

---

## 4. Only then, the captures

`/reload` first — SavedVariables flush on reload or logout, and a reload **in combat** produces a
blank cap, which is not a regression (`flight-reading.md`).

- `wowkb.capture cap bind` — **is there a `# row-order` note?** If yes, the reading model does not
  hold for your Cooldown Manager layout and the elimination walk above was pointed wrong; nothing
  else in the flight can be judged until that is understood.
- `wowkb.capture cap draw` — `C{}` for the graded cues and `P{}` for which rows were in the scan.
  ⚠ Shield of the Righteous is this catalog's **only** conditional member (`affordable(self)`), so it
  is the one row whose scan membership should come and go; everything else is a default ready-self
  member and should be steady.
- `wowkb.capture cap tier` — `W{}` for **why a readable hold fired**. The readable holds here are
  the Judgment/Blessed Assurance one and the Word of Glory/Shining Light one. ⚠ The three sealed
  bands emit **no `W{}` line at all**, and that reads exactly like a hold that never fired — judge
  those by eye and by `C{}`, never by grepping for a `W{}` that cannot exist.
- Grep `windowSink: SetDurationBar refused` and `# stomp RefreshLayout destructive=1 combat=1`.
  The first is V19 failing loudly rather than silently; the second is the mid-combat layout teardown
  that the Havoc/Retribution week did not reach.

---

## 5. What this flight cannot settle

Say these are unanswered rather than letting a green run imply otherwise.

- **Defeat 1 stands whole.** A sealed display can say *this aura is up* and can never say *this aura
  is absent* — absence draws nothing and nothing is indistinguishable from a refusal. Reading the
  absent case needs a boolean in a Lua condition, which needs the Category-3 TrackedBar alert-edge
  measurement. **No amount of looking answers it.**
- **The `shows` rollout has not happened here.** `ha_weapon_absent`, `ha_weapon_window` and
  `ha_weapon_healthy` all draw the entry's **base** face rather than Sacred Weapon's. Expect the
  wrong icon on those state cards; it is a known gap, not a finding.
- **`cons_field_up`'s provenance is loose.** Its subject resolves through a rung that merely
  *mentions* Consecration, while the fact it draws lives in two other rungs. The display can be
  correct and still be justified by a weaker thing than it looks.
- **V12 and the `gated` kind** have no consumer on Protection and are not exercised by this flight.
