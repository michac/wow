# Smart Glo — backlog

**What this file is for:** the current implementation status and the ordered work list.
`README.md` owns the design and why it is shaped the way it is.

The live addon version comes from `wowkb.addon list`, never from prose here.

**Measurements do not live here.** A fact this addon establishes about the client belongs in
`knowledge/addon-dev/`, where the KB's gates apply and the next reader will actually find it. A
status line may say a thing works; the evidence that it works is a claim in a topic file.

**An item here has to keep earning its place.** If its premise stopped being true, rewrite it or
delete it — never leave it standing with a note underneath.

## Status

**It records what is BUILT.**

- **The attach path.** A subject's glow is our own frame, `UIParent`-parented and two-point
  **anchored** to its Cooldown Manager item frame, at `MEDIUM` and `item:GetFrameLevel() + 5`,
  scaled by the item's effective scale. Blizzard's `Layout` moves the icon and the overlay
  follows; nothing of ours reasserts a position and nothing of ours is parented to a CDM frame.
- **Rebuild, never re-apply.** `Layout` / `RefreshLayout` on all four viewers, `OnCooldownIDSet`
  on all four item mixins and `CooldownViewerSettings.OnDataChanged` all mark dirty; one
  `C_Timer.After(0, …)` flush detaches every overlay, re-sweeps the pools and re-reads
  `GetCooldownID()` fresh. No id-to-frame table survives a flush. Overlays hide on Edit-Mode
  enter, and every show is gated on `IsVisible()` through a secret guard that fails closed.
- **The v1 rule vocabulary**, three-valued, no short-circuit: secondary-resource thresholds,
  `ready()`, `aura()`, and `and` / `or` / `not`. The checker refuses a primary as a gate, a
  charge count, and a count inside an expression. `/sg why` prints per-term `T | F | ?`.
- **The count element, as an OCCLUDER.** An `AuraContainer` slot pinned by `includeSpellIDs`,
  hosted as a child of the overlay, carrying an authored `NumericRuleFormatter` whose band
  **below** the threshold is an inline escape of the subject's **own icon, centre-cropped**, and
  whose band at the threshold is empty. The polarity is inverted on purpose: the client conceals
  our mark rather than revealing one of its own. Armed once in `initializeFrame`, in combat or
  out. Its readable gate closes the container's alpha before the client draws, which is how a
  gate composes with a binding. **§6.4's absence case is closed by `Rules.Gate`**, which gives
  every count an implicit presence term on its own aura, so the aura going away darkens the
  mark instead of revealing it. The authored `when` is untouched, so export and the checker
  still show the rule as written. The cost: a count glow now needs a Tracked Buffs row for its
  aura, which the occluder alone did not.
- **One look, one mark, on both sinks** — a spinning hexagon outline centred in the icon.
  It is **always our own Texture on our own frame**, so it takes a rotation and a vertex colour;
  what differs is who reveals it. A gate draws it; a count has the client take its occluder away.
  `Media/` is **generated** by `tool/gen_media.py` from a CC0 Kenney icon; do not hand-edit it.
  `/sg color <name>` recolours everything, both kinds, on the next evaluation.
- **`<resource>.after_cast` — a threshold read past the cast in flight.** `Cast.lua` keeps a
  one-slot ledger off `UNIT_SPELLCAST_START` and its five terminal events, registered against
  `"player"`, whose cast id reads plain because `SecretWhenUnitSpellCastRestricted` tests the
  unit and not combat. The projection is cost (`C_Spell.GetSpellPowerCost`, talent-correct) and
  gain (`PowerGain.lua`, generated from `SpellEffect.db2` energize rows) applied together,
  because the cost lands at completion. Computed in raw units and floored through
  `UnitPowerDisplayMod`, so a partial shard does not read as a whole one. **Soul Shards only**:
  the same Tier-1 rows show Holy Power and Combo Point gains moving with talents and procs, and
  the checker refuses those by name. Nothing casting is a projected zero, not an unknown.
  ⚠ **Unflown** — the ledger and the arithmetic are exercised offline, but no eyeball has seen
  a mark change mid-cast.
