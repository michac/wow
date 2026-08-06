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
  - `C_ClassTalents.GetActiveHeroTalentSpec()` → the active **SubTreeID**, nilable
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
- **`:66-73` quotes `HiddenSpell` / `HiddenAura` as `Enum.CooldownViewerCategory` members
  without saying they are not in the enum.** The generated enum is `NumValues = 4`,
  0–3 (Essential/Utility/TrackedBuff/TrackedBar). `HiddenSpell = -1` / `HiddenAura = -2`
  are Lua-side assignments at `Blizzard_CooldownViewer/CooldownViewerSettingsConstants.lua:4-5`.
  Two unstated consequences: they are **nil until `Blizzard_CooldownViewer` loads**, and
  they are **negative**, so anything iterating the enum or assuming 0..3 is surprised.
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
