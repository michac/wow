# Keybind hint on the CDM — execution plan

> ⚠ **Temporary working artifact, not a product authority.** Same status as the
> `simplification-*` / `rule-split-audit` migration artifacts beside it. It owns no gameplay
> opinion; it is
> the ordered brief for one feature. **Delete it when phase 5 exits** and the design lives in
> `spec.md` + `render-shelf.md`. Where this file and `authoring.md` or `spec.md` disagree,
> they win. Implementation status stays in `backlog.md` → `## Status`; this file is the route,
> not the record.

**What it is.** A key hint in the corner of each CDM row, so you know which icon is which
button — the thing EllesmereUI's CDM option provides and that this workspace has already mined
(`knowledge/addon-dev/cdm-rider-patterns.md` §11, re-grounded on shipped 12.1 source).

**What it is not.** Not a cue, not emphasis, not a badge. See *Decisions* below.

---

## Phase 0 — *(done 2026-08-19 — superseded)*

The lane → scan migration, which was never part of this feature: it was a **breakage** sitting in
front of it. The shelf had collapsed the four role lanes into one `tokens.ready` treatment and
`Style.lua` had been regenerated without `lanes`, while `Paint.lua`, `Treatment.lua`,
`Overlay.lua` and `StylePanel.lua` still read `ns.Style.lanes` — a nil index on the first row
paint. It landed as its own commit in the addon repo; `backlog.md` → `## Status` is the record.

**Everything below is unaffected and stands as written.** The only carry-over worth restating is
that `Catalog.TIERS` and every catalog's `band.tier` **stayed**: tiers are still the priority model
and still drive the "bands must not rise in priority" validation. Only the drawn treatment
collapsed.

## Phase 1 — `Binds.lua`, the data layer

New module, draws nothing. Public surface is one function: `ns.Binds.For(spellID) -> string|nil`.

- **Lookup order:** `C_Spell.GetBaseSpell(spellID)` first — it is the API's documented input,
  not a fallback — then the raw id. `C_ActionBar.FindSpellActionButtons` returns **nil, not an
  empty table**, when unslotted.
- **Slot → binding command:** `page = floor((slot-1)/12)+1`; pages 3/4/5/6/13/14/15 map to
  `MULTIACTIONBAR3/4/2/1/5/6/7BUTTON`, pages 1–2 and the bonus pages share `ACTIONBUTTON`.
  Then `GetBindingKey(cmd)` → `GetBindingText(key, 1)`.
- **Cache + debounce**, invalidated on `UPDATE_BINDINGS`, `ACTIONBAR_SLOT_CHANGED`,
  `ACTIONBAR_PAGE_CHANGED`, `UPDATE_BONUS_ACTIONBAR`, `UPDATE_OVERRIDE_ACTIONBAR`,
  `UPDATE_VEHICLE_ACTIONBAR`, `UPDATE_SHAPESHIFT_FORM`, `PET_BAR_UPDATE`,
  `PLAYER_SPECIALIZATION_CHANGED`, `PLAYER_ENTERING_WORLD`.
- **No combat fence.** The read chain is combat-safe and Blizzard itself runs it unguarded, so
  an out-of-combat-only rescan is a cost rule masquerading as a safety one — and one that
  blanks or stales the hint for the rest of a pull. Debounce; never defer to
  `PLAYER_REGEN_ENABLED`.
- **Unbound → nil → blank.** Never a placeholder: a fake keybind is worse than no keybind.

## Phase 2 — the shelf owns the look

- New `tokens.hotkey` in `render-shelf.md` Part 6: font, size, outline, rgb, alpha, anchor,
  offset. No number lives in the addon or the generator.
- `wowkb.capart` emits it as CSS variables and into `Style.lua`.
- The preview draws it, so placement is looked at rather than argued about. Badge slots 1–3 own
  the top-right corner, the top edge and the right edge, so **upper-left is the free corner**.

## Phase 3 — the draw

- `f.hotkey`, a FontString on **cap's own row frame** — never parented into Blizzard's pooled
  item frames. Those are recycled and re-bound (`OnCooldownIDSet`), which is what forces a
  re-parent-every-pass dance on riders that attach to them.
- One line in `Overlay.paint()`, beside the hatch and the badges.
- It inherits the existing refresh discipline for free. No new machinery, no new hooks.

## Phase 4 — gates and tests

- A busted spec for the slot → command arithmetic. Pure logic, no client (house rule 6).
- A `capart check` gate asserting the hint is not in the cue vocabulary and claims no badge slot.

## Phase 5 — verify in game

Spec swap · bar page flip · shapeshift · combat entry · combat exit · CDM re-layout. The hint
survives all six, or the phase has not passed.

---

## Decisions

1. **Chrome, not a cue.** A keybind is not a rotation signal; it is how you know which icon is
   which button. It stays out of the cue vocabulary, out of elimination and out of the badge
   slots — otherwise the reading gates begin ruling rows in and out on the basis of a keyboard
   layout. **← confirm**
2. **Macros show blank in v1.** The lookup is spell-keyed, so a slot holding a macro that casts
   the ability is invisible to it. The alternative is a `GetActionInfo` scan over slots 1–180
   matching macro bodies. **← confirm**
3. **Always on, or `/cap hotkeys on|off`?** `spec.md` says cap is opinionated, not configurable,
   which argues for always-on; but this is chrome rather than opinion, so a toggle violates
   nothing. **← open**

## Provenance

The API chain, its coverage gaps and its combat-safety live in
`knowledge/addon-dev/cdm-rider-patterns.md` §11 — Tier-1 against shipped 12.1 source. Read it before writing the lookup; do not re-derive
it here.
