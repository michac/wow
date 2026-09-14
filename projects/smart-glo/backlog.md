# Smart Glo — backlog

**What this file is for:** what is not yet established, and the ordered work list.
`README.md` owns the design and why it is shaped the way it is.

**It does not inventory what works.** A "what is built" list restates the code less accurately
than the code does, and goes stale on the next commit; `Status` was deleted for that reason.
The thing code cannot tell you is whether a built thing has ever been seen to WORK in the
client, so that is what `## Unproven` keeps.

The live addon version comes from `wowkb.addon list`, never from prose here.

**Measurements do not live here.** A fact this addon establishes about the client belongs in
`knowledge/addon-dev/`, where the KB's gates apply and the next reader will actually find it. A
line here may say a thing is unproven; what a flight then establishes is a claim in a topic
file, and discharging the line means deleting it, not writing the finding into it.

**An item here has to keep earning its place.** If its premise stopped being true, rewrite it or
delete it — never leave it standing with a note underneath.

## Unproven

**It records what is NOT established.** Every line is a claim a flight or a measurement can
discharge — when one does, delete the line. What is built and working is in the code, and the
code does not go stale; this section is not an inventory of it.

- **Whether a glow survives its icon being rebound to a different spell.** This is the question
  the attach path was built to answer, and nothing has forced a rebind or a re-layout under a
  live overlay. Edit Mode has not been opened with one attached and the icon-size slider has not
  been moved. Until then rebuild-on-flush is reasoning, not measurement.
- **Whether an override swap re-resolves.** `COOLDOWN_VIEWER_SPELL_OVERRIDE_UPDATED` marks
  dirty: a proc that swaps a row's spell keeps its cooldownID, so `OnCooldownIDSet` is silent
  for it and the bound map would go on naming the base spell. Ruination over Hand of Gul'dan
  and Infernal Bolt over Shadow Bolt both depend on it, and both are in the shipped Diabolist
  profile — a report that one of them never lights is most likely this.
- **`<resource>.after_cast` has never been seen to move.** The `UNIT_SPELLCAST_START` ledger
  and the cost/gain arithmetic are exercised offline, but no eyeball has watched a mark change
  mid-cast.
- **Whether the Cooldown Manager's Wild Imp buff is genuinely continuously present.** It is
  load-bearing: band 0 draws, so an absent aura means no button, no occluder, and a mark that
  reads as six (`rule-language.md` §6.4).
- **Whether the occluder's `+1.2` x trim is a constant in units or a fraction of the draw.**
  One icon size cannot tell them apart, and it is the whole durability question — move the Edit
  Mode icon-size slider and look again. If it still lands the constant is right; if it drifts it
  belongs in the source as a ratio.
  ⚠ It cannot be settled arithmetically. Both ends of an occluder quantise, so a drawn size
  almost never lands on its crop; a search minimising that residual picked `0.78125` over the
  measured `0.82` and **visibly resized the icon**. The residual is a diagnostic the probe
  prints, not an objective — nothing models what governs an inline escape's apparent scale.
  `/sg tune crop|x|y` changes the live occluder by eye. ⚠ **The probe takes the overlay's
  scale**, so a replica at a different scale rounds differently from the row it stands in for;
  that is how a probe reading and a live reading came apart once already.
- **Every `aura()` term and every count bind needs a Tracked Buffs row** for its aura, or it
  reads UNKNOWN forever and its glow never lights. This is a player-side checkbox no one will
  think to tick unless the addon says so, and it is currently unsaid. It gates all three
  shipped advice profiles; `aura(1276166)` on Dominion of Argus is the Diabolist case.
- **`affordable()` and the `power` bind family are built and have never run in the client.**
  Both grammars parse them, both checkers accept them, the Lua and Python ASTs were compared
  equal, and `rules/havoc-felscarred.sg` uses both — none of which is a pixel.
  `affordable()`'s evidence is a `[client 2026-08-03]` READ of `C_Spell.IsSpellUsable` from a
  probe, not this term inside a glow, so what is unflown is the wiring: at low Fury the
  spenders must go dark while Felblade and Immolation Aura stay lit. `fury% < 80` is the first
  power bind ever armed and its diagnostic is the capture log — `power <subject> fury% < 80 ->
  <secret>` is the client owning the alpha, a plain NUMBER means the curve domain is not
  [0, 1]. ⚠ With the domain wrong a `<` curve lights ALWAYS rather than never, so a mark that
  is on at full Fury is the first thing to suspect.