- **Aura presence read at the level, not only at the edge.** `Attach.AuraLatch` asks the frames
  carrying the aura whether it is up NOW, and falls back to the edge latch when none can say.
  This is what answers for a buff that was already up when we started watching, which an edge
  latch cannot see. Two instruments, the better one deciding alone: a **buff-viewer** item
  answers through `IsActive()`, whose `ShouldBeActive` the buff mixin overrides to track expiry,
  the linked-spell fallback and totems; a cooldown-viewer row has no such predicate and can only
  offer `wasSetFromAura` / `auraInstanceID`. ⚠ Those two fields are Tier-3
  (`mined-pending-verification.md` E2, `@verify-ingame`), so a client without them makes the
  cooldown-viewer half silent and the edge latch carries it exactly as before.
  ⚠ **Being SHOWN is a different question and is not used**: `ShouldBeShown` returns true
  whenever `hideWhenInactive` is off, a user setting, so a shown row says nothing about the aura.
- **The config dialog** — a subject dropdown built by enumerating live item frames, a detail
  pane, and a text box that is also the import/export surface.
- **Serialization and profiles.** `SG1:` + base64(deflate(JSON envelope)) with an adler32, every
  `C_EncodingUtil` call in its own `pcall`; `Profiles.lua` carries the Demonology set;
  `uv run python -m wowkb.smartglo encode|decode|check` is the Python side, stdlib only.
- **Flown, and both mechanisms draw.** Demonology at a dummy: the hexagon lit on Hand of Gul'dan
  across the shard threshold, and the count sink drew on Implosion at six Wild Imps — a count the
  addon never read, drawn by the client from a band table it was handed. Both confirmed by eye,
  which is the only oracle a sealed output has. That flight was the revealing polarity; what the
  occluder changes is which band draws, not whether the sink works.
- ⚠ **The crop is MEASURED BY EYE and must stay that way.** Both ends of an occluder quantise
  — the crop to whole texels of a 64px file, the draw to whole units of the host frame, because
  `CreateTextureMarkup` emits every field with `%d` — so a drawn size almost never lands exactly
  on its crop. A search that minimised that residual picked `0.78125` over the measured `0.82`,
  on arithmetic saying it was six times more accurate, and it **visibly resized the icon** where
  0.82 does not. The residual is therefore a diagnostic the probe prints, **not** an objective to
  optimise: nothing here models what actually governs an inline escape's apparent scale.
  `/sg tune crop <n>` picks a replacement on the real row, by looking. `Look.OCCLUDE_X` / `_Y`
  are a sub-unit trim on the FontString's own anchor, because an escape's offsets are integers.
- **The occluder DRAWS on a live row and is aligned**, at crop `0.82` with an x trim of
  `+1.2` units, both measured by eye. The trim is there because a centred escape does not draw
  centred — it claims more advance width than its ink fills, so a `CENTER` anchor centres the
  claim (`security-taint-and-restricted-data.md` §3.5). ⚠ **OPEN: whether `+1.2` is a constant
  in units or a fraction of the draw.** One icon size cannot tell them apart, and it is the
  whole durability question — move the Edit Mode icon-size slider and look again. If it still
  lands the constant is right; if it drifts it belongs in the source as a ratio.
  `/sg tune crop|x|y` changes the live occluder and re-arms; `/sg probe occluder` lays the crop
  in force beside its neighbours and an x-trim sweep beside that. ⚠ **The probe takes the
  overlay's scale** — a replica at a different scale rounds differently from the row it stands
  in for, and then disagrees with it, which is how a probe reading and a live reading came
  apart once already.
- ⚠ **Still unflown: whether the Cooldown Manager's Wild Imp buff is genuinely continuously
  present.** It is load-bearing — band 0 draws, so an absent aura means no button, no occluder,
  and a mark that reads as six (`rule-language.md` §6.4).
- ⚠ **Two mismatches the occluder cannot hide, both accepted.** The overlay sits at item level
  +5 and the swipe, `ChargeCount` and `CooldownFlash` all sit at +1, so a static copy of the icon
  draws over them. `ready(implosion)` removes the cooldown case outright and is the right
  rule anyway. Out-of-range and not-usable remain: `RefreshIconColor` tints the real icon and our
  copy is untinted, so a patch would show. Both are readable (`C_Spell.IsSpellInRange`,
  `C_Spell.IsSpellUsable`) if they turn out to matter in play.
- **The two bowls.** `when` carries unlimited readable terms; `bind` is one slot holding at
  most one sealed leaf, so at-most-one is structural rather than checked. `count` became
  `bind = { family = "count", … }` and survives as a legacy key on decode. The checker refuses a
  term in the wrong bowl **by name, both directions** — a sealed `X.stacks` offered to `when`,
  a readable `soul_shards` offered to `bind`.
