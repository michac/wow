---
title: Frames, widgets and rendering
patch: 12.0.7
fetched: 2026-07-23
reviewed: 2026-07-23
sources:
  - https://github.com/Gethe/wow-ui-source (live, version.txt 12.0.7.68887, commit 4383ced30106d51b27e3e86d1987f1552f0d259d)
  - Interface/AddOns/Blizzard_SharedXML/UI.xsd (1628 lines, the Tier-1 XML schema)
  - Interface/AddOns/Blizzard_APIDocumentationGenerated/ (593 files, 77 ScriptObject tables)
  - https://github.com/Ketho/BlizzardInterfaceResources (branch live, commit 774b2c550366, "12.0.7 (68256)") — Resources/WidgetAPI.lua for the inheritance graph
  - https://warcraft.wiki.gg/wiki/XML/Texture (revid 6776374, 2026-07-19)
  - https://warcraft.wiki.gg/wiki/API_Region_SetVertexColor (revid 6654858, 2026-02-19)
  - https://warcraft.wiki.gg/wiki/API_TextureBase_SetGradient (revid 6654937, 2026-02-19)
  - https://warcraft.wiki.gg/wiki/API_TextureBase_SetTexture (revid 6654547, 2026-02-19)
  - https://warcraft.wiki.gg/wiki/Frame_Strata (revid 5975111, 2024-02-23 — STALE, see §4.1)
  - https://warcraft.wiki.gg/wiki/Secret_Values (revid 6777907, 2026-07-22)
  - https://warcraft.wiki.gg/wiki/Patch_12.0.7/API_changes (revid 6778033, 2026-07-22)
  - https://warcraft.wiki.gg/wiki/API_CreateFrame (revid 6779954, 2026-07-23)
  - https://warcraft.wiki.gg/wiki/XML/Layer (revid 6769786, 2026-07-12)
  - https://warcraft.wiki.gg/wiki/XML/Color (revid 6771907, 2026-07-15)
  - https://warcraft.wiki.gg/wiki/API_Region_SetAlpha (revid 6654851, 2026-02-19)
  - https://warcraft.wiki.gg/wiki/API_ScriptRegionResizing_SetPoint (revid 6654887, 2026-02-19)
  - https://warcraft.wiki.gg/wiki/API_Frame_SetFlattensRenderLayers (revid 6654668, 2026-02-19)
  - https://warcraft.wiki.gg/wiki/UIOBJECT_AnimatableObject (revid 6749996, 2026-06-20) + the UIOBJECT_{Texture 6777822, Frame 6750022, FontString 6750105, Line 6750104, MaskTexture 6750102} pages that transclude it
  - https://github.com/Stanzilla/WoWUIBugs issues #107, #250, #474, #847, #848
confidence: high
---

> **Adversarial verification pass, 2026-07-23.** Every locator in this file was
> re-opened against the same checkout. **27 claims were corrected, weakened or
> re-scoped**; each edit is marked `[corrected 2026-07-23]` inline and states
> what the old text said and what the source actually says. Everything not so
> marked was opened and confirmed — including all seven Tier-3 addon-corpus
> counts, all 15 wiki revids/dates, all four WoWUIBugs issues, every strata and
> draw-layer census figure, and the whole `Pools.lua` / `UI.xsd` /
> `SecretPredicates` line set. (WoWUIBugs #250 was listed in `sources:` but cited
> nowhere; it is now cited, in §5.1.)
>
> The substantive ones, if you read nothing else: the §4.2 annotation table
> (`SetClipsChildren` was not unannotated), §4.4 (`SetDrawLayer` is not
> unannotated), §3.1 (`GetNumPoints` is not `SecretWhenAnchoringSecret`), §5.1
> (`SetMask` is not a base-image writer, and "exactly one is in force" was never
> cited), §5.1 `GetTextureInfo` (four `assetType` values, not two), §9.4 and
> rule 37 (region-pool proxies expose nine methods, not eight; collections nine,
> not eleven), and §6.3 (LibSharedMedia is vendored 5×, not 8×).

# Frames, widgets and rendering

**Scope.** Everything that can be put on screen: the widget type hierarchy,
object creation in Lua and XML, anchoring, z-ordering (strata / level / draw
layer), textures and their separate colour channels, fonts and media,
animations, object pooling, and attaching to Blizzard's own frames.

**Deferred to sibling topics.** *When* to repaint (event wiring, `OnUpdate`
budget) → `api-events-and-discovery`. What "protected", "tainted", "secret
value" and "forbidden" mean → `security-taint-and-restricted-data`. This file
records only where those concepts intersect rendering, and points there.

## Citation conventions used in this file

| Prefix | Means |
|---|---|
| `[T1 src]` | Blizzard's shipped UI source. Paths relative to the `wow-ui-source` checkout root (prefix `raw/addon-research/wow-ui-source/`). Build **12.0.7.68887**, commit `4383ced30106`. |
| `[T1 docs]` | `Interface/AddOns/Blizzard_APIDocumentationGenerated/…` in the same checkout — Blizzard's machine-generated API spec. Shape, not behaviour. |
| `[T1 xsd]` | `Interface/AddOns/Blizzard_SharedXML/UI.xsd` — the XML schema, authored by Blizzard (header attribution at `UI.xsd:2`). 1628 lines. |
| `[T1 obs]` | Directly observed by counting/grepping the shipped corpus or the live install at `/mnt/c/Program Files (x86)/World of Warcraft/_retail_/`. Observation, not spec. |
| `[T2 wiki]` | warcraft.wiki.gg, with revid + last-edit date. Pages rot silently; the stamp is load-bearing. |
| `[T2 res]` | `Ketho/BlizzardInterfaceResources` — a derived per-build dump. **Build 12.0.7.68256**, a *different build of the same patch*. |
| `[T2 bug]` | A WoWUIBugs issue. Evidence of observed behaviour; an `Acknowledged by Blizzard` label is evidence Blizzard agrees it is a bug — never evidence of intended design. |
| `[T3]` | A named community addon at a named commit. One data point. |

> ⚠ **Build skew.** Source checkout `12.0.7.68887`; `BlizzardInterfaceResources`
> `12.0.7.68256`; this repo's `_meta/game-version.md` records live as
> `12.0.7.68453`. Same patch, three builds. **Nothing in this file has been run
> in the client.** Items that need that are marked `@verify-ingame`.

---

## 1. The object model

### 1.1 The inheritance graph

The generated API docs **do not encode inheritance** — each of the 77
`ScriptObject` tables is a flat method list with `Type = "ScriptObject"` and no
parent field (e.g. `[T1 docs: SimpleTextureAPIDocumentation.lua:1-5]`, whose
whole header is `Name / Type / Environment / Functions`). The inheritance graph
comes from `[T2 res: Resources/WidgetAPI.lua]`, which carries an explicit
`inherits = {...}` per type. Reconstructed from that file:

```
FrameScriptObject                        WidgetAPI.lua:2      (GetName, GetObjectType, IsObjectType,
  │                                                            IsForbidden, HasSecretValues, SetToDefaults)
  └── Object                             WidgetAPI.lua:17     (GetParent, GetParentKey, GetDebugName)
        └── ScriptRegion   +ScriptObject WidgetAPI.lua:37     (anchoring, mouse, Show/Hide, scripts)
              └── Region                 WidgetAPI.lua:124    (GetDrawLayer/SetDrawLayer,
                    │                                          GetVertexColor/SetVertexColor, alpha, scale)
                    ├── FontString  +FontInstance   :170
                    └── TextureBase                 :211
                          ├── Texture               :253      (mask-texture attachment)
                          ├── MaskTexture           :262
                          └── Line                  :267
        └── Frame  (inherits ScriptRegion)          :474
              ├── Button → CheckButton              :600 :653
              ├── Model → PlayerModel → {Cinematic,DressUp,Tabard}Model  :664 :739 :768 :791 :819
              ├── ModelScene                        :837
              ├── EditBox / MessageFrame / SimpleHTML  (each +FontInstance)  :983 :1063 :1083
              ├── ColorSelect, GameTooltip, Cooldown, Minimap, MovieFrame,
              │   ScrollFrame, Slider, StatusBar, FogOfWarFrame,
              │   UnitPositionFrame, Browser, Checkout, OffScreenFrame, WorldFrame
              └── Blob → {ArchaeologyDigSite, QuestPOI, ScenarioPOI}Frame  :1378 :1397 :1402 :1410
AnimationGroup (Object + ScriptObject)   :280
Animation      (Object + ScriptObject)   :318
  └── Alpha :363, Scale :372, LineScale :385, Translation :398,
      LineTranslation :405, Path :412, Rotation :432,
      TextureCoordTranslation :443, FlipBook :450, VertexColor :465
Font (FrameScriptObject + FontInstance)  :159
```

`[corrected 2026-07-23]` The animation-subtype range was previously written
`:363–:474`; `:474` is `Frame`. The ten subtypes are the per-type lines above,
each with `inherits = {"Animation"}`; the block ends at `:466`.

Two facts that matter and that people get wrong:

- **`Frame` is not the root.** `Frame` inherits `ScriptRegion`
  `[T2 res: WidgetAPI.lua:474-475]`, so a `Texture` is a *sibling branch* of
  `Frame`, not a child of it. Methods like `SetPoint`, `Show`, `Hide`,
  `SetAlpha`, `SetScale`, `GetRect` live on `ScriptRegion`/`Region` and are
  shared by both. `[corrected 2026-07-23]` This bullet used to also assert
  "and so does `Region`" — that is exactly the edge the gap below says is
  unverified, so it has been removed from the claim.
- **`FontString` is a `Region`.** It inherits `Region` *and* `FontInstance`
  `[T2 res: WidgetAPI.lua:170-171]`. That is why a FontString has both
  `SetTextColor` (from the font side) and `SetVertexColor` (from the region
  side). See §5.4.

> `[gap]` The `inherits` entry for `Region` in that dump reads
> `inherits = {"Region"}` — a self-reference `[T2 res: WidgetAPI.lua:124-125]`.
> That is a generator artefact; the real parent is almost certainly
> `ScriptRegion` (the method split is consistent with it, and the wiki's
> `UIOBJECT Texture` page transcludes `UIOBJECT_Region`, `UIOBJECT_ScriptRegion`,
> `UIOBJECT_ScriptRegionResizing`, `UIOBJECT_AnimatableObject`, `UIOBJECT_Object`,
> `UIOBJECT_FrameScriptObject` in that order `[T2 wiki: UIOBJECT Texture, revid
> 6777822, 2026-07-21]`). I could not find a Tier-1 statement of the parent.
> Don't build on that one edge.

### 1.2 The `Simple*` naming in the generated docs

The generated docs name the widget tables `SimpleFrameAPI`,
`SimpleTextureBaseAPI`, `SimpleRegionAPI`, `SimpleScriptRegionAPI`,
`SimpleScriptRegionResizingAPI`, `SimpleAnimGroupAPI`, … while the
`BlizzardInterfaceResources` dump and the wiki use the un-prefixed widget names
(`Frame`, `TextureBase`, `Region`). They are the same types. When you look a
method up with `wowkb.uiapi`, search the method name, not the type name:

```bash
cd tools && uv run python -m wowkb.uiapi func '^SetVertexColor$'
cd tools && uv run python -m wowkb.uiapi widget 'SimpleTextureBaseAPI'
```

### 1.3 Which layer owns which method

This split is the single most useful thing to memorise, because it tells you
what a given object can do without looking anything up:

| Owner table | Owns | Cite |
|---|---|---|
| `SimpleFrameScriptObjectAPI` | `GetName`, `IsObjectType`, `IsForbidden`, `SetForbidden`, `HasSecretValues`, `HasSecretAspect`, `IsPreventingSecretValues`, `SetToDefaults` | `[T1 docs: SimpleFrameScriptObjectAPIDocumentation.lua:52,83,114,128,136]` |
| `SimpleScriptRegionAPI` | `Show`/`Hide`/`IsShown`/`IsVisible`, `SetParent`, mouse enable/propagate, `GetRect`/`GetLeft`/`GetTop`/…, `SetScript`/`HookScript`, `IsAnchoringSecret`, `IsAnchoringRestricted` | `[T1 docs: SimpleScriptRegionAPIDocumentation.lua:3…]` |
| `SimpleScriptRegionResizingAPI` | `SetPoint`, `SetAllPoints`, `ClearAllPoints`, `ClearPoint`, `GetPoint`, `GetPointByName`, `GetNumPoints`, `SetSize`/`SetWidth`/`SetHeight`, `AdjustPointsOffset` | `[T1 docs: SimpleScriptRegionResizingAPIDocumentation.lua:3…]` |
| `SimpleRegionAPI` | `GetDrawLayer`/`SetDrawLayer`, `GetVertexColor`/`SetVertexColor`/`SetVertexColorFromBoolean`, `GetAlpha`/`SetAlpha`/`SetAlphaFromBoolean`, `GetScale`/`SetScale`/`GetEffectiveScale`, `SetIgnoreParentAlpha`/`SetIgnoreParentScale`, `IsObjectLoaded` | `[T1 docs: SimpleRegionAPIDocumentation.lua:3…]` |
| `SimpleTextureBaseAPI` | `SetTexture`, `SetAtlas`, `SetColorTexture`, `SetMask`, `SetTexCoord`/`ResetTexCoord`, `SetGradient`, `SetDesaturated`/`SetDesaturation`, `SetBlendMode`, `SetRotation`, tiling, slice margins, vertex offsets, `SetSpriteSheetCell`, pixel-grid snapping | `[T1 docs: SimpleTextureBaseAPIDocumentation.lua:3…]` |
| `SimpleTextureAPI` | only 4 methods — `AddMaskTexture`, `RemoveMaskTexture`, `GetMaskTexture`, `GetNumMaskTextures` | `[T1 docs: SimpleTextureAPIDocumentation.lua:3]` |
| `SimpleFrameAPI` | `CreateTexture`/`CreateFontString`/`CreateLine`/`CreateMaskTexture`, strata/level/toplevel, `SetClipsChildren`, `SetFlattensRenderLayers`, `GetRegions`, `DesaturateHierarchy`, attributes, `Raise`/`Lower` | `[T1 docs: SimpleFrameAPIDocumentation.lua:3…]` |

