# BucketBinds — a one-shot keybind/bar dumper for WoW

**Status: M3.1 shipped + verified in-game (`/bb diagnostics`, v0.4.0) on top of M3
(spillover) + M2 (dumper) + M1 (snapshot/restore). Seed is JSON-authoritative
(xlsx frozen to archive), bars re-laid-out to a modifier-grouped 12-slot scheme
with the 2026-07-16 combat-key swap (`Q E R F` / number row), `/bb dump --nobind`
+ `/bb test` added, and `/bb diagnostics` gives an honest read-only resolution +
placement report (read off disk by `wowkb.diagnostics`). The 2026-07-16 in-game
pass confirmed the dump/placement path is solid and surfaced two follow-ups →
**M3.2** (classifier over-reports `unresolved` because `GetSpellInfo` is
knowledge-gated; + a seed-name triage list). M3.2 or M4 (in-addon tweak UI) next.
2026-07-16. **Also 2026-07-16: mouse relocate** — the movement + personal-defensive
family moved off `Z`/`X` onto the three mouse buttons (`M4`/`M5`/`M3` + Shift
variants), freeing those keys; `normKey` gained mouse + Shift-mousewheel tokens
and the dump now vacates stale keys on relocated slots (see "Mouse relocate" under
The layout). Autorun dropped from middle-mouse. **And v0.5.0: M6 OPie start** —
`/bb ring` builds an OPie overflow ring from the `/bb spill` set via
`SetExternalRing`, gated on `## OptionalDeps: OPie`; new `exclude_spells` seed
table filters noise out of both spill and the ring; two seed misses fixed
(`Implosion`, `Blight of Tongues`). All bundled into **v0.5.0 — committed +
released.** **Then v0.6.0 (WIP, uncommitted): contextual bar** — `ALT+1..8` now
binds the pet bar (`BONUSACTIONBUTTON`) or stance bar (`SHAPESHIFTBUTTON`) per
class (runtime-detected at dump); reclaims the keyless Trinket/Racial/Free
`A1..A4` slots. **Needs in-game verify + a v0.6.0 release.**

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

## The layout (decoded from the seed)

**Re-layout 2026-07-14: one modifier layer per physical bar, 12 slots each.**
Each stock MultiBar has 12 buttons; the seed now fills all 12 rather than 8, so
the four modifier layers pack onto four bars and **bar 5 is freed**:

| Bar (modifier) | Slots 1–8            | Slots 9–12         | Buckets                                     |
|----------------|----------------------|--------------------|---------------------------------------------|
| 1 unmod        | `Q E R F 1 2 3 4`    | `· · C V`          | Combat 1–8 + CC/Interrupt (slots 9–10 → bar 5) |
| 2 Shift        | `SQ SE SR SF · S2 S3 S4` | `· · SC SV`    | Combat 9–12, Class 2–4 + CC2/Slow (slots 5,9,10 → bar 5) |
| 3 Ctrl         | `CQ CE CR CF C1..C4` | `CZ CX · CV`       | Self-heals, purge/dispel/raid-def/lust + buff/res/taunt (slot 11 → bar 5) |
| 4 Alt          | `AQ AE AR AF` + `1–8`† | `AZ AX AC AV`      | item macros (M5 ✓) + **ALT+1–8 = pet/stance bar**† + PvP 1–3, Mount |
| 5 free         | `5 8 9 · M4 M5 M3 SM4 SM5` | `SM3`         | **prep band** (M5 ✓): focus→5, flask→8, buff→9 · **relocated mouse cluster** (movement/defensive/immune, buttons 4–9)‡ |

‡ **Mouse cluster on bar 5 (2026-07-17):** the movement/personal-defensive/immune
family is fired by the mouse buttons, so it lives on the free bar 5 (buttons 4–9)
rather than polluting the `<mod>+keyboard` keyset of bars 1–3. See "Mouse relocate"
below. This is why bars 1/2/3 show freed (`·`) slots.

† `ALT+1–8` no longer fires bar-4 slots 5–8 — it's bound to the **contextual bar**
(pet or stance, per class, at dump time; see "Contextual bar" below). The old
`A1..A4` Trinket/Racial/Free buckets are now keyless placeholders — **M5 Phase B
rebinds Trinket → key `6` and Racial → key `7`** (their bar-4 slots 5–6), leaving
Free (slots 7–8) unbound.

