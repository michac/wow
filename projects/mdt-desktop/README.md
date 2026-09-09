# MDT Desktop

A second-monitor Mythic+ route viewer. Fullscreen it on monitor 2, press a global hotkey to
advance to the next pull without alt-tabbing.

`backlog.md` owns status and the work list. This file owns the design and why it is shaped
this way.

## Why it exists at all

Mythic Dungeon Tools maps every trash pack in every M+ dungeon and lets you group them into
numbered pulls against an enemy-forces target — but it is an in-client addon with no external
window, and it does **not** auto-advance. `currentPull` is a manual cursor set by clicking a
pull button; there is no combat-log handler and no `SCENARIO_CRITERIA_UPDATE` subscription
anywhere in the addon. So manual advance loses nothing. The win is that the map is big, always
visible, and does not cover the game.

Two constraints shape everything below:

- **No WoW install required.** The app never reads `Interface/AddOns/` or
  `WTF/…/SavedVariables/`. All dungeon data comes off the network at runtime, from MDT's
  GitHub release zip. A machine that has never run the game must work.
- **Route strings are the input**, not MDT's saved presets. It is read-only *toward MDT and the
  game*: it authors no routes and writes nothing back. It does keep its own local library of the
  routes you import, so you paste a string once rather than every launch.

## Shape

```
lua/                      the sidecar: interpreter + scripts
src/MdtDesktop.Core/      net10.0 — fetch, sidecar, model, decode. No UI.
src/MdtDesktop.Cli/       net10.0 — `mdtdesk`, the headless driver
src/MdtDesktop.App/       net10.0-windows, WPF — the viewer
tests/MdtDesktop.Core.Tests/
```

**`Core` never references WPF and `App` holds no parsing.** The CLI exists so every data
milestone is verifiable before any UI exists, and it stays useful afterwards as the debugging
door into `Core`.

Runtime data — the extracted MDT release, `dungeons.json`, and a `version.json` recording
which release it came from — lives in the platform's local-data folder under `MdtDesktop/`,
not in the repo. It is ~18 MB of tiles and it is re-derivable from the network, so a `data
update` starting from nothing is the normal path rather than a recovery one. The downloaded
zip is deleted once unpacked.

`version.json` also stamps a **schema version** for the shape `dungeons.json` was written in,
and a cache written under an older one is refused rather than read. ⚠ That exists because the
failure it prevents is *silent*: schema 2 replaced `spellIds: [1,2,3]` with `spells: [{id,
flags…}]`, and a schema-1 cache deserializes against the new model without any error at all —
leaving every enemy with an empty spell list, so every mob classifies as melee and the caster
count reads zero with nothing anywhere saying why. Refusing it turns that into the message
every call site already handles: *run `mdtdesk data update` first*.

Schema **3** added `seasons`, and it bumped for the same reason: a widening is exactly the kind
of change that degrades silently. A schema-2 cache deserializes with `Seasons` empty, so every
dungeon falls into the synthetic *Other* group and the season picker reads as though MDT had
stopped shipping seasons. Every widening bumps this.

⚠ That root is resolved through `Environment.SpecialFolder.LocalApplicationData`, never a
literal `%LOCALAPPDATA%` — on Windows the two agree, but the literal form does not exist under
WSL, which is where the whole update path is actually developed and run.

WPF on .NET 10, Windows-only. Chosen over WinUI 3 / MAUI / Uno because this is one window
with a canvas, a list and a hotkey; the cross-platform layers are all WinUI underneath on
Windows and buy nothing here. It is the first .NET code in this repo, so its toolchain stays
in-tree — no `global.json` or `Directory.Build.props` hoisted to the repo root.

## Where the data comes from

One GitHub release zip, `Nnoggie/MythicDungeonTools`, fetched unauthenticated at runtime. The
packaged 14 MB zip carries the dungeon Lua, all 16 texture folders and MDT's own `Modules/`
— which is what `lua/hull_check.lua` reads to check our pull geometry against MDT's — so that is
the whole external dependency — no CurseForge API key, no
wago.io, and above all no game install to find. It unpacks to a staging directory and is
swapped into place, so a failure part-way leaves the previous cache intact rather than a
half-unpacked one that looks complete.

## The route library

Import a string once and it is there next launch. One JSON file per route, so a corrupt or
hand-edited entry costs one route rather than all of them.

⚠ It lives under `ApplicationData` (roaming), **deliberately not beside the dungeon cache** in
`LocalApplicationData`. The cache is derived data and deleting it is a documented recovery step;
saved routes are user data and are re-derivable from nothing. Keeping them apart is what stops
"clear the cache" eating the library.

`settings.json` — window placement, zoom, always-on-top, kiosk, the hotkey bindings, and what
was open last — sits **beside** `routes/`, in the same `ApplicationData/MdtDesktop/` folder. ⚠
Beside it, never inside: `RouteLibrary.List` reads every `*.json` in its own folder as a saved
route, so a settings file dropped in there would be parsed as one, silently skipped, and
eventually deleted by a `remove`.

