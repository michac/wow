# Plan — `api-events-and-discovery.md` **and** `cooldown-manager.md`

**Read `00-brief.md` first.** You own **these two files**, and no others.

**You have two files because there is a transfer between them** (§3). Two independent
agents would either duplicate the content or drop it.

**This is the largest and most delicate job in the fan-out.** It carries the corpus's
worst wrong-base-text case.

| File | Gate 1 | Gate 2 | Gate 3 |
|---|---|---|---|
| `api-events-and-discovery.md` (~95 KB) | **8** | **26** | 0 |
| `cooldown-manager.md` (~41 KB) | 0 | **24** | **2** |

---

## 1. The worst wrong-base-text case in the corpus — `api-events:626-650`

Read all 25 lines before editing. The structure is "hypothesis, then measured answer", but
**the hypothesis is written in flat present-tense fact-voice**, so a reader who greps
`pandemicEndTime` lands on the false half.

Base text (`:628-634`) currently says the item carries **live state an addon can read**,
lists `pandemicStartTime` / `pandemicEndTime` as *"plain numeric fields"*, and calls
`pandemicEndTime` **"one of the few routes to a tracked DoT's remaining duration"** — the
most attractive sentence in the section.

Eleven lines later (`:639-648`), measured:

| Read | In combat |
|---|---|
| `item.pandemicStartTime` | **`SECRET`** |
| `item.pandemicEndTime` | **`SECRET`** |
| `item:IsInPandemicTime(t)` | **throws** |
| the `PandemicTime` **alert** | ✅ fires normally |

**Rewrite the base text so the false claim cannot be reached.** The surviving facts: the
fields are set at `[:534-542]`; they **read secret in combat**; `IsInPandemicTime` **throws**
rather than returning a secret, because its body *compares* those fields (so the guard is
`pcall`, not `issecretvalue` — that distinction is a genuinely valuable claim, keep it);
the usable pattern is an **edge-driven latch on the `PandemicTime` alert**, not a state
poll. Out-of-combat behaviour is unmeasured — say so.

Tag the measurement `[client 2026-07-30]`. Delete the ❌/**MEASURED** framing.

⚠ `:650` then says *"So the earlier **hypothesis (b)** is what happens"* — **there is no
(a)/(b) list anywhere in §2.8.** It was deleted; the reference survived. Delete the
dangling clause.

---

## 2. `item:IsActive()` — `api-events:584`

This file cites `item:IsActive()` as **positive evidence** of a channel that stays readable
in combat. Three other files — `cooldown-manager.md` (`:503`, `:543`, `:556-564`) and
`security-taint-and-restricted-data.md` (`:1578-1588`, `:1990`) — call it a **constant
`true` on tab 1**, *"ACTIVELY MISLEADING"*, and *"the standing counter-example"*.

**api-events is the outlier and is wrong.** Rewrite `:584` so `IsActive()` is presented as
the counter-example it is: readable, and *useless* on a tab-1 row because the value is
constant. Cite `cooldown-manager.md`.

---

## 3. The transfer — `api-events` §2.8–2.9 → `cooldown-manager.md`

§2.8–2.9 is **~20.9 KB, 22% of `api-events`**, and it is a Cooldown-Manager study sitting
in the events topic file. README §1's own partition contract says any addon-dev question
lands in exactly one file; this violates it.

**Move it.** Leave behind in `api-events` only the *generalisable* claim §2.8 opens with
(`:563-567`): **a choke-point method is a dispatch shape, and `hooksecurefunc` on it is a
supported way to observe a subsystem** — that is an api-events fact. Everything specific to
CDM rows, alert types and pandemic fields goes to `cooldown-manager.md`.

Do §1 and §2 **first**, so you are moving corrected text rather than moving sediment.

Merge it into `cooldown-manager.md` where it belongs topically — do not append it as a
foreign block. Preserve every citation and `[client]` tag.

---

## 4. `cooldown-manager.md` specifics

**`:525` — the `AuraData` cell.** Opens *"The **entire `AuraData` record** is secret when
restricted."* then immediately *"⚠ But … was too strong — **CORRECTED 2026-08-05**."* The
first sentence is what a table scan returns. Rewrite the cell to state the corrected,
narrower claim directly.

⚠ While you are there: `RequiresNonSecretAura` appears in this file, in
`12.1.0-ptr-heads-up.md` and in `mined-pending-verification.md` — but **not** in
`security-taint-and-restricted-data.md` §4.7, which is the predicate census README routes
predicate questions to. Another agent owns that file. **Report it; do not edit security.**

**`:570-577` — three struck-through closed gaps.** A closed gap is not pending work.
Verify each answer already lives in the body (§7 / §2.7), then delete all three
strike-throughs. Keep the two live `[gap] NEW` entries.

**`:582-583` — a `[gap] NEW` that is already answered.** It asks how far
`GetValidAlertTypes` under-reports. `api-events:776-791` answers it: `CanTriggerAlertType`
is called in exactly one place, so the list gates `PandemicTime` only. **You own both
files — close this gap properly**, moving the answer across with the §3 transfer.

**`:504` — a 1,180-character table cell that is ~80% narrative** about a Destruction
Warlock's afternoon. The rule is one clause. Compress to something like:

> `[client 2026-07-31]` readable in combat. Plain `"player"`/`"target"`; non-nil **iff** the
> row has a live bound aura, and it discriminates (nil before application, set after) — the
> only in-combat "is the DoT up" read available.

Apply the same treatment across §7's Tier-2 table: a **narrow table** (field · family ·
status · one-line rule) plus short prose beneath for the three fields that genuinely need
explanation (`auraDataUnit`, `auraInstanceID`, `PandemicIcon`).

**Do not touch `cooldown-manager.md` §0** (`:22-48`). It is the best-written scope
statement in the corpus and is the model the other files should follow.

---

## 5. Gate 2 — the `[client]` conversion

Most of your 50 combined date hits are **measurements**, not narrative. The fix is
conversion, not deletion: `**MEASURED 2026-07-30:**` → `[client 2026-07-30]`, and
`✅ **CONFIRMED IN THE CLIENT, 2026-07-30**` → the same. The date survives; the theatre
does not.

`cooldown-manager.md`'s `reviewed:` line carries a `# + a client capture 2026-07-31`
comment. **That is a good pattern nothing else uses** — keep it, and mention it in your
report as a candidate convention.

---

## 6. Report, do not act

`api-events` has a non-standard extra front-matter key `verified: 2026-07-23`, used by only
this file and `libraries-and-ecosystem.md` — 2 of 12, defined nowhere. Leave it; report it.