---

## 2. Creating objects: Lua, XML, templates, mixins

### 2.1 `CreateFrame` is not in the generated docs

`CreateFrame` has **no entry** in `Blizzard_APIDocumentationGenerated`. Verified:
`wowkb.uiapi func '^CreateFrame$'` → 0 matches, and `FrameScriptDocumentation.lua`
(the system that *does* document `Mixin`, `CreateFromMixins`, `issecretvalue`,
`securecallmethod`, …) does not list it `[T1 docs: FrameScriptDocumentation.lua:3
onward; Mixin at :279, CreateFromMixins at :82]`. So the canonical signature —
`CreateFrame(frameType, name, parent, template, id)` — rests on the wiki
`[T2 wiki: API CreateFrame, revid 6779954, 2026-07-23]` and on **329** call
sites in the shipped source, e.g.
`[T1 src: Blizzard_Menu/11_0_0_MenuImplementationGuide.lua:107]`
(`CreateFrame("DropdownButton", nil, MyParentFrame, "WowStyle1DropdownTemplate")`).
`[corrected 2026-07-23]` The count was written as "~338"; a
`grep -rho 'CreateFrame(' --include='*.lua'` over `Interface/AddOns` returns 329.

`CreateForbiddenFrame` likewise has no doc entry; it appears **11** times in the
shipped source, and `[corrected 2026-07-23]` **not** all inside
`Blizzard_StoreUI` as previously claimed. The actual spread `[T1 obs]`:

| File | Lines |
|---|---|
| `Blizzard_StoreUI/Blizzard_Shared_StoreUISecure.lua` | 2961, 2990, 3140, 3506, 3528 |
| `Blizzard_GlueXML/Shared/CharacterServicesTemplates.lua` | 207, 229 |
| `Blizzard_SharedXMLBase/Pools.lua` | 548, 672 (the `forbidden and CreateForbiddenFrame or CreateFrame` selector, §9.1) |
| `Blizzard_EnvironmentCleanup/EnvironmentCleanup.lua` + `…/Classic/EnvironmentCleanup.lua` | 4 each — `CreateForbiddenFrame = nil;`, i.e. the glue-environment teardown, not a construction site |

Region constructors *are* documented, and their signatures are **not uniform**:

```
Frame:CreateTexture(name?, drawLayer?, templateName?, subLevel?)      SimpleFrameAPIDocumentation.lua:119
Frame:CreateLine(name?, drawLayer?, templateName?, subLevel?)         SimpleFrameAPIDocumentation.lua:83
Frame:CreateMaskTexture(name?, drawLayer?, templateName?, subLevel?)  SimpleFrameAPIDocumentation.lua:101
Frame:CreateFontString(name?, drawLayer?, templateName?)              SimpleFrameAPIDocumentation.lua:66  ← NO subLevel
```

All four carry `SecretArguments = "NotAllowed"` `[T1 docs:
SimpleFrameAPIDocumentation.lua:68,85,121]`.

> **Inconsistency worth knowing.** Blizzard's own pool code calls
> `parent:CreateFontString(name, layer, template, subLevel)` — four arguments —
> at `[T1 src: Blizzard_SharedXMLBase/Pools.lua:586]`, against a documented
> three-argument signature. Either the generated docs are incomplete for
> `CreateFontString` or the fourth argument is silently discarded.
> `[gap]` I could not settle which. `@verify-ingame`: create two FontStrings on
> the same frame and draw layer with different `subLevel` values and see whether
> the stacking order differs.

### 2.2 XML is a real, schema-defined language — and almost nobody uses it

`UI.xsd` is the Tier-1 definition of the markup: element names, nesting, and
every attribute enum. It is 1628 lines and is the *only* place several
enumerations are written down at Tier 1 (§4, §5).

Structure of the type system `[T1 xsd]`:

- `LayoutFrameAttributes` (`UI.xsd:468-490`) is the shared attribute set for
  *everything* placeable: `name`, `parentKey`, `parentArray`, `inherits`,
  `mixin`, `secureMixin`, `virtual`, `setAllPoints`, `collapsesLayout`,
  `hidden`, mouse flags, `protected`, `secureReferenceKey`,
  `propagateMouseInput`, `preventSecretValues`.
- `TextureAttributes` (`UI.xsd:546-569`) = `LayoutFrameAttributes` **plus**
  `file`, `mask`, `atlas`, `useAtlasSize`, `alphaMode`, `alpha`, `scale`,
  `rotation`, `snapToPixelGrid`, `texelSnappingBias`, `hWrapMode`, `vWrapMode`,
  `ignoreParentAlpha`, `ignoreParentScale`, `horizTile`, `vertTile`,
  `desaturated`, `nonBlocking`, `noanimalpha`, `nolazyload`, `nounload`.
- `FrameAttributes` (`UI.xsd:720-751`) = `LayoutFrameAttributes` **plus**
  `alpha`, `scale`, `parent`, `toplevel`, `flattenRenderLayers`,
  `useParentLevel`, `movable`, `resizable`, `frameStrata`, `frameLevel`, `id`,
  `enableKeyboard`, `clampedToScreen`, `depth`, `dontSavePosition`,
  `propagateKeyboardInput`, `ignoreParentAlpha`, `ignoreParentScale`,
  `intrinsic`, `clipChildren`, `propagateHyperlinksToParent`,
  `hyperlinksEnabled`, `fixedFrameStrata`, `fixedFrameLevel`, `frameBuffer`,
  `jumpNavigateEnabled`, `jumpNavigateStart`, `ignoreChildrenForBounds`.

**In practice the ecosystem builds frames in Lua.** Across the seven surveyed
addon clones, only **9 of 124** `.xml` files contain any widget markup
(`<Frame`, `<Button`, `<Texture`, `<FontString`) `[T1 obs]`:

| Addon (commit) | `.lua` | `.xml` | `.xml` with widget markup |
|---|---|---|---|
| WeakAuras2 `38d4bf1e6099` | 198 | 7 | 1 |
| BigWigs `3fdc10f6cfd1` | 131 | 0 | 0 |
| Details `e14de53cc2e1` | 326 | 36 | 4 |
| Plater `2b2ff463cccd` | 185 | 33 | 1 |
| ElvUI `f60934a174d6` | 680 | 28 | 2 |
| oUF `5672a3cb10e1` | 41 | 1 | 1 |
| Ace3 `4475787f06f7` | 74 | 19 | 0 |

The rest are mostly file-load manifests and `Bindings.xml` — WeakAuras' seven
XML files are `WeakAuras/locales.xml`, `WeakAurasTemplates/locales.xml`,
`WeakAurasOptions/locales.xml`, `WeakAuras/embeds.xml`,
`WeakAurasOptions/embeds.xml`, `WeakAuras/Bindings.xml` and
`WeakAuras/Profiling.xml` `[T1 obs]`. `[corrected 2026-07-23]` The earlier
wording implied none of them carried markup; `WeakAuras/Profiling.xml` is
precisely the one that does, and is the "1" in the table row.
Note Details and Plater share an author (Tercioo) so
they are not independent data points. This is a *practice* observation, not a
recommendation: XML remains fully supported and Blizzard's own UI is 1028 `.xml`
files `[T1 obs: wow-ui-source file census]`.

### 2.3 Templates, `virtual`, `parentKey`, `parentArray`

- `virtual="true"` on any layout element makes it a **template**, referenced by
  the `inherits` attribute or by the `templateName` argument of `CreateFrame` /
  `CreateTexture` / … `[T1 xsd:475 (virtual), :472 (inherits)]`.
- `parentKey="X"` assigns the created object to `parent.X`; `parentArray="X"`
  appends it to `parent.X` `[T1 xsd:470-471]`. There is no Lua equivalent —
  in Lua you assign the field yourself.
- Templates compose: `inherits` is typed `xs:string`, so the schema does not
  constrain the separator at all `[T1 xsd:472]`. In the shipped corpus a
  **comma** (usually comma-space) is what is actually used — 339 `.xml` files
  carry a comma-separated `inherits=`, e.g.
  `inherits="ArenaEnemyPrepFrameTemplate, PingableUnitFrameTemplate"` `[T1 obs]`.
  The wiki calls the `CreateFrame` `template` argument a "comma-delimited list"
  `[T2 wiki: API CreateFrame, revid 6779954, 2026-07-23]`.
  `[gap]` I found no Tier-1 statement that a bare space also separates.

Worked Blizzard example: `BackdropTemplate` is a `virtual="true"` `Frame` that
attaches `BackdropTemplateMixin` and wires two scripts
`[T1 src: Blizzard_SharedXML/Backdrop.xml:5-8]`.

### 2.4 Mixins

`Mixin(object, ...)` and `CreateFromMixins(...)` are **engine functions**, not
Lua helpers — both are documented in `FrameScriptDocumentation.lua`
(`CreateFromMixins` at `:82`, `Mixin` at `:279`), and both carry
`SecureHooksAllowed = false` `[T1 docs]`. What remains in Lua is only the secure
variant set `[T1 src: Blizzard_SharedXMLBase/Mixin.lua]`:

```lua
CreateAndInitFromMixin(mixin, ...)   -- Mixin.lua:8   CreateFromMixins + :Init(...)
CreateSecureMixinCopy(mixin)         -- Mixin.lua:15  copy + setmetatable{__metatable=false}
SecureMixin(object, ...)             -- Mixin.lua:23
CreateFromSecureMixins(...)          -- Mixin.lua:42
```

`SecureMixin` and `CreateFromSecureMixins` **return `nil` and do nothing when
`issecure()` is false** `[T1 src: Mixin.lua:24-26, :43-45]`. Addon code is
insecure by construction, so an addon calling `SecureMixin` gets a silent no-op.
Use `Mixin` / `CreateFromMixins`.

XML has two attributes: `mixin` and `secureMixin`, both on
`LayoutFrameAttributes` `[T1 xsd:473-474]` and on `AnimationType`
`[T1 xsd:1456-1457]`.

**Script reflection.** `FrameUtil.SpecializeFrameWithMixins(frame, ...)` mixes in
and then calls `FrameUtil.ReflectStandardScriptHandlers(frame)`, which
`SetScript`s any of nine conventionally-named methods it finds on the table —
`OnLoad, OnShow, OnHide, OnEvent, OnEnter, OnLeave, OnClick, OnDragStart,
OnReceiveDrag` — then calls `frame:OnLoad()` and, if visible, `frame:OnShow()`
`[T1 src: Blizzard_SharedXMLBase/FrameUtil.lua:86-124]`. **`OnUpdate` is
deliberately excluded**, with the comment "Many OnUpdates are set dynamically.
Leave this off for now." `[T1 src: FrameUtil.lua:99-100]`.

### 2.5 Intrinsics

`intrinsic="true"` promotes a template to a *new element name* usable as a
`frameType` — the third construction mechanism, sitting between "widget type"
and "template". `UI.xsd` declares ten intrinsic element bindings at the bottom of
the schema `[T1 xsd:1618-1627]`: `ContainedAlertFrame`, `DropDownToggleButton`,
`DropdownButton`, `EventEditBox`, `EventScrollFrame`, `EventFrame`,
`EventButton`, `ItemButton`, `TestFrame`, `UIThemeContainerFrame`.

Ten shipped XML files declare `intrinsic="true"` `[T1 obs]`, e.g.
`[T1 src: Blizzard_SharedXML/Shared/Frame/EventFrame.xml:3]`,
`[T1 src: Blizzard_ItemButton/Shared/ItemButtonTemplate.xml:4]`,
`[T1 src: Blizzard_Menu/DropdownButton.xml:3]`.

> `[corrected 2026-07-23]` **The two tens are not the same ten.** The counts
> match by coincidence; the sets differ by one element each way `[T1 obs]`:
> - `ScrollingMessageFrame` is declared `intrinsic="true"` at
>   `[T1 src: Blizzard_SharedXML/ScrollingMessageFrame.xml:3]` but has **no**
>   element declaration in `UI.xsd`'s intrinsic block.
> - `TestFrame` has an XSD element declaration `[T1 xsd:1626]` but is declared
>   `intrinsic="true"` by no shipped XML file.
>
> That matters for the gap below: a declared-but-unschema'd intrinsic
> (`ScrollingMessageFrame`) is Tier-1 evidence that the XSD element list is **not**
> the registration mechanism — the `intrinsic="true"` attribute is. It does not
> establish that an *addon*'s declaration is honoured.

**Zero of the seven surveyed addon clones declare an intrinsic** `[T1 obs]`.
They do *consume* Blizzard's (e.g. `CreateFrame("DropdownButton", …)`).

> `[gap]` The XSD puts `intrinsic` in the shared `FrameAttributes` group
> `[T1 xsd:740]`, so an addon *can* write it, but I found no Tier-1/Tier-2
> statement that an addon-declared intrinsic becomes usable as a `CreateFrame`
> `frameType`, and no addon in the corpus does it. `@verify-ingame`.

---

## 3. Anchoring and size

### 3.1 The model

A region's rectangle is defined by **anchor points**, not by coordinates. Each
anchor is `(point, relativeTo, relativePoint, offsetX, offsetY)` where `point`
and `relativePoint` are drawn from a **nine-value** enumeration
`[T1 xsd:4-16]`:

