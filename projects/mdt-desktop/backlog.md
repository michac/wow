# MDT Desktop — backlog

**What this file is for:** the current implementation status and the ordered work list.
`README.md` owns the design and why the app is shaped the way it is.

**An item here has to keep earning its place.** If its premise stopped being true, rewrite it
or delete it — never leave it standing with a note underneath. Completed rounds do not
accumulate in the status block; it says what IS, not what happened.

## Status

**It records what is BUILT.** Right now that is the whole app — sidecar, dungeon data, route
decoding, the map, pulls with a global hotkey, and role colouring — with **nothing yet seen on a
screen** (2026-09-05). Everything below is verified headlessly; what is not, and cannot be, is
listed under *Outstanding: only the author can close these*.

- **The solution is four projects** — `Core` (net10.0, no UI), `Cli` (`mdtdesk`), `App`
  (net10.0-windows, WPF) and `Core.Tests`. `dotnet build` and `dotnet test` are green from
  WSL, the WPF project included via `EnableWindowsTargeting`; only *running* `App` needs
  Windows.
- **The Lua sidecar works and the approach is retired as a risk** (2026-09-04). `LuaRunner`
  runs a real interpreter as a child process — stdin in, stdout out, both pipes drained
  concurrently, cancellation kills the tree, and a non-zero exit *or anything on stderr*
  raises a `LuaException` with the traceback in the message.
- **The interpreter is committed**, `lua/lua54.exe` + `lua54.dll` (Lua 5.4.2 win-x64,
  LuaBinaries, MIT), so a first run needs no network and no installed Lua.
  `LuaInterpreter.Resolve()` prefers a native `lua5.4` off Windows for WSL development; the
  bundled binary also runs there through interop, and carries the **whole extraction** — path
  argument and all — on a box with no Lua on `PATH`, measured not assumed.
- **`lua/json.lua` is the JSON encoder** the scripts emit through — hand-rolled, nothing
  vendored. Its shape rule is pinned by test: dense `1..n` becomes an array, a sparse or mixed
  table becomes an object with stringified keys.
- **The dungeon data is fetched, extracted and cached** (2026-09-04). `ReleaseFetcher` pulls
  MDT's latest GitHub release unauthenticated and unpacks it through a staging directory, so a
  failure part-way leaves the previous cache intact. `lua/extract_dungeons.lua` stubs `MDT`,
  loads `Locales/enUS.lua` for real English names, walks `load_midnight.xml` as the load order
  of record, and emits JSON; `DungeonExtractor` deserializes it into `Core.Model`.
  `DataCache` owns the paths and the `version.json` stamp.
- **On MDT 6.2.13 that is 16 dungeons, 462 enemies and 3065 clones**, and dungeon 164 is Altar
  of Fangs with `dungeonTotalCount.normal == 817`. Verified from an empty cache with no WoW
  install involved. Every sublevel's tile folder is present at exactly 150 files, and the
  coordinate extremes match MDT's own: `y ∈ [−550.48, −7.81]`, `x ∈ [18.07, 830.73]` across
  clones and POIs together (clones alone start at 32.93 — the 18.07 is a POI).
- **Collections cross the sidecar as arrays of objects carrying their own `index`**, never as
  position-keyed JSON, because MDT's indices are sparse and 6.2.13 proved it live: it deleted
  clone 12 of The Blinding Vale's Radiant Spellsower, leaving 1–11, 13–15. (6.2.12 had 3066
  clones; that one deletion is the whole difference.)
- **Spells cross as objects carrying MDT's seven flags** (2026-09-05), not as bare ids —
  `interruptible`, `enrage` and the five dispel types. 434 of 462 enemies carry a spell and 111
  carry an interruptible one, which is what makes the caster role exact rather than guessed. The
  outer list is built **densely** so `json.lua` emits an array; keying it by spell id would have
  produced an object, which is the trap the extractor's own header warns about.