The stored route string is the source of truth — everything else in the record is decoded
convenience that lets the library be listed with no dungeon cache present, and can always be
rebuilt by decoding the string again. The id is MDT's `uid` when there is one, so re-importing
an updated copy of a route replaces it instead of piling up duplicates — which is exactly what
keystone.guru intends by emitting a stable uid.

### It is also what makes staleness detectable

Each saved route records a **`MappingHash` of its dungeon at import time**. That converts the
weakest case into the strongest one: most strings carry no `addonVersion`, but once a route is
in the library we have our own record of what the dungeon looked like, so a later re-map is an
exact per-dungeon comparison rather than a heuristic — the same idea as keystone.guru's
`mdt_mapping_hash`, kept for our own imports.

The fingerprint covers what a route actually depends on: enemy indices, what each is worth,
where its clones stand, and the dungeon's forces total (MDT revises that on its own, and it
moves every percentage in a route without touching an enemy). Cosmetic churn — a renamed mob,
corrected health, a fixed spell list — deliberately does **not** move it, so it cannot cry wolf.

⚠ It answers "has this dungeon changed **since import**", not "was this route current when I
imported it". A route can arrive already stale — the fixture route did — and nothing in a route
string can tell us that. `HasDungeonChangedSinceImport` returns null for "cannot tell", which
must never be reported as "unchanged".

## The Lua sidecar

MDT's dungeon data is Lua, so it is read by Lua. `LuaRunner` starts a real interpreter as a
child process — script in, JSON on stdout, and a non-zero exit *or anything on stderr* raises
with the traceback attached. **Nothing in this repo parses Lua.** (`tools/wowkb/charstate.py`
has a hand-written `_LuaParser`; it is deliberately not reused here.)

The scripts emit JSON through `lua/json.lua`, a ~90-line hand-rolled encoder, so there is no
`dkjson` or `lua-cjson` to vendor. Its table-shape rule is load-bearing rather than cosmetic:
a table becomes a JSON **array** only when its keys are exactly `1..n`, and anything else —
a sparse array, a mixed table — becomes an **object** with stringified keys. MDT's dungeon
indices are sparse (11, 17, 20, 42, 45, 150–155, 160–164) and a pull table mixes integer enemy
indices with the string key `color`, so coercing either into a dense array would silently lose
data. `tests/…/Lua/JsonEncoderTests.cs` pins that.

### Reading the dungeon data

MDT's `Midnight/*.lua` files are plain table literals wrapped in `local _, MDT = ...`, so all
`extract_dungeons.lua` provides is a stubbed `MDT` holding the ten tables they assign into,
plus `Locales/enUS.lua` loaded first so `L["AltarOfFangs"]` answers *Altar of Fangs* rather
than the key. `Midnight/load_midnight.xml` is read as the load order of record, so a dungeon
added upstream needs no edit here. `dofile` cannot pass varargs, hence `loadfile(path)(name, MDT)`.

**The emitted schema is deliberately not MDT's raw table layout.** `json.lua` encodes a dense
`1..n` table as an array and anything else as an object, which is right for preserving the
data — but it means a table's JSON *shape* follows its contents. `enemies` is an array today
and would silently become an object the day a dungeon ships a sparse enemy index. That is not
hypothetical: **6.2.13 deleted clone 12 of The Blinding Vale's Radiant Spellsower**, leaving
that enemy at 1–11, 13–15. So every collection crosses as an array of objects carrying their
own `index`, and the C# side keys its dictionaries on that. Position is never identity.

### Seasons

**MDT groups the dungeons into seasons itself and we read that grouping rather than list it.**
`Modules/DungeonSelect.lua` in the release zip:

```lua
tinsert(MDT.seasonList, L["Midnight Season 2"])
tinsert(MDT.dungeonSelectionToIndex, { 160, 161, 162, 163, 164, 42, 20, 17 })
tinsert(MDT.seasonList, L["Midnight Season 1"])
tinsert(MDT.dungeonSelectionToIndex, { 45, 11, 150, 151, 152, 153, 154, 155 })
```

So a season rotation upstream needs **no edit here** — the same principle `load_midnight.xml`
already establishes as the load order of record. The order is MDT's own (Season 2 first) and is
never re-sorted, so our dropdown and its dropdown read the same way round.

Loading that file needs exactly **three** stubs beyond the `MDT` table the data files need, and
they were measured against a live release rather than guessed:

- `tinsert = table.insert` — a WoW client global, absent from stock Lua 5.4.
- `LibStub = function() return {} end` — line 2 calls it and only stores the result.
- `MDT:IsRetail()` answering true — it gates the whole `do…end` block.

Everything else in the file is function definitions that do not run at load. It is loaded after
the locale (so `L["Midnight Season 2"]` resolves) and after the Midnight data files.

⚠ A release shipping no `Modules/DungeonSelect.lua` — non-retail, or reshaped — **still
extracts**, with no seasons. And `DungeonData.SeasonsWithOrphans()` appends a synthetic trailing
group holding every cached dungeon no season names, emitted only when it is non-empty. That is
the safety valve: a dungeon MDT ships but does not file must stay reachable, and with nothing
declared at all the one synthetic group is the flat list the picker used to be. ⚠ A dungeon may
be in **several** seasons — MDT wrote the mechanism to allow it (`DungeonSelect.lua:8`), though
none is today — which is why the app resolves its startup dungeon first and uses the remembered
season only to disambiguate.

