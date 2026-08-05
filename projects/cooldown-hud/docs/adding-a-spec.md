# Cooldown HUD — recipe: adding a new spec

> **What this is.** A step-by-step pattern for teaching the HUD a second (third, …) spec,
> now that the multi-spec refactor is complete (`multispec-plan.md`, all 6 phases done
> 2026-07-29). The framework is one spec-agnostic pipeline + a per-spec brain that plugs
> in; adding a spec is **additive** — a docs folder, two Lua files, a `.toc` line pair, and
> a test. **You do not touch the pipeline** (State / Coach shell / Binder / Renderer /
> DecisionLog).
>
> ## ⚠ CORRECTIONS FIRST — read this box before the recipe (2026-08-02, +2026-08-03)
>
> The recipe below is **broadly right and specifically stale in ten places**. It was
> written before hero talents, virtual rows and the Phase-6/6.2 refactors, and
> **Retribution Paladin (70)** — the first non-Warlock spec — was authored against it and
> found the first seven. **Havoc DH (577)** added two more (8 and 9) at the desk, and a
> **tenth in game** — correction 0 below, which is the one that changes the rotation model
> before a line is written. Fix the recipe in your head as you read:
>
> 0. ⚠⚠ **ASK WHETHER THE SPEC'S RESOURCE IS SECRET, IN STEP 0, BEFORE ANYTHING ELSE.** The
>    recipe assumes throughout that a rotation can compare a resource against a threshold. For
>    **most specs in the game it cannot**, and this cost the project a whole flight
>    (2026-08-03, Havoc — `docs/multi-class-rollout.md` → § FLIGHT RECORD).
>
>    `UnitPower` secrecy is **per power type**, and the rule is **primary vs. secondary
>    resource** (Blizzard blue post, *Midnight Public Alpha Addon API Changes*, 2025-11-24).
>    The **seven never-secret** types are **Combo Points, Runes, Soul Shards, Holy Power, Chi,
>    Arcane Charges, Essence**. Everything else — **Mana, Rage, Focus, Energy, Runic Power,
>    Fury, Pain, Insanity, Maelstrom** — is **secret**. Check it directly:
>
>    ```lua
>    /dump C_Secrets.GetPowerTypeSecrecy(<Enum.PowerType.X>)   -- 0 NeverSecret · 2 Contextual
>    /dump C_Secrets.ShouldUnitPowerBeSecret("player", <X>)
>    ```
>
>    ⚠ **`ContextuallySecret` (2) on a player's own PRIMARY resource means SECRET FOREVER** —
>    the "context" is the *unit*, not combat, and it measured `true` in a city and mid-pull
>    alike. **Do not plan an out-of-combat seed; there isn't one.** ⚠ `UnitPowerMax` is a
>    *different* predicate and **is** readable, so a readable max next to an absent value is
>    the expected shape, not a bug.
>
>    **If it is secret, three things change before you write `rotation.md`:**
>    - **No resource-threshold gate may be written at all** — not degraded, not approximated.
>      Affordability comes from `C_Spell.IsSpellUsable(id)`'s **second** return,
>      `insufficientPower` (`ns.SpellUsable`; State attaches it per-ability, fenced on the
>      spec's `spends`). ⚠ Use `insufficientPower`, **never** `isUsable` — the latter was
>      measured `true` for a spell visibly on cooldown.
>    - **Overcap / pooling rules are unexpressible.** `IsSpellUsable` is binary. Drop them and
>      say so in the deviations rather than approximating.
>    - **Ordering carries the resource instead.** Blizzard's own assisted-combat lists for
>      such specs use **generator → spender → generator** with the spender repeated, and no
>      threshold anywhere. Copy that shape.
>
>    ⚠ **The DB2 `SpellPower` sweep becomes informational** for such a spec: there is nothing
>    to compare a cost against, and **DB2 costs disagree with the live client anyway** (DB2
>    says Throw Glaive costs 25; the client reports it **free**).
>
>    ⚠ **And the fixture rule that would have caught it:** if the spec's oracle can hand the
>    brain a resource *number*, it cannot reproduce the only state the game ever produces. A
>    secret-resource spec's pulse fixture must default to a **restricted** rail.
>
> 1. **`spec.SpecPowerDelta` is NOT read by State any more.** Step 2 and the Tier-1 table
>    both say State reads it for the in-flight projection. Phase 6 moved that to the
>    brains via **`ns.Coach.InflightPower`**, which takes the delta function as a
>    parameter. Your brain calls it from `Context`; State never sees it.
> 2. **The six "shell-read" `spec.Spec` fields are wrong in both directions.** Of the listed
>    six, **`emphasis` and `transform` have ZERO readers** in the v1 pipeline. And
>    **`expect` is load-bearing and missing from the list**: `State.lua`'s virtual-row walk
>    auto-promotes an untracked `kind = "button"` ability with no base cooldown into a
>    self-drawn icon, so an **alias** that passes those fences draws a *duplicate* beside
>    the real one. Every override/alias entry needs `expect = false`.
> 3. **`SHARD_CAP` is now `FRAG_CAP`**, `spec.powers` entries need **`modifier`**, and the
>    `FRAG_CAP` / `BAR_MAX` / `FRAGS_PER_SHARD` trio the Warlock specs carry is undocumented
>    here. Since the **`ns.Coach.PowerContext` hoist (2026-08-02)** the per-power fallbacks
>    live on the `spec.powers[]` entry as **`modifier` / `exactMax` / `barMax`** — that is
>    what a new spec fills in.
> 4. **Step 5's Renderer reasoning is superseded, twice.** Its two "generalization points"
>    are gone: `PowerBarColor` was never the blocker, and **`display = "none"`** (added to
>    `guidance-contract.json` 2026-08-02) means a spec can track a resource without drawing
>    anything, which is what the five Paladin/DH specs use. `drawResourceRow` also now
>    **clamps** the pip pool (`MAX_PIPS`), so a raw-unit `max` can no longer pool 50
>    textures. See `status.md`'s note on the spent "State cannot read the fraction" reason.
> 5. **Step 0 says to fetch APLs with `wowkb.simc`.** The **full simc clone is on disk** at
>    `~/code/fun/wow/raw/addon-research/simc` (branch `midnight`) and is strictly better —
>    it carries `ActionPriorityLists/default/*.simc` for specs the MID1 profiles lack
>    (Protection Paladin among them). ⚠ **Do NOT use `ActionPriorityLists/assisted_combat/`**
>    — that is Blizzard's one-button rotation from the `AssistedCombat*` DBC tables and it
>    is a *suboptimal* rotation, not a second Tier-1 opinion.
> 6. **It predates hero talents entirely.** `state.hero` carries the active tree
>    (`State.lua`'s `HERO_BY_SUBTREE`, `TraitSubTree` @ 12.0.7). A brain must read it off the
>    pulse and **never infer it from the tracked set** — that inference is field-fix B, and it
>    confidently returned the wrong tree on Destruction's first live session.
> 7. **It predates virtual rows.** An ability the CDM tracks nowhere can still get an icon
>    if it passes `State.virtualCandidates`' fences (`kind = "button"`, non-utility,
>    `expect ~= false`, not already on screen, `ns.BaseCooldown == 0`, and **known**).
> 8. **It never mentions `spec.SpecBindAlias`, which is not optional for every spec.** Where
>    `SkillLineAbility` teaches a **wrapper** spell whose only effect is
>    `trigger -> <the tracked id>`, the keybind rung ladder asks the action bar about the
>    tracked id, finds nothing, and the icon silently loses its key hint — no error, no log
>    line. Havoc needs two aliases (Chaos Strike 344862 → 162794, Fel Rush 344865 → 195072).
>    **Add "does the SkillLine teach this exact id?" to Step 0.**
> 9. **It treats "the CDM filed this Utility" as decisive, and it is not.** The field that
>    makes an ability cueable is the **spec-authored `cadence`**; both fences that could block
>    a press (`Coach.lua:501`, `State.lua:1941`) test that, never the CDM category. Three of
>    Havoc's rotational presses are CDM-Utility and needed **no pipeline edit at all**.
>
> **One more thing the Retribution run learned, which is not a correction but a warning:**
> **`SpellName` is full of homonyms and resolving one by eye is how bugs get in.** There are
> **eight** spells called "Hammer of Light" and three called "Hammer of Wrath" on the Paladin
> side alone. Resolve a name by a **property only the real spell has** — a Holy Power cost in
> `SpellPower`, a shared `ChargeCategory` in `SpellCategories`, membership of the spec's
> `CooldownSetSpell` rows — never by picking the plausible-looking number.

> **Status: reference pattern, not yet a skill — now EXERCISED THREE TIMES** (Destruction,
> Retribution, Havoc). Derived from how
> Demonology (266) is wired (`SpecDemonology.lua` + `CoachDemonology.lua`) and verified
> against the live code 2026-07-29. **Destruction (267) was then added by following it
> end to end** the same day, with no pipeline edit, no Renderer edit and no contract edit —
> so the recipe is confirmed, not just asserted. **Retribution (70) followed on 2026-08-02**,
> and it is the more informative run precisely because it is the first spec *outside
> Warlock*: it needed a Renderer edit, a contract edit and a shell-kit hoist, all of which
> the recipe said would not be necessary. What the two runs learned:
>
> - **Step 5 held**, and the *conclusion* outlived its *reason* — read both. Destruction
>   rides the same `SOUL_SHARDS` token rendered `discrete`, so neither Renderer
>   generalization point was touched. The draft docs predicted a `resourceDisplay` contract
>   edit for its fragment bar and that prediction is still wrong; but the ORIGINAL reason —
>   *"State cannot read the fraction, so an enum member would advertise precision we do not
>   have"* — **is SPENT as of Phase 6.2 (2026-08-01)**. State reads the exact 0–50 rail now
>   and the brain decides in fragments. What keeps the enum closed is that `Renderer.lua`
>   pools **one pip texture per unit of `max`** and has no fractional path. The lesson
>   survives with a sharper edge: **check what State can actually READ before concluding the
>   contract must grow — and when the read lands, re-check whether the RENDERER can use it,
>   because those are two separate gates.** The contract change Phase 6.2 did make was purely
>   **additive** (`valueExact`/`maxExact`/`incomingExact`/`modifier` on each resource bar),
>   which is the shape to copy: grow the payload, not the enum.
> - **Step 2's "don't guess IDs" extends to don't guess NUMBERS.** Demonology told its two
>   Demonic Art transforms apart by `generates == 3` — a rotation decision coupled to a
>   tuning constant — and both specs now branch on the semantic `art` field instead.
>   Destruction's Infernal Bolt *does* carry a yield today (`generatesFrags = 20`, Phase
>   6.2), which is precisely why identity had to stop being inferred from arithmetic:
>   **identity beats a quantity even when the quantity is real.**
> - **The Tier-3 omission is real, and safe.** All nine dormant tables were left out and
>   nothing broke — `ns.SetActiveSpec` nils them and no live module reads them.
> - **Expect one genuinely NEW open question per spec, and park it as a one-line switch.**
>   Destruction's was "what does *Art armed* actually read off?" — the spec docs proposed a
>   source that turned out to be a ritual *container*, not the proc. It became
>   `spec.ART_FROM_RITUAL = false`, defaulted to the safe reading, for the in-game pass to
>   settle. Better than either guessing or blocking the whole spec on it.
>
> **What the RETRIBUTION run learned (2026-08-02) — the first non-Warlock spec:**
>
> - **"You do not touch the pipeline" held for a second spec of the same class, and stopped
>   holding at the third.** Destruction needed no pipeline edit because it rode Demonology's
>   resource. Retribution needed three, and every one was a *generalisation the seam had
>   been deferring*, not a special case: `display = "none"` in the contract + Renderer
>   (a spec that tracks a resource it does not draw), the `ns.Coach.PowerContext` hoist (the
>   ~15-line block both Warlock brains had copied), and the `HERO_BY_SUBTREE` vocabulary.
>   **Read the rule as "a spec adds no pipeline BRANCH", not "a spec adds no pipeline line".**
>   The test is whether the edit is spec-agnostic when you are done, and all three were.
> - **The genuinely new open question was structural, not numeric.** Destruction's was "what
>   does Art armed read off?"; Retribution's is **"is a 1-charge charge-category ability
>   marked `charges = true` on the CDM row?"** — because *four of its nine* Essential buttons
>   (*"six" until 2026-08-03*) have `SpellCooldowns.RecoveryTime = 0` and keep their cooldown
>   on a **charge category**. That makes `ns.BaseCooldown` return 0 and the **napkin blind on
>   those four** — readiness survives on the charge count; `SOON` and the overdue call do not.
>   Destruction met this once (Conflagrate, field-fix C2). **Check
>   `SpellCategories.ChargeCategory` for every rotation button during Step 0** — it changes
>   how much of the readiness model you actually have.
> - **`spec.derived` exists now** for a class resource `Enum.PowerType` cannot carry (Demon
>   Hunter Soul Fragments). Retribution does not use it; Vengeance and Devourer do. It is a
>   declaration State reads, not a branch State runs — `{ name, kind, spellID, max }`.
> - **The parked one-line switch is a repeatable pattern, not a Destruction quirk.** Expect
>   exactly one per spec. Retribution's is `RET_HOL_FROM_BUFF`.
>
> **What the HAVOC run learned (2026-08-03) — the 4th spec, 2nd class outside Warlock:**
>
> - **THE FIELD THAT MAKES AN ABILITY CUEABLE IS `cadence`, NOT THE CDM CATEGORY.** Three of
>   Havoc's rotational presses (Felblade 232893, Vengeful Retreat 198793, Fel Rush 195072)
>   are filed **Utility** by Blizzard, and the rollout plan budgeted a pipeline edit for it.
>   There is none to make: both fences that could block them — the SOON fence
>   (`Coach.lua:501`) and the virtual-row fence (`State.lua:1941`) — test the **spec-authored
>   `info.cadence`**. Declaring them `"filler"` / `"oncd"` is the whole fix; the CDM category
>   only decides which viewer frame they draw on and how a claim is ranked when two roster
>   entries contest one row. ⚠ **Do not read a CDM-Utility filing as "the HUD cannot cue
>   this."** The next tank spec will meet the same shape at scale.
> - **A WRAPPER SPELL ON THE ACTION BAR IS A `SpecBindAlias` CASE, and Step 0 should look for
>   it.** `SkillLineAbility` can teach a *wrapper* whose only `SpellEffect` is
>   `trigger -> <the real id>`, and the CDM tracks the **real** id. Havoc has two (Chaos
>   Strike 344862 → 162794, Fel Rush 344865 → 195072). The rung ladder asks the action bar
>   about the tracked id, finds nothing, and the icon **silently loses its keybind hint** —
>   a failure with no error and no log line. **The check: for every declared button, does the
>   spec's SkillLine teach that exact id, or a different one that triggers it?**
>   ⚠ This is *not* the same as an override — an override rides a frame whose **base** id IS
>   on the bar, which the ladder already resolves. Only the wrapper needs an alias.
> - **A PARKED SWITCH NEEDS A QUESTION A FLIGHT CAN ANSWER.** The obvious candidate for
>   Havoc's switch was the Reaver's Glaive spend sequence — and it should **not** have been
>   one: `Rending Strike` 442442, `Glaive Flurry` 442435 and `buff.reavers_glaive` 442294
>   have **no `CooldownSetSpell` row**, so there is no presence channel on any surface the
>   addon can reach, and no in-game observation could ever flip the switch on. Machinery
>   behind a switch nothing can flip is worse than an honest documented gap. The real switch
>   became `HAVOC_RG_FROM_BUFF` — *may an 80-stack counter's presence count as "armed"* —
>   which is the `RET_HOL_FROM_BUFF` shape and **is** flight-settleable.
>   **Test before parking: "what would I look at in the decision log to decide this?"** No
>   answer ⇒ it is a documented deviation, not a switch.
> - **A LYING BASE COOLDOWN IS A DISTINCT FAILURE FROM AN ABSENT ONE, and it is worse.**
>   Retribution's four charge-category buttons read **0**, which trips HudNapkin's
>   declared-`chargeCD` fence (`not (len > 0)`) and gets the fallback. Havoc has **three that
>   read a WRONG POSITIVE NUMBER** — a short *shared-category lockout* on the spell row while
>   the real recovery lives on a charge category — and a lying `1` **passes** that fence, so
>   no declared constant can rescue it. **Step 0 must compare `RecoveryTime` /
>   `CategoryRecoveryTime` against `SpellCategory.ChargeRecoveryTime` for every button, not
>   merely check whether a base cooldown exists.** What saved Havoc was incidental: all three
>   are **1-charge** categories, so `usable()`'s one-charge rule lets the count veto the early
>   read. On a 2-charge pool it would not have.
> - **Zero pipeline generalisations is a legitimate outcome, and so is one.** Retribution
>   needed three; Havoc needed none. The number is not a quality signal in either direction —
>   what matters is that the two worries the plan *had* budgeted for both dissolved on
>   inspection (the CDM-Utility one had no fence to change; the lying-cooldown one was
>   already mitigated), and shipping a pipeline edit against a symptom nobody has observed is
>   how a guard outlives its reason. **Defer it to the flight and record the exact one-line
>   shape it should take.**
> - **The genuinely new open question was a MEASUREMENT, not a structure:** *does the charge
>   count actually arrive for a 1-charge category?* — because that count is the entire
>   mitigation above. Note it is the same question Retribution's run raised, now
>   **load-bearing** rather than merely interesting. A question that recurs across specs with
>   rising stakes is a sign the read belongs in the shared readability write-up, not in a
>   per-spec observability map.
> - **Cross-ability timing gates have a rule now.** simc is full of `cooldown.X.remains <= N`
>   gates on *other* abilities, and a client cooldown read is secret in combat — Retribution
>   dropped its whole Execution-Sentence/Wake-of-Ashes handshake for that reason. Havoc's L5
>   keeps one, reading **our own napkin's** `remaining` for Eye Beam. **The rule: a
>   cross-ability timing gate is allowed when the OTHER ability's cooldown is one the napkin
>   can HONESTLY count** — i.e. it lives on the spell row, not a charge category. Wake of
>   Ashes fails that test; Eye Beam passes. Flag any such line at the line, in the tunable
>   and in `rotation.md`, as the first suspect for that ability misbehaving.
> - **A "hard state fork" in simc is usually a DISPLAY OVERRIDE in the client.** Havoc's
>   `run_action_list,name=meta` is a second complete priority list where the same buttons mean
>   different things — and it collapsed to **one cascade with `ctx.inMeta` on two lines**,
>   because both overrides are 1:1 replacements riding their own base's frame. **Before
>   modelling a fork, check whether it is really an `EffectAura 332` override**: if it is, the
>   Coach cues the base, the icon supplies the label, and the fork is only about ORDER. Then
>   read the two lists side by side and record **exactly which orderings differ** — for Havoc
>   it was two out of fifteen.
> - **A `CumulativeAura = 0` on a TrackedBuff row usually means you have the TALENT id, not
>   the aura id — and it costs nothing to key on the tracked one.** `state.buffs` is keyed by
>   the **CDM row's** spellID (`State.lua:2304`) and the channel is `item:IsActive()`, a
>   **bool**, so a stack count was never reachable whichever id you declared. Declaring the
>   *real* aura instead creates a roster entry with **no CDM row**, which Coverage reports as
>   BLIND. **Declare the tracked id; put the real aura id in a comment.**
>
> May be converted into a skill later — keep it faithful to the code so the conversion is
> mechanical.
>
> **Doc map:** the technical contract is `architecture.md` (invariant #3 + "Settled
> decisions → Spec resolution"); the design + phasing that built the seam is
> `multispec-plan.md`; the live worklist is `status.md`. This recipe is the *how-to* those
> three imply.

---

## Source the data offline — the readability rules are already settled

The Secret-Values / cooldown-readability rules are settled **game-wide invariants** — they
are properties of the API + Secret-Values model, not of the spell, so a new spec obeys them
exactly as Demonology does. (These were discovered by the old `/cdmp probe`, retired
2026-07-29 once they were nailed down.) Do **not** re-verify them per spec:

| Settled rule (never re-check per spec) | Consequence for spec data |
|---|---|
| `C_Spell.GetSpellCooldown` reads **secret in combat**, real OOC (full DB incl. unlearned) | The napkin fills combat readiness; nothing to measure. |
| `UNIT_SPELLCAST_START` / `SUCCEEDED` spellIDs are **readable in combat** | The history/napkin inputs work; nothing to measure. |
| `item:IsActive()` is a **readable bool in combat** (the canonical proc/buff-presence signal) | If it worked for Demo it works for your spec. |
| `IsSpellOverlayed` glow **readable in combat**; `C_UnitAuras` **dead in combat** | Proc source = `buff.isActive` + glow, OOC aura = enrichment. |
| Override/transform fires via `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` + live-identity divergence | The transform channel works; you only need the *IDs*. |

The genuinely **spec-specific** data all comes from **offline sources**:

- **The tracked set (Essential / Utility / TrackedBuff / TrackedBar)** —
  `wowkb.spec_inventory --spec <spec>`, which reads it from the wago `CooldownSet` /
  `CooldownSetSpell` DB2 tables (the Cooldown Manager's own per-spec tracking config, keyed
  by `ChrSpecialization`). That is where per-spec CDM membership lives.
  - ⚠ **There is no per-spec table in Blizzard's CDM *Lua* source.** `Blizzard_CooldownViewer`
    hardcodes only the four *categories* (`cooldownCategories = { Essential, Utility,
    TrackedBuff, TrackedBar }`, `CooldownViewerSettingsDataProvider.lua:40`) and fetches the
    current spec's spells at runtime via `C_CooldownViewer.GetCooldownViewerCategorySet(category,
    allowAll)` (`:85`) — the same C-API our `State.lua` uses. So the offline door is DB2
    (`spec_inventory`); the runtime door is that API (current spec only). Don't go hunting the
    Lua source for a per-spec spell list — it isn't there.
  - **The data *shape*** each entry returns is the `CooldownViewerCooldown` struct in
    `Blizzard_APIDocumentationGenerated/CooldownViewerDocumentation.lua` (`cooldownID`,
    `spellID`, `overrideSpellID`, `overrideTooltipSpellID`, `linkedSpellIDs`, `selfAura`,
    `hasAura`, `charges`, `isKnown`, `flags`, `category`) — mirrored in `architecture.md`'s raw
    `cooldowns` shape. (Grep the source clone — see `knowledge/addon-dev/sources.md` §1.1.)
- **The rotation / APL** — `wowkb.simc <class> <spec>` (the Tier-1 default APL).
- **Named IDs, override/transform pairs, proc IDs** — simc + wago DB2 (`spec_inventory`
  surfaces the cdm-only residue and annotations).

So author from `spec_inventory` + `simc`, not from a capture. Demonology's data scars (the
Singe Magic pet-override hole, the Imp Lord entry-id-vs-cast-id bug) came from guessing IDs
*before* those tools existed — the tools are the fix.

**One in-game confirmation is still worth it (a check, not a gate):** the *default* tracked
set from DB2 can differ from what actually loads for a build — the Destruction draft's open
worry is exactly this ("Incinerate appears untracked"). A single **`/cdmp hud layout`** on a
real character of the spec lists the live tracked icons + resolved keybinds, **confirming the
predicted set** and catching a build-surprise. That is a one-time sanity check, not a
prerequisite. If a spec ever *violates* an established contract (something that worked for
Demo doesn't for it), that is a genuine surprise worth a new testing layer **at that point** —
don't pre-build one.

---

## Mental model — generic vs per-spec

The pipeline reads a **small, fixed surface** off the active spec object and nothing else.
Everything a spec provides falls into three tiers:

### Tier 1 — the surface the generic pipeline actually reads (REQUIRED)

| Symbol | Read by | Contract |
|---|---|---|
| `spec.SpecInfo(spellID) → info, known` | Coach shell (`Classify`), `DecisionLog` | Never errors, never keys on a secret; returns a neutral fallback + `false` for unknown/secret IDs. |
| `spec.SpecIDs` | your brain, `Probe` (diagnostics) | Named-ID table (`{ TYRANT = 265187, … }`). |
| `spec.SpecPowerDelta(spellID) → { power, delta }` | `State` (the in-flight `incoming` projection) | Signed net power delta of an in-flight cast + which named power it moves; `{ power = nil, delta = 0 }` for a no-op. |
| `spec.powers` (ARRAY) | `State`, Coach shell, `DecisionLog`, your brain | `{ { name, display, incoming, token } }` — one entry per rendered power. Read off `ns.ActiveSpec.powers` (an object read, **not** a rebound global). |
| `spec.log` (table) | `DecisionLog` | `{ cdOrder, procOrder, procBuffs, … }` — the decision-log vocabulary (below). Read off `ns.ActiveSpec.log`. |
| **`spec.Spec` bucket fields** the shell reads: `emphasis`, `kind`, `cadence`, `label`, `abbr`, `transform` | Coach shell `Emit`/`Classify`, `DecisionLog` | Every other bucket field is **your brain's private convention**. |
| `spec.SpecBindAlias` | `HudBinds` | **Optional** — only if a cast/tracked ID differs from the action-bar ID (Imp Lord's case). |

### Tier 2 — the brain (REQUIRED, attached by `Coach<Name>.lua`)

Three methods hung on the same spec object, plus tunables as `self.*`:

- `spec:Context(state, env) → ctx` — fold the pulse into whole-board facts.
- `spec:RankWinner(ctx, excluded) → winnerKey, level, note` — the flat priority list.
- `spec:Escalate(winnerKey, level, ctx) → level` — `ROTATION → LATE` from *readable*
  overdue-ness only.

### Tier 3 — carried but dormant (SKIP unless a feature revives it)

`ns.SpecFields` (in `SpecRegistry.lua`) rebinds a longer list of globals for back-compat,
but several have **no live consumer in the v1 pipeline**: `SpecGroups`, `SpecColor`,
`SpecPole`, `SpecGhost`, `SpecNoCue`, `SpecProcGlow`, `SpecStacks`, `SpecOpener`,
`SpecBurst` (the last five are old-engine render/sequence data; v1 colours cues by
`emphasis`, not group hue, and has no sequence panel). **A new spec can omit them.** Don't
copy Demonology's `SpecGroups`/`SpecOpener`/`SpecBurst` wholesale thinking the HUD needs
them — it doesn't today. (Some *bucket* fields like `spends`/`generates` look dormant to
the pipeline but are read by the Demo *brain* — those are Tier-2 private, keep whatever
your brain reads.)

---

## The recipe

### Step 0 — source the data
Have `wowkb.spec_inventory --spec <spec>` (the tracked set + IDs) and `wowkb.simc <class>
<spec>` (the APL) output for the target spec in hand — see the offline-sourcing section above.

### Step 1 — author the spec docs (`specs/<spec>/`)
Clone the four-file set every spec carries (see `demonology/` and the `destruction/`
draft):
- `rotation.md` — the flat priority list (the APL your `RankWinner` implements), distilled
  from the Tier-1 simc APL (`wowkb.simc <class> <spec>`).
- `notes.md` — ability roster, procs, resource mechanics, blind spots.
- `input-contract.md` — the evaluator's inputs.
- `observability-map.md` — what the game exposes vs. hides for this spec.

Mark them **DRAFT** with a status banner until the live capture confirms them (the
Destruction folder is the template for honest draft banners).

### Step 2 — the data file `Spec<Name>.lua`
Clone `SpecDemonology.lua`'s shape. Fill:
- `local spec = {}`.
- `spec.SpecIDs` — named IDs, **from `spec_inventory` + simc** (real cast/tracked IDs, real
  override/transform IDs — not maxroll guesses).
- `spec.powers` — the ordered power array. **`token`** is the game `Enum.PowerType` name
  (e.g. `"SOUL_SHARDS"`, `"BURNING_EMBERS"`); **`display`** is a `resourceDisplay` enum
  member from `guidance-contract.json` (`discrete` | `percentage` | `continuous`). List
  two entries for a dual-resource spec (energy+combo, runes+runic power).
- `spec.log` — the decision-log vocab (see Step 6).
- `spec.Spec` — the per-ability bucket table. Carry the six shell-read fields (`emphasis`,
  `kind`, `cadence`, `label`, `abbr`, `transform`) plus whatever your brain reads.
- `spec.SpecInfo` / `spec.SpecPowerDelta` — clone Demo's helpers; they're the two
  functions the pipeline calls. Keep `SpecInfo`'s secret-guard (`ns.IsSecret`) and neutral
  fallback verbatim — that guard is load-bearing (a Secret Value used as a table key
  taints).
- `spec.SpecBindAlias` — only if needed.
- **Self-register at the bottom:** `ns.RegisterSpec(<specID> --[[ <SpecName> ]], spec)`.
  **Registration is static; activation is the resolver's job** — do **not** call
  `SetActiveSpec`.

### Step 3 — the brain file `Coach<Name>.lua`
Clone `CoachDemonology.lua`'s shape:
```lua
local ADDON, ns = ...
local spec = ns.Specs[<specID>]   -- the object registered by Spec<Name>.lua
spec.<TUNABLE> = …                -- seconds/resource tunables as fields on the object
function spec:Context(state, env) … return ctx end
function spec:RankWinner(ctx, excluded) … return winnerKey, level, note end
function spec:Escalate(winnerKey, level, ctx) … return level end
```
Rules the Demo brain follows and yours must too:
- **Decide in BASE spellIDs** (the domain view keys `state.abilities`/`buffs`/`power` by
  base spellID). cooldownID is transport the Binder owns — it never appears in your brain.
- **Build `ctx.powers`** from `self.powers × state.power[name]` (copy Demo's loop) so the
  shell's `ResourceBars` can emit `resourceBars[]`.
- **`RankWinner` is a flat cascade**: top-to-bottom, first usable line wins; honour
  `excluded` at every line that names it (so the shell can recompute the honest runner-up).
- **`Escalate` only from readable state** — never escalate on a secret-gated quantity.
- Resolve live costs through `env.shardCostFn` (the injected reader), with a fallback
  constant on the object — never hardcode a talent-dependent cost.

Load-order safety: the `ns.Coach.*` references inside your methods are runtime-only, so the
brain file may load before `Coach.lua`.

### Step 4 — wire the `.toc`
Add the two files to `CDMProbe/CDMProbe.toc` **after `SpecRegistry.lua`**, data before
brain, both before `Coach.lua` (matching the Demo ordering):
```
SpecRegistry.lua
SpecDemonology.lua
CoachDemonology.lua
Spec<Name>.lua          ← new
Coach<Name>.lua         ← new
…
Coach.lua
```

### Step 5 — resources: mind the two Renderer generalization points
The Renderer is ~95% agnostic, with two **known** edges (`status.md` audit / multispec-plan
§4). Hitting either is a **Renderer code change** (→ release), not just spec data:
- **Power colour** — the Renderer still hardcodes the `SOUL_SHARDS` violet. A new `token`
  should resolve generically via Blizzard's `PowerBarColor[token]` (the sanctioned
  power-token exception); wiring that lookup is the generalization point, deferred until a
  spec needs it.
- **`continuous` fill** — the discrete (pips) pixel path is built; `continuous` is a
  contract-only **stub** (a continuous bar currently draws nothing). A spec whose resource
  is a continuous fill (energy/mana/fury) forces building that path.

If your spec is discrete pips on a token already coloured, you touch no Renderer code.

### Step 6 — decision-log vocabulary (`spec.log`)
`DecisionLog.lua` holds no spec constants. Provide:
- `cdOrder` — the `S{CD:…}` readiness render order, by `abbr`.
- `procOrder` — the `S{PR:…}` proc/buff render order, by code.
- `procBuffs` — `buff spellID → PR code` (the domain view's `buffs` is spellID-keyed).
- Optional spec-specific bits Demo carries (`artArmed`, `coreGlowID`) if your brain needs
  them.
Per-ability short codes ride the `abbr` field on each `spec.Spec` entry (one edit site per
ability), **not** in `spec.log`.

### Step 7 — tests (the regression gate)
- **Branch oracle:** clone `tests/spec/coach_apl_spec.lua` → `coach_<spec>_apl_spec.lua`:
  minimal hand-built `State` pulses that assert winner + `ROTATION_FALLBACK` + `SOON` per
  branch of your flat list, authored from your `rotation.md`. This is the independent
  oracle — write it from the APL, not from your own `RankWinner`.
- **Harness:** `tests/mock_ns.lua` loads `Util → SpecRegistry → SpecDemonology →
  CoachDemonology → SpecDestruction → CoachDestruction` and activates via the real
  resolver. Add `Spec<Name>.lua` + `Coach<Name>.lua` to that load list, and register the
  specID in `H.specByIndex` (index 1 = Demonology 266, 3 = Destruction 267; **index 2 =
  Affliction 265 is deliberately UNregistered** — `spec_detect_spec` needs it as the
  passive/unsupported fixture, so don't register that one). Drive your spec by calling
  `H.setSpecIndex(<idx>)` then `ns.ResolveActiveSpec()` after `H.fresh()` — see
  `coach_destruction_apl_spec.lua`'s `before_each` for the pattern.
- The existing specs must **stay green** — the Demo brain and pipeline are untouched, so
  any red is a wiring bug in your new files.

### Step 8 — confirm the tracked set in-game (one check, optional)
On a real character of the spec, `/cdmp hud layout` lists the live tracked icons + resolved
keybinds — confirm it matches the DB2-predicted set from Step 0 (catches the "default set ≠
what loads for this build" surprise, e.g. Destruction's suspected untracked Incinerate).
There is no assertion baseline to maintain (the probe + `probe-baseline.json` were retired);
this is a one-time eyeball, and `wowkb.cdmp decisionlog` is the trace to grep if a cue
misbehaves.

### Step 9 — gates
From `addon/`:
```bash
export PATH="$HOME/.luarocks/bin:$PATH"
luacheck CDMProbe/ && busted CDMProbe/tests/spec
```
Clean luacheck + all specs green (the count grows by your new oracle).

### Step 10 — release + in-game smoke
New Lua ships, so this **does** need a release (unlike the docs-only Phase 6):
`wowkb.addon release cdmp --patch`, then `/reload` and smoke on a real character:
- **Target spec:** HUD binds and draws; `/cdmp hud status` → `spec: <Name> (profile
  active)`; `/cdmp hud layout` lists the tracked icons with resolved keybinds.
- **Swap to it / away from it:** respec toggles the HUD between active and passive
  (overlay clears + "no profile" line for an unregistered spec) with no stale napkin cue
  carried across (the resolver's `HudNapkin.Reset`).
- **Rotation eyeball:** the winner/runner-up/SOON cues match your `rotation.md` at the
  dummy.

---

## What you must NOT do

- **Don't edit the pipeline** — `State.lua`, `Coach.lua` (the shell), `Binder.lua`,
  `Renderer.lua`, `DecisionLog.lua`, `SpecRegistry.lua` are spec-agnostic. The only
  sanctioned pipeline edits are the two Renderer generalization points in Step 5, and only
  when your spec actually needs them.
- **Don't call `SetActiveSpec`** in a spec file — registration is static, activation is
  `ns.ResolveActiveSpec`'s job (login + `PLAYER_SPECIALIZATION_CHANGED`).
- **Don't guess IDs or the tracked set** — source them from `spec_inventory` + simc (Step 0);
  guessing is how Demo accrued its override/transform bugs.
- **Don't copy Demo's dormant Tier-3 tables** (`SpecGroups`/`SpecOpener`/`SpecBurst`/…)
  expecting them to do something — they have no live consumer in v1.
- **Don't add a rebindable global** to `ns.SpecFields` unless a live pipeline module needs
  to read it through the legacy `ns.Spec*` name; prefer an object read off
  `ns.ActiveSpec.<field>` (the pattern `powers` and `log` use).

## If this becomes a skill

The mechanical spine (Steps 1–4, 6–9) is skill-shaped. The judgement that can't be
automated: the APL distillation into `rotation.md` + the branch oracle (Steps 1, 7), and
deciding whether a spec's resource forces the Renderer edges (Step 5). A skill should
scaffold the clone + wiring + test stub from `spec_inventory` + `simc` output, then hand
those judgement calls back to a human.
