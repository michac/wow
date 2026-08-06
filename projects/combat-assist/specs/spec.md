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
have, differently — and narrows decisions instead of making them.**

Concretely, that means three moves, in order of preference:

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
at once, and you pick. That is the difference between narrowing a decision and
making one, and it is the line the whole design is built along.

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
invisible, apart from setup affordances — moving frames, checking status.

## 3. What it does

Four features, plus the per-spec declaration all four read (§3.5). Each is a
separate deliverable and each is checkable in game.

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
branched on the count to say so. **A threshold cue is not a second visual language.**
The player must never be asked to AND together two differently-styled signals to
discover that something is worth pressing — an emphasis that means HIGH looks like
HIGH, whoever did the arithmetic. This is what §5's constraint costs us: not the
signal, only the ability to *reason* about it.

Three rules define what this is, and they matter more than the tiers themselves:

- **Tiers describe value, not order.** Several abilities may sit at the same tier
  simultaneously, and that is the normal case, not a tie to be broken.
- **cap never ranks within a tier.** There is no "the best HIGH". If you want a
  single answer, cap is the wrong addon.
- **If exactly one thing is ever HIGH, the tiering is wrong.** That's a rotation
  engine wearing a hat, and it fails §1. A tier design that collapses to one
  answer per GCD should be redesigned, not shipped.

Tiers come from the spec's catalog. No catalog, no tiers, nothing drawn.

**Check:** on Demonology in combat, confirm the emphasis moves as resources and
cooldowns change; confirm that at a typical mid-rotation moment **more than one**
ability is emphasised.

#### The visual vocabulary — two registers

What the platform allows splits cap's emphasis into two kinds, and the split is a
product constraint, not an implementation detail:

- **Graded** — where the deciding quantity is one cap may read, or may hand to the
  engine to evaluate on its behalf (resources, cooldown remaining, proc presence),
  emphasis is **continuous**. Brightness, colour and saturation move smoothly as
  the ability becomes more or less worth pressing. This is the default register.
- **Threshold text** — where the deciding quantity is an **aura stack count**, no
  continuous channel exists at all. The only thing the platform will show is text.
  So the cue is a **glowing number that appears at the threshold**: nothing below
  it, a lit count at and above it.

Threshold cues are therefore **binary, and that is accepted** — an appearing glow
is plenty of signal. Do not contort the design to make a stack count fade.

**The two registers differ in resolution, never in vocabulary.** A cue is drawn in the
**tier treatment it stands for** — a cue that means HIGH uses the HIGH colour and
styling, identical to a HIGH icon. The registers are two ways of *computing* an
emphasis, not two ways of *reading* one, and the player is never asked to learn a
second language or to AND two differently-styled signals together. The only thing the
threshold register gives up is the smooth ramp: it arrives at full strength instead of
fading in.

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
- **the same tier signal as §3.1, applied to the bars.** A cooldown that is ready
  and HIGH is emphasised; one that is ready but should be held — pooling, waiting
  for an alignment, saved for a phase — is not. One engine, two surfaces.

**Check:** in combat, confirm every bar counts down accurately and legibly;
confirm a held cooldown reads visibly differently from one that's ready to fire.

### 3.5 The catalog

The catalog is what a spec declares, and all four features above read it. It is
**data in a closed vocabulary, not code** — a catalog cannot express an arbitrary
computation, and the things it cannot express are the ones that would turn cap into
a rotation engine or into a Secret-Values violation.

Each supported spec has one, authored in `specs/<spec>/catalog.md` and transcribed
into the addon as a table. **The document is normative**: if the table and the
document disagree, the table is wrong.

#### What a catalog declares

| | Declares | Feeds |
| --- | --- | --- |
| **Applies-to** | the spec, and any hero tree or talent the catalog assumes | binding (§2) |
| **Roster** | the abilities cap has an opinion about — base spell, known transforms, and whether the ability earns a cooldown bar | §3.1, §3.4 |
| **Windows** | named fight situations, at most six, each defined once | shared context |
| **Entries** | per ability: its tier bands, its grade, its cues | §3.1, §3.2, §3.4 |
| **Silence** | the abilities cap deliberately has no opinion about, each with a reason | §3.1 |
| **Sequences** | named ordered step lists with an entry trigger | §3.3 |

#### Entries, and why they cannot see each other

An **entry** is one ability. It declares **bands** — `when <condition> → HIGH |
MEDIUM | LOW` — evaluated for that ability alone; the first band whose condition
holds sets the tier, and an ability matching no band has no tier. Every entry is
evaluated independently, every recompute.

Three restrictions do the work:

- **An entry's condition may name only its own ability, the spec's resources and
  player buffs, and windows.** There is no syntax for "another ability's tier" and
  none for "another ability is ready". Mutual exclusion — the thing a priority list
  is made of — is therefore not expressible between entries at all. (A buff you are
  carrying is state, like a resource; the restriction exists to stop an entry
  reasoning about *what else you could press*.)
- **Band conditions are positive.** No negation. An ability that should be held is
  not held by saying "not X"; it is *promoted* in the situations where pressing it is
  right, and falls to its lower band everywhere else. This forces the author to name
  the situation instead of encoding an order.
- **Cross-ability reasoning happens only in a window, and a window is named after a
  situation in the fight** — "the Tyrant setup", "cores are dry" — never after a rank.
  Windows are where negation is legal, they are few, and they are the reviewable
  surface. The cap of six is deliberate: a priority ladder re-encoded as windows runs
  out of room.

A **grade** modulates emphasis continuously *within* a band; it never changes the
band. It may be driven by a channel or by a readable gate quantity — the difference
is only who does the arithmetic. A **cue** is a threshold marker drawn beside the
icon; it never changes the band either, and it may be driven by a channel alone.
Both are §3.1's graded and threshold registers, and neither is allowed to be
laundered into a tier.

A cue declares **the tier it stands for**, and is drawn in that tier's treatment
(§3.1). It may also declare a **gate precondition** — a band-legal condition cap
evaluates itself — so that the cue is only offered to the client when it could be
meaningful; the channel threshold then decides whether it actually appears. The two
compose without cap ever seeing the sealed quantity:

> Implosion's cue is `ready(this)` → `stacks(Wild Imp) ≥ 6` → **HIGH**. cap tests
> readiness, the client tests the count, and what the player sees is a HIGH-styled
> number that means *press this now*.

⚠ **A cue's tier is a claim about what the player sees, and it is not free.** A cue
declared HIGH counts as a HIGH-capable entry for the breadth check below, and it must
carry a gate precondition strict enough that the cue is not simply lit all the time —
a permanent HIGH is the same failure as a HIGH that never fires.

#### The vocabulary is closed, and split by what the client allows

Two columns. Which column a quantity sits in is a fact about the client, not a
choice — see `knowledge/addon-dev/security-taint-and-restricted-data.md` §4.8 and
`cooldown-manager.md`.

**Gates — cap may branch on these, so they may appear in a band condition:**

| Term | Is |
| --- | --- |
| `resource` | the spec's secondary resource — Soul Shards, Combo Points, Holy Power and their siblings. These are the ones never sealed; a **primary** resource is, and is not a gate |
| `affordable(this)` | can I pay for this right now — the client's verdict, not a cost table |
| `ready(this)` | off cooldown, from the out-of-combat baseline plus observed readiness edges |
| `elapsed(this) > t` | cap's **own arithmetic** over its own observation of its own cast, against a base cooldown read out of combat. An estimate, and an entry using one says so |
| `proc(this)` | the spell-activation overlay is lit on this ability |
| `identity(this)` | which spell this row currently *is*, when the ability transforms |
| `auraUp(x)` | a tracked row has a live bound aura — presence only |
| `talent(x)` | resolved out of combat at bind time |
| `window(x)` | a window this catalog declared |

**Channels — cap never sees the value; it hands it to the client to draw. These may
appear in a grade or a cue and NEVER in a band condition:**

| Term | Register | Is |
| --- | --- | --- |
| `cooldownRemaining(this)` | graded | time left, evaluated against our curve inside the client |
| `auraRemaining(x)` | graded | the same for a tracked aura — §3.4's bars |
| `stacks(x) ≥ n` | threshold text | an aura's stack count, quantised by the client. **The only thing a stack count may ever drive** |

**Adding a term is a spec change.** A new gate means establishing the client fact
first — that the quantity is readable *and* branchable in restricted combat — writing
it into `knowledge/addon-dev/`, and adding a row here. A catalog that reaches for a
quantity not in this table does not load.

#### Silence is a declaration, not an absence

cap can enumerate what the Cooldown Manager tracks for the current spec. Every
tracked row must appear in the catalog as either an **entry** or a **silence** with a
one-line reason. A row in neither is an authoring defect and `/cap status` names it.
An omission is a decision or it is a bug; there is no third state.

**No catalog, nothing at all.** Binding happens out of combat, at load and on spec,
talent or hero-tree change. If no catalog claims the current spec — or the catalog's
applies-to does not match the build — cap draws nothing, alters no CDM pixel, and
says so plainly once. An individual **entry** whose ability is not talented, or has
no CDM row, is dropped the same way: silently in play, visibly in `/cap status`.

#### The checks a catalog must pass

These are the enforceable form of §3.1's three rules. They run at load and are
reported by `/cap status`.