```
TOPLEFT  TOP     TOPRIGHT
LEFT     CENTER  RIGHT
BOTTOMLEFT BOTTOM BOTTOMRIGHT
```

In XML the same shape is `<Anchors><Anchor point= relativeTo= relativeKey=
relativePoint= x= y=><Offset/></Anchor></Anchors>` `[T1 xsd:505-523]`. Note
`relativeKey` — an XML-only way to anchor to a sibling by `parentKey` path,
with no Lua equivalent.

The full anchoring/sizing method set lives on `ScriptRegionResizing`, and
**every mutator on it is `IsProtectedFunction = true`**
`[T1 docs: SimpleScriptRegionResizingAPIDocumentation.lua:10,22,32,43,111,…]`:
`SetPoint`, `SetAllPoints`, `ClearAllPoints`, `ClearPoint`, `ClearPointsOffset`,
`AdjustPointsOffset`, `SetPointsOffset`, `SetSize`, `SetWidth`, `SetHeight`.

`[corrected 2026-07-23]` The accessors are **not** uniform, contrary to what this
section previously said. `GetPoint` (`:65`) and `GetPointByName` (`:88`) are
`MayReturnNothing` + `SecretWhenAnchoringSecret` + `ConstSecretAccessor`;
**`GetNumPoints` (`:52`) carries no annotations at all** — it is not
`SecretWhenAnchoringSecret`, so a point *count* survives secret anchoring even
though every point *value* does not
`[T1 docs: SimpleScriptRegionResizingAPIDocumentation.lua:52,65,88]`.

### 3.2 Reading the rectangle

`GetLeft/GetRight/GetTop/GetBottom/GetCenter/GetRect/GetScaledRect` are all
`MayReturnNothing = True` **and** `SecretWhenAnchoringSecret = True`
`[T1 docs: SimpleScriptRegionAPIDocumentation.lua — GetBottom, GetCenter,
GetLeft, GetRect, GetRight, GetScaledRect, GetTop]`. `GetWidth/GetHeight/GetSize`
are `ConstSecretAccessor` + `SecretWhenAnchoringSecret` (they return a value but
may return a secret one). `IsRectValid()` is the guard: it carries no
annotations at all and is the intended "can I trust the geometry yet?" test.

Pixel space: the UI's virtual coordinate space is **768 units tall**, and the
conversion factor is `768.0 / physicalScreenHeight`
`[T1 src: Blizzard_SharedXML/PixelUtil.lua:3-6]`. `PixelUtil.SetPoint`,
`PixelUtil.SetSize`, `PixelUtil.GetNearestPixelSize(uiUnitSize, layoutScale,
minPixels)` snap offsets and sizes to whole device pixels
`[T1 src: PixelUtil.lua:8-56]` — the namespace is exactly
`GetPixelToUIUnitFactor:3, GetNearestPixelSize:8, ConvertPixelsToUI:30,
ConvertPixelsToUIForRegion:34, SetWidth:38, SetHeight:42, SetSize:46,
SetPoint:51`, and the file is 56 lines. Note there are **two**
`ConvertPixelsToUI`: the `PixelUtil.`-namespaced one at `PixelUtil.lua:30` and a
bare global of the same name in the secure file
`[T1 src: PixelUtilSecure.lua:2-5]`.

### 3.3 Anchoring and secret values (the Midnight seam)

This is the one place the security model reaches directly into layout, so it
belongs here as well as in the security file.

- The predicate `SecretWhenAnchoringSecret` is defined as: *"Guarded APIs and
  events produce secret values when an object has secret anchoring information."*
  `[T1 docs: SecretPredicatesDocumentation.lua:63-66]`. It carries
  `Type = "Secret"` and no `FailureMode`.
- 23 documented functions carry it (the `SecretWhenAnchoringSecret` count in the
  built index).
- `ScriptRegion:IsAnchoringSecret()` is the test
  `[T1 docs: SimpleScriptRegionAPIDocumentation.lua — IsAnchoringSecret,
  SecretReturnsForAspect = ObjectSecrets]`; `IsAnchoringRestricted()` is the
  older restricted-frame test `[same file]`.
- How an object *acquires* secret anchoring, per the wiki: passing a secret value
  to an API that accepts secrets but has **no** connected aspect marks the whole
  object as having secret values; that state marks its anchoring and position
  data secret, and **propagates downward to anything anchored to it** —
  "If child frame B is anchored to parent frame A, and A has secret anchoring
  data, B implicitly has secret anchors too." Clearing anchor points can reset it.
  `[T2 wiki: Secret Values, revid 6777907, §Secret anchors, 2026-07-22]`.

The practical shape: `StatusBar:SetValue(secretNumber)` can poison the geometry
readout of an entire anchored subtree.

### 3.4 Anchor families

Anchoring across "anchor families" raises a real error. The exact string, quoted
from a 2026 bug report:

```
Action[SetPoint] failed because[SetPoint would result in anchor family connection]:
attempted from: GameTooltip:SetPoint.
```
`[T2 bug: WoWUIBugs #848, created 2026-06-05, closed; same string in #847]`.
The wiki dates the rule to 8.2.0 and gives two reproducers — mixing
UIParent-relative with screen-relative anchors on the same region, and anchoring
one frame between two different nameplates
`[T2 wiki: API ScriptRegionResizing SetPoint, revid 6654887, 2026-02-19]`.

### 3.5 Layout helpers

`AnchorUtil` wraps anchors as first-class objects: `AnchorUtil.CreateAnchor`,
`CreateAnchorFromPoint`, `GridLayout`, `ChainLayout`, `VerticalLayout`,
`GridLayoutFactory`, plus mirroring helpers
`[T1 src: Blizzard_SharedXMLBase/AnchorUtil.lua:2,58,112,115,122,167,176,209,230,
370-413]`. `BaseLayoutMixin` (`Layout`, `MarkDirty`, `IsDirty`, `MarkClean`,
`IsLayoutFrame`, `MarkIgnoreInLayout`) is the dirty-flag layout engine
`[T1 src: Blizzard_SharedXML/LayoutFrame.lua:10 (mixin), :18 IsLayoutFrame,
:26 MarkIgnoreInLayout, :74 Layout, :84 MarkDirty, :106 MarkClean,
:119 IsDirty]`. The XML counterpart of
"ignore me in layout" is `collapsesLayout` `[T1 xsd:477]` with
`SetCollapsesLayout` / `CollapsesLayout` / `IsCollapsed` on ScriptRegion
`[T1 docs: SimpleScriptRegionAPIDocumentation.lua]`.

---

## 4. Z-order: strata, level, draw layer

Three independent orderings, applied in this nesting: **strata** contains
**frame level** contains **draw layer** contains **texture sub-level**.

### 4.1 Frame strata

`UI.xsd` enumerates **ten** values `[T1 xsd:18-31]`:

```
PARENT  BACKGROUND  LOW  MEDIUM  HIGH  DIALOG  FULLSCREEN  FULLSCREEN_DIALOG  TOOLTIP  BLIZZARD
```

`PARENT` is the XML attribute default (`frameStrata` default `"PARENT"`,
`[T1 xsd:730]`). `[corrected 2026-07-23]` The gloss *"i.e. inherit from parent,
not a z-band"* has been dropped — it is inference from the name. Tier 1 gives the
value and the default and nothing more, and no shipped XML or Lua ever writes
`PARENT` explicitly (0 occurrences, table below), so the corpus offers no
behavioural evidence either. `[gap] @verify-ingame`.

Observed usage in the shipped corpus `[T1 obs]`:

| Value | `SetFrameStrata("…")` in `.lua` | `frameStrata="…"` in `.xml` |
|---|---|---|
| HIGH | 12 | 254 |
| DIALOG | 26 | 186 |
| MEDIUM | 2 | 67 |
| LOW | 2 | 56 |
| TOOLTIP | 4 | 53 |
| FULLSCREEN_DIALOG | 8 | 24 |
| BACKGROUND | 2 | 12 |
| FULLSCREEN | 7 | 6 |
| BLIZZARD | 0 | 1 — `[T1 src: Blizzard_AuthChallengeUI/Blizzard_AuthChallengeUI.xml:65]` |
| PARENT | 0 | 0 |

> ⚠ **The wiki's `Frame Strata` page is stale.** Last edited **2024-02-23**
> (revid 5975111). It lists **nine** strata, headed by `WORLD`, and does not
> mention `BLIZZARD` or `PARENT` at all. `WORLD` does not appear in `UI.xsd`.
> Use the XSD list; use the wiki page only for the behavioural notes below.

Behavioural notes, Tier 2 only `[T2 wiki: Frame Strata, revid 5975111,
2024-02-23]`: frame levels run 0–10000; a child defaults to one level above its
parent; moving a parent shifts descendants by the same delta, and a shift that
would take a level below 0 is set to 10000 instead. **None of that is stated at
Tier 1** — `@verify-ingame`.

### 4.2 Frame level and the protection asymmetry

```
SetFrameStrata(strata)      IsProtectedFunction  SecretArguments=NotAllowed            :1188
SetFrameLevel(level)        IsProtectedFunction  AllowedWhenUntainted  +FrameLevel     :1176
SetToplevel(bool)           IsProtectedFunction  AllowedWhenUntainted  +Toplevel       :1366
SetFixedFrameStrata(bool)   IsProtectedFunction  AllowedWhenUntainted                  :1155
SetFixedFrameLevel(bool)    IsProtectedFunction  AllowedWhenUntainted                  :1144
SetUsingParentLevel(bool)   IsProtectedFunction  AllowedWhenUntainted                  :1388
SetClipsChildren(bool)                           AllowedWhenUntainted                  :1113
SetFlattensRenderLayers(b)                       AllowedWhenUntainted                  :1166
SetIsFrameBuffer(bool)                           SecretArguments=NotAllowed            :1288
```
`[T1 docs: SimpleFrameAPIDocumentation.lua, lines as shown]`
(`+X` = `SecretArgumentsAddAspect = { Enum.SecretAspect.X }`.)

> `[corrected 2026-07-23]` This table previously showed `SetClipsChildren` as
> "— no annotations —". It carries `SecretArguments = "AllowedWhenUntainted"`.
> The `SetFixedFrame*` / `SetUsingParentLevel` / `SetFrameLevel` / `SetToplevel`
> rows were also missing their `SecretArguments` value. `SetFrameStrata` is the
> only `NotAllowed` entry in the strata/level family, and `SetIsFrameBuffer` the
> only `NotAllowed` entry that is *not* also `IsProtectedFunction`.

Note the split: **strata rejects secret arguments outright; frame level accepts
them and marks the frame's `FrameLevel` aspect secret.** `GetFrameLevel` is
correspondingly `SecretReturnsForAspect = {Enum.SecretAspect.FrameLevel}`
`[T1 docs: SimpleFrameAPIDocumentation.lua:391-393]`, while `GetFrameStrata`
carries no annotation at all. `IsToplevel` is
`SecretReturnsForAspect = {Toplevel}`.

`Frame:GetHighestFrameLevel(iterateAllChildren)` (`:418`) and
`GetRaisedFrameLevel()` (`:519`) exist — useful for "put my overlay one above
whatever is there". `[corrected 2026-07-23]` They are **not** both unannotated:
`GetRaisedFrameLevel` is unannotated, but `GetHighestFrameLevel` carries
`SecretArguments = "AllowedWhenUntainted"` and its `frameLevel` return is marked
`ConditionalSecret = true` `[T1 docs: SimpleFrameAPIDocumentation.lua:418-431]`
— i.e. it can hand back a secret when the walked subtree contains one.

### 4.3 Render-layer flattening

`SetFlattensRenderLayers(flatten)` composites all descendant textures and
fontstrings into a single render layer, so unrelated overlapping frames stop
interleaving. `Frame:SetToplevel` implicitly enables it, and other frame
attributes can too `[T2 wiki: API Frame SetFlattensRenderLayers, revid 6654668,
2026-02-19]`. Tier 1 corroborates only the *shape*: there are both
`GetFlattensRenderLayers()` (explicit request) and
`GetEffectivelyFlattensRenderLayers()` (actual state) `[T1 docs:
SimpleFrameAPIDocumentation.lua]`, plus the XML attribute `flattenRenderLayers`
default `false` `[T1 xsd:726]`. The existence of two distinct getters is
Tier-1 confirmation that "explicit request" and "effective state" can differ.

### 4.4 Draw layers and texture sub-level

Within one frame, regions are ordered by draw layer. `UI.xsd` enumerates
**five**, in this order `[T1 xsd:33-41]`:

```
BACKGROUND  BORDER  ARTWORK  OVERLAY  HIGHLIGHT
```

Within a layer, `textureSubLevel` orders further, and the schema **bounds it
inclusively to −8 … 7** `[T1 xsd:790-796]`. The XML default layer is `ARTWORK`
and the default sub-level is `0` `[T1 xsd:789-790]`. The wiki repeats both the
range and the defaults `[T2 wiki: XML/Layer, revid 6769786, 2026-07-12]`.

Observed sub-levels in the shipped Lua: −8, −1, 1, 2, 3, 6, 7 `[T1 obs:
`SetDrawLayer("X", n)` call census]` — consistent with the schema bound, and
`-8` is actually used (`SetDrawLayer("BACKGROUND", -8)`).

> `[gap]` The XSD gives the five layer names but **does not state that the
> listing order is the z-order**. That BACKGROUND is behind HIGHLIGHT is
> universally-believed and matches the names, but I found no Tier-1 statement
> ordering them, and no Tier-1 statement that `HIGHLIGHT` has special
> mouse-over semantics. Tier 2: `[T2 wiki: XML/Layer]` says `level` "sequences
> graphical regions". `@verify-ingame`.