- **`version.json` stamps a schema version, and an older cache is refused rather than read**
  (2026-09-05). The failure it prevents is silent: a schema-1 cache deserializes against the
  widened model with no error at all, leaving every enemy with an empty spell list — so every mob
  reads as melee and the caster count reads zero with nothing saying why. Refusing it produces
  the message every call site already handles.
- **The spell widening cannot move a saved route's fingerprint, and that is now a test.**
  `MappingHash` digests enemy indices, forces, clone positions and the dungeon total — never
  spells. Had it read them, one schema edit would have made every route in the library report
  *dungeon re-mapped since import*, loudly and wrongly. The real library route still read `ok`
  across the change, and `Editing_a_mobs_spell_list_does_not_move_the_fingerprint` keeps it that
  way.
- **`mdtdesk data update [--force]` / `data list` / `data show <idx>`** are the headless door
  onto all of it. The cache root resolves through `SpecialFolder.LocalApplicationData`, so it
  is `%LOCALAPPDATA%\MdtDesktop\` on Windows and `~/.local/share/MdtDesktop/` under WSL.
- **Modern route strings decode, and the forces arithmetic is verified** (2026-09-04).
  `RouteDecoder` handles `!~MDT2~` end to end and `RouteForces` ports `MDT:CountForces`.
  `mdtdesk route decode <string>|- [--json]` prints the dungeon, the pulls and per-pull
  cumulative forces plus percentage.
- **The three things MDT's source could not answer were measured against a real route**, not
  guessed: `EncodeBase64` is standard RFC-4648 with standard padding; `CompressionMethod.Deflate`
  is **raw** deflate (`DeflateStream`, not `ZLibStream` — a zlib read fails the header check);
  and `SerializeCBOR` writes Lua strings as CBOR **byte** strings, not text strings.
- **The forces port agrees with MDT's own code.** On the 18-pull *Yoda easy route* for Altar of
  Fangs it gives **811/817 (99.27%)**, and running MDT's **unmodified `Modules/Pulls.lua`** over
  the same decoded pulls produces identical per-pull and cumulative numbers on all 18.
- **A paste that is not a route string is refused as such**, not as a legacy one (2026-09-05).
  The bare legacy format has no prefix, so "anything else is legacy" told a user who pasted a URL
  that their route was in an obsolete vintage — untrue, and it sends them looking in the wrong
  place. A bare string now has to be drawn from LibDeflate's 64-character print alphabet and be
  long enough to be a route before it is called one. `RouteDecoder.DescribeRefusal` owns all four
  wordings, so the paste box and the CLI cannot drift.
- **Stale routes are flagged** (2026-09-04). A route names enemies by index only, so one drawn
  before MDT re-mapped a dungeon decodes cleanly and counts against whatever now sits there —
  silently. `RouteHealth` gives three signals: `addonVersion` older than the cached MDT build
  (**exact**, when the string carries it), an unresolved reference, and a total short of 100%.
  The *Yoda easy route* fixture trips the last one, which is the correct read — Altar of Fangs
  was re-mapped in MDT 6.2.2 and again in 6.2.8.
- **`addonVersion` is read, and its absence is not read as "current"** (2026-09-04). MDT's export
  button stamps it (`MainFrame.lua:724`, dots stripped: `6213`); MDT's party-share path and
  keystone.guru's exporter both omit it. The fixture route is a KSG export — `uid` ending `xxKG`
  — so it has none.
- **`System.Formats.Cbor` is the one NuGet dependency.** Base64 and Deflate are in the shared
  framework; CBOR is not — it is a first-party Microsoft package that ships out of band.
- **Routes persist in a local library** (2026-09-04). `mdtdesk route save|list|show|remove`.
  One JSON file per route under `ApplicationData/MdtDesktop/routes`, kept **away from the
  dungeon cache** so the documented "delete the cache" step cannot eat it. The stored string is
  the source of truth; the id is MDT's `uid`, so a re-import replaces rather than duplicates.
- **A saved route records its dungeon's `MappingHash`**, which makes a later re-map exactly
  detectable for the many strings carrying no `addonVersion` — keystone.guru's `mdt_mapping_hash`
  idea, kept for our own imports. It answers "changed **since import**", never "was current when
  imported", and reports *unknown* rather than *ok* when it cannot tell — in the CLI and in the
  UI, from the same three strings.
- **The map geometry is in `Core`, not in the WPF project** (2026-09-04). `Map/MapGeometry.cs`
  owns the canvas constants, the coordinate flip, the tile numbering and the blip-scale chain;
  `Map/MapLayout.cs` turns a dungeon into placed, sized blips. It lives there because the part
  that can be wrong is the arithmetic, so the arithmetic is the part under test — `App` only draws.
- **`mdtdesk map <idx> [--sublevel n] [--plot]` is the headless view of it**: across all 16
  dungeons every sublevel has its **150/150 tiles on disk**, every blip falls inside the 840 × 560
  canvas, and the extremes come to `x ∈ [32.93, 830.73]`, `y ∈ [7.81, 550.48]` — independently
  reproducing what `README.md` measured off MDT.
- **Pull outlines are MDT's own geometry, and the agreement is measured** (2026-09-05).
  `Map/PullHull.cs` is hull → `expand_polygon(hull, 30)` → hull, with the number at the vertex
  mean. MDT's `convex_hull` is deliberately **not** ported as written — it is gift-wrapping with a
  `tries > 100` escape hatch and the comment `--deadlocked here otherwise?!?`, a workaround for a
  bug in its own loop — so `PullHull` uses Andrew's monotone chain and is tested on the degenerate
  inputs that guard exists for. Deviating meant proving the agreement: MDT's unmodified hull code,
  sliced out of `PullOutlines.lua` and loaded as a chunk (`lua/hull_check.lua`), run over the
  fixture route's 18 pulls, gives an **identical vertex count on every pull and every vertex
  within 7e-12 map units** — `json.lua`'s print precision, not a difference.
- **`Map/RouteOverlay.cs` is the seam that keeps WPF mechanical** (2026-09-05). One function
  turns a route plus a dungeon into per-pull colour, hull, centroid, forces, mob keys and
  `IsCurrent`, plus the map from each mob to the pull that owns it. `MapView` draws that and
  decides nothing. The current pull is alpha 1 and the rest 0.5, which is MDT's own
  `NONACTIVE_ALPHA`; a mob in no pull is **not** dimmed, because it is not part of the ordering.
- **Roles are classified in `Core` and colour the blips** (2026-09-05). Boss (79, MDT's flag),
  caster (95, an interruptible spell in the data), miniboss (9, ⚠ the one invented rule) and melee
  (279). Pull colour and role colour **coexist**: a mob in a pull wears its pull's colour, a mob
  in none wears its role's, which is MDT's own behaviour. Dispel/soothe flags and stealth ride as
  badge letters, never as fill.
- **`mdtdesk roles [<idx>]` and `mdtdesk pulls <str>|-|<id>` are how all of that is checked
  without Windows.** `roles` prints the census, the trash median, and every miniboss by name with
  its health multiple — so the invented rule can be argued with from a terminal. `pulls` prints
  per-pull colour, alpha, hull size, centroid and cumulative forces, asserts that no mob is in two
  pulls and that no hull overhangs the canvas, and `--plot` draws each pull's number where its
  mobs stand. `--vertices` dumps the hull input and our outline in MDT's own coordinate space, for
  `lua/hull_check.lua`.
- **The WPF viewer is written**: `Map/MapView` composes a sublevel's 150 tiles into one
  1920 × 1280 bitmap (flattened rather than 150 `Image` elements, which leave hairline seams at
  fractional zoom), draws role-coloured discs with forces labels, badge rows, boss rings, patrol
  paths and per-blip tooltips, lays pull outlines and numbers over them, and pans and zooms under
  one transform pair anchored on the cursor. It keeps a key→element map so advancing a pull is a
  sweep of property assignments rather than a rebuild of ~200 elements.
- **`MainWindow` is the product**: a paste box that refuses by name, a saved-route picker
  carrying the tri-state, a pull list with colour swatches and per-pull forces, the
  `<cumulative>/<total> (<pct>%)` readout, surfaced `RouteHealth` warnings, prev/next buttons, a
  kiosk toggle and always-on-top. It catches `IOException` and `UnauthorizedAccessException` from
  the library write as well as `RouteDecodeException` — the CLI lets those reach a top-level
  handler, a paste box has no such backstop.
- **The global hotkey is registered in `OnSourceInitialized` and given back in `OnClosed`**
  (2026-09-05), because the HWND does not exist earlier and a leaked registration blocks the same
  combination on the next launch. Every registration carries `MOD_NOREPEAT` — without it a held
  key walks the whole route in a second. `RegisterHotKey` returning false (another process owns
  the combination) is **checked and reported in the status bar**, because that is the likeliest
  way the feature dies quietly. What a press *means* is `PullCursor` in `Core`, which clamps
  rather than wraps.
- **Window, monitor, zoom and chrome persist** to `%APPDATA%\MdtDesktop\settings.json`
  (2026-09-05) — user data, a **sibling** of `routes/` rather than a file in it, since
  `RouteLibrary.List` reads every `*.json` in its own folder as a route. Restore runs through
  `WindowPlacement.ClampToVisible`, which does **not** clamp `Top` to zero (a monitor above the
  primary has negative coordinates), and zoom is stored as a multiple of fit so resizing the
  window does not re-frame the map.
- **It installs on Windows and has an icon** (2026-09-04). `./deploy-windows.sh` publishes
  through the Windows dotnet over WSL interop into `%LOCALAPPDATA%\Programs\MdtDesktop\` —
  deliberately **not** the `MdtDesktop` cache root, which is documented as safe to delete — and
  rewrites the desktop shortcut, resolving Desktop through Windows because OneDrive redirects it
  here. `assets/icon.ico` carries six sizes each drawn at its own geometry, and the `.csproj`
  stamps it into the `.exe`.
- **222 tests.** The M0 sidecar and `json.lua` set, plus a fixture MDT release that pins the
  stub contract: sparse clone indices, a per-clone `count` override, a patrol, flagged and
  unflagged spells, the verbatim texture-folder tail, the legacy `dungeonMaps[0]` slot, per-type
  POI extras, the locale fallback, and byte-stable output. Route decoding is pinned against a real
  exported route plus synthetic strings for the shapes one route does not contain. Hull geometry,
  role classification, the palette, the route overlay, the hotkey parsing, the pull cursor and the
  window-restore guard are all pure and all covered.

## Now

### Outstanding: only the author can close these

**Nothing here is a bug — it is the list of claims a machine with no display cannot make.** Every
one wants the app open, most want MDT or WoW open beside it.

- **⚠ Nobody has seen any of it render.** The app has never been on a screen. `dotnet build`
  proves it compiles; nothing proves `App.xaml` resolves at runtime or that the two new canvases
  bind. This is the first thing to check, and everything below assumes it passes.
- **Do the blips land on the mobs?** M3's own open item, still open, and the one that invalidates
  the most if it is wrong. Wants MDT open on the same dungeon, side by side. The geometry is
  verified headlessly — 150/150 tiles in all 16 dungeons, every blip inside the canvas, extremes
  reproducing MDT's — but that only says the arithmetic is self-consistent.
- **Do the pull outlines look right?** They agree with MDT's own hull code to 7e-12 units, which
  settles the *maths* and settles nothing about the *picture*. The specific risk is the y flip: an
  outline can be mathematically identical and visually mirrored. Also whether overlapping pulls
  read as separate outlines or as a tangle, and whether alpha 0.5 reads as "dimmed" or "broken"
  against the `#0D0F11` viewport.