1. **Coverage** — every CDM-tracked row is an entry or a declared silence.
2. **Breadth** — at least three entries are HIGH-capable, counting both HIGH bands and
   HIGH-declaring cues. A catalog where one ability owns HIGH is a ranked list with
   extra steps.
3. **No verdicts as inputs** — no condition references another entry's tier. Enforced
   by construction: the vocabulary has no term for it.
4. **Register legality** — no channel term appears in a band condition, and no cue's
   *threshold* is anything but a stack count. A cue's gate precondition is band-legal
   and is checked as one.
5. **Cue honesty** — every cue declares the tier it is drawn in, and a HIGH cue carries
   a gate precondition. A HIGH-styled marker with nothing gating it is permanently lit,
   which reads as "always press this" and fails §3.1 as surely as a bare HIGH band would.
6. **A named floor** — the catalog names the ability to press when nothing is lit,
   even when that ability has no CDM row to draw on. Where it has none, "the field is
   dark" is a *stated* meaning rather than a bug.

And one measurement, which is the honest form of the third rule: cap samples **how
many entries are HIGH at once** through a pull and reports the distribution. A
catalog that is usually at exactly one HIGH has failed §3.1 regardless of passing
every check above.

**Check:** on a spec with no catalog, confirm cap is completely inert and says why;
on Demonology, confirm `/cap status` lists every tracked row as graded or silent with
nothing left over.

## 4. What it explicitly does NOT do

- **It does not press anything.** No automation, no queuing, no macro generation,
  no action taken on your behalf. cap only ever changes what is on your screen.
- **It does not answer "what do I press next".** No single next-action indicator,
  not cap's own and not Blizzard's relocated. The tier signal is deliberately a
  *field* of emphasis, and §3.1's three rules are the enforceable form of this.
- **It does not surface Blizzard's Assisted Combat recommendation.** It is one
  answer where cap is a field, which is reason enough on its own; the shape is the
  objection, not the quality. On Demonology the list also drops **Implosion**, a real
  rotational press, and is single-target only with no burst planning — but the list
  is not as thin as it first looks, because most of what it appears to omit is not on
  the Midnight spec at all.
- **It is not configurable in the WeakAuras sense.** No trigger editor, no user
  packs, no per-ability toggles. You may move frames; you may not rewrite the
  opinion.
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

- **Legitimacy.** cap should be something Blizzard would recognise as playing
  along. If a feature only works by defeating a restriction rather than working
  within it, it isn't a cap feature — regardless of whether it's technically
  possible.

House rules for the code itself:
`.claude/skills/wow-developer/references/house-rules.md`. cap starts from a clean
slate — no code is ported from CDMProbe.

## 6. Open questions

- **Are three tiers enough?** HIGH / MEDIUM / LOW is the starting vocabulary. A
  fourth level, or a per-tier intensity within the graded register, may turn out to
  be needed — decide it against a built Demonology catalog, not in advance.
- **Does the tier signal stay honest under pressure?** §3.1's third rule is the
  one at risk: a catalog author under pressure to be *useful* will drift toward one
  HIGH per GCD. Worth an explicit check once Demonology is playable — measure how
  often more than one ability is emphasised.
- **How much does a demoted ability show?** A demoted Demonbolt should be visibly
  less urgent, but it must not become invisible — losing the proc entirely is worse
  than an over-loud one. The floor is a design question, not a technical one.
- **What does cap show when the right answer has no icon?** Demonology's filler —
  Shadow Bolt, and Infernal Bolt after it — is not tracked by the Cooldown Manager,
  so LOW has nothing to draw on and "nothing is lit" has to carry the meaning "go
  build shards". Either that reading is taught and accepted, or cap draws its own
  icon for an ability the CDM does not track — which is new surface, and a different
  addon from one that rides the CDM.
- **Is target count readable, and may cap branch on it?** Several Demonology calls —
  Implosion most of all — turn on how many things you are fighting, and §3.5's
  vocabulary has no term for it. Until the client fact is established the catalog
  cannot tell single-target from AoE at all, and every AoE opinion is unsayable.
- **Second spec.** Demonology first is settled; what follows isn't. Choose it for
  what stresses the design differently, not for what's easiest.
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
| M2 | Foundation — bind to the CDM, the movable frame, nothing visible but status | ⚠ code-complete, **not flown** |
| MC | §3.5 the catalog format, and Demonology's | ✅ 2026-08-05 |
| M3 | §3.1 the tier signal + §3.2 procs, on the Demonology catalog | — |
| M4 | §3.4 smart cooldowns — bars, then the tier signal applied to them | — |
| M5 | §3.3 sequences (Demonology catalog) | — |