- **Names in the surface.** `Symbols.lua` is generated from the KB's ability inventory by
  `wowkb.gen_smartglo_symbols` — 3,988 ids across all 40 specs — and `Names.lua` resolves a bare
  name inside a `spec` scope, a `class.spec.name`, or a raw id, refusing an ambiguous word rather
  than guessing. `/sg symbols` checks every row against `C_Spell.GetSpellName` in the live
  client, 250 ids a frame, and runs silently on login: the client is Tier 1 for `id → name`, so a
  patch rename is caught with no flight.
- **Rules are authorable in the game.** `Parse.lua` reads the same grammar `wowkb.smartglo`
  reads; the config box shows rule TEXT and takes either text or an `SG1:` string, and
  `/sg export text` gives the editable form. ⚠ The grammar now exists in two languages. The
  refusal STRINGS are what drift, and the capture log is the only detector — there is no test.
- **`talent()`, off the TRAIT CONFIG.** `C_ClassTalents.GetActiveConfigID` →
  `C_Traits.GetNodeInfo`, checking `ranksPurchased > 0` **and** `activeEntry.entryID`, so a
  choice node answers about the half the player actually picked. `C_SpellBook.IsSpellKnown` was
  rejected: it answers about a **spell**, not a node, so it stands in for the talent rather than
  being it, and a spell known from another source diverges silently — under a `not` a wrong
  `false` reads as a confident true. `Symbols.talentNodes` maps 2,469 talent spells to their
  `{node, entry}` pairs, generated from the KB's 40 `talents.json`; a spell that names a
  different node in another spec carries every candidate and the client arbitrates by refusing
  the one outside the player's tree. The fold is cached against the config id and dropped on
  `TRAIT_CONFIG_UPDATED` / spec change. ⚠ `C_Traits.GetNodeInfo` is **unmeasured** — every read
  is `pcall`ed and every unrecognised shape reads UNKNOWN, so a refusal costs a glow and can
  never invent one.
- **One frame per rule.** The subject frame carries attached-and-not-editing, an element frame
  per rule carries the readable gate, and the mark's alpha is left to whatever sealed the rule.
  Three channels, one owner each, decided at build. A count element's container hosts on its
  own element, so two rules on one icon no longer share an occluder.
- **The sealed health bind.** `Health.lua` compiles `health% < N` to a Step curve and hands it
  to `UnitHealthPercent("player", false, curve)`, whose result -- secret -- goes straight to the
  mark's alpha. Health can never be a gate: `UnitHealth` is unconditionally secret, so the
  readable half carries only what is readable (the Holy Power cost) and the threshold is the
  client's to evaluate. Shares the duration bind's 10 Hz ticker shape and its alpha ownership.
  ⚠ **Unflown**, twice over: the curve-to-alpha path has never been seen to work, and the
  curve's **input scale** is undocumented with no Blizzard caller to copy. The curves are shaped
  so the wrong scale reads DARK rather than permanently bright -- an extra Step point just above
  1 takes the whole 0..1 range to zero -- so the failure is a glow that never appears.
- **The sealed duration bind.** `Duration.lua` compiles `X.cooldown > Ns` and
  `outside A..Bs` into a Step curve, hands it plus the opaque duration object to the engine, and
  writes the secret result straight to `Texture:SetAlpha`. `>` and `>=` compile to the same
  curve, because Step is a floor and the client cannot draw the difference. Re-applied on one
  shared 10 Hz ticker, which draws and never evaluates. ⚠ **Unflown** — no eyeball has seen a
  Step curve drive a mark across a threshold, and there is no programmatic oracle for one.
- **The capture log.** One `attach` stream, six sessions: every dirty trigger by source, every
  flush with the subjects that found no frame, every verdict change with its per-term
  `T | F | ?`, aura-latch edges and UNKNOWN latch reads, count arm outcomes, parse refusals, and
  combat / Edit Mode / spec edges. Read it with
  `uv run python -m wowkb.capture sg attach`. The 10 Hz ticker never writes a line.
- **An override swap re-resolves.** `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` marks dirty: a proc
  that swaps a row's spell keeps its cooldownID, so `OnCooldownIDSet` is silent for it and the
  bound map would go on naming the base spell. Ruination over Hand of Gul'dan and Infernal Bolt
  over Shadow Bolt both depend on it. ⚠ **Unflown.**
- **The Diabolist profile.** `demonology-diabolist`, eleven glows transcribed from the simc
  `diabolist` list, with `rules/demonology-diabolist.sg` as its on-disk twin — the two render
  identically through `Parse.Render`, which is the cross-check that the shipped table and the
  file say the same thing. ⚠ **Unflown**, and `aura(1276166)` needs a Tracked Buffs checkbox on
  Dominion of Argus before it can ever read anything but UNKNOWN.