- **Whether the Cooldown Manager lays out an Eclipse row at all on Elune's Chosen.** The
  balance inventory flags exactly one Eclipse id as a CDM row, `solar_eclipse` 1233346, with
  `lunar_eclipse` 1233272 and the bare `eclipse` 1239669 carrying none — and Lunar Calling, an
  Elune's Chosen node, DISABLES Solar Eclipse. Two rungs in `rules/balance-eluneschosen.sg`
  ride that row. If the row is absent or is the Lunar id instead, they never light and nothing
  says why, because a subject with no viewer row is indistinguishable from a gate reading F.
- **Whether `aura(eclipse)` 1239669 is the row that carries under Lunar Calling.** The buff you
  hold is `eclipse_lunar` 48518. The Force of Nature and Wild Mushroom rungs gate on the
  generic id; if both stay dark inside Eclipse, that is the swap to make.
- **Whether `UnitPowerPercent` on a power the player does not have returns a plain number, a
  nil, or raises.** `Power.lua` handles all three the same way — dark, with the class logged —
  and deliberately compiles no class-to-power table, so a `fury%` rule on a Paladin is a
  runtime dark rather than an authoring refusal. Which of the three happens is unmeasured.
- **`C_Traits.GetNodeInfo` is unmeasured**, so `talent()` rests on an unverified read. Every
  call is `pcall`ed and every unrecognised shape reads UNKNOWN, so a refusal costs a glow and
  can never invent one.
- **`wasSetFromAura` / `auraInstanceID` are Tier-3** (`mined-pending-verification.md` E2,
  `@verify-ingame`). A client without them makes the aura latch's cooldown-viewer half silent
  and the edge latch carries it exactly as before.
- **The rule grammar exists in two languages, and the test covers one corpus.**
  `tools/tests/check_smartglo.py` runs a fixed corpus through both — asserting accept/reject
  parity and identical rendered text, and printing each refusal side by side — which is what
  caught `essence_break.up` in `- **Auto-load has never run in the client.** `/sg enable` reads the spec through
  `C_SpecializationInfo.GetSpecializationInfo` and the hero tree through the same
  `C_Traits` read `talent()` rests on, which is itself unmeasured — so the tree half can
  read UNKNOWN for a reason that has nothing to do with the player's build, and the path
  that matters (log in, watch the right profile arrive) has not been walked. The
  per-character `SmartGloCharDB` file has never been written or read back either.

## Now` below. It does NOT compare refusal wording (the two
  spell the dash differently on purpose) and it only knows the forms somebody wrote into the
  corpus, so a family added without a corpus entry is still untested. The capture log remains
  the detector for anything the corpus does not name.
- **Whether a plate that TURNS reads differently from one that sits still.** The black plate
  was reverted for reading as a hole punched in the row rather than as a ground under the mark;
  the theory is that a still plate is scenery while one turning in step with the mark is part of
  the same object. That is a theory about why something looked wrong, and only a look confirms
  it.
- **Whether `purple` at 35% is the right value for the plate.** Full `purple` would hand back
  the 15% luminance swing the black↔yellow cycle exists to undo; 35% keeps the hue at a Michelson
  0.60 under the bright phase. The arithmetic says it works and nothing has judged whether it
  still reads as purple at 40px rather than as a dark blur.
- **Whether `black` at 0.02 is an absence or a grey stroke.** The same swing shipped once with
  its dark end at 30% of `yellow` and was reported as grey. 0.02 is far past the 15% that
  corrected it, and against the plate the dark phase is now the mark going *darker than its own
  ground* — a different reading from disappearing, and an unjudged one.