The Lua pair is `Region:SetDrawLayer(layer, sublevel)` (`:147`) /
`GetDrawLayer() -> layer, sublayer` (`:24`)
`[T1 docs: SimpleRegionAPIDocumentation.lua]`. Draw layer is **not protected and
not secret-bearing**: neither carries `IsProtectedFunction`, neither carries a
`SecretArgumentsAddAspect` or `SecretReturnsForAspect`.
`[corrected 2026-07-23]` The earlier wording "neither is annotated" was wrong —
`SetDrawLayer` does carry `SecretArguments = "AllowedWhenUntainted"` (so tainted
code may not feed it a secret); `GetDrawLayer` genuinely has no annotations.

---

## 5. Textures and their separate channels

A `Texture` composites several *independent* pieces of state. Getting these
straight is the single most error-prone part of the topic.

### 5.1 Channel 1 — the base image

Three writers set the image:

| API | Meaning | Cite |
|---|---|---|
| `SetTexture(textureAsset?, hWrap?, vWrap?, filterMode?) -> success` | file path or FileID; call with no args or `nil` to clear | `[T1 docs: SimpleTextureBaseAPIDocumentation.lua:441; T2 wiki: API TextureBase SetTexture, revid 6654547]` |
| `SetAtlas(atlas, useAtlasSize, filterMode?, resetTexCoords?, hWrapMode?, vWrapMode?)` | a named atlas region (file + tex-coords in one) | `[T1 docs: SimpleTextureBaseAPIDocumentation.lua:278]` |
| `SetColorTexture(r, g, b, a?)` | a solid colour | `[T1 docs: SimpleTextureBaseAPIDocumentation.lua:313]` |

> `[corrected 2026-07-23]` This table used to be headed *"Exactly one of these is
> in force at a time, and each is a full replacement"* and used to include
> `SetMask(file)` (`:370`) as a fourth row. Both were wrong-ish:
> - **`SetMask` is not a base-image writer.** It attaches a mask by path and is
>   orthogonal to `SetTexture`/`SetAtlas`/`SetColorTexture`; it belongs with §5.7.
>   It is listed in `[T2 wiki: XML/Texture, revid 6776374]` as the Lua equivalent
>   of the `mask` **attribute**, alongside `file` and `atlas`, not instead of them.
> - **"Exactly one is in force" is uncited.** It is the near-universal mental
>   model and is consistent with `GetTexture` returning nil after `SetAtlas`, but
>   I could find no Tier-1 or Tier-2 statement of mutual exclusion.
>   `@verify-ingame`: `SetTexture(...)` then `SetAtlas(...)` then read
>   `GetTexture()`/`GetAtlas()`, and the reverse order.
>
> Related and unresolved: `[T2 bug: WoWUIBugs #250, created 2022-08-13, closed,
> labels Bug / Mainline / ✔️ Verifiable Example / Acknowledged by Blizzard]`
> reports that `SetTexture` with the *same* path but different wrap modes is
> ignored — evidence that the setter short-circuits on the asset, not the whole
> argument list. Not re-tested at 12.0.7.

`SetTexture`, `SetAtlas` and `SetColorTexture` all carry
`SecretArguments = "AllowedWhenTainted"` and **no** `SecretArgumentsAddAspect`
`[T1 docs, same file]` — i.e. they accept secret arguments and, having no
connected aspect, that marks the *whole object* as having secret values (§3.3).

Readers: `GetTexture() -> cstring?`, `GetTextureFileID() -> fileID`,
`GetTextureFilePath() -> cstring?`, `GetAtlas() -> textureAtlas` — all
unannotated `[T1 docs: SimpleTextureBaseAPIDocumentation.lua:129 and neighbours]`.

There is also an undocumented global `GetTextureInfo(obj)` — defined at
`[T1 src: Blizzard_SharedXMLBase/TextureUtil.lua:3-26]` and consumed by the
frame-stack tooling at `[T1 src:
Blizzard_DebugTools/Blizzard_TextureInfoGenerator.lua:44-47,59]`. It is **not**
in the generated docs (`wowkb.uiapi missing GetTextureInfo` → "generated docs:
no; UI source hits: 2"). Reading the body — it is 24 lines of plain Lua, so this
is fully determined:

```
GetTextureInfo(obj) -> assetName, assetType, ulX,ulY, blX,blY, urX,urY, brX,brY
  assetType is one of "Atlas" | "File" | "FileID" | "Unknown"   (TextureUtil.lua:6,10,15,20)
  returns NOTHING at all if obj:GetObjectType() ~= "Texture"    (TextureUtil.lua:4,26)
  the 8 coords are a straight passthrough of obj:GetTexCoord()  (TextureUtil.lua:23)
```

`[corrected 2026-07-23]` The `assetType` was previously given as
`("Atlas"|"File")`. There are **four** values — it falls through
`GetAtlas → GetTextureFilePath → GetTextureFileID → "UnknownAsset"` — and the
function returns nil for a non-Texture, so callers must nil-check.

### 5.2 Channel 2 — tex-coords, tiling, slicing, geometry

Independent of channel 1 and of colour:

- `SetTexCoord(left, right, bottom, top)` / `ResetTexCoord()` /
  `SetSpriteSheetCell(cell, rows, cols, w?, h?)`. Note the asymmetry: the
  documented `SetTexCoord` takes **four** numbers (`left, right, bottom, top`,
  `[T1 docs: …:417-429]`), while `GetTexCoord` returns **eight**
  (`ulX, ulY, llX, llY, urX, urY, lrX, lrY`, `[T1 docs: …:95-114]`). An
  eight-argument *setter* form exists and is undocumented — `[corrected
  2026-07-23]` this was previously asserted as "widely used" with no evidence;
  it is now counted: **13 call sites in Blizzard's own shipped Lua**, e.g.
  `[T1 src: Blizzard_FrameXML/EquipmentFlyout.lua:644-647]`, and **21 files**
  across the seven surveyed addon clones `[T3 obs]`. Still absent from the
  generated docs `[gap]`.  Both `SetTexCoord` and
  `SetSpriteSheetCell` are `SecretArguments=AllowedWhenTainted` +
  `SecretArgumentsAddAspect={Enum.SecretAspect.TexCoords}`, and `GetTexCoord` is
  `SecretReturnsForAspect={TexCoords}` `[T1 docs:
  SimpleTextureBaseAPIDocumentation.lua]`.
- `SetHorizTile` / `SetVertTile` + the six `WRAPMODE` values
  `CLAMP, REPEAT, CLAMPTOBLACK, CLAMPTOBLACKADDITIVE, CLAMPTOWHITE, MIRROR`
  `[T1 xsd:136-145]`; semantics of each per `[T2 wiki: API TextureBase
  SetTexture, revid 6654547]`.
- `SetTextureSliceMargins(l,t,r,b)` + `SetTextureSliceMode(mode)` +
  `ClearTextureSlice()`, where `Enum.UITextureSliceMode` = `{Stretched = 0,
  Tiled = 1}` `[T1 docs: UITextureConstantsDocumentation.lua:6]`. This is the
  single-texture nine-slice, distinct from the nine-*region* `NineSliceUtil`.
- `SetVertexOffset(vertexIndex, x, y)` / `GetVertexOffset` / `ClearVertexOffsets`
  — per-corner quad distortion. `GetVertexOffset` is `ConstSecretAccessor`.
- `SetRotation(radians, normalizedRotationPoint?)`, aspect `Rotation`.
- `SetBlendMode(blendMode)`; the XML spelling is `alphaMode` with five values
  `DISABLE, BLEND, ALPHAKEY, ADD, MOD`, default `BLEND` `[T1 xsd:43-51, :550]`.
- `SetSnapToPixelGrid(snap)` (XML `snapToPixelGrid`, default `true`) and
  `SetTexelSnappingBias(bias)` `[T1 xsd:554-555]`.

### 5.3 Channel 3 — per-vertex colour, and Channel 4 — alpha

**These live on `Region`, not on `TextureBase`** — which is why they also apply
to FontStrings and Lines.

```
Region:SetVertexColor(r, g, b, a?)               SecretArguments=AllowedWhenTainted
                                                 SecretArgumentsAddAspect={VertexColor, Alpha}
Region:SetVertexColorFromBoolean(v, cTrue, cFalse)   same annotations
Region:GetVertexColor() -> r,g,b,a               MayReturnNothing=True
                                                 SecretReturnsForAspect={VertexColor, Alpha}
Region:SetAlpha(alpha)                           SecretArguments=AllowedWhenTainted
                                                 SecretArgumentsAddAspect={Alpha}
Region:SetAlphaFromBoolean(v, aTrue, aFalse)     same
Region:GetAlpha() -> SingleColorValue            SecretReturnsForAspect={Alpha}
```
`[T1 docs: SimpleRegionAPIDocumentation.lua — GetAlpha, GetVertexColor,
SetAlpha, SetAlphaFromBoolean, SetVertexColor, SetVertexColorFromBoolean]`

`TextureBase:SetGradient(orientation, minColor, maxColor)` also writes colour,
but Tier 1 treats it **differently**: it carries
`SecretArguments = "AllowedWhenUntainted"` and **no**
`SecretArgumentsAddAspect` at all `[T1 docs:
SimpleTextureBaseAPIDocumentation.lua:348-358]`. It is also **write-only** —
across the whole generated corpus there is exactly one `SetGradient` on textures
and **no `GetGradient` and no `ClearGradient`** (`wowkb.uiapi func 'Gradient'`
returns 10 matches: `SetGradient` ×1 on TextureBase, `SetGradientMask`/
`SetGradientMaskWithDyes` on models/actors, and the FontString/Frame
`*AlphaGradient` family). Contrast `FontString:ClearAlphaGradient()` and
`Frame:ClearAlphaGradient()`, which do exist `[T1 docs:
SimpleFontStringAPIDocumentation.lua:55, SimpleFrameAPIDocumentation.lua:32]`.

How the channels compose, per Tier 2: vertex colour is a **multiplicative
filter** over the base image — "Each color component of the object will be
multiplied by the value given… setting (1.0, 1.0, 0.0) on a white object will
color it yellow. But doing the same thing on a blue object will make it black."
`[T2 wiki: API Region SetVertexColor, revid 6654858, 2026-02-19]`. And gradient
is the same kind of thing: "Gradient color shading does not change the
underlying color of the texture image, but acts as a filter; see
Region:SetVertexColor for details." `[T2 wiki: API TextureBase SetGradient,
revid 6654937, 2026-02-19]`.

> `[gap] — this is the load-bearing unknown of the section.` **Whether
> `SetVertexColor` and `SetGradient` write the same storage** (so the later call
> wins) or two composable slots is **not established by any source I could
> reach.** Tier 1 gives only that they sit on different types, have different
> security annotations, and that only one of them is readable. Tier 2 says both
> are multiplicative filters, which is consistent with either. I looked in:
> `UI.xsd`, all 593 generated doc files, the shipped Lua (there is no Blizzard
> file that applies both to the same texture — the only `SetGradient` call sites
> are `[T1 src: Blizzard_NamePlates/Blizzard_NamePlates.lua:519-520]`), the
> wiki pages for both methods, and WoWUIBugs.
> `@verify-ingame`: create a white 8×8 texture, `SetVertexColor(1,0,0)`, then
> `SetGradient("HORIZONTAL", yellow, blue)`, then `GetVertexColor()`; then
> reverse the order. Record whether the red tint survives the gradient and what
> the getter reports.

Alpha propagation: a frame's alpha applies to its descendants
`[T2 wiki: API Region SetAlpha, revid 6654851, 2026-02-19, citing the 2.1.0
change]`. Tier 1 corroborates that propagation exists, because there is an
explicit opt-out on both the region and the XML side —
`Region:SetIgnoreParentAlpha(ignore)` / `IsIgnoringParentAlpha()`
`[T1 docs: SimpleRegionAPIDocumentation.lua:158 and neighbour]` and
`ignoreParentAlpha` on `TextureAttributes` `[T1 xsd:558]`, `FrameAttributes`
`[T1 xsd:738]` and `FontStringType` `[T1 xsd:667]`
(`[corrected 2026-07-23]` — the texture-side line was cited as `:556`, which is
`hWrapMode`). Same story for scale (`SetIgnoreParentScale`,
`ignoreParentScale`), except `SetIgnoreParentScale` is additionally
`IsProtectedFunction = True` + `SecretArguments = NotAllowed`
`[T1 docs: SimpleRegionAPIDocumentation.lua]`.

The same wiki page records a 12.0.0 behaviour change: **`SetAlpha` now clamps to
[0, 1] silently instead of raising an error** (10.0.0 threw)
`[T2 wiki: API Region SetAlpha, revid 6654851]`.

### 5.4 FontString colour is the same annotation set as vertex colour

```
FontString:SetTextColor(r,g,b,a?)   SecretArguments=AllowedWhenTainted
                                    SecretArgumentsAddAspect={VertexColor, Alpha}
FontString:GetTextColor()           MayReturnNothing=True
                                    SecretReturnsForAspect={VertexColor, Alpha}
