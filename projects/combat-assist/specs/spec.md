# Combat Assist Plus — spec

**What this file is for:** what the addon is supposed to do. The product
definition, not the implementation. If you're about to build something and this
file doesn't say what it should do, the answer is to write it here first (or ask),
not to infer it from the code.

---

## 1. What it is

`/cap` — **Combat Assist Plus**, an addon that makes Blizzard's Cooldown Manager
tell you more without telling you what to press.

Blizzard's position on combat addons is that they should not be decision engines.
The 12.0 restrictions are that position expressed as code: an addon can *display*
your combat state but can't read it back to reason about it. Rather than fight
that, cap treats it as the design brief. **cap presents information you already
have, differently.**

**Three principles. Everything else in this file is downstream of them:**

- **a)** **cap does not fight the secret restrictions.** The gate/channel split
  (§3.5) already expresses this, and it is the one line worth enforcing in code.
- **b)** **cap freely uses non-secret information to give good hints.** Whatever the
  client hands an addon in the clear is fair material, and using it well is the job.
- **c)** **cap does not try to *always* present a single best decision.** This is
  distinct from "never present a single decision" and from "always present several
  options of equal status". Sometimes one option genuinely is best and the game hands
  us the data to say so — show it. Same for the inverse: sometimes everything is on
  cooldown and nothing is good, and that is worth showing too.

Underneath them, three moves, in order of preference:

1. **Re-present.** Take something the game already tells you and put it where you
   can actually use it — the right place on screen, the right size, the right
   moment.
2. **Grade.** Turn a yes/no signal into a *how much*. Blizzard's proc glow says
   "this is available." cap says "this is available, and right now it's worth
   about this much." A dim thing and a bright thing are the same information with
   a decision half-made by your eyes instead of by a rules engine.
3. **Contextualise.** Show what a moment *is* — an opener, a burst window, a
   cooldown coming back — so the choice you make is informed rather than made for
   you.

The central expression of move 2 is the **tier signal** (§3.1): every ability cap
has an opinion about carries an emphasis level, several things can be emphasised
at once, and you pick. **How many are lit at any one moment is a property of the
spec and the situation, not a quota** — which is principle (c).

cap is **opinionated, not configurable**. You get recommendations derived from
your class and spec, chosen by us. It is deliberately not WeakAuras: there is no
trigger editor, no condition builder, no library of user-made packs. If cap's
opinion about your spec is wrong, the fix is to change cap's opinion, not to
expose a slider.

It **rides on the Cooldown Manager** rather than replacing it. The CDM already
knows what your spec cares about and already draws it legally. cap binds to it,
skins it, and extends past its edges where the icons are too small to carry what's
needed.

## 2. Who it's for, and when it runs

**For:** the author first, other people later. Defaults are chosen, not offered;
there is no settings panel in v1. Nothing is designed around strangers' UI setups,
but nothing is hardcoded so aggressively that publishing later becomes a rewrite.

**Specs:** one at a time, starting with **Demonology Warlock**. Each supported
spec gets its own catalog — the tiers it assigns, the procs it grades, the
sequences it recognises, the cooldowns it charts. **A spec without a catalog gets
nothing at all.** cap has no generic fallback and does not guess.

**Content:** everywhere, but built against the hard case. The game restricts what
addons can read specifically in combat, instances and PvP — which is exactly where
cap is meant to be useful. A feature that only works on a target dummy in a city
is not a shipped feature.

**Combat:** cap is a combat addon. Out of combat it should be quiet and mostly
invisible, apart from setup affordances — moving frames, and the target mode.

**Target mode:** single-target or AoE is **something you tell cap**, not something it
reads. The client does not hand an addon a target count, so the alternative to asking is
having no AoE opinion at all. It is one toggle, it is macroable so it can ride the same
key as the pull, it persists, and the panel says which mode is live. It is the only
opinion you set — everything else is chosen for you (§4).

## 3. What it does

Four features, plus the per-spec declaration all four read (§3.5). Each is a
separate deliverable and each is checkable in game.

### 3.0 The words

Used precisely throughout, and worth reading before the rest of §3.

**The signal**

| Term | Means |
| --- | --- |
| **Tier** | The answer for one ability: **HIGH / MEDIUM / LOW / none**. Is this usable, and does it matter? |
| **Band** | One rule line inside an entry — `when <condition> → HIGH`. First match wins. Bands are how a tier is *computed*. |
| **Treatment** | The look of a tier — its colour and styling. Plus one **hold** treatment, reserved for negative cues and belonging to no tier. |
| **Grade** | Continuous emphasis *within* a tier. Never changes the tier. |
| **Cue** | A marker on an icon or on a §3.4 bar, decided by cap *and* the client: cap evaluates the gate precondition that decides whether the cue is **offered**, the client evaluates the sealed channel that decides whether it **appears**. Carries **polarity** — positive (a reason to press) or negative (a reason to wait). Never changes the tier either. |
| **Register** | Which way an emphasis was computed — **graded** (cap reads it) or **cued** (the client reads it). |
| **Floor** | The ability to press when nothing is lit. |

