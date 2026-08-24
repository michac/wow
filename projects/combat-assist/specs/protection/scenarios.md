---
title: Protection Paladin — the scenario catalog
spec: Protection Paladin (Lightsmith) — specID 66, Midnight 12.1
---

# Protection Paladin (Lightsmith) — the scenario catalog

**What this file is for.** `catalog.md` maps every ability to a role lane and the cues. This file is the **proof** that lane + cues actually reproduce the priority order — state by state, naming the press and, for every button that is available and skipped, the reason. It is what `capart check`'s reading gate mechanises, and it is where this design gets falsified. ⚠ **It falsified two things this pass** (*What this walk falsified*, at the end) and it **deletes one marker from the catalog's design** — the resolution the catalog deferred here.

**Cross-links.** `catalog.md` (beside this file) is the definition — roster, lanes, markers,
contract boundary. `../spec.md` §3.1 owns the tier model and §3.6 the readable/sealed boundary;
`../authoring.md`'s recipe index owns the recipe IDs and their evidence anchors;
`../render-shelf.md` owns every pixel and this file describes none. Priority source:
`knowledge/classes/paladin/protection/simc-apl.md` (Tier 1, generated, commit `0132642`),
whose prose supplement `rotation.md` is a deliberate pointer stub; neither is restated here.

**Three files per spec** (`../authoring.md` §0): a definition, its proof, and its safety case.
Demonology is the model this walk is shaped against.

---

## The state walk

Fourteen states, each naming the press, and for **every button that is available and skipped**,
the reason. Buttons the Cooldown Manager has already swiped need no explanation. The walk reads
the authored row order left to right and must satisfy the shape `capart check`'s **elimination
gate** enforces: *the leftmost entry that is neither swiped nor wearing a negative badge is the
press.*

Shorthand, defined once: **HP** = Holy Power · **DG** = Divine Guidance (the Lightsmith stacking
buff, `433106`) · **BA** = Blessed Assurance (`433015`, DG's partner on choice node `95235` — a
build has exactly one of them) · **RP** = Righteous Protector · **AW** = Avenging Wrath ·
**HoW** = Hammer of Wrath. Rungs are positions in `actions.default`, `auto_attack` = 1 to
`consecration` = 29. **The default build for this walk is RP + Divine Guidance + Blessed
Hammer**; where a scenario is on the other half of a choice node it says so in its **State**.

### The **CDM row** bullet is machine-read

Every scenario below carries a `- **CDM row.**` bullet in a fixed grammar — **nine entries in
authored order, separated by ` · `, each `<Ability> \`<verdict>\``**.
`wowkb.capart import scenarios protection` scrapes it into the preview's sidecar and
`wowkb.capart check protection` re-scrapes it and fails if the two disagree, so **this document
leads and the preview follows**.