- **Is the pull number legible at the centroid**, and does it collide with the blips under it? It
  carries a drop shadow because white-on-light-tile would not be, but that is a guess.
- **Are the four role colours actually distinguishable** at 7.8 map units, which is a plain trash
  blip? And are the badge letters readable at all at that size, or do they need to appear only
  above some zoom? Four roles rather than ten creature types is what makes this plausible; it does
  not make it true.
- **Does the hotkey fire while WoW has focus, and does the game never see the key?** Zero of this
  is exercisable from WSL. Check `MOD_NOREPEAT` too: hold F2 and confirm it advances **one** pull.
- **Is F2 already taken on this machine?** If another app owns it the status bar will say so —
  which is itself the thing to confirm works. And ⚠ F2 is WoW's own `TARGETPARTYMEMBER2`, so
  decide whether to rebind the app (`settings.json`) or the game.
- **Window, monitor and kiosk on a real second monitor** — including always-on-top over a WoW
  client, which is the classic place it loses. ⚠ WoW must be in Fullscreen (Windowed). Worth
  testing the unplug case: `ClampToVisible` is unit-tested, `Screens.Enumerate` returning what it
  expects is not.
- **Does advancing a pull feel instant?** It recolours rather than rebuilds for that reason, but
  156 blips on Altar of Fangs is the real test.

