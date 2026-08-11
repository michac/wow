# Combat Assist Plus — open discussion

**What this file is for:** topics raised and **not yet decided**. A discussion item is
not agreed work (that's `backlog.md`), not a product decision (that's `spec.md`), and not
a record of what we did (that's `notes.md`). It exists because those three have no home
for *"here is a question that would change the design, and here is the case on both
sides"* — which previously meant such questions either got decided in passing or lost.

**Lifecycle.** An item leaves this file when it is decided: the decision goes to
`spec.md` if it changes what cap should do, to `backlog.md` if it becomes work, and the
reasoning to `notes.md`. Strike it here with the date and where it went. Nothing here
ages, and nothing here is a commitment.

Each item is written to be read **cold**, with no conversation behind it.

---

## Open

### D17 — The stock proc glow was NOT suppressed. Is the dim not running, or not reaching a pixel?

**Raised:** 2026-08-10, from the first flight of the drawn surfaces (v0.2.4). Observed:
*"the blizzard proc is not suppressed. When Demonbolt procs its glow blows the others out of
the water, looks super high priority. Same with IB."*

**This is the first measured result on `Glow.lua`, and it is a negative one.** The module was
built against CDMProbe's `HudProcGlow.lua` — post-hook each item's `RefreshOverlayGlow`, set
`item.SpellActivationAlert:SetAlpha(0.5)` — and that mechanism was never measured by us; it was
read off another addon's source, which is exactly why `backlog.md` files the KB drain as
*blocked on the flight* rather than writing the claim.

**The observation is worse than "the dim is too shallow".** A proc'd Demonbolt reading as the
loudest thing on screen is the failure §3.2 exists to fix: cap's whole grading argument is that
Blizzard's glow says *available* while cap says *worth this much*, and an unsuppressed glow
overrides the tier signal on exactly the ability the tier signal has an opinion about. The
Infernal Bolt report matters separately — that is E10's transform, so a second row is affected
and it is not a Demonbolt-specific quirk.

**Four candidate causes, and they are distinguishable.** In rough order of likelihood:

1. **Nothing was hooked.** `Glow.Arm` refuses a frame whose `RefreshOverlayGlow` is not a
   function, silently. If the CDM item mixin does not carry that method under 12.0.7, or the
   rows `Bind.Rows()` yields do not carry `.frame`, the count is zero and no alpha was ever
   written.
2. **Hooked, but `live` was false.** Liveness rides `Sense.OnVerdicts`; if `light()` never
   fired, every callback returned early.
3. **Hooked and live, but `SpellActivationAlert` is the wrong field** on a CDM item — CDMProbe
   drove action-bar-shaped frames, and the CDM's alert may live elsewhere or be re-created per
   proc, in which case the alpha lands on a stale object.
4. **The alpha landed and the animation overrides it.** The whole premise is that alpha on the
   *alert frame* multiplies without fighting the proc animation, which drives the *children's*
   alpha. If that premise is wrong for the CDM's alert, the write is real and immediately
   stomped.

**How it gets decided — and the instrument already exists.** `glow:` on the `draw` stream reads
`<frames>/live` or `<frames>/off`. `glow:0/…` is cause 1 and needs no further guessing;
`glow:N/off` is cause 2; `glow:N/live` with the glow still bright narrows it to 3 or 4, which a
ClientLab probe of a live CDM item's field names would separate. ⚠ **The capture must come from
a `/reload` after a pull on v0.2.4 or later** — the ring on disk as of this writing is entirely
v0.2.3 and carries no `glow:` field at all.

**What this blocks.** **D10** cannot be answered until this is fixed. D10 asks whether cap's
ring reads as distinct from the stock glow; with the stock glow at full strength the comparison
is not the one D10 poses, and a "they look the same" verdict now would be measuring the wrong
thing.

### D16 — Tyrant should be MEDIUM with two markers, not promoted to HIGH. What draws a marker cap computes itself?

**Raised:** 2026-08-10, from the first flight. Observed: *"tyrant was promoted to HIGH when
dreadstalkers was cast. It's supposed to always be MED when off cooldown, and get a cue for
dreadstalkers and a second cue if the grimoire is out. Just coloured dots or plus signs."*

**The tier half is decided and is a catalog edit.** E1 band 1 is currently
`ready(this) and not ready(E2)` → HIGH — the promotion the window migration authored when it
re-expressed a deleted window as a band (`notes.md` 2026-08-08). Play says the promotion is wrong: Tyrant off
cooldown is *reasonable*, not *press this now*, and what the player actually wants to see is
**which setup pieces are in place**. So E1 collapses to one MEDIUM band on `ready(this)` and the
staging information moves to markers. That much needs no discussion; it is filed in `backlog.md`.

**The open question is what a marker like this even is, and the vocabulary does not currently
have one.** §3.0 defines a **cue** as decided by cap *and* the client — cap evaluates the gate
precondition, the client evaluates the sealed channel. But *"Dreadstalkers are out"* is
`not ready(E2)`, a **gate**: cap can read it and branch on it outright. There is no sealed
quantity, so there is nothing for the client to decide. Three ways out, and they are genuinely
different designs:

- **(a) Let a marker be driven by a gate alone.** Simplest and matches what was asked for — a
  dot cap lights because cap knows the fact. But it widens §3.0's cue definition, and the
  gate/channel split is the one line §1 principle (a) says is worth enforcing in code.
- **(b) Keep it a cue and find a channel.** `active(x)` → **pip** is already in §3.5's channel
  table and is one of the three forms with no marker built. It is the closest fit by name, but
  what `active` would name here is a *pet*, and whether the client exposes a pet's existence
  through any sealed sink is unmeasured.
- **(c) Say it with bands after all** — three tiers cannot carry two independent booleans, so
  this fails immediately. Recorded so nobody re-proposes it.

**Which marker is a second question.** §3.1 has two slots, count (top) and hold (bottom), and
the marker-placement rule that said *"there are two of them"* was culled on 2026-08-10 — so
adding a third is no longer forbidden, but nothing says where it goes either. Two dots that
mean different things also need to be told apart, and **D8** (how polarity is drawn) is already
open on the neighbouring question.

**How it gets decided.** (a) versus (b) is the real fork and it is a spec question, not a
measurement: does cap's vocabulary admit a marker with no client half? Worth noting that
`backlog.md`'s channel-coverage table predicted this exact moment — it says the trigger for
building an unbuilt marker form is *"a catalog entry that needs one"*, and this is the first one.

### D15 — A row whose override is a DIFFERENT ability reads as ready. Whose problem is that?

**Raised:** 2026-08-10, from the first flight. Observed: *"the grimoire:imp button transforms
into a Consume Magic when on cooldown … it just shows up on CDM as an ability that's not on
cooldown and slotted into my dps rotation. cap highlights it basically the entire time as a
high-priority ability, even when it's in this state and the real ability is on cooldown."*

**This is a real defect and the desired behaviour is decided: that state is *none*.** What is
open is **where the fix belongs**, and the two answers generalise very differently.

**Why it happens.** E3 binds the Grimoire row and its bands are `ready(this)` → MEDIUM,
`ready(this) and ready(E1)` → HIGH. When Grimoire goes on cooldown the row's *identity* flips to
Consume Magic — a real, castable, off-cooldown utility spell — so `ready(this)` reads **true**
for the whole cooldown. cap is not misreading anything; it is correctly reporting that the
ability the row currently shows is ready. The catalog simply never said which identity it meant.

**(a) Catalog-level.** cap already has the tool: `identity(this, …)` is a gate, it is measured
readable in combat (M3a: `info.overrideSpellID` plain on 21/21 rows), and **E6 Ruination is
built on exactly this channel**. E3 gains an identity term and the fix is four lines. Cheap,
precise, and it is the mechanism the vocabulary was designed for. But it is per-entry: every
future transforming row on every future spec has to remember, and forgetting is silent — the
entry lights permanently and looks like it is working.

**(b) Engine-level.** State the invariant once: *an entry whose bound row is currently
displaying a different ability has no opinion.* cap can see this — it has the authored spellID
and the live override on every evaluation — so `Tier` could refuse the entry outright rather
than each catalog remembering. This makes the failure structurally impossible. The cost is that
it is a new normative rule about what a tier *is*, and it would need to survive §3.1's own
test — which principle is it downstream of? Plausibly (b): using non-secret information well.
⚠ It also collides with the transform entries that exist **on purpose**: E6 and E10 declare one
entry per identity and *want* to fire on the overridden one, so the rule has to distinguish
"transformed into something another entry claims" from "transformed into something nobody
declared", and getting that boundary wrong silences Ruination.

**How it gets decided.** (a) unblocks the flight immediately and (b) is the durable answer;
they are not exclusive, and doing (a) now does not foreclose (b). What should not happen is (a)
shipping quietly and the general case being forgotten, which is why this item exists rather
than just a backlog line. ⚠ Worth checking against the roster before choosing: **how many other
CDM rows on this spec transform into an unrelated ability while on cooldown?** Nobody has
looked, and if the answer is "several" that argues for (b).

### D14 — The tier glows read as candles. Is the fault brightness, pulse depth, or rate?

**Raised:** 2026-08-10, from the first flight. Observed: *"the tier glows are way too
'flickery' — looks like candles. Needs to be brighter across the board."*

**Both halves of the report matter and they are not the same complaint.** "Too flickery" is
about the **pulse**; "needs to be brighter" is about the **alpha**. A fix that only raises alpha
leaves a bright candle.

**What is actually on screen, and which numbers were measured.** The tier alphas *were* picked
by a person on real spell art at true CDM size (`glow-palette.md`) — HIGH 1.00, MEDIUM 0.78,
LOW ungraded 0.43. **The pulse was not.** Rate came from the lab as 2.5 / 1.2 / 0.5 Hz, but the
**trough — 0.68 of the tier's alpha — was picked at a desk**, and it is the number that decides
how much a ring visibly dips. So the strongest suspect is the one thing here nobody looked at.

**Three candidate faults, and they call for different fixes:**

- **Trough too deep.** At 0.68 a HIGH ring swings between 0.68 and 1.00 every 0.4 s. That is a
  32 % luminance modulation at 2.5 Hz, which is close to the description. Raising the floor
  (0.85, say) keeps the motion and stops the guttering.
- **Rate too fast.** 2.5 Hz is at the top of the band the eye tracks as flicker rather than as
  breathing. ⚠ Rate is also load-bearing for something else: it is what separates HIGH from
  MEDIUM once §3.1's pulse-may-cross-brightness-bands clause let the two overlap in rendered
  alpha. Slowing everything flattens that separator.
- **Base alpha too low against real icon art.** Possible for MEDIUM and LOW, but HIGH is already
  at 1.00 and cannot go up — so if HIGH reads dim, the fault is the trough or the ring's own
  additive blend over a bright icon, not the alpha.

**A fourth possibility worth stating because it is cheap to test:** the ring is an `ADD`-blended
flipbook, and ADD *"blows out over a bright icon and vanishes over a dark one"*
(`cue-treatments.md`). Candle-like guttering is what an additive glow does over mixed art. `BLEND`
was offered as the alternative in the lab and was never compared on cap's own frames.

**How it gets decided.** By looking, with one variable moved at a time — and the numbers all
live in one table (`Treatment.lua`'s `TIERS` and `PULSE`), which is what makes that practical.
⚠ **The one thing that may not be quietly dropped is the per-row phase offset.** It is a
seizure-floor property, not a style choice: ~14 icons flashing *in sync* cross WCAG 2.3.1's
general flash threshold and the same 14 offset never approach it. Raising the trough reduces
the modulation and helps; synchronising the rows to look tidier is the one move that is off the
table.

### D13 — A resting bar and an empty track are two numbers nobody has looked at. What are they?

**Raised:** 2026-08-10, by the fix pass on the bars, which found the first answer was an
analogy. **Nothing here has been seen on screen** — no bar has drawn at all.

**What is derived, and it is only the ordering.** §3.1's surviving ladder property is that
the ladder is *ordered*, and *none* is its bottom rung. A bar has no ring, so the fill is the
only thing that can carry the LOW → *none* step, and the resting fill therefore has to read
**under LOW's dimmest**. The resting slate is LOW's own hue, so on the shared hue that reduces
to an alpha strictly under LOW's dim end. That much follows.

**What is picked.** Everything else. The value inside that bound (`Treatment.BAR.rest.a`) is a
pick; the empty track's colour and alpha are picks with no argument at all behind them. They
are not in the same class as §3.1's tier alphas, which a person chose looking at a real spell
icon at true CDM size, and `spec.md` §3.4 now states the property rather than the numbers for
that reason.

**Why the bound is not the whole question.** Two failures sit on either side of it. Too bright
and a resting bar reads as a dim LOW — *cap thinks this is filler* — which is the collision the
bound exists to stop, and which the first cut of this walked into: the resting fill was the
LOW hue at alpha `0.40`, inside LOW's own `0.36 – 0.50` band, so a LOW bar at grade ≈0.286 drew
exactly the resting pixels. Too dim and the bar reads as *empty* — the fill stops separating
from the track, and a countdown you cannot see the extent of is worse than no bar. Neither
edge is arithmetic; both are a look.

⚠ **Unreachable on Demonology today, and that is not a defence.** No entry on the roster bands
LOW — E1/E2/E3 are HIGH/MEDIUM and E8 is MEDIUM — so the bright-side collision cannot occur on
this catalog. It is a property of `Treatment.Fill`, which is the **shared engine** every future
spec draws through, and it was written into `spec.md` as a normative table before any spec
could reach it.

**How it gets decided.** By looking, and by nothing else. `B{}` says `armed`, which means cap
handed the client a duration object — it says nothing about a colour, and no capture can. The
first flight of the bars is the instrument: is a resting bar obviously *counting down with no
opinion*, is a tiered bar obviously not resting, and is the empty part obviously empty?
`backlog.md` → *Judge the bars on screen* carries it alongside the three legibility questions.

**Explicitly not being fixed here.** Do not re-derive the number from another surface's
constant — the veil, the pulse trough, a band width. That is the move this item exists because
of: an analogy between two different composites, presented as a derivation and then pinned by
a test. If the pick reads wrong, replace it with a number somebody looked at.

### D12 — If the Wild Imp count saturates, is E8's positive cue lit nearly all the time?

**Raised:** 2026-08-10, by the argument that gave Implosion a §3.4 bar. **Nothing here has
been seen on screen, and the two claims below cannot both be right.**

**The collision, stated plainly.** `catalog.md` §4 now gives Implosion a bar on the grounds
that *once the rotation is rolling you almost always have 6+ Wild Imps up, so the count is
saturated and what gates the press is the 15 s cooldown*. `catalog.md` **E8** says the
opposite about the same count, one section earlier: its band stops at MEDIUM because
`ready(this)` is true most of a pull and a permanently-lit HIGH is *"the same failure as a
HIGH that never fires"*, while the cue is safe because *"the imp count crosses 6 in bursts,
so the HIGH-styled number arrives and leaves with the actual opportunity."* If the count is
saturated in steady state, the cue is close to permanently lit and is the exact failure E8's
own ⚠ says it capped the band to avoid.

**Why the bar claim does not simply settle it.** The two statements are about different
stretches of a pull and both could be locally true: imps are generated in bursts by Hand of
Gul'dan and consumed by Implosion itself, so "saturated most of the time" and "crosses 6 in
bursts" differ mainly in how long the trough after an Implosion lasts. The bar argument only
needs the count to be *non-discriminating often enough that the cooldown is the real gate*;
the cue argument needs the count to be *below 6 often enough that a lit number means
something*. Nothing measured says which describes a real pull, and neither claim was.

**What is at stake if the cue is permanently lit.** It is not merely noisy — E8's cue is the
whole of its HIGH (no band may test the count, `spec.md` §3.1), so a cue that never goes out
means Implosion reads HIGH permanently, which is the one reading §3.1's ladder cannot carry.
The generic version of that worry is already a backlog line (*Cap the HIGH tier's
population*); this is its first concrete instance.

**How it gets decided.** By a pull, and cheaply: `C{}` on the `draw` stream already reports
E8's cue as `armed` / `refused` on every change, and `refused` on that cue means *there are no
imps* (`backlog.md` → *M3d*). The duty cycle of `armed` across a flown pull is the answer,
and it needs no new instrument. ⚠ **What it cannot tell you is where the threshold should
be** — `armed` says the quantiser was asked, never what it drew, so "the count crossed 6" is
still an eyeball's question.

**Explicitly not being fixed here.** Candidate answers, none argued: raise `n` above 6,
tighten the gate precondition beyond `ready(this)`, or accept a lit cue and change what
Implosion's HIGH means. Do not redesign E8 off this item without a flown duty cycle.

### D11 — Do the tiers need **separated** emphasis ranges, or is an ordered ladder enough?

**Raised:** 2026-08-10, by the §3.1 cull, which removed the rule that answered this by
assertion. **Nothing here has been seen on screen.**

**What was removed and why.** §3.1 carried *"each tier owns a disjoint brightness band, and
a grade moves an entry only inside its own — a fully-graded MEDIUM never reaches the dimmest
ungraded HIGH"*, justified as *a grade never changes the tier* **expressed as arithmetic**.
That justification does not hold: *a grade never changes the tier* is a claim about
**computation** and is true by construction — the bands settle the tier, and a grade is only
computed afterwards and only lerps inside that tier's own range. Nothing about the tiers'
ranges overlapping can make it false. The pixel claim is a **second, separate** claim wearing
the first one's argument, and it is not downstream of (a), (b) or (c).

**What it cost while it stood, which is what makes this worth an item.** It is the rule that
moved LOW's ring from the lab-measured **0.50** — picked by a person, on a real spell icon, at
true CDM size — to a band topping out at 0.36, a number nobody chose and nobody has seen. The
rule's own §3.1 text already conceded that the screen does not obey it: the pulse is a second
channel and HIGH's trough dips under MEDIUM's peak deliberately. So the invariant bound an
internal number that the renderer then violated anyway.

**The case for bringing separation back in some form.** Two icons at the same emphasis
carrying different tiers is a real thing to worry about, and the ladder's order is only
readable off the pixels if the rungs stay apart. A graded LOW can now reach a dim MEDIUM.

**The case against.** Separation was never measured against anything: the lab compared LOW's
ring against *none*, and it compared each tier at full strength against the others at full
strength. Nobody has yet looked at a dim MEDIUM beside a bright LOW and said which read
wrong. And a rule that narrows every grade's range to keep the tiers apart spends exactly the
thing §1's second move is for — a grade with room to move.

**How it gets decided — and ⚠ NOT by the flight this used to defer to.** The plan was: look
at a pull where E7 Demonbolt is graded down at LOW while something else sits at a dim MEDIUM,
and say whether the tiers are still telling you apart. **On the Demonology catalog that state
is unreachable**, so a flight will come back "looks fine" for a reason that has nothing to do
with the question. The bands overlap; the catalog never gets into the overlap:

| | Reachable extreme | Where |
| --- | --- | --- |
| brightest **LOW** | **0.3526** | E9 / E10 at their ungraded midpoint (`0.43 × 0.820`) |
| dimmest **MEDIUM** | **0.3989** | E7 at grade `0.4` (`0.60 × 0.665`) |

A gap of **0.046**, and every step of it is forced by the catalog rather than by the
treatment table. E7's MEDIUM band needs `shards ≤ 3` while its grade is `resource` *falling*,
so entering MEDIUM at all pins the grade at `≥ 0.4`; E5's needs `affordable`, and Hand of
Gul'dan's 3-shard cost pins that grade at `≥ 0.6`. In the other direction E7's LOW band needs
`shards ≥ 4` on the same falling grade, so a graded LOW is pinned at `≤ 0.2` (0.318) — the
brightest LOW anything reaches is an **ungraded** one, and it still lands under the floor.
*(Arithmetic: an exhaustive sweep of every gate combination the catalog admits, with
affordability tied to the DB2 cost. Both extremes above are that sweep's answer.)*

**So what the flight can actually answer is the weaker question**: whether E7's graded LOW at
0.318 reads apart from a MEDIUM at 0.399 — 0.08 of brightness plus a hue change, which is not
the adjacency the rule was about. **Observing the real adjacency needs one of three things,
none of them a pull:** a catalog entry whose LOW band is reachable while its grade is *high*
(nothing on Demonology grades that way); a second spec that has one; or a deliberate mock —
force LOW to its 0.410 bright end and MEDIUM to its 0.319 dim end side by side and judge
that, which is a lab picker's job and not a pull's. Until one of those happens **this stays
open, and a null result from the first pixels flight is not evidence either way.**

If it does turn out they cannot be told apart, the fix is a number — a lower MEDIUM ceiling,
a narrower grade range, or a hue that does not share a luma with the tier above — and not a
restored invariant.

⚠ **One consequence is already handled and must not be re-derived.** A row two entries bind
is drawn in the **higher of the two tiers**, which used to be delivered for free by "brighter
= higher tier". `Overlay` now compares tier order first and emphasis only inside one tier, so
this question cannot reach that path whichever way it goes.

### D10 — cap's ring **is** Blizzard's proc-glow sheet. On screen, do they read as one thing or two?

**Raised:** 2026-08-10, by the measured restyle, which made a rule and a design collide in
one commit. **Nobody has seen either of them on screen.**

**The collision, stated plainly.** `spec.md` §3.1's last surface rule was *"cap does not
reuse Blizzard's proc-glow art"*, because *"an emphasis that looks like the stock glow makes
the two indistinguishable — which is the failure §3.2 exists to fix."* The treatment a person
picked in the lab draws **`UI-HUD-ActionBar-Proc-Loop-Flipbook`** — which is precisely the
sheet Blizzard's proc alert plays. The rule as written forbade the pick.

**The case for the pick.** The rule's *reason* is about the two emphases being
indistinguishable, and three things separate them that did not exist when the rule was
written: §3.2's suppression dims the stock glow to a fraction of its volume, cap's ring is
drawn in a **tier hue** at a **tier alpha** where the stock glow is uniform gold at full, and
cap's **pulses** where the stock glow does not. A shared sheet is not a shared emphasis.
Against a stock glow that is no longer at full volume, "you cannot tell them apart" may
simply be false. And the sheet is a shipping client asset: no vendored library, no license
question, and art baked for exactly this size.

**The case against.** The rule may have meant what it said. A player who has spent years
reading that specific ring shape as *Blizzard says press this* is being asked to re-learn it
as *cap says this much*, which is a heavier ask than a colour change; and a proc'd icon would
then carry the same shape twice, once dimmed and once tinted. There is also a weaker version
of the worry that survives even if the strong one fails: the ring may read as a proc rather
than as an emphasis, which is a different failure from being confused with the stock glow.

**What the spec says today, and how it got there.** The rule was **narrowed to its root, not
re-transcribed around the pick.** Its root is §1's second move — Blizzard's glow says
*available*, cap says *available, and worth about this much* — which requires only that the
two be **distinguishable**. *"cap does not reuse Blizzard's proc-glow art"* is strictly
stronger than that: the same sheet in a different colour can satisfy the root, and a
different sheet in the same gold can violate it. So §3.1 now asks for distinguishable and
says the separation cannot come from the art, and the question of whether the shipped
treatment achieves it is **this item**, unchanged and still open. The code was not touched:
the rule was the thing that could not be argued from a principle, not the pick.

**How it gets decided: the first pixels flight, and nothing else.** Sit at a Demonic Core
proc on Demonology with the suppression live and look at whether the two read as one thing or
two. If they read as one, the fix is cheap and already inventoried — `Treatment.RING.atlas`
is one string, and `glow-palette.md`'s candidate run has ~15 shipping alternatives with their
grids already declared, `ui-cooldownmanager-alert-flipbook` first among them.

### D9 — What can actually be retrieved from a **bar** cooldown item?

**Raised:** 2026-08-08, after a claim that cap could not know whether a summon's pets are out
turned out to rest on two instruments, not on a property of summons.

**The question, stated generally:** a `TrackedBar` row is a cooldown item like any other, and
the client visibly knows a live remaining time for it — it draws a moving bar. So what of
that is reachable from an addon, and through which surface? This has never been asked as a
question about **bar rows in general**; it was only ever asked as "does `auraUp` work on one",
which is a question about cap's own gate.

**Why it matters beyond the one case.** If a bar row yields liveness or a duration, then
several things cap currently *infers from watching its own cast* become **reads**: whether the
Dreadstalkers are out, how long a summon has left, and — beyond Demonology — any spec whose
rotation turns on a pet or a temporary summon. It would also give the §3.4 bars an exact
source for a row the Essential viewer has no cooldown for. An inference that reads *short*
(the current one closes while the pets are visibly still up, because casting Tyrant extends
them) would become one that does not read short at all.

**What is measured, and it is narrow — do not re-run these:**

- `item.auraDataUnit` is `nil` on cid `760` (Call Dreadstalkers, BuffBar), 13 in-combat
  samples `[client 2026-08-06]`.
- The **alert channel is silent on that row**: 0 edges of any kind out of 1054 recorded,
  across 171 observed Dreadstalkers casts, while a genuine aura row in the same captures
  raised 141 `[client 2026-08-07]`.

⚠ **Neither of those is evidence about the bar itself.** A BuffBar item's bar is refreshed
from the item's own update path, not from the alert channel — so "the alerts are silent" most
likely says the alert channel is the wrong instrument for this row, which is a statement about
the instrument cap picked.

**Candidate surfaces, none tried, none claimed to work:**

- **`pipTexture:IsShown()`** — `CooldownViewerBuffBarItemMixin:RefreshCooldownInfo` computes
  `currentTime = expirationTime - GetTime()` and calls `pipTexture:SetShown(currentTime > 0)`.
  A boolean for *this bar is live*, in the `PandemicIcon` mould. Already carried as a `[gap]`
  in `knowledge/addon-dev/cooldown-manager.md`.
- **The bar widget's own state** — `barFrame:GetValue()` and its min/max. Likely secret in
  combat; the question is whether it refuses or answers.
- **The row's linked spell `193332`** (`CooldownSetLinkedSpell 688,193332,0,760`), which the
  icon row does not carry and which 404s on the Game Data spell endpoint — the shape of a
  hidden duration aura. If it is reachable, a duration object may be too.
- **The ordinary cooldown-item surface** — the info struct, the item frame's Cooldown widget —
  asked of a bar row rather than of a spell row.

**The counter-case, so it is not lost:** every one of those is a *widget* read, and this
project already has a standing example of a widget read that looks like a signal and is a
constant (`IsActive()` on a tab-1 row). Any candidate must clear a discriminate test — it has
to read differently when the pets are out and when they are not, in the same pull — before
anything is built on it.

**Not decided, and deliberately not scoped as "make the Dreadstalkers readable."** The
interesting answer is the general one, because it applies to every spec with a bar row.

### D8 — How is polarity drawn? **Reopened**, after the answer was removed rather than argued.

**Raised:** 2026-08-08, when the rule that had closed it was struck.

**Why it is open again.** `spec.md` §6 carried *"How is polarity drawn?"* as an explicitly
open visual-design question. M3c closed it by asserting **polarity is carried by shape, and
press and hold may never differ only in hue** — a claim that entered in the rule cull, was
never argued, and is not downstream of any of §1's three principles. It has been removed
(`notes.md`, 2026-08-08). Removing an answer reopens its question, so it comes back here
rather than quietly leaving the design unstated.

**What is settled and is not in question.** A positive cue is drawn in the treatment of the
tier it stands for; a negative cue uses the hold treatment, which belongs to no tier. Those
are statements about what a cue *means* and they survive. What is open is only **how a
player tells the two apart on screen.**

**The case for shape or position carrying it.** It survives a colour-blind read, it survives
a small icon, and it composes with the brightness ladder — which already uses hue as an
accent rather than as the signal — without adding a second thing to decode. Today's
implementation happens to work this way (a count at the top, a hold glyph at the bottom).

**The case against making that a rule.** It forbids designs that are simpler and say more.
The concrete example that raised this: **one marker whose visibility and colour are both
driven off the same duration**, so it appears as *hold* when a burst window is far and turns
into *press* as the window arrives. That is one mark, one position, two curves — against two
separate marks under a shape rule. It also directly fixes a known defect (`catalog.md` O8,
where the hold marker is lit through the stretch where pressing is correct) by saying the
useful thing there instead of merely going dark.

**What is a mechanism fact rather than a design opinion**, and must not be confused with
one: driving *colour* from a sealed value needs `C_CurveUtil.CreateColorCurve`, which
appears nowhere in Blizzard's shipped UI, and whether a duration object's `Evaluate*`
accepts a colour curve is **unmeasured** — the measured return is the plain evaluated
result (`knowledge/addon-dev/security-taint-and-restricted-data.md` §4.8.1 finding 9 and
§4.8.4). Driving *alpha* is measured and shipped. So a colour-flip design needs a lab
answer first; a design built from two alpha-driven textures of different colours needs
nothing new and is visually the same thing.

**Not decided.** Decide it against a flown build and what a person actually mistook for
what — which is the whole reason drawing came before the rest of §3's detail.

### D7 — May a grade exist without a tier? E1's and E2's `cooldownRemaining` grade cannot fire.

**Raised:** 2026-08-08, while wiring `Treatment.lua` to the verdicts.

**The finding, from the code.** `Tier.Evaluate` computes a grade **only when a band held**
(`if verdict.tier then verdict.grade = gradeOf(e, w) end`). E1's two bands both require
`ready(this)`; E2's single band requires `ready(this)` and `affordable(this)`. So the grade
`cooldownRemaining(this)` is produced **only when the cooldown is already up**, i.e. only
when its value is zero. Every moment it would say something — the cooldown ticking down —
the entry has no tier, so no grade is produced at all.

**`catalog.md` claims otherwise.** E1's grade line reads *"the icon warms as the window
approaches"* and calls it "the contextualising half of the spec's centrepiece". Nothing in
the current code can produce that, and nothing in the current *spec* can either: a grade is
emphasis **within a tier**, and there is no tier to be within.

**The case for "a grade may exist without a tier".** The information is real and legal —
the countdown is a channel, the client owns it, cap never sees it. Refusing to draw it
throws away exactly the contextualising move §1 ranks third. And "how far out is my burst
window" is not a claim that the button is worth pressing, so it is not a tier claim.

**The case against.** §3.0 defines a grade as *"continuous emphasis within a tier"* and
§3.5 as *"modulates emphasis continuously within a band; it never changes the band"*.
A grade with no band is a second, tier-less emphasis channel — a third register beside
graded and cued, which §3.1 says there are two of. And the thing it wants to draw is a
**countdown**, which is what §3.4's bars are for: an icon is too small to carry one, which
is the reason that feature exists.

**Provisional lean: it is a §3.4 question, not a §3.1 one.** The natural home for "Tyrant
is 40 s out and warming" is the cooldown **bar**, where the number is legible and the tier
is already applied. If that is the answer, E1's and E2's grades are deleted from the
catalog and the bar's own `cooldownRemaining` channel carries it — and `catalog.md`'s two
grade lines are wrong today and should be struck when M4 lands.

**Do not decide this from an armchair — decide it against M4's drawn bars.** Until then,
the two grades are inert rather than wrong-on-screen: `Treatment.For` passes a channel
descriptor through untouched, so nothing is drawn from them either way.

Candidates raised in passing and **not** yet written up as items — add them properly if
they start to matter:

- **What is a cue budget?** Tracked as a `spec.md` §6 open question rather than here,
  because it cannot be argued in the abstract — it needs a drawn catalog.

---

## Struck

### D3–D6 — the founding rules, re-read

**Raised:** 2026-08-07 · **Struck:** 2026-08-07 — **decided together, and the answer was
smaller than any of the four items assumed.**

The four were written as separate questions about separate rules. They were answered as
one, because the diagnosis underneath them was the same: **the rules had multiplied past
what they were protecting.** Each was individually defensible and the set had become a
governance apparatus written before a single pixel was drawn — much of it there to keep cap
visibly distinct from CDMProbe rather than to make cap good.

**The decision: cap's mission is three statements, and everything else is downstream.**

- **a)** cap does not fight the secret restrictions. The gate/channel split already
  expresses this and is the one line worth enforcing in code.
- **b)** cap freely uses non-secret information to give good hints.
- **c)** cap does not try to *always* present a single best decision. That is distinct from
  "never present a single decision" and from "always present several options of equal
  status". Sometimes one option genuinely is best and the game hands us the data to say so
  — show it, without stress. Same for the inverse: sometimes nothing is good, and that is
  also a thing to show.