- **Two Paladin profiles.** `retribution-herald` and `protection-lightsmith`, nine glows each,
  from the simc lists plus Method's 12.1 Protection priority, each with a `rules/*.sg` twin the
  profile table parses identically to. Hammer of Light is absent from both by design: it comes
  from Light's Deliverance, a **Templar** talent neither tree has. ⚠ **Unflown**, and every
  `aura(...)` term needs a Tracked Buffs checkbox before it reads anything but UNKNOWN.
- **`talent()` can read HERO talents.** The symbol generator walked `trees.hero` as a list, but
  it is a dict keyed by hero-tree name, so iterating it yielded strings and every hero talent in
  the game was silently missing — `talent(walk_into_light)` read UNKNOWN and its glow stayed
  dark. 2,469 mapped talent spells became 3,163.
- **What the flight did NOT cover**, and it is the question the attach path was built to answer:
  **whether a glow survives its icon being rebound to a different spell.** Nothing has forced a
  rebind or a re-layout under a live overlay, Edit Mode has not been opened with one attached,
  and the icon-size slider has not been moved. Until then the rebuild-on-flush design is
  reasoning, not measurement.

## Now

### Subject → frame resolution

A glow attaches to its subject's **cooldown row, and to zero or one of them**. Essential and
Utility are mutually exclusive placements of the same row rather than two frames — the drag
table moves rather than copies, and `GetValidAssignmentCategories` only offers categories from
the tab currently open `[T1 src @12.1.0: CooldownViewerSettings.lua]`. The aura-family row a
spell may separately carry answers a different question and is out of scope for v1
(`cooldown-manager.md` §1.1).

**A subject with no frame must read UNKNOWN in `/sg why`, never silently nothing.**
`GetCooldownViewerCategorySet` is a *superset* of the rows the viewers lay out, so resolution
has to distinguish a subject that has a frame from one that does not, and say which. Glowing
nothing while reporting success is the single most likely way this addon lies to its user.

⚠ The **picker cannot offer a frameless subject**, because it is built by *enumerating live
item frames* rather than by walking the category set — so "a subject with no frame" is
unrepresentable there rather than a state the dropdown has to detect. The UNKNOWN path above is
still needed, for a rule that arrives by paste or from a profile.

### One rule, end to end

**Soul Shards `>=` N on one hand-picked subject, glowing a real CDM icon** (Demonology is the
target spec). The point is the attach path, not the vocabulary: a secondary resource is a plain
`UnitPower` read, so the rule carries **no sealed binding, no band table and no refresh tick**,
and what the flight actually tests is the attachment. `cdm-rider-patterns.md` §4.2's rebind hook
is the seam, and **whether a glow survives an icon being rebound to a different spell** is the
question the first flight answers.

The overlay is **our own texture on our own frame** — parented to `UIParent`, two-point
**anchored** (`TOPLEFT`/`BOTTOMRIGHT`) to the item frame, never *parented* to it, which would
break Blizzard's pandemic-frame anchor chain (`cooldown-manager.md` §4.1). Being an
anchor-*follower* rather than an anchor-*setter* is what makes it cheap: Blizzard's `Layout`
moves the icon and the overlay follows in the same frame, with no hook and no reassert — so
§4.6.1's reassert seam and its two-riders hazard, which are about addons that *move* item
frames, do not apply.

### The config: one dialog — subject dropdown, detail pane, text box

**Decided 2026-09-08** (`rule-language.md` §8). One frame carrying three things:

- **A subject dropdown built by iterating the live CDM item frames** — each viewer's active
  item frames, each resolved `GetCooldownID()` → `C_CooldownViewer.GetCooldownViewerCooldownInfo`
  → the **currently-bound** spell (`overrideSpellID` when present). Because the list is built
  from frames, every entry has one.
- **A detail pane** driven by the selection: that subject's rules, and per-term `T | F | ?` for
  `/sg why`.
- **A text box that is ALSO the import/export surface** — the selected subject's rules as
  editable text, with copy / paste / apply / cancel. There is no second export UI.

Rebuild the dropdown on `CooldownViewerSettings.OnDataChanged`, deferred one frame
(`cdm-rider-patterns.md` §4.5).