### Tune the miniboss rule

⚠ **The one invented number in the whole classification**, and it cannot be falsified without eyes
on a map. `MobRoles.MinibossHealthMultiple` is 3 — a zero-forces non-boss at or above 3× the
global trash median (1,702,709 on 6.2.13). That selects **nine** mobs:

| Dungeon | Mob | Health | ×median |
|---|---|---|---|
| Murder Row | `Infernal` | 202.7M | 119.0 |
| Nexus Point Xenas | `Corewarden Nysarra` | 72.9M | 42.8 |
| Altar of Fangs | `Uncoiled Writhe` | 33.8M | 19.8 |
| Altar of Fangs | `Uncoiled Writhe` | 32.4M | 19.0 |
| Den of Nalorakk | `Zul'jarra` | 21.9M | 12.9 |
| Skyreach | `Skyreach Sun Construct Prototype` | 11.1M | 6.5 |
| Skyreach | `Solar Orb` | 10.3M | 6.0 |
| Murder Row | `Kystia Manaheart` | 5.4M | 3.2 |
| Altar of Fangs | `Ritual Spirit` | 5.2M | 3.0 |

Move the constant and re-run `mdtdesk roles`, which prints this table plus the nearest misses
(`Essence Defiler` at 2.5×, `Rokh'zal` at 2.3×, `Reban` at 2.2×) so the slack either side is
visible. **Do not tune it from the terminal** — the question is whether these nine read as "the
dungeon is doing something to you" on the map, and only the map answers that.

