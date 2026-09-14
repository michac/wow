# The Smart Glo rule language

**Status: mostly built.** The two bowls, the composition rules, the refusal list, the syntax
and both sealed sinks are in the addon; `§9. Open` carries the client questions that are not,
and no claim here is settled by a flight unless `backlog.md` says it flew. This file is the
language — `backlog.md` owns what is actually built.

`README.md` owns the product and the v1 scope. This file owns the language: what a rule can
say, what it can never say, how the two combine, and why.

---

## 0. The one thing to understand first

**Two kinds of term exist, and the difference is not a matter of degree.**

- A **gate** is a fact Lua may read and branch on. Unlimited, freely composable.
- A **binding** is a fact Lua may never read, handed to the client to evaluate. The client
  answers it in C and paints the result; we never learn the value.

Every constraint in this document follows from that split. A language that pretends the two
are one thing will generate rules that silently never fire — which is the specific failure
this design exists to prevent.

⚠ **The split is NOT "cooldowns and resources are sealed."** It is much narrower than that,
and getting it wrong in the pessimistic direction costs more than getting it wrong in the
optimistic one, because it makes the addon refuse things the client would happily do.

---

## 1. The boundary, exactly

For most subjects the discriminator is **the threshold value**, not the subject:

| subject | threshold at **zero** | threshold **elsewhere** |
| --- | --- | --- |
| cooldown | `ready(X)` — **gate** | `X.cooldown < 10s` — **binding** |
| aura | `has(X)` — **gate** (nil-test) | `X.stacks >= 6` — **binding** |
| charges | "on cooldown at all" — **gate** | current count — **binding** |
| secondary resource | **gate at any threshold** | — |
| primary resource | **binding, even at `> 0`** | **binding** |

**Readiness is a first-class gate and needs no trick.** `C_Spell.GetSpellCooldown` is *not*
sealed whole — its members seal individually, and `isActive` / `isEnabled` / `isOnGCD` read
plain in restricted combat while `startTime` / `duration` / `modRate` are secret. `isActive`
carries `NeverSecret = true` and was measured plain across 90 samples
*(`cooldown-manager.md` §7 "The readable surface", `[client 2026-08-09]`)*.

The scratch-frame trick — arm a hidden `Cooldown` from a duration object and read `IsShown()`
— is the **fallback** for when only a duration object is in hand, not the primary route
*(`cdm-rider-patterns.md` §2.3)*.

**Primary resources are the exception that breaks the threshold rule.** No zero-crossing is
readable, so even `fury > 0` is a binding — spelled `fury% >= 80`, a percent curve on
`UnitPowerPercent`, which is `UnitHealthPercent`'s sibling and the same mechanism the `health%`
family rides. The nearest **gate** is `IsSpellUsable`'s `insufficientPower`, shipped as
`affordable(<spell>)`: it answers *"can I afford this particular spell"* rather than anything
about the bar — and it is **binary**, false at 40 Fury and at 170 alike, so overcap is
unreachable through it *(§4.12)*. Both exist; they answer different questions, and the gate is
the one most rules want because it spends no bind slot.

⚠ **`ready()` is not the affordability gate and never was.** It reads
`isActive`/`isEnabled`/`isOnGCD`, and `isEnabled` is spell-book enablement. `ready(x) and
affordable(x)` is the pair that means *press this*.

### The readable vocabulary

Secondary resources (Holy Power, Soul Shards, Combo Points, Chi, Arcane Charges, Essence,
Runes), plainly or **projected past the cast in flight** · `isActive` · `isOnGCD` · `isEnabled` · `insufficientPower`, as `affordable()` · `maxCharges` ·
`cooldownID` / `linkedSpellID` · aura **presence, through the CDM's alert edges** · a DoT's
**refresh window**, as `refreshable()` · `C_AssistedCombat.GetNextCastSpell` · talent and
spec, as static load conditions.

#### `refreshable(<aura>)` — the pandemic window, computed by the client

`aura()`'s sibling: same namespace, same tracked row, same three values. It is the one
readable answer to *"is this DoT about to fall off"*, and the predicate is **Blizzard's**
rather than a threshold we picked — `item.PandemicIcon` mirrors `IsInPandemicTime` exactly,
and that window is `GetRefreshExtendedDuration − GetAuraBaseDuration` (`cooldown-manager.md`
§5.2, §7 Tier 2). So it matches an APL's `refreshable` instead of approximating it.

⚠ Its preconditions are the row's, not the aura's, and both directions are UNKNOWN rather
than absent: **no Cooldown Manager row bound to the aura**, and **a row that raises no
pandemic alert at all** — a self-buff (the window is target-auras-only), an aura with no
carry-over. `/sg why` names which.

#### `<resource>.after_cast` — the count once the cast in flight lands

A resource cost is debited at **completion**, not at cast start, so mid-cast the bar still
shows the pre-cast number. A plain threshold therefore answers about a state that is already
spent: at 5 Soul Shards, casting Hand of Gul'dan, `soul_shards == 5` keeps saying *capped* for
the whole cast and stops saying it exactly when the answer starts being useful. `.after_cast`
subtracts the cost and adds the gain at the same moment, because both land at the same moment.

