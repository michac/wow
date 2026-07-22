# BucketBinds — a one-shot keybind/bar dumper for WoW

**Status: v0.10.0 (LAYOUT v2), released + deployed 2026-07-21.** Next work item:
the per-spec re-filing — see the ⚠ below.

**In-game pass 2026-07-21 (partial):**

| Area | Result |
|---|---|
| **Dump / keybinds (layout v2)** | ✅ **verified** — bindings update as intended |
| **Console (M4a)** | ❌ **bug found + fixed** — see below; needs re-verify |
| **Macros (M5 A/B)** | ⚠ present on the bars, **not yet exercised** |
| **Spill reachability** | ❌ **bug found + fixed** — see below |
| Snapshot/restore, ring, diagnostics | not covered this pass |

The console bug: `ensureFrame()` never hid the frame it built, and `CreateFrame`
returns a **shown** frame. So the first `/bb` created the window in a shown state,
`Toggle` saw `IsShown() == true` and immediately hid it — the first press did
nothing and only the second opened the console, on every fresh login. Fixed by
`frame:Hide()` at the end of `ensureFrame()` so Toggle/Show/Hide have one known
origin state. **Unreleased** — needs a v0.10.1 cut to reach the game.

The spill bug (found from "why does Create Healthstone report as on a bar, but a
bar for a different stance?" on a Demonology warlock): `placedSpellSet()` scanned
absolute slots **1–144 flat**, which sweeps in the form/stance bonus bars
(73–120) for *every* class. Those are real action slots, but the UI only shows
them for a class that has forms — so Create Healthstone sitting on slot **114**
(bonus bar 4) counted as "already on a bar", and `/bb spill` suppressed it,
leaving it invisible and unbindable. Nine of thirteen classes are affected.
Now scans by **reachability**: 1–72 and 133–180 always; 73–120 only for a
`FORM_BONUS_BARS` class and only that class's own offsets; 121–132 (skyriding)
never, since it's usable only while flying.

Same root cause, second defect: `onShapeshift` fired for **any** class whenever
`GetBonusBarOffset()` went non-zero — including offset 5 on a skyriding mount
(base 121) — mirroring the rotation onto the empty half of the skyriding bar. Now
guarded on `FORM_BONUS_BARS[class]` plus a `base+11 > 120` bail.

⚠ Slot ranges confirmed empirically from a real snapshot this pass: **121–132 is
the skyriding bonus bar** (held Surge Forward / Skyward Ascent / Aerial Halt), so
73–120 = form bars 1–4 as assumed. `SPILL_BASE = 145` still `@verify-ingame`.

<details><summary>History (M0 → v0.9.0)</summary>

M3.1 shipped + verified in-game (`/bb diagnostics`, v0.4.0) on top of M3
(spillover) + M2 (dumper) + M1 (snapshot/restore). Seed is JSON-authoritative
(xlsx frozen to archive), bars re-laid-out to a modifier-grouped 12-slot scheme
with the 2026-07-16 combat-key swap (`Q E R F` / number row), `/bb dump --nobind`
+ `/bb test` added, and `/bb diagnostics` gives an honest read-only resolution +
placement report (read off disk by `wowkb.diagnostics`). The 2026-07-16 in-game
pass confirmed the dump/placement path is solid and surfaced a follow-up →
**M3.2** (classifier over-reports `unresolved` because `GetSpellInfo` is
knowledge-gated; + a seed-name triage list) — still open.
**Also 2026-07-16: mouse relocate** — the movement + personal-defensive
family moved off `Z`/`X` onto the three mouse buttons (`M4`/`M5`/`M3` + Shift
variants), freeing those keys; `normKey` gained mouse + Shift-mousewheel tokens
and the dump now vacates stale keys on relocated slots (see "Mouse relocate" under
The layout). Autorun dropped from middle-mouse. **And v0.5.0: M6 OPie start** —
`/bb ring` builds an OPie overflow ring from the `/bb spill` set via
`SetExternalRing`, gated on `## OptionalDeps: OPie`; new `exclude_spells` seed
table filters noise out of both spill and the ring; two seed misses fixed
(`Implosion`, `Blight of Tongues`). All bundled into **v0.5.0 — committed +
released.** **Then v0.6.0: contextual bar** — `ALT+1..8` now
binds the pet bar (`BONUSACTIONBUTTON`) or stance bar (`SHAPESHIFTBUTTON`) per
class (runtime-detected at dump); reclaims the keyless Trinket/Racial/Free
`A1..A4` slots. Since then: **M5 Phase A** set-focus + smart focus-interrupt
macros and **M5 Phase B** the rest of the utility/prep band — both developed as
"v0.7.0"/"v0.8.0" but **never released under those numbers**; they shipped folded
into **v0.9.0 (2026-07-17)** alongside M4a, the schema-driven console +
`Output.lua`. Releases run v0.6.0 → v0.9.0 → v0.10.0; there is no v0.7.0/v0.8.0
tag or release.

</details>

**Then LAYOUT v2 — shipped as v0.10.0, 2026-07-21. Addon is at v0.10.0.** Two
things landed together:

1. **An override-resolution bug fix.** `resolveSpellID` used
   `C_Spell.GetSpellInfo(name)`, which follows whichever override is live *at that
   instant* — so a dump taken while Grimoire: Fel Ravager was on cooldown baked
   **Devour Magic** onto its key, and a dump with the Diabolist Pit Lord art armed
   baked **Ruination** onto Hand of Gul'dan's. Both read in-game as "the ability
   never got bound". Now `normID`/`FindBaseSpellByID` is folded into
   `resolveSpellID`, so placement always uses the **base** spell and the game
   re-applies the override on the button itself.
2. **The layout v2 key map** — the band rename (`Combat 1-8 → Rotational 1-8`,
   `Combat 9-12 → Cooldown 1-4`, new `Overflow 1-6`), the bars 4/5 reorg, and the
   reactive buckets moved off Ctrl/Alt. Seed went 52 → **58 buckets (54 placed)**;
   40 specs and 1538 mappings unchanged. Design rationale, the banding contract,
   and the full per-spec plan live in **`data/layout-v2-proposal.md`**.

**⚠ What v0.10.0 did NOT ship: the per-spec re-filing** (that doc's §6). Every
spec's abilities still sit in their **v1 ordinals** — the bands were renamed and
re-keyed, but nothing moved between them. Concretely, Demonology still has Summon
Demonic Tyrant on `2`, a dead `3`, an entirely empty `Cooldown 1-4` band, and
Dominion of Argus bound nowhere. **That is the next work item.**

A self-contained WoW addon that does two things the game won't:

1. **Ability dump** — given your class+spec, place every ability/item into a
   fixed **bucket → action-slot** layout and set the keybinds in one shot, then
   get out of your way. No background daemon, no continuous re-sync. Dump once,
   tweak by hand, done.
2. **Transactional save/restore** — snapshot your entire keybind + action-bar +
   macro state to a named profile and restore it atomically (with a pre-restore
   backup). The game has binding *sets* and Edit Mode *layouts* but no
   snapshot/rollback of "this whole arrangement." This fills that gap.

Everything happens **inside the addon** — no external web tool. (Decision:
2026-07-10.) The seed data ships baked into the addon as a Lua table.

## Origin

Concept lifted from Bellular's "Ultimate Midnight Keybinding System"
([video](https://www.youtube.com/watch?v=PohMTq87jds)). We take their two good
ideas — (a) sort every ability into a **category/bucket**, (b) bind the same
category to the same key on **every spec** — and drop what we didn't want: a
live-maintained web tool and an addon that wants to run/re-sync continuously.

## The core insight (why "same key across all specs" works)

WoW keys bind to **action-bar slots** (`ACTIONBUTTON1`, `MULTIACTIONBAR…`), not
to spells. So "V always interrupts" really means:

> bind the key→slot layer **once** (stable, rarely touched), then for each spec
> place *that spec's* interrupt into the slot `V` fires.

The dump is therefore two independent layers:

- **Key→slot layer** — a stable table `(bar, slot) → keybind`. Set once.
- **Spec→slot layer** — the classification `(spec, bucket) → ability`, placed
  into the slot that bucket owns.

The Bellular spreadsheet turned out to encode exactly this (its "Master Sheet"
is literally `Bar | Slot | Keybind | Category | <ability per spec>`), which
validated the model and handed us the whole classification as a seed.

## The layout — **v2, current (shipped v0.10.0, 2026-07-21)**

> **This section is the layout-of-record: it describes what the shipped addon
> does today (v0.10.0).** The design rationale, the banding contract, and the
> not-yet-applied per-spec re-filing live in `data/layout-v2-proposal.md`. That
> doc's §2/§3 are **shipped** and mirrored here; its §6 is **still pending**.

**Why v2 exists.** The bucket ordinals `Combat 1…12` were spreadsheet row
numbers, never a priority ranking. Two key-layout swaps (2026-07-14, 2026-07-16)
re-keyed all 1538 spec→ability mappings without re-auditing what those ordinals
meant, so `Combat 9–12` became a junk drawer holding both burst cooldowns and
healer externals. v2 renames the bands so they mean something, and moves the
reactive buckets off the worst-reach modifiers.

### The band contract

| Band | Keys | Bar/slots | Holds |
|---|---|---|---|
| **Rotational 1–4** | `Q E R F` | 1 / 1–4 | the four most-pressed buttons, ordered by frequency |
| **Rotational 5–8** | `1 2 3 4` | 1 / 5–8 | AoE swaps, active mitigation, maintenance, short-CD (<45s) |
| **Cooldown 1–4** | `SHIFT-Q E R F` | 2 / 1–4 | major cooldowns ≥45s, pressed on CD or in a burst window |
| **Overflow 1–6** | `CTRL-R F 1 2 3 4` | 3 / 3–8 | specs with more real buttons than banded slots |

Three rules fall out: **frequency, not power** (a 30s button pressed twelve times
a minute is Rotational); **externals are not combat abilities** (defensives cast
on *other people* go to `Class 7 (Raid Defensive)`); **overrides share a key**
(bind the base — Infernal Bolt/Shadow Bolt, Wither/Immolate, Windstrike/
Stormstrike — and let the game swap the icon; this is what the v0.10.0 override
fix makes reliable).

#### Fixed vs floating buckets (v0.11.0)

A band slot is filled one of two ways:

- **Fixed** — a numbered bucket (`Rotational 3`) whose ability the spec always
  has. Exactly as before: `abilities["Rotational 3"] = "Blood Boil"`. The slot
  never goes empty, so the key never changes occupant.
- **Floating** — a band-level candidate list (`floats["Rotational"] = ["Power
  Siphon", "Implosion", …]`). At dump time the addon resolves each name, keeps the
  ones that resolve (= talented), and fills the band's **empty** slots (the ones
  with no fixed assignment) in list order. Mutually-exclusive choice-node abilities
  stop being a problem: only one ever resolves. This works because **keys bind to
  slots, not abilities** — a float landing in slot N is live on N's key with no
  extra `SetBinding`.

Default classification (overridable by the seed author): a `SkillLineAbility`
baseline → **fixed**; a talent → **floating**. In practice a spec's mandatory
core talents (Hand of Gul'dan, Summon Demonic Tyrant) are hand-promoted back to
**fixed** so `Q E R F` / `SHIFT-Q` stay anchored.

**The ordering rule.** When a float drops out on respec, the churn equals *the
number of floats after it* — fixed slots never move. So:

- **Fixed** abilities are placed purely by **press frequency** (the band contract
  above). There is no stability tradeoff — they never vanish.
- **Floats** are ordered by **likelihood of being talented** — meta-stable talents
  first, experimental last. That is the only lever on churn, and it's why floating
  is scoped to `Rotational` / `Cooldown` / `Overflow` only: the other numbered
  families (`Self-Heal`, `Class`, `PvP`) are stable role slots, not
  build-conditional pools.

**Anchors stay empty.** Floats fill only slots with no fixed assignment. A fixed
slot whose ability is somehow absent stays empty rather than being back-filled —
`Q E R F` must not change occupant based on talents. Floats that don't fit their
band spill to `Overflow`, then to `/bb spill` / the OPie ring; never silently
dropped. **Demonology was the v0.11.0 pilot** — **verified in-game 2026-07-21**
(talented floats fill the empty Rotational/Cooldown slots and the Grimoire
choice-node churn test passes). **v0.12.0 completed the rollout to all 33
DPS/tank specs** (batched by ~10, apply+eyeball+gate per batch, single release);
the 7 healers stay held per layout-v2 §10 until sourcing improves. In-game
verification of the 32 non-pilot specs' float placement is the outstanding pass.

### The key-tier model (added v2.1, 2026-07-21)

What made v2.0 place self-heals badly was having no written ranking of key
*reach*. Buckets are filed by how reactive they are; keys are ranked by how fast
they are; the two must line up.

| Tier | Keys | Holds |
|---|---|---|
| **S** | `Q E R F` | the most-pressed rotational buttons |
| **A** | `1 2 3 4`, `C`, `V`, `M4`, `M5` | secondary rotation, interrupt, CC, movement/defensive |
| **B** | `SHIFT-QERF`, `Z`, `X`, `M3`, Shift+mouse | cooldowns, reactive utility, self-heals |
| **C** | `SHIFT-1234`, `SHIFT-ZXCV` | situational combat, panic items |
| **D** | `CTRL-*`, **the `5`–`0` row**, far `ALT-*` | prep and out-of-combat only |

**Tier by finger, not by modifier name** (refined 2026-07-21). The first cut of
this table ranked `ALT-*` flat-bottom, which is wrong. What actually sets the
tier is *which finger holds the modifier and what that finger gives up*:

| Modifier | Finger | Costs you |
|---|---|---|
| `SHIFT` | left pinky (on `A`) | **strafe left** |
| `CTRL`  | left pinky, further down | **strafe left**, more awkwardly |
| `ALT`   | left **thumb** (on space) | **jump** only — strafing is unaffected |
| mouse   | right hand | nothing |

So `ALT` is not automatically worse than `CTRL`: the thumb is otherwise idle, and
`ALT-Z/X/C` in particular are a single relaxed hand shape because the modifier sits
directly beside the keys. The real distinction is **stationary-reachable vs
kite-reachable** — `ALT+`left-cluster is fine for a target-cast utility press you
make while planted, and bad only for something you need mid-movement.

**`5`–`0` is tier D, not tier B.** It reads *near* the number row, but your hand
has to leave home position — it's a row you reach for deliberately between pulls.
Nothing reactive may live there. That row is the **prep band**: Buff, Mount, Res,
trinket, racial, damage potion.

Corollary, and the exact v2.0 bug: **"use a Healthstone" is a panic button, not
prep.** Only *Create* Healthstone is prep. v2.0 had them backwards, and had both
self-heals on `6`/`7`.

### Bars 1–3 — the modifier layers

One modifier layer per physical bar over one shared 12-key template
`Q E R F 1 2 3 4 Z X C V`, so **slot N is the same physical key on every bar**.

| Bar (modifier) | Slots 1–4 | Slots 5–8 | Slots 9–12 |
|---|---|---|---|
| 1 unmod | Rotational 1–4 | Rotational 5–8 | `Z` Raid Defensive · `X` **Self-Heal 1** · `C` CC · `V` Interrupt |
| 2 Shift | Cooldown 1–4 | `S1` Self-Heal 3 · Class 2–4 | `SZ` **Healthstone (use)** · `SX` **Self-Heal 2** · `SC` CC 2 · `SV` Slow |
| 3 Ctrl | `CQ` focus macro† · `CE` Self-Heal 4 · Overflow 1–2 | Overflow 3–6 | `CZ` PvP 1 · `CX` PvP 2 · `CC` PvP 3 · `CV` Taunt/Quick Access |

The `Z X C V` cluster is a coherent **react-to-what-just-happened** group.
Refilling `Z`/`X` (vacated by the 2026-07-17 mouse relocate) is not a reversal of
that decision — the relocate moved abilities you press *while kiting*; these are
target-cast or self-cast presses.

### Bars 4/5 — the two vertical side bars

These do **not** follow the 12-key template. They sit side by side on screen, so
slot *N* of each is horizontally adjacent — which is why the mouse cluster is
laid out row-wise across the two columns instead of running up one bar.

| Slot | Bar 4 (`MULTIACTIONBAR3`, "Right") | Bar 5 (`MULTIACTIONBAR4`, "Left") |
|---|---|---|
| 1 | `M3` Class 1 (Movement) | `SM3` Immune/Spell Immune/Movement |
| 2 | `M4` Movement Ability | `SM4` Movement Ability 2 |
| 3 | `M5` Personal Defensive 1 | `SM5` Personal Defensive 2 |
| 4 | `5` **Buff** *(Create Healthstone on Warlock)* | `ALT-Q` flask macro† |
| 5 | `6` **Mount** | `ALT-E` buff-food macro† |
| 6 | `7` **Res** | `ALT-R` Drinking/Mana Potion |
| 7 | `8` Trinket macro | `ALT-F` Another Combat Item |
| 8 | `9` Racial | `ALT-Z` **Class 6 (Dispel)** |
| 9 | `0` Damage Potion | `ALT-X` **Class 5 (Purge)** |
| 10–12 | Free ×2, free | `ALT-C` **Class 8 (Lust/BRes)** · free ×2 |

**Bar 4's `5`–`0` row is the prep band** — everything on it is pressed between
pulls, never in reaction to anything.

† **Not seed buckets** — the focus/flask/buff-food macros are hardcoded to their
bar+slot in `Macros.lua` (`FOCUS_SLOT`, `PREP`). Grepping the seed for them finds
nothing by design. `ALT+1..8` remains the contextual pet/stance bar (bound, never
placed; see "Contextual bar" below).

**What v2 bought:** the reactive family — Healthstone-use, Self-Heal 1/2, Raid
Defensive — sits in tiers A–C instead of on Ctrl/Alt, and flask + buff-food
(pressed once an hour, out of combat) stopped squatting on unmod `8`/`9`.

**What it cost (v2.1, deliberate):** tiers A–C were full, so Dispel, Purge and
Lust/BRes were demoted to the `ALT` band to make room. Per the finger model above
this is a smaller cost than it first looked — `ALT-Z/X/C` is a relaxed one-hand
shape, stationary-reachable, just not kite-reachable. Fine for a DPS.

⚠ **Still the first thing to revisit for a healer.** Dispel is among the most
reactive presses in the game for them, and "stationary-reachable" is not good
enough when you're dispelling on the move. Accepted knowingly for a DPS-first
layout. `@verify-ingame` on a healer spec.

**⚠ Abilities have not moved between bands yet.** The rename and re-key shipped;
the per-spec re-filing (proposal §6) has not. Every spec's abilities still sit in
their v1 ordinals.

### History: the combat-key swap (2026-07-16)

Superseded by the banding above, kept for context. Within slots 1–8, the letter
cluster `Q E R F` took the most-spammed abilities and the number row `1 2 3 4`
the next tier — swapped from the original `1 2 3 4 / Q E R F` because QERF are
faster to hit under pressure. v2 kept both key runs exactly where they were and
changed only what the ordinals *mean*; a scan of all 40 specs showed the old
`Combat 5–8` band was the *more* rotational one (Death Strike, Ignore Pain,
Ironfur, Demon Spikes, Rejuvenation, Penance), so demoting it to a modifier layer
would have been the most damaging change available.

### History: the mouse relocate (2026-07-16, revised 2026-07-17)

The movement + personal-defensive + immune family is fired by the **three mouse
buttons** (+ Shift) — strictly easier to hit while strafing. Its *current* home
is bars 4/5 slots 1–3 (see the table above); this is how it got there.

The **first cut (2026-07-16)** only re-keyed these buckets to the mouse buttons
but left them on their bar-1/2/3 slots. That **broke the modifier-bar invariant**
("slot N = `<mod>` + the *same physical key* on every bar"): slot 9 became
`Mouse5 / Shift-Mouse5 / Ctrl-Z` across bars 1/2/3 — a keyboard/mouse mix.

The **fix (2026-07-17)** *moved* the six mouse-fired buckets onto the then-free
bar 5 (buttons 4–9), keeping the mouse keybinds. Bars 1/2/3 reverted to a clean
`<mod>+{Q E R F 1 2 3 4 Z X C V}` keyset, freeing `Z`, `X`, `S1`, `SX`, `SZ` and
`Ctrl+C`. Because bars 4/5 are form-static, the mouse button fires these in
**every** form with no form-mirror needed (an improvement over hosting
Movement/Def-1 on the paging bar 1).

**v2 (2026-07-21) moved them once more**, from bar 5 buttons 4–9 to **bar 4/5
slots 1–3**, so the six read as three horizontal rows across the two adjacent
vertical bars (`M3/SM3`, `M4/SM4`, `M5/SM5`) rather than a single vertical run.
The keybinds themselves did not change. v2 also refilled `Z` and `X` with Raid
Defensive and Dispel — see the bars 1–3 table.

M4/M5 = thumb buttons (primaries), M3 = middle/scroll-click (tertiary). Ease
order honored: only unmodified + Shift, no Ctrl/Alt. Autorun (formerly unmod
middle-mouse) was dropped — it stays on the NumLock default. `normKey` also
learned `MU`/`MD` (Shift+mousewheel) tokens for future use — unmodified wheel
stays reserved for camera zoom.

⚠ **Relocation caveat (applies to the v2 move too):** a re-dump repoints every
key correctly — `SetBinding` is authoritative per key, so a key can only ever
point at one command — but a stale *ability icon* may linger on a slot that left
the managed set until `/bb undo` or a fresh restore, because the dump's clear
pass only walks current seed buckets. After v2 the only such slot is bar 4 / 12
(the old Mount placeholder), which never held real content. **Take a `/bb save`
before your first v2 dump regardless** — it moves nearly every key.

**Contextual bar → `ALT+1..8` (2026-07-16):** the `ALT`+number row now binds the
character's **pet bar** (`BONUSACTIONBUTTON1-8`) or **stance/form bar**
(`SHAPESHIFTBUTTON1-N`) — whichever that class uses, **detected at dump time**
(`GetNumShapeshiftForms() > 0` → stance; else a `PET_CLASS` → pet; else the row is
cleared/free). This is *dumper* logic, not a seed bucket: these are separate
binding namespaces the game auto-populates, so BucketBinds only binds them, never
places. It reclaims `ALT+1..4`, which were the (M5, not-yet-built) **Trinket /
Racial / Free** macro slots — those buckets are now **keyless** (`keybind: ""`,
bar-4 slots 5–8 retained under v1). **M5 Phase B landed them**, and **LAYOUT v2
re-keyed them**: the macro pass now binds Trinket → `8` (bar 4 / slot 7) and
Racial → `9` (bar 4 / slot 8); the two `Free` buckets (bar 4 / slots 10–11) stay
unbound. `@verify-ingame`: command names + per-class button counts in 12.0.7.

Out-of-combat sprawl (mounts/toys/teleports/buffs/specs) is **not** bound to
keys — it goes on OPie rings. The addon marks those buckets "on a ring" and
skips them. The OPie master-ring import string is a separate, untouched asset
([pastebin](https://pastebin.com/bG3zMdT7)).

## Data pipeline

```
data/bellular-keybinds.seed.json   CANONICAL, hand-edited source of truth
  └─ tool/gen_data_lua.py          (the one live-workflow step)
       └─ addon/BucketBinds/Data.lua   generated; the addon loads this (never hand-edit)
```

The **JSON is authoritative** — it carries the Tier-A/B ability corrections and
the modifier-grouped re-layout the workbook never had. Edit the JSON, run
`gen_data_lua.py` (which also has `--check` for CI), diff, ship. `Data.lua` is a
generated build artifact.

The Bellular **.xlsx is a frozen archive**, no longer in the workflow.
`tool/extract_seed.py` still exists but only to *re-derive* the seed from the
workbook for reference — it writes a **side file**
(`data/bellular-keybinds.archive-import.json`, gitignored) and does **not** touch
the canonical seed or `Data.lua`. Diff it by hand if Bellular ever ships a sheet
worth comparing. Current seed: **58 buckets (54 placed + 4 stance), 40 specs,
1538 ability mappings**, plus item-ID and buff reference tables and an
**`exclude_spells`** noise list (keyed by spellID and/or name) that `gen_data_lua`
emits as `ns.SEED.excludeSpells` for `/bb spill` + `/bb ring` to suppress.

## Milestones

- [x] **M0 — seed + skeleton.** Extract workbook → seed.json + Data.lua; project
      home under `projects/keybinder/`; this doc.
- [x] **M1 — snapshot/restore.** Read current bindings (`GetBinding` /
      `GetCurrentBindingSet`), every action slot (`GetActionInfo` incl.
      bonus/stance/dragonriding bars), and macro bodies → serialize to a named
      SavedVariables profile. Restore = back up current, then re-apply
      atomically, combat-guarded. **Ship this first** — it's taxonomy-independent
      and de-risks the write-bars plumbing everything else needs.
      *Shipped v0.1.0: `Snapshot.lua` (`Capture`/`Apply`) + `/bb
      save|restore|undo|list|delete` + combat-defer queue.*
- [x] **M2 — dumper.** Given class+spec, walk the seed's placeable spell
      buckets, resolve each ability name→spellID at runtime, place it on the
      fixed `(bar, slot)` action slot, mirror the main bar onto form/stance
      bonus bars, and set the key→slot bind — one shot, combat-gated, with an
      auto-backup so `/bb undo` reverts it. The `bar=None` Stance buckets
      (consumable/trinket/racial macros + Stance/Free) are reported as
      `skipped (M5)`, never silently dropped.
      *Shipped v0.2.0: `Dump.lua` (`ResolveSpec`/`Resolve`/`Run`, runtime
      `resolveSpellID` + spellbook fallback + alias layer, `BAR_MAP`,
      `FORM_BONUS_BARS` + self-healing `UPDATE_SHAPESHIFT_FORM` hook) + `/bb
      dump [<Spec>|<Class> <Spec>]` + generalized combat-defer thunk queue
      (`ns.QueueAction`). Dev-side `tool/check_seed_spells.py` cross-checks every
      seed ability name against a wago `SpellName` dump (caught the
      `Efflorescence?` sheet typo → aliased).*
- [x] **M3 — spillover: surface every unmapped ability.** After a dump, enumerate
      the character's full active spellbook (General + class + active-spec skill
      lines), subtract what's already on a bar (**override-normalized** via
      `FindBaseSpellByID`, so a placed base and its talented replacement count as
      one), drop passives / `FutureSpell` / `Flyout` / `PetAction`, and place the
      remainder onto a reserved free-slot region with a log of each `name (spellID)`.
      No keybinds — the value is *visibility*. Triple payoff: (a) **live QA of the
      seed** — an important ability landing in spillover is a seed miss; (b) surfaces
      useful-but-non-rotational utility the buckets don't cover; (c) **subsumes
      hand-encoding build-specific abilities** — spillover catches
      `Tempest`/`Reaver's Glaive`/etc. per-character, so the seed stays
      build-agnostic. Combat-guarded; caps the region and reports overflow (listed,
      never dropped). Natural precursor to M4 (its bar is the tweak palette).
      *Shipped v0.3.0: `Dump.Spill` (`enumerateCastable` + `placedSpellSet` +
      `normID` override-collapse) + `/bb spill [clear]`. Reserve region = Action
      Bars 6–7, abs slots **145–168** (flagged `@verify-ingame` — the 133–180 range
      shifted across expansions; placement is empty-slots-only so a wrong base can't
      clobber real bars). Tracks the slots it filled in `BucketBindsDB.spillSlots`
      so re-runs are idempotent and never wipe abilities the player parked there.
      Also v0.3.0: JSON-authoritative pipeline, modifier-grouped 12-slot re-layout,
      `/bb dump --nobind` (place without rebinding), and `/bb test` (Recuperate →
      ALT-0 place+bind smoke test, `test clear` to revert).*
- [x] **M3.1 — `/bb diagnostics` (honest resolution + placement report).** The
      lead item of the "harden M1–M3" set. In-game the dump places most abilities
      but leaves *significant gaps*, with no way to see *why*. `/bb diagnostics`
      makes it concrete: for the **active spec** it classifies every seed bucket
      (`unresolved` = seed name a wrong string → **seed bug**; `resolved-known` =
      should place; `resolved-unknown` = untalented/not-learned, expected skip;
      `placeholder` = M5 item/macro), reads the live bars back to flag which
      `resolved-known` abilities didn't actually land (`empty`/`wrong-type`/
      `wrong-spell`, normID-compared), and lists castable abilities **no bucket
      covers** ("the gaps"). Crux: an id from `C_Spell.GetSpellInfo` does *not*
      imply castable — spellbook membership (by name AND `normID`) is the primary
      "known" signal (handles talented overrides), `IsPlayerSpell`/`IsSpellKnown`
      corroborate. **READ-ONLY** (no `PlaceAction`/`SetBinding` → no combat guard).
      Addons can only persist via SavedVariables, so it writes into account-level
      `BucketBindsDB.diagnostics[<char>][<spec>]` — runs **accumulate** across
      specs and characters (merge, never wipe); the user `/reload`s to flush and a
      Python reader parses it off the WSL mount.
      *Shipped v0.4.0: `Dump.Diagnostics(opts)` (reuses the file-local
      `buildSpellbookMap`/`resolveSpellID`/`enumerateCastable`/`normID`/`BAR_MAP`/
      `PLACEHOLDER`/`FORM_BONUS_BARS`/`normKey`/`ResolveSpec` upvalues — zero
      refactor) + `/bb diagnostics [clear]` + `wowkb.diagnostics` reader
      (`uv run python -m wowkb.diagnostics [--character N] [--spec N] [--json]`,
      reuses `charstate.parse_savedvar` + `DEFAULT_WOW`). Batched the
      combat-key-swap seed/Data.lua/spec release in the same v0.4.0 tag.*
      **✅ Verified in-game 2026-07-16** (Encomplete Warlock: Affliction/Demonology;
      Uncomplete DH: Devourer/Havoc/Vengeance — 5 reports across 2 characters in
      one `BucketBinds.lua`). Confirmed: accumulate across specs+characters,
      **merge-not-wipe** (re-running one spec refreshed only that slot, stalest-hint
      correct), reader render + `--character`/`--spec`/`--json`, and the QERF
      combat-key swap landed. **Placement path is solid** — Havoc 19/19 · Vengeance
      21/21 · Devourer 18/18 with **0** placement issues *when the spec is actually
      dumped first*. The original "significant gaps" complaint **did not reproduce**:
      the big mismatch counts on the first pass were **un-dumped specs** (bars showing
      their Blizzard-default layout), not a dump bug — a `/bb dump` immediately before
      `/bb diagnostics` is required for the placement read-back to be meaningful.
- [ ] **M3.2 — diagnostics classifier hardening + seed-name triage** (from the
      2026-07-16 pass — the follow-ups that pass surfaced):
      - **`unresolved` over-reports — the plan's premise was wrong.** `C_Spell.GetSpellInfo(name)`
        is **knowledge-gated in 12.0.7**: it returns nil for names the character
        hasn't learned/talented, so it is **not** the universal name→id lookup M3.1
        assumed ("id == nil ⇒ seed typo"). Proof from the pass: *Vengeful Retreat*,
        *Consume Magic*, *Curse of Exhaustion* each **resolve in one spec but read
        `unresolved` in a sibling spec** on the same/like character. Effect:
        untalented abilities are misfiled as `unresolved` ("seed bug") instead of
        `resolved-unknown` ("expected skip"). **Fix:** add a client-wide name→id
        fallback (e.g. a wago `SpellName` map shipped in Data.lua, or a broader API
        call) so `unresolved` means *only* "no such spell name," and downgrade the
        knowledge-gated cases to `resolved-unknown`.
      - **Genuine seed-name fixes to triage** (real, not knowledge-gating):
        - ✅ **FIXED 2026-07-16** (seed JSON, confirmed vs live castable IDs):
          `Implosion/Power Siphon` → **`Implosion`** (Demo Combat 5 — the compound
          collapsed to the core spell); `Blight of Weakness` → **`Blight of Tongues`**
          (**1271802**, all three Warlock Class-4 slots — Midnight rename);
          warlock `Interrupt` `Spell Lock` → **`Command Demon`** (Affl + Destro; Demo
          already had it) — casts the active demon's interrupt (Spell Lock/Axe Toss),
          so the interrupt slot finally resolves for all 3 warlock specs.
        - Still open: `Soul Carver` (DH/Veng — now `Cooldown 3`).
          ~~`Summon Doomguard`~~ — **DISPROVEN 2026-07-21.** The name is live in
          12.0.7 as spell **1276672** (the Demonology talent; confirmed against
          `raw/wago/SpellName-12.0.7.68256.csv`). It was never a seed bug — it's
          the knowledge-gating over-report below, and resolves once talented.
          The only two names that still fail a `check_seed_spells.py` run are the
          documented-benign `Poisons` (Rogue) and `Res` (Monk/MW).
          NOTE several first-suspected "misses" (`Soul Carver`, `Essence Break`,
          `Vengeful Retreat`, `Consume Magic`, `Curse of Exhaustion`) are actually
          the **knowledge-gating over-report above**, not seed bugs — they resolve
          once talented. `Spell Lock` (Affl Interrupt) was the **Felhunter pet**
          ability with **no player spell** — now resolved by switching the warlock
          `Interrupt` seed value to **`Command Demon`** (a player spell that fires
          the demon's interrupt); also generally reachable since the contextual-bar
          work binds the whole pet bar to `ALT+1..8`.
          Model the **DH PvP-talent** slots (`Rain from Above`, `Illidan's Grasp`,
          `Reverse Magic`) like the M5 placeholders. Fix real typos via `Dump.lua`
          `ALIASES` + the seed JSON; refresh `check_seed_spells.py` findings.
      - **Coverage gap surfaced:** `Lighthook Grapple` (**1287466**, Midnight DH) is
        castable-and-unmapped — deferred (added to `exclude_spells` for now; it's a
        cross-class ability already default-bound, so it's noise on spill/ring).
- [ ] **M4 — console + seed round-trip** (re-scoped 2026-07-17 from "in-addon
      tweak UI"). The "then tweak" half of the pitch — but WoW already gives you
      native drag-drop on the real bars (+ Edit Mode), so M4 **drops the WYSIWYG
      slot editor** (don't reinvent the game's own UI) and instead ships a console
      for driving BB comfortably plus a loop that feeds in-game tweaks back to the
      seed. **Two independent halves** so the cheap win isn't gated on the harder one.
      - [x] **M4a — schema-driven console** (shipped v0.9.0, 2026-07-17). A
        movable/resizable in-game window
        toggled by `/bb` (no args) or `/bb console`, running the existing `/bb`
        command surface with real scrollback + a rich input — the fix for the pain
        of driving BB from the tiny chat frame.
        - **Addon-driven, not chat-skinning.** Own `Frame` + a `ScrollingMessageFrame`
          for output (the same widget class the chat frame is built from, but our
          own instance/content) + an `EditBox` for input. Movable = the standard
          `SetMovable`/`RegisterForDrag`/`StartMoving` boilerplate; resizable adds a
          grip + `SetResizeBounds`.
        - **Two enabling refactors (wanted anyway):** (1) route `say()`/`print`
          through an **output sink** — append to the console when open, optionally
          still echo to chat; (2) extract the slash handler into `BB.Dispatch(args)`
          shared by `SlashCmdList` and the EditBox.
        - **Unprotected.** Pure UI — **zero secure/protected surface** (unlike the
          dump's `PlaceAction`/`SetBinding`); ~150–250 lines of standard Lua. A
          command the console runs (`/bb dump`) still hits its existing combat guards
          — no regression.
        - **Schema-driven input — the spine.** Define commands **once** as
          `{ name, args, flags, desc, complete = fn }`; the hint line, autocomplete
          dropdown, tab-complete, tooltips, `/bb help`, and "did you mean?" all derive
          from that single table, so every new `/bb` command lights up all affordances
          for free. This schema is the thing to design first.
        - **Affordance tiers:**
          - *Easy (ship):* live **syntax hint line** (on `OnTextChanged`),
            **autocomplete dropdown** (matches + one-liners), **tab-complete**,
            **context arg completion** (spec names after `dump`, `clear` after
            `macros`), **`GameTooltip` help** on hover, **"did you mean?"** on unknown
            commands (prefix/fuzzy). EditBox `SetHistoryLines` gives ↑/↓ command
            history nearly free.
          - *Fiddly (later):* fish-style **ghost-text autosuggestion** (overlay a grey
            FontString sized to caret x), **arrow-key dropdown nav** (disambiguate vs.
            history when the box is empty), **fuzzy ranking**, **aligned scrollback
            tables**.
          - *Skip:* per-token **syntax coloring inside the editable input** — a live
            EditBox can't render mixed colors mid-edit (would need a custom text
            engine); colorize the **echoed** command in the scrollback instead (free).
        - **One asset:** bundle a monospace `.ttf` (WoW ships none) for aligned
          tables. References to crib from: BugSack, ViragDevTool / DevTool, TinyPad;
          the game's own `` ` `` dev console.
        - **Shipped (v0.9.0):** `Output.lua` (`ns.Emit` sink; every module's
          `say`/`print` routes through it), `Core.lua` `ns.Commands` schema +
          `ns.Dispatch` + `ns.SuggestCommand` (prefix→Levenshtein-≤2 "did you
          mean?") + schema-generated `cmdHelp`, and `Console.lua` (movable/
          resizable terminal frame, `ScrollingMessageFrame` scrollback, `EditBox`
          with ↑/↓ history, live hint line, autocomplete dropdown + GameTooltip,
          tab-complete with arg-cycling). Bundled font is **JetBrains Mono**
          under **OFL-1.1** (`Media/JetBrainsMono.ttf` + `-OFL.txt`; the plan's
          "Apache-2.0" was the pre-v2.304 license). Easy-tier only — Fiddly tier
          (ghost text, arrow-key dropdown nav, fuzzy ranking, aligned tables) and
          per-token in-input coloring stay deferred; the echoed command is
          colorized in scrollback instead.
      - [ ] **M4b — `/bb diff` → seed round-trip** (replaces "save as profile").
        Push in-game ability moves back to the **canonical seed**, not a throwaway
        per-character profile — the "grows through use" doctrine applied to the seed
        (which still carries Bellular's known classification errors).
        - **Decision — the layout is fixed.** The `buckets` table
          (category→bar/slot/keybind) is **canonical and never edited** by the
          round-trip. The only thing the loop writes is the **ability→category**
          assignment: `specs[key][category]` (+ the racial/buff/item category data).
          Fixing the layout **eliminates** the earlier "universal-layout change vs.
          spec change?" ambiguity — it's *always* a spec-map edit.
        - **Approach — reconstruct-and-diff (not move-tracking).** Read the live bars
          (diagnostics already does), run each occupied slot through the **fixed**
          slot→bucket→category map (`BAR_MAP` + `buckets`), yielding a proposed
          `specs[currentSpec]` map straight from your bars; **diff** it against the
          seed's. Changed categories are the edits — handles swaps, moves-to-empty,
          and adds in one pass. Found → **rebind** (moved category); not in the seed
          → **bind** (add) at the new category.
        - **Scope-by-search (the "class / race / universal" question).** For each
          changed ability, search the seed to classify how wide the edit is: appears
          in **all specs of the class** → class ability (offer to update all N); **only
          this spec** → spec-specific; matches a **racial** → race scope; a
          **consumable/mount** → universal. The search *determines* the scope — no
          human classifier needed for the common cases.
        - **The one residual choice:** moving a **class-shared** ability = this-spec-
          only vs. all-class-specs. Default **this-spec-only** (you were rearranging
          one spec); the `wowkb` reader **flags class-shared moves for confirmation**
          rather than silently fanning out. Racials/universals are unambiguous.
        - **Rails it reuses:** `/bb diff` = diagnostics' bar read-back + the seed
          compare; writes proposals to `BucketBindsDB` (same SavedVariables→Python
          bridge as `/bb diagnostics`); a `wowkb` reader emits into the existing
          `data/seed-edits-proposed.md`; review + `gen_data_lua.py`; shipping the
          regenerated `Data.lua` closes the loop.
        - **Wrinkles to remember:** the live bar gives a **spellID**, the seed stores
          a **name** → the reader resolves ID→name (BB does both ways). An untalented/
          unloaded ability isn't on the bar, so the diff only ever reflects what you
          currently have — it **never removes** seed entries, only rebinds/adds what
          it sees, so the seed self-corrects **incrementally** across the specs/talents
          you actually play.
        - A local snapshot/profile survives as a lightweight fallback — M1's
          `/bb save` already is one.
- [x] **M5 — items/macros.** Auto-generate potion/trinket/racial macros from the
      Items table; respect the macro caps.
      - **Phase A** (released inside v0.9.0) (`Macros.lua`: `FocusBody`/`InterruptBody`
        body builders, cap-aware `upsert` returning the index, `placeMacro`,
        `Apply` (called from the `Dump.Run` post-pass) + `RunStandalone`/`Clear`;
        `Dump.FormOffsets`; `/bb macros [Spec]` + `/bb macros clear`). Delivers
        exactly the hand-picked roster below: `BBfocus` (account) → key 5
        (**v2: `CTRL-Q`**), `BBintr` (per-char, per-spec) → V (unchanged in v2),
        idempotent, combat-guarded, reverted
        by `/bb undo`. Hazard-1 fix: `Apply` nils `bar1IDs[12]` so `onShapeshift`
        can't re-place the raw interrupt over the macro on form entry. Test-probe
        slot moved 37→48 to free key 5's button.
      - **Phase B** (released inside v0.9.0) — the rest of the utility/prep band.
        ⚠ **The keys below are the v1 assignments this milestone shipped with.**
        LAYOUT v2 (v0.10.0) re-keyed every one of them — see "The layout" above for
        the current map. v1 → v2: focus `5`→`CTRL-Q`, `BBhp` `ALT-Q`→`5`,
        `BBmana` `ALT-E`→`ALT-R`, `BBdmg` `ALT-R`→`0`, `BBtrinket` `6`→`8`,
        `BBracial` `7`→`9`, `BBflask` `8`→`ALT-Q`, `BBbuff` `9`→`ALT-E`:
        - `gen_data_lua.py` emits two new generated tables into `Data.lua`:
          `ns.SEED.items` (potions/flasks/oils grouped into `{q2,q1}` ID pairs) and
          `ns.SEED.specBuffs` (per-spec buff spell list, pre-resolved in Python from
          the seed `buffs` fuzzy `Spec` strings — `Poisons Macro` → `Instant Poison`).
        - **Fall-through consumables** (`Macros.ConsumableBody`): `#showtooltip` +
          `/use item:<id>` for **every** ID in a group (Q2 higher-rank first), so
          whichever potion the player carries fires. `BBhp` (+`/use Healthstone`
          prefix) → Alt+Q, `BBmana` → Alt+E, `BBdmg` → Alt+R (bar-4 slots 1–3, Alt
          keys pre-bound by the dump), `BBflask` → key **8** (bar-5). 255-char cap
          guarded (drop-tail + warn).
        - **`BBtrinket`** (`/use 13`+`/use 14`) → key **6**; **`BBracial`** (per-char,
          from a hardcoded `RACIALS` race→spell table, `@verify-ingame`) → key **7**;
          **`BBbuff`** (per-char, from `specBuffs[seedKey]`) → key **9**. Racial/buff
          skip gracefully (reported) on an unmapped race / a spec with no buff row.
        - `Macros.HANDLED_CATEGORIES` drops the five handled buckets from `Dump.Run`'s
          `skipped (M5)` report; item/prep counts fold into the dump + `/bb macros`
          reports. `Macros.Clear` deletes the seven new `BB*` macros, clears their
          slots, and unbinds keys `6/7/8/9` (Alt item keys left to the dump layout).
        - **Documented gaps:** Oils (`ns.SEED.items.Oils`, catalogued) + food not
          auto-wired; "Another Combat Item If Needed" (no seed mapping) + Mount
          (deferred to OPie M6) stay placeholders.
      - **Hand-picked utility-macro roster (2026-07-16 request) — Phase A, done:**
        - **Set focus** — `/focus` (static, universal). Home: key **`5`** (v1) /
          **`CTRL-Q`** (v2). ⚠ under v2, key `5` is the Healthstone macro and still
          collides with the `ExtraActionButton` bind (`bonus_binds`) — rehome that.
        - **Focus interrupt → REPLACES the `Interrupt` bucket.** Every spec's `V`
          becomes a smart interrupt instead of the raw spell. Per-spec macro
          generated from the seed's `Interrupt` value:
          `#showtooltip <Interrupt>` / `/cast [@focus,harm,nodead][] <Interrupt>`
          — fires on focus if it's a live enemy, else current target.
        - **Warlock variant** (same slot): the seed's warlock `Interrupt` is now
          **`Command Demon`** (all 3 specs; was the unresolvable `Spell Lock`) — so
          the generated macro is `/cast [@focus,harm,nodead][] Command Demon`, which
          casts the active demon's interrupt (Spell Lock on Felhunter, Axe Toss on
          Felguard). ⚠ `@focus` redirect on Command Demon is `@verify-ingame`; and
          it only interrupts when an interrupt-capable demon is out (Imp/Succubus/
          Voidwalker → their utility instead).
        - *(Dropped: the generic `/click PetActionButton<N>` pet-ability macros —
          an overshoot; Command Demon covers the warlock case natively.)*
      - Building these needs the M5 macro engine (`CreateMacro`/`EditMacro` +
        place + cap budget). The **raw-spell** step is already done: warlock's
        interrupt slot now resolves to Command Demon today (pre-macro).
- [~] **M6 — OPie integration.** Push out-of-combat sprawl onto OPie radial rings
      instead of keys. Design + API research in `opie-automation-research.md`
      (companion vs built-in resolved: the only *dynamic* ring is intrinsically a
      BucketBinds concept, so it lives in-addon behind `## OptionalDeps: OPie`).
      - [x] **`/bb ring` (overflow ring)** — shipped v0.5.0. Reuses the `/bb spill`
        computation (castable − on-a-bar − `excludeSpells`), then hands the set to
        OPie via `OPie.CustomRings:SetExternalRing("BB_Overflow", desc)` (runtime,
        addon-owned; deterministic `_u="s"..baseID` tokens → idempotent rebuild).
        No-ops without OPie. Slices are bare `{id=<spellID>}` — flagged
        `@verify-ingame` (confirm bare-id slices resolve; else switch to macrotext).
        New seed table **`exclude_spells`** (keyed by id and/or name) filters BOTH
        `/bb spill` and `/bb ring` — the "inventory of noise" (Auto Attack, Shoot,
        Glide, Revive Battle Pets, Mobile Banking, Lighthook Grapple). Warlock-niche
        utility (Eye of Kilrogg, Ritual of Doom/Summoning, Subjugate Demon) and
        **all hunter pet control** deliberately kept — the ring is *for* "random
        stuff not worth a keybind."
      - [ ] **Static hearth/travel + marker rings** — handcraft in OPie once (mounts
        collapse to `Summon Random Favorite Mount`; markers are OPie built-ins), or
        seed + `AddDefaultRing` later. No dynamic collection scan needed (v2 in the
        research note is deferred — the built-ins cover the common case).
- [ ] **M7 — per-dungeon interrupt-focus macros** (reuses the M5 macro engine).
      *"About to pull → mash one key → focus jumps to the highest-priority interrupt
      caster present in the pack,"* so you don't have to remember each dungeon's
      priority casters. Data-driven from the M+ KB, generated like every other seed
      table. (Requested 2026-07-17.)
      - **The macro mechanic (load-bearing — get this exactly right):** chained
        bare `/focus <Name>` lines. Macros **never abort** mid-body; a name **miss
        is a silent no-op** (focus unchanged); a **hit overwrites** focus → so **the
        last matching line wins**. Therefore emit names in **reverse priority order**
        (least-important first, top priority last) so the highest-priority mob that's
        actually present is applied last and wins. **No quotes** — the whole argument
        is the name; multi-word is fine. There is **no `/focusexact`**: `/focus name`
        is a partial/nearest match (fine for distinctive M+ mob names); the exact-but-
        janky fallback (`/targetexact N` → `/focus` → `/targetlasttarget`) is only
        worth it on a real partial-name collision.
      - **Environmental requirement (`@verify-ingame`):** `/focus name` only resolves
        a unit the client already knows (nameplate up / in range / LoS). Needs **enemy
        nameplates always-on** and the pack loaded — fire it a few yards out. Out of
        sight → no-op.
      - **One key, addon-swapped body (recommended UX):** a macro can't branch on
        dungeon (no dungeon conditional), so instead of N per-dungeon keys, keep a
        single `BBfoc` macro whose body the addon **rewrites on zone-in**
        (`PLAYER_ENTERING_WORLD` / `ZONE_CHANGED_NEW_AREA` → resolve the current
        `GetInstanceInfo()` / map ID → `EditMacro` the dungeon's reverse-priority
        list). `EditMacro` is protected, but zone-in is out of combat → safe; guard
        with `InCombatLockdown` / `QueueAction` like the rest of the engine. Fall back
        to a bare `/focus [@mouseover,harm]` outside known dungeons. Alternative: N
        account macros (`BBfoc_<dungeon>`) surfaced on an OPie ring (folds into M6).
      - **Data source:** a new **generated** table (`ns.SEED.mplusFocus` or a sibling
        data file) keyed by dungeon → ordered interrupt-priority mob-name list,
        sourced from `knowledge/systems/mechanic-archetypes.md` + the `mplus_memory`
        per-dungeon files. **Do not hardcode 12.0.7 mob names in the addon**
        (staleness doctrine) — pull from the KB and regen via the gen pipeline,
        `--check`-gated like `Data.lua`. Names need to match the in-game unit name
        exactly-enough for a partial match; `@verify-ingame` per dungeon.
      - **Scope + budget:** account-wide (mob names are identical for everyone),
        `BB`-prefixed, idempotent upsert. Single-macro design costs **1** account
        macro; the per-dungeon fan-out costs ~8 (Midnight S1) — both trivial under
        the 120 cap. Reuse `ConsumableBody`'s 255-char drop-tail guard (3–4 names +
        `#showtooltip` ≈ 120 chars, safe; a long list could crowd it).
      - **Out of scope — the impossible version:** auto-detecting *which* mob is
        currently casting and focusing it. Target selection by live cast state is
        secure/protected in combat — no addon can do it. Best achievable is a
        nameplate cast-bar highlighter (Plater / OmniCD-style, "who to hover") + this
        priority-focus button. Documented so future-me doesn't chase the wall.

## M1 plan — snapshot / restore (target release v0.1.0)

Capture the full keybind + action-bar + macro state to a named profile and
restore it safely with an auto-backup. Taxonomy-independent; also builds the
write-bars plumbing M2 needs.

### Three subsystems

| Layer | Read | Write | Note |
|---|---|---|---|
| Keybindings | `GetNumBindings()`/`GetBinding(i)` → key→command; `GetCurrentBindingSet()` (account/char) | `SetBinding` → `SaveBindings(set)` | must `SaveBindings` or lost on relog |
| Action slots | `GetActionInfo(slot)` for **slots 1–180** → `{type,id}` | pickup (`C_Spell.PickupSpell`/item/macro) → `PlaceAction(slot)` | protected in combat; 1–180 already covers stance/skyriding bars |
| Macros | `GetNumMacros()`, `GetMacroInfo(i)` → name/icon/body/scope | `CreateMacro`/`EditMacro` | index unstable → slots reference macros **by name** |

### Restore ordering (safe, not truly atomic)

1. **Combat guard** — `InCombatLockdown()` → refuse + queue to `PLAYER_REGEN_ENABLED`.
2. **Auto-backup** current state into a single `__prerestore` slot → `/bb undo`
   (single level; no undo stack).
3. Apply in dependency order: **macros first** (build name→index map) →
   **action slots** (resolve macro slots via map; skip unknown spells) →
   **bindings** (apply map, then `SaveBindings`).
4. **Report** counts + anything skipped; never fail silently.

### Settled decisions

- **Bindings = exact mirror** (clear all, apply saved). **Macros = additive**
  (create/update saved; don't delete the user's other macros) with an opt-in
  `exact` mode.
- **Stance/skyriding bars**: captured by full 1–180 enumeration — no deferral,
  no shapeshifting. (Per-form *targeting* is M2, see risks.)
- **`/bb undo`**: single-level restore of `__prerestore`.

### Files (in the michac/BucketBinds repo)

- `Snapshot.lua` (new) — `Capture()→table`, `Apply(profile,opts)`; split
  `{capture,apply}{Bindings,Actions,Macros}`; combat queue.
- `Core.lua` — add `/bb save|restore|list|delete|undo`.
- `BucketBinds.toc` — load `Snapshot.lua` before `Core.lua`; bump `## Version: 0.1.0`.

### SavedVariables shape

```lua
profiles["<name>"] = {
  meta     = { created, char="Name-Realm", class, specID, bindingSet=1|2 },
  bindings = { {key="SHIFT-1", command="ACTIONBUTTON9"}, ... },
  actions  = { [slot] = {type="spell|item|macro|mount|...", id=, name=, body=, icon=} },
  macros   = { {name, body, icon, scope="account|char"}, ... },
}
-- plus BucketBindsDB.autobackup = <the __prerestore snapshot>
```

### Verification

luaparser syntax gate + an in-game smoke protocol (documented in the addon's
`CLAUDE.md`): save → rebind a key & move an action → restore → confirm revert;
`/bb undo`; combat-lockdown deferral; Druid Cat/Bear bar round-trip.

## Open technical questions / risks

- **Spell-ID resolution (the one real engineering piece).** The seed carries
  ability *names*, `PlaceAction` needs the spellbook entry. Resolve name→ID at
  apply-time from the player's spellbook; cross-check offline against wago DB2
  (this repo already pulls wago). Names drift with patches — needs a fuzzy/alias
  fallback and a "couldn't place N abilities" report rather than silent gaps.
- **Combat lockdown.** Can't change bindings or move actions in combat. Guard
  everything behind `InCombatLockdown()`; queue to `PLAYER_REGEN_ENABLED`.
- **Macro caps.** 120 account + 18 per-char. Auto-generated @cursor/item macros
  eat into this — M2/M5 need a budget and a graceful "out of macro slots" path.
- **Bonus-bar slot numbering.** Druid forms / Rogue stealth / Warrior stances /
  skyriding page the *visible* bar to a bonus bar — but the underlying slots are
  fixed absolute IDs, so `GetActionInfo`/`PlaceAction` reach them regardless of
  current form (you can write the Cat bar while in Bear form). The bonus bars sit
  at computable ranges:

  ```
  firstSlot = 1 + (NUM_ACTIONBAR_PAGES + bonusOffset − 1) × 12   -- pages=6, buttons=12
    offset 1 → 73–84    offset 2 → 85–96    offset 3 → 97–108
    offset 4 → 109–120  offset 5 → 121–132 (skyriding)
  ```

  Consequence: **M1 capture is complete by enumerating slots 1–180** — form bars
  come along for free, no shapeshifting needed. What's genuinely fiddly is
  *labeling*: which `bonusOffset` each form/stance/stealth uses is a per-class
  table the API doesn't hand you by name, and some forms re-page the base bar
  instead of taking a bonus bar. That table is load-bearing for **M2** (a Feral's
  abilities must land on the Cat slots or they won't show in Cat form) — it's a
  bounded, formula-backed chunk of the dumper, **not** an M1 concern.
  Refs: [Wowpedia API_GetBonusBarOffset](https://wowpedia.fandom.com/wiki/API_GetBonusBarOffset).
- **Bar addon assumptions — DECIDED (2026-07-10): direct modifier binds on
  all-visible stock bars, no paging.** The seed stores an explicit keybind string
  per `(bar, slot)` (`1`, `S1`=Shift+1, `C1`=Ctrl+1…), so each combo maps **1:1**
  to one fixed absolute action slot via `SetBinding(key, <SLOT_COMMAND>)` — no
  paging addon, nothing hidden, every bar clickable and showing its own cooldown
  swipe. Rationale: placement (where an ability lives / whether it's visible) is
  independent of binding (what key fires it); paging bundles them only by
  convention. Modifier paging's *only* wins are screen-declutter and stock-bar
  setup speed — but it costs click-ability and at-a-glance cooldowns, and the
  seed already carries per-combo keys that direct binding consumes WYSIWYG (every
  combo always points at the same slot — simpler to reason about than paged
  swaps). Cooldown-tracking at the high end is done off-bar anyway (WeakAuras /
  Cooldown Manager as "front end", bars as "back end"), so hiding bars buys
  little. **Paging is a deferred opt-in "compact mode", not the M2 default.**
  Refs: [wowinterface Paging](https://www.wowinterface.com/downloads/info18229-Paging.html),
  [Blizzard: tracked bars w/o WeakAuras](https://us.forums.blizzard.com/en/wow/t/feedback-action-bars-tracked-bars-and-unit-frame-options-after-playing-without-weakauras/2203580).
- **Naming.** Addon is provisionally `BucketBinds` — easily renamed; not final.

## Layout

The seed pipeline + this doc live in **`wow`** (this workspace). The
**addon is its own git repo** (`michac/BucketBinds`), checked out at
`addon/` but gitignored here — mirroring how `planner-state/`
(michac/wow-planner-state) is handled. `gen_data_lua.py` writes the generated
`Data.lua` across that boundary into the addon repo's working tree; you then
commit + cut a **GitHub Release** there so `ghaddons` can install/update it. See
`addon/CLAUDE.md` for the release workflow (a plain push does **not** reach the
game).

```
projects/keybinder/                    ── tracked by wow ──
  project-spec.md                     this doc
  data/
    bellular-keybinds.seed.json       CANONICAL seed (hand-edited, diffable)
    seed-notes.md                     provenance + notation legend
    seed-review.md                    per-spec placement audit (findings)
    seed-edits-proposed.md            Tier-A/B correction list
    unmapped-abilities.md             inventory of unbound abilities
    layout-v2-proposal.md             layout v2: §2/§3 SHIPPED (v0.10.0), §6 floats SHIPPED (v0.12.0, healers held §10)
  tool/
    gen_data_lua.py                   seed.json → Data.lua (the live step; writes ↓)
    extract_seed.py                   ARCHIVAL: frozen .xlsx → side file only

  addon/            ── separate repo michac/BucketBinds; gitignored here ──
    CLAUDE.md                         addon-repo instructions + release flow
    README.md
    BucketBinds/
      BucketBinds.toc
      Core.lua                        slash cmds, namespace, load, ns.Dispatch
      Data.lua                        GENERATED — the seed as a Lua table
      Snapshot.lua                    (M1) save/restore
      Dump.lua                        (M2) seed → bars; (M3) spill + ring;
                                      (M3.1) diagnostics; /bb test
      Macros.lua                      (M5) generated macros (focus/interrupt/items/prep)
      Output.lua                      (M4a) ns.Emit output sink
      Console.lua                     (M4a) in-game console window
      Media/JetBrainsMono.ttf         (M4a) bundled console font (OFL-1.1)
```

**Shipped-version signal is `gh release list --repo michac/BucketBinds`, not local
`git tag`** — releases are cut server-side, so local tags stop at v0.3.2.