### The interpreter is committed

`lua/lua54.exe` + `lua/lua54.dll` — **Lua 5.4.2, win-x64**, from the LuaBinaries project
(<https://luabinaries.sourceforge.net/>, `lua-5.4.2_Win64_bin.zip`). Lua is **MIT**-licensed;
the LuaBinaries builds are distributed under the same terms. ~478 KB together.

Committed rather than downloaded so a first run is offline-capable and one failure mode
disappears. `bin/` and `obj/` are gitignored; this path deliberately is not.

`LuaInterpreter.Resolve()` picks, in order: `MDTDESK_LUA` if set → the bundled binary on
Windows → `lua5.4` / `lua54` / `lua` on `PATH` → the bundled binary as a last resort. The
native-PATH preference off Windows is for WSL development; the bundled binary does also run
there through interop, script path and all, which is measured rather than assumed.

Development happens under WSL and the whole solution — the WPF project included, via
`EnableWindowsTargeting` — builds and tests there. Only *running* `MdtDesktop.App` needs
Windows.

## Route strings

MDT's current format is **Base64 → raw Deflate → CBOR** (`Modules/Transmission.lua`, the
`!~MDT2~` prefix), built by `C_EncodingUtil` — a Blizzard *client* API, not a vendored
library. That also means the sidecar could not decode it even in principle: `C_EncodingUtil`
does not exist outside the game.

Two older formats exist. **We deliberately do not support them** — see below.

| Prefix | Pipeline | Us |
|---|---|---|
| `!~MDT2~` | Base64 → raw Deflate → CBOR | **decoded** |
| `!` | `LibDeflate:DecodeForPrint` → `DecompressDeflate` → `AceSerializer` | **rejected, by name** |
| *(bare)* | `LibDeflate:DecodeForPrint` → `LibCompress:Decompress` → `AceSerializer` | **rejected, by name** |
| anything else | — | **rejected as not a route string** |

⚠ That last row is not padding. The bare legacy format has no prefix, so "everything that is
not `!` or `!~MDT2~`" is *not* a safe reading of it — a pasted URL, a keystone.guru page
address or a stray word would all be classified as the legacy format and refused with a message
telling the user their route is in an obsolete vintage, which is untrue and sends them looking
in the wrong place. So a bare string has to *look* like one — drawn entirely from LibDeflate's
64-character print alphabet, and long enough to be a route — before it is called one.
`RouteDecoder.DescribeRefusal` owns all four wordings, so the paste box and the CLI cannot drift
into telling the same user different things about the same string.

### Why the two legacy formats are out of scope

This viewer is for **current-season routes**, and a current-season route cannot be in a legacy
format. MDT's `StringToTable` still *reads* all three (`Transmission.lua:25-62`) but
`TableToString` only ever *writes* `!~MDT2~`, so nothing has produced a legacy string in a long
time — and these dungeons are new, so no route for one predates the switch. The other producer
is keystone.guru, and its exports are `!~MDT2~` too: the route in `tests/…/Fixtures` is a KSG
export for Altar of Fangs and carries that prefix.

So the cost of supporting them is a Lua sidecar path plus MDT's vendored `libs/`, and the
benefit is routes for dungeons this app does not show. `RouteDecoder.Classify` recognises both
prefixes and **refuses them with a reason that names the format**, rather than failing as a
corrupt string — so if one ever does turn up, the error says exactly what it is and this
decision can be revisited on evidence.

### Three things measured against a real exported route

None of these could be settled from MDT's source, because all three live inside Blizzard's
client API. Each was tried against an actual string rather than guessed:

- **`C_EncodingUtil.EncodeBase64` is standard RFC-4648**, standard alphabet and standard `=`
  padding. `Convert.FromBase64String` reads it directly.
- **`Enum.CompressionMethod.Deflate` is *raw* deflate**, no wrapper — so `DeflateStream`, not
  `ZLibStream`. A zlib or gzip read of the same bytes fails the header check outright.
- ⚠ **`SerializeCBOR` writes Lua strings as CBOR *byte* strings** (major type 2), not text
  strings (major type 3). Every key in a real route — `"pulls"`, `"color"`, the lot — arrives
  as a byte string. `CborTree` decodes both as UTF-8 so nothing downstream has to care.

The one dependency this costs is **`System.Formats.Cbor`**, a first-party Microsoft package
that ships out of band rather than in the shared framework. Base64 and Deflate genuinely are
in-box; CBOR is not, and hand-rolling a binary-format reader to avoid one Microsoft package
would be a poor trade.

### Preset objects — the author's notes and drawings

