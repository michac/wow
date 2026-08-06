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
- **A hole, not an error: the file documents what you can read off a row you already hold,
  and nowhere documents how to OBTAIN the rows.** No coverage of the four viewer globals,
  `CooldownViewerMixin:GetItemFrames()` (it is `GetLayoutChildren()`, so shown-children-
  with-a-layoutIndex only), `GetCooldownIDs()`, or the `minimumItemCount = 2` padding
  frames that make a naive frame count over-report. Sourced from `CooldownViewer.lua` +
  `CooldownViewer.xml:283-333`. Would slot into §7 as a "getting the rows" preamble.

**`frames-textures-animation.md` — two, from the movable-frame work:**

- **The movable-frame family is entirely absent.** `SetMovable`, `StartMoving`,
  `StopMovingOrSizing`, `RegisterForDrag`, `SetClampedToScreen`, `SetUserPlaced`,
  `dontSavePosition` appear nowhere in §3 (Anchoring and size) or §4, despite §3 being the
  declared home for anchoring. The subtree's only mention of the drag family is inside the
  enumeration of the protected 59 in `security-taint-and-restricted-data.md:104`/`:108`.
  Every addon that draws anything needs this; cap had to reconstruct the position-
  persistence contract from Blizzard's Edit Mode source instead. Suggested home: a new
  `### 3.6 Moving a frame, and persisting where it went`, anchored on
  `EditModeManager.lua:295-320` + `EditModeSystemTemplates.lua:355-380`.
- **§8.1 (`:1252-1266`) omits that `UIParent` is itself `protected="true"`.** Tier 1:
  `Blizzard_UIParent/Mainline/UIParent.xml:4` —
  `<Frame name="UIParent" setAllPoints="true" protected="true" preventSecretValues="true" frameStrata="MEDIUM">`.
  Load-bearing for "is my addon frame protected?", because §1.2 says protection propagates
  to parents and anchor targets — and every addon frame is a child of, and anchored to, a
  protected frame. The resolution is that propagation is upward, so children are
  unaffected; but the KB never states the premise, so a careful reader can reason their way
  to the wrong answer. The same line is also the Tier-1 source for UIParent's `MEDIUM`
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
