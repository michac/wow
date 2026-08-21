# Combat Assist Plus — the pattern shelf

**What this file is for.** The catalog of *known recipes* for authoring a cap spec. The
goal (Phase 9's whole point) is that adding a spec becomes **"which known patterns do I
apply,"** not another tour through the Secret-Values and Cooldown-Manager APIs. Start from a
spec's APL, name the player problem each hint solves, enumerate the facts each rule needs,
then look each fact up here.

**This is knowledge, not a code registry.** It records what we know how to do and where the
evidence is. It is deliberately **not** a pre-built helper library or capability registry —
the backlog forbids that (`not a generalized APL DSL, capability registry or vocabulary for
mechanisms no authored experience uses`). A Lua helper is written when a real vertical
slice needs it.

**The two lanes (spec.md §3.6).** Every fact is one of:

- **READABLE** — Lua may compare/branch on it; it may drive an emphasis tier or a readable
  marker.
- **SEALED-DISPLAY** — Lua may only forward it to a client-owned display sink; it may never
  be compared, indexed, added, or tested for truthiness.
- **OPEN** — not yet measured / no API. Do not guess it into either lane.

**Evidence tiers.** **Settled** = in-client measurement (OBS-nnn / `[client]`) or Tier-1
source. **Candidate** = cookbook / generated-doc support, medium confidence, no confirming
in-client probe. **Open** = unmeasured or no API.

**Version note.** API *signatures* below are from the `12.0.7.68887` UI-source clone;
combat-*sealing* behaviour is from 12.1 in-client OBS runs (interface 120100). Where they
could differ (aura wholesale-secrecy, AuraContainer) the 12.1 OBS is the authority. Provenance
lives in `knowledge/addon-dev/` — `cdm-rider-patterns.md` (cookbook), `cooldown-manager.md`,
`security-taint-and-restricted-data.md`, `observations.md`.

**One product boundary that is NOT on the shelf.** `C_AssistedCombat.GetNextCastSpell` is
readable and would hand you a single next-cast answer. `spec.md` §4 forbids surfacing it as
cap's own opinion. It stays off the shelf by product rule, not by API limit.

---

## Part 1 — Readable facts (may drive Lua conditions, emphasis, markers)

### R1 · Can I afford this cast? — **Settled / readable**

`C_Spell.IsSpellUsable(spellID) -> isUsable, insufficientPower` (`AllowedWhenTainted`, not
combat-sealed; `SpellDocumentation.lua:873`). Read the **second** return.

- **Use `insufficientPower`, never `isUsable`** — `isUsable` returns true for a spell on
  cooldown; it answers "can I afford," not "can I cast" (`security-…:2442`).
- **Binary only** — false at 40 Fury and at 170 alike, so it cannot drive overcap avoidance.
- Canonical example: `Sense.lua`'s `readAffordable` → returns `not insufficient`; gate term
  `affordable`, worn as the `starved` cue by Havoc's two Fury spenders
  (`Catalogs/Havoc.lua`, `chaos_strike` / `blade_dance`). Demonology declares no such term —
  an earlier cite here named one, and it never existed.
- ⚠ **It is the only carrier of affordability on a spender with no real cooldown.** Such a row
  never raises an `Available` / `OnCooldown` alert edge, so `ready` stays latched true and the row
  sits in the scan whatever the resource. The scan edge cannot say this; the cue must.

### R2 · Is it ready / on cooldown? — **Settled / readable (but not by polling in combat)**

The direct read is **sealed in combat**: `C_Spell.GetSpellCooldown(spellID)` carries
`SecretWhenCooldownsRestricted`; only `.isActive`, `.isEnabled`, `.isOnGCD` are `NeverSecret`
inside it. So there are three real routes, in order of what cap actually uses:

1. **Alert-edge latch (the in-combat route).** Latch readiness off the CDM's own
   `Available` / `OnCooldown` alert edges — `hooksecurefunc` on `frame.TriggerAlertEvent`.
   Canonical: `Sense.lua:161-183` `onAlert` → `Track.lua:113-127` `EDGES`.
2. **Out-of-combat baseline.** `C_Spell.GetSpellCooldown` directly, with a GCD floor.
   Canonical: `Sense.lua:113-122` `readCooldown` (comment: "GetSpellCooldown is secret in
   combat").
3. **`.isActive` boolean** — `NeverSecret`, the plain "a cooldown timer is running"
   discriminator (OBS: 90 in-combat samples, `cooldown-manager.md:1443`). Cannot tell *why*,
   only that a timer is running. (Charge-spells have their own `isActive` — see R6.)

Boolean-from-a-secret-time: feed a duration object into a hidden scratch `Cooldown` widget
and read `IsShown()` (plain bool). Gotcha: after `SetCooldownFromDurationObject` the widget's
`GetCooldownTimes()` is **secret** — re-read the cached duration object, never scrape times
back (`cdm-rider-patterns.md:206-228`).

### R3 · Secondary vs primary resource level — **Settled / SPLIT by power type**

`UnitPower(unit, powerType)` is `SecretWhenUnitPowerRestricted` — but the restriction is
**per power type and per unit**, not ambient combat.

- **Readable (never-secret) secondaries — exactly seven:** Combo Points, Runes, **Soul
  Shards**, **Holy Power**, Chi, Arcane Charges, Essence.
- **Secret primaries:** Mana, Rage, Focus, Energy, Runic Power, **Fury**, Pain, Insanity,
  Maelstrom — most specs' main bar. ⚠ **Fury is secret**, so a Havoc catalog can only
  *display* Fury (see S1), never branch on it.
- `UnitPowerMax(player, t)` **is** readable (different predicate) — you can read the cap,
  never the current primary value. Query secrecy directly: `C_Secrets.GetPowerTypeSecrecy(t)`
  (0 = never, 2 = contextually) / `C_Secrets.ShouldUnitPowerBeSecret`.
- Canonical: `power = "SoulShards"` in the catalog (`Catalogs/Demonology.lua:27`), resolved
  `Enum.PowerType[name]` at `Sense.lua:481`, read at `Sense.lua:102-110`; gate term
  `resource` (`Tier.lua:91-97`). Provenance `security-…:2378-2412`.

### R4 · Static resource cost & generation (measure once, cache) — **Settled for cost, authored for generation**

Cost and generation are **static per-spell values** — obtain them **out of combat** and cache,
so you never query them in restricted combat at all. This is the insight that makes R5 work.

- **Cost:** `C_Spell.GetSpellPowerCost(spellID) -> table<SpellPowerCostInfo>` — each entry
  `{ type, name, cost, minCost, costPercent, costPerSec, requiredAuraID, hasRequiredAura }`
  (`SpellDocumentation.lua:457`, `AllowedWhenTainted`). Prefer a **measured OOC value** cached
  at load / spec-change over the raw DB2 number — the static table can disagree with the
  client's real cost (`security-…:2445`).
- **Generation:** **no generation API found** (as of the 12.0.7 doc surface sweep) — a
  spell's resource generation must come from an **authored static table** (the APL / spec
  data), cached the same way.
- Both end up as cached Lua numbers, so they are readable in combat by construction. Refresh
  the cache on `PLAYER_ENTERING_WORLD` / `SPELLS_CHANGED` / talent + spec change.

### R5 · Projected secondary resource for a cast-time ability — **Candidate (derived from settled inputs; no consumer yet)**

The capability R3/R4 exist to serve: decide whether you can cast a spell given resource that is
**incoming** (generated by the cast in flight) and **outgoing** (the candidate's cost). The
*inputs* are all settled; the *composition* is unbuilt, so it stays Candidate until a slice
proves it.

`projected = current (R3) + generation[in-flight] − cost[candidate]`, where generation/cost are
the cached statics (R4). Every input is readable, so the projection may drive an emphasis or a
marker.

- **Only for cast-time abilities.** An instant resolves immediately, so `current` already
  reflects it and no projection is needed; the projection only matters across the in-flight
  cast's window, before its generation/cost has landed.
- **The in-flight cast's identity must come from the readable press route (R9)** — not
  `UnitCastingInfo` or the cast events, whose `spellID` is sealed in combat (R9).
- Keep it to *availability* ("will I have enough"), matching R1's binary spirit — not exact
  overcap arithmetic. (No cap consumer yet; a natural fit for a shard-builder→spender spec.)

### R6 · Is a charge-spell castable? — **Settled / readable only at full**

`C_Spell.GetSpellCharges(spellID)` (`SecretWhenCooldownsRestricted`): `maxCharges` and
`isActive` are `NeverSecret`; `currentCharges`/start/duration/`chargeModRate` seal **below
full**. OBS-066 (`observations.md:1177`, Conflagrate): at 2/2 all readable; at 1/2 and 0/2
`currentCharges` is secret and **`isActive` is `true` in both** — it describes *recharge
running*, so it **cannot distinguish castable 1/2 from dead 0/2**.

→ The only way to a per-charge readiness *number* in combat is the **napkin estimator**: seed
exact `current/max/recharge` out of combat, **debit** on a readable cast trigger (the R9 press
route, or a CDM charge-alert edge — *not* `UNIT_SPELLCAST_SUCCEEDED`, whose spellID is sealed;
see R10), **credit** on a non-duplicate `ChargeGained` alert, **clamp** to `[0,max]`,
**re-seed** when combat ends. Captures label exact `live` vs maintained `napkin` (spec.md §3.5). `maxCharges <= 1` means "not a charge spell." Never
derive "0 charges" from `IsSpellUsable`. Recharge as a duration object:
`C_Spell.GetSpellChargeDuration(spellID)`. (Not in v0.2.4; the Conflagrate estimator is the
desktop/design example.)

### R7 · Spells that switch mid-combat (transform-safe identity) — **Settled / readable**

The pattern behind Shadow Bolt↔Infernal Bolt, Grimoire: Imp→Consume Magic, and — the one
that silently corrupts napkin math — **DH Havoc's Immolation Aura changing in demon form**
(different id, different charges).

- **Identity route:** read `overrideSpellID` off the CDM cooldown-info struct
  (`C_CooldownViewer.GetCooldownViewerCooldownInfo`). It is **readable in combat on 21/21
  rows**; `item:GetSpellID()` reads **secret and the secret set *moves* between reads** — do
  not build identity on it (`cooldown-manager.md:1191`, `observations.md:1053`).
- **The only honest test is `overrideSpellID ~= spellID`** — `overrideSpellID` is *always*
  populated (mirrors `spellID` when nothing overrides), so `~= nil` is meaningless. Lua `0`
  is truthy, so an override of `0` must be checked explicitly.
- **Bind a static identity, never the live id.** Choose `primary = override or base` at bind
  and keep a stable `spellIDs` union so the row matches across the flip
  (`Bind.lua:88-111`). The `identity`/`transformed` gate reads
  `overrideSpellID ~= spellID` (`Sense.lua:89-98`); a transforming ability may be **two
  entries on one row**, keyed by entry not cooldownID (`Tier.lua:9-10`). Choice-node pairs
  use catalog `alt` ids (`Catalogs/Demonology.lua:65-66`, Grimoire `1276452`/`1276467`).
- **Charge/napkin safety across a switch:** adopt override-aware max —
  `C_Spell.GetSpellCharges(overrideSpellID or spellID)`; key the **debit** (R6's readable
  trigger) on the *normalised* identity; and **re-seed the estimate when the override id
  changes** rather than carrying a count across the transform. This is the Immolation-Aura fix.
- Standalone resolvers also exist (`C_Spell.GetOverrideSpell`, `C_Spell.GetBaseSpell`,
  `C_SpellBook.FindSpellOverrideByID`, all readable), useful off the CDM path; secret-guard
  the id before any `>0`/`floor` test.

### R8 · Pandemic window (DoT refresh) — **Settled / readable as a BOOLEAN, sealed as a number**

The *state* is a readable Lua fact; the *time* is sealed.

- **Readable boolean:** `item.PandemicIcon ~= nil` on a CDM tab-1 (target-DoT) row mirrors
  `IsInPandemicTime` exactly, recomputed every frame, **never secret**
  (`cooldown-manager.md:1303-1309`, `[client 2026-07-31]`).
- **Sealed number:** `item.pandemicStartTime`/`pandemicEndTime` are secret and
  `item:IsInPandemicTime(timeNow)` **throws** (a comparison inside the body) — guard with
  `pcall`, not `issecretvalue`. Blizzard computes the true window (not the community "30% of
  base") and then seals it.
- The `PandemicTime` alert edge fires **one-shot per aura instance**; use `PandemicIcon` for a
  continuous signal. Target-DoTs only. (No cap consumer yet.)

### R9 · What am I casting right now? — **Readable via the press; SEALED via the cast API**

Two routes, and the lane depends on which you take:

- **Readable (predictive, pre-cast):** hook the action-button input — `ActionButtonDown` /
  `MultiActionButtonDown` / per-button `PreClick` — and resolve the pressed slot with
  `GetActionInfo(slot)` → spellID (readable — it is the action bar, not combat state),
  tolerant of spell/item/macro action types. This is "what you pressed," available the instant
  the key goes down (`cdm-rider-patterns.md` §9.1). Match under the `{self, override, base}` id
  set (R7).
- **SEALED (authoritative, mid-cast):** `UnitCastingInfo("player")` / `UnitChannelInfo` and
  **every** `UNIT_SPELLCAST_*` event carry **`SecretWhenUnitSpellCastRestricted`**, and their
  `spellID` payload is **not** `NeverSecret` — so *which* spell you are casting is **secret in
  restricted combat**. Only `castBarID` is `NeverSecret`. Use these for the *fact/timing* of a
  cast or to forward to a display, never to branch on identity.
- ⚠ **Tier-1 doc annotation** (`UnitDocumentation.lua:815-859, 4534-4700`); the *restricted*
  case is **unmeasured**. There is a `[client]` reading of the id **readable out of instances**
  (unrestricted — `cooldown-manager.md:1425`), which does not refute the sealed-in-instance
  claim. The open probe is specifically: does `UNIT_SPELLCAST_SUCCEEDED`'s `spellID` read
  secret *inside* an instance? — which also tests the cookbook §9.2 "debit the charge on
  SUCCEEDED" assumption this annotation calls into question.

### R10 · A rolling history of the last N casts — **Readable ring (press) vs sealed ring (confirmed)**

An addon-maintained ring buffer of recent casts; the lane follows R9's split:

- **Readable ring:** push the **press**-derived spellID (R9 readable route) into a fixed-size
  ring. Fully branchable — it is the addon's own data. Predictive: a press can be cancelled or
  out of range, so it records "what I tried," not "what landed."
- **Sealed ring:** push `UNIT_SPELLCAST_SUCCEEDED`'s spellID (player-filtered) — it confirms
  the cast and filters fat-fingers, but the id is **secret in restricted combat**, so the ring
  is forward-to-display only, never compared.
- **Consequence for the R6 napkin:** the readable trigger for "the tracked spell was just
  cast" is therefore the **press** (or a CDM charge-alert edge), because the confirmed-cast id
  is sealed. Debit the estimate on the readable trigger; treat SUCCEEDED as timing only until a
  probe says otherwise.

---

## Part 2 — Sealed display cues (forward secret → a client-owned sink; never branch)

The safe `AllowedWhenTainted` setters that accept a secret directly: `Region:SetAlpha`
(SecretAspect Alpha, clamps [0,1]), `Texture:SetDesaturation` (SecretAspect Desaturation),
`StatusBar:SetValue`, `FontString:SetText`. Duration-object setters
(`Cooldown:SetCooldownFromDurationObject`, `StatusBar:SetTimerDuration`) are
`AllowedWhenUntainted` but the secrecy rides **inside** the duration object, so they are legal.
⚠ **ACCEPTED IS NOT DRAWN — the one statement of it, cited from everywhere else.** Every sink
above is aspect-less on readback: the call being accepted is not proof a pixel appeared. A capture
reports `offered` / `armed` / `refused`, never `drew`, and a display question is closed only by an
eyeball. `spec.md` §6, `authoring.md` stage 8, `flight-reading.md` and the anti-patterns below all
point here rather than restating it.

### S1 · Primary resource as a display cue — **Settled / sealed-display**

A secret primary (Fury, Energy, …) may be *shown* though never branched. Straight route:
secret `UnitPower` → `SetText`/`SetValue`/`SetAlpha`. Graded route:
`UnitPowerPercent(unit, powerType, unmodified, curve)` evaluated in C with a color curve,
result handed straight to a draw call (`security-…:1942-1949`). This is how a Havoc catalog
could surface Fury it cannot read.

### S2 · Aura stack count, shown/hidden by value — **Settled / sealed-display**

The managed AuraContainer owns the whole display: a slot filtered to the one aura
(`candidateFilters.includeSpellIDs[auraSpellID]`, unit `player`), with `SetIcon`,
`SetDurationCooldown`, and **`SetApplicationCount`** registered inside `initializeFrame`. The
count FontString is empty below threshold and shows the number at/above it — the client draws
it from the secret; Lua never reads it. OBS-065 (`observations.md:1161`, Backdraft 117828,
human verdict: 1 stack = icon/swipe only, 2 = the number "2").

⚠ **The threshold of 2 is Blizzard's no-formatter DEFAULT, not the form's limit** — the apply
path is `elseif applications > 1` when `options.formatter` is absent
`[T1 src: Blizzard_CustomAuraButton.lua:351-368]`, and cap has always passed no options. **S7 is
the general form**; treat S2 as its zero-configuration case and do not cite "2" as a ceiling.

- **Eye-catch:** the value **appearing** is itself the draw-the-eye event; add motion only if
  play asks (a pulse/scale on the FontString, or a glow-lib flipbook — `cdm-rider…` §12).
- **"Value-as-alpha" trick:** to hide a widget when a secret count is zero, write the count
  straight into `SetAlpha` (clamps, so 0 → hidden, 1+ → shown) — no comparison performed.
- ⚠ **Gotchas:** `initializeFrame` is the **only** window — the button is a *forbidden object*
  whenever its aura is secret, so build everything at creation and anchor a **proxy**, never
  the button. `IsShown()` on it is secret (that's why the type exists). The mixin method
  names (`SetApplicationCount`, `SetDurationCooldown`, …) are **cookbook-illustrative** (a
  12.1 addon wrapper) — absent from the 12.0.7 clone; verify against a 12.1 source when
  building. ⚠ v0.2.4's `Channel.StackText` (`GetAuraApplicationDisplayCount`,
  `Channel.lua:31`) is the **superseded** pre-12.1 stack path — do not carry it forward.

### S3 · Show/hide a texture by whether a cooldown is up — **Settled / sealed-display**

A `C_CurveUtil.CreateCurve()` **step** curve — `SetType(Enum.LuaCurveType.Step)`,
`AddPoint(0, 0)`, `AddPoint(0.001, 1)` — evaluated by the duration object
(`durObj:EvaluateRemainingDuration(curve, Enum.DurationTimeModifier.RealTime)`), result piped
into `SetDesaturation(val)` or `SetAlpha(val)`. Any remaining > 0 maps to 1. Feature-gate
`C_CurveUtil`/`Enum.LuaCurveType`/the method before use. ⚠ The second Evaluate arg is the
**DurationTimeModifier**, not a fallback (cookbook prose is loose; `Channel.lua`/`Bars.lua`
pass `RealTime` correctly). Alternative: the scratch-frame `IsShown()` boolean (R2).

### S4 · Show/hide a texture by cooldown-remaining within a RANGE — **Settled / sealed-display**

Same step curve with the **break point at the threshold** — e.g. suppress a swipe that ends
within the GCD: `AddPoint(0, 0)`, `AddPoint(len, normalAlpha)`, result → alpha. ⚠ If the
threshold itself is secret (e.g. `UnitSpellHaste` in instanced combat), guard and floor it
**first** (assume unhasted; GCD floor 0.75) before building the curve. Canonical shape:
`Channel.Threshold` (`Channel.lua:76-89`).

### S5 · An aura's remaining DURATION as a FontString in a custom place — **CLOSED at 12.1 / kept for its duration-object facts**

`C_UnitAuras.GetAuraDuration(unit, auraInstanceID)` → `LuaDurationObject` →
`durObj:FormatRemainingDuration(formatter, Enum.DurationTimeModifier.RealTime)` → secret
string → `FontString:SetText(...)`, which **ticks in combat**.

⛔ **This route is closed to cap at 12.1 and the entry is kept for its duration-object facts
only.** It needs a **plain** `auraInstanceID` (`AllowedWhenUntainted`), and the 12.0.7 measurement
that supplied one — `item.auraDataCached.auraInstanceID` reading plain off a CDM item frame while
the aura's magnitudes were secret (`cooldown-manager.md:1744-1760`, `[client 2026-08-05]`) — no
longer holds: aura instance IDs are secret at 12.1 (`projects/addon-lab/questions.json:1186`,
which parks the old CAP route as obsolete for exactly this reason). **The replacement is the
AuraContainer's own duration sinks** — `SetDurationCooldown` / `SetDurationText`
`[T1 src: Blizzard_CustomAuraButton.lua:139-192]` — where the duration object is handed to the
sink by the client and cap never holds an instance ID at all. @verify-ingame — the 12.1 secrecy of
`auraInstanceID` is carried on our own registry note, not on a `[client]` measurement.

- **Two args, unit + auraInstanceID** (NOT a spellID); **both must be plain** or it refuses.
- FontString must be a leaf; for a bar sink call `SetMinMaxValues(0,1)` **before**
  `SetTimerDuration` or it draws at 0 % width. You still cannot learn the number.
- OBS-034 (object obtained both player-buff and target-debuff) + OBS-035 (eyeball: bars
  animate like the control). **This is the Destruction Immolate (target-DoT) countdown
  example** (design/desktop).

### S6 · Totem duration FontString + show/hide — **Settled / sealed-display**

`GetTotemDuration(slot) -> LuaDurationObject` (`AllowedWhenUntainted`, no `Secret*When*`
seal); feed it the same FontString path as S5. `GetTotemInfo(slot)` /
`GetTotemTimeLeft(slot)` carry `SecretWhenTotemSlotSecret`. ⚠ Iterate
`1..GetNumTotemSlots()` — **measured 5 on a Warlock** (`cooldown-manager.md:1507`,
`[client 2026-08-09]`); the legacy `MAX_TOTEMS` global is **4** and undercounts non-shaman
slots, so a loop sized by it can miss an occupied 5th slot (exactly the Dreadstalkers case).

- **Show/hide (occupied vs empty):** discriminate off `GetTotemDuration(slot) ~= nil`, or
  off `GetTotemInfo`'s **`icon` (the 5th return, not last)** being non-nil on an occupied
  slot. Prefer the raw `GetTotemInfo` API over Blizzard's cached wrapper — the raw call owns
  no shared state (`cooldown-manager.md` §7).
- **Dreadstalkers (104316) is CONFIRMED totem-backed** (`[client 2026-08-09]`): a cast raised
  `PLAYER_TOTEM_UPDATE`, the row is `CooldownSetSpell …104316,3` (Category 3 TrackedBar, cid
  760), `totemData` reads populated while `auraDataUnit` stays nil. Readable liveness for a
  CDM totem row: **`item.Bar.Pip:IsShown()`** (plain boolean). **This is the Demonology
  Dreadstalkers countdown example** (design/desktop).
- ⚠ The API facts are settled, but no totem-duration → sink *render* has been eyeballed — only
  S5's aura channel has (OBS-035). The pixel is a design/desktop hypothesis until flown.

### S7 · Aura stack count in a BAND — **Settled / sealed-display, FLOWN `[client 2026-08-21]`**

S2 shows a count at or above one threshold. S7 is the general form: **cap authors a piecewise
function from the secret count to a string, and the client evaluates it.** That is what makes
"blank until 4, then 4", "blank above 1" (the complement), and a middle band all one primitive.

The rule object is a **`NumericRuleFormatter`**, not a curve:

- `C_StringUtil.CreateNumericRuleFormatter()` — *"converts numbers to strings with flexible
  rulesets"* `[T1 docs: StringUtilDocumentation.lua:21-29]`.
- A breakpoint is `{ threshold, format, step, rounding, min, max, components }`; `threshold` is
  *"Minimum input value that this rule applies to"* and `format` *"The format string to apply at
  this threshold"* `[T1 docs: NumericRuleFormatterSharedDocumentation.lua:19-30]`. `min`/`max`
  are input **clamps**, not visibility thresholds — the name collides with S2's and means
  something else.
- `AddBreakpoint` / `SetBreakpoints` / `GetBreakpoints` / `ClearBreakpoints` / `Copy`
  `[T1 docs: NumericRuleFormatterAPIDocumentation.lua:11-67]`. Breakpoints are plain authored
  numbers, so building one is ordinary addon code; `Copy` is `ReturnsNeverSecret`, so one
  configured template can be cloned per row.
- The evaluator is `FormatNumber(number) -> string`, `ConstSecretAccessor = true`
  `[T1 docs: NumericFormatterAPIDocumentation.lua:11-27]` — secret in, secret out, no aspect
  applied to the formatter.

It reaches the pixel through S2's existing sink `[T1 src: Blizzard_CustomAuraButton.lua:351-368]`:

```lua
local formatter = options.formatter
if formatter then text = formatter:FormatNumber(applications)
elseif applications > 1 then text = applications end
fontString:SetText(text)
```

⚠ **The `min = 2` in `Catalog.Check` is not a platform limit.** It mirrors that `elseif
applications > 1` — Blizzard's behaviour when **no formatter is passed**, which is what cap has
always passed. **S7 has now flown `[client 2026-08-21]`, so lifting it is unblocked** — `min = 2`
→ "any positive integer" is a cap change (`Catalog.lua:192` + a release, ask-first); do not treat
S2's threshold as the shelf's ceiling.

- **An empty `format` is the whole point.** It is the only way to express *absence*, and both
  known consumers are absence-shaped. Neither `SecondsFormatter` nor
  `AbbreviatedNumberFormatter` can emit nothing, so this is the one of the three factories
  that matters to us.
- **`format` need not carry a specifier at all**, so a band may emit a fixed string (`MAX`) or
  a single glyph rather than the number.
- ⚠ **Do not reach for `SecondsFormatterMixin`** `[T1 src: Blizzard_SharedXML/TimeUtil.lua:95]`.
  It is a pure-Lua lookalike with nearly the same method names, used all over Blizzard's own
  addons via `CreateFromMixins`, and it does its arithmetic **in script** — feed it a secret and
  it dies. The secret-safe objects are `Userdata` and come only from `C_StringUtil.Create*`.
- ✅ **Flown, and honoured `[client 2026-08-21]`.** A tainted-created `NumericRuleFormatter`,
  built in `initializeFrame` and passed as `SetApplicationCount(fs, {formatter=f})`, drives
  Blizzard's apply path. Five Backdraft tiles read exactly as authored: the control (blank
  below 2), a band showing a lone **`1`** (the discriminator — the default never prints a 1, so
  the 1 proves cap's ruleset ran), a `MAX` word-band, per-band colour escapes, **and the
  complement (`1` then blank)** — the low-shown/high-hidden shape S2 below had recorded as
  *impossible*. The exact working chain is drained to
  `knowledge/addon-dev/security-taint-and-restricted-data.md` §3.5.2.

### S8 · Per-band COLOUR on a banded count — **Settled / sealed-display, FLOWN `[client 2026-08-21]`**

S7 with polarity. Two routes, and they differ in what they cost:

- **Inline colour escapes in the band's `format`** — `{threshold=0, format="|cffff4040%d|r"}`,
  `{threshold=6, format="|cff40ff70%d|r"}`. One sink, one FontString, both polarities. Escapes
  in a format string are precedented in Blizzard's own code: the gamepad key labels expand to
  `|A:Gamepad_%s_32:14:14|a`, markup and a specifier in one string
  `[T1 src: SharedConstants.lua:56-58]`.
- **Two slots on one spell ID**, each with a complementary ruleset and its own statically
  coloured FontString. Costs a second container button and is unverified, but needs no markup
  to survive the formatter.

**What makes the colour ours at all:** `SetApplicationCount` adds only `Text` and `Shown`
`[T1 src: Blizzard_CustomAuraButton.lua:59-68]` — **not `Alpha`, not `VertexColor`**. Compare
`SetDurationText` (`:158-192`), which adds `Text`, `Alpha` *and* `VertexColor` because its colour
curve drives them. So on the **count** FontString `SetTextColor` stays cap's to call at setup, and
one static hue needs no markup at all. Per-*band* hue is what needs the escapes.

- **A symbol font is the same primitive.** `SetFont` runs in `initializeFrame`, before lockdown,
  and carries `RequiresValidFontAsset` + `RequiresValidFontHeight` with the FontString variant
  returning `success: bool` `[T1 docs: SimpleFontStringAPIDocumentation.lua — SetFont]` — a
  checkable result while we can still read one. A band emitting a PUA codepoint in a cap-shipped
  TTF draws a **shape**, tintable through the text-colour path and outline-able via the
  `"OUTLINE"` flag. This is the only known way to get cap-owned *art* out of a stack count: no
  API evaluates a curve against an aura's applications, so `SetAlpha`/`SetVertexColor` on a
  sprite cannot be driven by one.
  ⚠ It is a **second art channel** the `render-shelf` → `capart export` pipeline does not own
  today. Adopting it means the shelf declares the glyph set and `capart check` gates the font
  the way it gates badge TGAs, or the preview↔addon guarantee lapses.
- ⚠ **Unflown, and it has a distinct failure mode from S7.** `C_StringUtil` ships
  `EscapeQuotedCodes` and `StripHyperlinks(…, maintainTextures, maintainAtlases)`
  `[T1 docs: StringUtilDocumentation.lua]`, which proves the client sanitises markup from
  untrusted strings *somewhere*; whether `NumericRuleFormatter` strips it is invisible from Lua.
  **The font route survives that failure and the escape route does not** — but the escape
  route flew: tile D drew its numbers **red at one stack, green at two** `[client 2026-08-21]`,
  so `NumericRuleFormatter` did **not** strip the `|c…|r` markup on this build. The escape route
  is therefore usable today; the font route remains the more robust fallback if a later build
  starts sanitising. The static-hue floor (`SetTextColor` at setup) is unchanged and still ours.

### S9 · Pandemic window as a client-drawn texture — **Settled / sealed-display, FLOWN `[client 2026-08-21]`**

R8's readable boolean is a **CDM tab-1 row** fact (`item.PandemicIcon ~= nil`). S9 is the same
window on the **AuraContainer** channel, which needs no CDM row and works on a player buff:

`AddPandemicRegion(region)` `[T1 src: Blizzard_CustomAuraButton.lua:236-248]` registers any
Region and adds `SecretAspect.Shown` to it. The client then drives its visibility directly
`[T1 src: :567-573]`:

```lua
local isInPandemicTime = self:IsInPandemicWindow()
for _index, pandemicRegion in ipairs(self.pandemicRegions) do
    region:SetShown(isInPandemicTime)
end
```

- **The window is Blizzard's, not the community's 30 %.** It is computed as
  `GetRefreshExtendedDuration - GetAuraBaseDuration`, and exists only when that carry-over is
  positive `[T1 src: :612-628]`. cap authors no threshold here at all — this is the one sealed
  form with **no curve and no ruleset**, which also means nothing to get wrong.
- **It is the only sink that costs an `OnUpdate`**, and the enablement is itself `secretwrap`ped
  `[T1 src: :634-641]`, with Blizzard's own note that *"the enablement of our OnUpdate script is
  inferred (partly) through presence of an aura."* Budget one `OnUpdate` per armed tile and do
  not attach it speculatively.
- **Any Region qualifies** — a Texture, so cap's existing badge art is usable directly. This is
  the one primitive in Part 2 that reaches cap-owned art without a font trick.
- ✅ **Flown `[client 2026-08-21]`.** A Texture handed to `AddPandemicRegion` on an Immolate
  slot stayed hidden for most of the DoT's duration and switched on **only near the end**, then
  cleared when the DoT was refreshed inside the window — i.e. the client drove its own real
  pandemic window onto cap's texture, no threshold authored. ⚠ **The one trap the flight cost:
  the aura id is not the cast id** — Immolate casts as `348` but applies aura `157736`, Wither
  casts `445468` → aura `445474`; `includeSpellIDs` must carry the aura id or it matches nothing
  forever, looking exactly like a refused call. Still **no consumer yet** — Demonology's Doom is
  the obvious first subject. Drained with the working chain to
  `knowledge/addon-dev/security-taint-and-restricted-data.md` §3.5.2.

⚠ **All three share one gate, and it is the same gate.** `initializeFrame` is the only window in
which any of them may be built: it runs **before** `ApplyAccessRestrictions`
`[T1 src: Blizzard_AuraContainerFrameProviders.lua:74-92]`, and the restriction applied a beat
later is `DenyTaintedAccessWhenAurasAreSecret`
`[T1 src: Blizzard_AuraContainerShared.lua:105-108]`. Every sink widget must be a **descendant of
the button** or the registration `error()`s outright
`[T1 src: Blizzard_AuraContainerUtil.lua:255-270]`. And frames are created in **batches of 10** to
obfuscate how many auras you have — *"Must be sufficiently high to obfuscate the number of auras
as this invokes initialization callbacks"* `[T1 src: Blizzard_AuraContainerShared.lua:105]` — so
**never infer anything from how many times your callback fires.**

---

## Part 3 — Mechanism seams (small helpers, written per-slice)

These are the reusable seams the patterns above imply. Author each when its **first** real
consumer needs it.

- **Duration acquisition.** Four sources, one return type (`LuaDurationObject`): spell
  cooldown `GetSpellCooldownDuration(id, ignoreGCD)`, charge recharge
  `GetSpellChargeDuration(id)`, totem `GetTotemDuration(slot)` — and, for auras, **not**
  `GetAuraDuration(unit, auraInstanceID)`, which needs a plain instance ID cap cannot hold at
  12.1 (S5): the container hands its own duration object to `SetDurationCooldown` /
  `SetDurationText` instead. Keep source-specific **identity + liveness** work explicit; share
  only the curve/sink plumbing.
- **Curve guard.** Feature-gate `C_CurveUtil.CreateCurve` / `Enum.LuaCurveType.Step` /
  `Enum.DurationTimeModifier.RealTime`; on any missing piece return the inert path. Curves and
  durations are `userdata`, not tables.
- **Sink routing.** Know which sink accepts a secret directly (`SetAlpha`, `SetDesaturation`,
  `SetValue`, `SetText`, `SetApplicationCount`) vs which carry secrecy inside a duration
  object (`SetTimerDuration`, `SetCooldownFromDurationObject`). Never read back.
- **Identity resolution + re-seed (R7).** The transform-safe read plus the napkin re-seed on
  override change.
- **Marker construction / placement — the shared renderer, and the 9.4 seam.** Tier→pixels
  lives in `Treatment.lua` (the only place the visual numbers exist) and `Overlay.lua`; a
  context marker reuses the existing `count`/`hold` slots (`Overlay.lua` `SLOTS`) and an
  existing `polarity`+`channel` shape that `slotFor` already maps. **A new spec that reuses an
  existing tier and an existing marker/channel shape edits nothing in Treatment/Overlay — it
  is authored purely as `Catalogs/<Spec>.lua` data.** Renderer edits are needed *only* to
  introduce a genuinely new marker shape or channel pairing. This is the definition-of-done
  for 9.4.

---

## Anti-patterns (the ways each lane breaks)

- **Branching on a secret** — comparing, indexing, adding, or truth-testing a secret aborts
  the handler (and every later frame in a `pairs()` loop). Guard **secret-first**, before any
  other test; use `type(x) ~= "number"`, never `x == nil`, on a possibly-secret value.
- **Identity off `item:GetSpellID()`** — secret and moving in combat. Use `overrideSpellID`.
- **"0 charges" from `IsSpellUsable`** — a spell can be unusable for many reasons; a secret
  count leaves zero genuinely unknown.
- **Trusting a static cost table** — DB2/doc cost can disagree with the client (R4).
- **Reading a duration back** — see Part 2's *accepted is not drawn*.
- **Carrying a napkin count across a transform** — re-seed on the override flip (R7).
- **Treating cookbook mixin names as Blizzard signatures** — the AuraContainer wrapper (S2)
  is illustrative; confirm against a 12.1 source.

---

## How to use this shelf

This file is the **reference**, not the route. `authoring.md` owns the route: its **stage 3**
classifies each fact the spec needs against Part 1 / Part 2 above, its **stage 4** maps the
readable ones to lanes and markers and the sealed ones to cues, and its **stage 6** points each
mechanism at a Part-3 seam.

The canonical example for each mechanism, when you need one to author against: Demonbolt = proc
+ resource, Tyrant = readiness + readable markers, Conflagrate = charged readiness, Backdraft =
sealed stacks, Immolate = aura-duration display, Dreadstalkers = totem-duration display.