A route string carries more than a pull order. `preset.objects` is a **sibling of `text` / `uid`
/ `difficulty` on the preset ROOT** — ⚠ *not* under `preset.value`, where `pulls` lives — and it
holds the annotations the author drew over the map. For a real keystone.guru-exported King's Rest
route (*Skandar Tank — King's Rest (+10 to +15)*, `uid` `eMIO4TPxxKG`), that is **16 notes and 2
drawings**, notes of 54–357 characters each — *"GOLDEN SERPENT — STACK THE GOLD / Drop Spit Gold
pools together near one edge…"*. It is most of what makes that route a **tank guide** rather than
a pull order, and the viewer used to drop all of it on the floor.

MDT's own schema comment (`Modules/PresetObjects.lua:174-175`) is the whole format:

```
--d: size,lineFactor,sublevel,shown,colorstring,drawLayer,[smooth]
--l: x1,y1,x2,y2,...
```

Four creating tools (`Modules/Toolbar.lua:177-207` — pencil, line, arrow, note) produce **three**
stored shapes. Pencil and line are indistinguishable on the wire.

| Kind | Discriminator | Fields |
|---|---|---|
| **Note** | `n = true` | `d` = x, y, sublevel, shown, **text**. No `l`. |
| **Polyline** | `l`, no `t` | `l` = the segments; `d` as above |
| **Arrow** | `t` present | as polyline, **`t[1]` = head rotation in radians** |

#### ⚠ `l` is a list of SEGMENTS, not a polyline

The single trap most likely to produce a wrong picture. `Toolbar.lua:585-588,640-644` append
**four** numbers per stroke segment (`oldx, oldy, x, y`), and the draw loop
(`PresetObjects.lua:194-219`) consumes four at a time and **resets all four to nil** after each.
So `l` = `x1,y1,x2,y2, x3,y3,x4,y4, …` is segment (1→2) and segment (3→4) — the endpoint shared
between consecutive segments appears **twice**.

In the real route both drawings are contiguous (24 and 16 values → 6 and 4 segments, every
segment's end equal to the next one's start), so a pencil stroke *is* a stroke in practice. But
the format does not guarantee it and MDT draws disjoint groups disjoint, so `RouteObject` stores
segments and `RouteOverlay` coalesces contiguous runs into figures. Reading `l` as a plain
polyline would invent segments MDT does not draw.

#### ⚠ Coordinates and colours cross as strings

`d` is a genuinely **mixed** array. Measured on the real route:

```
NOTE d : str('686.1')  str('-459.4')  int(1)  bool(True)  str('OPENING — PURGE…')
LINE d : int(5) int(1) int(1) bool(True) str('ffffff') int(-8) bool(True)
LINE l : str('734.2')  str('-389.5')  str('718.9')  str('-394.9')
```

Every coordinate and the colour hex are strings; sublevel, size, lineFactor and drawLayer are
ints; shown and smooth are bools. So `CborTree.AsDouble` parses **invariant** — under a
comma-decimal culture an ambient parse reads `686.1` as `6861` and puts the pin eight canvas
widths off the map, with nothing thrown. `AsInt` was made invariant at the same time, for the
same reason.

#### ⚠ `d` can arrive sparse, and the hole is load-bearing

`Toolbar.lua:542-543` builds a drawing's `d` as `{ size, 1.1, sublevel, true, colorstring, nil,
true }` — a literal `nil` at index 6 — and a Lua table with a hole serialises as an integer-keyed
map rather than an array. Both container shapes have to be read, and **by key**: collapsing that
hole into a dense list slides `smooth` (index 7) into `drawLayer`'s slot, so `drawLayer` reads a
boolean and `smooth` reads nothing, silently. `objects` itself goes sparse the same way whenever
a user erases a drawing, which makes the map shape the likely case rather than the exotic one.

#### ⚠ Sublevel semantics are the OPPOSITE of a clone's

MDT draws an object only `if obj.d[3] == currentSublevel and obj.d[4]` (`:177`) — an **equality**
test, so a **missing** sublevel means **not drawn**. `Clone.SubLevel == null` is MDT's own "show
everywhere" (`MapGeometry.IsVisibleOn`), which is why that predicate must not be reused here. The
two look identical and mean opposite things.

#### Coordinates, and what is deliberately ignored

Objects live in the **same unscaled canvas space as clones and POIs**: they are stored divided by
`MDT:GetScale()` and drawn multiplied by it, and `GetScale()` is `db.scale`, a pure UI zoom
preference (`MainFrame.lua:229`) — the identical treatment `mapPOIs` gets
(`Pointsofinterest.lua:54-58`). So `MapGeometry.ToCanvas` applies directly, with no new
arithmetic. The measured note range is x 102.9…750.6, y −544.6…−129.5, inside the documented
clone+POI extremes.

Stroke width is `d[1] * 0.3`, MDT's own factor (`PresetObjects.lua:211`), and the arrow head is
drawn at the **last** point at size `d[1] * 1.0` (`:221-225`). **`lineFactor` (`d[2]`) is
deliberately ignored**: it exists to overlap WoW's square line textures so they do not gap at a
joint, and a WPF `Path` with round joins has no such gap. `smooth` (`d[7]`) makes MDT draw
circles at every joint — which *is* round joins and caps, drawn the long way because a WoW
texture has no cap setting. A colour MDT cannot parse it rewrites to white (`:185-189`); so do we,
in `Core`, so junk never reaches a draw loop.

#### Note numbering deviates from MDT, on purpose

A note's number is **positional, not stored** — MDT numbers pins in draw order (`:582,587-588`),
wrapping at 25 because that is how many numbered quest-pin icons its texture sheet has, which
means its note 25 wears note 1's badge. We draw our own pin and have no such limit, so we do not
wrap. Numbering runs across the **whole route** rather than the drawn subset, so a pin, its row
in the notes list and `route decode --notes` cannot disagree about which note is note 3.

#### Two things this settled about keystone.guru

- **The `!` pins in keystone.guru's UI *are* MDT preset notes**, re-skinned. Its popup is the
  decoded object verbatim.
- **The long coloured arrowed lines in its UI are not.** Only the white strokes are in the
  string; the coloured paths are keystone.guru's own layer and cannot be imported.

This is **decode-only**. Nothing here writes a route string back, which is a decision rather than
a gap: the viewer's job is to show somebody else's route, not to author one.

#### Rendering

Final z-order is `Tiles → Drawings → Hulls → Blips → PullLabels → NotePins`. Drawings sit under
the hulls so a pull outline is never buried — ⚠ a divergence from MDT, which draws objects above
everything, made for the reason already recorded for the hulls themselves; it is one line of XAML
to flip if the rendered map disagrees. Note pins go on top because they are the one thing you
point at, and they are the only annotation layer that takes hover: a brush-size-5 stroke that
accepted hit-testing would steal hover from every blip beneath it and silently break the mob
tooltips.

⚠ **Annotations do not dim with the pull cursor.** They carry no pull association whatsoever, so
fading them on a non-current pull would assert a relationship that is not in the data — the same
reasoning already recorded for a mob in no pull.

### The wire still carries dead fields

A decoded preset holds `week`, `teeming` and `riftOffsets`. **They mean nothing.** The affix
machinery is gone from Midnight MDT, and `Presets.lua` force-nils `week` on load. `difficulty`
survives and moves displayed enemy *health* only — never forces. The decoder reads none of them.

### Forces

`RouteForces` is the port of `MDT:CountForces`: cumulative over pulls `1..N`, summing
`clone.count ?? enemy.count`, over `dungeonTotalCount[idx].normal`. Two departures from the
original, both deliberate — it filters on the pull number instead of copying MDT's `break`
out of an order-less `pairs()` loop, and it has no affix filtering to do because
`IsCloneIncluded` has decayed to a bare existence check.

That existence check still earns its keep. A route drawn on one MDT version can name a clone a
later one deleted — 6.2.13 removed clone 12 of The Blinding Vale's Radiant Spellsower — so
unresolved references are skipped and **reported**, never silently counted as zero.

### ⚠ A route can go stale silently, and this cannot be fixed properly

**A route stores enemy and clone *indices*, and nothing that identifies the mobs.** When MDT
re-maps a dungeon, an old route still decodes cleanly and still counts — against whatever now
sits at those indices. It is the one silent failure mode of a route viewer: wrong pull
positions, wrong forces, no error.

It is also not rare. MDT corrected Altar of Fangs' enemy data in **6.2.2** and again in
**6.2.8**, and revised several dungeons' *total* forces in between — Temple of Sethraliss went
649 → 689 → 649 → 687 across five weeks, so both sides of the percentage move.

⚠ **Those are addon release numbers, not data versions.** The dungeon data carries no stamp of
its own; it simply differs between releases, and only a changelog entry says so.

**The one thing a route string can carry is `addonVersion`** — the exporting MDT build with the
dots stripped, `6213` for 6.2.13. `Modules/MainFrame.lua:724` sets `preset.addonVersion =
db.version` on the export button, from
`GetAddOnMetadata(…, "Version"):gsub("%.", "")`. When present it is exact: a route exported by an
older MDT was drawn against different data, no heuristic required.

⚠ **It is frequently absent, and absence must never be read as "current".** MDT's own
party-share path (`Transmission.lua`'s `SendToGroup`) sets `difficulty` but not this, and
keystone.guru's exporter omits it as well — a KSG-exported string is recognisable by a `uid`
ending `xxKG`. The route in `tests/…/Fixtures` is one, which is why it has no `addonVersion`.

Even when present it says only that MDT moved, not whether *this dungeon* did. So it narrows
the question; it does not close it.

⚠ **MDT writes `addonVersion` and never reads it back** — grep the addon: one assignment at
`MainFrame.lua:724`, no read anywhere. It is a write-only field that only third parties consume,
which means it is a de-facto convention rather than a contract, and MDT could drop it without
noticing. Treat it as a bonus, never as something to depend on.

### Nothing guards the boundary

There is no hash, no mapping id, no content stamp in a route string from either side, and
**MDT's import validation never looks at the data**: `ValidateImportPreset` (`Presets.lua:372`)
checks that `text`, `value`, `currentDungeonIdx`, `currentPull`, `currentSublevel` and `pulls`
are present and correctly typed, and that the dungeon is one MDT knows. That is all. No enemy
index, clone index or forces total is examined.

Worse, a keystone.guru export is translated through **the route's own mapping version**
(`extractPulls($this->dungeonRoute->mappingVersion, …)`), so a KSG string for an older route is
born carrying indices valid only against MDT data that has since moved — with nothing in the
string to say so.

So importing a stale route into MDT produces no warning at all. Indices that no longer exist
drop silently out of the pull; indices that still exist but now mean different mobs are drawn as
those mobs. **This viewer's `RouteHealth` warnings are, on this one axis, better than MDT's
own** — which is a low bar, and exactly why they must never be dropped for being noisy.

MDT also handles the *coarse* case: `knownDungeons` catches a preset for a dungeon MDT no longer
ships. It has nothing for the same dungeon re-mapped, which is the case that bites.

### How keystone.guru actually does it

Worth recording, because it is the correct solution and it shows why we cannot simply copy it.
KSG has a first-class `MappingVersion` model (`app/Models/Mapping/MappingVersion.php`) carrying
`version`, `enemy_forces_required` — *the denominator is versioned too* — and `mdt_mapping_hash`.

On each import it **content-hashes MDT's mapping** for a dungeon (`getMDTMappingHash`, over
`counts` + `npcs` + `floorSwitchMarkers`, with keys recursively sorted so Lua's unstable table
iteration order cannot churn the hash — the same reason our extractor sorts). A changed hash
mints a new mapping version. Every route then carries a foreign key to the mapping version it
was authored against, so the "new mapping version available" warning is an exact comparison,
not a guess. Importing an MDT string, they resolve `addonVersion` → release date → the mapping
version current at that date, falling back to newest when it is missing.

**A database can do this; a pasted string cannot.** KSG knows the provenance of routes it
stores. We get 616 characters and whatever the exporter chose to put in them.

So `RouteHealth` gives three signals and claims nothing more:

- `addonVersion` older than the cached MDT build — exact, when the string carries it,
- a reference that no longer resolves, and
- a route whose total falls short of 100% — a published route normally reaches it, so falling
  short is a good tell that the data moved underneath it.

Never silently "correct" a stale route. Warn, name the reason, and show what was decoded.

MDT's dungeon indices are sparse and reused across expansions — Midnight ships 11, 17, 20, 42,
45, 150–155 and 160–164 — so the index is the identity everywhere, including in route strings.

## Coordinates

There is no transform to derive. `clone.x` / `clone.y` are already in map-canvas units from
the canvas top-left, **+x right, −y down**; the only factor MDT ever applies is the user's
zoom. The canvas is **840 × 560** units, composed from **10 rows × 15 columns of 128 px
tiles** (1920 × 1280 px), row-major and 1-based.

> `pixelX = clone.x / 840 * canvasWidthPx`
> `pixelY = -clone.y / 560 * canvasHeightPx`

## Pulls, and the outline round one

A pull is drawn the way MDT draws it (`Modules/PullOutlines.lua`): a **convex hull** of its
mobs' positions, each vertex carrying that blip's `normalScale`; then `expand_polygon(hull, 30)`,
which scatters `max(1, floor(30 * scale))` points on a circle of radius `scale * 10` round every
vertex; then a second hull over the scatter, which is what turns it into a rounded outline. The
pull number goes at the **vertex mean** of the un-expanded hull, which is MDT's own choice of
centre rather than the polygon's area centroid — matching it is what makes the two windows
comparable side by side.

⚠ **MDT's `convex_hull` is not ported as written.** It is gift-wrapping with a `tries > 100`
escape hatch and the comment `--deadlocked here otherwise?!?`, which is a workaround for a bug in
its own loop rather than a property of the problem. `PullHull` uses Andrew's monotone chain
instead: it terminates because it is two sorted sweeps rather than a search, and it is tested on
the inputs the gift-wrapper trips over — collinear points, duplicates, all-identical points,
fewer than three points.

**Deviating meant the agreement had to be measured rather than assumed, and it was.** MDT's
unmodified hull code, sliced out of its own `PullOutlines.lua` and loaded as a chunk
(`lua/hull_check.lua` — the same move that validated the forces port against `Pulls.lua`), was run
over the *Yoda easy route*'s 18 pulls. **Every pull came back with an identical vertex count and
every vertex agreeing to 7e-12 map units** — `json.lua`'s `%.14g` print precision, not a
difference. Reproduce it with `mdtdesk pulls <route> --vertices`, which prints the hull input and
our outline in MDT's own coordinate space so nothing is lost in the y flip.

⚠ It is deliberately **not** an xunit test: it needs a populated dungeon cache and it slices a
file MDT can reshape at any release. It is a check you run, and whose result is recorded here.

**The current pull draws at alpha 1 and every other at 0.5** — `NONACTIVE_ALPHA`
(`PullOutlines.lua:4`), MDT's own answer to marking the current pull, taken rather than
reinvented. A mob in **no** pull is not dimmed: it is not part of the route's ordering, so
dimming it would say something untrue about it.

## What colour a blip is

Two channels, and **they coexist rather than compete**. A mob assigned to a pull wears its
pull's colour; a mob in no pull wears its **role** colour. That is not a compromise — it is
exactly what MDT does, tinting assigned blips from the pull colour
(`DungeonEnemies.lua:962,997`) and resetting the rest (`:983`). The two sets are disjoint by
construction, so the role palette only ever has to separate against itself.

The roles are a **tactical** read, not a taxonomic one — what you have to *do* about a mob, not
whether it is Humanoid or Undead. Four of them, because a blip is 7.8 map units across for plain
trash and a ten-way palette cannot separate at that size.

| Role | Rule | On MDT 6.2.13 | How earned |
|---|---|---|---|
| **Boss** | `isBoss` | 79 | exact — MDT's own flag |
| **Miniboss** | not boss, `count == 0`, health ≥ 3× the trash median | 9 | ⚠ **invented** |
| **Caster** | ≥1 spell flagged `interruptible` | 95 | exact — in the data |
| **Melee** | the residual | 279 | by construction |

Precedence is boss → miniboss → caster → melee, so a kickable miniboss reads as a miniboss and
its caster-ness survives on `Enemy.HasInterruptibleSpell` rather than being lost. (111 enemies
carry an interruptible spell; the 16 that are not counted as casters are bosses and minibosses.)

⚠ **Only the miniboss row is invented**, and it is the one thing here worth arguing with. MDT
ships no flag for it. The signal it rides on is that MDT excludes scripted and encounter mobs from
the forces count, so a mob worth **zero** forces that is nonetheless enormous is not trash the
route pulls — it is something the dungeon does to you. Trash median health is 1,702,709 and the
top zero-forces non-bosses are `Infernal` 202M, `Corewarden Nysarra` 72M and `Zul'jarra` 21M.
Both halves of the rule matter: 115 non-boss enemies are worth zero forces and only nine clear
the health bar, while plenty of ordinary trash is large.