**What each item resolved to:**

- **D3 — narrow, and narrower than the item's own "narrow".** The broad reading was already
  dead: §3.3's primary/secondary step hints are a literal next-action answer. But the narrow
  reading's *"cap's output is a field"* framing was itself part of the problem — it is (c)
  overstated into a requirement. §3.1's third rule ("if exactly one thing is ever HIGH the
  tiering is wrong") is replaced by (c). §4's bullet is restated to the real anti-goal: cap
  does not reduce to a bare flag on the next button with no *why* and no *what else*. The
  Assisted Combat justification changes from "one answer where cap is a field" to **cap did
  not author it and cannot grade it** — which is the honest reason and survives the
  reframing.
- **D4 — the debate was hair-splitting and is dropped.** Its hypothetical (a hundred
  client-evaluated comparisons whose composite tells you what to press) is a strawman: if
  displaying available data clearly reads as an instruction, the UI has been fixed, which is
  (b). Legitimacy shrinks to (a) and stops being a veto with a test. No test for "defeats
  the intent" is sought, because the thing it was hunting is not a failure mode.
- **D5 — moot.** It asked for a threshold on the HIGH-at-once distribution. Under (c) there
  is nothing for a threshold to enforce. The distribution survives as a **reported
  statistic with no pass/fail** — the instrument for saying *why* something felt wrong in
  play, not a gate.