- **Two mismatches the occluder cannot hide, both accepted.** The overlay sits at item level +5
  and `RefreshIconColor` tints the real icon while our copy is untinted, so out-of-range and
  not-usable would show as a patch. Both are readable (`C_Spell.IsSpellInRange`,
  `C_Spell.IsSpellUsable`) if they turn out to matter in play — which nothing has tested.

## Now

### A `remains` bind can only watch the target

`bind <aura>.remains < <n>s` hardcodes the container to `target` / `HARMFUL|PLAYER`, because
the family exists for a DoT you are maintaining and the grammar carries no unit. A `remains`
bind named on a **self-buff** therefore matches nothing, arms no occluder, and leaves the mark
bright whenever the implicit presence gate passes — the mirror of the hazard `count` carries
for a target debuff, and the same shape §6.4 describes. The presence family already solved
this with `[on <unit>] [mine]`; the question is whether `remains` should take the same tail or
whether its unit should be inferred from the aura's own row.

### The two grammars disagree about what an aura BIND may name, and a shipped rule is caught in it

`rules/havoc-felscarred.sg:185` — `bind essence_break.up on target mine` — **does not load in
the addon.** `Parse.ResolveAura` resolves in the aura namespace with no fallback, and Essence
Break has no tracked row, so line 185 is a refusal and the whole file is rejected. The Python
tool used to accept it by falling back to the ability inventory; that fallback is gone now
(the two grammars agree), which is what made the breakage visible.

The design question underneath is real and unanswered: `aura()` genuinely needs a CDM row
(it rides the alert edges), but a **container bind does not** — `Presence.lua` reads through
`C_UnitAuras.GetUnitAuraInstanceIDs` and reaches any aura on any unit. So the aura table may
be the wrong universe for the three container families, and the refusal string is wrong for
them too: it says "an aura() term reads through a Cooldown Manager row" about a bind. Either
the container binds get a wider namespace, or that rung needs a different form.

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

### Which mark actually survives the periphery

`site/styles.html` carries seven candidates and one of them has been built, released, flown and
reverted: the mark shrunk over a **translucent black plate**, the cycle swinging one hue
dark↔bright instead of purple→yellow, and `urgent` moved off the size channel onto a **bounce**
run 18% faster than a plain glow. Offline it won everything — `tool/measure_motion.py` put its
urgent rate and swing above every other row, and under the lab's blur it survived backdrops the
bare hexagon disappears against.

It lost as a whole and was then taken apart, and three of its four ideas are shipping: the
**smaller mark** (`FRACTION` 0.53), the **dark end of the swing** (`alarm` is black↔yellow), and
the **plate** — purple rather than black, and turning in step with the mark rather than sitting
still under it. A still black plate read as a hole punched in the Cooldown Manager row; whether
turning it fixes that is `## Unproven`'s to answer. The **bounce** did not come back: beside
icons that were not moving it read as fidgeting, and `urgent` is a pop again.

⚠ **The lesson is about the measurement, not the candidates.** Every offline axis this project
has — blur, rate, swing — ranked the whole package first, and could not tell which of its parts
were carrying it. They rule a candidate *out*; they cannot pick the winner, and a row at the top
of `measure_motion.py` is a reason to go and look, never a reason to ship. The retired entries
stay in the lab so the next session finds that already written down.

## Parked

### The vocabulary the APLs want and we do not have

From §10's exercise, in priority order: **enemy count** (by far the most wanted — it is the
difference between "Implosion at 6 imps" and the APL's real condition), GCD remaining, time in
combat, and guardian-active. `fight_remains` / `target.time_to_die` and `raid_event.*` are
unreachable rather than missing.

**Protection's "Consecration to refresh, nothing else up", which `<aura>.remains` does not
reach.** The rung should fire in the last few seconds of the field and instead fires whenever
the builders are down. The `remains` family cannot answer it: the Consecration aura a rule can
name is `188370`, the *standing in it* flag, whose `SpellDuration.Duration` is `-1` — a
presence marker with no clock. The 12s field lives on the cast, `26573`. So this one needs a
source neither the duration nor the remains family offers, and scoping it should start by
establishing whether the CDM hands out a duration object for that row at all.

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