Everything it needs is readable. The player's own cast id is not sealed —
`SecretWhenUnitSpellCastRestricted` tests **which unit** is being asked about, not whether
combat is restricted (`cdm-rider-patterns.md` §9.2) — so `UNIT_SPELLCAST_START` opens a window
keyed by spell id and the terminal events close it. Only a **hard** cast opens one: `_START`
does not fire for an instant, whose result is already in the bar by the time anything could
read it. Costs come from `C_Spell.GetSpellPowerCost`, which is talent-correct at the moment it
is asked; gains come from a table generated out of `SpellEffect.db2`'s energize rows.

⚠ **Soul Shards are the only resource this is offered for, and the reason is measured.** The
same Tier-1 energize rows show Wake of Ashes returning 1, 3 or 5 Holy Power and Ambush 1, 2 or
3 Combo Points depending on talents and procs; a projection needs one number and those have
none. The generator marks such a spell `varies` and the checker refuses the term by name.

Three outcomes, kept apart: nothing in flight is a projected **zero**, not an unknown, so the
term reads exactly like a plain threshold while you stand still; a spell whose gain varies, an
unreadable cast id, or a refused cost reads **UNKNOWN** and the glow fails dark; anything else
is a number.

⚠ **Aura presence is readable, but NOT through `C_UnitAuras`, and the difference decides
whether a rule works.** Measured in combat from tainted code, the spell-keyed getters return a
silent `nil` — indistinguishable from "no such aura" — and the enumerators raise outright, on
the player's own auras as much as the target's
(`security-taint-and-restricted-data.md` §4.7.1, `[client 2026-08-19]`). So a nil-test against
`GetPlayerAuraBySpellID` is not a presence gate; it is a gate that reads *absent* whenever it
is refused, which is the exact shape §3 forbids. The readable route is
`CooldownViewerItemMixin:TriggerAlertEvent`'s `OnAuraApplied` / `OnAuraRemoved` edges — a
*call* observed rather than a value read, so a latch built on them may be branched on
(`cooldown-manager.md` §5.1). ⚠ It carries its own precondition: the edges fire only on a row
the viewers actually laid out, so an aura the player has not enabled in Tracked Buffs raises
nothing at all. **That silence is UNKNOWN, never absent** — and the remedy is one tracked-buff
toggle the player will never think of unless the addon says so.

### The sealed vocabulary, in three families

They are not interchangeable — different sinks, different domains, different preconditions:

| family | source | sink | domain | precondition |
| --- | --- | --- | --- | --- |
| **duration** | cooldown remains · recharge remains | curve → any texture channel — **a real glow** | seconds, or percent | none |
| **remains** | **aura** remains | authored `NumericRuleFormatter` → `SetDurationText`, **leaf FontString only** | seconds | a live aura on the unit the container watches — and the implicit presence gate below |
| **count** | aura applications | authored `NumericRuleFormatter` → `SetApplicationCount`, **leaf FontString only** | integer stacks | a live `auraInstanceID`, i.e. the player's CDM must be tracking that aura |
| **percent** | primary resource | `UnitPowerPercent` + colour curve → texture channel | percent | none |

⚠ **A count binding is TEXT, and that is a product fact rather than an implementation
detail.** Its only sink is `SetText` on a leaf FontString; the route to art is a texture escape
inside a band's format string. So whatever the client draws for a count is an inline texture
laid out as text — **not** a ring or ants around the icon border, which is what "glow" normally
means.

⚠ **And an inline escape takes the FontString's ALPHA and none of its geometric transforms** —
measured with nothing sealed anywhere: a plain Texture rotated, a FontString of ordinary text
rotated, the same FontString carrying only a `|T…|t` escape neither rotated nor scaled, and an
alpha animation on it faded the mark normally
(`security-taint-and-restricted-data.md` §3.5, `[client 2026-09-08]`). So a mark drawn *as* an
escape may blink and may not spin. The FontString's animation channel is genuinely ours —
`SetApplicationCount` seals only `Text` and `Shown` — but what it moves is the glyph run.

**The route to a moving mark is therefore to INVERT the polarity, not to animate the escape.**
Our own Texture spins permanently on the overlay; band 0 draws an **occluder** over it — the
subject's own icon, centre-cropped, so the "off" state is an untouched Cooldown Manager icon —
and the band at the threshold draws `""`, revealing the mark already in motion. The addon has
still branched on nothing; the client simply stops concealing. ⚠ The cost is §6.4: band 0 draws,
so absence is no longer free.

**Alpha, scale, translation and rotation all move on a sealed FontString** `[client
2026-09-08]` — translation included, which was the one expected to fail, since a secret
`SetText` marks all anchoring and positioning data secret and that is what a Translation
animation writes. The engine evidently applies it as a render offset rather than an anchor
write. Colour was not tried and is unmeasured; a static `SetTextColor` separately works.

⚠ **On the COUNT sink this is measured only one step, and the step is a refusal to READ.**
`IsPlaying()` on a group the addon built on a FontString it handed to `SetApplicationCount`
raises forbidden-object, so the addon cannot inspect its own animation afterwards — and **no
flight has yet reported a count mark actually turning**. Arming before the handover and gating
by `SetAlpha(0)` rather than `:Hide()` are what this project does in response; both are
precautions consistent with the evidence, neither is established as necessary
*(`security-taint-and-restricted-data.md` §3.5)*.

Four limits come with it — the motion **cannot differ per band** (one group, one region; bands
choose what is drawn, never how it moves); an animation can never **start** on the threshold
crossing, because the crossing is never observed, so it runs permanently; a **bar sink gets no
gating** at all, because a bar has no blank state and its track draws at zero; and the
FontString must be a **layout leaf** — anchor it *to* things, never anything *to* it, and note
that a FontString fed a secret also stops being measurable by tainted code, so no decoration
can position itself relative to the count.

