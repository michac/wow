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

## 2. Scope

cap is built for the author first and may be published later. It has chosen defaults and no
settings panel. The player may move its independent surface and set single-target or AoE mode;
those are inputs, not a way to rewrite cap's opinions.

Specs are added one at a time. The first pilot is Demonology Warlock / Diabolist. A spec or
build cap has not deliberately authored is completely inert: no generic recommendations, no
fallback skin and no guesses.

cap is meant to work in the restrictive case—combat, instances and PvP—not only on a target
dummy in a city. Out of combat it is quiet apart from setup controls.

## 3. What the player sees

Section 1 wins over every detail below. A later rule that produces a next-action engine,
requires cap to branch on sealed data, or prevents a useful hint from readable data is invalid.

### 3.1 Emphasis

cap may place one **emphasis** treatment on an ability it has a useful opinion about. No
named HIGH / MEDIUM / LOW ladder exists. An ability is emphasized or it is not; readable
facts may vary the strength inside that treatment when a gradual distinction helps.

Emphasis is not a quota and not a promise that exactly one option will be lit. Several
abilities may be emphasized, one may be, or none may be. cap does not rank emphasized
abilities against each other.

The baseline treatment is static. Color, alpha, blend mode, size and interaction with
Blizzard's proc glow are tuning hypotheses until judged in the game. Motion is added only to
solve a specific observed problem.

An ability cap does not enhance remains visually untouched. cap does not dim the rest of the
Cooldown Manager merely to make its own signals look stronger.

### 3.2 Context markers

A marker adds a fact the player can combine with an emphasis; it does not collapse several
facts into a single verdict.

- A **readable marker** is driven directly by a fact Lua may read. It needs no sealed client
  half. Tyrant setup dots are the first example.
- A **sealed marker** is optional. The client may evaluate a sealed value and draw the result,
  but Lua never reads that value or branches on it.
- A **hold marker** is context that says there is a reason to wait. It is visually distinct
  from emphasis and does not silently turn an available ability into an unavailable one.

Every supported marker has a visible implementation. A catalog form that loads successfully
and then renders nothing is a defect.

The initial marker shapes, colors and placement are provisional. The first flight asks
whether the player can identify the fact without consulting the catalog.

### 3.3 Tyrant cooldown experiment

One movable Tyrant countdown bar tests whether a larger surface adds information the CDM icon
cannot carry legibly. It is independent: it does not automatically inherit icon emphasis or
markers.

The client owns the remaining duration. cap may hand that duration to the bar but may not read
it back. Ready, counting-down and unreadable states must not be confused, and a capture may
report only which path cap armed—not what appeared on screen.

The bar is an experiment, not a required surface for every cooldown. It remains only if play
shows that it earns the extra screen space.

### 3.4 Demonology pilot

The first pilot is deliberately small:

| Ability | Player problem | Initial hypothesis |
| --- | --- | --- |
| **Demonbolt** | Blizzard's proc glow says available even when using the proc would waste readable Soul Shards. | Show one static emphasis for a live proc and vary its strength from readable shard state. Exact thresholds and stock-glow handling are chosen through play. |
| **Summon Demonic Tyrant** | Readiness alone does not show whether familiar setup pieces are present. | Show one base emphasis while Tyrant is ready. Add separate readable markers for Dreadstalkers and Grimoire setup facts; do not combine them into a press/don't-press verdict. |
| **Tyrant bar** | The icon may be too small to make the next burst window legible. | Test one independent countdown bar as described in §3.3. |

Everything else begins absent. An ability is added only after naming the player problem its
hint solves. Gameplay facts come from authoritative rotation sources; usefulness comes from
play.

### 3.5 Safety boundary

The implementation distinguishes two data paths:

- **Readable facts** may enter Lua conditions and drive emphasis or markers.
- **Sealed facts** may flow only into client-owned display sinks. They never enter a Lua
  condition, comparison, score or verdict.

A refused readable fact is **unknown**, not false. Unknown input produces no confident hint,
and negation never turns unknown into confidence.

The catalog contains only abilities cap enhances and only data forms the current renderer
supports. Unclaimed CDM rows may appear in diagnostics but are not authoring failures and need
no silence declarations. Unused or unwired vocabulary is not admitted in anticipation of a
future spec.

No catalog, no matching build, an unsafe read, or an unsupported binding all fail inert. The
capture names developer-actionable failures without turning them into player-facing noise.

## 4. What cap does not do

- It never presses, queues, macros or takes an action for the player.
- It does not automatically detect an opener or burst sequence and mark the current and next
  spell. A future sequence idea must first show how it informs a choice rather than choosing
  the next press.
- It does not surface Blizzard's Assisted Combat recommendation as its own opinion.
- It is not a WeakAuras-style rule editor and does not accept user-authored priority packs.
- It does not replace or configure the Cooldown Manager.
- It does nothing on specs and builds without an authored experience.
- It does not own keybinds or action-bar layout; that is BucketBinds.
- It supports Retail / Midnight only.

Combat Assist Plus supersedes the old Cooldown HUD product. Its measured client facts remain
in `knowledge/addon-dev/`; its decision-engine code is not carried forward.

## 5. Platform constraints

Secret Values and combat lockdown bound the implementation. The authoritative facts live in
`knowledge/addon-dev/`, not in this product spec.

- Secret Values decide which facts are readable and which may only be displayed through a
  client-owned sink.
- Combat lockdown decides when binding, placement and protected-frame work may happen.

The product consequence is §3.5. The source may enforce that boundary and safe failure. It
must not turn provisional gameplay or visual opinions into platform rules.

## 6. How a hypothesis becomes a feature

New hints begin as small hypotheses. Before a flight, state the player-experience question.
Play first and record the player's report in their own terms. Use captures afterward to
explain whether the authored mechanism ran and why the observed result may have happened.

Captures never overrule the player's visual judgment and never reveal what a sealed sink drew.
Occupancy and refusal rates are diagnostics, not acceptance quotas. A green unit suite means
the engine obeys its mechanical and platform contracts; it does not prove that a gameplay
opinion is useful or a treatment looks good.
