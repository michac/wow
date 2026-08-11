# Combat Assist Plus — open discussion

**What this file is for:** topics raised and **not yet decided**. A discussion item is not
agreed work (that's `backlog.md`), not a product decision (that's `spec.md`), and not a record
of what we did (that's `notes.md`). It exists because those three have no home for *"here is a
question that would change the design, and here is the case on both sides"* — which previously
meant such questions got decided in passing, or lost.

**Lifecycle.** An item leaves this file when it is decided: the decision to `spec.md` if it
changes what cap should do, to `backlog.md` if it becomes work, and the reasoning to
`notes.md`. Strike it here with the date and where it went. **Nothing here ages, and nothing
here is a commitment.** Each item is written to be read **cold**.

---

## Open

### D17 — The stock proc glow was NOT suppressed. Is the dim not running, or not reaching a pixel?

**Raised:** 2026-08-10, from the first flight of the drawn surfaces. Observed: *"the blizzard
proc is not suppressed. When Demonbolt procs its glow blows the others out of the water, looks
super high priority. Same with IB."*

**Why it matters more than "the dim is too shallow".** A proc'd icon reading as the loudest
thing on screen is the failure §3.2 exists to fix — an unsuppressed glow overrides the tier
signal on exactly the ability cap has an opinion about. Infernal Bolt is E10's transform, so a
second row is affected and it is not a Demonbolt quirk.

**Four candidate causes, in rough order of likelihood:** (1) nothing was hooked — `Glow.Arm`
silently refuses a frame whose `RefreshOverlayGlow` is not a function; (2) hooked but `live`
was false, so every callback returned early; (3) hooked and live, but `SpellActivationAlert`
is the wrong field on a CDM item — the recipe came from action-bar-shaped frames; (4) the
alpha landed and the proc animation overrides it, i.e. the premise that the alert *frame*'s
alpha multiplies without fighting the animation is wrong here.

📊 **Measured: two causes are eliminated and two survive.** The flown pull read `glow:14/live`
for all but one of its lines — the frames were hooked and the dim was armed — so **causes 1
and 2 are dead**. Causes 3 and 4 both stand.

⚠ **And `glow:` cannot separate them, by construction.** The hook is installed when
`type(frame.RefreshOverlayGlow) == "function"`, and that is the whole of what the counter
counts. `dim()` separately requires `type(frame.SpellActivationAlert) == "table"`, and it
wraps the setter in a `pcall` whose result is discarded — so a wrong field name on a CDM item
(cause 3) and a setter that runs and lands on nothing (cause 4) **both report `live`**.

**This is the `nosize:` defect a second time**: a counter reporting the step before the one
that can fail, so a broken pull prints healthy. ⚠ **What would decide it is therefore not
another flight** — it is a counter on the dim itself, saying whether the alert field resolved
and whether the setter ran. `backlog.md` carries it. A ClientLab probe of a live CDM item's
field names is the follow-on if that counter says the field is absent.

**⚠ This blocks D10**, whose comparison is not the one available while the stock glow is at
full strength.

### D16 — Tyrant should be MEDIUM with two markers, not promoted to HIGH. What draws a marker cap computes itself?

**Raised:** 2026-08-10, from the first flight. Observed: *"tyrant was promoted to HIGH when
dreadstalkers was cast. It's supposed to always be MED when off cooldown, and get a cue for
dreadstalkers and a second cue if the grimoire is out. Just coloured dots or plus signs."*

**The tier half is decided and is a catalog edit** — E1 collapses to one MEDIUM band on
`ready(this)` and the staging information moves to markers. It is filed in `backlog.md`.

**The open question is what a marker like this even is.** §3.0 defines a **cue** as decided by
cap *and* the client. But *"Dreadstalkers are out"* is `not ready(E2)`, a **gate** — cap can read
it and branch on it outright, so there is nothing sealed for the client to decide.

- **(a) Let a marker be driven by a gate alone.** Simplest, and matches what was asked for. But
  it widens §3.0's cue definition, and the gate/channel split is the one line §1 principle (a)
  says is worth enforcing in code.
- **(b) Keep it a cue and find a channel.** `active(x)` → **pip** is already in §3.5's table
  and is one of the forms with no marker built. Closest fit by name — but what `active` would
  name here is a *pet*, and whether the client exposes a pet's existence through any sealed
  sink is unmeasured.
- **(c) Say it with bands.** Three tiers cannot carry two independent booleans. Recorded so
  nobody re-proposes it.

**What would decide it.** (a) versus (b) is a spec question, not a measurement: does cap's
vocabulary admit a marker with no client half? ⚠ A second question rides along — the rule that
fixed the number of marker slots was struck, so a third is no longer forbidden but nothing says
where it goes, and two dots meaning different things must be told apart (**D8**).

### D15 — A row whose override is a DIFFERENT ability reads as ready. Whose problem is that?

**Raised:** 2026-08-10, from the first flight. Observed: *"the grimoire:imp button transforms
into a Consume Magic when on cooldown … cap highlights it basically the entire time as a
high-priority ability, even when the real ability is on cooldown."*

**Why it happens.** E3's bands are `ready(this)` → MEDIUM and `ready(this) and ready(E1)` →
HIGH. When Grimoire goes on cooldown the row's *identity* flips to Consume Magic — a real,
castable, off-cooldown utility — so `ready(this)` reads **true** for the whole cooldown. cap is
not misreading anything; the catalog never said which identity it meant.

**The desired behaviour is decided: that state is *none*.** What is open is where the fix
belongs, and the two answers generalise very differently.

- **(a) Catalog-level.** `identity(this, …)` is a gate, is measured readable in combat, and E6
  Ruination is built on exactly that channel. Four lines in E3 — cheap, precise, the mechanism
  the vocabulary was designed for. But per-entry: every future transforming row has to
  remember, and forgetting is silent, because the entry lights permanently and looks correct.
- **(b) Engine-level.** State the invariant once — *an entry whose bound row is currently
  displaying a different ability has no opinion* — and `Tier` refuses it outright, making the
  failure structurally impossible. Costs a new normative rule about what a tier *is*. ⚠ It also
  collides with the transform entries that exist on purpose: E6 and E10 declare one entry per
  identity and *want* to fire on the overridden one, so the rule must distinguish "transformed
  into something another entry claims" from "transformed into something nobody declared" — and
  getting that boundary wrong silences Ruination.

**What would decide it.** They are not exclusive: (a) unblocks play immediately and does not
foreclose (b). ⚠ Count first — **how many other CDM rows on this spec transform into an
unrelated ability while on cooldown?** Nobody has looked, and "several" argues for (b).

📊 **Measured, and the player's report is exact: E3 was emphasised for 98 % of the pull** —
HIGH **74 %**, MEDIUM **24 %**, *none* 2 %, with a single unbroken stretch of **503.9 s** out
of a 700.7 s window. This is the **size** of the problem rather than an answer to it: the
desired behaviour was already decided, and the open half above — *where* the fix belongs — is
untouched by the measurement. ⚠ **What it does change is the urgency**: E3 is the largest
single contributor to the saturation D14 now rests on, so the *where* wants deciding sooner
than it did. The roster count asked for above is a different question and this capture does
not answer it.

### D14 — The tier glows read as candles. Is the fault brightness, pulse depth, or rate?

**Raised:** 2026-08-10, from the first flight. Observed: *"the tier glows are way too
'flickery' — looks like candles. Needs to be brighter across the board."*

📊 **Measured, and it moves the question upstream of everything below.** Across the flown pull,
two or more entries were HIGH **74.8 %** of the time against the M3b baseline's 16 %, something
was HIGH **87.4 %**, and five of the eight entries held a single tier **unbroken for 500–545 s**
of a 700.7 s window (E8 544.9 · E5 538.9 · E2 524.7 · E1 503.9 · E3 503.9). Nothing receded.
The screen was a near-static wall of lit rings whose only moving part was the pulse, on
everything, at once — **and that is what "too flickery" is describing**. The root is the
catalog's bands being satisfied near-permanently, which is upstream of every candidate below;
it also means *"needs to be brighter"* cannot be taken at face value, because a brighter ring
on a saturated screen is worse. ⚠ **This does not clear the candidates** — it says fixing them
alone cannot fix the complaint. `backlog.md` carries the band re-cut as the item above them.

**Both halves matter and they are not one complaint.** "Too flickery" is the **pulse**; "needs
to be brighter" is the **alpha**. A fix that only raises alpha leaves a bright candle. The tier
alphas *were* picked by a person on real spell art at true CDM size — **HIGH 1.00, MEDIUM 0.78,
LOW 0.50, each the top of its tier's graded range** (`spec.md` §3.1) — and the pulse **rate**
came from the lab (2.5 / 1.2 / 0.5 Hz). **The trough — 0.68 of the tier's alpha — was picked at
a desk**, and it decides how far a ring dips: the strongest suspect is the one thing nobody
looked at. ⚠ Do not read the *ungraded midpoints* (0.91 / 0.63 / 0.43) as the picked numbers —
they are derived from the bands, and an entry only sits at one when it has no grade.

**Five candidate faults, and they call for different fixes:**

- **Trough too deep.** At 0.68 a HIGH ring swings 0.68 → 1.00 every 0.4 s — a 32 % luminance
  modulation at 2.5 Hz, close to the description. Raising the floor keeps the motion.
- **Rate too fast.** 2.5 Hz is at the top of the band the eye reads as flicker rather than
  breathing. ⚠ Rate is load-bearing for something else — it is what separates HIGH from MEDIUM
  where the pulse lets their rendered alphas overlap. Slowing everything flattens that.
- **Base alpha too low against real icon art.** Possible for MEDIUM and LOW; HIGH is already at
  1.00 and cannot go up, so a dim HIGH is the trough or the blend, not the alpha.
- **The `ADD` blend**, which blows out over a bright icon and vanishes over a dark one
  (`cue-treatments.md`) — candle-like guttering is what an additive glow does over mixed art.
  `BLEND` was the lab's alternative and was never compared on cap's own frames. Cheap to test.
- **A pulse that never completes a cycle.** `Overlay.lua` records that a re-arm **re-pays the
  animation start delay**, so a row whose treatment changes more often than its own delay never
  reaches a first pulse — LOW's worst case is ~1.98 s. A ring repeatedly restarting its fade-in
  and being re-armed before it arrives is an excellent candidate for *guttering*, and it is a
  different fault from all four above: it is not the trough, the rate or the blend, but how
  often the paint path runs. ⚠ It also interacts with `armPulse`'s open `--@unverified`.

**What would decide it.** Looking, with one variable moved at a time; the numbers all live in
one table (`Treatment.lua`'s `TIERS` and `PULSE`). ⚠ **The per-row phase offset may not be
quietly dropped.** It is a seizure-floor property: ~14 icons flashing *in sync* cross WCAG
2.3.1's general flash threshold and the same 14 offset never approach it. Raising the trough
helps; synchronising the rows to look tidier is off the table.

### D13 — A resting bar and an empty track are two numbers nobody has looked at. What are they?

**Raised:** 2026-08-10, by the fix pass on the bars, which found the first answer was an
analogy. **Neither has been judged on screen.**

**What is derived, and it is only an ordering.** §3.1's surviving ladder property is that the
ladder is *ordered* and *none* is its bottom rung. A bar has no ring, so the fill is the only
thing that can carry the LOW → *none* step; the resting fill therefore has to read **under
LOW's dimmest**, which on the shared slate hue reduces to an alpha strictly under LOW's dim end.
That much follows and no more. **Everything else is picked** — the value inside that bound
(`Treatment.BAR.rest.a`) and the empty track's colour and alpha, which have no argument behind
them at all. `spec.md` §3.4 states the property rather than the numbers for that reason.

**Why the bound is not the whole question.** Two failures sit either side of it. Too bright and
a resting bar reads as a dim LOW — *cap thinks this is filler* — which is the collision the
first cut walked into. Too dim and the bar reads as *empty*: the fill stops separating from the
track, and a countdown whose extent you cannot see is worse than no bar. Neither edge is
arithmetic; both are a look. ⚠ **Unreachable on Demonology, and that is not a defence** — no
entry on the roster bands LOW, but `Treatment.Fill` is the **shared engine** every future spec
draws through.

**What would decide it.** Looking, and nothing else. `B{}` says `armed`, which means cap handed
the client a duration object — it says nothing about a colour and no capture can.
`backlog.md` → *Judge the bars on screen* carries it beside the three legibility questions.
⚠ **Do not re-derive the number from another surface's constant** — a veil, a pulse trough, a
band width. That is the move this item exists because of.

### D12 — If the Wild Imp count saturates, is E8's positive cue lit nearly all the time?

**Raised:** 2026-08-10, by the argument that gave Implosion a §3.4 bar. **The two claims below
cannot both be right.**

**The collision.** `catalog.md` §4 gives Implosion a bar on the grounds that *once the rotation
is rolling you almost always have 6+ Wild Imps up, so the count is saturated and what gates the
press is the 15 s cooldown*. `catalog.md` **E8** says the opposite about the same count one
section earlier: its band stops at MEDIUM because a permanently-lit HIGH is *"the same failure
as a HIGH that never fires"*, while the cue is safe because *"the imp count crosses 6 in
bursts, so the HIGH-styled number arrives and leaves with the actual opportunity."*

**Why the bar claim does not settle it.** Both could be locally true — imps are generated in
bursts by Hand of Gul'dan and consumed by Implosion itself, so the two statements differ mainly
in how long the trough after an Implosion lasts. Neither was measured.

**What is at stake.** E8's cue is the whole of its HIGH — no band may test the count — so a cue
that never goes out means Implosion reads HIGH permanently, the one reading §3.1's ladder
cannot carry. The generic worry is `backlog.md`'s *Re-cut the catalog's bands so the tiers
recede*; this is one concrete instance of it.

📊 **Measured — cap's half is answered, and it saturates.** Time-weighted across the flown pull,
E8 was MEDIUM with the cue `armed` for **81.9 %**, MEDIUM with it `refused` for **2.8 %**, and
had **no tier at all for 15.3 %** — that last stretch emits no `C{}` cell, because an entry with
no tier offers nothing. The three account for the pull exactly.

**So the headline is not the whole-pull figure, which understates it by counting the time the
entry is correctly dark. Whenever E8 was lit at all — 84.7 % of the pull — cap offered the cue
for 96.7 % of that time.** The 15.3 % is precisely the stretch where Implosion is on cooldown,
which the gate precondition `ready(this)` correctly excludes. The precondition is therefore
doing the only job it can do, and **past it the cue discriminates essentially nothing**: it is
offered on virtually every moment the entry is up. On cap's side of the line the §4 claim is the
one the pull supports, not E8's.

⚠ **The 2.8 % `refused` is a read refusal on cap's side** — no live `auraInstanceID`, so there
was nothing to hand over. It is **not** the client declining to draw; the client's decision is
never visible here at all.

⚠ **The client's half is not answered, and no capture can ever answer it.** Whether the
**marker** appeared is decided from a stack count cap never learns, so neither figure above is a
statement about a marker: `armed` means *cap asked the quantiser*, and **96.7 % of E8's lit time
is how often cap asked**, not how often anything was drawn. The two halves can differ in either
direction, and the only oracle for the second is an eyeball on the Implosion icon through a
pull.

**What that leaves open.** Whether a permanently-offered cue is acceptable now depends on a
thing cap cannot instrument, so the choice is a design one. Candidate fixes, none argued: raise
`n` above 6, tighten the gate precondition, or accept a lit cue and change what Implosion's
HIGH means. ⚠ E8 also sat MEDIUM for 84.7 % of that pull, so it is one of the entries the band
re-cut in `backlog.md` has to look at either way.

### D11 — Do the tiers need **separated** emphasis ranges, or is an ordered ladder enough?

**Raised:** 2026-08-10, by the §3.1 cull, which removed the rule that answered this by
assertion. **The tiers have been seen** — that is what raised D14 — but **the specific LOW /
MEDIUM adjacency this item is about has not**, and on Demonology it cannot be.

⚠ **The struck rule, named only so the question is legible:** §3.1 used to require each tier to
own a non-overlapping brightness band, justified as *a grade never changes the tier* expressed
as arithmetic. That justification does not hold — *a grade never changes the tier* is a claim
about **computation**, true by construction, so the pixel claim was a second claim wearing the
first one's argument. What it cost while it stood: LOW's ring moved off the lab-measured 0.50 to
a ceiling nobody chose and nobody has seen, and the rule's own text conceded the screen does not
obey it anyway, since the pulse crosses the bands deliberately.

**The case for bringing separation back in some form:** two icons at the same emphasis carrying
different tiers is a real thing to worry about, and a graded LOW can now reach a dim MEDIUM.
**The case against:** it was never measured against anything — the lab compared each tier at
full strength against the others at full strength, and nobody has looked at a dim MEDIUM beside
a bright LOW. A rule narrowing every grade's range spends exactly the thing §1's second move is
for.

**What would decide it — and ⚠ NOT a Demonology flight.** The bands overlap; the catalog never
gets into the overlap.

| | Reachable extreme | Where |
| --- | --- | --- |
| brightest **LOW** | **0.3526** | E9 / E10 at their ungraded midpoint (`0.43 × 0.820`) |
| dimmest **MEDIUM** | **0.3989** | E7 at grade `0.4` (`0.60 × 0.665`) |

A gap of **0.046**, every step forced by the catalog rather than by the treatment table — E7's
MEDIUM band needs `shards ≤ 3` on a *falling* `resource` grade, pinning it at `≥ 0.4`; its LOW
band needs `shards ≥ 4` on the same grade, pinning a graded LOW at `≤ 0.2`. *(An exhaustive
sweep of every gate combination the catalog admits, affordability tied to the DB2 cost.)*
**Observing the real adjacency needs one of three things, none of them a pull:** an entry whose
LOW band is reachable while its grade is *high*; a second spec that has one; or a deliberate lab
mock putting LOW's bright end beside MEDIUM's dim end. Until then a null result from a flight is
not evidence either way. If they turn out indistinguishable the fix is a number — a lower MEDIUM
ceiling, a narrower grade range, or a hue not sharing a luma with the tier above — not a
restored invariant.

⚠ **One consequence is already handled and must not be re-derived.** A row two entries bind is
drawn in the **higher of the two tiers**; `Overlay` compares tier order first and emphasis only
inside one tier, so this question cannot reach that path whichever way it goes.

### D10 — cap's ring **is** Blizzard's proc-glow sheet. On screen, do they read as one thing or two?

**Raised:** 2026-08-10, by the measured restyle, which made a rule and a design collide in one
commit. **Nobody has seen the two side by side under a working suppression.**

**The collision.** §3.1's last surface rule was that cap does not reuse Blizzard's proc-glow
art, because an emphasis that looks like the stock glow makes the two indistinguishable. The
treatment a person picked in the lab draws **`UI-HUD-ActionBar-Proc-Loop-Flipbook`** — precisely
the sheet Blizzard's proc alert plays.

**The case for the pick.** The rule's *reason* is about the two emphases being
indistinguishable, and three things separate them: §3.2's suppression dims the stock glow, cap's
ring is drawn in a **tier hue** at a **tier alpha** where the stock glow is uniform gold at
full, and cap's **pulses** where the stock glow does not. A shared sheet is not a shared
emphasis. And it is a shipping client asset — no vendored library, art baked for this size.

**The case against.** A player who has spent years reading that ring shape as *Blizzard says
press this* is being asked to re-learn it as *cap says this much*, and a proc'd icon then
carries the same shape twice. A weaker version survives even if the strong one fails: the ring
may read as a *proc* rather than as an emphasis, which is a different failure.

**What the spec says today.** The rule was **narrowed to its root** — §1's move 2, which
requires only that the two be **distinguishable**. The code was not touched: the rule was the
thing that could not be argued from a principle, not the pick.

**What would decide it.** Sitting at a Demonic Core proc with the suppression **working** and
looking. ⚠ **Blocked on D17.** If they read as one thing the fix is cheap and inventoried:
`Treatment.RING.atlas` is one string, and `glow-palette.md`'s candidate run has ~15 shipping
alternatives with their grids declared.

### D9 — What can actually be retrieved from a **bar** cooldown item?

**Raised:** 2026-08-08, after a claim that cap could not know whether a summon's pets are out
turned out to rest on two instruments rather than on a property of summons.

**The question, stated generally:** a `TrackedBar` row is a cooldown item like any other, and
the client visibly knows a live remaining time for it — it draws a moving bar. What of that is
reachable from an addon, and through which surface? It has only ever been asked as "does
`auraUp` work on one", which is a question about cap's own gate. **It matters beyond the one
case:** if a bar row yields liveness or a duration, several things cap infers from watching its
own cast become **reads** — whether the pets are out, how long a summon has left, and beyond
Demonology any spec whose rotation turns on a pet.

**What is measured, and it is narrow — do not re-run these:** `item.auraDataUnit` is `nil` on
cid `760`, 13 in-combat samples `[client 2026-08-06]`; and the **alert channel is silent on that
row**, 0 edges out of 1054 across 171 observed casts while a genuine aura row in the same
captures raised 141 `[client 2026-08-07]`. ⚠ **Neither is evidence about the bar itself** — a
BuffBar item's bar is refreshed from the item's own update path, not from the alert channel.

**Candidate surfaces, none tried:** `pipTexture:IsShown()` (the mixin computes
`currentTime = expirationTime - GetTime()` and calls `SetShown(currentTime > 0)` — a boolean for
*this bar is live*, already a `[gap]` in `cooldown-manager.md`); the bar widget's own
`GetValue()` and min/max; the row's linked spell `193332`, which the icon row does not carry and
which 404s on the Game Data endpoint — the shape of a hidden duration aura; and the ordinary
cooldown-item surface asked of a bar row.

**What would decide it.** A discriminate test, and it is a precondition rather than a nicety:
this project already has a standing example of a widget read that looks like a signal and is a
constant. **Any candidate must read differently when the pets are out and when they are not, in
the same pull**, before anything is built on it. Deliberately *not* scoped as "make the
Dreadstalkers readable" — the interesting answer is the general one.

### D8 — How is polarity drawn? **Reopened**, after the answer was removed rather than argued.

**Raised:** 2026-08-08, when the rule that had closed it was struck.

**Why it is open again.** `spec.md` §6 carried *"How is polarity drawn?"* as an explicitly open
visual-design question. M3c closed it by asserting that polarity is carried by shape and that
press and hold may never differ only in hue — a claim that entered in the rule cull, was never
argued, and is downstream of none of §1's three principles. Removing an answer reopens its
question rather than leaving the design unstated.

**What is settled and is not in question.** A positive cue is drawn in the treatment of the tier
it stands for; a negative cue uses the hold treatment, which belongs to no tier. What is open is
only **how a player tells the two apart on screen.**

⚠ **The colour-blind / greyscale defence below was struck from §3.1 on 2026-08-10 as downstream
of none of §1's three principles.** It is admissible here **as an argument** — this file's
contract is the case on both sides, and an argument does not become inadmissible because a rule
built on it was culled — but it carries no authority, and adopting it would need the principle
it has never had. Same shape as D10's and D11's struck rules.

**The case for shape or position carrying it.** It survives a small icon and a colour-blind
read, and it composes with the emphasis ladder without adding a second thing to decode. Today's
implementation happens to work this way — a count at the top, a hold glyph at the bottom.

**The case against making that a rule.** It forbids designs that are simpler and say more. The
concrete example that raised this: **one marker whose visibility and colour are both driven off
the same duration**, appearing as *hold* when a burst window is far and turning into *press* as
it arrives — one mark, one position, two curves, against two separate marks under a shape rule.
It also directly fixes `catalog.md` **O8**, where the hold marker is lit through the stretch in
which pressing is correct.

**A mechanism fact, not a design opinion:** driving *colour* from a sealed value needs
`C_CurveUtil.CreateColorCurve`, which appears nowhere in Blizzard's shipped UI, and whether a
duration object's `Evaluate*` accepts a colour curve is **unmeasured**. Driving *alpha* is
measured and shipped. So a colour-flip design needs a lab answer first; two alpha-driven
textures of different colours need nothing new.

**What would decide it.** A flown build and what a person actually mistook for what — which is
the whole reason drawing came before the rest of §3's detail.

### D7 — May a grade exist without a tier? E1's and E2's `cooldownRemaining` grade cannot fire.

**Raised:** 2026-08-08, while wiring `Treatment.lua` to the verdicts.

📊 **Measured: the hypothesis below is now a fact, and it is a register error rather than a
tuning question.** Across the flown pull HIGH sat at exactly its **ungraded midpoint `a91` for
about 95 % of its occupancy** (summed across entries: `a91` 157.3 % of the pull against `a96`
3.3 %, on ~165 % total HIGH occupancy). MEDIUM *did* vary — `a63` 181.2 %, `a66` 83.2 %, `a60`
17.1 %, `a72` 3.1 % against ~263 % occupancy — precisely because E5 and E7 grade on `shards`,
which is a **gate**. E3 declares no grade at all, and E1's and E2's name
`cooldownRemaining(this)`, a **channel**: cap by construction cannot read it, so a grade
written on cap's own frame alpha can never fire from one. §3.1's continuous emphasis is, on
this catalog, running on **two of eight entries**. ⚠ **What to do is still open** — the
provisional lean below is untouched — but *whether the grades are inert* no longer is.

**The finding, from the code.** `Tier.Evaluate` computes a grade **only when a band held**, and
E1's and E2's bands all require `ready(this)`. So the grade `cooldownRemaining(this)` is produced
only when the cooldown is already up — i.e. only when its value is zero. Every moment it would
say something, the entry has no tier and no grade is produced at all. ⚠ **`catalog.md` claims
otherwise**: E1's grade line describes the icon warming as the window approaches, which nothing
in the current code or the current spec can produce.

**The case for "a grade may exist without a tier".** The information is real and legal — the
countdown is a channel, the client owns it, cap never sees it. Refusing to draw it throws away
exactly the contextualising move §1 ranks third, and "how far out is my burst window" is not a
claim that the button is worth pressing.

**The case against.** §3.0 defines a grade as *continuous emphasis within a tier*; a grade with
no band is a third register beside graded and cued, where §3.1 says there are two. And the thing
it wants to draw is a **countdown**, which is what §3.4's bars are for.

**Provisional lean: it is a §3.4 question, not a §3.1 one.** The natural home for "Tyrant is
40 s out and warming" is the cooldown **bar**, where the number is legible and the tier is
already applied. If that is the answer, E1's and E2's grades are deleted from the catalog.

**What would decide it — and it is now answerable.** The bars are built and have flown
(v0.2.4, 2026-08-10), so the surface this item was parked on exists and the question is a
look rather than an armchair: put a warming Tyrant bar in front of someone and ask whether the
countdown wants the emphasis. The two grades remain inert rather than wrong-on-screen in the
meantime — `Treatment.For` passes a channel descriptor through untouched — so nothing is
drawing from them either way while this is open.

⚠ Raised in passing and **not** written up as an item: **what is a cue budget?** — tracked as a
`spec.md` §6 open question instead, because it cannot be argued in the abstract.

---

## Struck

*(what it asked, what it resolved to, and where the decision lives now)*

### D3–D6 — the founding rules, re-read

**Raised + struck 2026-08-07.** Four questions about four rules, answered as one: the rules had
multiplied past what they were protecting. **Resolved to:** cap's mission is three principles and
everything else is downstream — they are `spec.md` §1 (a)/(b)/(c), which is where the decision
now lives. The process change mattered more than the cull: **ship it, play with it, refine until
it feels good, then reverse-engineer the rules from that for the second spec.**

### D1 — Can a channel select between BANDS, by driving alpha on two rendered treatments?

**Raised + struck 2026-08-07.** **Resolved to:** *no* to the literal proposal — channels stay out
of band conditions entirely, which is `spec.md` §3.5's register-legality check. But its real
content — *cross-ability facts should reach the player through the client rather than through
cap's arithmetic* — **was** adopted, larger: cues gained polarity and arbitrary subjects.
⚠ One cost is permanent and was accepted rather than solved: a secret-driven rendering has **no
readback**, so cap can never learn what appeared.

### D2 — What problem does the window mechanic solve?

**Raised + struck 2026-08-07.** **Resolved to:** it does not solve one — every window read
something cap could already see, so the budget constrained *expression*, not capability. The
mechanic was deleted; bands may name any declared ability through the gate vocabulary
(`spec.md` §3.5), and the guard against a priority ladder moved from syntax to the HIGH-at-once
measurement. The code followed on 2026-08-08 (`notes.md`, the window migration).