```
`[T1 docs: SimpleFontStringAPIDocumentation.lua — SetTextColor, GetTextColor]`

That is **byte-for-byte the annotation set of `Region:SetVertexColor` /
`GetVertexColor`** (§5.3), including the unusual `MayReturnNothing` on the
getter. Since `FontString` inherits `Region` `[T2 res: WidgetAPI.lua:170-171]`,
a FontString has both methods.

> `[gap]` "Identical annotations ⇒ identical storage" is inference, not a cited
> fact. Neither the wiki's `API FontInstance SetTextColor` (revid 6654635,
> 2026-02-19) nor `API FontString SetTextColor` (revid 4473731, **2021-08-09**,
> effectively abandoned) says anything about the relationship.
> `@verify-ingame`: `fs:SetTextColor(1,0,0)` then `fs:GetVertexColor()`, and the
> reverse.

FontString also has `SetFixedColor(fixedColor)` and an `OnColorsUpdated()` hook
`[T1 docs: SimpleFontStringAPIDocumentation.lua]`, neither of which I could find
prose for at any tier — `[gap]`.

### 5.5 XML `<Color>` and `<Gradient>`

Both are `TextureField` child elements of `<Texture>` `[T1 xsd:607 (Color),
:608 (Gradient)]`; `<Gradient>` has `orientation` (default `HORIZONTAL`) and
`<MinColor>` / `<MaxColor>` children `[T1 xsd:277-285]`. `<Color>` takes
`r g b a` (defaults `0,0,0,1`) **or** a named `color` (a `ColorMixin` global made
with `CreateColor`); setting both rgb and `color` is an error
`[T2 wiki: XML/Color, revid 6771907, 2026-07-15]`.

The wiki's `XML/Texture` attribute table has a "Lua Equivalent" column, and the
`<Color>` child element (transcluded from `XML/Color`) has **no Lua equivalent
given anywhere** `[T2 wiki: XML/Texture, revid 6776374, 2026-07-19;
XML/Color, revid 6771907]`. `[corrected 2026-07-23]` The earlier phrasing —
"gives a Lua-Equivalent for every *attribute* but leaves it blank for `<Color>`"
— overstated the contrast: `alphaMode`, `noanimalpha`, `nolazyload` and
`nounload` also have blank Lua-Equivalent cells on that same table. The blank
cell is therefore weaker evidence than it looked; the Tier-1 evidence below is
what carries the point.

What Tier 1 does establish: **`<Color>` cannot simply be replacing the image**,
because Blizzard ships textures that carry *both* a `file` and a `<Color>`:

- `[T1 src: Blizzard_UIPanelTemplates/Mainline/UIPanelTemplates.xml:1261-1263]`
  — a `GuildFrame` texture with `TexCoords` and `<Color r="1.0" g="0.7567"
  b="0.0" a="1"/>` (a gold tint).
- `[T1 src: Blizzard_FrameXML/ArchaeologyProgressBar.xml:45-47]` — a
  `parentKey="Shadow"` texture with `file="…ArcheologyToast"` and
  `<Color r="0" g="0" b="0"/>` (a black silhouette of the same art).

And a texture with **no** `file` plus a `<Color>` renders as a flat fill:
`[T1 src: Blizzard_ReforgingUI/Classic/Blizzard_ReforgingUI.xml:176-177]`
(`MissingFadeOut`, `<Color r="0" g="0" b="0" a="0.5"/>`).

401 shipped XML files contain a `<Color ` element `[T1 obs]`.

> `[gap]` Whether `<Color>` compiles to `SetVertexColor` or `SetColorTexture` is
> **not stated** by `UI.xsd` or by the wiki. The evidence above rules out "plain
> `SetColorTexture` replacement", but does not distinguish "`SetVertexColor`"
> from "`SetColorTexture` only when no file/atlas is given". `@verify-ingame`:
> load a texture from XML with both `file` and `<Color>`, then read
> `GetTexture()` and `GetVertexColor()`.

### 5.6 Desaturation

`SetDesaturated(bool)` and `SetDesaturation(0..1)` both add the
`Desaturation` aspect; `GetDesaturation()` returns for that aspect;
`IsDesaturated()` additionally carries the precondition
`RequiresScriptObjectDesaturationAccess`, whose failure mode is
`ReturnWithError` `[T1 docs: SimpleTextureBaseAPIDocumentation.lua —
SetDesaturated/SetDesaturation/GetDesaturation/IsDesaturated;
SecretPredicatesDocumentation.lua:32-35]`. There is a frame-wide
`Frame:DesaturateHierarchy(desaturation, excludeRoot)`
`[T1 docs: SimpleFrameAPIDocumentation.lua:137]`.

### 5.7 Masks

`MaskTexture` is a `TextureBase` sibling of `Texture` `[T2 res:
WidgetAPI.lua:262-263]`. Attachment is on `Texture` only —
`AddMaskTexture(mask)`, `RemoveMaskTexture(mask)`, `GetMaskTexture(index)`,
`GetNumMaskTextures()` `[T1 docs: SimpleTextureAPIDocumentation.lua:3]`. Both
getters are `SecretReturnsForAspect = {Enum.SecretAspect.Hierarchy}`, so mask
membership is treated as hierarchy information. `SimpleMaskTextureAPI` itself
declares **zero** methods `[T1 docs: SimpleMaskTextureAPIDocumentation.lua:3]`
— a MaskTexture is configured entirely through its inherited TextureBase/Region
methods. In XML the binding is the other way round: `<MaskTexture>` carries a
`<MaskedTextures><MaskedTexture childKey= target=/></MaskedTextures>` block
`[T1 xsd:611-636]`.

---

## 6. Fonts

### 6.1 Three things called "font"

1. **`FontString`** — a `Region` that draws text.
2. **`Font` object** — a shared, named style holder (`FrameScriptObject` +
   `FontInstance`) `[T2 res: WidgetAPI.lua:159-160]`. Created by the global
   `CreateFont(name)`, which is **not in the generated docs** and appears exactly
   twice in the shipped source `[T1 src:
   Blizzard_SharedXML/FontableFrameMixin.lua:120,131]`.
3. **`FontInstance`** — the interface both share, plus `EditBox`,
   `MessageFrame` and `SimpleHTML` `[T2 res: WidgetAPI.lua:136,983,1063,1083]`.

`FontInstance` methods `[T1 docs: SimpleFontAPIDocumentation.lua:3…]`:
`GetFont`/`SetFont`, `GetFontHeight`/`SetFontHeight`,
`GetFontObject`/`SetFontObject`, `CopyFontObject`, `GetFontObjectForAlphabet`,
`GetJustifyH`/`V` + setters, `GetShadowColor`/`SetShadowColor`,
`GetShadowOffset`/`SetShadowOffset`, `GetSpacing`/`SetSpacing`,
`GetTextColor`/`SetTextColor`, `GetIndentedWordWrap`/`SetIndentedWordWrap`,
`GetAlpha`/`SetAlpha`.

`SetFont(fontFile, height, flags)` carries **two preconditions**,
`RequiresValidFontAsset` and `RequiresValidFontHeight`
`[T1 docs: SimpleFontAPIDocumentation.lua — SetFont;
SimpleFontStringAPIDocumentation.lua — SetFont, which additionally returns
`success: bool`]`. 12.0.7 improved the failure message: "`SetFont` has more
informative error messaging when supplied invalid font flag names"
`[Tier-1 content via Tier-2 archive: `Patch 12.0.7/API changes`, revid 6778033,
2026-07-22]`.

System-level font APIs `[T1 docs: FontDocumentation.lua]`:
`GetFonts() -> table` (`:41`), `GetFontInfo(fontObject) -> FontScriptInfo?`,
`CreateFontFamily(name, members) -> SimpleFont` (`:10`). `FontScriptInfo` =
`{color: colorRGBA, height: number, outline: string, shadow:
FontScriptShadowInfo?, fontObject: SimpleFont, canBeUserScaled: bool}`
`[T1 docs: FontDocumentation.lua:69]`. XML's `<FontFamily>` with `<Member>`
elements is the markup counterpart `[T1 xsd:453-463]`, with an alphabet
enumeration `roman, korean, simplifiedchinese, traditionalchinese, russian`
`[T1 xsd:126-134]`.

### 6.2 FontString text metrics and layout

XML attributes with their defaults `[T1 xsd:638-675]`: `font`, `bytes` (255),
`text`, `spacing` (0), `outline` (`NONE`; enum `NONE|NORMAL|THICK` at
`UI.xsd:53-59`), `monochrome` (false), `nonspacewrap` (false), `wordwrap`
(**true**), `justifyV` (`MIDDLE`), `justifyH` (`CENTER`), `maxLines` (0),
`indented` (false), `alpha` (1.0), `degrees` (0), `scaleAnimationMode`
(`FontSize`; enum `FontSize|Vertex` at `UI.xsd:154-159`), `smoothScaling`
(false).

Measurement methods are **all** `SecretWhenAnchoringSecret`: `GetStringWidth`,
`GetStringHeight`, `GetUnboundedStringWidth`, `GetUnboundedStringWidthForText`,
`GetWrappedWidth`, `GetNumLines`, `IsTruncated`
`[T1 docs: SimpleFontStringAPIDocumentation.lua]`. `GetText` is
`SecretReturnsForAspect = {Enum.SecretAspect.Text}`; `SetText`,
`SetFormattedText` and `SetTextToFit` accept secrets and add the `Text` aspect.
`CalculateScreenAreaFromCharacterSpan` and `FindCharacterIndexAtCoordinate` carry
the precondition `RequiresFontStringTextAccess`, defined as *"Guarded APIs
reject access for tainted callers if the object has the secret Text aspect
assigned"*, failure mode `ReturnNothing`
`[T1 docs: SecretPredicatesDocumentation.lua:21-25]`.

### 6.3 Media

**File formats.** Custom images must be BLP, JPEG, PNG or TGA with
power-of-two dimensions; PNG requires an explicit `.png` extension in the path
`[T2 wiki: API TextureBase SetTexture, revid 6654547, 2026-02-19]`. Not stated
at Tier 1 anywhere I looked — `[gap]`.

**Asynchronous loading is Tier-1-visible.** `Region:IsObjectLoaded()`
`[T1 docs: SimpleRegionAPIDocumentation.lua]`, plus
`SetBlockingLoadsRequested(blocking)` / `IsBlockingLoadRequested()` on
TextureBase, plus the XML `nonBlocking` `[T1 xsd:560]`, `nolazyload`
`[T1 xsd:567]` and `nounload` `[T1 xsd:568]` attributes
(`[corrected 2026-07-23]` — previously cited as `:558,566-568`; `:558` is
`ignoreParentAlpha` and `:566` is `noanimalpha`), plus
`TextureLoadingGroupMixin` `[T1 src: Blizzard_SharedXML/MixinUtil.lua:302-326]`.
Tier 2 spells out the
consequence: `texture:GetSize()` returns `0,0` until `IsObjectLoaded()` is true
`[T2 wiki: API TextureBase SetTexture, revid 6654547]`.

**New in 12.0.7 — path validation before use.** `C_UIFileAsset` with three
functions `[T1 docs: UIFileAssetAPIDocumentation.lua:3]`:

```
C_UIFileAsset.GetFileID(asset)    -> fileID?     -- nil if unknown to the client
C_UIFileAsset.IsKnownFile(asset)  -> bool        -- shipped data or known loose file
C_UIFileAsset.IsLooseFile(asset)  -> bool        -- locally known loose (non-shipped) file
```

Blizzard's stated purpose: *"to help addons validate font and texture paths
before using them"* `[Tier-1 content via Tier-2 archive: `Patch 12.0.7/API
changes`, revid 6778033, 2026-07-22, §File Asset APIs]`.

**Atlases.** `C_Texture.GetAtlasInfo(atlas) -> AtlasInfo` (`MayReturnNothing`),
`GetAtlasExists`, `GetAtlasElements`, `GetAtlasElementID`, `GetAtlasID`,
`GetFilenameFromFileDataID` `[T1 docs: TextureUtilsDocumentation.lua:3…]`.
`AtlasInfo` = `{elementName, width, height, rawSize, leftTexCoord,
rightTexCoord, topTexCoord, bottomTexCoord, tilesHorizontally, tilesVertically,
file?, filename?, sliceData?}` `[T1 docs: TextureUtilsDocumentation.lua:204]`.

**Shared media across addons** is a library convention, not an API.
`LibSharedMedia-3.0` defines five media types — `background`, `border`, `font`,
`statusbar`, `sound` — and a `Register/Fetch/List/HashTable/IsValid` interface
`[T3: as shipped in Bartender4 on this install,
`_retail_/Interface/AddOns/Bartender4/libs/LibSharedMedia-3.0/LibSharedMedia-3.0.lua:54-58,
:239 (Register), :275 (Fetch), :282 (IsValid), :286 (HashTable), :290 (List)]`.
`[corrected 2026-07-23]` It is vendored into **5** addon folders on this install,
not 8 — Bartender4, BigWigs, DandersFrames, EllesmereUI, TellMeWhen
`[T1 obs: find -iname '*LibSharedMedia*' under _retail_/Interface/AddOns]`.
Its `Register` refuses any background/border/statusbar/sound
path that does not match `^interface` and any sound that is not `.ogg`/`.mp3`
`[T3: same file, :251-261]` — that is the *library's* policy; I found no Tier-1
or Tier-2 statement that the client itself enforces either rule. `[gap]`
Upstream is CurseForge SVN, so the only readable copies are the vendored ones.

---

## 7. Animations

### 7.1 Structure

An **AnimationGroup** hangs off any `AnimatableObject` and contains ordered
**Animation**s. `[corrected 2026-07-23]` The widget list used to be given bare;
the generated docs do not encode inheritance (§1.1) and `AnimatableObject` does
**not** appear in `WidgetAPI.lua` at all, so the set rests on Tier 2: the wiki
transcludes `UIOBJECT_AnimatableObject` into `Frame` (revid 6750022),
`FontString` (6750105), `Line` (6750104), `MaskTexture` (6750102) and `Texture`
(6777822) — all last edited 2026-06-20 or later. **MaskTexture** was missing from
the old list. Creation:

```
AnimatableObject:CreateAnimationGroup(name?, templateName?) -> SimpleAnimGroup   [SecretArguments=NotAllowed]
AnimatableObject:GetAnimationGroups() -> SimpleAnimGroup
AnimatableObject:StopAnimating()
AnimGroup:CreateAnimation(animationType?, name?, templateName?) -> SimpleAnim    [SecretArguments=NotAllowed]
```
`[T1 docs: SimpleAnimatableObjectAPIDocumentation.lua:3;
SimpleAnimGroupAPIDocumentation.lua:3]`

Ten animation types, all extending `AnimationType` `[T1 xsd:1473-1595]`. Line
numbers are the `<xs:complexType name="…Type">` line —
`[corrected 2026-07-23]`, seven of the ten were previously off by one (they
pointed at the `<xs:complexContent>` line inside the type):

| Type | Distinguishing attributes | XSD |
|---|---|---|
| `Translation` | `offsetX` (0.0), `offsetY` (0.0) | `:1473` |
| `LineTranslation` | (extends Translation, adds nothing) | `:1483` |
| `Rotation` | `degrees` (0.0), `radians` (0.0) | `:1490` |
| `Scale` | `scaleX/Y`, `fromScaleX/Y`, `toScaleX/Y` (all 1.0) | `:1500` |
| `LineScale` | (extends Scale, adds nothing) | `:1514` |
| `Alpha` | `fromAlpha` (0.0), `toAlpha` (1.0) | `:1521` |
| `Path` | `<ControlPoints>`, `curve` (`NONE`\|`SMOOTH`, default `NONE`) | `:1546` |
| `FlipBook` | `flipBookRows/Columns/Frames/FrameWidth/FrameHeight` (all 0) | `:1560` |
| `VertexColor` | `<StartColor>`, `<EndColor>` | `:1573` |
| `TextureCoordTranslation` | `offsetU` (0), `offsetV` (0) | `:1587` |

Shared `Animation` attributes `[T1 xsd:1447-1469]`: `name`, `mixin`,
`secureMixin`, `inherits`, `virtual`, `target`, `targetKey`, `parentKey`,
`childKey`, `startDelay` (0), `endDelay` (0), `duration`, `order` (default 1,
**bounded 0–100** by `AnimOrderType` at `UI.xsd:1405-1410`), `smoothing`
(default `NONE`).

`ANIMSMOOTHTYPE` = `NONE | IN | OUT | IN_OUT | OUT_IN` `[T1 xsd:1388-1396]`.
`ANIMLOOPTYPE` = `NONE | REPEAT | BOUNCE` `[T1 xsd:1380-1386]`.
`AnimationGroup` attributes: `looping` (default `NONE`) and `setToFinalAlpha`
(default `false`) `[T1 xsd:1611-1612]`.

### 7.2 Scripts

Animation: `OnLoad, OnPlay, OnPause, OnStop, OnUpdate, OnFinished`
`[T1 xsd:1412-1423]`.
AnimationGroup: the same six **plus `OnLoop`** `[T1 xsd:1425-1437]`.
`OnLoop` exists only on the group — a checkable asymmetry.

### 7.3 Runtime control

```
AnimGroup: Play(reverse, offset) / Pause / Stop / Restart(reverse, offset) / Finish
           SetPlaying(bool)                     :308  AllowedWhenUntainted
           SetLooping(LoopType)                 :298  SecretArguments=NotAllowed
           SetToFinalAlpha(bool) / IsSetToFinalAlpha()
           SetAnimationSpeedMultiplier(x) / GetAnimationSpeedMultiplier()
           GetDuration / GetElapsed / GetProgress / GetLoopState / GetLooping
           IsPlaying / IsPaused / IsDone / IsReverse / IsPendingFinish
           GetAnimations() / RemoveAnimations()
Anim:      Play / Pause / Stop / Restart / SetPlaying(bool)
           SetDuration(sec, recomputeGroupDuration) / SetStartDelay / SetEndDelay
           SetOrder(n) / SetSmoothing(weights) / SetSmoothProgress(sec)
           SetTarget / SetTargetKey / SetTargetName / SetTargetParent / SetChildKey
           SetParent(group, order?)
           GetProgress / GetSmoothProgress / GetElapsed / GetRegionParent / GetTarget
           IsDelaying / IsDone / IsPaused / IsPlaying / IsStopped
```
`[T1 docs: SimpleAnimGroupAPIDocumentation.lua:3…, SimpleAnimAPIDocumentation.lua:3…]`

Security annotations on the animation surface are sparse and specific. The
complete `SecretArguments = "NotAllowed"` set across the five animation doc
tables is **exactly seven** entries `[T1 obs over the generated docs]`:
`Anim:SetOrder` (`:312`), `Anim:SetEndDelay` (`:301`), `Anim:SetPlaying`
(`:333`), `Anim:SetSmoothProgress` (`:354`), `AnimGroup:SetLooping` (`:298`),
`AnimGroup:CreateAnimation` (`:10`) and
`AnimatableObject:CreateAnimationGroup` (`:10`). Note the `SetPlaying`
asymmetry: **`Anim:SetPlaying` is `NotAllowed`, `AnimGroup:SetPlaying` is
`AllowedWhenUntainted`.** `Anim:SetDuration` (`:290`) and `Anim:SetStartDelay`
(`:374`) are `AllowedWhenUntainted`, i.e. **not** rejected outright.
The `VertexColor` animation's `SetStartColor` / `SetEndColor` are
`SecretArguments = "AllowedWhenTainted"`
`[T1 docs: SimpleAnimVertexColorAPIDocumentation.lua:3]`. The `Alpha`
animation's `SetFromAlpha`/`SetToAlpha` are `NotAllowed`
`[T1 docs: SimpleAnimAlphaAPIDocumentation.lua:3]`.

**Animations are a third writer to the colour channels.** A `VertexColor`
animation drives the same per-vertex colour that `Region:SetVertexColor` writes,
and an `Alpha` animation drives region alpha. `setToFinalAlpha` exists precisely
because the default is *not* to keep the final value `[T1 xsd:1612]`. Combined
with §5.3's open question, treat "who owns the colour of this texture right now"
as something to decide once per widget, not per call site.

> `[gap]` I could not find, at any tier, a statement of what an alpha or
> vertex-colour animation does to the underlying value when it stops **without**
> `setToFinalAlpha`. The attribute's existence implies restoration, but that is
> inference. `@verify-ingame`.

Related bug worth knowing: `SetParent` on a FlipBook animation could crash the
client `[T2 bug: WoWUIBugs #474, closed, labels Bug/Mainline/Classic/Stale]`.

### 7.4 Interpolation without animations

`Blizzard_SharedXML/Interpolator.lua` and `EasingUtil.lua` provide
frame-by-frame interpolation as an alternative to the AnimationGroup system
`[T1 src: Blizzard_SharedXML/Interpolator.lua, EasingUtil.lua]`.

Tier-3 practice: all 7 surveyed addons except Ace3 build AnimationGroups —
file counts mentioning `CreateAnimationGroup`: WeakAuras 3, BigWigs 8,
Details 8, Plater 5, ElvUI 8, oUF 1, Ace3 0 `[T1 obs]`.

---

## 8. Skinning and attaching to Blizzard's frames

### 8.1 What is reachable

Blizzard's UI ships **317 `Blizzard_*` addons** inside the client's CASC
archives, not on disk `[T1 obs]`. Their frames are ordinary widgets and are
reachable by global name or `parentKey` walk — except:

- **Forbidden frames.** `FrameScriptObject:IsForbidden()` /
  `SetForbidden()` `[T1 docs: SimpleFrameScriptObjectAPIDocumentation.lua:83,
  :128]`, with `IsForbidden` returning for the `ObjectSecurity` aspect.
  `CreateForbiddenFrame` is what creates them (§2.1).
  `[corrected 2026-07-23]` The sentence "Touching one from addon code errors"
  was uncited and has been cut. What Tier 1 actually gives is only the
  *existence* of the flag and its getter/setter, plus `IsForbidden` returning
  for the `ObjectSecurity` aspect. What happens on access is
  `security-taint-and-restricted-data.md`'s subject — do not restate it here.
  `[gap]`
- **Protected frames in combat.** All the geometry and visibility mutators are
  `IsProtectedFunction = true` (§3.1, §4.2). See
  `security-taint-and-restricted-data.md` §1.1 for the enumerated 59.

### 8.2 The taint hazard specific to rendering

Reading *and writing back* a Blizzard layout table from insecure code taints it
permanently for every later consumer. The canonical case is `NineSliceUtil`:
`PropagateLayoutSettingsToPieceLayout` used to write `pieceLayout.mirrorLayout =
userLayout.mirrorLayout` when the piece value was nil, so an addon creating any
`ButtonFrameTemplate`-derived frame tainted the shared layout table and every
subsequent Blizzard use of that layout
`[T2 bug: WoWUIBugs #107, created 2021-04-21, labels Bug / ✔️ Verifiable Example
/ Acknowledged by Blizzard]`.

**That one is fixed.** In the 12.0.7 source there is no
`PropagateLayoutSettingsToPieceLayout` at all; the mirror flag is read from both
tables without mutating either:

```lua
local pieceMirrored = pieceLayout.mirrorLayout;
if ... then
    pieceMirrored = userLayout and userLayout.mirrorLayout;
```
`[T1 src: Blizzard_SharedXML/NineSlice.lua:61-63]` — i.e. the reporter's
"Option 2" was adopted. The *pattern* remains the lesson: a shared Blizzard
table that is lazily back-filled is a taint vector.

### 8.3 Backdrops

`SetBackdrop` is **not a widget method.** It has no generated-doc entry, and the
only definition in the shipped source is
`[T1 src: Blizzard_SharedXML/Backdrop.lua:336]`, a method on
`BackdropTemplateMixin`. To get it you inherit the virtual `BackdropTemplate`
frame `[T1 src: Blizzard_SharedXML/Backdrop.xml:5-8]`, which supplies
`SetBackdrop`, `GetBackdrop`, `ClearBackdrop`, `ApplyBackdrop`,
`SetBackdropColor`, `GetBackdropColor`, `SetBackdropBorderColor`,
`GetBackdropBorderColor`, `SetBorderBlendMode`, `HasBackdropInfo`
`[T1 src: Backdrop.lua:285,289,301,336,354,397,406,416,429,273]`. The file also
exports **17** `BACKDROP_*` preset tables `[T1 src: Backdrop.lua:1-140,
`grep -c '^BACKDROP_'` = 17]` — `[corrected 2026-07-23]`, previously written as
"~dozens".

### 8.4 Hooking, in practice

Tier-3 file counts mentioning `hooksecurefunc` `[T1 obs]`: ElvUI **274**,
Details 13, Plater 11, Ace3 6, WeakAuras 4, oUF 1, BigWigs **0**. ElvUI is an
outlier by two orders of magnitude because skinning Blizzard frames *is* its
product. BigWigs at zero is the interesting data point: a large, mature addon
that ships no hooks into Blizzard's UI at all. Neither is a rule.

`hooksecurefunc` is not in the generated docs; see
`security-taint-and-restricted-data.md`.

---

## 9. Object and frame pooling

`Blizzard_SharedXMLBase/Pools.lua` (866 lines) is the whole system, and it was
**substantially rewritten for the secret-values era** (proxies, secure
containers, secret-release guards).

> `[corrected 2026-07-23]` This section used to open "If you learned pools before
> Midnight, most of what you know about the *names* is wrong." That overstates
> it. **Every** legacy constructor name still exists and still works — they are
> aliases (§9.1). Exactly one name in the pool surface is known to have gone
> away: the resetter `FramePool_HideAndClearAnchors` (§9.2). What changed
> underneath the names — the proxy, the eight-method surface, the
> secret-release assert — is the real story.

### 9.1 The constructor set at 12.0.7

```lua
-- secure (proxied) variants -- these are the real implementations
CreateSecureObjectPool(createFunc, resetFunc, capacity)                                    Pools.lua:732
CreateSecureFramePool(frameType, parent, template, resetFunc, forbidden, postCreate, cap)  Pools.lua:736
CreateSecureTexturePool(parent, layer, subLayer, template, resetFunc, capacity)            Pools.lua:740
CreateSecureFontStringPool(parent, layer, subLayer, template, resetFunc, capacity)         Pools.lua:744
CreateSecureActorPool(parent, template, resetFunc, capacity)                               Pools.lua:748
CreateSecureMaskTexturePool(parent, layer, subLayer, template, resetFunc, capacity)        Pools.lua:752
CreateSecureFramePoolCollection() / CreateSecureFontStringPoolCollection()                 Pools.lua:801,805

-- unsecured variants (no proxy, no secret guards)
CreateUnsecuredObjectPool / CreateUnsecuredTexturePool / CreateUnsecuredFontStringPool
CreateUnsecuredFramePool / CreateUnsecuredMaskTexturePool / CreateUnsecuredFramePoolCollection
                                                            Pools.lua:810, 816, 824, 832, 840, 846

-- the legacy names are ALIASES to the secure variants
CreateObjectPool            = CreateSecureObjectPool             Pools.lua:856
CreateFramePool             = CreateSecureFramePool              Pools.lua:857
CreateTexturePool           = CreateSecureTexturePool            Pools.lua:858
CreateFontStringPool        = CreateSecureFontStringPool         Pools.lua:859
CreateActorPool             = CreateSecureActorPool              Pools.lua:860
CreateFramePoolCollection   = CreateSecureFramePoolCollection    Pools.lua:861
CreateFontStringPoolCollection = CreateSecureFontStringPoolCollection  Pools.lua:862
CreateMaskTexturePool       = CreateSecureMaskTexturePool        Pools.lua:863
```
`[T1 src: Blizzard_SharedXMLBase/Pools.lua]`, with Blizzard's own comment above
the alias block: *"Aliases until we determine if we want to change any code to
explicitly create the secure or unsecured variant of pools and pool
collections."* `[T1 src: Pools.lua:854-855]`.

### 9.2 The resetter renames — this breaks real addons

```lua
function Pool_HideAndClearAnchors(pool, region)      -- Pools.lua:519
    region:Hide();
    region:ClearAllPoints();
end

function Pool_HideAndSetToDefaults(pool, region)     -- Pools.lua:524
    region:SetToDefaults();
    region:Hide();
end

function ActorPool_HideAndClearModel(actorPool, actor)  -- Pools.lua:562
    actor:ClearModel();
    actor:Hide();
end
```

**`FramePool_HideAndClearAnchors` no longer exists.** `wowkb.uiapi missing
FramePool_HideAndClearAnchors` → *"generated docs: no / UI source hits: 0 / NOT
FOUND in either"*. Shipped addons on this install compat-guard the rename by
hand:

```lua
(FramePool_HideAndClearAnchors or Pool_HideAndClearAnchors)(pool, obj)
```
`[T1 obs: _retail_/Interface/AddOns/Auctionator/Source/Groups/View.lua:11;
Baganator/ItemViewCommon/Pools.lua:14,27,40,51,59;
Syndicator/Search/UI/Builder.lua:1026,1031]` — three independent addons, eight
call sites.

### 9.3 What a resetter actually has to clear

The default resetter is **not the same for every pool kind**:

| Pool kind | Default `resetFunc` | Cite |
|---|---|---|
| Object pool | `nop` — **nothing at all** | `Pools.lua:532` |
| Region pool (frame/texture/fontstring/masktexture) | `Pool_HideAndClearAnchors` | `Pools.lua:537` |
| Actor pool | `ActorPool_HideAndClearModel` | `Pools.lua:572` |

So the default region reset performs exactly two operations: `Hide()` and
`ClearAllPoints()`. It does **not** clear size, scale, alpha, vertex colour,
texture/atlas, tex-coords, desaturation, rotation, draw layer, frame level,
scripts, registered events, attributes, or any Lua field you put on the table.
Anything you set on an acquired object and do not clear will be visible to the
next acquirer.

The thorough option is `Pool_HideAndSetToDefaults`, which calls
`FrameScriptObject:SetToDefaults()` — documented as *"Reset all script
accessible values to their default values. If possible, clears secret states"*,
and itself `IsProtectedFunction = true`
`[T1 docs: SimpleFrameScriptObjectAPIDocumentation.lua:136]`.

**Third-party decorations on release.** Nothing in the pool machinery touches
foreign state: neither default resetter iterates regions or children, and
`Release` calls only `CallReset(object)` then `ReclaimObject(object)`
`[T1 src: Pools.lua:96-105]`. A texture, glow, or overlay another addon parented
to a pooled frame therefore **survives release and reappears on the next
acquire**, still parented, still anchored, unless the pool's own resetter was
written to remove it. Blizzard's resetter cannot know about it.

### 9.4 Lifecycle details worth knowing

- `Acquire()` calls the reset function **only for freshly created objects**
  (`if new then … self:CallReset(object, new) end`) — recycled objects were
  already reset at `Release` `[T1 src: Pools.lua:41-70]`.
- Reset is called *before* any pool bookkeeping is mutated, deliberately:
  *"The reset function will error if forbidden actions are attempted insecurely…
  If an error is thrown, it will do so before we make any further modifications
  to this pool. Note this does create a potential for a dangling frame or region,
  but that is less of a concern than mutating the pool."*
  `[T1 src: Pools.lua:57-64, and again :97-101]`
- Releasing an untracked object asserts:
  `"Attempted to release inactive object '%s'"` /
  `"Attempted to release object '%s' that doesn't belong to this pool"`
  `[T1 src: Pools.lua:33-39, :89]`.
- **Secret objects cannot enter a secure pool**: `CheckAllowReleaseObject`
  asserts `"attempted to release a secret value into a pool: %s"` because
  *"if one secret object enters a pool, all future acquisitions end up being
  secret too"* `[T1 src: Pools.lua:265-279]`.
- Pools are **only allowed to hold tables**: `assert(type(object) == "table")`
  with the comment that other types are "not… allowed until we can justify a use
  for them" `[T1 src: Pools.lua:51-55]`.
- `Reserve(pool, capacity)` is **deliberately not exposed** — *"to prevent the
  attack vector of addons having control over the quantity of objects available
  to a preexisting pool"* `[T1 src: Pools.lua:18-31]`.
- A secure pool handed to addon code is a **proxy**, not the pool. The
  `ObjectPoolProxyMixin` surface is eight methods: `Acquire, ReleaseAll, Release,
  EnumerateActive, GetNextActive, IsActive, GetNumActive,
  DoesObjectBelongToPool` `[T1 src: Pools.lua:282-297]`.
  `[corrected 2026-07-23]` **"Exactly eight" is true only of a plain object
  pool.** Every *region* pool (frame / texture / fontstring / masktexture /
  actor) goes through `CreateSecureRegionPoolInstance`, which bolts a ninth
  method straight onto the proxy — `proxy.GetTemplate = function(self) return
  template end` `[T1 src: Pools.lua:536-544, the assignment at :539]`. So a
  frame-pool proxy has **nine** callables. A pool **collection**
  proxy exposes **nine** — `GetNumActive, Acquire, Release, ReleaseAll,
  ReleaseAllByTemplate, EnumerateActiveByTemplate, EnumerateActive, IsActive,
  DoesObjectBelongToPool` (`Dump` is present but commented out) — plus
  `GetPool`/`CreatePool`/`GetOrCreatePool`, which re-proxy their results
  `[T1 src: Pools.lua:757-769 (the Funcs list), :774-792 (the three re-proxying
  accessors)]`. `[corrected 2026-07-23]` The collection count was previously
  given as eleven; the list has nine live entries. The file's header comment states the
  motive: *"Any file using ProxyUtil needs to have local references to each
  function in the event an addon tries to replace them [to] expose the private
  objects."* `[T1 src: Blizzard_SharedXMLBase/ProxyUtil.lua:1-4]`.
- The `specialization` argument to a pool collection may be a function or a
  table; a table is applied via `FrameUtil.SpecializeFrameWithMixins` (§2.4), so
  conventionally-named handlers on it become real scripts
  `[T1 src: Pools.lua:604-617]`.

Tier-3 adoption: files referencing any pool constructor —
WeakAuras 7, Plater 3, Details 2, and **zero** in BigWigs, ElvUI, oUF, Ace3
`[T1 obs]`.

---

## 10. Honest gaps

Collected for visibility; each is also stated inline.

1. **Vertex colour vs gradient composition** (§5.3) — the single most important
   unknown here. Not stated at Tier 1 or Tier 2. Concrete in-game test given.
2. **`FontString:SetTextColor` vs `Region:SetVertexColor`** (§5.4) — identical
   Tier-1 annotations, no statement that they are the same storage.
3. **XML `<Color>`'s Lua equivalent** (§5.5) — no Lua equivalent is given by the
   wiki or the XSD. (The "blank cell" argument is weaker than it first looked;
   four *attributes* on the same table are blank too — see §5.5.)
4. **Draw-layer z-order** (§4.4) — the five names are Tier 1, the *ordering*
   between them is not.
5. **`Region.inherits` self-reference** (§1.1) — generator artefact in the only
   available inheritance dump.
6. **`CreateFontString` arity** (§2.1) — Blizzard's own code passes four
   arguments to a three-argument documented signature.
7. **Animation stop semantics without `setToFinalAlpha`** (§7.3).
8. **Addon-declared intrinsics** (§2.5) — schema-permitted, zero corpus usage.
   Narrowed 2026-07-23: `ScrollingMessageFrame` is declared `intrinsic="true"`
   with no XSD element declaration, so the XSD list is evidently not the
   registration mechanism. Whether an *addon*'s declaration is honoured remains
   untested.
9. **Texture file-format rules** (§6.3) — power-of-two, BLP/JPEG/PNG/TGA, and the
   PNG-extension quirk are Tier 2 only.
10. **Frame-level range 0–10000 and the parent-shift/clamp-to-10000 behaviour**
    (§4.1) — Tier 2, from a page last edited 2024-02-23.
11. **`FontString:SetFixedColor` / `OnColorsUpdated`** (§5.4) — no prose at any
    tier.
12. **The eight-argument `SetTexCoord` form** (§5.2) — `GetTexCoord` returns
    eight numbers but the documented setter takes four; the eight-argument setter
    has 13 Blizzard call sites and 21 addon files behind it, and is absent from
    the generated docs.
13. **Base-image mutual exclusion** (§5.1) — that `SetTexture` / `SetAtlas` /
    `SetColorTexture` each fully replace the others is uncited at every tier.
    Added 2026-07-23 after the adversarial pass removed the flat assertion.
14. **Forbidden-frame access semantics** (§8.1) — what actually happens when
    addon code touches a forbidden frame is not established here; the claim was
    cut rather than guessed. Owned by `security-taint-and-restricted-data.md`.
15. **`FRAMESTRATA.PARENT` semantics** (§4.1, rule 11) — Tier 1 gives the value
    and that it is the XML default; the "inherit from parent" reading is
    inference and is not stated anywhere I looked.
16. **Nothing in this file has been executed in the client.**

---

## 11. Rules we could audit against

Each is checkable by grep or by reading a call site. The tier in brackets is the
evidence the rule rests on. Rules stated as *facts about the API surface* are
Tier 1; rules stated as *observed behaviour* say so.

**Object model and construction**

1. `Texture`, `MaskTexture`, `Line` and `FontString` are **not** Frames — they
   have no `CreateTexture`, no `SetFrameStrata`, no `RegisterEvent`. Any code
   calling a `SimpleFrameAPI` method on a texture is a bug.
   [Tier 1: `SimpleFrameAPIDocumentation.lua` vs
   `SimpleTextureBaseAPIDocumentation.lua` / `SimpleFontStringAPIDocumentation.lua`;
   Tier 2 for the graph: `BlizzardInterfaceResources/Resources/WidgetAPI.lua:211,253,262,267,170,474`]
2. `Frame:CreateFontString` is documented with **three** parameters
   (`name, drawLayer, templateName`) while `CreateTexture`, `CreateLine` and
   `CreateMaskTexture` take a fourth, `subLevel`. Code that passes a fourth
   argument to `CreateFontString` is relying on undocumented behaviour — as
   Blizzard's own `Pools.lua` does.
   [Tier 1: `SimpleFrameAPIDocumentation.lua:66-81` vs `:119-135`; violation at
   `Blizzard_SharedXMLBase/Pools.lua:586`]
3. `SecureMixin` and `CreateFromSecureMixins` return `nil` without doing anything
   when `issecure()` is false. Addon code must not call them.
   [Tier 1: `Blizzard_SharedXMLBase/Mixin.lua:23-26, :42-45`]
4. `SetBackdrop` is only available on frames that inherit `BackdropTemplate`.
   A `CreateFrame("Frame", …)` with no template has no `SetBackdrop`.
   [Tier 1: no generated-doc entry (`wowkb.uiapi missing SetBackdrop` → "generated
   docs: no"); sole definition at `Blizzard_SharedXML/Backdrop.lua:336`;
   template at `Blizzard_SharedXML/Backdrop.xml:5`]
5. `CreateFrame` is not in Blizzard's generated API documentation, so any claim
   about its exact signature or error behaviour must cite the wiki or a call
   site, not the docs.
   [Tier 1 (absence): `wowkb.uiapi func '^CreateFrame$'` → 0 matches;
   `FrameScriptDocumentation.lua` documents `Mixin`:279 and `CreateFromMixins`:82
   but not `CreateFrame`]

**Anchoring and geometry**

6. Every mutating method on `ScriptRegionResizing` is `IsProtectedFunction = true`
   — `SetPoint`, `SetAllPoints`, `ClearAllPoints`, `ClearPoint`,
   `ClearPointsOffset`, `AdjustPointsOffset`, `SetPointsOffset`, `SetSize`,
   `SetWidth`, `SetHeight`. What the flag *means* at runtime (blocked action on a
   protected frame in combat) is `security-taint-and-restricted-data.md`'s
   claim, not this file's — the generated docs assert only the flag.
   `[corrected 2026-07-23]` — the runtime consequence used to be stated here
   flatly with a Tier-1 citation that only supports the flag.
   The accessors are **not** uniform: `GetPoint`/`GetPointByName` are
   `MayReturnNothing` + `SecretWhenAnchoringSecret`; `GetNumPoints` carries no
   annotations at all.
   [Tier 1: `SimpleScriptRegionResizingAPIDocumentation.lua` — `AdjustPointsOffset`:10,
   `ClearAllPoints`:22, `ClearPoint`:32, `ClearPointsOffset`:43, `SetAllPoints`:111,
   `SetPoint`:134, plus `SetPointsOffset`/`SetSize`/`SetWidth`/`SetHeight` in the same file;
   see `security-taint-and-restricted-data.md` §1.1]
7. `GetLeft`, `GetRight`, `GetTop`, `GetBottom`, `GetCenter`, `GetRect` and
   `GetScaledRect` are all `MayReturnNothing = True`. Code that assumes a number
   comes back without checking is a latent `nil` arithmetic error.
   [Tier 1: `SimpleScriptRegionAPIDocumentation.lua`, those seven entries]
8. The same seven, plus `GetWidth`/`GetHeight`/`GetSize`/`Intersects`/
   `IsMouseOver` and the FontString metrics, are `SecretWhenAnchoringSecret`.
   If a region's anchoring is secret, they return secret values. What may then be
   done with those values is `security-taint-and-restricted-data.md`'s business.
   [Tier 1: `SecretPredicatesDocumentation.lua:63-66` for the predicate;
   `SimpleScriptRegionAPIDocumentation.lua` and
   `SimpleFontStringAPIDocumentation.lua` for the carriers]
9. Anchoring secrecy propagates from a region to everything anchored to it, and
   is testable with `ScriptRegion:IsAnchoringSecret()`.
   [Tier 2: `Secret Values`, revid 6777907, §Secret anchors, 2026-07-22 · Tier 1 for the API's
   existence: `SimpleScriptRegionAPIDocumentation.lua — IsAnchoringSecret`]
10. Only nine `FRAMEPOINT` values exist. A string outside
    `TOPLEFT TOP TOPRIGHT LEFT CENTER RIGHT BOTTOMLEFT BOTTOM BOTTOMRIGHT`
    is invalid.
    [Tier 1: `Blizzard_SharedXML/UI.xsd:4-16`]

**Z-order**

11. `frameStrata` has exactly ten schema values, including `PARENT` (the XML
    attribute default) and `BLIZZARD`. Any list that says nine and starts with
    `WORLD` is describing a pre-Midnight page. `[corrected 2026-07-23]` — the
    gloss *"meaning 'inherit'"* was uncited inference from the name and has been
    dropped; the XSD states only the value and that it is the default. `[gap]`
    [Tier 1: `UI.xsd:18-31`, `UI.xsd:730` for the default · the nine-value
    `WORLD`-headed list is Tier 2 `Frame Strata`, revid 5975111, **2024-02-23**,
    which also says "WORLD is reserved for the world frame and cannot be
    assigned" — consistent with its absence from the XSD]
12. `Frame:SetFrameStrata` is `SecretArguments = "NotAllowed"` while
    `Frame:SetFrameLevel` is `SecretArgumentsAddAspect = {FrameLevel}`. Passing a
    secret to the former is rejected; passing one to the latter succeeds and
    marks the frame's `FrameLevel` aspect secret, after which `GetFrameLevel`
    returns a secret.
    [Tier 1: `SimpleFrameAPIDocumentation.lua:1188-1191`, `:1176`, `:391-393`]
13. `textureSubLevel` is bounded inclusively to **−8 … 7**. Values outside that
    range are schema violations.
    [Tier 1: `UI.xsd:790-796` · corroborated Tier 2: `XML/Layer`, revid 6769786,
    2026-07-12 · observed usage spans −8 to 7 in the shipped Lua]
14. There are exactly five draw layers: `BACKGROUND BORDER ARTWORK OVERLAY
    HIGHLIGHT`. The XML default is `ARTWORK` and the default sub-level is `0`.
    [Tier 1: `UI.xsd:33-41`, `:789`, `:790`]
15. A frame has both `GetFlattensRenderLayers()` (the explicit request) and
    `GetEffectivelyFlattensRenderLayers()` (the actual state). Code that reads one
    and means the other is wrong.
    [Tier 1: `SimpleFrameAPIDocumentation.lua`, both entries · Tier 2 for
    "`SetToplevel` implicitly enables it": `API Frame SetFlattensRenderLayers`,
    revid 6654668, 2026-02-19]

**Textures and colour**

16. The base-image writers (`SetTexture`, `SetAtlas`, `SetColorTexture`) live on
    `TextureBase`; the colour writers (`SetVertexColor`, `SetAlpha`) live on
    `Region`. They are different types, so a claim that one "resets" the other
    needs evidence.
    [Tier 1: `SimpleTextureBaseAPIDocumentation.lua:313 and neighbours` vs
    `SimpleRegionAPIDocumentation.lua`]
17. `TextureBase:SetGradient` is write-only *as documented*: no `GetGradient` and
    no `ClearGradient` exist anywhere in the generated API. Code that expects to
    read a gradient back is wrong. On *unsetting* one, the docs are silent rather
    than negative — there is no documented clear, which is not the same as
    proving none is reachable. `[gap]`
    [Tier 1: `wowkb.uiapi func 'Gradient'` → 10 matches, exactly one of which is
    `SetGradient` at `SimpleTextureBaseAPIDocumentation.lua:348`; contrast
    `ClearAlphaGradient` at `SimpleFontStringAPIDocumentation.lua:55` and
    `SimpleFrameAPIDocumentation.lua:32`]
18. `Region:SetVertexColor` adds the aspects `{VertexColor, Alpha}` to the object;
    `TextureBase:SetGradient` adds **none** and is `AllowedWhenUntainted` rather
    than `AllowedWhenTainted`. Any code that treats the two as interchangeable
    with respect to secret handling is wrong.
    [Tier 1: `SimpleRegionAPIDocumentation.lua — SetVertexColor` vs
    `SimpleTextureBaseAPIDocumentation.lua:348-358`]
19. `Region:GetVertexColor` and `FontString:GetTextColor` are both
    `MayReturnNothing = True`. Unpacking four values from either without a nil
    check is a latent error.
    [Tier 1: `SimpleRegionAPIDocumentation.lua:66`,
    `SimpleFontStringAPIDocumentation.lua — GetTextColor`]
20. `Region:SetAlpha` clamps to [0, 1] silently as of 12.0.0; code that still
    guards against a 10.0.0-era error is dead code.
    [Tier 2: `API Region SetAlpha`, revid 6654851, 2026-02-19, Patch-changes list]
21. A texture's size is `0, 0` until `Region:IsObjectLoaded()` is true. Sizing
    logic that reads `GetSize()` immediately after `SetTexture` is racing the
    loader.
    [Tier 1 for the API: `SimpleRegionAPIDocumentation.lua — IsObjectLoaded` ·
    Tier 2 for the 0,0 behaviour: `API TextureBase SetTexture`, revid 6654547]
22. `IsDesaturated()` carries the precondition
    `RequiresScriptObjectDesaturationAccess` whose failure mode is
    `ReturnWithError` — it can *throw*, not merely return nothing.
    [Tier 1: `SimpleTextureBaseAPIDocumentation.lua — IsDesaturated`;
    `SecretPredicatesDocumentation.lua:32-35`]
23. `SimpleMaskTextureAPI` declares zero methods of its own; anything you do to a
    MaskTexture goes through inherited TextureBase/Region methods, and attachment
    is done from the *masked* `Texture` via `AddMaskTexture`.
    [Tier 1: `SimpleMaskTextureAPIDocumentation.lua:3`,
    `SimpleTextureAPIDocumentation.lua:3`]

**Fonts and media**

24. `FontInstance:SetFont` carries both `RequiresValidFontAsset` and
    `RequiresValidFontHeight`; the FontString override additionally returns
    `success: bool`. Code that calls `SetFont` and ignores the return has no idea
    whether the font applied.
    [Tier 1: `SimpleFontAPIDocumentation.lua — SetFont`;
    `SimpleFontStringAPIDocumentation.lua — SetFont`]
25. Since 12.0.7 there is a Tier-1 way to validate an asset path before using it:
    `C_UIFileAsset.IsKnownFile` / `GetFileID` / `IsLooseFile`. Addons that ship
    their own "does this texture exist" heuristics can be replaced.
    [Tier 1: `UIFileAssetAPIDocumentation.lua:3` · Tier-1 content via Tier-2
    archive: `Patch 12.0.7/API changes`, revid 6778033, 2026-07-22]
26. **Library convention, not a client rule.** `LibSharedMedia-3.0` — the
    de-facto shared-media registry, vendored by 5 addons on this install —
    refuses to register a background/border/statusbar/sound **whose `data` is a
    string** and whose lowercased path does not match `^interface`, and any sound
    whose path contains neither `.ogg` nor `.mp3`. `font` is exempt from the
    `^interface` guard. Registration failure is a `false` return, not an error;
    a duplicate key also returns `false`. The client itself is **not** known to
    enforce either rule — I found no Tier-1 or Tier-2 statement that it does.
    `[gap]`
    [Tier 3: as shipped in Bartender4 on this install,
    `libs/LibSharedMedia-3.0/LibSharedMedia-3.0.lua:251-261` (guards),
    `:239` (Register), `:264-267` (duplicate key), `:54-58` (the five types)]

**Animations**

27. `AnimationGroup` has an `OnLoop` script; individual `Animation`s do not. A
    handler registered as `OnLoop` on an Animation will never fire.
    [Tier 1: `UI.xsd:1425-1437` (group) vs `UI.xsd:1412-1423` (animation)]
28. `Animation.order` is bounded 0–100 by the schema, and defaults to 1.
    [Tier 1: `UI.xsd:1405-1410`, `:1467`]
29. `ANIMSMOOTHTYPE` is exactly `NONE IN OUT IN_OUT OUT_IN`; `ANIMLOOPTYPE` is
    exactly `NONE REPEAT BOUNCE`; `Path`'s `curve` is exactly `NONE SMOOTH`.
    [Tier 1: `UI.xsd:1388-1396`, `:1380-1386`, `:1398-1403`]
30. `AnimGroup:CreateAnimation` and `AnimatableObject:CreateAnimationGroup` are
    `SecretArguments = "NotAllowed"`; so are `Anim:SetOrder`, `Anim:SetEndDelay`,
    `Anim:SetPlaying`, `Anim:SetSmoothProgress`, `AnimGroup:SetLooping`, and the
    Alpha animation's `SetFromAlpha`/`SetToAlpha`. `Anim:SetDuration` and
    `Anim:SetStartDelay` are `AllowedWhenUntainted`, not `NotAllowed`.
    **Watch the `SetPlaying` split**: it is `NotAllowed` on `Anim` (`:333`) but
    `AllowedWhenUntainted` on `AnimGroup` (`:308`) — a rule keyed on the method
    name alone will misfire.
    [Tier 1: `SimpleAnimGroupAPIDocumentation.lua:3…`,
    `SimpleAnimAPIDocumentation.lua:3…`, `SimpleAnimAlphaAPIDocumentation.lua:3`,
    `SimpleAnimatableObjectAPIDocumentation.lua:3`]

**Pooling**

31. `FramePool_HideAndClearAnchors` does not exist at 12.0.7. The name is
    `Pool_HideAndClearAnchors`. Code referencing the old global must guard it.
    [Tier 1 (absence): `wowkb.uiapi missing FramePool_HideAndClearAnchors` →
    "NOT FOUND in either"; the current definition is
    `Blizzard_SharedXMLBase/Pools.lua:519` · Tier 1 (observed guards):
    Auctionator `Source/Groups/View.lua:11`, Baganator
    `ItemViewCommon/Pools.lua:14,27,40,51,59`, Syndicator
    `Search/UI/Builder.lua:1026,1031` on this install]
32. `CreateFramePool` is an **alias for `CreateSecureFramePool`**. If you need an
    unproxied pool you must call `CreateUnsecuredFramePool` explicitly.
    [Tier 1: `Pools.lua:857`, `:832`]
33. An object pool's default resetter is `nop`; a region pool's is
    `Pool_HideAndClearAnchors`, which performs exactly `Hide()` and
    `ClearAllPoints()`. Any pool whose objects carry per-use state — texture,
    vertex colour, alpha, scale, scripts, registered events, Lua fields — needs a
    custom resetter, or the state leaks to the next acquirer.
    [Tier 1: `Pools.lua:532` (object default `nop`), `:537` (region default),
    `:519-522` (what it does)]
34. Nothing in the pool machinery inspects an object's children or regions. A
    decoration another addon attached to a pooled frame survives `Release` and is
    still present after the next `Acquire`.
    [Tier 1: `Pools.lua:96-105` (`Release` calls only `CallReset` +
    `ReclaimObject`), `:519-527` (neither shipped resetter iterates)]
35. A pool's reset function runs at `Release` for every object, and at `Acquire`
    **only for objects created on that call**. A resetter with side effects that
    assumes "runs once per acquire" is wrong.
    [Tier 1: `Pools.lua:41-70` (`if new then … CallReset`), `:96-105`]
36. Releasing a secret value into a secure pool asserts with
    `"attempted to release a secret value into a pool: %s"`.
    [Tier 1: `Pools.lua:265-279`]
37. A secure pool handed to addon code is a proxy exposing eight methods —
    `Acquire, ReleaseAll, Release, EnumerateActive, GetNextActive, IsActive,
    GetNumActive, DoesObjectBelongToPool` — **plus `GetTemplate` on any region
    pool** (frame / texture / fontstring / masktexture / actor), for nine.
    There is no `Reserve`, no `resetFunc` accessor, and no `Dump`.
    A secure **pool collection** proxy exposes nine (`GetNumActive, Acquire,
    Release, ReleaseAll, ReleaseAllByTemplate, EnumerateActiveByTemplate,
    EnumerateActive, IsActive, DoesObjectBelongToPool`) plus the three
    re-proxying accessors `GetPool`/`CreatePool`/`GetOrCreatePool`.
    [Tier 1: `Pools.lua:282-297` (pool `Funcs`), `:539` (`GetTemplate` added to
    region-pool proxies), `:757-769` (collection `Funcs`, with `Dump` commented
    out), `:774-792`; `Reserve` withheld deliberately per the comment at
    `Pools.lua:18-31`]
    *`[corrected 2026-07-23]` — was "exactly eight methods … and no access to the
    underlying pool table", and gave the collection surface as eleven.*
38. Pools may only hold tables; a pool `createFunc` returning a non-table asserts.
    [Tier 1: `Pools.lua:51-55`]

**Skinning**

39. Mutating a shared Blizzard layout table from insecure code taints it for all
    later consumers. `NineSliceUtil` no longer does this — `12.0.7`'s
    `NineSlice.lua` reads `mirrorLayout` from both the piece and user tables
    without writing back — but the pattern is the hazard.
    [Tier 1 (current code): `Blizzard_SharedXML/NineSlice.lua:61-63`, and the
    absence of `PropagateLayoutSettingsToPieceLayout` from the file ·
    Tier 2 (the bug it fixed): WoWUIBugs #107, *Acknowledged by Blizzard*]
40. The default XML `wordwrap` for a FontString is **true**, `justifyH` is
    `CENTER`, `justifyV` is `MIDDLE`, and `bytes` is 255. Lua-built FontStrings
    that assume otherwise are assuming.
    [Tier 1: `UI.xsd:638-675`]