⚠ **`Uncoiled Writhe` is the interesting case and should be looked at first.** An earlier draft of
this file cited it as an example of *normal* zero-count trash. At 19× the median the rule
disagrees, and both readings are defensible. Whichever is right, one of the two claims has to go.

⚠ **The median is global, and that was a deliberate choice against the alternative.** Per-dungeon
medians span 0.7M to 3.4M and are defensible on their own terms, but they leave 11 of the 16
dungeons with no minibosses at all, which reads as a broken feature rather than as a dungeon that
happens not to have one. Revisit only with the map open.

### The rich tooltip

Deferred out of M5 on purpose and still deferred: basic function first. A blip carries a working
tooltip today — name, role, forces, health, the enemy/clone index, whether it has an interruptible
cast, its dispel flags, and stealth. What it does not carry is the CC-susceptibility table
(**81/462** enemies: `Taunt` 79, `Stun` 37, `Slow` 37, `Disorient` 34, `Fear` 30, `Root` 30,
`Silence` 29), the spell list itself, or a click through to `wowhead.com/npc=<id>` — the NPC id is
in hand, so that costs nothing to host.

Worth doing once the map reads correctly, and not before.

## Later

### Confirm the forces readout against the game

⚠ **Open, and only the author can close it.** The forces port agrees with MDT's own `Pulls.lua`
run over the same pulls, which rules out a bug in the arithmetic — but both could still be fed a
mis-decoded route. The confirmation wants a route known to be **current** for its dungeon, since
the *Yoda easy route* fixture predates an Altar of Fangs re-map and its 99.27% is a real
shortfall rather than a decode error. Open one in MDT and compare the percentage and a pull's
mob count.

