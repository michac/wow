# Smart Glo

Rule-driven glows on **Cooldown Manager icons**. Pick a cooldown the client already knows
about, attach one or more glows to it, and give each glow a rule that decides when it fires.

`backlog.md` owns status and the work list. This file owns the design and why it is shaped
this way.

## Why it exists

The capability splits in two, and the shipping addons each have one half:

| | Glows an existing CDM icon | Resource predicate |
|---|---|---|
| **EllesmereUI** (standalone CDM) | yes | no — buff/proc conditions only, including *Glow at Stacks* |
| **TellMeWhen** | no | yes — `HOLY_POWER`, `SOUL_SHARDS` and the rest are first-class conditions |
| **WeakAuras** | frame selector only, bound to a bar slot | yes |
| **MaxDps** | yes, whole-rotation | not as configuration |

TellMeWhen's glows do take an anchor, but it resolves as a child of TellMeWhen's own icon, so
it can never reach a CDM frame. Its only CDM integration is a setting to **hide** the viewers —
it treats the Cooldown Manager as a competitor, not a surface. Nobody joins the two halves, and
the join is the whole product.

## The shape

**Decorate, never replace.** No viewer is hidden, no icon row of our own is drawn, and a
cooldown the CDM does not lay out is not conjured onto the screen. If Smart Glo is switched
off, the Cooldown Manager is exactly as Blizzard shipped it.

**A rule is configuration, not code.** The user picks a subject and a predicate from
dropdowns. Nothing about the design requires a scripting surface, and adding one would be a
different product. *(Re-examined 2026-09-08 against a direct request for a Lua predicate
surface, and kept.)*

Two reasons that were not obvious when this was first written. **A rule that cannot be
evaluated must be impossible to author, not merely broken at runtime** — the primary-resource
wall under *The rules* below is exactly that, and only a structured surface can enforce it; user Lua can only
fail at 3am mid-pull. And **the interesting half of a rule is not a value at all**: a sealed
term is a binding the client evaluates and we never see, so there is no boolean for user code
to return. See `rule-language.md`.

**A rule is also an exchangeable artifact.** Import/export is in scope. The wire format may
be an opaque base64 blob — compactness is worth more than readability for something people
paste — but **decoding one must never require a Lua interpreter**, because tooling in this
repo has to open a rule, edit it and re-encode it in Python alone. `rule-language.md` §7.

### Picking the subject

`Enum.CooldownViewerCategory` has nine members, and the config groups them the way a player
thinks about them rather than the way the enum is ordered:

- **Essential** and **Utility** — the two viewers most people actually look at.
- **Items** — the `EquipSlot*` categories: trinkets and the rest of the equipped kit.
- **Unset** — known to the category set but not laid out on screen. This bucket exists because
  `GetCooldownViewerCategorySet` returns a **superset** of the rows the viewers lay out; the
  KB is explicit that it is not a row count. A subject here has no frame to glow, so the
  config must say so rather than offering a glow that silently never appears.

### The rules

v1 is **secondary-resource thresholds** — *at or above N Holy Power*, *at or above N Soul
Shards* — and that is deliberately the whole vocabulary for the first pass.

**The rule language itself has its own document: [`rule-language.md`](rule-language.md).** It
owns the type system, what may be combined with what, the compilation model and the syntax.
This section owns only the v1 scope decision.

⚠ **The boundary is not a matter of taste — but it is not where this file used to say it
was.** Secondary resources (Holy Power, Soul Shards, Combo Points, Chi, Arcane Charges,
Essence, Runes) are never secret and can be **branched on** anywhere. Every **primary** —
Mana, Rage, Focus, Energy, Runic Power, Fury, Pain, Insanity, Maelstrom — reads secret in
every context, in a city as much as mid-pull, so a primary threshold can never gate a
decision in Lua. The per-type table is
`knowledge/addon-dev/security-taint-and-restricted-data.md` §4.12.

**A primary is still usable, as a BINDING rather than a gate.**
`UnitPowerPercent(unit, type, unmodified, curve)` accepts a colour curve and the client
evaluates the secret internally: measured, secret Fury drove `SetVertexColor` directly, with
no boolean quantisation *(§4.8.1 finding 8)*. So "glow at 80% Fury" is one curve — the addon
never learns the number, and the appearance is the answer. What is impossible is *combining*
that with something else in Lua, because there is no boolean to combine.