⚠ **Everything a sink is given is fixed at the moment it is given** — a formatter's bands, and
every size literal inside a format string. A count display that must follow a resizing icon has
no other route than re-calling the sink, and whether that is legal is **open and now
PARKED after five flights** `[client 2026-09-08]`. Every call is *accepted* — first arm, second
arm on the same FontString, a fresh one, clear, re-arm after clear — and `GetApplicationCount`
reports the second string; whether the second formatter's output is what **draws** was never
established, because the sink seals `Text` and no getter reports the rendered string. The last
reading had the shape of a yes but an unidentified subject. **Acceptance is not pixels. Do not
design a re-arming display on the assumption that it works.**

**The count route is measured and shipping, pin included.** A tainted-created
`NumericRuleFormatter` **is** honoured on `SetApplicationCount`, four band tables drew on
player-HELPFUL tiles including the complement `{{0,"%d"},{2,""}}`, a band's inline `|T…|t`
escape **renders** as art rather than passing through as text, and
`candidateFilters.includeSpellIDs` binds a player-buff slot to the aura it names — measured by
two pins drawing side by side, each tracking its own aura
(`security-taint-and-restricted-data.md` §3.5.1-§3.5.2, `[client 2026-08-11]`,
`[client 2026-08-21]`). So a count binding may be relied on to be about the aura the rule
names.