⚠ `scale >= 1.5` is deliberately **not** the rule, though it looks tempting: it covers 128 trash
mobs and tracks how the mapper drew the blip, not what the mob does.

⚠ The median is **global**, across every cached dungeon, not per dungeon. Per-dungeon medians
would be defensible on their own terms — they span 0.7M to 3.4M — but they leave 11 of the 16
dungeons with no minibosses at all, which reads as a broken feature rather than as a dungeon that
happens not to have one. A global bar means "big for trash *in this game*", which is what the eye
is actually asking. `MobRoles.MinibossHealthMultiple` is one named constant so the whole rule can
be retuned by one edit.

**Flags ride as badges, not as fill.** MDT tags each spell with `interruptible`, `enrage` and the
five dispel types, a mob can carry several at once, and they are orthogonal to its role — so
colour says what a mob *is* and a row of letters says what can be done *to* it. `interruptible`
is deliberately not among them: it *is* the caster role, and a badge would spend a slot restating
the colour.

### A third channel: the tactical ring

⚠ **Fill is spent.** Under a route a blip wears its pull's colour, so the role colour — the thing
that says what the mob *is* — is gone exactly when the map is most in use. A **ring around the
disc** is the one channel a pull colour cannot overwrite, and it carries what you have to *do*
about the mob.

