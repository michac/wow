---
title: KB Inbox — free-form parking lot for un-routed todos
patch: 12.0.7
fetched: 2026-07-10
reviewed: 2026-07-10
confidence: high
---

# KB Inbox

A **free-form parking lot for the game KB and this workspace's tooling**. Drop a todo
here the moment it appears, instead of half-implementing it, or asserting an unvalidated
claim into a `knowledge/**` file. Nothing here is trusted as fact or acted on
automatically — it's a holding pen until someone routes each item to where it belongs.

⚠ **`knowledge/addon-dev/` does not park anything here.** That subtree is firewalled from
the game KB (its README §0) and runs **four queues of its own** — `observations.md`,
`mined-pending-verification.md`, `<version>-ptr-heads-up.md`, and the unknowns registry
`projects/addon-lab/questions.json` (`wowkb.lab note`). An addon-dev *claim* or *open
question* goes to one of those, never here. What may still land here is a **structural or
tooling** call *about* that subtree — "should addon-dev grow an eighth topic file", "teach
`wowkb.lab` to validate anchors" — because that is workspace work, not a claim.

## What goes here vs. the other queues

This is deliberately the *catch-all*. Use the more specific queue when one fits:

| If the todo is… | Put it in | Not here |
|---|---|---|
| a **claim that needs an in-game check** before we trust it | the in-line verify marker on the claim → harvested into `verify-in-game.md` by `wowkb.gen_verify` | ✗ |
| a **weekly the addon saw but the watchlist doesn't track** | `planning/discovered-weeklies.json` (auto-maintained) | ✗ |
| a **per-reset chore to tick off** | `planning/todo.md` (session checklist) | ✗ |
| a **stub/next-step scoped to one KB doc** | that doc's own `## TODO` section (a **game-KB** convention — `addon-dev/` has none and wants none) | ✗ |
| **anything about writing addon code** — a fact, an unknown, a patch-day landmine | the four `knowledge/addon-dev/` queues above | ✗ |
| **anything else** — tooling ideas, a feature idea for one of our addons, research-to-do, structural KB work, "look into X" | **here** | ✓ |

## How to use it

- **Add:** append a bullet under the right heading (or make a new heading). One line of
  *what* + one of *why it matters* + any *how/pointer* is plenty. Date it.
- **Route/clear:** when an item is implemented, or promoted into a real KB doc / an
  in-game-verify marker / a tool ticket, **strike it and note where it went** (or delete
  it). This file should shrink as often as it grows.
- **Don't** let items rot silently — a `/update` or sync is a good moment to skim it.

---

## Tooling / KB structure

- **📌 12.1.0 addon-API sweep — driving doc `knowledge/addon-dev/12.1.0-ptr-heads-up.md`
  (2026-08-04).** Five-file audit of `addon-dev/` against the PTR
  `Patch_12.1.0/API_changes` page: nothing in the KB is falsified *today* (all
  changes are PTR-only, docs well-hedged), so **do not touch the `patch: 12.0.7`
  bodies until 12.1.0 is live**. The heads-up doc carries the per-file patch-day
  anchor list. Headline: **auras go fully secret** (`C_UnitAuras` secret vectors,
  `UNIT_AURA` secret payload, `SecureAuraHeaderTemplate` removed →
  `AuraContainer`/`AuraButton`) + **unit-identity APIs return secrets**. Only one
  live *example* actually rots: `UIParentLoadAddOn` → `LoadAddOnWithErrorHandling`.
  On patch day the `/update` full-apply + `kb-patch-sweep` should consume the
  heads-up doc's edit list (and re-pull exact signatures verbatim — the initial
  fetch paraphrased some). Also flags a separate **Cooldown HUD / CDMProbe**
  review pass (route via `todo/addon-engineering.md`).