⚠ **Clicking the icon itself was the earlier plan and is DROPPED.** Blizzard makes item frames
non-clickable on purpose — `CooldownViewerItemMixin:SetTooltipsShown` calls
`self:SetMouseClickEnabled(false)`, reached from `OnAcquireItemFrame` (every pool acquire, so
every `RefreshLayout`) and from the viewer's own `SetTooltipsShown`. Re-enabling it from tainted
code is a standing re-assert war against a user setting, restarted on every layout.

### Rule serialization: JSON through `C_EncodingUtil`

`SG1:` + `EncodeBase64(CompressString(SerializeJSON(ast), Deflate))` — all three calls ship in
the client (Tier 1, `state-persistence-and-communication.md` §6.1), so the Lua side is three
built-ins and the Python side is stdlib. ⚠ `pcall` every call and checksum the payload: these
raise rather than return nothing, and `DecodeBase64` accepts invalid input and returns a short
string. Wants a `wowkb` subcommand on the Python side (`rule-language.md` §7 constraint 3).

### Built-in profiles in `Profiles.lua`

Named rule sets carried in the addon source, so a profile can be authored outside the game,
deployed, and picked up on `/reload`. Hand-editing SavedVariables was **rejected** as the
supported path — `/reload` commits SavedVariables from memory *before* reloading
(`anatomy-and-runtime.md:955`), so an edit made while the client is running is overwritten.
The paste box covers anything not pre-baked.

### The evaluation loop

Each term declares the events that change its answer; a glow's trigger set is the union over
its leaves — no blanket `OnUpdate`. Sealed **duration** leaves are the exception: a curve
evaluation is a snapshot, not a live binding, so they re-arm on a **10 Hz** ticker, and only a
glow that uses one pays for it.

### The rule language exists as a design

`rule-language.md` is the thing to read before writing any rule-evaluation code, and the thing
to correct where a flight disagrees with it. §5's two bowls, §6's gate-over-binding composition
and §7's syntax are built; §9's open client questions are not, and are what the next flight is
for.

What it decided, so it is not re-litigated: **subject-first** (rule-first deferred until
repetition is felt) · **configuration, not code** (re-examined against a direct request for a
Lua predicate surface, and kept) · **import/export in scope**, wire format free to be an
opaque base64 blob but decodable in Python with no Lua interpreter · **multiple glows on one icon are independent
layers**, and draw order is the entire arbitration vocabulary.

A second decision session on 2026-09-08 closed six more, all in §8: **the config is one
dialog — subject dropdown, detail pane, text box** · **profiles live in source** · **terms
resolve against the icon's currently-bound spell**, `base(...)` to force · **v1 has one fixed look and no `look`
keyword** · **triggers come from a term catalogue** plus a 10 Hz tick for sealed duration
leaves · **one cooldown row per subject**, no frame → UNKNOWN. Its §9 now carries **client
facts only**: selectors, the customizable `look` vocabulary and temporal terms were deleted
rather than deferred, and nothing downstream refers to them.

## Parked

### The vocabulary the APLs want and we do not have

From §10's exercise, in priority order: **enemy count** (by far the most wanted — it is the
difference between "Implosion at 6 imps" and the APL's real condition), GCD remaining, time in
combat, and guardian-active. `fight_remains` / `target.time_to_die` and `raid_event.*` are
unreachable rather than missing.

### Rule classes beyond resource thresholds

Aura present/absent, stacks, charges, target count. All plausible, none scoped. The v1
vocabulary is deliberately one class wide so the attach path is what gets proven.

⚠ `rule-language.md` §1 now says which of these are **gates** and which are **bindings**, and
they are not the same kind of work. Aura presence and "on cooldown at all" are ordinary
readable gates. Stacks are a binding whose only sink is a leaf FontString — so what the client
draws for a stack count is an inline texture laid out as text rather than a ring around the
icon, which is a product decision hiding inside what looks like a rule class. An escape takes
alpha and no geometric transform, so the way to a mark that moves is the **occluder**: band 0
hides our own spinning Texture and the threshold reveals it. The motion still cannot vary per
band. Charge COUNT is neither gate nor binding and must be refused outright.

### Blizzard's own next-cast suggestion as a rule input

`C_AssistedCombat.GetNextCastSpell` is readable and `cdm-rider-patterns.md` §8 documents the
rider, so "glow the icon the client would suggest next" is available as a rule predicate
whenever we want it. Parked for the same reason every other rule class is: v1 proves the
attach path with one predicate. Recorded so the capability is not rediscovered as a novelty.
No position taken here on how far toward rotation advice the addon should go — that is a
call to make against a concrete request, not one to pre-decide in the backlog.