⚠ **The ability name is whatever the Cooldown Manager would *display* in that state** — `Sacred
Weapon`, not `Holy Bulwark`, while row 4 is transformed; `Hammer of Wrath`, not `Judgment`, while
row 7 is transformed; `Blessed Hammer` for row 8 on this walk's build, and `Hammer of the
Righteous` for a reader on the other side of the spec choice node at 3,19. That is the identity
the client draws and the swipe follows.

A verdict says what cap concluded, never what the button looks like: **the pixels belong to
`../render-shelf.md`**. `cd` = swiped by Blizzard, no cap opinion. `hold-readable` /
`hold-sealed` = the red `blocked` badge, from a readable Lua term or from a sealed band the
client paints. `starved` = the red affordability badge. `overcap` = the red waste badge, unspent
in this catalog. `off-mode` = the mode pawn, also unspent — `aoe` is never named here.
`press` = the button an unobstructed scan reaches. `below` = shown, but the walk never got
there. ⚠ `press` and `below` render identically, by design — the press is not something cap
draws.

⚠ **`ruled-sealed` is the third eliminating signal**, and this catalog leans on it harder than
any before it. It is neither Blizzard's swipe nor cap's badge: the client evaluated a **band
table cap authored** against an aura count cap never saw, and drew the hatch and a negative mark
out of the one FontString the count sink owns. The row reads as ruled out and wears **no cue at
all**, because a cue is a badge *cap* shows. `capart check`'s elimination gate knows about it
explicitly (`tokens.verdicts.ruled-sealed.eliminates`); nothing about it is inferred. ⚠ It is
also **not budgeted**, and that is not a loophole — it is the fact the density resolution below
turns on.

⚠ **`{sealed: …}` is an annotation channel, not a cue**, and it names the SINK rather than the
picture: `count-bands` (V16/V17) is the only one this catalog arms. It appears on a row exactly
where that display is **drawing something in that state** — a band at its silent value, or an
aura that is not up at all (no aura, no button, no sink), carries no annotation. What VALUE the
client found is deliberately nowhere in this file: that is the one thing cap cannot know.

⚠ **No entry in this catalog wears a positive cue**, so **every** scenario here is judged by pass
2 of `../render-shelf.md` Part 0.5, elimination. Why Protection declines both positive cues is
argued in `catalog.md` (*Why this catalog does not spend a positive cue*), and the closest call —
`priority` on the Judgment row — is what *Resolving the density problem* below settles.

⚠ **Five states are deliberately absent from this walk**, and their absence is the finding rather
than an omission — see *The state this walk does not contain*, at the end.

---

### Resolving the density problem — the one thing this walk was asked to decide

`catalog.md` → *Defeats*, item 7 records a state in which **three** budgeted holds stand between
the left edge and the press, against `../render-shelf.md` Part 0.5's budget of **two**, and
defers the resolution here: *"the honest move is to delete a hold rather than add a badge, and
the walk decides which."* The walk decides. **`cons_no_guidance` is deleted.**

**First, the state the catalog names is not the state that overflows.** Defeat 7 describes it as
Shield of the Righteous unaffordable, Holy Armaments held by cue **D**, Avenger's Shield held by
cue **E**, Consecration held by cue **E**, press Hammer of Wrath, *with Divine Guidance below
five*. But below five **with the aura present**, Consecration is not held by a badge at all — it
is eliminated by `cons_awaits_hammer`'s low band, which is `ruled-sealed`: client-drawn, carrying
no cue, and explicitly outside the budget. On the build the catalog is written for, that state
costs **two** budgeted holds and passes the gate — it is **PROT-8** below, and its press is
correct. The count in Defeat 7 is right and the state it attaches to is wrong.

**The state that actually overflows is the one where the DG aura is *absent*.** Then the sealed
complement has no subject — no aura, no button, no sink — and `cons_no_guidance`, a readable
`blocked`, does the eliminating instead. That happens on a **Blessed Assurance build**, where DG
can never exist at all, and for the single GCD after a five-stack Consecration on a DG build.
There it is routine, not exotic: **PROT-13**.

**Second, there are two such trios, not one.** Cue **A** (Avenging Wrath waiting for Divine Toll)
substitutes for cue **D** in the same shape: `{A, as_awaits_hammer, cons_no_guidance}` is
reachable whenever Avenging Wrath is ready with Divine Toll more than ten seconds out, in the
same execute state. Deleting cue **D** — the candidate Defeat 7's phrasing points at — fixes only
the first trio. **Deleting `cons_no_guidance` fixes both**, because it is the common term.

**Third, `cons_no_guidance` is the hold that earns its place least**, and the argument is not
that it is wrong:

1. **Its job is already done for free on the build the catalog is written for.** On a Divine
   Guidance build with stacks the identical elimination arrives as `ruled-sealed` from
   `cons_awaits_hammer`'s low band, at zero cost to the reader. The marker exists solely to cover
   the case where the aura is absent — which is a whole build (Blessed Assurance) plus one GCD.
   **It is the only marker in the catalog whose entire function is to convert a free elimination
   into a budgeted one.**
2. **Its deletion costs the smallest rung distance of the three.** Without it the walk presses
   Consecration where the APL presses Hammer of Wrath: rung 19 against rung 16 with the ground
   effect down, rung 29 against rung 16 with it up. Consecration is never a forbidden press — it
   is a button three rungs further down the same list, and it is the spec's most-pressed one.
   Deleting cue **D** instead would put the press on Holy Bulwark at rung 23; deleting
   `as_awaits_hammer` would put it on Avenger's Shield at rung 18 in *every* execute state on
   *every* build, including the DG build that currently reads correctly.
3. **The loss is bounded in time.** Hammer of Wrath is not lost, only delayed by one global: the
   moment Consecration goes on cooldown the walk reaches row 7 again.

⚠ **It is being deleted for density, not for being wrong** — and the catalog's claim that it *is*
wrong on a Blessed Assurance build is itself false (*What this walk falsified*, item 1). That
distinction matters, because it is what makes the deletion reversible: a **readable** substitute
for the DG count, or a measured Category-2 row for the DG aura on a BA build, would make the
marker cost nothing again.

**What the walk keeps.** Cues A, B, C, D, E's Avenger's Shield half, F, G, H and both
`sealed-count-bands` tables are unchanged and every one of them is exercised below. The catalog's
cue vocabulary is otherwise confirmed as authored.

---

### PROT-1 · The opener — everything ready, and rung 5 is position 1

- **State.** Pull timer at zero, every cooldown up, **0 HP**, Consecration already down from
  `actions.precombat` and therefore swiped, no Glory of the Vanguard, no Shining Light, row 4
  armed as **Holy Bulwark**, row 7 in its base life.
- **CDM row.** Avenging Wrath `press` · Divine Toll `below` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Holy Bulwark `below` ·
  Avenger's Shield `below` · Consecration `cd` · Judgment `below` · Blessed Hammer `below` ·
  Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath** — ready, and cue **A** is dark: rung 5 is
     `avenging_wrath,if=cooldown.divine_toll.remains<=10`, Divine Toll is *ready*, so the band's
     `beyond = 10` on Divine Toll's cooldown finds nothing to hold → **press.**
  2. Everything to the right is read only if the eye goes looking. Divine Toll is up, Shield of
     the Righteous is already blue-tinted by the client at zero HP, and none of that has to be
     interpreted to find the press.
- **Eye-direction.** ⚠ **The opener is free here, and it is free for a reason worth naming.** Cue
  A's sense is `beyond`, not `within`, so a *ready* Divine Toll releases the hold rather than
  applying it — the one window rung 5 fires in is exactly the one where the badge is dark.
  Getting that sense backwards would hold Wings in its only correct opener and light it for the
  rest of the fight. Retribution had to promote its opener because its rung-1 press sat seventh
  from the left; Protection's sits first.
- **Density.** No budgeted hold before the press. `starved` is not budgeted — it restates the
  tint Blizzard already put on the icon.
- **Cue set.** Starved (C) → **have**. Shining Light hold (G) → **have**, on the last entry, where
  it will sit for almost the whole fight. Divine Toll hold (A) → correctly **dark**.

### PROT-2 · Wings up — Divine Toll follows it in

- **State.** One global later. Avenging Wrath is on cooldown and **its buff is up**; Divine Toll
  is ready; **0 HP**; row 4 still Holy Bulwark and ready.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `press` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Holy Bulwark `hold-sealed` ·
  Avenger's Shield `below` · Consecration `cd` · Judgment `below` · Blessed Hammer `below` ·
  Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath** — swiped → skip.
  2. **Divine Toll** — ready, and it wears nothing: cue **B** is withheld by the talent gate
     **H** on this Righteous Protector build → **press.** Rung 7's first disjunct,
     `buff.avenging_wrath.up`.
- **Eye-direction.** ⚠ **The press is right and the reason cap has for it is nothing at all**, and
  that is worth seeing once. Rung 7's first disjunct is Avenging Wrath's *buff*, which lives on a
  **Category-3 (TrackedBar)** row (set 637, OrderIndex 27) whose alert edges are unmeasured, so
  cap does not read it; cue B expresses only the second disjunct, and the gate withholds even that
  here. Position 2 happens to be correct in this state. **PROT-2 is the good half of
  `catalog.md`'s first defeat** — the state where the same silence is wrong is the first entry
  under *The state this walk does not contain*.
  ⚠ Holy Bulwark is already held: cue **D**'s `beyond = 5` on Avenging Wrath's cooldown is
  satisfied the instant Wings is pressed, which is rung 14 read as a hold and correct — inside the
  window the Bulwark is not what the window is for.
- **Density.** No budgeted hold before the press.
- **Cue set.** Bank the Bulwark (D) → **sealed**, and irrelevant to the press. The talent gate (H)
  → **withholding**, harmlessly. Starved (C) → **have**.

### PROT-3 · Inside the window, five Holy Power — the spender leads by position alone

- **State.** Two globals later. Wings is up, Divine Toll is spent and swiped, its Holy Power dump
  has taken the player to **5 HP**. Row 4 is Holy Bulwark, ready. No Vanguard.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `cd` · Shield of the Righteous `press` ·
  Holy Bulwark `hold-sealed` · Avenger's Shield `below` · Consecration `cd` · Judgment `below` ·
  Blessed Hammer `below` · Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath / Divine Toll** — swiped → skip.
  2. **Shield of the Righteous** — affordable, so cue **C** is dark, and nothing else is authored
     on the row → **press.** Rung 9, which on Lightsmith is **unconditional**: every term in its
     APL condition is Templar's, so the first disjunct is trivially true.
- **Eye-direction.** ⚠ **This is the catalog's central bet and the scenario that shows it
  reading.** Holy Power is *readable* and goes *unread*: the 12.1 Protection list carries no
  `holy_power` term anywhere, so the catalog declares no `power` field, authors no `resource`
  term and spends no `overcap`, and the spender is placed by **position** instead. The badge that
  fires here is the absence of one. A reader coming from Retribution — same class, same resource,
  a whole design built on it — should read this state before assuming the two are the same
  problem.
- **Density.** No budgeted hold before the press.
- **Cue set.** Starved (C) → correctly **dark**, which is the whole content of the state. Bank the
  Bulwark (D) → **sealed**, past the press.

### PROT-4 · Sacred Weapon armed — the identity is the whole cue

- **State.** Mid-fight. Avenging Wrath ~40 s out, Divine Toll swiped, **2 HP**, and row 4 is
  displaying **Sacred Weapon** with no Sacred Weapon buff on the player. Row 7 base. DG at 2
  stacks. No Vanguard.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `cd` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Sacred Weapon `press` ·
  Avenger's Shield `below` · Consecration `below` · Judgment `below` · Blessed Hammer `below` ·
  Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath / Divine Toll** — swiped → skip.
  2. **Shield of the Righteous** — `starved` at two HP against a cost of three → skip.
  3. **Sacred Weapon** — the row is transformed, so cue **D**'s `identity(holy_armaments) == base`
     gate is false and the hold is dark → **press.** Rung 10, which sits above everything from
     rung 13 down.
- **Eye-direction.** ⚠ **`next_armament` reads like sim-internal state and is in fact the only
  free fact on this row.** Sacred Weapon `432472` has zero `CooldownSetSpell` rows anywhere in the
  file, so the only route by which the Cooldown Manager can show it is an override on the Holy
  Bulwark row — which means "which armament is next" is simply *which spell row 4 is displaying*,
  and R7 reads it with no new vocabulary. **The identity gate is load-bearing in both directions**:
  without it the Bulwark's bank hold would sit on the Sacred Weapon life, where the correct press
  is now.
  ⚠ The **direction** of that identity — which spell is `base` and which is `transformed` — is
  Tier-1 by exhaustive absence about *whether*, and marked about *which way round*. If it reads
  the other way this scenario and PROT-5 swap their badges, which is why the catalog carries an
  `@verify-ingame` on it rather than a footnote.
- **Density.** No budgeted hold before the press.
- **Cue set.** Starved (C) → **have**. Bank the Bulwark (D) → correctly **dark**, on the identity
  gate. The V16 band on Avenger's Shield → **armed and silent** at two stacks, drawing nothing.

### PROT-5 · Holy Bulwark armed, Wings far — the bank hold, and the count is silent

- **State.** As PROT-4, but row 4 is displaying **Holy Bulwark** and is ready. Avenging Wrath
  ~40 s out, **2 HP**, DG at **2 stacks**, row 7 base, no Vanguard, Avenger's Shield ready.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `cd` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Holy Bulwark `hold-sealed` ·
  Avenger's Shield `press` · Consecration `below` · Judgment `below` · Blessed Hammer `below` ·
  Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath / Divine Toll** — swiped → skip.
  2. **Shield of the Righteous** — `starved` → skip.
  3. **Holy Bulwark** — ready and affordable, and `blocked` lights from `ha_banks_bulwark`: the
     row is in its base life and Avenging Wrath is more than five seconds away, so rung 14's
     `cooldown.avenging_wrath.remains<5` is false and this is not the Bulwark's moment → skip.
  4. **Avenger's Shield** — both of its treatments are dark. Cue **E** needs row 7 transformed and
     it is not; the V16 band is armed but silent below five stacks → **press.** Rung 18.
- **Eye-direction.** ⚠ **This is the resting state of the middle of the row, and it is the
  scenario to read PROT-6 against**: same build, same position, same aura, one number different,
  and the row says the opposite thing. A treatment that only ever lights is a treatment nobody can
  read, so the silent half of the V16 table earns its place here rather than in the state where it
  draws.
  ⚠ Rung 17 — the Judgment second-charge dump — sits between rungs 16 and 18 and is **not
  authored** (`charged` is undeclarable on this row, *Defeats*, item 5), so if the second charge
  were two globals from full the APL would press Judgment here and the walk would still say
  Avenger's Shield.
- **Density.** One budgeted hold (Holy Bulwark) before the press. Well inside Part 0.5.
- **Cue set.** Bank the Bulwark (D) → **sealed**, and this is the state it exists for. Starved (C)
  → **have**. The V16 band → **armed, drawing nothing**.

### PROT-6 · Divine Guidance at five — the count rules out a row it does not belong to

- **State.** As PROT-5, but DG is at **five stacks**. Row 7 still base, no Vanguard, **2 HP**,
  Holy Bulwark armed and ready, Avenging Wrath ~40 s out, Consecration off cooldown.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `cd` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Holy Bulwark `hold-sealed` ·
  Avenger's Shield `ruled-sealed` {sealed: count-bands} · Consecration `press` · Judgment `below` ·
  Blessed Hammer `below` · Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath / Divine Toll** — swiped → skip.
  2. **Shield of the Righteous** — `starved` → skip.
  3. **Holy Bulwark** — cue **D**, as PROT-5 → skip.
  4. **Avenger's Shield** — cap draws nothing on it. What rules it out is the **client**: cap
     handed it a two-band table over Divine Guidance's application count, and at five the upper
     band draws the hatch and a negative mark out of the one FontString the count sink owns →
     skip. That is rung 15 outranking rung 18.
  5. **Consecration** — its own sealed complement is gated on row 7 being transformed and it is
     not, so nothing on the row draws → **press.** Rung 15,
     `consecration,if=buff.divine_guidance.stack>=5`.
- **Eye-direction.** ⚠ **First sealed display in any catalog that rules out a row the aura does
  not belong to.** Demonology's two count tables both sat on the row whose own press the count
  gated. Here the count is Divine Guidance's, the row wearing it is Avenger's Shield, and the
  statement is *"the row to your right outranks this one right now."* `Channel.Plan` has always
  bound `display.ability` independently of `entry.ability`, so the mechanism is old; using it to
  express a **relationship** is new, and it is `../spec.md` §3.1's readable-relationship rule
  reaching a fact cap may not read.
  ⚠ **The direction is V16 and not V17, and that is the whole of whether it is honest.** Drawn the
  other way it would say *"Avenger's Shield is ruled out until Divine Guidance is capped"*, which
  is false for the entire rest of the fight — PROT-5 is that state, and the row is clean there.
  ⚠ **The correction arrives from the other side.** Rung 15 promotes Consecration; a sealed
  display cannot promote, so the catalog demotes Avenger's Shield instead and lets elimination
  arrive at the same press. That asymmetry — *a sealed display may demote the row it is armed on
  and may never promote any row* — is the general statement, and it is also why the density
  problem above could not be solved with `priority`.
- **Density.** One budgeted hold (Holy Bulwark). The client-drawn elimination on Avenger's Shield
  is not budgeted, and PROT-13 is where that stops being an accounting detail.
- **Cue set.** Bank the Bulwark (D) → **sealed**. Starved (C) → **have**. The V16 band →
  **drawing**, and it is what makes this scenario expressible at all.

### PROT-7 · Glory of the Vanguard up — the same count, the opposite reading

- **State.** As PROT-6 — DG at **five stacks**, **2 HP**, Holy Bulwark armed and ready, Avenging
  Wrath ~40 s out, row 7 base — except that **Glory of the Vanguard is up**.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `cd` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Holy Bulwark `hold-sealed` ·
  Avenger's Shield `press` · Consecration `below` · Judgment `below` · Blessed Hammer `below` ·
  Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath / Divine Toll** — swiped → skip.
  2. **Shield of the Righteous** — `starved` → skip.
  3. **Holy Bulwark** — cue **D** → skip.
  4. **Avenger's Shield** — the V16 table is **not armed at all**: its `when` carries the readable
     `!aura(vanguard)`, and Vanguard is up. Cue **E** is dark for two independent reasons — row 7
     is base, and the same Vanguard term. Nothing draws → **press.** Rung 13's authored half,
     `avengers_shield,if=buff.vanguard.up`.
- **Eye-direction.** ⚠ **A readable gate on a sealed display, and this is the state that proves it
  is load-bearing.** Without `!aura(vanguard)` the hatch would rule out Avenger's Shield in the one
  state where rung 13 puts it *first* — the count is identical to PROT-6's and the correct reading
  is inverted. The `when`-beside-`display` shape is what makes that expressible.
  ⚠ **The other half of rung 13 is not authored and should not be.** `buff.avenging_wrath.up &
  apex.3` — `apex.3` is a sim-side Apex rank, absent from `talents.json`, `ability-inventory.tsv`
  and the whole repo. It is simulation state, not a player fact.
- **Density.** One budgeted hold (Holy Bulwark).
- **Cue set.** Bank the Bulwark (D) → **sealed**. Starved (C) → **have**. The V16 band →
  **withheld by its gate**, which is a third state distinct from *drawing* and from *silent*, and
  the only scenario in this walk where it appears.

### PROT-8 · Hammer of Wrath armed, Divine Guidance below five — the two tables disagree on purpose

- **State.** Execute range: **row 7 is displaying Hammer of Wrath** and it is off cooldown. DG at
  **three stacks**, **2 HP**, Avenging Wrath ~40 s out, Divine Toll swiped, Holy Bulwark on
  cooldown, Avenger's Shield ready, Consecration ready, no Vanguard.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `cd` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Holy Bulwark `cd` ·
  Avenger's Shield `hold-readable` · Consecration `ruled-sealed` {sealed: count-bands} ·
  Hammer of Wrath `press` · Blessed Hammer `below` · Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath … Divine Toll** — swiped → skip.
  2. **Shield of the Righteous** — `starved` → skip.
  3. **Holy Bulwark** — swiped → skip.
  4. **Avenger's Shield** — `blocked` from `as_awaits_hammer`. Every term is readable: row 7 reads
     `identity == transformed`, that row is off cooldown, Vanguard is down, and Avenger's Shield
     itself is ready. That is rung 16 outranking rung 18 → skip.
  5. **Consecration** — cap draws nothing on it; the **client** does. Under the readable gate
     *"row 7 is transformed and off cooldown"*, cap's complement table over the same Divine
     Guidance count draws its hatch and mark **below** five → skip. Rung 15 is false, so nothing
     puts Consecration above rung 16.
  6. **Hammer of Wrath** — **press.** Rung 16, unconditional, and it needs no cue of its own
     because the two rows to its left both wear one.
- **Eye-direction.** ⚠ **Both count tables are armed on the same aura and run in opposite
  directions, and this is the state that shows why that is not a contradiction.** Avenger's Shield
  is demoted **at** five; Consecration is demoted **below** five. Each is a claim about a different
  neighbour relationship, and only one of them can be true at a time — PROT-9 is the other half,
  same row, same count, one number different.
  ⚠ **The readable gate is what makes the complement honest, and this is the answer to Demonology's
  warning rather than an exception to it.** *"A complement is only correct where the low band is a
  REAL elimination"* — and below five stacks Consecration is **not** eliminated in general, because
  rung 19 presses it whenever the ground effect is down. What the gate does is narrow the display
  to the one state where the low band *is* an elimination: while Hammer of Wrath is armed and off
  cooldown, rung 16 outranks rung 19 and only rung 15 could put Consecration back on top. Outside
  that gate the client is never asked to paint anything. **A readable gate can turn a dishonest
  complement into an honest one.**
  ⚠ **The identity term is what makes "Hammer of Wrath is castable" a fact cap has** without ever
  asking about target health. The button's existence is the execute gate, and the Cooldown
  Manager's dial answers about the button currently *displayed* — so `ready(judgment)` here means
  *Hammer of Wrath is off cooldown*, which is exactly what rung 16 needs.
- **Density.** **One** budgeted hold (Avenger's Shield) plus one client-drawn elimination. ⚠ This
  is the state `catalog.md` → *Defeats*, item 7 believed cost three, and it costs one — the
  correction is argued in full under *Resolving the density problem*.
- **Cue set.** Hammer of Wrath yield (E) → **have**, on Avenger's Shield. Starved (C) → **have**.
  The V17 complement → **drawing**, on Consecration. The V16 table → **silent**, at three stacks.

### PROT-9 · Hammer of Wrath armed at five stacks — Consecration takes it back

- **State.** As PROT-8, but DG is at **five stacks**.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `cd` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Holy Bulwark `cd` ·
  Avenger's Shield `hold-readable` {sealed: count-bands} · Consecration `press` ·
  Hammer of Wrath `below` · Blessed Hammer `below` · Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath … Holy Bulwark** — swiped, except Shield of the Righteous, which is
     `starved` at two HP → skip.
  2. **Avenger's Shield** — ruled out **twice over**, and the two statements agree. `blocked` from
     `as_awaits_hammer` (row 7 is transformed and off cooldown, Vanguard down), and the client's
     V16 upper band drawing at five stacks. Rungs 15 and 16 both outrank rung 18 → skip.
  3. **Consecration** — the complement emits nothing at five and both of its marks clear →
     **press.** Rung 15.
- **Eye-direction.** ⚠ **The one state where the authored order is wrong and the sealed count has
  to correct it.** Position 6 encodes rung 19 — the common case, correctly below Avenger's Shield
  18 and above Judgment 22 — and rung 15's promotion of Consecration above rungs 16, 17 and 18 is
  what the count restores. It restores it by demoting the two rows to Consecration's left, one with
  a badge and one with a band, because **a sealed display cannot promote**.
  ⚠ **A badge and a band land on the same corner of the same icon here**, which no other scenario
  in this walk does. Whether that reads as one statement or as a mess is a question for the eye,
  not for this document; it is the Protection analogue of Demonology's DEM-8 and it is in the walk
  on purpose.
- **Density.** One budgeted hold (Avenger's Shield) before the press.
- **Cue set.** Hammer of Wrath yield (E) → **have**. Starved (C) → **have**. The V16 band →
  **drawing**. The V17 complement → **silent**, at five, which is the state it is in when
  Consecration is the press.

### PROT-10 · Blessed Assurance up — the empowered hammer, expressed as a demotion

- **State.** The **other half of the hero choice node**: Blessed Assurance talented, so Divine
  Guidance does not exist on this build and neither count table is ever armed. **Blessed Assurance
  is up**, row 7 is in its **base** life (target above execute range), **2 HP**, Avenging Wrath
  and Divine Toll swiped, Holy Bulwark swiped, Avenger's Shield swiped, Consecration swiped.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `cd` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Holy Bulwark `cd` ·
  Avenger's Shield `cd` · Consecration `cd` · Judgment `hold-readable` · Blessed Hammer `press` ·
  Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath … Consecration** — swiped, except Shield of the Righteous, which is
     `starved` → skip.
  2. **Judgment** — `blocked` from `judgment_awaits_assurance`: Blessed Assurance is up, the
     talent is taken, and row 7 is in its base life. That is rungs 20 and 21 outranking rung 22 →
     skip.
  3. **Blessed Hammer** — **press.** Rung 21.
- **Eye-direction.** ⚠ **The promotion is written on the row that has to move, not on the press.**
  Blessed Assurance makes the hammer better; it does not make it a different *kind* of button, and
  a rank change within one kind is what a left-to-right scan already carries. Badging Blessed
  Hammer would be a promotion this catalog does not spend, and it would then have to be true
  against everything to its left.
  ⚠ **The identity term on cue F is not decoration.** Rung 16 puts Hammer of Wrath above both
  hammer rungs, so the yield has to vanish while row 7 is transformed — otherwise the row that
  earns cue E on two neighbours in PROT-8 would stand *itself* down.
  ⚠ **A reader on the other side of the spec choice node at 3,19 reads this scenario with `Hammer
  of the Righteous` in position 8** and rung 20 instead of 21. The two are the same entry; the APL
  never names Crusader Strike at all, and the transform is permanent, which is why row 8 declares
  no band on `identity`.
- **Density.** One budgeted hold (Judgment) before the press.
- **Cue set.** Empowered-hammer yield (F) → **have**. Starved (C) → **have**. Both count tables →
  **structurally absent on this build**, which is what PROT-13 turns on.

### PROT-11 · Shining Light free — Word of Glory, and the badge going out

- **State.** Late in a pull. **Shining Light is up**, **2 HP**, and everything from row 1 to row 8
  is swiped — Blessed Hammer's charges are both down. Row 7 base.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `cd` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Holy Bulwark `cd` ·
  Avenger's Shield `cd` · Consecration `cd` · Judgment `cd` · Blessed Hammer `cd` ·
  Word of Glory `press`
- **Walk.**
  1. **Avenging Wrath … Blessed Hammer** — swiped, except Shield of the Righteous, which is
     `starved` at two HP → skip.
  2. **Word of Glory** — `wog_awaits_shining_light` is `!aura(shining_light)` and Shining Light is
     up, so the badge is out → **press.** Rung 28,
     `word_of_glory,if=buff.shining_light_free.up`.
- **Eye-direction.** ⚠ **Cue G is the load-bearing one in this catalog and it is on in every other
  state in this walk.** Rung 28 is Word of Glory's *only* rung: without the proc the button has no
  place in the damage priority at all, so an unbadged position 9 would stop the walk every time
  the rest of the row went dark. The signal is the badge going **out**.
  ⚠ **It is a pure negation, and that is where "unknown never becomes confidence" bites.** A player
  who never enabled the Shining Light tracked-buff row makes `aura(shining_light)` refuse, and a
  refusal withholds rather than asserting the opposite — so Word of Glory reads clean and the walk
  stops here in states the APL never presses it. That is a correct failure direction (the row is
  reached, not held) and it is why the marker is written as a negation rather than as a hold on the
  positive.
  ⚠ **No `starved` on this row, deliberately.** Word of Glory costs three HP as itself and nothing
  under Shining Light, but cue G already holds it in every state where affordability could matter,
  and a second badge on the last entry would say the same thing twice.
- **Density.** No budgeted hold before the press.
- **Cue set.** Shining Light hold (G) → correctly **dark**, the only scenario in this walk where
  it is. Starved (C) → **have**.

### PROT-12 · Plain filler — position 7 is rung 22, not rung 16

- **State.** Mid-fight, target above execute range so row 7 is in its **base** life and ready.
  **2 HP**; Avenging Wrath, Divine Toll, Holy Bulwark, Avenger's Shield and Consecration all
  swiped. Divine Guidance build, so Blessed Assurance never exists.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `cd` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Holy Bulwark `cd` ·
  Avenger's Shield `cd` · Consecration `cd` · Judgment `press` · Blessed Hammer `below` ·
  Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath … Consecration** — swiped, except Shield of the Righteous, which is
     `starved` → skip.
  2. **Judgment** — cue **F** needs the Blessed Assurance aura, which cannot exist on this build,
     and the `talent(blessed_assurance)` gate withholds it a second time. Nothing draws →
     **press.** Rung 22.
- **Eye-direction.** ⚠ **This is the state position 7 was chosen for, and the choice was between
  two wrongs.** Row 7's rungs are 16, 17 and 22, and the alternative — placing the row above
  Avenger's Shield to encode rung 16 — would badge this state instead. Rung 22 is the common one
  and rung 16 is the rare one, so the catalog encodes the common one and carries the rare one on
  cue **E**, worn by the *neighbours*. Part 0.5's model is to badge the state the player is in less
  often, and PROT-8 is the price of that decision paid in full.
  ⚠ **The double gate on cue F is belt-and-braces in the safe direction.** On this build the aura
  latch would withhold on its own; the talent gate makes the *reason* legible and matches how the
  sealed tables are gated on the other half of the same node.
- **Density.** No budgeted hold before the press.
- **Cue set.** Empowered-hammer yield (F) → correctly **dark**, twice over. Starved (C) →
  **have**.

### PROT-13 · The three-hold state, and the marker this walk deletes

- **State.** A **Blessed Assurance build** in execute range — so Divine Guidance does not exist,
  and neither count table has a subject. Row 7 is displaying **Hammer of Wrath** and is off
  cooldown; row 4 is displaying **Holy Bulwark**, ready, with Avenging Wrath ~40 s away; Avenger's
  Shield is ready; Consecration is off cooldown; **2 HP**; Divine Toll swiped; no Vanguard.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `cd` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Holy Bulwark `hold-sealed` ·
  Avenger's Shield `hold-readable` · Consecration `press` · Hammer of Wrath `below` ·
  Blessed Hammer `below` · Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath / Divine Toll** — swiped → skip.
  2. **Shield of the Righteous** — `starved` → skip.
  3. **Holy Bulwark** — cue **D**: base life, Avenging Wrath beyond five seconds → skip.
  4. **Avenger's Shield** — cue **E**: row 7 transformed and off cooldown, Vanguard down → skip.
  5. **Consecration** — **press.** ⚠ **And the APL presses Hammer of Wrath here.** Consecration's
     sealed complement has no subject on this build, and `cons_no_guidance` — the readable marker
     that used to cover exactly this case — **is deleted by this walk**. The press is rung 19 with
     the ground effect down, rung 29 with it up, where the APL is at rung 16.
- **Eye-direction.** ⚠ **This is the state `catalog.md` deferred to this document, and the trade is
  explicit: one rung of throughput, bought with one badge.** As authored the row stood **three**
  budgeted holds before the press — Holy Bulwark, Avenger's Shield, Consecration — against Part
  0.5's budget of two, and Part 0.5's prescribed remedy, promoting the press with `priority`, is
  unavailable: pass 1 is pre-emptive, so a promotion is a claim against *every* row to its left,
  and Consecration outranks Hammer of Wrath whenever Divine Guidance is capped. Gating the
  promotion on that would mean cap comparing a sealed count, which is §3.6 itself. **So a hold had
  to go, and `cons_no_guidance` is the one that earns its place least** — the full argument is
  under *Resolving the density problem*, and the short form is that it is the only marker in the
  catalog whose entire job is to convert a free client-drawn elimination into a budgeted badge, and
  it only ever draws on the build where that elimination has no subject.
  ⚠ **On the Divine Guidance build this same state costs nothing**, because the elimination arrives
  as `ruled-sealed` instead: that is PROT-8, two rows further right and one budgeted hold cheaper.
  The deletion is therefore paid for entirely by the half of the choice node the catalog's sealed
  machinery does not serve.
  ⚠ **The loss is one global, not a cast.** Hammer of Wrath is a seven-and-a-half-second button;
  the moment Consecration goes on cooldown the walk reaches row 7 again.
- **Density.** **Exactly two** budgeted holds before the press, which is Part 0.5's budget. Before
  the deletion it was three.
- **Cue set.** Bank the Bulwark (D) → **sealed**. Hammer of Wrath yield (E) → **have**, on
  Avenger's Shield. Starved (C) → **have**. `cons_no_guidance` → **deleted**. Both count tables →
  **no subject on this build**.

### PROT-14 · No Righteous Protector — the only build cue B exists on

- **State.** The rare build: **Righteous Protector not talented**. Avenging Wrath is ~20 s from
  ready and its buff is down; **Divine Toll is ready**; **2 HP**; row 4 is Holy Bulwark, ready;
  Avenger's Shield ready; DG at two stacks; row 7 base; no Vanguard.
- **CDM row.** Avenging Wrath `cd` · Divine Toll `hold-sealed` ·
  Shield of the Righteous `starved` {client: not-enough-power} · Holy Bulwark `hold-sealed` ·
  Avenger's Shield `press` · Consecration `below` · Judgment `below` · Blessed Hammer `below` ·
  Word of Glory `hold-readable`
- **Walk.**
  1. **Avenging Wrath** — swiped → skip.
  2. **Divine Toll** — ready, and `blocked` lights from `dt_awaits_wrath`: the talent gate **H**
     lets the marker through on this build, and the `within = 30` band on Avenging Wrath's
     cooldown is satisfied at twenty seconds. That is the complement of rung 7's
     `cooldown.avenging_wrath.remains>30` — the Toll belongs inside the window → skip.
  3. **Shield of the Righteous** — `starved` → skip.
  4. **Holy Bulwark** — cue **D** → skip.
  5. **Avenger's Shield** — nothing draws → **press.** Rung 18.
- **Eye-direction.** ⚠ **This is the whole reach of cue B, and it is a build almost nobody
  plays.** Righteous Protector halves Avenging Wrath's cooldown, which both deletes rung 7's second
  disjunct from the APL and would leave a thirty-second band covering half a sixty-second cycle —
  a rule the priority does not contain. So gate **H** withholds the marker everywhere else, and on
  the standard build Divine Toll wears nothing at all. That hole is the first entry under *The
  state this walk does not contain*.
  ⚠ **Cues A and B can never both draw, and neither can A and D.** A requires Divine Toll to have
  at least ten seconds left; B requires Divine Toll to be *ready*. A requires Avenging Wrath to be
  ready — remaining zero — and D requires it to be more than five seconds out. So the COOLDOWN
  lane's three sealed bands can contribute **at most two** budgeted holds to any row, which is this
  scenario, and it is the structural reason the lane never overflows the budget on its own.
- **Density.** **Exactly two** budgeted holds (Divine Toll, Holy Bulwark) before the press. At
  budget, not over.
- **Cue set.** Avenging Wrath hold (B) → **sealed**, and this is its only appearance. The talent
  gate (H) → correctly **not withholding**. Bank the Bulwark (D) → **sealed**. Starved (C) →
  **have**. Divine Toll hold (A) → structurally **dark**.

---

## The state this walk does not contain

⚠ **This is the finding, not an omission.** `capart check`'s elimination gate requires the
leftmost un-ruled-out entry to be the press. In each state below it is not, and **cap draws
nothing that would rule the wrong row out** — so writing it as a scenario would mean asserting a
reading the player cannot perform. Each is argued in full at `catalog.md` → *Defeats*.

1. **Divine Toll ready, Avenging Wrath down, on a Righteous Protector build.** Rung 7 reduces on
   that build to `buff.avenging_wrath.up`, which is false, so the APL skips the Toll — and cue B
   is withheld by gate H, so Divine Toll wears nothing and the walk stops on it at **position 2**.
   This is the largest hole in the catalog: a stop at position 2 is a stop almost immediately.
   *Reopened by one measurement* — does a **Category-3 (TrackedBar)** row raise the `aura` latch's
   `OnAuraApplied` / `OnAuraRemoved` alert edges? Avenging Wrath's buff is one (set 637, ord 27).
   If it does, `aura(avenging_wrath)` becomes a readable boolean, cue B is replaced by a marker
   correct on **both** builds, and gate H is deleted with it. `catalog.md` → *Defeats*, item 1.
2. **Consecration ready with its ground effect still ticking.** Rungs 19 and 24 are false, so the
   APL presses the hammer, Judgment or Word of Glory and only reaches Consecration at rung 29; cap
   draws nothing and position 6 takes the press. *Reopened by the same single measurement* —
   Consecration's duration is the Category-3 row at ord 24. **Both defeats close together or
   neither does**, which is the argument for doing it. ⚠ This one now also bounds PROT-13's cost:
   with the ground effect up, the deletion's one-rung loss is a rung-29 press instead of a rung-19
   one. `catalog.md` → *Defeats*, item 2.
3. **A Sacred Weapon buff with eighteen seconds left.** Rung 10 fires on
   `buff.sacred_weapon.remains<6 | !buff.sacred_weapon.up`; with a healthy buff the APL skips row
   4 and cap cannot tell that row from PROT-4's. The walk stops at **position 4** in a state the
   APL steps over. *Reopened by* an **aura-remaining band** — the S-form nobody has written, whose
   step curve S4 already applies to a cooldown — plus one census read for whether Sacred Weapon's
   buff holds a Category-2 row. **Retribution wants the same S-form**, so it now has two consumers.
   `catalog.md` → *Defeats*, item 3.
4. **Holy Bulwark at two charges with Wings a minute away**, and **Judgment's second charge two
   globals from full.** Rungs 23 and 17 are pure charge facts and `charged` is undeclarable here —
   no Tier-1 charge count exists for Holy Armaments at all, and Judgment's is talent-conditional
   while `charged` has no conditional form. In the first, cue D holds a press the APL makes and a
   charge may be lost, which is the worst failure direction in the catalog. *Reopened by* a
   measured charge count (item 4) and a talent-conditional `charged` (item 5) — **a measurement
   and a mechanism, which do not close together.** ⚠ The measurement would also give this catalog
   its first positive cue: `capped` on row 4 is loss in progress with no negative phrasing, and a
   scenario wearing a positive cue is judged by pass 1 and leaves the density budget entirely —
   so the same measurement that closes item 4 would also have offered a second route out of
   PROT-13. `catalog.md` → *Defeats*, items 4 and 5.
5. **A third trio that survives the deletion, on a doubly-rare build.** On a **non-Righteous
   Protector, Blessed Assurance** build with Avenger's Shield *and* Consecration both swiped, cues
   **B**, **D** and **F** stand three budgeted holds before Blessed Hammer. It is not in the walk
   because every term of it is a conjunction of rarities — the build gate H exists to withhold
   from, the half of the hero node the sealed tables cannot serve, and two swiped ROTATION rows at
   once — and because deleting a second marker to cover it would cost more than the state is
   worth. ⚠ **If a flight finds it, cue B is the candidate**, not cue D: B already exists only on
   that build, and item 1's single measurement would replace it outright.

**It is not a client limit in any of the five.** Four are measurements or a written S-form, and
the fifth is a design choice this walk took deliberately. That is a set of named shapes, which is
a different and much better thing than "cap cannot do this".

---

## What this walk falsified

⚠ **This is the point of the document, and both items are `catalog.md`'s to carry — this file does
not edit it.**

1. **Documented misordering 3 is wrong, in its second half.** The catalog states that on a Blessed
   Assurance build `cons_no_guidance` *"fires unconditionally — so on that build Consecration
   yields to Hammer of Wrath in a state where nothing outranks it"*, and calls it a one-rung
   throughput loss. It is not a loss. Rung 15 is `consecration,if=buff.divine_guidance.stack>=5`,
   and without the Divine Guidance talent that stack count can never reach five, so **rung 15 is
   dead on a Blessed Assurance build and Hammer of Wrath's rung 16 outranks every Consecration
   rung on it** (19, 24 and 29). The marker was **correct** on that build — and it is correct at
   zero stacks on a Divine Guidance build for the same reason. It is being deleted for *density*,
   which is a different justification and a reversible one.
2. **Defeat 7 counts three holds in a state that costs one.** Its scenario — Shield of the
   Righteous unaffordable, cue D, cue E on Avenger's Shield, cue E on Consecration, Divine
   Guidance *below five* — has Consecration eliminated by `cons_awaits_hammer`'s low band, which
   is `ruled-sealed`: client-drawn, cue-less and unbudgeted. Cue D is on Holy Bulwark, which in
   that state is either ready (one hold) or swiped (none), and `starved` is unbudgeted. **That
   state is PROT-8 and it stands at one budgeted hold.** The overflow is real but it lives one
   build over, where the DG aura is absent and the readable marker does the eliminating — PROT-13.
   ⚠ And Defeat 7 names only the cue-**D** trio; **there is a second**,
   `{A, as_awaits_hammer, cons_no_guidance}`, in which Avenging Wrath's own hold takes cue D's
   place. That is why the deletion is `cons_no_guidance` rather than cue D: only the common term
   fixes both.

**Everything else in the catalog survived the walk.** All nine entries, the authored order, all
seven cues plus gate H, both `sealed-count-bands` tables and all three `sealed-cooldown-range`
bands are exercised above and none of them read wrong in the state they were written for. Two
mutual exclusions the catalog does not state fell out of the walk and are worth keeping: **cues A
and B can never both draw** (A needs Divine Toll on cooldown, B needs it ready), and **cues A and
D can never both draw** (A needs Avenging Wrath ready, D needs it beyond five seconds), which
together cap the COOLDOWN lane's contribution to the density budget at two.

**What the walk did not have to explain.** No state above required cap to know a target count, a
target's health, an aura duration, a cooldown's remaining *value*, an aura stack count, or which
armament the game considers next beyond the icon it is drawing. Every skip is a readable Lua term,
one sealed band on a cooldown (A, B, D), or a band table the client evaluated against a count cap
never received (PROT-6, PROT-8, PROT-9).

**Fourteen states, no promotion, and one marker deleted to keep it that way.** The catalog's own
argument for spending no positive cue turned on a state it could not evaluate; the walk found that
state, found a second one the catalog had not seen, and answered both by removing vocabulary
rather than adding it — which is the shelf's own test for a design that is getting simpler.
