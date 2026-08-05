---
title: Mined but not yet verified — the double-check queue
patch: 12.0.7
fetched: 2026-08-05
reviewed: 2026-08-05
sources:
  - EllesmereUI v8.7.5 @ c4eba58d996a8436f467ac8f297148bff9dd3008 (2026-08-04),
    https://github.com/EllesmereGaming/EllesmereUI — license CUSTOM, ALL RIGHTS
    RESERVED; read for API discovery only, no code copied. Mined 2026-08-05 via the
    `mine-addon` skill, five surfaces, ~51 raw facts. ⚠ CLONE DELETED — the file:line
    anchors below resolve ONLY against that commit; re-clone per
    `raw/addon-research/ELLESMEREUI-REMOVED.md` (gitignored, local).
  - https://github.com/Gethe/wow-ui-source (12.0.7 checkout) — the Tier-1 corroboration
    source for everything below.
confidence: low
---

# Mined but not yet verified

**This file is a QUEUE, not a claim.** Nothing in it may be cited as fact, copied into
a `knowledge/addon-dev/**` body, or built on. Everything here came out of a
third-party-addon mining run (Tier 3) and failed, or could not be given, Tier-1
corroboration. Each item says **exactly what would settle it**.

⚠ **Items marked COMMENT-SOURCED are the weakest class here, not the strongest** —
however convincing they read. The mined addon mandates rationale comments in its own
house style, so its comments are abundant, confident and narratively detailed; a claim
that exists *only* in a comment, with code merely consistent rather than demonstrative,
is capped at `confidence: low` no matter how specific the prose (`mine-addon` skill
§2.2, the strip-the-comments test). Build numbers and named exonerations raise
**specificity, not tier**.

⚠ **Why this is separate from `_meta/verify-in-game.md`:** that file is **generated**
from `@verify-ingame` markers on claims the KB already *asserts*, and it means "confirm
this while logged in." These are different — they are **not asserted anywhere**, and
several need a Tier-1 re-read or a PTR rather than a login. When an item here is
settled, either promote it into the right KB body (with `@verify-ingame` if it still
wants a client check) or strike it. It is not harvested by any tool.

Related queues, so nothing gets filed twice: `_meta/kb-inbox.md` (free-form un-routed
todos), `_meta/verify-in-game.md` (generated, asserted-claim confirmations),
`12.1.0-ptr-heads-up.md` (next-patch edit list).

---

## A. Needs an in-game measurement (12.0.7 live)

### A1. ✅ SETTLED `[client 2026-08-05]` — `item.auraDataCached` is a plain container with SECRET members

**Measured** in a real pull (Demonology, 29 item frames, the bound row on
`BuffIconCooldownViewer`): the record reads `table` through **both** the field and
`GetAuraDataCached()`, and is indexable — but `.expirationTime`, `.duration`, `.timeMod`
and `.applications` all read **secret**. Only `.auraInstanceID` is a plain `number`.

**So the capability this entry was chasing does not exist.** `cooldown-manager.md` §5.1
and §7 are correct that the in-combat DoT-remaining read is unanswerable, and this route
does not change it — the full claim now lives in `cooldown-manager.md` §7. What *is* new:
`auraInstanceID` is a readable in-combat per-aura identity, enough to distinguish "still
the same application" from "a fresh one", though it carries no timing.

The reasoning below is kept as the record of why the lead was worth chasing — the
"Blizzard's untainted code performed this read" caveat is exactly the thing that turned
out to matter.

**The highest-value open question in the queue**, and the reason the run was worth it.
Every CDM item frame parks the complete `AuraData` record of its bound aura on itself,
written in the same statement block as `auraDataUnit` — which we already measured
readable in combat — and exposed via `GetAuraDataCached()`
[Tier 1: `Blizzard_CooldownViewer/CooldownViewerItemData.lua:395-408, 411-413`].
Blizzard's own consumers read `.expirationTime`, `.duration`, `.timeMod`,
`.applications`, `.auraInstanceID` off it.