- **D6 — the cull went further than the item proposed.** Checks 2, 3, 8 and 9 are deleted
  outright rather than demoted to disclosures. Five survive, and every one is either schema
  integrity or principle (a): 1 coverage, 4 register legality, 5 declared subjects, 6's
  mechanical half (a cue declares polarity / its tier / a precondition — fields the renderer
  needs filled in; the "strict enough" judgement half goes), 7 estimate disclosure (it names
  the places cap guesses at a number the client would state exactly, which is (a)'s own
  to-do list).

**And the process change that came with it, which matters more than the cull.** The rules
were reverse-engineered from nothing. **Ship the tier/cue system, play with it, refine until
it feels good, then reverse-engineer the rules from that for the second spec.** Drawing
jumps the queue ahead of the documentation migration.

Reasoning: `notes.md` 2026-08-07 (second entry). Work: `backlog.md` → **the rule cull**.

### D1 — Can a channel select between BANDS, by driving alpha on two rendered treatments?

**Raised:** 2026-08-07 · **Struck:** 2026-08-07 — **decided, and then overtaken.**

**Decision:** *no* to the literal proposal — a channel may not select a band, and
channels stay out of band conditions entirely. Landed as `spec.md` §3.5's register
legality check.

But the item's real content was *"cross-ability facts should reach the player through
the client rather than through cap's arithmetic"*, and that **was** adopted, in a larger
form than D1 proposed: cues gained polarity, gained arbitrary subjects, and took over the
job windows were doing (D2). So D1's mechanism was rejected and its argument won.