**The catalog**

| Term | Means |
| --- | --- |
| **Catalog** | Everything one spec declares. No catalog, cap draws nothing. |
| **Roster** | The abilities in it. |
| **Entry** | One ability cap has an opinion about — its bands, its grade, its cues. |
| **Silence** | A tracked ability cap deliberately has no opinion about *pressing*, with a written reason. Every row is an entry or a silence. A silence is still nameable as a subject — a proc or a buff cap reads and never grades is a silence, not an absence. |
| **Sequence** | A named ordered step list with a trigger (§3.3). |
| **Subject** | The ability a term names. `this` is the entry's own; any declared ability is legal. |

**What a rule may look at**

| Term | Means |
| --- | --- |
| **Gate** | A quantity cap can read **and branch on**. Legal in a band. Three-valued — a refused read is *unknown*, and an unknown fails its band. |
| **Channel** | A quantity **only the client sees**. Legal in a grade or a cue, never in a band. Usually more exact than a gate. |
| **Gate precondition** | The band-legal condition on a cue, so it is only offered when it could mean something. |

**The plumbing**

| Term | Means |
| --- | --- |
| **Binding** | Matching catalog entries to live CDM rows, out of combat. |
| **CDM row** | One entry in Blizzard's Cooldown Manager. Which rows are *displayed* is a player setting. |
| **Mode** | `single` / `aoe`, set by the player (§2). |
| **Capture / stream** | The one way data leaves the addon — `wowkb.capture cap <stream>`. |
| **Gate health** | How often reads refused during a pull. |

**In one sentence:** a *catalog* holds *entries*; an entry's *bands* compute a *tier*
from *gates*; a *grade* and a *cue* decorate that tier without changing it; *channels*
are what only the client may see, and cues are how they reach the screen.

### 3.1 The tier signal

The core feature. Every CDM icon cap has an opinion about carries one of three
emphasis levels, recomputed continuously:

| Tier | Means | Demonology examples |
| --- | --- | --- |
| **HIGH** | worth pressing now | Dreadstalkers off cooldown · Tyrant off cooldown with the Dreadstalkers already out |
| **MEDIUM** | reasonable now | Hand of Gul'dan with the shards for it · Demonbolt with a proc · Implosion off cooldown |
| **LOW** | filler, or demoted — press it if nothing above it is lit | Shadow Bolt · Demonbolt on a proc you'd overcap on |
| *(none)* | cap has no opinion, or the answer is "not now" | — |

⚠ **A tier is computed only from quantities cap is allowed to branch on** — but it is
not always *drawn* by cap. "Implosion at 6+ imps" cannot be a computed tier: the stack
count is sealed, so no rule may test it. It is still **presented as HIGH**, and the
distinction is where the evaluation happens, not what the player sees:

- cap gates the cue on what it may read (`ready(this)`) and hands the threshold to the
  client;
- the client decides whether the number appears, from a count cap never learns;
- **the number is drawn in the HIGH treatment** — the same colour and styling as a HIGH
  icon.

So when the imps are there and the button is up, Implosion reads HIGH, and cap never
branched on the count to say so. **A positive cue is not a second visual language.** A
cue that means *press* is drawn in the treatment of the tier it stands for, so the player
is never asked to AND together two differently-styled signals to discover that something
is worth pressing — an emphasis that means HIGH looks like HIGH, whoever did the
arithmetic. (A **negative** cue is the deliberate exception, and is the subject of the
polarity paragraphs below.) This is what §5's constraint costs us: not the signal, only
the ability to *reason* about it.

Two rules define what a tier *is*, and they matter more than the tiers themselves:

- **Tiers describe value, not order.** Several abilities may sit at the same tier
  simultaneously, and that is the normal case, not a tie to be broken.
- **cap never ranks within a tier.** There is no "the best HIGH". If you want a
  single answer, cap is the wrong addon.

Both are statements about the vocabulary rather than quotas on the output. **How
many things are emphasised at once is whatever the spec and the moment are** — §1's
principle (c). cap does not try to *always* reduce to one answer, and where the data
genuinely says one thing is best, it says so.

Tiers come from the spec's catalog. No catalog, no tiers, nothing drawn.

**Check:** on Demonology in combat, confirm the emphasis moves as resources and
cooldowns change.

#### The visual vocabulary — two registers

Two registers, and the split is **who does the arithmetic**, not what the player
learns:

- **Graded** — the deciding quantity is one cap may read (resources, readiness,
  proc presence). Emphasis is **continuous**: brightness, colour and saturation
  move smoothly as the ability becomes more or less worth pressing. This is the
  tier's own register.