⚠ **The generated docs cannot answer this.** They annotate secrecy on **API
surfaces**; `auraDataCached` is a *Lua field on a frame* and appears nowhere in them
(verified by grep, 2026-08-05) — exactly like `auraDataUnit`, which is why
`cooldown-manager.md` §7 has a *measured* Tier 2 at all. Secrecy is tagged per value at
read time; Blizzard's **untainted** code performed this read.

**Settled by:** ClientLab `cdm-auradatacached-plain-in-combat` — class-check the record
*before* indexing it, then class-check each member, on a row with a live aura in combat.
⚠ The 12.1 note that `.applications` goes secret under a combat restriction is **moot
here**: it already reads secret at 12.0.7, along with every other time-bearing member.

### A2. Does `EvaluateRemainingDuration` leak a readable number?
§4.8.1 finding 4 ships the mechanism but **not** this. The API is annotated
`SecretWhenCurveSecret` — secret *when the curve is*. Ours is not. Read literally, a
**readable** number comes back derived from a sealed duration, which would let you
binary-search the remaining cooldown with step curves.
**Settles it:** one CurveLab cell — build a non-secret Step curve, evaluate against a
secret-bearing cooldown duration in combat, `ns.ClassOf` the result.
**Either answer is worth having:** secret ⇒ route only to `AllowedWhenTainted` sinks;
readable ⇒ a genuine gap in the seal, and a Tier-1 annotation that is incomplete.
Until then the KB says *treat the result as secret*.

### A3. `GetAuraDataByAuraInstanceID` off the item frame — nil, secret, or throw?
The frame's `auraInstanceID` is already proven to pass into
`GetAuraApplicationDisplayCount` (§7 Tier 2). A Tier-3 report says it also unlocks the
**full-record** getter — but that the call **hard-errors** on a restricted unit rather
than returning nil, so it needs `pcall` armour, not an `if`.
**Settles it:** call it in combat with a guarded instance id and classify the outcome
three ways. ⚠ Do this *before* A1's fallback path is designed.

### A4. Is `item.spellID` / struct-field secrecy real, or defensive superstition?
**A direct contradiction with our own measurement.** A shipping addon guards
`info.spellID`, `info.overrideSpellID` and every `linkedSpellIDs` entry from a *fresh*
`GetCooldownViewerCooldownInfo(cdID)` behind `issecretvalue`, on the stated grounds
that they can be secret on an active frame in combat. Our `/cdmp census` measured the
struct readable across 72 cooldownIDs, in and out of combat — but **on Destruction
only**.
**Most likely reconciliation:** their guard is carried over by analogy from the *frame*
read `GetSpellID()`, which genuinely does go secret (that one is confirmed, and tracks
frame **active-ness** rather than combat). **Settles it:** one census pass on a
non-Warlock spec with alternating overrides — Paladin armaments (cooldownID 29342, base
375576 Divine Toll) is the named case.
⚠ **Do not weaken §7 Tier 1 on this Tier-3 evidence alone.**

### A5. Does the loading screen really permit secure setup in combat? — ⚠ COMMENT-SOURCED, confidence LOW
Claim: `C_Timer` callbacks do not run during a loading screen, so an addon deferring
init by even one tick misses the only window in which `RegisterStateDriver` / `WrapScript`
/ protected `SetCVar` succeed on a `/reload` taken in combat. Corollary claimed: post-login
`ADDON_LOADED` **must** be deferred a tick, because it can dispatch from inside Blizzard's
own secure executions.