| Ring | Rule | Carried | Worn | Colour |
|---|---|---|---|---|
| *(none)* | none of the below | **295** | 295 | — |
| **Interrupt** | any spell `interruptible` | 111 | 111 | red `e34b3f` |
| **Enrage** | any spell `enrage` | 31 | 25 | amber `e8892b` |
| **Crowd control** | a `characteristics` entry other than `Taunt` | 49 | 31 | teal `3fb8a5` |

Measured across all 16 cached dungeons on MDT 6.2.15, not estimated; `mdtdesk roles` prints the
table so it can be argued with from a terminal. **295 of 462 enemies wear no ring**, and that
majority is the point — a ring on everything is a ring on nothing.

*Carried* is how many mobs have the flag at all; *worn* is how many end up in that colour once
precedence has run. Precedence is **interrupt → enrage → CC**, the order of how mandatory and how
time-critical the press is. The two columns differ by exactly the **24** mobs carrying two axes
(16 interrupt+CC, 6 interrupt+enrage, 2 enrage+CC; none carries three), and precedence alone
would hide the second — so those get a **dashed** ring in the winning colour, which is cheap,
honest about there being more, and backed by a tooltip that carries the full picture.

⚠ **`Taunt` is excluded deliberately.** It sits on 79 enemies, only **16** of which are bosses,
so it is not a boss proxy — but it is not a crowd control that changes how a pull is planned
either. It stays in the tooltip's CC row and out of the ring.