- **BucketBinds: source `spec_inventory` talents from wago `Trait*` (shrink `inventoryGaps` to
  zero).** The talent side of `wowkb.spec_inventory`'s union comes from `all-talents.tsv`, built
  off the Blizzard talent-tree API — whose static build (67808) **itself omits some real
  talents**, and a `wowkb.talents fetch` re-fetch returns the same holes (verified during the
  floats rollout). The floats workflow works around it with a **relaxed name-gate** (a name in the
  spec's `rotation.md` **and** in `raw/wago/SpellName.csv` is allowed, flagged in `inventoryGaps`,
  resolved by-name at runtime), but the real fix is to build the talent inventory natively from the
  wago **`Trait*`** tables (`TraitNodeXTraitNodeEntry` → `TraitNodeEntry` → `TraitDefinition.SpellID`,
  joined to the spec's tree via the manifest). Then API-omitted talents are covered and
  `inventoryGaps` shrinks to zero. **Per-spec gaps observed across the DPS/tank floats rollout**
  (the verification checklist — each already resolves in `SpellName.csv` and binds at runtime):
  - Hunter/Beast Mastery: Wailing Arrow
  - Hunter/Marksmanship: Arcane Shot, Steady Shot, Multi-Shot, Wailing Arrow
  - Mage/Arcane: Arcane Blast · Mage/Fire: Fireball
  - Monk/Brewmaster: Empty the Cellar · Monk/Windwalker: Zenith Stomp
  - Paladin/Protection: Hammer of Wrath, Hammer of Light, Hammer of the Righteous
  - Paladin/Retribution: Hammer of Light, Hammer of Wrath, Templar Slash
  - Priest/Shadow: Void Volley
  - Rogue/Subtlety: Shadowstrike, Shuriken Storm, Black Powder
  - Shaman/Elemental: Fire Elemental, Storm Elemental
  - Warlock/Destruction: Incinerate
  - Warrior/Arms: Heroic Strike · Warrior/Protection: Devastate
  - (Batches 1–2 — Frost Mage, Evoker Engulf, Devourer Consume/Devour/Pierce the Veil, etc. — noted
    in prior sessions; fold those in when building the checklist.)

- 🧭 **Planner re-architecture — see `../planning/goal-model.md` (design proposal, 2026-07-10).**
  Replace the activity-centric multiplier scorer (`scoring-model.md`) with a **goal-centric**
  pipeline: per-slot upgrade-candidate graph → goals → rank(value, steps) → select-to-time →
  TODO expansion with **shared-step dedup**. This is the agreed direction; the doc has a worked
  Uncomplete sketch. The remaining scoring items below are folded into it.

## Cooldown HUD / CDMProbe

- **⚑ DRIVING DOC: `todo/addon-engineering.md`** — the multi-session program covering
  the lab addon, verifying the new `knowledge/addon-dev/` KB against the client, a
  `wow-developer` skill, and the Cooldown HUD audit + three-layer refactor (game-state
  abstraction / rotation engine / display engine), plus a UI test mode, rotation-engine
  unit tests and several independent code reviews. **The audit is landing:** W4a
  (dead-code strip) and W4b (the `HudBoard` engine + the `docs/architecture.md`
  pipeline design) are done; **Cooldown HUD *feature* work stays frozen until the
  rest of W4 lands.** Items below that the program supersedes should be struck as it
  absorbs them, not worked in parallel. *(updated 2026-07-24)*


_(design context: `projects/cooldown-hud/docs/`; source-read findings folded into
`notes.md` §1 + §6/§8 on 2026-07-22, build 68453.)_

- **Affliction pandemic probe (verify-in-game).** The pandemic mechanism is
  understood from source (`notes.md` §1 "Pandemic — two edge signals") but is
  **untested in restricted combat** — the probe has only ever run on Demo, which
  tracks no target-DoT. Log onto Affliction, get Agony on a target dummy in a
  delve, and confirm: (a) `hooksecurefunc(item, "ShowPandemicStateFrame", …)` fires
  in combat, (b) `TriggerAlertEvent(PandemicTime)` shows in the choke-point counter,
  (c) `self` resolves to the item's base spellID for glow routing. Gates any DoT
  assist. *(2026-07-22)*

- **Second spec / generalization (M7, but seed it now).** Two source-grounded
  levers make "40 specs" tractable rather than 40 hand-authored tables:
  1. `C_CooldownViewer.GetCooldownViewerCooldownInfo(cooldownID)` returns a
     **readable** per-item classifier (`hasAura`/`selfAura`/`charges`/
     `linkedSpellIDs`/`flags`) — a candidate `wowkb.gen_spec_table <spec>` could
     fuse it with `spec_inventory` + `simc`/`rotation.md` into a draft
     `Spec<Name>.lua`. Richer than the current hand-authored `kind = "button"|"aura"`.
  2. The engine's **judgment layer isn't spec-agnostic yet** — `HudScore`/`HudState`
     hold the Demo builder/spender→Tyrant model as control flow. Adding a
     same-archetype second spec (Ret / Feral / Rogue) is what forces the
     resource/mode model into declared fields. Do that before any DoT spec.
  See `milestones.md` §6 M7 second-spec bullet for the full framing. *(2026-07-22)*

- **Reading the player's BUILD (spec + hero tree) has no home in `knowledge/addon-dev/`.**
  The seven topic files partition the *programming model*; "which API tells me the player's
  current spec / hero talent tree / loadout" fits none of them cleanly, and the only mention
  anywhere is an incidental `GetSpecializationInfo` note in
  `state-persistence-and-communication.md` §2.3 (about logout, not about spec reads).
  Two Tier-1 facts established 2026-07-30 while fixing CDMProbe's hero detection, worth
  keeping wherever this eventually lands:
  - `C_ClassTalents.GetActiveHeroTalentSpec()` → the active **SubTreeID**, nilable —
    **nilable confirmed in-client** `[client 2026-08-06]`: a Retribution Paladin with no
    hero tree returned nil through `pcall`, i.e. a genuine "none", not a refusal. (cap
    v0.2.0's `bind` log renders the four cases apart — a name · `#id` · `-` none · `?`
    unreadable — and logged `hero:-`.)
    *[T1 docs: `Blizzard_APIDocumentationGenerated/ClassTalentsDocumentation.lua:82`;
    used by Blizzard itself at `Blizzard_MicroMenu/Mainline/MainMenuBarMicroButtons.lua:723`]*.
    Warlock SubTreeIDs @ 12.0.7: Soul Harvester 57, **Hellcaller 58, Diabolist 59**
    *[T1 DB2: `TraitSubTree` @ 12.0.7, TraitTreeID 720]*.
  - **`PLAYER_SPECIALIZATION_CHANGED` is not enough to invalidate a hero-tree cache** — a
    hero swap changes the build without changing the spec, so `TRAIT_CONFIG_UPDATED` is the
    event that actually fires. (It fires several times per loadout swap, so anything it
    triggers must be idempotent and must not re-announce an unchanged answer.)
    [Reasoned from the event's purpose, not yet observed in-client. Registered as
    `traitconfig-fires-on-hero-swap` in `projects/addon-lab/questions.json`.]
  Deciding whether this becomes an eighth topic, a section of `api-events-and-discovery`, or
  stays parked is a KB-structure call, not a drive-by edit. *(2026-07-30)*

## Research to-do

- **The addon-mining queue lives in its own file, not here.**
  `knowledge/addon-dev/mined-pending-verification.md` (created 2026-08-05 by the first
  `/mine-addon` run, against EllesmereUI 8.7.5). It holds everything mined from a
  third-party addon that is **Tier 3 or needs a client** — nothing in it is asserted
  anywhere, and each item names exactly what would settle it.
  ⚠ It is a **third** queue, deliberately distinct from the two that already exist:
  `_meta/verify-in-game.md` is **generated** from `@verify-ingame` markers on claims the
  KB *already asserts* ("confirm this while logged in"); this inbox is free-form and
  un-routed. The mining queue is neither — several of its items need a **Tier-1 re-read**
  or a **PTR**, not a login. Not harvested by any tool.
  ⚠ **Its former headline item is ANSWERED and should be struck from that file** — whether
  `item.auraDataCached` is plain in combat. `cooldown-manager.md` §7 now carries the
  measurement `[client 2026-08-05]` and **the answer is no**: the container is plain but
  `expirationTime` / `duration` / `timeMod` / `applications` are all secret (only
  `auraInstanceID` is plain). So the in-combat DoT-remaining read stays unanswerable. The
  matching `[gap]` line in §9 was deleted 2026-08-05; this one is noted here because the
  mining queue is a separate file. *(2026-08-05)*

## Combat Assist Plus — findings from the M2/catalog session *(2026-08-05)*

Raised by three parallel tracks building `cap`. **None is asserted anywhere**; each names
what would settle it. The addon code they came from is unflown (cap has no release yet).

**`cooldown-manager.md` — four, from the CDM-binding work:**

- **`:740` is the one untagged row in a §7 Tier 2 table where every neighbour is
  `[client]`-measured.** `item.cooldownID | both | can read secret` carries neither a
  `[client]` tag nor `@verify-ingame`, so an unmarked source-read sits visually identical
  to a measurement — and it is the claim cap's whole merge-don't-replace binding design
  honours. Either measure it or mark it. (cap built the conservative branch, which is
  correct either way, so this is not blocking.)
- ~~**`:66-73` quotes `HiddenSpell` / `HiddenAura` as `Enum.CooldownViewerCategory` members
  without saying they are not in the enum.**~~ **ROUTED 2026-08-07** → `cooldown-manager.md`
  **§1.2** (new), which states the `-1` / `-2` Lua-side assignment at
  `CooldownViewerSettingsConstants.lua:4-5` against the generated `NumValues = 4` enum, and
  both consequences (nil until `Blizzard_CooldownViewer` loads; negative, so anything
  assuming `0..3` is surprised).
- **Rule 15's spellID union is narrower than Blizzard's own matcher, and the file does not
  reconcile them.** Rule 15 (`:963-966`) = base ∪ override ∪ overrideTooltip ∪ live; but
  §2.4 (`:186-195`) shows `SpellIDMatchesAnyAssociatedSpellIDs` *also* tests every
  `linkedSpellIDs` pool candidate. For "is ability X on this row?" they give different
  answers — the pool also matches aura ids (Wither `445474` hits Immolate's *cast* row).
  Genuinely ambiguous which is intended; cap split it behind an opt-in flag rather than pick.
- **PARTLY CLOSED — the file documents what you can read off a row you already hold, and
  barely documents how to OBTAIN the rows.** §7 now carries the `GetItemFrames()` account
  (it is `GetLayoutChildren()`, and every item template sets
  `includeAsLayoutChildWhenHidden`, so a hidden viewer still enumerates — measured
  `[client 2026-08-06]`). Still uncovered: the four viewer globals as such,
  `GetCooldownIDs()`, and the `minimumItemCount = 2` padding frames that make a naive
  frame count over-report. Sourced from `CooldownViewer.lua` + `CooldownViewer.xml:283-333`.

**`frames-textures-animation.md` — two, from the movable-frame work:**

- **The movable-frame family is still mostly absent.** §3.6 now exists and covers
  `SetClampedToScreen` only — that the clamp is continuous and inline, measured
  `[client 2026-08-06]`. `SetMovable`, `StartMoving`, `StopMovingOrSizing`,
  `RegisterForDrag`, `SetUserPlaced` and `dontSavePosition` still appear nowhere in §3 or
  §4, and the persistence half is unwritten; cap had to reconstruct that contract from
  Blizzard's Edit Mode source instead. Suggested shape: grow §3.6 into
  *"Moving a frame, and persisting where it went"*, anchored on
  `EditModeManager.lua:295-320` + `EditModeSystemTemplates.lua:355-380`, and overlapping
  `state-persistence-and-communication.md` on the persistence half. **Batch it with the
  EditBox section `observations.md` OBS-002 and OBS-003 already owe the same file** — one
  structural edit and one anchor re-stamp instead of two of each.
- **§8.1 (`:1252-1266`) omits that `UIParent` is itself `protected="true"`.** Tier 1:
  `Blizzard_UIParent/Mainline/UIParent.xml:4` —
  `<Frame name="UIParent" setAllPoints="true" protected="true" preventSecretValues="true" frameStrata="MEDIUM">`.
  Load-bearing for "is my addon frame protected?", because §1.2 says protection propagates
  to parents and anchor targets — and every addon frame is a child of, and anchored to, a
  protected frame. §1.1 now settles the consequence by measurement (a UIParent child reads
  `false, false` while UIParent reads `true, true`; the spread runs outward from the
  protected frame) `[client 2026-08-06]`, but §8.1 still does not carry the XML line
  itself, which is the Tier-1 premise. The same line is also the Tier-1 source for UIParent's `MEDIUM`
  strata and a live `preventSecretValues="true"` example — both flagged `[gap]` at
  `security-taint-and-restricted-data.md:1077` and `:1900`. ✅ **Verified verbatim against
  the local UISRC checkout** (`raw/addon-research/wow-ui-source/Interface/AddOns/Blizzard_UIParent/Mainline/UIParent.xml:4`)
  — the attribute list is exactly as quoted, so this is Tier 1 and ready to write, not a
  lead. One detail the report missed and the file should carry: the frame sits inside
  `<ScopedModifier addToSecureEnv="true">` (`:3`), which is also a live example for the
  open `scoped-modifier-for-addons` lab question.

**Demonology data — two, from the catalog work:**

- **Transform spell-ID conflict, one pair is wrong.** Ruination reads `433885` via DB2
  (`wowkb.spec_inventory`) vs `434635` in `projects/cooldown-hud/specs/demonology/notes.md`;
  Infernal Bolt reads `433891` (DB2, and `abilities.md`) vs `434506`. Resolve via game data
  per the workspace's conflict rule, then correct whichever doc is wrong. cap's catalog
  binds by observing the override so it is not blocked.
- **Unverified inference now load-bearing in cap's catalog:** that the Dreadstalkers
  **buff-bar** row carries a live bound aura (readable via `auraDataUnit`) for the pair's
  ~12s duration. Inferred from the row existing plus general in-combat readability of
  bound-aura presence — **not measured on Demonology**. It is the whole basis of Tyrant's
  HIGH band; if it does not hold, that entry collapses to one band and loses its point.
  Marked medium-confidence in `projects/combat-assist/specs/demonology/catalog.md`.

**`wowkb.spec_inventory` — a fixed bug worth knowing about (2026-08-06):**

- `_class_skill_lines()` picked each class's kit line by "most rows carrying my class
  bit". **SkillLine 810 is a shared line carrying rows for all 12 class masks**, so it
  won for **Hunter, Priest and Druid** — beating Priest's own 804 (13 rows vs 5) and
  edging Druid's 798 by one. The inverted `line_to_class` map then resolved 810 to a
  single class, and the other two got **no `class-baseline` abilities at all**. Ten
  specs were affected; the union went 2980 → 3217 rows once exclusivity (a kit line's
  class-restricted rows name *only* that class) replaced popularity as the test.
- **Consequence for BucketBinds:** the floats work reads this inventory, so Hunter /
  Priest / Druid specs were being planned against an inventory missing their baseline
  kit. `--unseeded` grew accordingly — those specs' seed coverage is worth re-checking
  before the next placement pass.
- **Consequence for the KB:** absence from this union was being read as "the ability is
  gone", which is what made Flare, Circle of Healing and Renewal look removed.

- **`wowkb.talents` does not emit `reviewed:`, but every generated `talents.md` has one
  (2026-08-06).** `talents.py` writes `title, patch, build, fetched, sources, confidence`
  and never `reviewed:` — yet all 40 committed `talents.md` carry `reviewed: 2026-07-07`,
  hand-stamped by a later sweep. **This is a latent `--check` trap**: the moment anything
  byte-compares a regenerated `talents.md` against the committed one it fails permanently,
  and no amount of regenerating fixes it. Three ways out — the generator emits `reviewed:`
  itself, `--check` compares semantically, or the patch sweep skips generated files. Pick
  one before adding a `--check` to any new generator. (`wowkb.gen_abilities` is being
  written to emit `reviewed:` itself.)

## Ability inventory — the seven tool gaps *(2026-08-06)*

Routed out of `knowledge/classes/_abilities/reconcile-ledger.md` §5, which adjudicated
1,578 prose claims against the generated Tier-1 inventory and named seven places the
mining genuinely cannot reach. Each is **measured**, not suspected. Nothing here is
scheduled — this is the parking lot, and these are recorded so the next person who hits
one knows it is known.

⚠ **The ledger's own instruction "file TOOL-GAP rows to kb-inbox" is superseded.** Every
name a TOOL-GAP verdict covers now lives in `knowledge/classes/_abilities/section-4-catalogue.md`
with its provenance, which is a better home: it is generated, so it cannot rot, and it
carries the explicit *catalogue, not backlog* rule. **Do not also copy those names here** —
Lunar Eclipse, Half Moon, Full Moon, Auto Shot, Heroic Strike, Crushing Blow, Restless
Blades, Hammer of Light, Templar Slash, Void Volley, Mind Flay: Insanity and the rest are
already recorded. What belongs here is the **tool** gap, not the ability.

- **G1 — passive `SpecializationSpells` rows are dropped.** 458 of 632 real-spec rows are
  passive and only 27 reach `all-abilities.tsv`. Most of the loss is junk (`Plate
  Specialization`), but it swallows real spec identity: **Mastery: Echo of Light** 77485
  (Holy), **Restless Blades** 79096 (Outlaw), **Mastery: Combo Strikes** 115636
  (Windwalker), **Demonic Wards** 203513 / 278386 / 1277736 (Vengeance / Havoc / Devourer).
  4 TOOL-GAP verdicts. ⚠ Admitting them means the inventory stops being "things you can
  press" — decide what `castable=false` rows are *for* before widening, because
  BucketBinds reads this file. (Leg B already closed Restless Blades into section 3 off a
  live `/data/wow/spell/79096`, so the symptom is partly masked; the gap is not.)
- **G2 — runtime override / proc-replacement buttons have no acquisition row.** ⚠ Read that
  literally: they are in `SpellName` (Wowhead/WoWDB find them) and several are reachable
  through `SpellEffect`. What is missing is a row saying a **spec learns** them. Hammer of
  Light is the worked case — eight `SpellName` entries, reached from Light's Guidance 427445,
  and **Protection already carries it** (`cdm-only` 1246643, `CooldownSetSpell` set 637 =
  spec 66); only **Retribution** lacks an acquisition row, on a hero tree they share. **First
  move on any of these: check a sibling spec of the same class.** 13 TOOL-GAP
  verdicts. **Partly refuted 2026-08-06**: `gen_abilities`' override walk (leg A) reaches
  five of them from `SpellEffect` alone — Templar Strike 407480, Cull 1245453, Voidblade
  1245412, Condemn 317485, Kill Shot 53351. The rest (Annihilation, Death Sweep, Reaver's
  Glaive, Abyssal Gaze, Consuming Fire, Devour, Pierce the Veil, Half/Full Moon, Templar
  Slash, Hammer of Light, Void Shield, Void Volley, Mind Flay: Insanity, Heroic Strike,
  Crushing Blow, Lunar Eclipse) still need an in-game spellbook enumeration (ClientLab),
  not another DB2 join.
- **G3 — `SkillLine 183 "GENERIC (DND)"` is outside both allowlists**, so **Auto Shot 75 is
  invisible for every Hunter spec**. 2 TOOL-GAP verdicts. Widen carefully and measure
  first: the two closed allowlists exist to keep the dead Shadowlands covenant lines out
  (2730-2733 carry 13 class masks each), and that guard must survive. Check what else line
  183 carries before admitting it.
- **G4 — `castable` is computed on the trait entry's *visible* spell, which is often the
  passive aura.** 45 rows across 23 specs read `castable=false` / `talent-passive` for
  abilities that are unmistakably pressed — Drain Soul, Comet Storm, Shadow Mend, Flourish,
  Summon Gargoyle, Raise Abomination, Tempest, Void Blast, Mindbender. Windwalker's
  **Zenith Stomp** is recorded as 1272694 (passive) when 1272696 / 1291484 are castable.
  ⚠ **These are not KB errors** — the prose rows are right and the column is wrong. Only
  four names have no castable spell anywhere (Ascendant Eclipses, Draconic Attunements,
  Void Apparitions, Embers of Nihilam) and only those are ORIGIN-SHIFT.
- **G5 — pet abilities have no spec granularity** (already documented, re-confirmed). Not
  in `SkillLine`, `SkillLineAbility`, `SkillRaceClassInfo` or `CreatureFamily`. Spell Lock
  19647, Axe Toss 89766, Freeze 33395, Primal Rage 264667 are all real and all class-level.
  5 ORIGIN-SHIFT verdicts ride on it. `pet-family-annex.tsv` carries the first three;
  section 4 now names the annex line for any prose row that resolves there, so a prose file
  should cite the **annex**, not a per-spec tsv. (This is the fix for the false
  `pet-family-annex.tsv # … (Primal Rage)` pointer that was in Beast Mastery's front
  matter — the annex has no Primal Rage row and never did.)
- **G6 — charge recharge times are unreachable at the pin, and this one is a one-command
  fix.** `SpellCooldowns` returns the **GCD** for charge abilities (Fire Blast 0.5s,
  Celestial Alignment 1s, Purifying Brew 1s, Prayer of Mending 1.5s). The real value is
  `SpellCategory.ChargeRecoveryTime` via `SpellCategories`, and both CSVs in `raw/wago/`
  are unversioned, so reading them would break the 67808 pin. **15 markers stay open on
  this alone.** `uv run python -m wowkb.wago SpellCategory --build 12.0.7.67808` (and
  `SpellCategories`) closes it — deliberately not done in this pass because it changes the
  `cooldown` column, which is BucketBinds' banding input.
- **G7 — `mage/frost` "Icy Veins (Thermal Void)" cannot be re-anchored. UNBLOCKED
  2026-08-06.** The stated blocker was that `SpellEffect.csv` was unversioned and could not
  be pinned; `raw/wago/SpellEffect-12.0.7.67808.csv` now exists (fetched for leg A). Thermal
  Void 1247729 is live on tree 658; what it now extends is answerable from that table and
  was simply never asked. Still do not guess — read the effect rows.

**Also routed here, from the adversarial verification of the prose pass:**

- **Holy Armaments is NOT a Tier-1 vs Tier-1 conflict** — recorded so nobody re-opens it.
  At 67808 tree 790 subtree 49 carries both node 95234 (TraitDefinition 122894 → spell
  432459, named *Holy Bulwark*) and node 110257 (TraitDefinition 141558 → *Holy Armaments*
  1289728, whose `VisibleSpellID` **is** 432459). That is exactly what the tsv's `aliases`
  column encodes. One entry, two names, no collision.
- **The ledger's §4 row for fury `Champion's Spear` / fury `Enraged Regeneration` / prot
  `Champion's Spear` is wrong.** It files them under "markers the tsv settles", but those
  markers asked about Rage-on-cast and heal-%/DR-% — questions ledger §6 itself says the
  tsv cannot answer. Dropping them removed three genuine open unknowns. They are re-opened
  as markers in the prose files.

## Ability inventory — a `none` description marks a stub row *(2026-08-06)*

Fell out of adding `description` + `description_source` to the generated inventory
(`wowkb.gen_abilities`, DB2 `Spell.Description_lang` spine + a cached Blizzard-API
rendering). **Recorded as an observation, not a task** — nothing here is scheduled, and
the fix is explicitly *not* ours to make: dropping a row changes the union BucketBinds
reads as a spec's real kit.

**The finding.** 26 of the 7,065 inventory rows (12 distinct spellIDs) get
`description_source: none` — no text in DB2 and no text from the API. That is **not** all
junk. Six of them are **stub twins**: the name is a real ability, but *that* spellID is a
hollow shell sitting in specs that do not have the ability, while the real button is a
different spellID with a real cooldown and full API text.

| name | hollow spellID | carried by | the real button |
|---|---|---|---|
| Force of Nature | `37846` cd 0, `SkillLineAbility:798` | Feral, Guardian, Restoration | `205636` cd 60, **Balance** `talent-active` |
| Incarnation: Tree of Life | `81098` cd 0, `NameSubtext_lang` "Passive" | Balance, Feral, Guardian | `33891` cd 180, **Restoration** `talent-choice` |

The other 20 rows / 10 names have no twin and are fairly called junk: four spec identity
auras (`Frost Death Knight` 137006, `Unholy Death Knight` 137007, `Protection Paladin`
137028, `Enhancement Shaman` 137041 — all `cdm-only`, all passive-flagged), one internal
driver (`Pyroblast Clearcasting Driver` 44448), UI plumbing (`Hotbar Slot 01/02` 294184 /
294189) and internal class-line entries (`Energy Usage` 119650,
`Zen Pilgrimage/Death Gate/Moonglade Storage Aura I` 126893, `Shapeshift Form` 228545).

**Measured caveats, so nobody over-reads this:**

- `AuraDescription_lang` — the other DB2 text column, which the generator does not read —
  is **also empty** for all 12 spellIDs. No third source rescues them.
- **The signal under-detects.** 101 inventory names carry more than one spellID; **11**
  have the stub *shape* (a cd-0 `class-baseline` member beside a cd>0 member) and only
  **2 of the 11** are `none`. The other nine — Ardent Defender, Bestial Wrath, Bladestorm,
  Chi Burst, Fists of Fury, Ravager, Track Beasts, Track Humanoids, Tranquility — carry
  full API text on both spellIDs, and several of those pairs are a legitimate
  button/aura or player/pet split rather than a stub. A `none` is a free lead; it is not a
  survey of stub rows, and "11" is a count of a *shape*, not of confirmed stubs.
- All figures are at build **12.0.7.67808**.

`wowkb.gen_abilities` prints the split on every run and
`knowledge/classes/_abilities/README.md` § *When a row has no description* carries the
same table. Nothing ages either one.

## Ability inventory — the prose rollout is BLOCKED, plan written *(2026-08-06)*

The mining is done and committed (`b66df73`..`7b03190`): 88 generated files, 7,065
rows, every DB2 read pinned to 12.0.7.67808, plus descriptions transcribed from game
data (99.6% coverage). What is **not** done is stripping the now-redundant restatement
out of the 40 hand-written `abilities.md` files.

📄 **The full plan, with enough context to resume cold, is `todo/ability-inventory-rollout.md`.**
Read it before touching `knowledge/classes/*/*/abilities.md` or
`tools/wowkb/gen_abilities.py`. Summary of why it is parked:

- **Blocker 1 — `cost` and `cast_time` have no generated home.** The API tooltips say
  what a spell *generates*, never what it *costs*. The `Resource` and `Cast / CD`
  columns of the 40 prose files are the only record of Holy Power / Rage / mana costs
  and of every cast time. A "delete the restated columns" pass destroys both. Sources
  are already on disk (`SpellPower`, `SpellMisc.CastingTimeIndex` → `SpellCastTimes`),
  both need a pinned refetch.
- **Blocker 2 — `abilities.md` is a MACHINE INPUT and 18 of 40 specs are dark to it.**
  `gen_abilities._inventory_names()` harvests the first table column under a heading
  starting with `inventory`; `## Ability inventory` does **not** match. So the
  `prose-only` leg of `section-4-catalogue` has never seen 18 specs — **10 rows are
  missing**, including Cull, Devour, Pierce the Veil, Sacred Weapon and Spell Lock,
  several of which were described as "recorded in the catalogue" when they were not.
  Any rollout must keep a table with clean names in column 1 under a matching heading,
  or it silently deletes tracked unknowns.
- **Decision pending from Mike** — a 3-spec pilot (retribution / warrior-protection /
  priest-holy) is **uncommitted in the working tree** proposing a four-section shape
  with a two-column `Ability | Role` table. `git diff` to see it, `git checkout --` to
  discard. Honest headline: the files got **longer**, not shorter.
- **A free win that needs no decision:** a 16-line boilerplate blockquote is duplicated
  verbatim across all 40 files and the hero-tree sections duplicate `builds.md`.
  Deleting both shrinks 40 files by ~25 lines each with zero loss.

Two quality caveats recorded there, not fixed: some tooltips render the **wrong spec's
branch** (Protection Warrior's `Burst of Power` says "Bloodthirst", which is Fury's —
Blizzard's API resolves `$?spec[…]` without spec context; ~445 loose candidates,
2 confirmed), and `priest/holy/rotation.md` is **stale** in a way that contradicts its
own `abilities.md` — so "check the sibling covers it" is not a sufficient test.

## Warlock / Demonology — Dominion of Argus reads 25 s in game, 15 s in the KB *(2026-08-07)*

**A hotfix has not been ingested.** The live in-game tooltip, read 2026-08-07, says
*"Summoning your Demonic Tyrant leaves open a portal to Argus for **25 sec**…"*. The KB and
the DB2 extract both say **15 sec**:

- `knowledge/classes/warlock/demonology/ability-inventory.tsv` (row 84) and
  `ability-inventory.md` §83 — generated from the Blizzard API description at build
  12.0.7.67808, "for 15 sec".
- `maxroll-raid.md:49,51` and `maxroll-mplus.md:49,51` — `verbatim: true` captures, "For 15
  seconds after casting Summon Demonic Tyrant…". Third-party, so they follow whatever they
  were written against; not independent corroboration.
- `diabolist-sequences.md:250` — "possible for 15 s".

**The running game outranks DB2 and the KB** (workspace `CLAUDE.md`, staleness doctrine
§4: resolve a conflict against what the game is actually running). So the 25 s is the fact
and the 15 s is stale, which means the numbers below it — how many Hand of Gul'dans fit in
the window, and therefore the shard maths in `rotation.md` and `diabolist-sequences.md` —
are all sized against the wrong window and want re-checking.

**What to do:** re-pull `Spell`/`SpellDuration` at the current build (the extract on disk is
12.0.7.67808, and live is 12.0.7 — check whether a newer build has landed), confirm the
25 s, then correct the four game-KB files above. ⚠ Do **not** just edit the prose: the
`ability-inventory.*` pair is **generated** by `wowkb.gen_abilities`, so fixing it by hand
puts it back the next time the generator runs.

*Raised by the Combat Assist Plus spec review — `projects/combat-assist/specs/notes.md`
2026-08-07, where 25 s is recorded and a reviewer's "it is 15 s" was rejected on this
basis.*

## addon-dev — §4.2 and §4.8.1 finding 7 disagree about `type(secret)` *(2026-08-08)*

**A reconciliation, not a new question.** `security-taint-and-restricted-data.md`
contradicts itself on what `type()` does to a Secret Value, and both statements predate the
session that filed this. Filed here as **structural work on the subtree** — an
internal-consistency defect in one file, which is an editing job — rather than as an
addon-dev claim, which would belong in that subtree's own queues.

- **§4.2, the operation table** — row `type(secret)`: *allowed, **returns the real type***,
  result a plain string. The whole table is tagged `[client 2026-08-05]` ("every row below
  has now been executed in the client against a genuine Secret Value"), and the registry
  row `secret-op-type` drained it as **OBS-033**.
- **§4.3, Trap 1** — *"`type()` is not a guard"*, and the worked example is built **on**
  §4.2's answer: `type(v) == "number"` **passes**, and the comparison on the next line is
  what errors.
- **§4.8.1, finding 7** — *"⚠⚠ AND `type(x) == "number"` IS THE WRONG GUARD. **A secret
  number fails it**, so a bare `type()` check silently rejects exactly the in-combat case
  you need."* That is the opposite reading: the guard is wrong because it is **false**, not
  because it is true. Untagged prose, no `[client]` stamp.

Both sections reach the same *advice* — ask `issecretvalue` first — by opposite mechanisms,
which is exactly why neither reader notices the clash.

**Nothing depends on the answer today.** Every guard in `projects/combat-assist`
(`Channel.lua`'s `field()`, `Overlay.lua`'s `num()`) class-checks with `issecretvalue`
before it ever asks `type()`, so both codebases are correct under either reading. That is
what makes this a filing rather than a fix.

**What to do:** decide which is right and rewrite the loser **in place** (README §7.1's
current-state rule — no correction note left standing over the old text). ⚠ The evidence is
not symmetric and the resolution should say so: §4.2's row is measured and drained, finding
7's sentence is not. Do **not** settle it by re-running the test — `secret-op-type` is
`answered` and `wowkb.lab drain` refuses an answered question; if the measurement needs
re-reading, read **OBS-033**.

---

## `frames-textures-animation.md` §7.1 — the FlipBook Lua setters are missing from the setter table

Filed 2026-08-10 by the cap measured-restyle round, which needed them and found the KB
saying only that the XML attribute names are not the Lua setter names.

§7.1's *"animation | Lua setters `[T1 docs]`"* table carries **Scale**, **Alpha** and
**Rotation** and stops there — so a reader who needs `FlipBook` gets the warning without the
answer. The generated docs have it: `SimpleAnimFlipBookAPIDocumentation.lua` declares
`SetFlipBookRows` / `SetFlipBookColumns` / `SetFlipBookFrames` / `SetFlipBookFrameWidth` /
`SetFlipBookFrameHeight` plus the five matching getters, every setter
`SecretArguments = "AllowedWhenUntainted"` and every argument `Nilable = false`. The stem is
the XSD attribute name with `Set` in front — the **opposite** of the `Scale` trap the same
section warns about, which is worth stating because it is what makes guessing feel safe.

Worth pairing with the usage: `Blizzard_ActionBar/Shared/ActionButtonSpellAlerts.xml:25`
declares `flipBookFrameWidth="0" flipBookFrameHeight="0"` — the XSD defaults — so a caller
setting only rows/columns/frames matches Blizzard's own declaration for that sheet.

**A documentation read, not a measurement.** It takes `[T1 docs: …]`, not `[client]`.

---

## `rewards.py` has no `veteran_crest` / `adventurer_crest` consumer — S2 crest yields value at 0

Filed 2026-08-11 by the 12.1 sweep of `planning/activities/ritual-sites.md`.

12.1 re-pointed the Season-1 world activities at **Season 2 crests**, and several of them
now pay the *low* tiers: Ritual Sites T1–6 pay Delve-equivalent crests (Veteran at T6, per
`endgame/delves/overview.md`), Void Assaults and Val/Naigtal pay **S2 Adventurer** crests.
`tools/wowkb/rewards.py`'s `CURRENCY_CONSUMERS` only defines `champion_crest`,
`hero_crest`, `myth_crest`, `field_accolade` and the two spark keys — **`veteran_crest` is
in `CANONICAL_CURRENCY_NAME` but has no consumer test, and `adventurer_crest` does not
exist at all**. So every activity whose 12.1 yield is a low-tier crest contributes **0** to
`plan.py:currency_R()` and gets under-ranked for exactly the character the crest is for: a
fresh/early-S2 character still upgrading Veteran- and Adventurer-track slots.

**What to do:** add both keys with `_crest_consumer("Veteran")` / `_crest_consumer("Adventurer")`
and an `adventurer_crest` entry in `CANONICAL_CURRENCY_NAME`, then re-check the crest names
themselves — S2 crests are **Mistcrests**, and `CANONICAL_CURRENCY_NAME` still says
"Dawncrest" for all four tiers. Also worth a pass over the `_facets.md` canonical-key list,
which likewise has no `adventurer_crest`.

---

## `rewards.py` still carries Season-1 ilvl constants — `FIELD_ACCOLADE_ILVL` and `CREST_CEILING`

Filed 2026-08-11 by the 12.1 sweep of `planning/activities/val-naigtal.md`.

Two hard-coded S1 numbers in `tools/wowkb/rewards.py` are now wrong by a full season:

- **`FIELD_ACCOLADE_ILVL = 259`** encodes the **removed** 12.0.7 Maren Silverwing
  Hero-track box. 12.1 deleted the Season 1 gear caches outright; the Field-Accolade
  shelf is now a **200** Warbound S2 Adventurer cache and **500 / 750** BoP S2 Veteran
  caches (random / slot-specific). So `_consume_field_accolade` values Accolades against
  a 259 sidegrade when the real slot-targeted buy lands at **~279 (Veteran 1/6)** — and
  it prices no distinction between the 200 and 750 tiers.
- **`CREST_CEILING = {"Champion": 263, "Hero": 276, "Myth": 285}`** is the S1 Dawncrest
  ladder. The S2 Mistcrest bands (Tier-1 `CurrencyTypes` DB2 @ 12.1.0.69214) are
  Adventurer 269–282 · Veteran 282–295 · Champion 295–308 · Hero 308–321 · Myth 321–334.
  Every crest-headroom calculation is therefore capped ~45 ilvl too low, which will read
  as "no consumer / geared past this track" for a character who is in fact mid-track.

**What to do:** re-fit both constants to the S2 ladder alongside the `adventurer_crest` /
`veteran_crest` consumer work above (same file, same sweep), and consider sourcing the
ceilings from the KB rather than a literal so the next season is a data edit.

---

## `goalboard.py` (the `--board`) is Season-1-hard-coded — Dawncrests, the 263 gate, 272/285 crafts

Filed 2026-08-11 by the 12.1 sweep of `planning/goal-model.md`.

The deterministic goal **board** behind `wowkb.plan --board` / `/plan-character` reads
S1 values throughout `tools/wowkb/goalboard.py`:

- **Currencies:** `MAT_KEYS` names `"Adventurer/Veteran/Champion/Hero/Myth Dawncrest"`,
  and `_crest_up()` builds `f"{tname} Dawncrest"`. In S2 those balances are **Mistcrests**
  — every crest lookup will read **0**, so *every* crest-up candidate reports unaffordable.
- **`CHAMPION_LADDER = [246, 250, 253, 256, 259, 263]`** — the S1 Champion track. S2's
  Champion band is **292 (1/6) → 308 (6/6)**.
- **`DAWN_CHAMPION_ILVL = 263`** drives both the discount gate state and the
  `sub_263_slots` cross-char fact. The S2 lever is **Champion of the Mist** at a **308**
  high watermark in every slot; the Dawn discount is per-crest-currency and **does not
  carry over**.
- **`CRAFT_*` yields 272 (Hero) / 285 (Myth)** — S1 spark-craft brackets. The S2
  brackets are **not published yet**; don't guess, gate this on `systems/professions.md`.

**Impact:** `--board` output is untrustworthy in S2 until re-pointed — it will look
plausible while claiming a fully-geared character has 15 sub-263 slots and can afford
nothing. The *rubric* in `planning/goal-model.md` needs no change; only the constants do.

**What to do:** re-fit alongside the `rewards.py` constants above (same season shift,
same fix shape) — and prefer sourcing the ladders/ceilings from `endgame/dawncrests.md`
over literals so the next season is a data edit, not a code edit.

---

## `CLAUDE.md` + `character.py` + `goalboard.py` still hardcode the **Season 1** Catalyst currency

Filed 2026-08-11 by the 12.1 sweep of `endgame/catalyst.md`.

Season 2's Catalyst charge currency is **Venomblight Manaflux**, currency **3465**
(`CurrencyTypes` DB2 @ 12.1.0.69214, `MaxQty` 8, +1 per 1209600000 ms = 14 days).
Season 1's **Dawnlight Manaflux (3378)** is now the *old* currency, and it is still
asserted as the current one in three places:

- **`CLAUDE.md`**, `wowkb.character` paragraph: *"Catalyst charges = Dawnlight Manaflux
  (currency 3378 — a normal currency)"*.
- **`tools/wowkb/character.py:608`** — emits that same sentence into every character
  snapshot's digest.
- **`tools/wowkb/goalboard.py:45`** — `CATALYST_CURRENCY = "Dawnlight Manaflux"`
  (and the docstring at `:187` repeats "currency 3378, cap 8").

**Impact:** a Syndicator balance lookup keyed on the S1 name/id will read **0** for every
character in S2, so charge-aware board/digest output silently claims nobody can catalyze.
Same failure shape as the `rewards.py` / `goalboard.py` crest-ladder entries above — fix
in the same pass, and prefer sourcing the currency id from `endgame/catalyst.md` over a
literal so the next season is a data edit.

⚠ Open question the KB cannot answer yet: whether **leftover S1 Dawnlight Manaflux**
carries, converts, or is lost at the S2 rollover — the 12.1 notes are silent
(`@verify-ingame` marker lives on the claim in `endgame/catalyst.md`).

---

## `factions/` is missing a file for **Captain Tokka's Crew** (new in 12.1)

Filed 2026-08-11 by the 12.1 sweep of `factions/amani-tribe.md`.

The `changelog-12.1.md` `factions/` impact map lists exactly one **NEW** row —
`factions/zuljarras-forces.md` — but 12.1 shipped **two** new Midnight reputation
tracks. The second is **Captain Tokka's Crew**, the tortollan sea captain's
fishing/friendship track on the Coiled Isle, documented Tier-1 at
`raw/pages/worldofwarcraft-com-en-us-news-24293963.md` (l.398, l.410):

- **5 ranks:** Stranger · Doomed Sailor · Cursed Angler · **Venom Trawler** ·
  **Bloodsworn Crew** (vs the 20-rank shape of a normal renown faction).
- Quartermaster **Second Mate Sluggs** at **Tokka's Folly**; Tokka himself at
  **Tokka's Landing** teaches Cursed Fishing and tracks progress.
- Currencies: Coins, **Voidlight Marl**, **Coiled Filament**, **Artisan Moxie**.
- Rewards gated on rank: Sea-Dwelling Isle Serpent flying mount (2,500 Coiled
  Filament + *Bloodsworn Crew or above*), the Envenomed weapon line (500–1,000
  Coiled Filament + Bloodsworn Crew), Recipe: Tokka's Multi-Ward (1,500 Voidlight
  Marl + Venom Trawler), Venom Elemental pet (Venom Trawler), profession recipes
  at Cursed Angler, Eerie Lure (10 Voidlight Marl, ungated).
- Also new: **Midnight Anglin' Score** (up to 100 pts/fish; 2,500 → *The Briny
  Best* + the "Briny" title) and an **Epic Fishing Rod** with interchangeable boons.

**Two knock-on fixes owed:** `factions/zuljarras-forces.md` l.18 calls itself
*"The **sixth** Midnight renown faction"* against a five-faction list, which double-counts
badly once Tokka's Crew exists; and the sweep's own faction counts need to stop asserting
a bare number. `factions/amani-tribe.md` has been rewritten to enumerate rather than count.

---

## ~~DECIDE: flip `planning/activities/omnium-folio.md` to `scope:account`?~~ — DONE 2026-08-11

Filed and **settled** 2026-08-11 by the 12.1 sweep of
`planning/activities/omnium-folio.md`. **Flipped to `scope: account`** in the file's
front matter (never in `candidates.json`).

Why it was safe to settle inside the sweep rather than defer: the facet's only
justification was the per-character Sunstrider Omnium unlock questline, and **12.1 made
that intro account-skippable** once any one character finishes it (`patch-notes/12.1.md`
l.1539; `changelog-12.1.md` l.390). Row unlocks were already account-wide, and the
2026-06-25 hotfix already made the weekly's *prerequisites* account-wide from Week 2. So
`account` is the factually correct value, not a tuning preference.

**Measured while settling it — `scope` is a documented facet the tooling does not read.**
`_facets.md` → *Cross-character scoring (v2)* describes `scope:character` as scoring a row
per active character, but `grep scope tools/wowkb/gen_candidates.py tools/wowkb/plan.py`
returns **nothing**: `gen_candidates` emits only `id / name / why / reward_base / urgency /
time_blocks / enjoyment_key / gate`, and `candidates.json` has no `scope` key on any row.
So the v2 cross-character rule is **specified but unimplemented** — the flip cannot have
changed ranker output, and the earlier worry that a regen would "bake in" the wrong scope
was unfounded. **Follow-up worth filing separately:** either implement v2 in `plan.py` or
mark that section of `_facets.md` as aspirational, because a contract doc that describes
scoring nobody performs will mislead the next sweep the same way.

---

## VERIFY IN GAME: is the Omnium Folio "Seeking Knowledge" weekly still offered?

Filed 2026-08-11 by the 12.1 sweep of `planning/activities/omnium-folio.md`, which now
carries `status: invalidated` and an `@verify-ingame` marker over exactly this.

Tier-1 fixes the series at **five weeks**, one row per reset (the hotfix archive names
*"Seeking Knowledge Week 4 of 5: Magical Primessence"*, `patch-notes/12.0.7.md`). 12.0.7
went live **2026-06-16**, so Week 5 fell in the reset week of **2026-07-14**. Nothing at
any tier — Tier-1 notes, hotfix archive, wiki, or the SEO guides — states whether a Seeking
Knowledge quest is offered after that, or whether a character who never started restarts at
Week 1. (12.1's intro-skip change is *not* evidence either way: the skip is worth shipping
purely so alts can reach the folio interface, whose rune slotting is per-character.)

**Two questions to answer with one login:** (1) does a caught-up character get a Seeking
Knowledge quest this reset? (2) does a character that never did the intro get offered
*Week 1* or the *current* week? Re-activate the planner row on a sighting, not on an
assumption.

---

## Planner/tooling debts from the 12.1 retier of Field Accolades + world-boss loot

Filed 2026-08-11 by the 12.1 sweep of `planning/activities/showdown-weekly.md`.

Three items, all **scoring/tooling**, none a fact problem in the KB text:

1. **`rewards.py` has no canonical `adventurer_crest` key.** 12.1 pays S2 Adventurer
   crests from a wide set of sources (Val/Naigtal WQs/rares/elites, Void Strikes +
   Incursions + their weekly, the Showdown weekly on Normal WT). Every one of those
   activity rows currently under-declares its yield because there is no key to declare
   it into. Add the key (and a Veteran-crest counterpart for the Heroic-WT payouts).
   Blocked on: no Tier-1 source states crest *amounts* — confirm in game.
2. **`rewards.py::_consume_field_accolade` values Accolades against a deleted item.**
   It prices them against the Season 1 ~259 Hero-track slot cache, which 12.1 removed.
   Re-point the consumer at the S2 slot-specific cache: **750 Accolades → Veteran 1/6
   (279)**, with the 200-Accolade S2 Adventurer Warbound cache as the cheap tier.
3. **Frozen world-boss loot is still credited at full value.**
   `world-boss.md` declares `{track: hero, ilvl: 263, chance: 1.0}` for the boss's drop
   (S1 Hero 1/6 = 263; `showdown-weekly.md` dropped its duplicate of this vector on
   2026-08-11, since a Season 1 ilvl under a `track:` label that now names a Season 2
   band is unreadable to the ranker). 263 is still *where the item lands*, but 12.1
   froze it at Season 1 with **no upgrade path**, so its planning value is far below an
   equivalent live-track slot —
   the ranker keeps recommending the row for gearing while the prose sends gearing to
   the lair (279 Veteran 1/6 + a Veteran Mistcrest). Needs a scoring-model answer for
   "non-upgradeable yield", not a per-file number tweak (`planning/scoring-model.md`).

Related open question, KB-side not tooling: `systems/void-incursions.md` records the
200-Accolade S2 Adventurer cache as **slot-specific**, which the Tier-1 12.1 notes do not
state (they give cost, track and binding only). The **ilvl half is settled** — 266 =
Adventurer 1/6, derived from `CurrencyTypes` DB2 @ `12.1.0.69214` in
`endgame/dawncrests.md`, closed 2026-08-11. Only the slot is open. Resolve at Maren
Silverwing in game; if the cache *is*
slot-targeted, the cheap deterministic slot buy is 200, not 750, and both files plus any
Accolade-budget advice change.

---

## From the 12.1 full sweep (2026-08-11) — structural, not per-file

1. **The 2026-08-18 Season-2 rollover is an unsignalled calendar event.** 12.1 shipped
   into a pre-season week, so ~40 claims across `endgame/` and `planning/activities/`
   are written as "opens Aug 18" and become present tense that reset, and **seven
   planner activities are parked `status: invalidated`** awaiting re-activation
   (`mplus`, `delve-bountiful`, `prey-weekly`, `pvp-conquest`, `voidcores`,
   `turbulent-timeways` (permanently — the event ended), `omnium-folio` (parked for an
   unrelated reason)). **No build or blue post will fire on that date** — the feeds
   cannot catch it. `_meta/next-patch.md` carries the full unlock schedule.
   ⚠ `delve-bountiful` and `prey-weekly` must have their `yields:` **re-sourced before**
   `status:` flips back, not after — they were nulled rather than carried forward with
   Season 1 numbers.

2. **102 class files across 34 specs were not re-verified for 12.1** and carry a dated
   "NOT RE-VERIFIED FOR 12.1" banner instead of a `reviewed:` stamp. This was a scope
   decision, not an oversight: 12.1's **+25% player health and creature damage** retune
   moved numbers in every one of them, so a mechanical restamp would have put a false
   guarantee on exactly the most misleading content. They stay `patch: 12.0.7` until
   someone does a real pass. The warlock + demon-hunter specs (6) *were* swept.

3. **`endgame/dawncrests.md` is now a Mistcrest-primary document under a Dawncrest
   filename.** Left as-is for link stability, but it is a naming decision that should be
   made deliberately rather than inherited — a rename touches every file that links it.

4. **`wowkb.uiapi` still indexes the 12.0.7 UI-source tree** while `knowledge/addon-dev/`
   now cites 12.1.0. `uiapi stats` therefore disagrees with the topic files by design.
   Needs repointing or a `--build` flag. (Also logged as a `[gap]` in
   `addon-dev/sources.md`.) A second worktree of Blizzard's shipped source now exists at
   `raw/addon-research/wow-ui-source-12.1.0`; the 12.0.7 checkout is **deliberately kept**
   because several hundred `file:line` citations still resolve against it.

5. **Two hardcoded constants silently defeat "regenerate on patch day":**
   `spec_inventory.PINNED_BUILD` and `gen_abilities.PATCH`. Both were bumped on
   2026-08-11 and a checklist item was added to `game-version.md`, but they should
   probably read the live build rather than be edited by hand each patch.

6. **`talents.md` and `ability-inventory.md` are pinned to different builds** —
   `12.1.0.68914` (the Game Data API's `static-12.1.0` namespace) and `12.1.0.69214`
   (the live client) respectively. Verified harmless this patch: the `Trait*` DB2
   exports at the two builds are byte-identical (md5 on `TraitNodeEntry`). Each
   `talents.md` now carries a provenance note saying so. If the API namespace ever lags
   across a *real* data change, this becomes a live defect.

7. **The five Midnight renown gear pieces look RESCALED to Season 2 ilvls, and the
   faction files say the opposite.** `factions/the-singularity.md` and
   `factions/harati.md` both assert the S1 numbers were "**not** rescaled by 12.1's
   +45 ilvl ladder shift" and read as legacy tracks; `factions/amani-tribe.md` says
   the 246 neck "now sits well below the S2 floor". Two Tier-3 guides (Method's S2
   gearing guide, corroborated by a second) say instead that the neck (Amani R9),
   helm (Silvermoon R9), belt (Hara'ti R8) and trinket (Singularity R7) "**have been
   upgraded to Season 2 item levels**", and that Zul'jarra's Forces R9 bracers are a
   *new* S2 Champion-track piece. If true, S2 Champion 1/6 = **292** (Tier-1, see
   `endgame/mythic-plus/loot.md`), not 246 — a 46-ilvl error in the other direction,
   and it turns four "collection only" rewards back into real alt-gearing catch-up.
   ⚠ Not written into `knowledge/` because: (a) the sources are Tier 3 and one of them
   calls the same set **Veteran**-track rather than Champion, (b) no source states the
   pieces' actual ilvl, (c) Season 2 does not open until **2026-08-18**, so nothing was
   observable when this was found (2026-08-17).

   **RESOLVED SAME DAY — and the guides were wrong in a second way.** Owner
   observation (in game 2026-08-16, plus video): the re-issued pieces are
   **VETERAN** track, not Champion. The Silvermoon Rank-9 helm was collected again
   on a character that already had the S1 version — **the runestone quest has to be
   redone** — and came back Veteran. That makes the rule: *every S1 renown track
   re-issues an S2 Veteran item in the slot it gave in S1* (S2 Veteran = **279**
   1/6, band **282 → 295**). It is corroborated by the KB's own
   `factions/zuljarras-forces.md`, which already had **Veteran** bracers at Rank 2
   and **Champion** at Rank 9 — Veteran is the renown baseline, Champion the
   deep-rank exception. All five faction files were corrected 2026-08-17.
   **Residual:** only the Silvermoon **helm** was directly observed; the Amani neck,
   Hara'ti belt and Singularity trinket are inferred from the pattern (~90%) and
   each carries its own `@verify-ingame`. The early-rank ilvl-180 pieces
   (Silvermoon helm, Singularity gloves, Hara'ti belt) were **not** re-checked and
   are still S1 numbers.
   **Standing lesson:** on renown reward tracks the Tier-3 guides were unanimous and
   unanimously wrong (Method et al. all say "Champion"). Prefer the tooltip.

---

## Havoc Demon Hunter — parked from the `rotation.md` → APL-supplement rewrite *(2026-08-17)*

`classes/demon-hunter/havoc/rotation.md` now supplements the generated `simc-apl.md`.
These are the questions it could not assert, plus the open items its old `## TODO`
carried.

1. **Is Fury actually a limiting resource for Havoc on 12.1?** The 12.0.7 parses said
   no (14.1 % pooled overcap, generation dominated by the ungateable Demon Blades —
   tables in `_meta/changelog-12.1.md`). But 12.1 moved generation **off** Immolation
   Aura (Burning Hatred 40→30) and **onto** Demon Blades (8–15→10–16), and at least one
   Havoc source reports Fury as limiting on 12.1. **Needs Season 2 parses (2026-08-18+).**
   Until then `rotation.md` asserts no Fury-management conclusion in either direction.
2. **Re-verify the hero-tree recommendation for Season 2** (`builds.md`). Fel-Scarred-first
   is a Season 1 claim, and Icy Veins' hero-filtered priority tool expresses no
   preference between the trees. Needs Tier-1/Tier-2 evidence post-2026-08-18, not
   day-one editorial.
3. **Sanity-check the opener against a top WCL Havoc log** (`wowkb.wcl`). The opener
   currently in circulation is method.gg's, written for an Inertia build at 12.0.7;
   `rotation.md` no longer transcribes it.
4. **Confirm the Exergy-over-Inertia call once Season 2 sims exist.** It is Tier-3
   consensus, unsimmed. `rotation.md` and `builds.md` both carry the caveat.
5. **Immolation Aura's high rung requires Burning Wound as well as A Fire Inside, and
   nobody says why.** `rotation.md` marks the "capping risks letting the debuff lapse"
   explanation as an inference. Worth confirming against a sim or a class source.

---

## `wowkb.character` still prints the Season 1 "…of the Dawn" ladder *(2026-08-20)*

Found while re-syncing Encomplete on the first post-Season-2 pull. The digest's
`## Upgrade tracks & "…of the Dawn" discount` section is hardcoded to the
**Season 1** ladder: it lists the S1 Dawn achievements and computes the discount
off a **263-in-every-slot** gate against achievement **42768**
(`tools/wowkb/character.py:477-510`; the same constant is duplicated in
`tools/wowkb/goalboard.py:56-57, 358-365` and referenced from `plan.py:326-329`).

For Season 2 that output is **actively misleading** — it printed
*"Champion 50% discount: LIVE — every slot ≥ 263"* for a character that has in
fact earned **no** "…of the Mist" rung and gets **no** discount. Dawncrests are
dead currency from S2 onward; the discount is per-crest-currency, so an S1
achievement carries nothing forward (`endgame/dawncrests.md` § *The "…of the
Mist" achievements*).

**Fix:** re-point the section at the S2 ladder — thresholds **282 / 295 / 308 /
321** per-slot high watermark and **331 average** for Myth, achievement IDs
**62410 / 62411 / 62412 / 62414 / 62416**, currency **Mistcrest**. Both the
per-slot gate list ("which slots are below the gate") and `goalboard`'s
cheapest-character-to-earn heuristic need the same numbers. Ideally the
thresholds move out of the code into `endgame/dawncrests.md`'s table so the next
season turnover is a KB edit, not a code edit.

⚠ Until it is fixed, **do not quote the tool's discount line** — read the
Mist ladder off `endgame/dawncrests.md` and the gear table by hand.

---

## 1174 rotting line-number locators in `knowledge/addon-dev/` *(2026-08-21)*

Filed by `wowkb.citecheck`, the citation-resolution gate added when
`projects/combat-assist/specs/pattern-shelf.md` was dissolved into the KB.

The gate's rule is that a Tier-1 citation should anchor on a **symbol** (and,
where it quotes, a verbatim fragment), never on a line number. The reason is
measured: `Blizzard_SharedXML/Dump.lua` is 486 lines in both 12.0.7.68887 and
12.1.0.69273 with `type(val)` at 98 / 149 / 309 in **both**, while
`CooldownViewer.lua` went 2168 → 2374 lines over the same interval. So a line
anchor is right in the files Blizzard did not touch and silently wrong in the
ones it reworked — and nothing about the citation itself distinguishes them. That
is exactly what the pattern-shelf audit found: every
`Blizzard_CustomAuraButton.lua` citation exact, every `cooldown-manager.md` one
wrong.

**The size of the job, as the tool currently measures it:**

- **11** symbol-anchored citations — all resolve, and these are gated (exit 1).
- **392** line-anchored citations inside a `[T1 src …]` / `[T1 docs …]` bracket.
- **1174** `File.lua:123` locators in the subtree once the ones written inline in
  prose (rather than inside a citation bracket) are counted too.

```bash
cd tools
uv run python -m wowkb.citecheck --lines    # every one of them, with its file:line
```

**Not scheduled.** Repairing them is mechanical but not cheap — each one has to
be re-resolved against the right clone and rewritten as a symbol, and a wrong
re-resolution is worse than the stale number. The right time is probably a
patch-day sweep of one file at a time, highest-churn file first
(`cooldown-manager.md`, then `security-taint-and-restricted-data.md`). New
citations should be written symbol-anchored from the start; the gate enforces
that they resolve.

## ClientLab — parked 2026-08-21, mid-session

Shelved deliberately: the useful next step is a **real cap flight on Demonology**, not another
lab pull. Nothing here is urgent and nothing is broken.

**Open question, narrowed and still `built`:** `aura-container-composite-layers` — tiles A and B
only. Do TWO escapes in one band draw as two marks (a full-tile hatch plus a corner badge), and
do an application BAR and an application COUNT both draw on one row? Both calls already recorded
`accepted` `[client 2026-08-21]`; only the pixels are unproven. The pull that would have answered
them was flown on **Destruction**, which has no Demonic Core, so both slots correctly matched
nothing. Re-fly on Demonology with Cores up — **or let a real cap row answer it**, which is the
better trade now that the composites are what we want to see.

**Settled and drained the same day** (in `security-taint-and-restricted-data.md` §3.5):
`AddPandemicRegion` takes a Frame with children · `StatusBarRenderMode.Radial` works on the
duration bar · a button takes both count sinks at once · `SetDurationText` honours a rule
formatter through `options.textFormatter`.

**Two follow-ups nobody is on, both small:**
- `options.textFormat`'s `{ property, formatter }` components are the only route to banding on
  `RemainingPercent` rather than remaining seconds. Source read; marked `@verify-ingame` on the
  claim.
- `render-shelf.md` Part 7 L7's cells are captioned in **percent** and a bare `textFormatter`
  bands on **seconds**. Right shape, wrong unit, and the entry says so — re-caption when the
  percent route runs.

**Lab harness changes made this session and NOT parked** (they are done, and they were the
reason the session stalled): `wowkb.lab deploy` now runs `luacheck` and refuses on failure — the
game had been the linter, reporting `attempt to perform arithmetic on global 'OPTION_AREA'` at
the worst possible moment. `Ask.lua` is 620px wide with real font sizes, and `Ask.Register`
now refuses a `note` over 300 chars or a `question` over 200: the panel is a stimulus, not a
briefing, and the long form belongs in `questions.json`'s `expect`, which is written for whoever
drains the run rather than whoever flies it.