Three things worth keeping from the analysis:

- **The route it proposed was a detour.** `Region:SetAlphaFromBoolean(v, aTrue, aFalse)`
  and `SetVertexColorFromBoolean` do the job in one call with less surface than the
  `C_CurveUtil.EvaluateColorValueFromBoolean` pair it sketched, and `SetVertexColorFromBoolean`
  needs one region rather than two stacked, which removes the combinatorial objection.
- **Its cost #2 was the decisive one and it is permanent.** A secret-driven rendering has
  no readback, so cap can never learn what appeared. Accepted rather than solved — see
  `notes.md` 2026-08-07 for why that is the right call.
- **Its claim to retire O2 was overstated at the time and then came true anyway.** O2
  needed the *window* to use an exact cooldown, which a channel could never do. Deleting
  windows retired it instead.

Reasoning: `notes.md` 2026-08-07. Spec: §3.1's two registers, §3.5's cue declaration.

### D2 — What problem does the window mechanic solve?

**Raised:** 2026-08-07 · **Struck:** 2026-08-07 — **answered, and the answer was that it
does not solve one.**

The item's own answer — *"a window is a budget for cross-ability reasoning"* — was
correct about what the mechanism **did** and wrong about whether it was needed. Its two
live sub-questions ("is six right?", "`opener` spends a slot on nothing") were both
symptoms of a mechanism nobody could size, and both dissolved with it.

What the analysis missed, and what decided it: **every window read something cap could
already see.** The budget therefore constrained *expression*, not capability, while
pushing authors toward cap's own arithmetic in exactly the places the client would have
answered exactly. `cores_dry` is the worked example — it needed a window because one
entry may not name another, not because the proc was unreadable.

**Decision:** windows deleted. Bands may name any declared ability through the gate
vocabulary; the guard against a priority ladder moves from syntax to the HIGH-at-once
measurement.

Reasoning: `notes.md` 2026-08-07. Spec: §3.5 "Entries, bands and cues". Work: the
Demonology catalog migration, `backlog.md` → `Now`.