The ring is drawn *before* its disc so it can never cover the disc edge, it is not hit-testable
so the disc keeps the tooltip, and it dims with the rest of a non-current pull — leaving it out
of that sweep is the one way this feature could look broken rather than merely absent.

### The tooltip

`Core.Map.MobTooltip` owns the **content** and `MapView.xaml` owns the look, the same seam
`MapPalette` and `RouteOverlay` already establish. A blip's `ToolTip` is set to that **data
object, never a control**: 462 pre-built tooltip visual trees would be paid for at load, while a
data object plus one `DataTemplate` is materialised lazily, on hover, once.

It carries the name and role, the creature line, forces and health, the three tactical rows
(interrupt count, dispel flags, CC susceptibility including `Taunt`), stealth, and the identity
line `enemy N · clone M · npc <id>` — which is what a blip is cross-checked against MDT's own
window with. A section with no rows is **omitted**, so a plain melee mob gets a short tooltip.
Everything is built once except the pull, which changes without the mob changing and is the one
notifying property, assigned in the overlay sweep that was already happening.

## The hotkey

`RegisterHotKey` via `HwndSource.AddHook`, registered in `OnSourceInitialized` — not `Loaded`,
because the window HWND does not exist before then — and given back in `OnClosed`. ⚠ A leaked
registration lives until the process exits and blocks the same combination on the next launch, so
the app would refuse its own hotkey after one unclean close.