The rule, then: **a primary may never appear as a gate, and may appear as a binding.** Which
one a given term is, and why the distinction is load-bearing for the whole config surface, is
`rule-language.md`.

This is the same wall that ended Hekili on retail. What survives it is not only the
secondary-resource slice — it is every question the client will answer in C on our behalf.

### Attaching the glow

The KB already owns every piece of this and it should be read before any of it is written —
`knowledge/addon-dev/cdm-rider-patterns.md` §4.2 (knowing when an icon is rebound, via the
mixin hook), §4.3 (enumerating icons), §4.4 (resolving an icon to its cooldown info), §5
(resolving an icon to a spell ID with the clean-cache pattern) and §6 (proc glow without
polling). §4.5's once-guarded, coalesced post-hook is the shape a per-icon decoration takes.

⚠ **None of that has been exercised for this addon yet.** The sections are the design's
intended foundation, not a claim that the foundation has been tested here.

## Deploy

A normal addon with its own repo and releases; ghaddons installs from the latest GitHub
release, so a push alone deploys nothing.

    uv run python -m wowkb.addon release sg --patch

Then `/reload`. Commands: `/sg status`.

## Turning it on for a character

    /sg enable

Reads the spec you are playing, matches it to the profile written for that spec, loads it,
and remembers the answer **for that character** — every later login on it takes the same
profile without being asked. `/sg disable` turns the switch off and leaves the applied rules
alone. `/sg status` says which way the switch is set and what it would load.

A profile is eligible for this only if it declares the spec it is for (`spec` in
`Profiles.lua`); the starter set and the probes declare none, so `/sg enable` can never hand
one out. The shipped profiles are each transcribed for **one hero tree**, so a profile also
names the talent that proves you are in it: in the wrong tree `/sg enable` refuses and says
so rather than loading advice written for someone else's build, and when the talent cannot
be read it loads and says the tree is unconfirmed.

Two things it will not do, both deliberate:

- **It never replaces rules you have edited.** The applied set is stamped when it is taken
  from a profile; if it no longer matches that stamp, a login says what it wanted to load and
  leaves your rules standing.
- **It is one switch per character over one account-wide rule set.** The rules live in
  `SmartGloDB` and there is one applied set; the switch lives in `SmartGloCharDB`. So an
  enabled character claims the rule set on the way in, and a character with the switch off
  sees whatever the last one applied.

## The profile viewer

`rules/*.sg` is the authoring surface and it reads badly in a terminal: the table you want
when comparing rungs and the commentary you want when questioning one are the same text, and
neither is scannable. `tool/gen_site.py` renders both as a static site.

    uv --directory tools run python ../projects/smart-glo/tool/gen_site.py
    uv --directory tools run python -m wowkb.serve projects/smart-glo/site \
        --watch projects/smart-glo/rules \
        --on-change 'uv --directory tools run python ../projects/smart-glo/tool/gen_site.py'

⚠ **`site/` is generated and gitignored — never hand-edit it.** Edit the `.sg` file, or the
generator.

Three properties it is built to keep, each of which is a way it could quietly start lying:

- **The table comes from `wowkb.smartglo.parse`, not from the source lines.** It renders the
  AST the *checker* reads, so a page cannot agree with a rule's comment while disagreeing
  with the rule. A profile that renders is a profile that checks.