⚠⚠ **DOWNGRADED 2026-08-05 (was: low-medium). Fails the strip-the-comments test**
(`mine-addon` skill §2.2). The code shows only that they *do* init synchronously on
`PLAYER_LOGIN`; the reason — that this is the sole window, and why — lives entirely in a
comment. Synchronous init has several other plausible motives (ordering, simplicity), so
the code does not discriminate. One Tier-3 assertion.
**Settles it:** `/reload` while in combat; log `InCombatLockdown()` at `PLAYER_LOGIN` and
whether a `RegisterStateDriver` there succeeds. Cheap, and directly relevant to our own
addons' init ordering — this is the one on the list most worth actually testing.
[Tier 1 partial: `SecureHandlers.lua:435-439` hard-errors under `InCombatLockdown()`,
which is consistent only if the flag is false during the loading screen. That is the
mechanism being *consistent*, not the claim being *demonstrated*.]

### A6. Is `C_Item.IsItemInRange` genuinely *protected* against non-attackable units?
Claim: in combat it raises `ADDON_ACTION_BLOCKED` rather than returning a secret, so the
gate must be `UnitCanAttack` **before** the call — a value-side `issecretvalue` guard is
useless because the error has already fired. Would be a clean field example of §4.7's
`Secret` vs `Precondition` split. **Tier 1 declares no protection on it**, and 12.0.7
Blizzard UI has no live call site. Confidence: low.

---

## B. Needs a Tier-1 re-read or a second source (no client required)

### B1. Anchoring to a Blizzard frame as a taint injector — ⚠ COMMENT-SOURCED, confidence LOW
Claim: an **insecure frame anchored** (`SetPoint`) to a Blizzard frame poisons a secure
layout pass that later reads those anchors — parenting, existence and strata each
individually exonerated by bisection; the anchor tie alone sufficient. Stated rule:
geometry **reads** of a Blizzard frame are safe, anchor **ties** are not.
⚠ **This matters to us directly** — CDMProbe anchors its own textures to Blizzard's
Cooldown Manager icons, which is the exact shape described.

⚠⚠ **DOWNGRADED 2026-08-05 (was: medium). This claim does not survive the
strip-the-comments test** (`mine-addon` skill §2.2). The bisection, the exonerations and
the causal story exist **only in a source comment**; the code merely avoids anchoring and
is *consistent* with the claim without demonstrating it. The detail — nine gates, named
exonerations, a specific error string — raises **specificity, not tier**, and specificity
is precisely what made it read as measured. It is one Tier-3 assertion.
**Settles it:** find a Blizzard secure pass that demonstrably walks anchors, or a second
independent report, or reproduce it. No Blizzard source names anchors as a taint edge.
⚠ Do **not** restructure CDMProbe's anchoring on this alone.

### B2. Edit Mode calls `SetParent` on managed containers
Claim: `SetParent` fires Blizzard's layout handlers **synchronously in the caller's
execution**, and Edit Mode calls it on managed containers on every enter/exit — so
re-parenting inline from a `hooksecurefunc` on `SetParent` taints everything Edit Mode
touches for the rest of the session, invisibly (a "did it hide?" test passes).
**Settles it:** locate the Edit Mode `SetParent` call site in Blizzard source.
The accompanying rule — **`UnregisterAllEvents` is combat-legal and taint-clean, so
prefer it to reparenting** — is sound independent of the trigger and can be promoted
separately.

### B3. Attribute driver with a constant value as the restricted environment's only timer
Mechanism is Tier 1 (`SecureStateDriver.lua` re-applies only on change, on a ~0.2 s
poll), so a driver resolving to a **constant** self-rearms whenever a snippet writes a
different value. What is Tier 3 is whether this is *intended* or merely tolerated.
**Settles it:** judgement call — record as a technique with the caveat, or omit.

---

## C. 12.1.0 — annotate, do not act (keep writing 12.0.7)

⚠ **None of this changes 12.0.7 code.** It is here so that when something stops working
on patch day the cause is already written down. Detail lives in
`12.1.0-ptr-heads-up.md`; this section is only the *"what might stop working"* list.