⚠ **`MOD_NOREPEAT` is not optional.** Without it a held key auto-repeats and walks the whole route
in a second, on a monitor you are not looking at. Every registration carries it.

⚠ **`RegisterHotKey` returns false when another process already owns the combination**
(`ERROR_HOTKEY_ALREADY_REGISTERED`, 1409) and that is the single most likely way this feature
dies — quietly, with the app looking fine and the key doing nothing. The return value is checked
and the reason reaches the status bar.

⚠ **F2 is WoW's own default `TARGETPARTYMEMBER2`.** Since the OS consumes the key, binding it
here removes party-frame targeting via F2 for as long as the app runs. That is why the binding
is a setting (`settings.json`, parsed by `HotKeySpec`) rather than a constant — rebind one side
or the other.

Everything a press *means* lives in `Core`: `HotKeySpec` parses the text into Win32's own
`MOD_*` values, `PullCursor` decides what next and previous do. It **clamps rather than wraps** —
jumping from the last pull back to the first on a keypress you cannot see reads as the app having
lost your place, while stopping reads as the end of the route. `App` is left with a p/invoke.

## The affix machinery is gone

Verified by grep across MDT 6.2.12/6.2.13 outside `libs/`: no `teeming`, `week`, `faction`,
`inspiring`, `negativeTeeming`, `blacktoothEvent` or `riftOffsets` anywhere in code or data.
`dungeonTotalCount` has only `.normal`. **The viewer needs no week / difficulty / affix
filtering at all** — any older MDT reverse-engineering write-up is wrong for Midnight.

## Installing it on Windows

Development happens under WSL and the whole solution — the WPF project included — builds and
tests there. But `MdtDesktop.App` can only *run* on Windows, so what you double-click is a
published copy, and it goes stale the moment the app changes.

`./deploy-windows.sh` re-cuts it: it publishes Release through the **Windows** dotnet reached
over WSL interop (the Linux SDK cannot emit a runnable WPF app) into
`%LOCALAPPDATA%\Programs\MdtDesktop\`, then rewrites the desktop shortcut. Run it after
touching anything under `src/MdtDesktop.App/`.

⚠ The install directory is **`Programs\MdtDesktop`, not `MdtDesktop`** — the latter is the
dungeon cache, and "delete the cache" is a documented recovery step. Putting the binaries there
would make that step uninstall the app.

The shortcut is rewritten on every deploy rather than only when missing: it is one COM call, and
it repairs a link that was moved, renamed or deleted. Its target folder comes from Windows
itself (`[Environment]::GetFolderPath("Desktop")`), because OneDrive redirects Desktop on this
machine and the literal `%USERPROFILE%\Desktop` is the wrong, near-empty one.

The icon lives in `assets/` — `icon.ico` (16 through 256 px, each size drawn at its own
geometry rather than downscaled, so 16 px stays legible), the `make_icon.py` that produced it,
and a 256 px `icon.png` for review. `MdtDesktop.App.csproj` stamps it into the `.exe` via
`ApplicationIcon`, so the shortcut needs no icon wiring of its own, and carries it again as a
`Resource` for the window and taskbar at runtime.

## Running it alongside the game

⚠ WoW must be in **Fullscreen (Windowed)**, not exclusive fullscreen, or the app will not
stay visible on the second monitor.

⚠ `RegisterHotKey` means **the OS consumes the hotkey and WoW never sees the keystroke**, so
the default must be a key you have not bound in game. F2 / Shift+F2 — see *The hotkey* above for
why that default is worth changing if you use party frames.

**Kiosk** (F11) drops the chrome and both panels so the map is the only thing on the monitor,
and moves the forces readout into the status bar, which is the one thing worth keeping mid-pull.
F11 is bound at the window rather than to the button, so there is always a way back out: a
borderless window with no visible control and no working key is not recoverable without ending
the process.

⚠ The remembered window position is restored through `WindowPlacement.ClampToVisible`, never
raw. A window put back on a monitor that has since been unplugged is invisible, and the only way
out is deleting a file the user does not know exists. It deliberately does **not** clamp `Top` to
zero — a monitor placed above the primary has negative coordinates, and `Math.Max(0, top)` would
drag the window off it on every launch. Zoom is remembered as a **multiple of fit**, not an
absolute scale, or resizing the window would silently re-frame the map.

## Licensing

⚠ **MDT is GPLv2.** Personal use carries no obligation. Distributing anything that bundles its
data or its tiles would make this a derivative work that must also be GPL. Nothing is bundled
today — the release zip is fetched at runtime into `%LOCALAPPDATA%` and never redistributed —
so the question stays open until there is a public release. **Decide before publishing, and
record the decision here.**