⚠ **The count precondition is the user's own CDM configuration**, which no checker can verify
at authoring time. It has to surface as a runtime unknown ("requires Wild Imps tracked in your
Cooldown Manager"), never as a rule that quietly draws nothing.

### The `look` vocabulary is not uniform across families

Duration and percent bindings reach real texture channels and get the full look set. A count
binding is one FontString carrying one looping animation, so its looks are a constrained
subset. **Whenever the look picker exists, it must narrow once the binding family is known**,
or it will offer a look that cannot be drawn — which is the same failure as offering an
unevaluable rule, one layer further down.

⚠ **v1 does not have that picker.** It ships **one fixed look** — a yellow box inside the icon,
roughly where the proc flipbook sits — and no `look` keyword (§8). The non-uniformity above is
why the picker is a later question and not a v1 omission: designing the narrowing rule before
a single glow has drawn would be designing it blind.

---

## 2. Composition — what may be combined with what

**The affine resource is the CHANNEL, not the secret.** One duration object may drive any
number of sinks; what cannot happen is two secrets writing *the same widget channel*, because
neither can be compared nor maxed in Lua and the second write silently wins.

| combination | available? | how |
| --- | --- | --- |
| gate ∧ gate | ✅ unlimited | ordinary Lua |
| gate ∧ binding | ✅ | `:Hide()` the widget before C ever sees it |
| ¬ binding | ✅ | invert the curve or the band table — free |
| binding ∨ binding | ✅ | two **sibling** widgets; alpha compositing performs the OR |
| **binding ∧ binding** | ✅ **`[client 2026-09-08]`** | **NESTING.** A child renders at parent alpha × its own, and that still holds when both alphas came from secrets — measured |

**So the sealed values form a complete boolean algebra, and the widget tree is the circuit.**
NOT is a curve inversion, OR is siblings, AND is nesting *(§4.8.5)*. There is no boolean
operation the language has to refuse on composition grounds.

So **"one sealed leaf per widget"** is a *derived* allocation rule, not a primitive. A second
sealed leaf costs a second widget — a **sibling** for OR, a **parent or child** for AND.

**What AND is FOR, now that it has a real consumer: alignment.** The question a rotation
actually asks of two secrets is *"are these both nearly up at once"*, and the APLs are full of
it. Havoc's Vengeful Retreat wants `gcd.remains < 0.3s` **and** `eye_beam.cooldown < 0.45s`
together — two sealed durations, no readable term between them — so before the nesting result
it could only be refused. It is now an outer frame whose alpha is a curve on one duration and
an inner texture whose alpha is a curve on the other, visible only in the intersection. ⚠ It
reaches only leaves that produce an **alpha** — duration and percent; a count reaches `SetText`
and never yields an alpha to combine.

⚠ **None of this helps the count family, and it is worth saying so explicitly.** The AND
result is about combining secrets that already reach an alpha channel. A count reaches
`SetText` and nothing else, so it never produces an alpha to combine. The count family's limit
is a **sink** limit, not a **composition** limit, and the AND measurement does not move it.

⚠ **A curve evaluation is a SNAPSHOT, not a binding, and this is the cost the word "binding"
hides.** `EvaluateRemainingDuration(curve, mod)` returns a value at the instant it is called,
so the `SetAlpha` fed from it is a one-shot write that must be **re-applied on a refresh
tick**. Only the sinks taking the duration *object* — `SetCooldownFromDurationObject`,
`StatusBar:SetTimerDuration`, `DurationTextBinding`, and the authored aura formatter — are
genuinely live and poll-free. **The duration family, which is the one a real glow would use
most, is on the polling side.** Budget for a per-glow refresh loop rather than assuming the
client watches it.

⚠ **In practice this constraint almost never binds.** Most rules a player actually wants are
pure gates:

- *"Tyrant is ready and I have 4+ shards"* — two gates, **zero bindings**
- *"Implosion ready and Dreadstalkers not"* — two gates, **zero bindings**
- *"6+ imps"* — one binding
- *"10s left on Tyrant"* — one binding

The config surface should be shaped around that: gate rows are the default form, and the
binding slot is an advanced section most rules never open.

---

## 3. Evaluation semantics

**Three-valued, and the third value is mandatory.** Reads genuinely refuse — a talent read on
an unresolvable build, an aura row the player never enabled, a resource that comes back a
non-number. `UNKNOWN` must never collapse to `false`.

1. Evaluate **every** term. No short-circuit — the diagnostic needs all of them.
2. Any `false` → **off**. A false rules a rule out even when another term is unknown.
3. Any `UNKNOWN` with no `false` → **blind** → **fail dark**.
4. Never let a negated unknown become true. (SQL's `NOT IN (…, NULL)` is forty years of
   evidence for this being the trap it looks like.)

Interaction with bindings: `unknown ∧ S` → dark. `unknown ∨ S` → drive from `S` (sound: if `S`
is true the whole is true; if false the whole is unknown, which is dark anyway).

A binding has **its own** three-way at arming time — source present · source absent (readable,
nil) · row unbound (unknown) — and see §5 on why the author must decide the absent case.

**Every rule owes the user an explanation.** Ship a per-term `T | F | ?` readout behind
`/sg why <glow>`. A fail-dark rule with no explanation is indistinguishable from a broken
addon, and that is the support burden this design would otherwise create.

---

## 4. The compilation model

**This section describes the COMPILER, not the surface.** The author writes two bowls (§5);
what the tool does with them is below, and the two are the same machine seen from either end —
a `when` list is the readable remainder, a `bind` is the sealed leaf it is cofactored against.

Compile by **cofactoring on the sealed leaf**: substitute it with `true`, then with `false`,
and evaluate the readable remainder under the semantics above.

- both cofactors equal and known → a **constant driver** (show / hide). No secret spent.
- cofactors differ → the widget is **driven by that leaf**, inverted if `f(S=true) = false`.
- either cofactor unknown → **dark**.

**Readable-OR-sealed still collapses when it can.** `soul_shards >= 4 and (ready(tyrant) or
tyrant.cooldown < 5s)` written as one glow compiles to: when `ready` is true the driver is the
constant *show*; when false the driver is the curve — one widget, no second glow. §5 authors it
as two glows instead, which draws the same picture through layering; the cofactor is what lets
the compiler notice the collapse when a rule arrives already joined, as one does from a paste
or a profile.

**The refusal is precise, and it is about ALLOCATION rather than logic.** No boolean
combination has to be refused — nesting composes two secrets and siblings compose them the
other way, so the algebra is complete (§2). What the compiler spends is *widgets*: a second
sealed leaf on the same channel costs a sibling or a child, and the only refusal left is being
unable to spend one. So it can name the exact resource it ran out of, instead of refusing
anything cooldown-shaped.

The check is still structural — a pure expression has no control-flow paths, so it is leaf
counting, not path analysis. This is why an imperative form with early returns was rejected:
`if UNKNOWN:` has no honest branch, silently takes the else, and attaches the *wrong* binding.
(The nearest well-known analogue is query pushdown — EF Core 2's implicit client evaluation is
the imperative form; EF Core 3 making an untranslatable expression a hard error is this.)

---

## 5. Syntax sketch

⚠ **A sketch, not a grammar.** The semantics above are the settled part; this is one surface
over them, and the builder UI is expected to generate it more often than a person types it.

**Two keywords, and they are the two bowls of §0.** `when` carries readable terms and takes as
many as you like; `bind` carries the one sealed leaf a glow may spend. The checker knows which
bowl every term belongs to and refuses a mis-sorted one by name, so the sorting is enforced
rather than remembered.

```
glow "Implosion at six imps"
  on     implosion
  when   ready(implosion) and talent(to_hell_and_back)
  bind   wild_imp.stacks >= 6

glow "Tyrant: press"                  glow "Tyrant: soon"
  on     tyrant                         on     tyrant
  when   soul_shards >= 4                when   soul_shards >= 4
         and ready(tyrant)               bind   tyrant.cooldown < 5s

glow "Fury nearly capped"          glow "Chaos Strike I can pay for"
  on     chaos_strike                on    chaos_strike
  bind   fury% >= 80                 when  affordable(chaos_strike)
```

**The only look keyword in v1 is `color`**, naming one of eight baked hues (§8); everything else
about the mark is fixed. The band-table form below is still the way one secret drives several
appearances; it is the *bands* that vary, not a named preset per rule.

**A subject resolves to the icon's currently-bound spell.** `on tyrant` and `ready(tyrant)`
both mean the ID the icon is showing right now, override included — which is what the player is
looking at. `base(tyrant)` forces the static ID for the cases where that is what the author
means. Demonbolt/Shadow Bolt, Ruination and Metamorphosis are why the escape hatch exists.

**Why two keywords rather than one expression.** An earlier draft used a single `show` and
compiled it by cofactoring (§4); the draft before *that* split it into `when`/`while` and was
dropped because the very first worked example mis-sorted `ready(tyrant)` onto the sealed line.
The current split is not a return to that mistake, because the tool now **owns the
classification and refuses a term in the wrong bowl**, naming the bowl it belongs to. What
decided it is `README.md`'s founding rule — *a rule that cannot be evaluated must be impossible
to author, not merely broken at runtime, and only a structured surface can enforce it.* A single
expression with a checker behind it is the unstructured surface: you write a whole rule and the
compiler puts an asterisk on it afterwards, which is the TellMeWhen failure this product exists
to avoid. Two bowls make the illegal rule unwritable.

⚠ **The classification is a fact about the CLIENT BUILD and must never be stored in a rule.**
The never-secret roster moves per patch, so a rule that baked its own sorting would silently
mean something different after a patch. Bowls handle that better than free text: the tool
presents which bowl each term is in *today*, and a patch moves a term between bowls visibly.

**The spanning-OR objection, and why it costs nothing.** `soul_shards >= 4 and (ready(tyrant)
or tyrant.cooldown < 5s)` has an OR that crosses the bowls, and a two-slot form has nowhere to
put it. It does not need one: distribute to DNF and each disjunct becomes its own glow, and §8
already makes multiple glows on one icon independent layers that both draw. The two "Tyrant"
glows above *are* that expression. **DNF-as-layering is the general answer** — any expression
distributes, one glow per disjunct, and the only disjunct that needs more than a bowl-A slot is
one carrying two sealed leaves, which §2's nesting result covers.

**Units are typed on the literal** — `5s`, `6`, `80%` — and `1 gcd` earns a unit, since §2.2's
curve computes the GCD from guarded haste and pushes it into the break point.

**A bind is a curve, so it is strictly more expressive than a comparison.** A curve is a list of
`AddPoint(x, y)` pairs, so a *disjoint* range is one curve with four points and therefore one
bind — `tyrant.cooldown outside 12s..20s` spends the same single slot that `> 5s` does. The
bowl-A budget buys more than the syntax suggests.

Multi-look from one secret is a band table, which is sugar for N layers fed the same object:

```
  show   tyrant.cooldown:
           0s+   full
           5s+   dim
           30s+  off
```

⚠ **In v1 a band names an intensity of the one fixed look, not a colour** — there is no look
vocabulary to draw from (§8). Colour names return here whenever looks become authorable; the
band *grammar* below is fixed by the client either way.

Band grammar is fixed by the client and not by taste: **thresholds must strictly rise** (the
client picks the highest one a value reaches), **the first band must start at 0** (it is the
resting state; without it the client falls back to its own default), and **a threshold is the
minimum value its band applies to** — a value *on* a threshold takes the upper band.

---

## 6. What the checker must refuse

Each of these is a rule that would otherwise author cleanly and then never fire:

1. **Two sealed leaves writing the same widget channel.** Not the combination itself — every
   boolean operation is available *(§2)* — but the allocation: the compiler must spend a
   sibling or a nested widget, and refuse only if it cannot.
2. **A primary resource as a gate.** `fury >= 30` in a position that needs a boolean.
3. **`charges >= N`.** The current count has no curve sink and no formatter sink, so this is
   neither a gate nor a binding. It must be an error, not a silent no-fire. (`recharge < 3s`
   is a duration and works.)

   **But two charge questions ARE gates, and refusing them with the count would be the
   pessimistic error §0 warns about.** `isActive` stays plain on a charge spell, so *"on
   cooldown at all"* is readable — and because a charge spell's recharge is active exactly
   while it is *below* maximum, **"capped on charges" is the same gate read the other way**.
   For a two-charge spell that is the whole count: not recharging = 2, recharging and usable
   = 1, recharging and unusable = 0, all from readable booleans. ⚠ The
   `isActive ⟺ below max` equivalence is **inferred from how charge cooldowns behave, not
   measured**; it is a positive claim and will announce itself if wrong.
4. **A count band whose band 0 is not `off`, with no `absent` clause.** ⚠ **Absent is not
   zero, and a band table cannot see absence** — with no aura there is no candidate, the
   client hides the button, and every sink on it blanks. So *"fewer than six imps"* silently
   never fires at zero imps. The author must state the absent case as a Lua-side default, and
   ⚠ **the term that carries it is an alert-edge latch, not a `C_UnitAuras` nil-test** (§1) —
   which means it is three-valued in practice: present, absent, or *the row is not bound and
   nothing can be heard*.

   ⚠ **This refusal is narrow — it applies exactly when band 0 draws something — and the
   OCCLUDER form makes that every count element there is.** The reading it replaces was that
   an *at-or-above* rule has band 0 blank and therefore no absence case at all. That was true
   while the mark was drawn as an escape *at* the threshold. It is not true now: an escape
   takes a FontString's alpha and none of its geometric transforms, so a mark drawn that way
   can never move, and the way to a moving mark is to invert the polarity — our own Texture
   spins permanently underneath, and **band 0 draws an occluder over it** which the band at the
   threshold takes away.

   So every occluder rule is the genuine case. **With the aura absent the client hides the
   button, the occluder goes with it, and the mark would read as though the threshold were
   met** — a bright failure rather than a dark one, which is worse.

   **The readable half is where this is caught, and `Rules.Gate` does it for every count
   automatically.** A count bind gets an implicit `aura(<its own aura>)` term, so absence reads
   F and an unreadable presence reads UNKNOWN; either closes the element's alpha, and because
   the container is hosted on the element the occluder and the mark go together. The gate is
   not folded into the authored `when` — export and the checker still see what the author
   wrote, and `/sg why` prints the implicit term as its own row.

   This is what makes an aura that drops safe, so the rule is no longer *"point a count only at
   an aura that cannot drop."* Both of Demonology's shapes are now expressible: *"Implosion at
   6+ imps"* on Wild Imps, and *"Power Siphon at ≤1 Demonic Core"*, whose zero case the
   implicit term covers.

   ⚠ **The cost is real and is now paid by every count.** The presence term resolves through a
   Cooldown Manager row, which the occluder itself does not need — so a count glow now depends
   on a Tracked Buffs checkbox for its aura. A row in one of the two **buff** viewers answers
   through `IsActive()`; a cooldown-viewer row can only offer the two unmeasured presence
   fields. When neither can speak the term is UNKNOWN and the glow stays **dark and
   self-diagnosing** — `/sg why` names the missing checkbox — rather than bright and wrong.
5. **A temporal operator on a sealed leaf.** You never learn when a band flipped, so
   `for 2s` / debounce apply to gates only. A sealed term supports curve *shaping* instead —
   a `Linear` curve gives a ramp with no state at all.
6. **A threshold on a primary written without `%`**, since the only sink is a percent curve.

---

## 7. Serialization and exchange

Import/export is in scope. The constraint is **not** that the wire format be human-readable —
a base64 blob is fine, and compactness is worth something for copy/paste. The constraint is:

1. **No Lua interpreter anywhere in the decode path.** Tooling in this repo must be able to
   open a rule string, edit it and re-encode it in **Python alone**. The anti-pattern is
   `projects/mdt-desktop/`, which has to run real Lua in a child process because MDT's data is
   Lua; that is a cost this project should not take on. (Note the line is not "no Lua-shaped
   data" — `wowkb.charstate._LuaParser` already reads SavedVariables table literals in pure
   Python. It is *spawning an interpreter* that is out.)
2. **An agent must be able to author a rule directly** — write the source form, run a tool,
   hand back a paste-able string. Needing a running game client to produce one would make
   every authoring loop a login cycle.
3. A **`wowkb` subcommand is an acceptable and expected dependency.** This does not have to
   work by pasting the string into some other chat window with no context.

### What follows from that

**The AST is canonical; everything else is a rendering of it.** There are three:

| rendering | who produces it | who consumes it |
| --- | --- | --- |
| **surface text** (§5) | an agent, or the builder | a person reading a rule; the `wowkb` tool |
| **wire string** — `SG1:` + base64(deflate(payload)) | the addon, or the tool | the addon, or the tool |
| **the builder UI** | — | a person |

⚠ **The addon never parses the surface syntax.** It reads the wire payload and nothing else;
the builder constructs the AST directly, and surface text is converted by the Python tool.
That is what keeps the Lua side small — a grammar has to exist in exactly one place, and that
place is Python.

**WeakAuras is the anti-pattern, but not for the reason it looks like.** Its base64 envelope is
fine and worth copying. The problem is that the payload inside is a *serialized Lua table*
(AceSerializer / LibSerialize), so decoding it means being Lua. Keep the envelope, change the
payload.

### The payload is JSON

`SG1:` + `EncodeBase64(CompressString(SerializeJSON(ast), Deflate))`, and the same encoding
serves the built-in profiles in §8.

**Every one of those three calls ships in the client.** `C_EncodingUtil` is Tier 1 and carries
`SerializeJSON` / `DeserializeJSON`, `CompressString` / `DecompressString` (`CompressionMethod`
= `Deflate`/`Zlib`/`Gzip`) and `EncodeBase64` / `DecodeBase64` (`Base64Variant` = `Standard` /
`StandardUrlSafe`) `[T1 src: Blizzard_APIDocumentationGenerated/EncodingUtilDocumentation.lua;
state-persistence-and-communication.md §6.1]`. So the Lua side is three built-in calls and the
Python side is `json` + `zlib` + `base64`, all stdlib — JSON is now the cheapest option in
**both** languages, and none of it is a Lua interpreter, so constraint 1 above holds.

⚠ **Wrap every `C_EncodingUtil` call in `pcall`, and checksum the payload.** The generated docs
mark six of the ten `MayReturnNothing`, but that is not how they fail: measured
`[client 2026-08-05]`, nil sources, out-of-range enums and garbage input **raise** rather than
return nothing, while `DecodeBase64` on invalid input **accepts it and returns a short string**.
A decoder returning a value is not evidence the input was well-formed
*(`state-persistence-and-communication.md` §6.1)*.

The two alternatives, and why they lost:

- **A flat tab-separated directive format.** `strsplit` on the Lua side, `.split("\t")` in
  Python. Genuinely cheap, but no longer *cheaper* — and it costs a bespoke flattening scheme
  for the expression tree that JSON gets for nothing.
- ⚠ **A Lua table literal decoded with `loadstring` — rejected on security, not convenience.**
  `loadstring` is present in the sandbox and it would make the Lua side nearly free, but
  running `loadstring` over a string a stranger pasted is arbitrary code execution in the
  client. A shared-rules feature is exactly where that gets exploited.

Two requirements that hold whichever is chosen: a shared rule must **round-trip through the
builder without loss**, and **displaying an imported rule legibly is harder than composing
one** — most users will import far more rules than they write, so design the serialization
before the builder rather than after.

## 8. Decisions taken

- **Subject-first.** Pick a CDM icon, then attach rules to it. Rule-first ("build the rule,
  then choose what it decorates") is the answer to repetition and is deferred until repetition
  is actually felt — see `backlog.md`.
- **Configuration, not code.** Re-examined against a direct request for a Lua predicate
  surface and kept, for the two reasons in `README.md` § The shape.
- **Import/export in scope**, with the **AST** canonical and surface text, the wire string and
  the builder all renderings of it (§7).
- **Multiple glows on one icon are independent layers.** If two match, both draw. Priority
  between two *sealed* glows is unimplementable — you cannot know which fired — so the whole
  arbitration vocabulary is draw order. Say plainly that this is a rendering fact, not a
  logical one.

Settled 2026-09-08, in dependency order:

- **The config is ONE dialog: a subject dropdown, a detail pane, and a text box that is also
  the import/export surface.** The dropdown is built by **iterating the live CDM item frames**
  (§4.3's enumerators, each frame resolved through `GetCooldownID()` → `GetCooldownViewerCooldownInfo`),
  so every subject it offers has a frame *by construction* — which makes "a subject with no
  frame" unrepresentable in the picker rather than a state to detect, and takes the Unset bucket
  out of the common path. The detail pane follows the selection; the text box carries that
  subject's rules as editable text and doubles as paste-in / copy-out, so import/export needs no
  second surface. The UNKNOWN path (§3) still matters, for a rule arriving by paste or from a
  profile naming a subject the viewers do not lay out.
- ⚠ **Clicking Blizzard's own icons is out, and not as a matter of taste.**
  `CooldownViewerItemMixin:SetTooltipsShown` calls `self:SetMouseClickEnabled(false)`
  `[T1 src @12.1.0: Blizzard_CooldownViewer/CooldownViewer.lua —
  CooldownViewerItemMixin:SetTooltipsShown]`, and it is reached from
  `CooldownViewerMixin:OnAcquireItemFrame` — **every pool acquire, so every `RefreshLayout`** —
  and again from `CooldownViewerMixin:SetTooltipsShown`, which walks every active frame when the
  player changes the setting. So the client re-asserts non-clickability on a schedule we do not
  control, and re-enabling it from tainted code would be a standing re-assert war against a
  deliberate Blizzard setting. An earlier draft reached the config by clicking the icon itself;
  that route is dropped, and the dropdown replaces it.
- **Built-in profiles live in the addon source, not in SavedVariables.** A `Profiles.lua`
  carrying named rule sets is edited, deployed and `/reload`ed. Hand-editing SavedVariables was
  considered and rejected as the supported path: `/reload` **commits SavedVariables from memory
  before reloading** (`ADDONS_UNLOADING`, `anatomy-and-runtime.md:955`), so an edit made while
  the client is running is overwritten. The paste box is the escape hatch for anything not
  pre-baked.
- **Terms resolve against the icon's currently-bound spell**, with `base(...)` to force the
  static ID. Chosen because it matches what the player is looking at; Demonbolt/Shadow Bolt,
  Ruination and Metamorphosis are the cases that bite. Stated in §1 and §5.
- **v1 has one look, in nine colours plus the `alarm` cycle** — a hexagon outline centred in
  the icon over a translucent purple plate that turns with it, swinging black↔yellow, popping
  when `urgent`, on both sinks. It is
  deliberately the SAME mark either way, which is what makes the gate/binding
  split invisible to the player, and under the occluder form it is literally the same object:
  **both sinks reveal one Texture we own**, so both reach `SetVertexColor` and both turn. What
  the escape carries is the *occluder*, and an occluder wants no hue at all — it is a copy of
  the icon. That is what took colour and motion off the list of things the two sinks differ on.
  ⚠ It is also why a colour escape's known limit no longer bites: `|T` art is untintable
  (measured full white against a `SetVertexColor` control on the same row `[client 2026-08-22]`),
  and nothing we tint is drawn by an escape any more. A fuller look vocabulary is still a later
  question.
- **Evaluation triggers come from a term catalogue.** Each term declares the events that can
  change its answer; a glow's trigger set is the union over its leaves. No blanket `OnUpdate`.
  Sealed **duration** leaves are the exception — a curve evaluation is a snapshot (§2), so they
  are re-armed on a **10 Hz** ticker, and only a glow that uses one pays for it.
- **A glow attaches to the subject's cooldown row, and to zero or one of them.** Essential and
  Utility are **mutually exclusive** placements of the same row, not two frames — the drag
  table moves rather than copies, and `GetValidAssignmentCategories` only ever offers
  categories from the tab currently open `[T1 src @12.1.0: CooldownViewerSettings.lua —
  GetValidAssignmentCategories]`. A subject with **no** frame reads **UNKNOWN** in `/sg why`,
  never silently nothing. The aura-family row a spell may separately carry
  (TrackedBuff/TrackedBar) answers a different question — *is this running* rather than *can I
  press this* (`cooldown-manager.md` §1.1) — and is out of scope for v1.
- **The wire payload is JSON**, as `SG1:` + `EncodeBase64(CompressString(SerializeJSON(ast),
  Deflate))`. §7 records why the tab-separated alternative lost.

**Reversed after the APL exercise (§10):**

- **The surface is TWO BOWLS — `when` and `bind` — not one expression.** This overturns the
  earlier "one expression, one keyword" decision. The reason is `README.md`'s founding rule:
  an unevaluable rule must be *impossible to author*, and only a structured surface enforces
  that; a single expression with a checker behind it puts the asterisk on afterwards, which is
  the TellMeWhen failure. The mis-sorting that killed the original `when`/`while` split is
  handled by the tool owning the classification and refusing a term by the bowl it belongs to.
- **DNF-as-layering is the general composition rule.** Any expression distributes; one glow per
  disjunct; §8's independent layers do the OR on screen. Only a disjunct carrying two sealed
  leaves needs §2's nesting.

---

## 9. Open

**Client facts** — all in `knowledge/addon-dev/`. None of them blocks anything:

- Whether re-arming a count sink actually redraws — `aura-sink-recall`, parked; see §1.
- Whether a `LuaDurationObject` tracks later casts or is a snapshot. The KB's "cache the
  object and re-read it" reads as snapshot but is not stated as measured.

---

## 10. Worked against real APLs

**This is the evidence the two-bowl surface works, and it is the only section written against
priority lists nobody authored for this document.** Every rule below is a transcription of a
line from `knowledge/classes/**/simc-apl.md` at 12.1.

The Demonology block is no longer an exercise: it ships as the `demonology-diabolist` profile,
with `rules/demonology-diabolist.sg` as its on-disk twin. Two lines below differ from what
shipped, and both differences are the sketch being wrong rather than the language —
`tyrant.cooldown` is not a name the symbol table carries (`summon_demonic_tyrant` is), and the
Dreadstalkers line's `talent(reign_of_tyranny)` is inverted, since Reign banks imps for the
Tyrant instead of spending them on demand.

### Demonology — the `diabolist` list

```
glow "Tyrant at five shards"          glow "Hand of Gul'dan — dump"
  on    summon_demonic_tyrant           on    hand_of_guldan
  when  soul_shards == 5                when  soul_shards >= 3
                                        bind  tyrant.cooldown > 5s

glow "Dreadstalkers window"           glow "Hand of Gul'dan — capped"
  on    call_dreadstalkers              on    hand_of_guldan
  when  talent(reign_of_tyranny)        when  soul_shards == 5
  bind  tyrant.cooldown outside 12s..20s

glow "Demonbolt on a Core"            glow "Implosion at six imps"
  on    demonbolt                       on    implosion
  when  soul_shards < 4                 when  ready(implosion) and talent(to_hell_and_back)
        and aura(demonic_core)          bind  wild_imp.stacks >= 6
```

### Havoc and Retribution

```
glow "Essence Break"                  glow "Blade of Justice on a proc"
  on    essence_break                   on    blade_of_justice
  when  ready(essence_break)            when  ready(blade_of_justice)
  bind  eye_beam.cooldown > 4s                and (aura(art_of_war) or aura(righteous_cause))

glow "Death Sweep in the window"      glow "Spend at five"
  on    death_sweep                     on    templars_verdict
  when  ready(death_sweep)              when  holy_power == 5
        and aura(essence_break, target)       and not ready(wake_of_ashes)
                                              and not aura(hammer_of_light_ready)
```

### What the exercise established

**The binding budget is nearly free.** Counting the Demonology list: **14 priority lines — 10
need no bind at all, 3 need exactly one, 1 needs vocabulary we do not have, and none needs
two.** Across all three specs the one-bind limit was reached exactly once, on Havoc's Vengeful
Retreat, which is a GCD-alignment micro-optimisation rather than a rule a person would author.

**The two Hand of Gul'dan glows are one APL line.** `soul_shard>=3&cooldown...>5|soul_shard=5`
distributes into two glows that composite on screen, and it reads better split than joined —
which is the DNF-as-layering claim tested rather than asserted.

**Retribution barely needs bowl A at all.** `cooldown.wake_of_ashes.remains` in its finisher
gate is simc for *"not ready"* — a boolean wearing a duration's clothes, and an ordinary gate.

**What actually blocks a line is VOCABULARY, not structure.** In priority order:

| missing term | what it blocks |
|---|---|
| **enemy count** | the real Implosion condition, Divine Storm, every AoE branch — by far the most wanted |
| GCD remaining | Havoc's off-GCD weaves |
| time in combat | opener-only lines |
| guardian active | *"is Tyrant out"*, which gates Demonology's whole burst list. ⚠ Diabolist has a way around it: Dominion of Argus's buff window **is** the Tyrant window, so `aura(...)` on its tracked row answers the same question — a per-spec substitute, not the missing term |

And two things are unreachable rather than missing: `fight_remains` / `target.time_to_die`,
which the client does not know either, and `raid_event.*`, which is a simulator construct with
no in-game referent.

---

## 11. Provenance

Every client fact above is cited to `knowledge/addon-dev/`, which is the authority; this file
paraphrases and must not be treated as a source. Four facts were established by this project's own lab
flights on 2026-09-08:

- `OBS-085` — every duration-object getter is secret, and an armed widget's `GetCooldownTimes`
  reads secret too, so a cooldown threshold **cannot** be reified into a boolean and genuinely
  is a binding. Every mutator is an absolute overwrite, which closes the time-shift route.
- `OBS-086` — alpha, scale, translation and rotation **all** animate on a sealed FontString,
  so a count cue is fully animatable rather than a static glyph.
- `OBS-087` — **nesting is an AND over two sealed values**, which completes the boolean algebra
  in §2 and means the language never has to refuse a combination on composition grounds.
- Unnumbered, and learned by getting it wrong: a **curve evaluation is a snapshot, not a
  binding** (§2). It cost a flight whose tiles only changed when the panel was rebuilt.

⚠ **Combat Assist Plus solved a structurally similar problem and is NOT precedent here.**
What legitimately crossed from it is *mechanism* — the authored-formatter route, why two
secrets cannot share a widget, that a third truth value is unavoidable. Its **decisions** —
its DNF-only condition shape, its closed draw vocabulary, its cue polarity rules — were made
against a different product's goals and were re-decided here from scratch. See this project's
`CLAUDE.md`.