- **Cued** — the deciding quantity is **sealed**, so cap hands the comparison to
  the client and never learns the answer. What comes back is a marker beside the
  icon: a countdown, a count, a coloured pip. cap knows it *offered* the cue; it
  does not know what was drawn.

**The tier and the cue answer different questions, and that is the whole model.**

| | Answers | Computed by | Example |
| --- | --- | --- | --- |
| **Tier** | *Is this usable, and does it matter?* | cap, from gates | Dreadstalkers is off cooldown and it's a core cooldown → HIGH |
| **Cue** | *What about right now?* | the client, from sealed values | Tyrant is **within 8s** → a hold marker on Dreadstalkers meaning **wait** |

So a tier is a standing property of the ability plus its availability, and a cue is
the situation. Tiers are stable and few; cues are where the nuance lives.

**Cues carry polarity.** A **positive** cue adds a reason to press now and is drawn
in the treatment of the tier it stands for — a HIGH-meaning cue uses HIGH's colour
and styling. A **negative** cue is a reason to *wait*, and is drawn in a treatment
reserved for holding, distinct from every tier. Polarity must be unmistakable at a
glance: "press" and "hold" may never differ only in hue.

⚠ **A negative cue does ask the player to read two things at once, and that is
deliberate.** The alternative — folding the situation back into the tier — requires cap to
branch on quantities the client seals, which means substituting cap's own arithmetic
for the client's exact one. The cue is honest about what cap knows: it pipes a real
value through and lets your eyes do the joining. A lit button that grows a hold marker
when the situation arrives is a clearer statement than a button that silently went
dark.

*Why the two registers exist is a fact about the client, not about cap — see
`knowledge/addon-dev/security-taint-and-restricted-data.md` §4.8. That file is the
authority; this section only records the design consequence.*

### 3.2 Smart procs

Today a proc on the CDM is a large, uniform "PRESS ME." That's frustrating because
availability and *desirability* aren't the same thing: a Demonbolt proc that would
overcap your shards is being advertised at full volume when the right answer is to
wait.

Under §3.1 a proc is an **input to the tier**, not a signal of its own. So:

- cap **replaces** the stock proc treatment on the CDM rather than adding to it.
- A live proc raises its ability's tier; a live proc whose use would waste
  something does not. Demonbolt with a proc is MEDIUM; Demonbolt with a proc at
  high shards is demoted, because pressing it now throws away the shards it makes.
