# OPie automation research — a companion to BucketBinds

**Status:** research only (no code, no seed edits). Game scope: Retail, Midnight,
patch **12.0.7** (level cap 90, 2026). OPie is version-agnostic here — its API is
Retail-current as of the 2023+ CustomRings rework and is still shipping.
**Date:** 2026-07-16.

## Why this exists

BucketBinds deliberately pushes out-of-combat sprawl (mounts / toys / teleports /
buffs / professions) **off the keyboard and onto OPie rings**. Today that boundary
is a hand-made OPie master-ring import string ([pastebin bG3zMdT7](https://pastebin.com/bG3zMdT7))
that we treat as an opaque external asset — the seed marks those buckets "on a ring"
and the dumper skips them (`bonus_binds` in `bellular-keybinds.seed.json`: OPie
Master Ring on `T`, Markers `Shift+G`, World Markers `Ctrl+G`, Quest Item `Shift+\``).

The goal: give the ring half the same **seed → generate → apply** treatment
BucketBinds gives the bar half, and go one step further — **scan the collection and
build rings dynamically** so a favorites-mount ring / toy ring stays current.

This note answers four questions and recommends an architecture.

---

## 1. OPie's data model / storage

Confirmed against the **live install: OPie 8.6.2 (store v122), patch 12.0.7** — read
directly from the addon's readable-Lua source and its on-disk `OPie.lua`. OPie is
**proprietary/closed-source** (foxlit; "All Rights Reserved"); there is **no official
git repo** — it ships as readable Lua and is hosted at
[townlong-yak.com/addons/opie](https://www.townlong-yak.com/addons/opie) + CurseForge.
(Third-party GitHub mirrors like `abtris/wow-plugins` are **Cata-era/stale** — they
use the old `OneRing_Config` var; don't trust them for schema.)

### Where it lives (confirmed)
`.toc` declares `## SavedVariables: OPie_SavedData` and
`## SavedVariablesPerCharacter: OPie_SavedDataPC`. On disk:
`…/_retail_/WTF/Account/<acct>/SavedVariables/OPie.lua`. Real shape:
```lua
OPie_SavedData = {
  _OPieVersion="8.6.2 (…)", _StoreVersion=122, _StoreVersion2=122, _GameVersion="12.0.7",
  CharProfiles     = { [charSpecKey] = profileName },
  ProfileStorage   = { ["default"] = { Bindings = { [ringName] = "`" }, RotationTokens={…} } },
  PersistentStorage= { RingKeeper = { [ringName] = <ringDescTable>, OPieDeletedRings=…, OPieFlagStore=… } },
}
```
- **Custom rings live under `OPie_SavedData.PersistentStorage.RingKeeper[ringName]`.**
- **A ring's open-keybind is separate:** `ProfileStorage[profile].Bindings[ringName]`.
- Rings are edited in-game via **`/opie rings`**. The module is `CustomRings.lua`
  (internal name "RingKeeper"/"RK"); it registers the public handle as
  `OPie.CustomRings` (see §2).

### Ring descriptor + slice schema (confirmed from `CustomRings.lua`)
**Ring descriptor** (`props`) — named fields: `name, hotkey, offset, limit, id,
skipSpecs, caption, icon, show, internal, noOpportunisticCA, noPersistentCA`, plus
`save`, `v` (schema version), `vm`, `dropTokens`; **array part `[1..n]` = the slices**.

**Slice table** — positional `[1]`=action-type string, `[2]`=action id, `[3]`=packed
flags/target int; named: `id, sliceToken, icon, label, show, embed, r/g/b (color),
rotation/forceRotation, tipType/tipDetail, fastClick`. Type inference
(`SLICE_ACTIONID_TYPE`): if `[1]` is nil, a **number `.id` ⇒ `"spell"`**, a **string
`.id` ⇒ `"imptext"`** (an encoded macro/slash). **Action-type tokens seen in code:**
`"spell", "item", "toy", "macro", "macrotext"/"imptext", "extrabutton",
"opie.databroker.launcher", "ring"` (nested ring by name), `"func"`. So OPie has a
**native `toy` slice type** (and `item`, `spell`) — you are *not* forced to macrotext.
Flag ints: item `[3]` = `forceShow(1)+byName(2)+onlyEquipped(4)`; spell `[3]`=16 lock-rank.
On disk slices are **plain Lua tables**, not strings.

### Import / export ("snapshots") — confirmed bespoke codec
Shareable strings are **ring snapshots**: `RK:GetRingSnapshot(name[,bundleNested])`
produces them, `RK:GetSnapshotRing(snapshot)` parses. The encoder is **OPie's own
bespoke serializer (`serialize`/`unserialize` in `CustomRings.lua`) — NOT LibDeflate,
NOT AceSerializer/LibSerialize, NOT base64:**
- custom **base-62 alphabet** `01234qwertyuiopasdfghjklzxcvbnm5678QWERTYUIOPASDFGHJKLZXCVBNM9`;
- a **stack-based bytecode** (table-build / key-assign / int / float / string / bool /
  back-reference opcodes) with dictionary compression of repeated substrings;
- **wire layout:** `[7-char signature][7-char checksum][payload]` re-grouped into
  space-separated 7-char blocks, terminated with `.` — which is exactly why the
  user-guide example (`oetohH7 vtKqGge q4WZuwi …`) looks space-chunked with readable
  substrings bleeding through;
- a **custom rolling checksum** guards it — `unserialize` returns nil on checksum
  mismatch or unknown signature; snapshot content-version `_scv=1` (rejects `>1`).
  ([User Guide](https://www.townlong-yak.com/addons/opie/guide))

### Can rings be authored offline / injected?
- **Path A — write `OPie_SavedData` directly (feasible, while WoW is closed).** The
  file is read at launch and rewritten at logout, and the **on-disk form is a plain
  Lua table with NO checksum** — so you can emit a ring descriptor under
  `PersistentStorage.RingKeeper[<name>]` + a `Bindings` entry from an external script.
  Constraints: every slice needs a **globally-unique `sliceToken`** or load **asserts**;
  the ring's `v`/`_StoreVersion` (122) shape must match OPie's migrations; higher
  shape-drift risk across OPie versions. This is a *viable* alternative to the runtime
  API for the **static** seed — but see §4, it doesn't help the dynamic scan.
- **Path B — emit a paste-in snapshot string:** hard/brittle. You'd have to
  reimplement the undocumented base-62 serializer + custom checksum + compression +
  `_scv` gating (no off-the-shelf lib). The only robust way is to run OPie's *actual*
  `serialize()` under headless Lua rather than reimplement it. Not worth it.
- **Path C — the runtime API (§2), recommended.** Build rings in Lua at login. Also how
  OPie builds its own **Trade Skills ring** (auto-populated from known professions) —
  first-party precedent for programmatically/dynamically generated rings, and the only
  path that works for the live collection scan.

---

## 2. OPie's runtime API for addons (the clean path)

Confirmed against **OPie 8.6.3 source (files dated 2026-07-10, Midnight-current)**.
OPie exposes three globals after it loads: **`OPie.CustomRings`** (ring registration —
the main door), **`OPie.ActionBook`** (the `AB` action-abstraction lib), and
`OPie.UI` (skins — not needed here). Real-world external-addon precedent:
Narcissus's [`Bridge/Opie.lua`](https://github.com/Peterodox/Narcissus/blob/main/Narcissus/Bridge/Opie.lua).

### The two registration calls — CONFIRMED (`OPie/CustomRings.lua`)
```lua
OPie.CustomRings:AddDefaultRing(name, descTable)          -- user-EDITABLE seeded ring
OPie.CustomRings:SetExternalRing(name, descTable | false) -- addon-OWNED ring; false removes
```
This distinction drives the whole architecture:

| | `AddDefaultRing` | `SetExternalRing` |
|---|---|---|
| **Timing** | asserts `loadLock == 0` → **must be called BEFORE `PLAYER_LOGIN`** (at file-load / `ADDON_LOADED`) | **no load-timing lock — call any time at runtime** |
| **Ownership** | materializes once into SavedVariables; **user can then edit** it in `/opie rings` | fully **addon-owned**, not user-editable; pass `false` to delete |
| **Update model** | bump the ring's `v=<int>` to push later changes to already-seeded users | just call again with a new `descTable` |
| **Use for** | **v1 static seed** (stable curated rings the user may tweak) | **v2 dynamic collection rings** (rebuilt after a live mount/toy scan) |

⚠ **Correction to keep front-of-mind:** `AddDefaultRing` is *not* a `PLAYER_LOGIN`
call — it's a load-time call. A collection scan (which needs the game loaded) therefore
**cannot** feed `AddDefaultRing`; the dynamic rings must go through `SetExternalRing`.

### Ring `descTable` schema — CONFIRMED (examples in `OPie/Bundle/Editable.lua`)
Array of slice tables **plus** ring-level keys: `name=` (display), `hotkey=` (default
open-binding string, supports macro conditionals e.g. `"ALT-B"`, `"[group] ALT-Y"`),
`limit=` (class/spec gate, e.g. `"DRUID"`), `_u=` (this ring's token prefix), `v=`
(version int, for `AddDefaultRing` migrations), `internal=true`, `embed=`, `onOpen=`.

### Slice table — two accepted forms
1. **`id`-based** (spell number or macro string):
   ```lua
   {id=45438, _u="b"}                                 -- number ⇒ spellID
   {id="/cast [mod]{{spell:13262}};{{spell:7411}}", _u="e"}  -- macro; {{spell:ID}} {{item:ID}} {{mount:air}} tokens
   ```
   Optional per-slice: `show="[cond]"` (visibility conditional), `fastClick=true`,
   `c="rrggbb"` (color), `icon=`, `label=`.
2. **Typed array form** `{"<type>", <arg>, _u="x"}` — e.g. `{"ring","HunterPets"}`
   (nested ring), `{"raidmark",1}`, `{"worldmark",1}`, `{"extrabutton",1}`,
   `{"zoneability",0}`. (Type tokens confirmed in source, §1: `spell/item/toy/macro/
   macrotext/imptext/extrabutton/databroker/ring/func`.)

### `sliceToken` — the one hard rule (mandatory)
Every slice needs a globally-unique, **persistent** token. Two spellings:
- **modern shorthand `_u="x"`** — a short suffix OPie combines with the ring's `_u`
  prefix (see examples above);
- **explicit `sliceToken="MyAddonThing13"`** — still works (the `caption` field is
  deprecated).

Rules ([dev doc](https://www.townlong-yak.com/addons/opie/dev/slice-token-requirements)):
pattern **`^[A-Za-z][A-Za-z0-9_=/]*$`**; **globally unique** across all slices in all
rings (prefix by addon — OPie uses `OP`, player-created `AB`; use e.g. `BR`); and
**persistent** — unchanged meaning ⇒ unchanged token across reloads. **Derive it
deterministically from the action's stable id** (`_u="m"..mountID`,
`_u="t"..itemID`) so a re-scan reproduces identical tokens → ring updates in place,
no dupes, no orphans. Missing/dup tokens **assert (hard error)** on current OPie
(enforcement hardened Jul–Aug 2023).

### Referencing a spell / item / toy / mount in a slice
For simple cases you **don't need ActionBook** — `{id=<spellID>}` or a macro `id`
covers it:

| Action | Slice `id` |
|---|---|
| Spell by id | `{id=<spellID>}` (bare number) |
| Spell/mount by id (macro) | `{id="/cast {{spell:<spellID>}}"}` |
| **Toy** (item) | `{id="/use item:<itemID>"}` (or typed `{"toy",<itemID>}`) |
| **Mount** (summon spell) | `{id="/cast {{spell:<mountSpellID>}}"}` |
| Random favorite mount | `{id="/cast Summon Random Favorite Mount"}` |
| Icon / label override | macro metacommands `#icon [cond] <fileID|name|path>` / `#label <text>` |

### ActionBook (`AB`) — the lower-level door (optional)
`local AB = OPie.ActionBook:compatible(2, 45)` (current MAJ.REV ≈ **2.52**; request the
lowest minor you need). Then:
- `AB:GetActionSlot("item", <itemID>, <flags>)` / `("macrotext", "/cast Foo")` /
  `("toy", <itemID>)` — resolve a **built-in** action to a slot token;
- `AB:CreateActionSlot(hintFn, hintArg, "func", callback, cbArg)` — a custom callback
  slice; `("collection", colTable)` — a sub-ring; `("attribute", …)` — raw secure slice;
- `AB:RegisterActionType("myaddon.type", createFn, describeFn, argCount)` — new type;
- `AB:AugmentCategory(cat, fn)` / `AB:AddActionToCategory(...)` — surface actions in
  OPie's "add slice" browser.

For the BucketRings use case, `{id=…}`/macro slices in `AddDefaultRing`/`SetExternalRing`
are sufficient; AB is only needed if we want typed toy/mount slots or custom behavior.
⚠ *Uncertain:* the exact full token list `GetActionSlot` accepts (item/macrotext/toy/
housing/collection confirmed in shipped rings; `GetActionSlot("spell",…)` not seen
literally — spells are used via `{id=<number>}`), and the `RegisterActionType`
`describeFn` return-tuple order. Confirm against `Libs/ActionBook/ActionBook.lua` if we
go the typed route.

### Load-time skeleton (guarded, static ring)
```lua
-- MyRings.lua, loaded via .toc → runs at ADDON_LOADED, BEFORE PLAYER_LOGIN
local f = CreateFrame("Frame"); f:RegisterEvent("ADDON_LOADED")
f:SetScript("OnEvent", function(_, _, who)
  if who ~= "BucketRings" then return end
  if not (OPie and OPie.CustomRings and OPie.CustomRings.AddDefaultRing) then return end
  OPie.CustomRings:AddDefaultRing("BR_Movement", {
    {id="/cast {{spell:<hearthToySpellOrItem>}}", _u="hs"},
    name = "Movement", hotkey = "ALT-M", _u = "BRmv", v = 1,
  })
end)
```
Declare OPie as **`## OptionalDeps: OPie`** in the `.toc` and no-op if
`OPie.CustomRings` is absent, so the companion never breaks a non-OPie user.

---

## 3. Collection-scanning APIs (12.0.x)

All Retail-current; verified against Warcraft Wiki / Wowpedia.

### Mounts — `C_MountJournal` (the clean one)
```lua
local ids = C_MountJournal.GetMountIDs()          -- ALL mountIDs, filter-independent
for _, mountID in ipairs(ids) do
  local name, spellID, icon, isActive, isUsable, sourceType,
        isFavorite, isFactionSpecific, faction, shouldHideOnChar,
        isCollected, mountID2 = C_MountJournal.GetMountInfoByID(mountID)
  -- keep where isCollected (and, for a favorites ring, isFavorite)
end
```
- `GetMountIDs()` returns every mountID regardless of UI filters — **no filter
  dance needed** (unlike toys). Added 7.0.3, current. ([GetMountIDs](https://wowpedia.fandom.com/wiki/API_C_MountJournal.GetMountIDs))
- `GetMountInfoByID(mountID)` → `name, spellID, icon, isActive, isUsable, sourceType,
  isFavorite, isFactionSpecific, faction, shouldHideOnChar, isCollected, mountID`.
  ([GetMountInfoByID](https://wowpedia.fandom.com/wiki/API_C_MountJournal.GetMountInfoByID))
- **Ownership-gated:** only `isCollected == true` mounts are usable; `isUsable`
  further reflects current form/zone eligibility.
- **How to reference in a slice:** the mount's `spellID` is the summon spell →
  `id = "/cast spell:"..spellID`. (Or, if you'd rather not hardcode a spell:
  `/cast Summon Random Favorite Mount` for a single "smart mount" slice, and
  `C_MountJournal.SummonByID(mountID)` inside a `/run` for edge cases.)
- `GetDisplayedMountInfo(displayIndex)` exists but takes a **filtered** index — avoid;
  `GetMountIDs` + `GetMountInfoByID` is the robust enumeration.

### Toys — `C_ToyBox` (mind the filtered-index gotcha)
There is **no "give me all owned toy itemIDs" call**. `GetToyFromIndex(i)` walks a
**filtered** list, so you must open the filters, then loop:
```lua
-- widen filters so every owned toy is visible
C_ToyBox.SetCollectedShown(true)
C_ToyBox.SetUncollectedShown(false)
C_ToyBox.SetAllExpansionTypesChecked(true)   -- or SetExpansionTypeFilter per exp
C_ToyBox.SetAllSourceTypeFilters(true)       -- or SetSourceTypeFilter per source
-- (clear the search box too if set)
C_ToyBox.ForceToyRefreshOnce()
for i = 1, C_ToyBox.GetNumFilteredToys() do
  local itemID = C_ToyBox.GetToyFromIndex(i)          -- -1 if invalid
  if itemID and itemID > 0 and PlayerHasToy(itemID) then
    local _id, name, icon, isFavorite, hasFanfare, quality = C_ToyBox.GetToyInfo(itemID)
    -- keep (and, for a favorites ring, gate on isFavorite)
  end
end
```
- `GetToyFromIndex(index)` — index `1..C_ToyBox.GetNumFilteredToys()`, returns itemID
  or `-1`. `GetNumToys()` = total in DB; `GetNumFilteredToys()` /
  `GetNumTotalDisplayedToys()` = current filtered count (the one to loop).
  ([GetToyFromIndex](https://warcraft.wiki.gg/wiki/API_C_ToyBox.GetToyFromIndex),
  [GetNumToys](https://wowpedia.fandom.com/wiki/API_C_ToyBox.GetNumToys))
- `GetToyInfo(itemID)` → `itemID, toyName, icon, isFavorite, hasFanfare, itemQuality`.
  `PlayerHasToy(itemID)` → bool ownership. ([GetToyInfo](https://wowpedia.fandom.com/wiki/API_C_ToyBox.GetToyInfo),
  [PlayerHasToy](https://wowpedia.fandom.com/wiki/API_PlayerHasToy))
- ⚠ **Side effect:** the `Set*Filter` calls mutate the player's *actual* ToyBox UI
  filter state. **Snapshot the current filters, set, scan, then restore** — or the
  user opens their Toy Box later to find filters changed. This is the main
  implementation footgun for the toy ring.
- **How to reference in a slice:** a toy is an **item** → `id = "/use item:"..itemID`.

### Ownership/knowledge gating summary
- Toys: `PlayerHasToy` / `isCollected`. Mounts: `isCollected`. Only enumerate owned.
- Both collections are account-wide (warband) in Retail, so a scan reflects the whole
  account's toys/mounts, not just the logged-in character — good for a stable ring.
- Refresh triggers to rebuild on: `NEW_TOY_ADDED`, `COMPANION_LEARNED` /
  `NEW_MOUNT_ADDED` (confirm exact event name), and `PLAYER_LOGIN`.

### Toy vs mount as a slice — bottom line
| Collectible | Underlying type | Slice `id` |
|---|---|---|
| Mount | spell (summon spell) | `/cast spell:<spellID>` |
| Toy | item | `/use item:<itemID>` |
| Random smart mount | built-in spell | `/cast Summon Random Favorite Mount` |

---

## 4. Recommended architecture

**Ship a companion addon that registers rings via `OPie.CustomRings:AddDefaultRing`
at login.** This mirrors BucketBinds' proven shape (seed JSON → generated Lua →
in-game apply → GitHub-release deploy via `ghaddons`) and avoids OPie's internal
formats entirely.

### The three options, weighed
| Option | Verdict | Why |
|---|---|---|
| **(a)** Generate an OPie **import string** offline from a seed | ✗ reject | Snapshot codec is proprietary & undocumented; brittle; breaks on format revs. |
| **(b)** **Companion addon** builds rings via `AddDefaultRing` at runtime | ✓ **recommend** | Public, supported API. Same author-time model as BucketBinds. Handles both static seeds *and* live collection scans. Format churn is OPie's problem, not ours. |
| **(c)** Write OPie's **SavedVariables** (`OPie_SavedData`) directly, WoW closed | ◐ possible, not preferred | Feasible for the *static* seed — the on-disk form is a plain checksum-free Lua table (§1 Path A). But undocumented schema, `sliceToken`-assert + `_StoreVersion` shape-drift risk, and it **can't do the dynamic scan** (that needs the game running). Use (b) instead. |

### Why (b) fits BucketBinds so well
- **Same pipeline:** a `rings.seed.json` (shared + per-class ring definitions) →
  `gen_rings_lua.py` → `Rings.lua` (generated) → addon calls `AddDefaultRing` on
  `PLAYER_LOGIN`. Identical author→generate→ship discipline; identical ghaddons
  release deploy (a plain push doesn't reach the game).
- Could even live **inside the BucketBinds addon** as an optional module (guarded by
  `OptionalDeps: OPie`), so one release ships bars + rings. Or a sibling addon
  `BucketRings` in its own repo, deployed the same way.
- The static seed is *literally analogous* to the bar seed: instead of
  `(bucket) → (bar, slot)` it's `(ring) → [ordered actions]`.

### Which API for which ring
- **Static rings → `AddDefaultRing`** (at `ADDON_LOADED`, before login). User can
  tweak them; push updates by bumping `v=`.
- **Dynamic collection rings → `SetExternalRing`** (at runtime, after the scan). Addon
  owns them; rebuild = call again. Since `AddDefaultRing` is load-locked *before*
  `PLAYER_LOGIN`, it literally can't consume a live collection scan — the dynamic half
  **must** use `SetExternalRing`. (Trade-off: `SetExternalRing` rings aren't
  user-editable — acceptable for auto-generated collection rings, which the user would
  re-generate anyway.)

### Risks & mitigations
- **OPie internal-format churn** — avoided by using the public `CustomRings` API, not
  SV/snapshot internals. `AddDefaultRing`/`SetExternalRing` have been stable since the
  2023 CustomRings rework; version-gate with `OPie.ActionBook:compatible(2, N)`.
- **`sliceToken` persistence** — derive tokens deterministically from stable ids
  (`_u="m"..mountID`, `_u="t"..itemID`), never random, so re-scans are idempotent
  (update-in-place, no dupes, no orphaned tokens). Dup/missing tokens **hard-error**.
- **Combat lockdown — a non-issue.** Rings are OOC and building a ring via
  `AddDefaultRing`/`SetExternalRing` is not a protected action (unlike
  `PlaceAction`/`SetBinding` in BucketBinds). No combat guard needed.
- **Macro/slot caps — a non-issue.** Rings don't consume the 120/18 macro budget or
  the 1–180 action-slot space. A macrotext slice's body lives in OPie, not the macro
  UI. Ring size is soft (radial gets crowded past ~12–16 slices — a UX cap, not a
  hard one) — so for large collections, prefer **favorites-only** or category-split
  rings.
- **ToyBox filter mutation** (§3) — snapshot & restore the player's filter state
  around the scan.
- **OPie absent** — optional-dep + `if OPie and OPie.CustomRings then` guard; no-op
  cleanly.
- **Binding the rings** — OPie rings get their *open* keybind inside OPie (or via the
  binding UI); the seed's `bonus_binds` already reserves keys (`T`, `Shift+G`, etc.).
  `AddDefaultRing` can suggest a default binding but must not fight the user's binds
  (same "default only if unbound" rule OPie's built-ins follow). Keep BucketBinds'
  bar binder and the ring binder in separate keyspaces (they already are: rings on
  `T`/`Shift+G`/`Ctrl+G`/`Shift+\``, bars on QERF/number-row/ZXCV + modifiers).

---

## 5. Milestones — v1 static, v2 dynamic

### v1 — static ring seed (the BucketBinds-analogue)
A hand-authored seed of **common, stable** actions → rings, shipped as generated Lua.
- **Rings to seed** (shared + per-class):
  - *Utility / master ring* — hearthstone-class toys, teleport toys, cosmetic staples.
  - *Movement / teleport ring* — Hearthstone, Dalaran/garrison hearth toys, mage
    portals (per-class), engineering wormholes, Path of Least Resistance, class
    movement toys.
  - *Profession ring* — analogous to OPie's built-in Trade Skills ring (may just reuse
    the built-in; seed only what it misses).
  - *Per-class ring* — class-specific utility (e.g. warlock summon/soulwell, mage
    table, DK raise-ally variants) not on the keyboard.
- **Data:** actions carry a stable id (spellID / itemID) so `id` + deterministic
  `sliceToken` generate cleanly. Reuse BucketBinds' `items`/`buffs` reference tables
  where they overlap.
- **Deliverable:** `rings.seed.json`, `gen_rings_lua.py`, generated `Rings.lua`, a
  login handler calling `AddDefaultRing` per ring, `.toc` OptionalDeps guard.
- **Verify in-game:** `/reload`, hold the ring key, confirm slices resolve (icons +
  labels), no `sliceToken` errors.

### v1.5 — polish the static layer
- Split shared vs per-class rings; `#icon`/`#label` on macrotext slices for clean
  visuals; a couple of `[cond]` slices (e.g. hearth toy `[nomounted]`).
- Reconcile with the existing pastebin master ring — regenerate it from seed rather
  than treating it as an opaque asset (retire bG3zMdT7 as source of truth).

### v2 — dynamic collection scan (via `SetExternalRing`)
On `PLAYER_LOGIN` (+ refresh events), scan the account and (re)build collection rings
with **`OPie.CustomRings:SetExternalRing(name, desc)`** (runtime-callable; `AddDefaultRing`
can't be used here — it's load-locked before login):
- **Favorites mount ring** — `GetMountIDs` → keep `isCollected and isFavorite` →
  slices `{id="/cast {{spell:"..spellID.."}}", _u="m"..mountID}`.
- **Toy ring(s)** — filter-scan `C_ToyBox` (snapshot/restore filters) → owned (or
  favorite) toys → slices `{id="/use item:"..itemID, _u="t"..itemID}`.
- **Idempotent refresh** — deterministic `_u` tokens mean a re-scan rebuilds the ring
  in place as the collection grows; re-call `SetExternalRing` on `NEW_TOY_ADDED` /
  new-mount events too. Pass `false` to retire a ring.
- **Sizing** — favorites-only by default; optional category split (utility toys vs
  cosmetic toys) once collections exceed a comfortable radial count.
- **Verify in-game:** learn a new favorite toy/mount → ring updates without dupes and
  without disturating the ToyBox filter UI.

### v2.5 — refinements
- Favorites-vs-all toggle; per-category toy rings; battle-pet ring (same `C_PetJournal`
  pattern); teleport ring auto-built from known teleport toys/spells rather than
  hand-listed.

---

## Open items to confirm (honesty log)
Most of the earlier unknowns were resolved by reading the **live 8.6.2/8.6.3 source**.
Remaining low-confidence spots (per staleness doctrine):
1. Exact full token list `AB:GetActionSlot` accepts — item/macrotext/toy/housing/
   collection confirmed in shipped rings; a literal `GetActionSlot("spell",…)` wasn't
   seen (spells go via `{id=<number>}`). Confirm in `Libs/ActionBook/ActionBook.lua`
   before choosing typed toy/mount slots over macro `id`s.
2. `RegisterActionType`'s `describeFn` return-tuple order (only needed if we register a
   custom action type — likely unnecessary).
3. Precise new-mount event name (`NEW_MOUNT_ADDED` vs `COMPANION_LEARNED` /
   `MOUNT_JOURNAL_USABILITY_CHANGED`) for v2 refresh triggers. `@verify-ingame`.
4. Whether `SetExternalRing` rings can carry a default `hotkey=` that survives a
   `/reload` the same way `AddDefaultRing` ones do. `@verify-ingame`.

## Sources
- OPie source (authoritative, current — release **8.6.3, 2026-07-10**; readable Lua):
  https://www.townlong-yak.com/addons/opie — key files `CustomRings.lua`,
  `Bundle/Editable.lua`, `Bundle/ExtraActions.lua`, `Bundle/QuestItems.lua`,
  `Libs/ActionBook/ActionBook.lua`, `Libs/ActionBook/Imp.lua`. (Also read from the live
  install `…/Interface/AddOns/OPie/` + `…/WTF/…/SavedVariables/OPie.lua`.)
- OPie dev: Slice Token Requirements (CustomRings API) — https://www.townlong-yak.com/addons/opie/dev/slice-token-requirements
- OPie User Guide — https://www.townlong-yak.com/addons/opie/guide
- OPie Extended macros (`id` syntax, `#icon`/`#label`) — https://www.townlong-yak.com/addons/opie/macros
- OPie (CurseForge) — https://www.curseforge.com/wow/addons/opie
- Real external-addon example (Narcissus OPie bridge) — https://github.com/Peterodox/Narcissus/blob/main/Narcissus/Bridge/Opie.lua
- OPie (WoWInterface) — https://www.wowinterface.com/downloads/info9094-OPie.html
- C_MountJournal.GetMountIDs — https://wowpedia.fandom.com/wiki/API_C_MountJournal.GetMountIDs
- C_MountJournal.GetMountInfoByID — https://wowpedia.fandom.com/wiki/API_C_MountJournal.GetMountInfoByID
- C_ToyBox.GetToyFromIndex — https://warcraft.wiki.gg/wiki/API_C_ToyBox.GetToyFromIndex
- C_ToyBox.GetToyInfo — https://wowpedia.fandom.com/wiki/API_C_ToyBox.GetToyInfo
- C_ToyBox.GetNumToys — https://wowpedia.fandom.com/wiki/API_C_ToyBox.GetNumToys
- PlayerHasToy — https://wowpedia.fandom.com/wiki/API_PlayerHasToy
- WoW collections API idioms (toy/mount enumeration) — https://github.com/jburlison/wowaddonapiagents/blob/main/.github/skills/wow-api-collections/SKILL.md