**Combat-key swap (2026-07-16):** within slots 1–8, the letter cluster `Q E R F`
now drives **Combat 1–4** (the most-spammed abilities) and the number row `1 2 3 4`
drives Combat 5–8 — swapped from the original `1 2 3 4 / Q E R F` because QERF are
faster to hit under pressure. The `Z X C V` utility cluster (Def1/Move/CC/**Interrupt
on V**) is deliberately untouched. Applied identically across all four modifier bars
so a physical key maps to the same slot-position on every layer.

Consequences: the singles (`Z X C V` + Shift/Ctrl variants) join their modifier's
bar instead of being scattered, and the bar-1 form-mirror covers the unmod slots
that remain on bar 1 (druids/rogues get interrupt + CC on their form bars too).

**Mouse relocate (2026-07-16, revised 2026-07-17):** the movement + personal-
defensive + immune family is fired by the **three mouse buttons** (+ Shift) —
strictly easier to hit while strafing.

The **first cut (2026-07-16)** only re-keyed these buckets to the mouse buttons
but left them on their bar-1/2/3 slots. That **broke the modifier-bar invariant**
("slot N = `<mod>` + the *same physical key* on every bar"): slot 9 became
`Mouse5 / Shift-Mouse5 / Ctrl-Z` across bars 1/2/3 — a keyboard/mouse mix.

The **fix (2026-07-17)** *moves* the six mouse-fired buckets onto the free **bar 5**
(buttons 4–9), keeping the mouse keybinds. Bars 1/2/3 revert to a clean
`<mod>+{Q E R F 1 2 3 4 Z X C V}` keyset, and the vacated keyboard keys free up.
Because bar 5 is form-static, the mouse button fires these in **every** form with
no form-mirror needed (an improvement over hosting Movement/Def-1 on the paging
bar 1).

| Combo | Bucket → **bar 5 slot** | Vacated (bar/slot) | Freed key |
|-------|--------------------------|--------------------|-----------|
| `M4`  (Mouse4)      | Movement Ability   → **s4** | bar 1 / 10 | `X`  |
| `M5`  (Mouse5)      | Personal Defensive 1 → **s5** | bar 1 / 9  | `Z`  |
| `M3`  (MMB)         | Class 1 (Movement) → **s6** | bar 2 / 5  | `S1` |
| `SM4` (Shift-Mouse4)| Movement Ability 2 → **s7** | bar 2 / 10 | `SX` |
| `SM5` (Shift-Mouse5)| Personal Defensive 2 → **s8** | bar 2 / 9  | `SZ` |
| `SM3` (Shift-MMB)   | Immune / Movement  → **s9** | bar 3 / 11 | `Ctrl+C` |

M4/M5 = thumb buttons (primaries), M3 = middle/scroll-click (tertiary). Ease
order honored: only unmodified + Shift, no Ctrl/Alt. Autorun (formerly unmod
middle-mouse) was dropped — it stays on the NumLock default. `normKey` also
learned `MU`/`MD` (Shift+mousewheel) tokens for future use — unmodified wheel
stays reserved for camera zoom. Bar 5 buttons 1–3 stay the macro prep band
(focus/flask/buff); the mouse cluster occupies buttons 4–9, so the two never
collide. ⚠ Relocation caveat: a *re-dump* repoints the mouse keys correctly
(`SetBinding` is authoritative per key), but a stale ability icon may linger on
the old bar-1/2/3 slot until `/bb undo` or a fresh restore — those slots are no
longer managed buckets, so the dump's clear pass skips them.

**Contextual bar → `ALT+1..8` (2026-07-16):** the `ALT`+number row now binds the
character's **pet bar** (`BONUSACTIONBUTTON1-8`) or **stance/form bar**
(`SHAPESHIFTBUTTON1-N`) — whichever that class uses, **detected at dump time**
(`GetNumShapeshiftForms() > 0` → stance; else a `PET_CLASS` → pet; else the row is
cleared/free). This is *dumper* logic, not a seed bucket: these are separate
binding namespaces the game auto-populates, so BucketBinds only binds them, never
places. It reclaims `ALT+1..4`, which were the (M5, not-yet-built) **Trinket /
Racial / Free** macro slots — those buckets are now **keyless** (`keybind: ""`,
bar-4 slots 5–8 retained). **M5 Phase B (v0.8.0) landed them:** the macro pass
binds Trinket → `6` and Racial → `7` on those very slots; Free (7–8) stays
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
worth comparing. Current seed: **52 buckets (48 placed + 4 stance), 40 specs,
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
- [x] **M2 — dumper.** Given class+spec, walk the seed's 40 placeable spell
      buckets, resolve each ability name→spellID at runtime, place it on the
      fixed `(bar, slot)` action slot, mirror the main bar onto form/stance
      bonus bars, and set the key→slot bind — one shot, combat-gated, with an
      auto-backup so `/bb undo` reverts it. The 12 `bar=None` buckets
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
        - Still open: `Soul Carver` (DH/Veng Combat 11), `Summon Doomguard` (Demo
          Combat 7 — legacy name, gone/renamed; needs wago `SpellName` research).
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
      tweak UI"). WoW already does drag-drop bar editing natively, so M4 drops the
      WYSIWYG editor and splits into **M4a — schema-driven console** (a movable
      in-game command window with live hints/autocomplete) and **M4b — `/bb diff`
      → seed** (push in-game ability moves back to the canonical seed). Detail below.
- [x] **M5 — items/macros.** Auto-generate potion/trinket/racial macros from the
      Items table; respect the macro caps. **Phase A shipped v0.7.0** (set-focus →
      5, smart focus-interrupt → V); **Phase B shipped v0.8.0** (fall-through
      potion/flask macros, trinket → 6, racial → 7, per-spec buff → 9). Documented
      gaps: Oils + food catalogued but not auto-wired; "Another Combat Item" +
      Mount (→ OPie M6) stay placeholders.
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
      - **Phase A shipped v0.7.0** (`Macros.lua`: `FocusBody`/`InterruptBody`
        body builders, cap-aware `upsert` returning the index, `placeMacro`,
        `Apply` (called from the `Dump.Run` post-pass) + `RunStandalone`/`Clear`;
        `Dump.FormOffsets`; `/bb macros [Spec]` + `/bb macros clear`). Delivers
        exactly the hand-picked roster below: `BBfocus` (account) → key 5,
        `BBintr` (per-char, per-spec) → V, idempotent, combat-guarded, reverted
        by `/bb undo`. Hazard-1 fix: `Apply` nils `bar1IDs[12]` so `onShapeshift`
        can't re-place the raw interrupt over the macro on form entry. Test-probe
        slot moved 37→48 to free key 5's button.
      - **Phase B shipped v0.8.0** — the rest of the utility/prep band:
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
        - **Set focus** — `/focus` (static, universal). Home: key **`5`**. ⚠ `5`
          is currently the `ExtraActionButton` bind (`bonus_binds`) — rehome that.
          Keys **`5`–`9`** become a new **utility / prep band** (casual + pre-pull).
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

The seed pipeline + this doc live in **`wwt-keyboard`** (this workspace). The
**addon is its own git repo** (`michac/BucketBinds`), checked out at
`addon/` but gitignored here — mirroring how `planner-state/`
(michac/wow-planner-state) is handled. `extract_seed.py` writes the generated
`Data.lua` across that boundary into the addon repo's working tree; you then
commit + cut a **GitHub Release** there so `ghaddons` can install/update it. See
`addon/CLAUDE.md` for the release workflow (a plain push does **not** reach the
game).

```
projects/keybinder/                    ── tracked by wwt-keyboard ──
  project-spec.md                     this doc
  data/
    bellular-keybinds.seed.json       CANONICAL seed (hand-edited, diffable)
    seed-notes.md                     provenance + notation legend
  tool/
    gen_data_lua.py                   seed.json → Data.lua (the live step; writes ↓)
    extract_seed.py                   ARCHIVAL: frozen .xlsx → side file only

  addon/            ── separate repo michac/BucketBinds; gitignored here ──
    CLAUDE.md                         addon-repo instructions + release flow
    README.md
    BucketBinds/
      BucketBinds.toc
      Core.lua                        slash cmds, namespace, load
      Data.lua                        GENERATED — the seed as a Lua table
      Snapshot.lua                    (M1) save/restore
      Dump.lua                        (M2) seed → bars
```