- Where the deciding quantity is continuous, so is the transition — a **fade, not
  a flip** (§3.1's graded register).
- A proc with no catalog entry gets the plain treatment, not a guess.

**Check:** on Demonology, sit at high shards with a Demonbolt proc up and confirm
the icon is visibly demoted; spend down to low shards and confirm it comes up.

### 3.3 Sequences

Guides describe openers and burst windows as ordered lists — do this, then this,
then this. In the moment, that knowledge is exactly the thing that evaporates.

Each supported spec gets a **catalog of named sequences** (opener, burst window,
execute, and so on). cap **detects when one applies on its own** — from combat
entry, from what you've cast, from the state it can legally observe — and while a
sequence is running it shows, on the CDM:

- a **primary hint** on the current step, and
- a **secondary hint** on the step after it, so you can pre-plan the next GCD
  rather than react to it.

Detection is fully automatic. There is no key to arm a sequence and no menu to
pick one — being asked to declare "I am now doing my opener" at the exact moment
you're opening defeats the purpose.

Because detection is automatic it will sometimes be wrong. What follows from that:

- **Losing the thread is silent and instant.** If what you actually cast leaves the
  sequence, cap drops it without complaint or correction. It never nags you back
  on script.
- **The sequence signal is layered over the tier signal, and reads differently
  from it.** The tier signal is always running; a sequence hint sits on top of it
  when a sequence is live. You must always be able to tell "this is a high-value
  press" from "you're three casts into your opener."
- Sequences are hints about *what comes next in a pattern you chose*, not
  instructions. They stop at the end of the sequence and don't resume.

**Check:** pull a dummy on Demonology, confirm the opener is recognised within the
first cast or two and that both hints advance in step; deliberately cast off-script
and confirm the hints vanish immediately and quietly.

### 3.4 Smart cooldowns

CDM icons are too small to carry a real timer, so this feature lives outside them.

cap draws a **free-floating, movable panel of duration bars** for the cooldowns
that matter on your spec. You place it once, wherever your eyes already are — it is
not tied to wherever the CDM happens to sit. It shows:

- a **clear, readable bar per important cooldown**, with the time remaining legible
  at a glance and in combat;
- **which cooldowns matter, chosen per spec** — a short curated list, not
  everything you own;
- **the same tier signal as §3.1, applied to the bars** — tier treatment, grade and cues,
  all one engine and two surfaces. A cooldown that is ready and HIGH is emphasised.
- **A reason to hold is a negative cue here too**, not a lower tier. A ready cooldown you
  should pool, align or save for a phase *is* ready, so the bar keeps its tier and the cue
  says *wait* — drawn in §3.1's hold treatment, which belongs to no tier.

⚠ **The bars are the roomier of the two surfaces.** A CDM icon is small; a bar is not, so
a cue that would crowd an icon can live here instead — see §6's cue-budget question.

**Check:** in combat, confirm every bar counts down accurately and legibly; confirm a
ready cooldown carrying a negative cue reads visibly differently from one that's ready to
fire, and that it reads as *hold* rather than as a demotion to a lower tier.

### 3.5 The catalog

The catalog is what a spec declares, and all four features above read it. It is
**data in a closed vocabulary, not code** — a catalog cannot express an arbitrary
computation, and the things it cannot express are the ones that would turn cap into
a rotation engine or into a Secret-Values violation.

Each supported spec has one, authored in `specs/<spec>/catalog.md` and transcribed
into the addon as a table. When the two disagree, which one is wrong depends on what
they disagree about:

- **What the client has** — spell ids, which rows exist, what the Cooldown Manager
  actually tracks. **The running game outranks both**, and a capture is how you ask it.
  A document that contradicts a live capture is the thing to fix, and it has happened.
- **What cap should do** — the tiers, the bands, the cues, the deliberate silences.
  **The document is normative**, and a table that has drifted from it is wrong. This
  half is not a formality: a tier edited in the table because it felt better in play,
  and never argued in the document, is how the catalog becomes a rotation engine one
  commit at a time.

#### What a catalog declares

| | Declares | Feeds |
| --- | --- | --- |
| **Applies-to** | the spec, and any hero tree or talent the catalog assumes | binding (§2) |
| **Roster** | the abilities cap has an opinion about — base spell, known transforms, and whether the ability earns a cooldown bar | §3.1, §3.4 |
| **Entries** | per ability: its tier bands, its grade, its cues | §3.1, §3.2, §3.4 |
| **Silence** | the abilities cap deliberately has no opinion about, each with a reason | §3.1 |
| **Sequences** | named ordered step lists with an entry trigger | §3.3 |

#### Entries, bands and cues

An **entry** is one ability. It declares **bands** — `when <condition> → HIGH |
MEDIUM | LOW` — the first band whose condition holds sets the tier, and an ability
matching no band has no tier. Every entry is evaluated independently, every
recompute.

Three rules govern what a band may say, and only one of them is a restriction:

- **A band may name any ability the catalog declares**, plus the spec's resources
  and player buffs — but only through the **gate** vocabulary below, which is the
  closed set of quantities cap may read *and* branch on. Naming a subject is how a
  band says "the cores are dry" without cap inventing arithmetic to get there.
- **A verdict is never an input.** There is no syntax for "another ability's tier", and
  there will not be one. It is enforced by construction — the vocabulary has no term for
  it — and what it prevents is the *cheapest* form of a priority ladder: an entry demoting
  itself because another entry came out HIGH. It does not prevent a ladder assembled out
  of gates, and it must not be read as if it did.
- **Negation is legal.** `not <term>` may appear in a band condition, on any subject. A
  proc is a self-contained readable signal and "no core is lit" is a real fact about the
  fight rather than an ordering trick, so refusing negation bought nothing and cost
  expressiveness. **Prefer a negative cue** where the reason is *wait rather than press* —
  it is more informative and it can rest on a sealed quantity — but a negating band is
  available and is not a defect.

⚠ **What the vocabulary rules out is narrow, and worth stating plainly.** It has no term
for another entry's verdict, and that is the whole of it. A band may name any declared
ability and may negate, which is expressive enough to write an ordering if an author sets
out to — nothing in the grammar stops that, and nothing is meant to. Authoring the catalog
well is what keeps it a field of values rather than a list.

A **grade** modulates emphasis continuously *within* a band; it never changes the
band. A **cue** is a marker on an icon or on a §3.4 bar; it never changes the band either.
Neither may be laundered into a tier.

A cue declares:

- **its polarity** — positive (a reason to press) or negative (a reason to wait);
- **the tier it stands for**, if positive, and is drawn in that tier's treatment
  (§3.1). A negative cue stands for no tier and uses the hold treatment;
- **a gate precondition** — a band-legal condition cap evaluates itself, so the cue
  is only offered when it could be meaningful;
- **the channel** the client evaluates to decide whether it actually appears.

The two compose without cap ever seeing the sealed quantity:

> Implosion's cue is `ready(this)` → `stacks(Wild Imp) ≥ 6` → **positive, HIGH**. cap
> tests readiness, the client tests the count, and what the player sees is a
> HIGH-styled number that means *press this now*.
>
> Dreadstalkers' cue is `ready(this)` → `cooldownRemaining(Summon Demonic Tyrant) ≤ 8` →
> **negative**. cap tests its own readiness, the client tests how far out Tyrant is, and
> what the player sees is a lit button that grows a hold-styled marker only in the last
> few seconds before the window — which is the stretch where holding is right.

⚠ **The threshold is the cue.** Un-thresholded, `cooldownRemaining(Summon Demonic Tyrant)`
draws *hold* at 45 s remaining as readily as at 5, and 45 s out is precisely when
Dreadstalkers should be pressed. A negative cue whose channel is a bare countdown is a
permanent cue wearing a number, and **check 4 below refuses it**: a negative cue's channel
must be one of the thresholded forms.

⚠ **A cue's polarity and tier are claims about what the player sees, and they are not
free.** Every cue should carry a gate precondition strict enough that it is not simply lit
all the time — a permanent cue of either polarity is noise. Check 4 asks only that a
precondition is *present*; whether it is strict enough is an authoring judgement, made here
and argued in the catalog document.

#### The vocabulary is closed, and split by what the client allows

Two columns. Which column a quantity sits in is a fact about the client, not a
choice — see `knowledge/addon-dev/security-taint-and-restricted-data.md` §4.8 and
`cooldown-manager.md`.

**A subject is `this` or any ability the catalog declares.** `this` is shorthand for the
entry's own ability and carries no special privilege. **Not every term takes a subject:**
`resource` and `combat` describe the pull rather than an ability, and `mode(x)`'s argument
is a literal — `single` or `aoe` — not a subject at all. `elapsed` is the one term
restricted to `this`.

**Gates — cap may branch on these, so they may appear in a band condition:**

| Term | Is |
| --- | --- |
| `resource` *(no subject)* | the spec's secondary resource — Soul Shards, Combo Points, Holy Power and their siblings. These are the ones never sealed; a **primary** resource is, and is not a gate |
| `affordable(x)` | can I pay for this right now — the client's verdict, not a cost table |
| `ready(x)` | off cooldown, from the out-of-combat baseline plus observed readiness edges |
| `elapsed(this) > t` | cap's **own arithmetic**, stamped off the `OnCooldown` alert edge, and **restricted to the entry's own ability**: an entry may estimate about itself and about nothing else. An estimate, and an entry using one says so (check 5). **Prefer a cue** wherever the client will evaluate the same fact exactly |
| `proc(x)` | the spell-activation overlay is lit |
| `identity(x)` | which spell a row currently *is*, when the ability transforms |
| `auraUp(x)` | a tracked row has a live bound aura — presence only |
| `talent(x)` | resolved out of combat at bind time. Its argument is a **talent**, which need not have a CDM row and so need not be an entry or a silence — check 3 exempts it |
| `combat` *(no subject)* | a pull is running |
| `mode(x)` | the target mode **you** set. The argument is the literal `single` or `aoe`, not a subject. Not a game read at all: it is cap's own state, so it is always readable and always branchable. §4's answer to a count the client will not give us |

⚠ **"How many casts so far" is not a gate.** A count of rotational presses since combat
entry is a *position in an order*, and a band testing it writes an opener: `casts == 0 →
HIGH` on one ability and `casts == 1 → HIGH` on the next is a literal ordered list, which
duplicates §3.3 and breaches §4. It exists only as **sequence-trigger vocabulary** (below),
where being an ordered list is the point.

**Channels — cap never sees the value; it hands it to the client to draw. These may
appear in a grade or a cue and NEVER in a band condition:**

| Term | Draws | Is |
| --- | --- | --- |
| `cooldownRemaining(x)` | countdown | time left on a cooldown, evaluated inside the client. **Exact**: cap never counts down from a declared base cooldown |
| `cooldownRemaining(x) ≤ t` | marker | the same value compared against a threshold inside the client. What comes back is a marker that appears or does not; cap learns neither the value nor which side of *t* it fell |
| `auraRemaining(x)` | countdown | the same for a live bound aura — §3.4's bars, and the route to "the pets are out" where the summon's row carries a duration |
| `auraRemaining(x) ≤ t` | marker | the thresholded form — *this is about to fall off* |
| `stacks(x) ≥ n` | count | an aura's stack count, quantised by the client |
| `active(x)` | pip | a sealed boolean off a duration object — live / not live. Drives a treatment, never a branch |

⚠ **Both forms exist because they answer different questions.** The thresholded form is
what a cue wants — an edge, arriving when the situation does. The bare countdown is what
§3.4's bars want — the number itself, drawn continuously. Neither is the other's fallback.

⚠ **The thresholded forms rest on a measured client mechanism, and the measurement is not
in this file.** The threshold edge lands exactly on *t* rather than somewhere near it, and
the evaluation result is sealed even when nothing cap supplied was — so cap hands the
comparison over and never learns the answer, which is the property that makes this legal at
all. `knowledge/addon-dev/security-taint-and-restricted-data.md` §4.8.1 is the authority.

⚠ **A channel is not weaker than a gate — it is usually stronger.** A gate is what
cap can see; a channel is what the client can see, which is more, and exactly. Where
both could express a fact, **the channel is the correct choice** and the gate is the
fallback. The `elapsed` arithmetic in the gate column is the one place cap guesses at a
number the client would state, and every use of it is a candidate for deletion.

**Adding a term is a spec change.** A new gate means establishing the client fact
first — that the quantity is readable *and* branchable in restricted combat — writing
it into `knowledge/addon-dev/`, and adding a row here. A catalog that reaches for a
quantity not in this table does not load.

**What a sequence trigger may name.** A sequence's `enter:` is **a band-legal condition** —
the gate vocabulary above, negation included — plus `casts == n`, which is legal here and
nowhere else. The asymmetry is the point: a sequence *is* an ordered list the player opted
into by starting it, so "before the first cast" is a legitimate entry condition there and a
rotation engine everywhere else. A trigger naming a channel, or naming a term outside this
set, does not load. Everything else about sequences — the steps, the hints, the silent drop
— is §3.3.

#### A gate is three-valued

A read can refuse. When it does the gate is *unknown*, not false — and a band naming
an unknown gate **fails** it, so the entry demotes rather than quietly asserting that
the situation is absent. A term whose value **after negation** is known false settles the
band whatever else refuses. This is why a blind cap looks quiet rather than confident, and
the refusal rate is reported as gate health.

⚠ **Negation does not rescue an unknown.** `not <term>` on an unknown term is *unknown*,
not true — a refused read is not evidence that the situation is absent, which is the whole
point of the third value. "Unknown fails the band" is a rule about the band, so it holds
however the term is written. Getting this wrong is the one way a blind cap reads confident.

⚠ **A cue's gate precondition is a band-legal condition and behaves as one.** If a term in
it reads *unknown*, the precondition does not hold and the cue is **withheld** — the same
answer a band gives, for the same reason. This matters now that a precondition may name an
ability other than `this`, which is a subject that can go unreadable on its own.

⚠ **Cues have no equivalent on the channel side, by construction.** The client always picks a branch, so
a cue driven by a refused read is not detectably wrong — it is simply drawn from
whatever the client saw. cap logs that a cue was **offered**; it never learns what
appeared. That is accepted: the thing being verified is whether the hint pointed the
player right, which is answered by playing, not by a log.

#### A row the player has hidden is not the same as a row that does not exist

The Cooldown Manager's tracked set is **user-configurable**. A spec's full row list comes
from game data, but which of those rows the player has displayed is a setting — including
rows the game data itself ships switched off, which the player can turn on. What the
player may and may not rearrange is a client fact and lives in
`knowledge/addon-dev/cooldown-manager.md` §1; cap assumes nothing about it beyond "a row
that exists in the data may or may not be on screen".

So a catalog entry or cue may depend on a row that exists for the spec and is simply
switched off. cap must tell these apart:

- **Not in the spec's data** — the ability is not part of this spec's tracked set. The
  entry is dropped; nothing is owed.
- **In the data, not displayed** — the row exists and the player could enable it. The
  entry is still dropped in play, but the capture log says **"available, not
  displayed"** and names the row, because that is a thing the player can fix and a
  silent drop reads as a bug in cap.

**This applies to bands as much as to cues**, and that is a consequence of a band being
able to name a subject other than `this`. A term naming a subject that is dropped,
untalented, or present in the data but not displayed reads **unknown** — so its band fails
and the entry demotes, exactly as any other refused read does. It never reads *false*,
because "the situation is absent" and "cap cannot see the situation" are different
statements and only one of them is true. The log line names the row for a band's subject
just as it does for a cue's, so an entry that quietly lost a band is visible.

A cue that rests on a hidden row remains the sharpest case: it will simply never appear,
with no other symptom at all.

#### Silence is a declaration, not an absence

cap can enumerate what the Cooldown Manager tracks for the current spec. Every
tracked row must appear in the catalog as either an **entry** or a **silence** with a
one-line reason. A row in neither is an authoring defect and the capture log
(`wowkb.capture cap <stream>`) names it. An omission is a decision or it is a bug;
there is no third state.

**No catalog, nothing at all.** Binding happens out of combat, at load and on spec,
talent or hero-tree change. If no catalog claims the current spec — or the catalog's
applies-to does not match the build — cap draws nothing, alters no CDM pixel, and
**says nothing at all**: the reason goes to the capture log and nowhere else. An
individual **entry** whose ability is not talented, or has no CDM row, is dropped the
same way: silently in play, visibly in the capture log.

Silence rather than a chat line, because a warning is only worth its cost if it fires
when it matters, and cap cannot promise that. The one state a player could act on —
the Cooldown Manager switched off in Options — raises **none** of the events cap
listens to, so it would be quiet exactly there; and "this spec has no catalog" is a
permanent property of the build, which a line at every login turns into noise. A
developer reading the log is the audience that can use the message.

#### The checks a catalog must pass

A check earns its place only if it is **schema integrity** or **principle (a)**. There are
five. They run at load and are reported to the capture log.

1. **Coverage** — every CDM-tracked row is an entry or a declared silence. ⚠ "Tracked"
   means **the rows cap actually binds**, not the spec's wider candidate set: a row that
   exists in the data and is not displayed is the "available, not displayed" state above,
   not a coverage failure.
2. **Register legality** — no channel term appears in a band condition, and no gate term
   drives a cue's channel. A cue's gate precondition is band-legal and is checked as one.
   **This is principle (a) in code, and it is the most important line in this file**: it
   is the one place where "cap may display it but may not reason about it" stops being an
   intention and becomes something a catalog can fail on.
3. **Declared subjects** — every subject named by a band, a grade or a cue is an ability
   this catalog declares as an entry or a silence. A term naming an ability the catalog
   has no opinion about is an authoring defect. Two exemptions, both because the argument
   is not a subject: the subject-less terms (`resource`, `combat`) and `mode(x)`'s literal
   are not checked, and **`talent(x)`'s argument is exempt** — a talent may be a passive
   with no CDM row, so it can be neither an entry nor a silence, and checking it would
   make the one gate whose whole purpose is talents an authoring defect.
4. **Cue schema** — every cue declares its polarity, a positive cue declares the tier it
   is drawn in, every cue carries a gate precondition, and a **negative** cue's channel is
   one of the thresholded forms (`… ≤ t`). These are the fields the renderer needs in
   order to draw anything at all; an un-thresholded negative cue is a permanent marker
   wearing a number. Whether a precondition is *strict enough* is authoring judgement and
   is not checked.
5. **Estimate disclosure** — every band using `elapsed` is flagged in the load report,
   with the channel that would replace it if one exists. Not a failure — it cannot fail,
   and that is fine. It is a standing list of the places cap is guessing where the client
   would answer exactly, which is (a)'s own to-do list.

And one measurement, which is not a check and has no pass/fail: cap samples **how many
entries are HIGH at once** through a pull and reports the distribution. It is the
instrument for explaining *why* a moment felt wrong in play — read it after playing, next
to what you actually felt. It is not a gate, and no number in it is a failure.

**Check:** on a spec with no catalog, confirm cap is completely inert and that the
capture log says why; on Demonology, confirm the log lists every tracked row as graded
or silent with nothing left over.

## 4. What it explicitly does NOT do

- **It does not press anything.** No automation, no queuing, no macro generation,
  no action taken on your behalf. cap only ever changes what is on your screen.
- **It does not reduce to a bare flag on the next button.** An indicator that says
  *press this* with no **why** and no **what else** is the thing cap is not: whatever
  emphasis is on screen carries the reason it is there and what it is standing next to.
  cap does answer "what comes next" where §3.3's sequence hints apply — but that is a
  named pattern with its steps visible, which is the opposite of a bare flag.
- **It does not surface Blizzard's Assisted Combat recommendation.** **cap did not
  author it and cannot grade it.** It is an opaque verdict produced by rules cap did not
  write, so §1's grade and contextualise moves are unavailable on it, and re-presenting it
  means shipping someone else's opinion as ours. On Demonology the list also drops **Implosion**, a real
  rotational press, and is single-target only with no burst planning — but the list
  is not as thin as it first looks, because most of what it appears to omit is not on
  the Midnight spec at all.
- **It is not configurable in the WeakAuras sense.** No trigger editor, no user
  packs, no per-ability toggles. You may move frames and set the target mode; you may
  not rewrite the opinion. The target mode is not an exception to this — it is an input
  the client refuses to give us, not a preference.
- **It does not replace the Cooldown Manager.** cap needs the CDM enabled and
  configured. It ships no layout, chooses nothing about what's tracked, and does
  nothing useful if the CDM is off.
- **It does not cover every spec.** Only specs with a catalog. Others get nothing,
  visibly and deliberately.
- **It does not do keybinds or action-bar layout.** That's BucketBinds
  (`projects/keybinder/`).
- **Retail / Midnight only.** No Classic.

### The Cooldown HUD boundary — cap supersedes it

**Combat Assist Plus replaces Cooldown HUD (`projects/cooldown-hud/`, CDMProbe).**
The HUD grew into a next-action decision engine, which is the thing this project is
deliberately not. Its measured facts about the client already live in
`knowledge/addon-dev/` and stay authoritative; its per-spec rotation research is
worth harvesting into catalogs; its *code* is not carried over. There is one addon
riding the CDM going forward and it's this one.

## 5. Constraints

Two are fixed by the platform, and both shape the design more than anything in §3:

- **Secret Values (12.0).** Many combat values are unreadable to addons — cap can
  display them but cannot reason about them. Every tier in §3.1 has to survive
  that: either the deciding quantity is one we're allowed to read, or the emphasis
  is driven by that quantity without cap ever seeing it. This is what produces
  §3.1's two visual registers. What's readable, and the sanctioned routes for
  showing what isn't, live in `knowledge/addon-dev/` — that KB is the authority,
  not this file.
- **Combat lockdown.** Secure-frame changes are blocked in combat. cap only *shows*
  things, which keeps it on the right side of this — but frame setup, binding and
  placement all have to happen before the pull.

A third is self-imposed and matters just as much:

- **Legitimacy — §1's principle (a).** cap does not fight the secret restrictions; it
  works inside them. The gate/channel split is that principle expressed in code, and
  §3.5's register-legality check is the one place it is enforced rather than intended.

House rules for the code itself:
`.claude/skills/wow-developer/references/house-rules.md`. cap starts from a clean
slate — no code is ported from CDMProbe.

## 6. Open questions

- **Are three tiers enough?** HIGH / MEDIUM / LOW is the starting vocabulary. A
  fourth level, or a per-tier intensity within the graded register, may turn out to
  be needed — decide it against a built Demonology catalog, not in advance.
- **What is a cue budget, and does an icon need one?** Cues carry the whole of the
  situational nuance, and nothing caps how many an entry may declare or how many can be
  lit at once. A CDM icon is small; §3.4 exists because it is too small to carry a timer.
  Likely answers: a per-entry limit, a rule that cross-ability cues live on the §3.4 bars
  rather than the icons, or both. Decide it against a drawn catalog.
- **How is polarity drawn?** A negative cue must read as *hold* at a glance and must not
  be mistakable for any tier. Whether that is a colour, a shape, a position, or a
  treatment on the icon itself is unresolved and is a visual-design question, not a
  vocabulary one.
- **How much does a demoted ability show?** A demoted Demonbolt should be visibly
  less urgent, but it must not become invisible — losing the proc entirely is worse
  than an over-loud one. The floor is a design question, not a technical one.
- **What does cap show when the right answer has no icon?** Open in general, but
  **not on Demonology** — the filler is tracked there after all (Shadow Bolt is an
  Essential row, with Infernal Bolt riding it as an override), so LOW has something to
  draw on and the floor is graded like anything else. The question survives for a spec
  whose floor genuinely has no row: either "nothing is lit" is taught to mean *go
  build*, or cap draws its own icon for an ability the CDM does not track — which is
  new surface, and a different addon from one that rides the CDM.
- **Second spec.** Demonology first is settled; what follows isn't. Choose it for
  what stresses the design differently, not for what's easiest. ⚠ A spec whose resource
  is **primary** (Fury, Energy, Mana…) cannot use the graded register at all — the value
  is always secret and `IsSpellUsable` is binary. Havoc looks cheap because Fury rarely
  gates the rotation in play, but "the bar is unreadable" and "the bar rarely matters"
  are different facts, and only the second is spec-specific.
- **Prior art.** A `/mine-addon` pass is worth doing once §3's behaviours are
  concrete — especially for how shipping addons handle graded emphasis under the
  12.0 restrictions.

## Milestones

Ordered so the thing worth having arrives early: foundation, then the tier signal,
then the surfaces that reuse it.

| # | Milestone | Status |
| --- | --- | --- |
| M0 | Scaffold — repo, `.toc`, `/cap` router, registered in `wowkb.addon` | ✅ 2026-08-05 |
| M1 | Spec §1–§5 written | ✅ 2026-08-05 |
| M2 | Foundation — bind to the CDM, the movable frame, nothing drawn yet | ✅ 2026-08-06, flown |
| M2a | Lab the four client claims M2 rests on, and fly the lab | ✅ 2026-08-06 |
| M2b | Strip cap's diagnostic surface — client behaviour is a lab question | ✅ 2026-08-06 |
| M2c | The standard capture log (`ns.Capture` → `wowkb.capture cap`) | ✅ 2026-08-06 |
| M2d | Fly cap and read the log — M2's real acceptance | ✅ 2026-08-06 |
| MC | §3.5 the catalog format, and Demonology's | ✅ 2026-08-05 |
| M3 | §3.1 the tier signal + §3.2 procs, on the Demonology catalog | — |
| M3a | Lab the client claims M3 rests on; the pure core | ✅ 2026-08-07 |
| M3b | The gates read and the tiers computed, nothing drawn | — |
| M3c | §3.1's graded register — cap's own overlay | — |
| M3d | §3.1's threshold register — the Implosion cue | — |
| M3e | §3.2 procs, and the honesty measurement | — |
| M4 | §3.4 smart cooldowns — bars, then the tier signal applied to them | — |
| M5 | §3.3 sequences (Demonology catalog) | — |