- **A subject is named as the RULE names it.** An id can answer to more than one word —
  432459 is `holy_bulwark` to a rule and "Holy Armaments" in the ability inventory — so the
  page prints the `on` token, borrowing the inventory only for punctuation the slug cannot
  carry (`avengers_shield` → Avenger's Shield).
- **Every number on the prototype page is read out of `addon/SmartGlo/Look.lua` at build
  time** — the spin period and direction, the black↔yellow cycle and its hold/cross wave, the
  mark fraction, the plate's scale, colour and alpha, the urgent pulse's period and scale, the
  palette — and the art drawn is the addon's own `Media/hex-white.tga` and `Media/hex-fill.tga`.
  Its tiles are rendered from the same `STYLES` entry the style lab marks `shipping`, so the two pages
  cannot disagree. A renamed constant fails the build rather than drawing a stale picture. The
  one thing it cannot simulate is the client: the icon behind the mark is a still.

### The style lab

`styles.html` runs candidate marks across icons chosen to fight them — gold to swallow the
bright end of the cycle, violet and dark art to swallow its dark end — with an **icon size** slider, a
**freeze**, and a **peripheral blur**. A style is a data entry in `STYLES` (a list of layers,
each a mask + fill + scale + spin); `glow.js` knows no style names, so adding a candidate is
a Python-side change and never a CSS one.

⚠ **Only `current` is what the addon draws.** Every other entry is a prototype and carries
what it would actually cost in the client, because a style that cannot be drawn there is not a
candidate. The last four are a look that was **built, released, flown and then taken apart**:
the mark over a translucent black plate, with `urgent` moved off the size channel onto a bounce
run 18% fast. It won every offline measure on this page and lost the only one that counts — so
it came back in pieces. Shipping now are the smaller mark, the dark end of the swing, and the
plate in purple *turning with the mark*, which is what stops it reading as a hole punched in the
row. The bounce did not come back; beside icons that are not moving it read as fidgeting.
Those entries stay in the lab because "why not the one that measured better" is a question the
page should be able to answer. The retired numbers live in `gen_site.py`'s `LAB` dict,
deliberately separate from the `Look.lua` values `current` is built from, so the lab cannot show
a constant the addon does not have.

The prototype masks the other candidates need — a dilated hexagon for the rim, the triangle
and dot shapes — are generated in `gen_site.py` from the shipping master, and so is the plate
mask — ⚠ derived rather than converted, because the shipped `hex-fill.tga` has `PLATE_ALPHA`
baked into its alpha and converting it would apply the translucency twice. `hex-white` is
converted from the `.tga` the addon loads. Promoting a style means moving its derivation into
`tool/gen_media.py` and emitting a `.tga`, which is the trip the plate has made.

**The blur control is the point, not a toy — and it takes an ANGLE, not a pixel count.** A
pixel count was unanswerable: 5px means one thing on a 28px icon and another on a 120px one.
The slider now sets **eccentricity in degrees off-axis** and derives the blur from
`MAR(E) = MAR₀(1 + E/E₂)` — the standard linear acuity falloff, `MAR₀` one arcminute, `E₂`
2.3° — with sigma taken as half the minimum resolvable angle. Converting to pixels needs one
assumption, stated on the page so it can be argued with: **a CDM icon subtends ~0.9°** (40px
at ~45 px/deg — a 27" 1440p panel at 60cm). **10–15° is where the Essential viewer actually
sits** while you watch your character; 20–25° is a side-mounted bar.

⚠ It models low acuity and **nothing else** — not the periphery's much better **motion**
sensitivity, nor its near-intact contrast sensitivity at low spatial frequencies. So it is
systematically unfair to anything that moves and fair to anything large, which is exactly why
the spin measured worse than it may fly. It rules candidates out; it does not pick the winner.

`tool/measure_motion.py` renders the same compositing offline at a controlled time step and
reports two numbers per candidate, because they disagree and the disagreement is the finding:
**rate** (mean change between consecutive blurred frames — a derivative, so it rewards fast
change and punishes slow) and **swing** (per-pixel max minus min over the period — an
amplitude, blind to rate). It shares the eccentricity model with the page; keep them together.

⚠ **The measurement is a ranking aid, not a verdict.** It cannot tell a change that draws the
eye from one that merely irritates, and it says nothing about whether plain and `urgent` stay
*tellable apart* — only how much each one moves.

⚠ **A missing icon draws a blank tile rather than a near-miss.** `ICON_FALLBACK` in the
generator carries the ids the media endpoint cannot resolve, and each entry is a claim that
the art is *the same picture* — Protection's Hammer of Wrath override borrowing 24275 is one,
because the client draws one picture for both. Infernal Bolt (434506 / 433891) has no
reachable icon at all and is left blank on purpose: the Holy Armaments node resolves to the
**Bulwark** icon, so a borrowed sibling would have shown the wrong armament and looked right
doing it.