Worth knowing when checking: pulls coming to **zero** forces are normal — bosses are worth
nothing, and Altar of Fangs also has zero-count non-boss mobs (`Hatchling`, and `Uncoiled
Writhe`, which the miniboss rule now claims — see *Tune the miniboss rule*). The fixture route's
pulls 7, 12 and 18 are all worth zero for exactly this reason.

### Detect a re-map exactly, rather than heuristically

`README.md` § *How keystone.guru actually does it* records the working design: content-hash each
dungeon's mapping per MDT release, mint a version when the hash changes, and resolve a string's
`addonVersion` to the mapping current at that build's release date.

We could do the first half — hash each dungeon at `data update` and keep a small history — but
the payoff is limited: without an `addonVersion` in the string there is nothing to resolve
against, and MDT-native strings that *do* carry one are already handled exactly. Revisit only if
the heuristics prove to miss real staleness in use.

### M6 — keystone.guru browsing

Genuinely optional. keystone.guru exports MDT strings, so the paste box already covers "get a
keystone.guru route into the app" with one copy-paste. It needs a registered API key —
unauthenticated calls return 401, confirmed — so build it only if browsing is worth the auth
plumbing.

### Legacy route-string formats — deliberately not built

MDT still *reads* the two pre-CBOR formats but has long written only `!~MDT2~`, and keystone.guru
exports that too, so no current-season route can be in one. The paste box and the CLI refuse them
by name, from one shared wording, and a paste that is not a route string at all is refused as
that rather than mislabelled a legacy one. Revisit only if a string actually turns up that
someone needs — the reasoning is in `README.md`.

### Real creature portraits

**The data problem is solved; only rendering is left** — which is the opposite of what this item
assumed when it was written ("would need a `displayId` → image source outside the client"). Every
step below was fetched, not inferred, on 2026-09-04:

| Step | Source | Result |
|---|---|---|
| `displayId` → `ModelID` | `CreatureDisplayInfo` via `wowkb.wago` | 462/462 |
| `ModelID` → `.m2` FileDataID | `CreatureModelData` | 462/462 |
| FileDataID → bytes | `wago.tools/api/casc/{fdid}` | `MD21`/`MD20` v274, fetched |
| skin texture → bytes | same endpoint | `BLP2`, fetched |

⚠ **No game install is needed for any of it** — that is `wowkb.uiart`'s existing pipeline
(browser-UA quirk included) pointed at creature models instead of icons. The founding constraint
survives.

⚠ **There is no baked portrait to shortcut to.** `CreatureDisplayInfo.PortraitTextureFileDataID`
exists but is populated for only **13 of our 462** displays. That is also why MDT renders rather
than stores: for 449 of 462 there is no stored image. MDT calls
`SetPortraitTextureFromCreatureDisplayID` (`DungeonEnemies.lua:769-777`, falling back to display
39490) and `Model:SetDisplayInfo` for the 3D tooltip (`MythicDungeonTools.lua:149`).
keystone.guru takes the other road — it hosts one pre-rendered PNG per NPC,
`images/enemyportraits/{npc_id}.png` (`app/Models/Npc/Npc.php:143-145`), keyed on NPC id and not
display id.

**What remains is a renderer**: pose an `.m2` and shoot a headshot. Likeliest path is
wow.export → glTF → headless Blender; a hand-rolled M2 rasteriser is a real project, not an
afternoon. ⚠ **Unverified**: whether M2 carries portrait camera data. That is the difference
between rendering 415 models and hand-framing 415 models, so check it before committing.

Sizing: 462 enemies collapse to **415 distinct `displayId`s**, ~2.4 MB at 64x64 RGBA for all 16
dungeons. It would ship as an optional pack keyed on `displayId`, absent → the coloured disc, so
a mob added by an MDT update degrades instead of breaking.

⚠ **This sharpens the GPLv2 question rather than softening it** (`README.md` § Licensing).
Rendered creature art is Blizzard's IP; pairing it with MDT's mapping in anything distributed is
exactly the derivative-work case. Generating it locally is fine — shipping it is a decision.