⚠⚠ **Read every 12.1 name below as "real at some PTR build", not as a shipping
signature.** The mined addon's own migration history shows the API changing **twice**
under it: a `SetAuraLayout*` → `SetFlowLayout*` rename, and an
`Enum.CustomAuraButtonBorderStyle` → `…DispelTypeTextureStyle` deletion. Build numbers
cited in the raw findings (68745, 68824, 68914) are PTR builds, not releases.

| what may stop working | why | our exposure |
|---|---|---|
| `GetPlayerAuraBySpellID` on a given spell | the `RequiresNonSecretAura` allowlist is **narrowing** build-over-build (Ebon Might dropped) | **high** — any aura read keyed to one spell |
| Reading `AuraData` at all | structs go **wholly** secret; `UNIT_AURA` payload secret — and the payload **table itself** is a secret value, so `issecretvalue` it *before* indexing, then again on `isFullUpdate` | high |
| `item.auraDataCached.applications` | Tier-3 report of a 12.1 combat restriction | **high if A1 pays off** |
| Reparenting Blizzard unit frames | alt-power bars under `PlayerFrameAlternatePowerBarArea` become descendants of an insecure frame and drive a chain into `GetAuraSlots` → hard error `RequiresUnitAuraAccess` | medium |
| `SECURE_ACTIONS.click` | reported broken; workaround is a **globally named** proxy driven by `/click <name>` | medium |
| `SecureAuraHeaderTemplate` | removed in favour of AuraContainers ⚠ **unconfirmed by this run** — the mined addon never used it, so we have no evidence either way. It still exists at 12.0.7 (`SecureGroupHeaders.lua/.xml`) | low |

**The replacement contract, in one line each** (all `IS_121`-gated, all Tier 3):
`CreateFrame("AuraContainer", …, "CustomAuraContainerTemplate")` → set layout →
`AddAuraGroup` / `AddAuraSlot` → **`SetUnit` LAST** (it re-evaluates event registrations,
which are gated on content already existing) → `UpdateAllAuras()`. The container must be
**visible with a real rect** or the engine builds it and never parses an aura, silently.
- **A button never learns which aura it shows.** You register *output sinks* —
  `SetIcon`, `SetDurationCooldown`, `SetApplicationCount`, `SetDurationText` — and the
  engine fills them. §4.8's thesis as a first-class widget API.
- **`initializeFrame` is the only window** in which addon code may touch a button;
  afterwards `DenyTaintedAccessWhenAurasAreSecret` blocks **reads and writes**.
  *Build it all at creation, then never touch it.*
- **Forbidden aspects are conferred at CREATION only** — reparenting does not grant
  them; birth the object inside a `DisableUntrustedLayoutScriptsTemplate` holder.
- **Flow layout only anchors** — an unsized button renders nothing.
- Filter strings gain `!` negation (absent at 12.0.7, verified); groups cannot OR.

---

## D. Applied already — do NOT re-mine

Recorded so a future run does not re-derive them. All Tier-1 corroborated 2026-08-05.

- `security-taint-and-restricted-data.md` §7 claim 7 — **`table` IS in the restricted
  environment** (`table.new()` is the sanctioned `{}` substitute)
- §7 rule 19 — the `Shown` aspect **is** reachable on engine-owned subtrees; guard the
  getter
- §4.7 — `C_Spell.IsSpellInRange` is the unpredicated substitute for secret `UnitInRange`
- §4.8.1 findings 11–14 — curve-on-duration, `SetToTargetValue`,
  `SetCooldownFromDurationObject` needs no range, `GetRemainingDuration` →
  `SetFormattedText` (and `type()` is the wrong guard)
- `cooldown-manager.md` §7 — `RequiresNonSecretAura` correction, `auraDataCached` row
- `12.1.0-ptr-heads-up.md` — the per-spell-lookup correction

**Rejected as superstition, do not resurrect:** *"never call `EnableMouse`/`SetAlpha` on
a secure button after creation — it breaks the trust chain."* No Blizzard source supports
it; the real constraint is the ordinary combat/protected-frame rule.
