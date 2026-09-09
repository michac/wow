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
