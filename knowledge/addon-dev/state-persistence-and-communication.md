---
title: State, persistence & communication (Midnight 12.0.7)
patch: 12.0.7
fetched: 2026-07-23
reviewed: 2026-07-23
sources:
  - https://github.com/Gethe/wow-ui-source (live, 12.0.7.68887, commit 4383ced30106d51b27e3e86d1987f1552f0d259d)
  - https://warcraft.wiki.gg/wiki/Saving_variables_between_game_sessions (rev 5890180, 2023-12-11)
  - https://warcraft.wiki.gg/wiki/SavedVariables (rev 3736139, 2022-09-03 — stale, cited only to mark it stale)
  - https://warcraft.wiki.gg/wiki/TOC_format (rev 6767089, 2026-07-09)
  - https://warcraft.wiki.gg/wiki/AddOn_loading_process (rev 6302251, 2025-04-23)
  - https://warcraft.wiki.gg/wiki/API_C_ChatInfo.SendAddonMessage (rev 6734853, 2026-06-04)
  - https://warcraft.wiki.gg/wiki/API_C_ChatInfo.RegisterAddonMessagePrefix (rev 6734819, 2026-06-04)
  - https://warcraft.wiki.gg/wiki/PLAYER_LOGOUT (rev 6589507, 2026-01-03)
  - https://warcraft.wiki.gg/wiki/SAVED_VARIABLES_TOO_LARGE (rev 6591049, 2026-01-03)
  - https://warcraft.wiki.gg/wiki/Patch_12.0.0/Planned_API_changes (rev 6746061, 2026-06-17)
  - https://warcraft.wiki.gg/wiki/Patch_12.0.0/API_changes (rev 6747189, 2026-06-18)
  - https://warcraft.wiki.gg/wiki/Patch_12.0.5/API_changes (rev 6747894, 2026-06-19)
  - https://warcraft.wiki.gg/wiki/API_C_ChatInfo.InChatMessagingLockdown (rev 6724642, 2026-05-23)
  - https://github.com/Stanzilla/WoWUIBugs (issues 216, 241, 414, 549, 573, 748)
  - https://github.com/WoWUIDev/Ace3 (commit 4475787f06f74d2079b2ab2082195432103da424)
  - https://github.com/WeakAuras/WeakAuras2 (commit 38d4bf1e60b0995e0442ab4ee778ceba07f4be75)
  - https://github.com/rossnichols/LibSerialize (commit e89d5055c761)
  - https://github.com/SafeteeWoW/LibDeflate (commit afc3b78d12fb)
  - https://github.com/wow-rp-addons/Chomp (commit 0b2e0b067a0a)
  - https://github.com/tekkub/libdatabroker-1-1 (commit 1a63ede0248c)
confidence: high
---

# State, persistence & communication

Everything here concerns data that outlives a frame or leaves the client:
SavedVariables, schema migration, settings/profiles, serialization, and the addon
message channel.

**Citation convention used below.**
`UISRC` = the local Blizzard UI source checkout,
`raw/addon-research/wow-ui-source` @ `4383ced30106d51b27e3e86d1987f1552f0d259d`,
`version.txt == 12.0.7.68887` — paths are relative to that checkout.
`INSTALL` = the live game install,
`/mnt/c/Program Files (x86)/World of Warcraft/_retail_` (packaged release copies —
their code differs from upstream because the packager has substituted keywords).
Wiki citations carry the `lastedit` timestamp because wiki pages rot silently.
Wiki **line numbers** refer to the raw wikitext of the cited revision as returned by
`https://warcraft.wiki.gg/api.php?action=query&prop=revisions&rvprop=content&rvslots=main`
(identical to `index.php?…&action=raw`). All wikitext line numbers in this file were
re-measured against that source on 2026-07-23; an earlier pass had them uniformly
five lines high.

Tiers: **1** Blizzard's shipped artefacts · **2** warcraft.wiki.gg + WoWUIBugs ·
**3** community addons/libraries (practice, never rules) · **4** everything else.

---

## 1. SavedVariables — the three scopes

### 1.1 Declaration

Persistence is declared in the `.toc`, not in Lua. Three scope directives exist,
all naming **globals** (comma-separated):

| Directive | Scope | Where it lands |
|---|---|---|
| `## SavedVariables` | one copy per **account** | `WTF/Account/<ACCT>/SavedVariables/<AddOn>.lua` |
| `## SavedVariablesPerCharacter` | one copy per **character** | `WTF/Account/<ACCT>/<Realm>/<Char>/SavedVariables/<AddOn>.lua` |
| `## SavedVariablesMachine` | one copy per **install** | `WTF/SavedVariables/<AddOn>.lua` |

All three paths are **verified by direct observation** on this install
[Tier 1 by observation]:

- account: `INSTALL/WTF/Account/LLOYDCHRISTMAS/SavedVariables/` (49 `.lua` files + 44 `.lua.bak`)
- per-character: `INSTALL/WTF/Account/LLOYDCHRISTMAS/Hyjal/Steaki/SavedVariables/`
- machine: `INSTALL/WTF/SavedVariables/` — contains exactly
  `Blizzard_AddOnList.lua`, `Blizzard_Console.lua`, `Blizzard_GlueSavedVariables.lua`,
  which are precisely the three shipped addons that declare `SavedVariablesMachine`
  (`UISRC Interface/AddOns/Blizzard_Console/Blizzard_Console.toc:3`,
  `.../Blizzard_GlueSavedVariables/Blizzard_GlueSavedVariables.toc:4`,
  `.../Blizzard_AddOnList/Blizzard_AddOnList.toc:6`).

The `SavedVariablesMachine` on-disk location is **not documented on the wiki** —
the wiki only says "List of global variable names to be persisted across all
accounts on the same machine" (`TOC format`:415-418, lastedit 2026-07-09; contrast
`===SavedVariables===` at `:357` and `===SavedVariablesPerCharacter===` at `:364`,
which *do* give paths). The `WTF/SavedVariables/` path is our observation.

> ⚠ **The wiki's `SavedVariables` page is wrong for Midnight.** It claims
> `WTF/Account/<ACCT>/SavedVariables.lua` "only contains settings for Blizzard's own UI"
> (rev 3736139, lastedit **2022-09-03**, 17 lines of wikitext). No such file exists
> anywhere under `INSTALL/WTF` (checked with `find -maxdepth 5 -name SavedVariables.lua`,
> zero hits).
> Blizzard's own UI now persists through ordinary per-addon files —
> e.g. `Blizzard_ClientSavedVariables.lua`, declared at
> `UISRC Interface/AddOns/Blizzard_ClientSavedVariables/Blizzard_ClientSavedVariables.toc:3`.
> Use the HOWTO `Saving variables between game sessions` instead (lastedit
> 2023-12-11), and even that page repeats the stale path in its `== Storage ==`
> section. That HOWTO also predates both other directives — it opens
> *"There are two directives you may add to your .toc file"* and never mentions
> `SavedVariablesMachine` or `LoadSavedVariablesFirst`. For the directive list,
> use `TOC format` (lastedit 2026-07-09), which documents all three scopes plus
> the load-order flag.

Blizzard's shipped `.toc` corpus uses `SavedVariables` 10×,
`SavedVariablesPerCharacter` 10×, `SavedVariablesMachine` 3× across 346 tocs.
(Counts are files, not declarations: 10 tocs carry a `## SavedVariables:` line,
10 a `## SavedVariablesPerCharacter:` line, 3 a `## SavedVariablesMachine:` line.)
In the live install's 81 addon folders, **63 have a top-level `<Folder>/<Folder>.toc`**
and of those: **42 declare `SavedVariables`,
10 declare `SavedVariablesPerCharacter`, 0 declare `SavedVariablesMachine`**
(census over top-level `<AddOn>/<AddOn>.toc`). [Tier 1 by observation]

### 1.2 `LoadSavedVariablesFirst` — the opt-in that changes load order

`## LoadSavedVariablesFirst: 1` makes the client load the addon's SavedVariables
files **before** the first file listed in the TOC, instead of after the last one.

- Tier 1: used by two shipped addons —
  `UISRC Interface/AddOns/Blizzard_DamageMeter/Blizzard_DamageMeter.toc:3` and
  `.../Blizzard_SettingsDefinitions_Shared/Blizzard_SettingsDefinitions_Shared.toc:6`.
- Tier 2: the wiki documents it — "`1` if SavedVariables file(s) should be loaded
  before all script files for this addon" (`TOC format`:352-355, lastedit
  2026-07-09) — and its `== Patch changes ==` list dates it to **Patch 11.1.5**
  (`:436`). `AddOn loading process`:10-11 (lastedit 2025-04-23) says saved variables
  "load after the last file listed in the TOC" by default, "can be reconfigured by
  the LoadSavedVariablesFirst directive to instead be loaded before all files", and
  then "**Finally**, `ADDON_LOADED` fires to indicate the AddOn has finished loading"
  — i.e. the wiki places `ADDON_LOADED` last in both orderings, though it does not
  spell out "either way" in so many words.
- Tier 2 provenance, with a caveat: the same feature was **requested** as WoWUIBugs
  **#414** "Saved Variables: Add TOC field to load saved variables before other files
  in addons" (filed 2023-03-31, closed, labelled *Acknowledged by Blizzard* +
  *Feature Request*). The issue proposed the name `SavedVariablesLoadFirst`;
  Blizzard shipped `LoadSavedVariablesFirst`. No Blizzard statement links the two —
  "this issue is where the directive came from" is our inference from the label and
  the matching semantics, not a sourced fact. The issue
  states the reason such a change must be opt-in, verbatim:
  > an author may be initializing their saved variables global in a script body
  > (`MyAddOn_DB = { <defaults> }`) with the expectation that if this is the first
  > time a user has logged in with the addon installed then the defaults wouldn't
  > get replaced… In this case were the default behaviour to change then such an
  > addon would end up replacing its saved data with defaults on every load.

  It also *proposes* that `ADDON_LOADED` and `SAVED_VARIABLES_TOO_LARGE` "would
  continue to be sequenced as they are today, effectively firing *after* the final
  file specified in the TOC has been loaded". That is a proposal in a feature
  request, not a shipped-behaviour statement; the wiki's "Finally, ADDON_LOADED
  fires" ordering is consistent with it. **[gap]** No Tier-1 artefact states the
  event ordering under `LoadSavedVariablesFirst`. @verify-ingame
- Tier 3 adoption: 2 of the 63 third-party addons in the install use it —
  `INSTALL/Interface/AddOns/BigWigs/BigWigs.toc:18` and
  `INSTALL/Interface/AddOns/DragonRider/DragonRider.toc:49`.

### 1.3 Load lifecycle

Default order (no `LoadSavedVariablesFirst`) [Tier 2, wiki
`AddOn loading process` lastedit 2025-04-23 + `Saving variables between game
sessions` lastedit 2023-12-11]:

1. addon's Lua/XML files execute in TOC order;
2. the addon's SavedVariables files are loaded and executed;
3. `ADDON_LOADED(addOnName, containsBindings)` fires for that addon —
   **the earliest point an addon may read its own saved variables**;
4. `PLAYER_LOGIN` once all non-LoD addons are loaded.

Tier 1 backing for the event shape:
`ADDON_LOADED(addOnName: cstring, containsBindings: bool)`, `SynchronousEvent`,
`UISRC Interface/AddOns/Blizzard_APIDocumentationGenerated/AddOnsDocumentation.lua:389`.

Blizzard's own helper for step 3 is
`EventUtil.ContinueOnAddOnLoaded(addOnName, callback)`
(`UISRC Interface/AddOns/Blizzard_SharedXML/EventUtil.lua:71-79`) — it calls back
immediately if `C_AddOns.IsAddOnLoaded` already reports loaded, otherwise it
registers a one-shot `ADDON_LOADED` filtered on the name. Blizzard's own
documentation example for settings uses exactly this
(`UISRC Interface/AddOns/Blizzard_Settings_Shared/Blizzard_ImplementationReadme.lua:57`).

### 1.4 What can be persisted

[Tier 2, wiki `Saving variables between game sessions`, lastedit 2023-12-11]

- Only **strings, booleans, numbers and tables** survive. Functions, userdata and
  coroutines do not.
- "Circular references in tables may not be preserved."
- Two saved variables referencing the same table are written twice and come back
  as **two distinct tables**.
- Variables live in the **global** environment. A file-local must be published to
  `_G` before logout and read back from `_G` on `ADDON_LOADED`.

[gap] I found no Tier-1 statement of the type whitelist. The generated API docs
describe API shapes, not the SavedVariables serializer; there is no serializer
source in `wow-ui-source`. The list above is Tier 2 only. Number precision,
NaN/inf handling, integer-key vs string-key round-tripping, and the maximum
nesting depth are **undocumented at every tier I checked** (generated docs, UI
source grep for `SavedVariables`, wiki, WoWUIBugs).

### 1.5 The on-disk file format (observed)

Observed on `INSTALL/WTF/**/SavedVariables/*.lua`, 12.0.7 [Tier 1 by observation]:

- Plain Lua source, one top-level assignment per declared global, in declaration
  order. A declared global that is `nil` at save time is still written:
  `INSTALL/WTF/Account/LLOYDCHRISTMAS/Hyjal/Steaki/SavedVariables/Blizzard_ClientSavedVariables.lua`
  contains literally `CHANNELPULLOUT_FADEFRAMES = nil`.
- The file starts with a blank line, then `NAME = {` … `}`.
- **No indentation at all** — table contents are flush left. This is a deliberate
  10.2.7 change; WoWUIBugs #549 "SavedVariables are looking rather flat in 10.2.7"
  (closed, labelled Bug/Regression) recorded it and it is still the behaviour at
  12.0.7.
- Line endings are CRLF on Windows (verified with `cat -A`).
- Hash keys are written as `["key"] = value,`; array parts are written
  positionally with no key (`INSTALL/WTF/SavedVariables/Blizzard_Console.lua`).
- **No comments are emitted** in the normal case (grep for `^\s*--` across the
  49 account-scope files: zero hits).
- The format is executable Lua, so "in theory, you could put actual code in them
  and have it be loaded, but it would be overwritten the next time variables are
  saved" [Tier 2, wiki `SavedVariables`, lastedit 2022-09-03].

---

## 2. Flush semantics — when does it actually hit disk

This is the part that matters for anyone taking a **capture mid-session**.

### 2.1 The write points

[Tier 2, wiki `Saving variables between game sessions` lastedit 2023-12-11]
The client writes the declared globals to disk when you **log out, disconnect,
quit the game, or `/reload`**. There is no addon-callable "save now".
`C_AddOns.SaveAddOns()`
(`UISRC .../AddOnsDocumentation.lua:371`, no arguments, no returns, no
documentation string) is *not* it. `wowkb.uiapi missing SaveAddOns` finds exactly
two call sites in the whole 3685-file UI source, both in the addon-list UI:
`Blizzard_AddOnList/AddonList.lua:665`, where it is the `self.save` branch of
`AddonListMixin:OnHide` whose `else` is `C_AddOns.ResetAddOns()` (`:667`), and
`:813`, immediately after a loop calling `C_AddOns.DisableAddOn(i)` (`:810`).
It commits the **enable/disable selection**. [Tier 1 by code context — Blizzard
publishes no statement of what it saves, so this is inference from its only two
callers, not a documented claim.]

**Operational consequence:** a table your addon fills during play is not on disk
until one of those four events. A tool that reads SavedVariables off disk mid-session
is reading the *previous* flush. This repo's own capture protocol encodes exactly
that rule — `projects/cooldown-hud/docs/m4.5-t3-plan.md:108` "Everything flushes to
disk only on `/reload`." [Tier 3: local practice, one addon]

### 2.2 The logout event sequence

| Event | Payload | Tier 1 locator |
|---|---|---|
| `PLAYER_LOGOUT` | none | `UISRC .../SystemDocumentation.lua:135` |
| `ADDONS_UNLOADING` | `closingClient: bool` | `UISRC .../AddOnsDocumentation.lua:400` |

(Generated-doc line numbers here are the **entry-start** line, as `wowkb.uiapi`
reports them; the `LiteralName = "…"` line is two lower.)

`PLAYER_LOGOUT` is the documented last-chance hook: "it fires just before the
character logs out, and is the last event before your saved variables are written
to disk" [Tier 2, wiki HOWTO lastedit 2023-12-11]; the event page adds "Sent when
the player logs out **or the UI is reloaded**, just before SavedVariables are
saved" [Tier 2, wiki `PLAYER_LOGOUT`, lastedit 2026-01-03].

`ADDONS_UNLOADING` carries `closingClient`, which distinguishes "quitting the
client" from "logging out / reloading". Blizzard's own console uses it to force
its window closed only on a full client exit:
`UISRC Interface/AddOns/Blizzard_Console/Blizzard_Console.lua:124-128` (registered
at `:18`). Three other shipped addons handle it —
`Blizzard_Commentator/Blizzard_CommentatorScoreboard.lua:11,25`,
`Blizzard_EventTrace/Blizzard_EventTrace.lua:693`,
`Blizzard_SettingsDefinitions_Shared/Audio.lua:20,64,84`. That is **4 of 317
shipped addons**, which is the honest size of the Tier-1 sample.

⚠ The wiki's ordering claim — `PLAYER_LEAVING_WORLD` → `PLAYER_LOGOUT` →
`ADDONS_UNLOADING`, and "this does not occur during a crash or Alt-F4" — carries
the wiki's own `{{fact}}` (citation-needed) markers on both bullets
(`AddOn loading process`, lastedit 2025-04-23). Treat the relative order of
`PLAYER_LOGOUT` and `ADDONS_UNLOADING` as **unverified**. @verify-ingame

### 2.3 Not everything works during a real logout

WoWUIBugs **#748** "Certain API calls don't work correctly during `PLAYER_LOGOUT`"
(open, labelled *Acknowledged by Blizzard*, filed 2025-07-03) lists APIs that
return **no value** during a genuine logout but work fine during a `/reload`:
`C_MythicPlus.GetOwnedKeystoneLevel/MapID/ChallengeMapID`,
`C_PlayerInfo.GetPlayerMythicPlusRatingSummary("player")`, and
`GetSpecializationInfo(1)` (while `GetSpecialization()` still works).
[Tier 2: observed behaviour, Blizzard-acknowledged — **not** intended design.]

So a `PLAYER_LOGOUT` handler that computes its final state from live API calls can
silently write `nil`s on real logout and be fine in every `/reload` test.

### 2.4 The `.lua.bak` sibling

Every SavedVariables directory observed contains at most **one** `.lua.bak` per
`.lua`, whose mtime matches the *previous* save and whose contents differ from the
current file (e.g. `INSTALL/WTF/Account/LLOYDCHRISTMAS/SavedVariables/DandersFrames.lua`
128 935 B @ 17:26 vs `.lua.bak` 126 496 B @ 15:00). Files written exactly once have
no `.bak` sibling (`.../Hyjal/Steaki/SavedVariables/Blizzard_RaidUI.lua`).
[Tier 1 by observation]

[gap] Whether the `.bak` is produced by renaming the old file or copying it, and
whether it is written before or after the new file, is **not established**. I found
no Tier-1 or Tier-2 statement of `.bak` semantics at all — the wiki does not mention
`.bak`. What is on record is that it does **not** reliably save you: WoWUIBugs #241
"Suggestion to improve SavedVariables writing process" (closed, Feature Request,
2022) reports users losing data to empty or partially-written `.lua` files after
crashes/Alt-F4/hard shutdown and states "The .bak file does not help restore data."
[Tier 2: user reports, no Blizzard acknowledgement label.]

### 2.5 The out-of-memory failure mode

`SAVED_VARIABLES_TOO_LARGE(addOnName: cstring)` — Tier 1 event, payload verified at
`UISRC .../AddOnsDocumentation.lua:410`. The client's own reaction is a static popup:
`UISRC Interface/AddOns/Blizzard_UIParent/Mainline/UIParent.lua:140` registers it,
`:1772-1774` shows `StaticPopup_Show("SAVED_VARIABLES_TOO_LARGE", addonName)`, and the
dialog is defined at
`UISRC Interface/AddOns/Blizzard_StaticPopup_Game/GameDialogDefs.lua:2878`. The user-facing
string is *"Your computer does not have enough memory to load settings from the
following AddOn. Please disable some AddOns."*
(`BlizzardInterfaceResources/Resources/GlobalStrings/enUS.lua:17688`, build 68256 —
Tier 2 derived dump, same patch, different build).

The critical consequence is Tier 2 only: the wiki's event page states it fires
**after** `ADDON_LOADED`, that it may affect `SavedVariables` and/or
`SavedVariablesPerCharacter`, and that **"SavedVariables will not save on the next
logout"** [wiki `SAVED_VARIABLES_TOO_LARGE`, lastedit 2026-01-03]. So an addon that
overflows once loses that session's writes too.

[gap] No threshold is documented anywhere I looked (generated docs, UI source,
wiki, WoWUIBugs). "Too large" is a client memory condition, not a fixed byte cap.
For calibration only, the largest account-scope files on this install are
`EllesmereUI.lua` 590 761 B, `TellMeWhen_Options.lua` 521 612 B,
`Syndicator.lua` 422 116 B, `TradeSkillMaster.lua` 141 069 B,
`DandersFrames.lua` 128 935 B, `CDMProbe.lua` 125 842 B — all loading fine.
So ~0.5 MB of persisted Lua is demonstrably under the limit, wherever it is.

---

## 3. Secrets must not reach SavedVariables (Midnight)

Blizzard, in a **12.0 blue post archived verbatim on the wiki** (November 11,
"Upcoming Restriction Changes (Beta 1 and later)"):

> **Secrets in Saved Variables**
> Saved variables are no longer allowed to contain secrets.
> Serialization of secret values in saved variables will result in them being
> replaced with nil values. A comment will also be present.

[Tier 1 content via Tier 2 channel: `Patch 12.0.0/Planned API changes`, wikitext
lines **436-438**, **rev 6746061, lastedit 2026-06-17**; the section header at
line **424** names the source as a WoWUIDev Discord post,
`discord.com/channels/327414731654692866/1437889756460744735`, which is **not
publicly fetchable** — see §10. An earlier, weaker phrasing of the same rule
("Saved variables *will no longer be allowed* to contain secrets") appears at
`:366-367`, under the November 4 header at `:336`.]

@verify-ingame — I could not corroborate the "a comment will also be present"
half. No comment lines exist in any of the 49 account-scope SavedVariables files on this
install, but none of them was holding a secret at save time, so this is *absence
of the test case*, not a contradiction.

Consistent Tier-1 evidence that Blizzard hard-rejects secrets at storage
boundaries generally:
`UISRC Interface/AddOns/Blizzard_SharedXMLBase/SecureTypes.lua:35,114,234,262,287,328,357`
all assert `not issecretvalue(value)` before storing into `SecureMap`/`SecureArray`/
`SecureStack`/`SecureValue`/`SecureNumber`/`SecureBoolean`/`SecureFunction`, and
`UISRC Interface/AddOns/Blizzard_SharedXMLBase/Pools.lua:275`
`assertsafe(false, "attempted to release a secret value into a pool: %s", ...)`.
That is Blizzard's own code, not the SavedVariables writer — cite it as
corroboration of the design stance, not as proof of SV behaviour.

---

## 4. Schema versioning and migration

There is no Blizzard-provided migration framework. There *is* a canonical Tier-1
pattern, in `Blizzard_Console`:

```lua
-- UISRC Interface/AddOns/Blizzard_Console/Blizzard_Console.lua
local DEFAULT_SAVED_VARS = { isShown = false, commandHistory = {}, messageHistory = {},
                             height = 300, fontHeight = 14 };   -- :7
local SAVED_VARS_VERSION = 3;                                    -- :8
...
if not Blizzard_Console_SavedVars or not Blizzard_Console_SavedVars.version then
    Blizzard_Console_SavedVars = CopyTable(DEFAULT_SAVED_VARS);  -- :103
elseif Blizzard_Console_SavedVars.version < SAVED_VARS_VERSION then
    if Blizzard_Console_SavedVars.version < 3 then
        Blizzard_Console_SavedVars.fontHeight = DEFAULT_SAVED_VARS.fontHeight;  -- :106
    end
end
Blizzard_Console_SavedVars.version = SAVED_VARS_VERSION;         -- :109
```

Shape of the pattern: an integer `version` **inside** the saved table; a bare
`nil`/missing-version case that resets to defaults wholesale; then ascending
`if version < N` blocks that mutate in place; then stamp the current version last.
Lines 102-109. The persisted file really does carry it —
`INSTALL/WTF/SavedVariables/Blizzard_Console.lua` is a blank line, then
`Blizzard_Console_SavedVars = {` on line 2, then `["version"] = 3,` on **line 3**.

A second Tier-1 variant, without versioning, in `Blizzard_DamageMeter`
(`UISRC Interface/AddOns/Blizzard_DamageMeter/DamageMeter.lua:8,12,16,20`): declare the
global as `X = X or nil` at file scope, keep a `DefaultXSettings` local, and lazily
`CopyTable` the defaults on first access (`:16`, called from `:20`). This addon also
sets `LoadSavedVariablesFirst: 1` (`Blizzard_DamageMeter.toc:3`).
**Do not read a causal link into that pairing:** `Blizzard_Console.lua:2` uses the
identical `X = X or nil` idiom *without* the directive, so the idiom is not a
consequence of it. What the directive does change is that under it a file-scope
`X = { defaults }` would clobber loaded data — see rule 4.

Tier 3 practice, one data point at scale: **WeakAuras** keeps a monotonic
`internalVersion` (currently **90**, `WeakAuras2 WeakAuras/WeakAuras.lua:6`, exposed via
`WeakAuras.InternalVersion()` at `:98`) and a 2 514-line `Modernize.lua` that is one
long ladder of `if data.internalVersion < N then … end` blocks (`Modernize.lua:15`
through `:2502`, which finishes with
`data.internalVersion = max(data.internalVersion or 0, WeakAuras.InternalVersion())`).
It also stores a separate `db.dbVersion` and explicitly detects **downgrade** —
`WeakAuras.lua:2427` `return db.dbVersion and db.dbVersion > WeakAuras.InternalVersion()`.
That downgrade check is the piece the Blizzard pattern lacks: a `version` field
tells you the data is *older*, but only a comparison in the other direction tells
you the user has rolled the addon back onto newer data.

---

## 5. Settings and profile patterns

### 5.1 Blizzard's Settings API (Tier 1)

`UISRC Interface/AddOns/Blizzard_Settings_Shared/Blizzard_Settings.lua`:

- `Settings.RegisterAddOnSetting(categoryTbl, variable, variableKey, variableTbl, variableType, name, defaultValue)` — `:173`
- `Settings.RegisterProxySetting(categoryTbl, variable, variableType, name, defaultValue, getValue, setValue)` — `:177`
- `Settings.RegisterAddOnCategory(category)` — `:133`

Blizzard documents the intended usage in a shipped readme file,
`UISRC Interface/AddOns/Blizzard_Settings_Shared/Blizzard_ImplementationReadme.lua:53-98`.
The material distinction it draws:

> A **proxy setting** allows for get and set accessors, but it is your
> responsibility to default initialize the saved variable value and write the
> value to your saved variable table when it changes. (`:60-61`)
> An **addon setting** will write any value changes directly to your saved variable
> table … unlike a proxy setting, you do not need to default initialize the variable
> table if the value is currently nil as it will be done for you before
> `RegisterAddOnSetting` returns. (`:82-85`)

So `RegisterAddOnSetting` owns the write-back and the nil-defaulting;
`RegisterProxySetting` does neither. The readme's example declares
`## SavedVariables: MyAddonSettings` (`:54`) and wraps registration in
`EventUtil.ContinueOnAddOnLoaded` (`:57`).

### 5.2 AceDB-3.0 profiles (Tier 3 — the de-facto community convention)

`raw/addon-research/Ace3/AceDB-3.0/AceDB-3.0.lua` @ commit `4475787f06f7`,
`ACEDB_MAJOR, ACEDB_MINOR = "AceDB-3.0", 33` (`:44`).

**Nine data types** layered over **one** SavedVariable table, documented in the
library's own header at `:7-15`: `char`, `realm`, `class`, `race`, `faction`,
`factionrealm`, `locale`, `global`, `profile`. (A tenth key,
`factionrealmregion`, is computed but not listed there.) Keys are computed once
at load:
`realmKey = GetRealmName()` (`:254`), `charKey = UnitName("player") .. " - " .. realmKey`
(`:255`), `factionrealmKey` (`:259`), `factionrealmregionKey` (`:264`).
Entry point `AceDB:New(tbl, defaults, defaultProfile)` (`:762`).

Two design decisions worth naming because they explain what you see on disk:

1. **Defaults are injected via metatables and stripped again at logout.**
   `AceDB.frame:RegisterEvent("PLAYER_LOGOUT")` (`:403`) →
   `logoutHandler` (`:355`) walks every registered db, fires `OnDatabaseShutdown`,
   calls `db:RegisterDefaults(nil)` (which runs `removeDefaults`, `:134`), then
   deletes now-empty sections and namespaces (`:361-399`). Net effect: an AceDB
   SavedVariable contains **only values that differ from the defaults**. A key
   missing from the file is not corruption.
2. Sub-modules get **namespaces** rather than their own SavedVariable
   (`:2`, `:20-21`); namespaced children cannot switch profile independently.

You can read the result directly:
`INSTALL/WTF/Account/LLOYDCHRISTMAS/SavedVariables/BigWigs.lua` opens with
`BigWigs3DB = { ["profileKeys"] = { ["Hallick - Kil'jaeden"] = "Default", … },
["namespaces"] = { ["BigWigs_Plugins_BossBlock"] = { ["global"] = { … } } } }`.

**Do not read this as a rule.** It is one library's convention, adopted widely;
Blizzard's own addons do none of it.

---

## 6. Serialization and compression

### 6.1 Blizzard now ships this (Tier 1) — `C_EncodingUtil`

`UISRC Interface/AddOns/Blizzard_APIDocumentationGenerated/EncodingUtilDocumentation.lua:3`,
10 functions, no events:

```
C_EncodingUtil.SerializeCBOR(value: LuaValueVariant?, options: CBORSerializationOptions?) -> string
C_EncodingUtil.DeserializeCBOR(source: stringView) -> value: LuaValueVariant?
C_EncodingUtil.SerializeJSON(value: LuaValueVariant?, options: JSONSerializationOptions?) -> string
C_EncodingUtil.DeserializeJSON(source: string) -> value: LuaValueVariant?
C_EncodingUtil.CompressString(source, method: CompressionMethod, level: CompressionLevel) -> string   [MayReturnNothing]
C_EncodingUtil.DecompressString(source, method: CompressionMethod) -> string                          [MayReturnNothing]
C_EncodingUtil.EncodeBase64(source, variant: Base64Variant) -> string                                 [MayReturnNothing]
C_EncodingUtil.DecodeBase64(source, variant: Base64Variant) -> string                                 [MayReturnNothing]
C_EncodingUtil.EncodeHex(source) -> string                                                            [MayReturnNothing]
C_EncodingUtil.DecodeHex(source: string) -> string                                                    [MayReturnNothing]
```

Enums, same file:
`CompressionMethod` = `Deflate`/`Zlib`/`Gzip` (`:207`);
`CompressionLevel` = `Default`/`OptimizeForSpeed`/`OptimizeForSize` (`:194`);
`Base64Variant` = `Standard` (RFC 4648) / `StandardUrlSafe` (RFC 4648 URL-and-
filename-safe alphabet) (`:182-190`).
Options structs `CBORSerializationOptions` (`:220`) and `JSONSerializationOptions`
(`:228`) each carry one field, `ignoreSerializationErrors` (default `false`) —
"attempt to ignore errors from unsupported values and instead replace them where
applicable with 'undefined' CBOR items" / "'null' JSON values".

Note the asymmetry: the six byte-level functions are `MayReturnNothing`
(they can return *nothing*, so a bare `local s = C_EncodingUtil.CompressString(...)`
can leave `s` nil), while the four serialize/deserialize functions are not.
`SerializeCBOR` (`:144`) and `SerializeJSON` (`:160`) are
`SecretArguments = "AllowedWhenUntainted"`, i.e. tainted code may not hand them
secrets — but note that is **not** a distinguishing feature: **all ten**
`C_EncodingUtil` functions carry the same annotation.

[gap] No max input size, no error text, and no statement of which Lua types CBOR
vs JSON serialization accepts. The generated docs give shape only. Nothing in
`wow-ui-source` calls `C_EncodingUtil` in a way that demonstrates the failure
modes.

### 6.2 The library stack (Tier 3)

The wiki's `SendAddonMessage` page (lastedit 2026-06-04) names both the Blizzard
APIs above **and** the libraries, in a "Libraries" section, and gives the
canonical LibSerialize + LibDeflate + AceComm recipe.

| Library | Local copy | Role |
|---|---|---|
| **LibSerialize** | `raw/addon-research/libs/LibSerialize` @ `e89d5055c761` (2026-07-16), `MAJOR, MINOR = "LibSerialize", 6` (`LibSerialize.lua:571`) | table → string; writes a leading version byte (`:1120`) and asserts `version <= DESERIALIZATION_VERSION` on read (`:1176-1177`). It **writes** format 1 but **reads** 1–2 (`SERIALIZATION_VERSION = 1`, `DESERIALIZATION_VERSION = 2`, `:584-585`) — read-newer/write-older is deliberate |
| **LibDeflate** | `raw/addon-research/libs/LibDeflate` @ `afc3b78d12fb` (HEAD of the clone; last commit **2021-05-05**) | DEFLATE, plus channel-safe codecs |
| **AceSerializer-3.0** | `Ace3/AceSerializer-3.0` MINOR 5 | older serializer; errors on unsupported types (`:106`) |

`LibDeflate:EncodeForWoWAddonChannel(str)` exists because compressed bytes contain
NUL, which the addon channel forbids: it is `CreateCodec("\000", "\001", "")` —
escape the single reserved byte `\000` using `\001` as the escape character —
and the docstring promises "The encoded string is guaranteed to contain no NULL
("\000") character" (`LibDeflate.lua:3060-3079`). The chat-channel codec is much
more expensive: it must escape `\000, s, S, \010, \013, \124, %` *and* every byte
above 127 (UTF-8 completeness), "about 13-14%" overhead (`:3095-3105`).

Worked Tier-3 example of the whole pipeline: WeakAuras' import/export builds
`LibSerialize:SerializeEx` (`Transmission.lua:272`) →
`LibDeflate:CompressDeflate` (`:279`) → prefix `"!WA:2!"` (`:291`) → then
**branches on destination**: `EncodeForPrint` for a chat/clipboard string
(`:293`) but `EncodeForWoWAddonChannel` when it goes over comms (`:295`).
On the way back in, `:306-308` parses the version out of that prefix with
`inString:find("^(!WA:%d+!)(.+)$")` and `:344-348` uses it to choose between the
legacy AceSerializer path and `LibSerialize:Deserialize` (`:347`).
The version marker in the prefix is what lets an
old client refuse a new string.
[Tier 3: `WeakAuras2` @ `38d4bf1e60b0`.]

---

## 7. Addon-to-addon messaging

### 7.1 The API surface (Tier 1)

`UISRC Interface/AddOns/Blizzard_APIDocumentationGenerated/ChatInfoDocumentation.lua`:

```
C_ChatInfo.RegisterAddonMessagePrefix(prefix: cstring) -> result: RegisterAddonMessagePrefixResult  -- :469
C_ChatInfo.IsAddonMessagePrefixRegistered(prefix: cstring) -> bool                                  -- :303
C_ChatInfo.GetRegisteredAddonMessagePrefixes() -> registeredPrefixes: table                         -- :284
C_ChatInfo.SendAddonMessage(prefix, message, chatType?, target?) -> result: SendAddonMessageResult        -- :516  [SecretArguments=NotAllowed]
C_ChatInfo.SendAddonMessageLogged(prefix, message, chatType?, target?) -> result: SendAddonMessageResult? -- :535  [SecretArguments=NotAllowed]
C_ChatInfo.AreOutgoingAddonChatMessagesRestricted() -> isRestricted: bool                                 -- :11
C_ChatInfo.InChatMessagingLockdown() -> isRestricted: bool                                                -- :293
```

Events: `CHAT_MSG_ADDON(prefix, text, channel, sender, target, zoneChannelID, localID, name, instanceID)`
(`ChatInfoDocumentation.lua:799`), `CHAT_MSG_ADDON_LOGGED` (same payload, `:817`),
`BN_CHAT_MSG_ADDON(prefix, text, channel, senderID)` (`:610`). All three are
`SynchronousEvent`.

Blizzard's own doc strings:
`SendAddonMessage` — "Sends a text payload to other clients specified by chatChannel
and target which are registered to listen for prefix" (`:519`);
`SendAddonMessageLogged` — "Intended for plain text payloads; **logged and
throttled**" (`:538`);
`AreOutgoingAddonChatMessagesRestricted` — "Returns false if addons are allowed to
send outgoing chat messages. This is controlled on a **realm-by-realm** basis
(tournament realms allow it), and the ability for addons to **receive** comms is
controlled separately" (`:13`).

Result enums, `UISRC .../ChatConstantsDocumentation.lua`:

```
Enum.RegisterAddonMessagePrefixResult (:130)  Success=0 DuplicatePrefix=1 InvalidPrefix=2 MaxPrefixes=3
Enum.SendAddonMessageResult (:144)            Success=0 InvalidPrefix=1 InvalidMessage=2 AddonMessageThrottle=3
                                              InvalidChatType=4 NotInGroup=5 TargetRequired=6 InvalidChannel=7
                                              ChannelThrottle=8 GeneralError=9 NotInGuild=10
                                              AddOnMessageLockdown=11 TargetOffline=12
```

`AddOnMessageLockdown` and `TargetOffline` were **added in 12.0.0**
[Tier 2, wiki `Patch 12.0.0/API changes` lines 1151-1153 — the `Enum.SendAddonMessageResult`
heading at `:1151` with `+ AddOnMessageLockdown` / `+ TargetOffline` beneath it].
Two of only four values
tell you a *rate* problem (`AddonMessageThrottle`, `ChannelThrottle`); one tells you
Midnight's lockdown refused it.

The result "indicat[es] if the message has been enqueued by the API for
submission. **This does not mean that the message has yet been sent**, and may
still be subject to any server-side throttling" [Tier 2, wiki, lastedit 2026-06-04].

⚠ **Both result enums are numbers, and `Success` is `0`.** In Lua `0` is truthy,
so `if C_ChatInfo.SendAddonMessage(...) then` and
`if C_ChatInfo.RegisterAddonMessagePrefix(p) then` are **true for every outcome**,
success and failure alike — the test silently does nothing. This is a real trap
because both calls returned a **boolean** before 10.2.7 ("Now returns a result
code, rather than a boolean" — wiki patch-changes on both pages, lastedit
2026-06-04), so pre-10.2.7 code that tested truthiness kept "working" while
losing all error detection. Compare against
`Enum.SendAddonMessageResult.Success` / `Enum.RegisterAddonMessagePrefixResult.Success`
explicitly. The wiki additionally notes that *prior to* Patch 11.0.0 a Blizzard
deprecation wrapper shifted the result code to the **second** return position,
and recommends a negative `select` index for forward-compatible access [Tier 2,
`API C_ChatInfo.SendAddonMessage` §Details].

### 7.2 Prefixes, limits, chat types (Tier 2/3)

[Tier 2, wiki `API C_ChatInfo.SendAddonMessage` + `…RegisterAddonMessagePrefix`,
both lastedit 2026-06-04]

- prefix: **at most 16 characters**, non-empty; recommended to be the addon name.
- message: **at most 255 characters**; all byte values 1-255 allowed, **NUL (0) is
  not**.
- **Prefix registration does not survive `/reload`** — re-register every load
  ("Registering prefixes does not persist after doing a /reload", wiki
  `API C_ChatInfo.RegisterAddonMessagePrefix` §Details).
- receipt requires registration: "Recipients must register a prefix using
  `C_ChatInfo.RegisterAddonMessagePrefix()` to receive its messages via
  `CHAT_MSG_ADDON`" — unregistered prefixes never reach the event.
- Retail chat types: `PARTY`, `RAID` (falls back to PARTY if not in a raid),
  `INSTANCE_CHAT`, `GUILD`, `OFFICER`, `WHISPER` (same or connected realms only),
  `CHANNEL` (target = channel number). `SAY`/`YELL` are **Classic-only**.

Tier 3 corroboration of the 255 figure, with a note that is worth carrying:
`Ace3/AceComm-3.0/AceComm-3.0.lua:95` —
`local maxtextlen = 255  -- Yes, the max is 255 even if the dev post said 256. I tested. Char 256+ get silently truncated.`
[Tier 3, one author's test, 2011.] The generated docs type both `prefix` and
`message` as bare `cstring` with **no length constraint**, so **there is no Tier-1
statement of either limit**. [gap]

`SendAddonMessageLogged` exists so Blizzard game masters can read user-generated
content on report; the wiki records that "the message has to be plain text for the
game masters to read it" and that messages containing unsupported non-printable
characters "silently fail to be sent" [Tier 2, wiki, lastedit 2026-06-04, sourced
to a 2018 Blizzard IRC log].

### 7.3 Throttling

[Tier 2, wiki `API C_ChatInfo.SendAddonMessage` §"Message throttling", lastedit
2026-06-04 — Blizzard-derived but not currently traceable to a Tier-1 page]

- Every registered prefix gets an allowance of **10** messages.
- Each send costs 1; at zero, further sends on that prefix return
  `Enum.SendAddonMessageResult.AddonMessageThrottle`.
- The allowance regenerates at **1 per second**, capped at 10.
- Does **not** apply to whispers outside instanced content.
- "All numbers provided above are the default values, however these can be
  dynamically reconfigured by the server at any time." — so do not hard-code them.
- Separately: "if too much data is being sent simultaneously on separate prefixes
  then the client **may be disconnected**".

The page carries a red warning box: *"Please use ChatThrottleLib or AceComm –
otherwise you will blow up the server."*

Two real disconnect bugs on record [Tier 2, WoWUIBugs]: #573 "SendAddonMessage can
trigger disconnects if sending whispers to cross-realm players with long names"
(closed, *Acknowledged by Blizzard*; triggers when character+realm exceeds ~47-48
bytes, reproducible with no addons enabled) and #216 "SendAddonMessage disconnects
player if zero-length message is sent" (Classic only; on retail the call simply
fails to queue).

**ChatThrottleLib** [Tier 3 — as vendored in
`INSTALL/Interface/AddOns/MythicDungeonTools/libs/AceComm-3.0/ChatThrottleLib.lua`,
`CTL_VERSION = 31`]: a byte-rate limiter, not a message-rate limiter.
`MAX_CPS = 800` (`:60`), `MSG_OVERHEAD = 40` bytes guessed per message (`:61`),
`BURST = 4000` (`:63`, comment: "WoW's server buffer seems to be about 32KB. 8KB
should be safe, but seen disconnects on _some_ servers"), and it halves throughput
when `GetFramerate() < MIN_FPS = 20` (`:65`, `:323`). It installs itself globally
and refuses to load over a newer copy (`:30-33`).

**AceComm-3.0** [Tier 3, `Ace3/AceComm-3.0/AceComm-3.0.lua`, MINOR 14] layers
unlimited-length messages on top: it hard-errors if the prefix exceeds 16 chars
(`:61-63`), auto-calls `C_ChatInfo.RegisterAddonMessagePrefix` inside
`RegisterComm` (`:64-68`), and splits with a one-byte protocol marker as the first
character of the payload — `\001` first, `\002` next, `\003` last, `\004` escape
for a single-part payload that happens to start with `\001`-`\009` (`:41-44`,
`:105-137`). It requires ChatThrottleLib at load (`:21`) and deliberately uses one
priority for all chunks of a message to avoid out-of-sequence delivery (`:84`).

**Chomp** [Tier 3, `raw/addon-research/libs/Chomp` @ `0b2e0b067a0a`] is an
alternative transport that also delegates rate control to ChatThrottleLib and
raises its ceilings on its own `ADDON_LOADED` handler, **only when
`WOW_PROJECT_ID == WOW_PROJECT_MAINLINE`** (`Internal.lua:491-497`; the three
assignments are `:494-496` — `BURST` ≥ 6144, `MAX_CPS` ≥ 2048,
`MSG_OVERHEAD` ≤ 32) and re-exposes them via `Chomp.GetBPS`/`SetBPS`
(`Public.lua:400-407`).

### 7.4 Battle.net game data

`C_BattleNet.SendGameData(gameAccountID: number, prefix: stringView, data: stringView)
-> result: SendAddonMessageResult`
(`UISRC .../BattleNetDocumentation.lua:144`), received via `BN_CHAT_MSG_ADDON`.

`BNSendGameData` is **deprecated** and only exists at all if the CVar
`loadDeprecationFallbacks` is set — `UISRC Interface/AddOns/Blizzard_DeprecatedBattleNet/Deprecated_BattleNet.lua:4-11`
guards the whole file on `if not GetCVarBool("loadDeprecationFallbacks") then return; end`
and the shim drops the result code ("New API additionally returns a result code
similar to SendAddonMessage"). Same treatment for `BNSendWhisper`, `BNSetCustomMessage`,
`BNInviteFriend` (`:13-23`). Any addon still calling `BNSendGameData` is one CVar
away from a nil-call error.

[gap] The wiki's `API C_BattleNet.SendGameData` page (lastedit 2026-06-04) is a
stub: signature and result enum only. No prefix or payload length limit is
documented at any tier, and Chomp — which routes Battle.net traffic — carries no
BN-specific size constant.

---

## 8. Midnight's chat-messaging lockdown

This is the single biggest change to addon comms in 12.0.x.

**Blizzard's statement** [Tier 1 content via Tier 2 channel — blue post archived at
`Patch 12.0.0/Planned API changes`, lines **145-148**, under the October 1 header at
`:28`, lastedit 2026-06-17]:

> There are also some new rules that apply to communication while the player is in
> an instance. While in an instance, chat messages will be sent to Lua as Secret
> Values, and addons are not allowed to send communications to other players
> (either through addon comms or regular chat).

Relaxed ten days later (same page, October 11 post "Upcoming Restriction Changes
(Week 3 and later)", header at `:174`,
`discord.com/channels/327414731654692866/1426652212200996874`, quote at
lines **185-188**): the
restriction now applies only when **a mythic keystone run has started and not yet
completed**, **a PvP match has started and not yet completed**, or **an instance
encounter is in progress** — rather than for the whole instance. Note the post files
this under "Coming in Alpha 3 (ETA 10/15)", i.e. it is a *planned* change at the time
of writing, not a shipped one. Corroborated by
`Patch 12.0.5/API changes:182` "The recent restrictions to countdown, ready check,
ping and loot method APIs have been loosened to only apply when in chat messaging
lockdown rather than in all combat."

**Tier-1 machinery.** The `SecretInChatMessagingLockdown` predicate is documented at
`UISRC .../SecretPredicatesDocumentation.lua:53-55`:

> Guarded APIs and events produce secret values when encounter, challenge mode, or
> PvP match addon restrictions are in effect, and when the player is on a
> communication-restricted map such as a dungeon or raid.

At 12.0.7.68887 it annotates **36 functions and 62 events** (98 annotation sites in
the generated docs). The function breakdown by namespace is
`C_Club` 13 · `C_VoiceChat` 9 · `C_LFGList` 5 · `C_Calendar` 4 · `C_ChatInfo` 3 ·
globals 2 (`UnitIsAFK` `UnitDocumentation.lua:1696`, `UnitIsDND` `:1817`).
Within `C_ChatInfo` the guarded functions are exactly
`GetChatLineSenderGUID` (declared `:146`, annotated `:148`),
`GetChatLineSenderName` (`:162`) and `GetChatLineText` (`:178`).
(Counts reproduced 2026-07-23 by parsing every `*.lua` in
`Blizzard_APIDocumentationGenerated` into entries and counting
`SecretInChatMessagingLockdown` per entry: 6144 functions / 1741 events total.)

**How to test the state, at Tier 1:**

```
C_ChatInfo.InChatMessagingLockdown() -> isRestricted: bool
C_RestrictedActions.IsAddOnRestrictionActive(Enum.AddOnRestrictionType.Chat) -> bool
C_RestrictedActions.GetAddOnRestrictionState(type) -> Enum.AddOnRestrictionState
```

`UISRC .../RestrictedActionsDocumentation.lua:55` documents
`IsAddOnRestrictionActive` — "Returns true if an addon restriction type is in an
active state. **Will always return false during dispatch of
`ADDON_RESTRICTION_STATE_CHANGED`.**"
`Enum.AddOnRestrictionType` = `Combat=0, Encounter=1, ChallengeMode=2, PvPMatch=3,
Map=4, Chat=5` (`RestrictedActionsConstantsDocumentation.lua:19`);
`Enum.AddOnRestrictionState` = `Inactive=0, Activating=1, Active=2` (`:6`).

`ADDON_RESTRICTION_STATE_CHANGED(type, state)` is the edge to listen for, and its
Tier-1 doc string states the ordering guarantee explicitly:
"This event is sequenced such that it will always be fired **before** a restriction
becomes active, or **after** it is deactivated."
(`RestrictedActionsDocumentation.lua:97`).

`C_ChatInfo.InChatMessagingLockdown()` lost its second return value
(`lockdownReason`) in 12.0.5 [Tier 2, wiki `Patch 12.0.5/API changes:374-375`,
lastedit 2026-06-19, which lists `- ret2 = lockdownReason` under that function;
also `API C_ChatInfo.InChatMessagingLockdown`, lastedit 2026-05-23]. The same
page records at `:210` that "various chat channel APIs are no longer usable while
chat lockdown is in effect, or from within macros."

**A CVar exists for testing it.** `addonChatRestrictionsForced` — Blizzard's own
description in the 12.0.0 change list: "If true, force the client into the chat
lockdown state. This is provided for addon author testing and will not persist
across client restarts" [Tier 2, wiki `Patch 12.0.0/API changes:839`]. The CVar dump
at build 68256 carries a terser description: "If set, APIs guarded by in lockdown
will be restricted, or may return secrets"
(`BlizzardInterfaceResources/Resources/CVars.lua:17`, Tier 2).

**Secrets may never be sent.** `C_ChatInfo.SendAddonMessage` and
`SendAddonMessageLogged` both carry `SecretArguments = "NotAllowed"`
(`ChatInfoDocumentation.lua:518,537`) — they are 2 of only **84** functions in the
whole 6144-function API with that annotation. Passing a secret to them is not
"it sends garbage", it is a disallowed call.

**Tier-3 adaptation, as shipped.** Across the 81 addon folders installed here,
`C_ChatInfo.InChatMessagingLockdown` is **actually called at 7 sites, in 5 addon
folders belonging to 3 independent projects** (the BigWigs family, Auctionator,
Baganator) — plus one addon that names it in a comment only, in order to explain
why it is *not* calling it. Four distinct shapes, counted 2026-07-23 by grepping
the install for `InChatMessagingLockdown` and `ADDON_RESTRICTION_STATE_CHANGED`:

1. **Pre-check, then register the edge event and retry** — 3 sites, all BigWigs:
   `BigWigs_Core/BossPrototype.lua:462,466-470` (defers private-aura sound
   registration into `modulesNeedingUpdated` and
   `frame:RegisterEvent("ADDON_RESTRICTION_STATE_CHANGED")`),
   `BigWigs_Core/BossPrototype_Classic.lua:535,539-541` (the Classic twin), and
   `BigWigs/Libs/LibSpecialization/LibSpecialization.lua:405,415-418` with the
   handler at `:635`.
2. **Pre-check and simply refuse / cancel, no retry** — 2 sites, also BigWigs:
   `BigWigs_Plugins/Pull.lua:508,510` (the `/pull` slash command prints
   `L.encounterRestricted` and returns) and `BigWigs/Tools/AutoInvite.lua:238,245`
   (cancels its invite ticker).
3. **Pre-check on a chat-link insertion, written defensively inline** — 2 sites in
   2 unrelated addons: `Auctionator/Source/Utilities/InsertLink.lua:4` and
   `Baganator/Core/Utilities.lua:92`, both spelled
   `if not C_ChatInfo.InChatMessagingLockdown or not C_ChatInfo.InChatMessagingLockdown() then`.

4. **Refuse to use it, and approximate it instead** — 1 site.
   `EllesmereUIChat/EllesmereUIChat.lua:3092-3098` tests
   `GetCVarBool("addonChatRestrictionsForced") or C_ChallengeMode.IsChallengeModeActive()`
   and says so in a comment: *"C_ChatInfo.InChatMessagingLockdown exists but its
   breadth on Midnight is unverified — do not swap it in blind."* Note this reads
   the **testing** CVar as if it were the live state, which it is not.

Shapes 1 and 2 (5 sites) all bind `local InChatMessagingLockdown =
C_ChatInfo.InChatMessagingLockdown or function() end` — two carry the comment
`-- XXX 12.0 compat` (`Pull.lua:508`, `AutoInvite.lua:238`) — i.e. a nil-guard so
the addon still loads on a pre-12.0 client. Shape 3 (2 sites) does the same job
with an inline `not … or`. So a nil-guard is universal across all 7 real call
sites, while the register-and-retry appears in only 3.

Two further addons register `ADDON_RESTRICTION_STATE_CHANGED` without going
through `InChatMessagingLockdown` at all — `OPie/Bundle/Mythport.lua:21` and
`TellMeWhen/Components/Core/Conditions/Categories/Location.lua:342` — so the
event has adopters outside the BigWigs family.

**This is convention, not rule:** nothing in Tier 1 or Tier 2 requires the
pre-check; the Tier-1-sanctioned failure signal is
`Enum.SendAddonMessageResult.AddOnMessageLockdown`. What the sample does show is
that authors prefer *not to attempt the send at all*, which is also the only way
to avoid the secret-value returns on the read side.

---

## 9. LibDataBroker — the interop convention

LDB is a 90-line library, frozen since 2008 (`raw/addon-research/libs/libdatabroker-1-1`
@ `1a63ede0248c`, `LibStub:NewLibrary("LibDataBroker-1.1", 4)`). It is a **pub/sub
table**, nothing more:

- `lib:NewDataObject(name, dataobj)` wraps a table in a metatable whose `__newindex`
  fires four CallbackHandler events on every attribute write:
  `LibDataBroker_AttributeChanged`, `…_<name>`, `…_<name>_<key>`, `…__<key>`
  (`LibDataBroker-1.1.lua`, the `oldminor < 3` block).
- `__metatable = "access denied"` and `__index` reads through a private
  `attributestorage` — so consumers cannot enumerate with plain `pairs`; the library
  provides `lib:pairs` / `lib:ipairs` (`oldminor < 4` block).
- Discovery: `lib:DataObjectIterator()`, `lib:GetDataObjectByName(name)`,
  `lib:GetNameByDataObject(obj)`.
- The README states the goal: "detach plugins for TitanPanel and FuBar from the
  display addon" and "provides a place for addons to register 'quicklaunch'
  functions, removing the need for authors to embed many large libraries to create
  minimap buttons."

The attribute vocabulary (`type`, `label`, `icon`, `text`, `value`, `OnClick`,
`OnTooltipShow`, …) is **not in the library** — `NewDataObject` accepts any table.
It lives on a GitHub wiki page the README links to
(`github.com/tekkub/libdatabroker-1-1/wikis/data-specifications`). [gap] I did not
fetch that page; treat the attribute list as convention established by usage, not
as a spec. What *is* verifiable is a real object:
`INSTALL/Interface/AddOns/BigWigs/Loader.lua:894-896` creates
`{type = "launcher", label = "BigWigs", icon = "…minimap_disabled.tga"}` and then
attaches `dataBroker.OnClick` (`:898`) and `dataBroker.OnTooltipShow` (`:905`).

**Where LDB meets persistence:** `LibDBIcon-1.0` is the renderer BigWigs uses (one
data point — see the adoption note below), and its registration signature as vendored
is `function lib:Register(name, object, db, customCompartmentIcon)`
(`LibDBIcon-1.0.lua:363`) —
`INSTALL/Interface/AddOns/BigWigs/Loader.lua:1236` passes `BigWigsIconDB`, which is
one of the four globals declared at `INSTALL/Interface/AddOns/BigWigs/BigWigs.toc:29`.
The library writes `minimapPos`, `hide`, `lock`, `showInCompartment` into that table
(`INSTALL/Interface/AddOns/BigWigs/Libs/LibDBIcon-1.0/LibDBIcon-1.0.lua:203, 287, 304-312, 375, 386, 642, 669`).
So the addon owns the SavedVariable and the library owns its schema.

Adoption on this install: **12 of the 81 installed addon folders** contain a
reference to `LibDataBroker-1.1` — Bartender4, BigWigs, ClassCodex, DandersFrames,
MochaAlerts, MythicDungeonTools, OPie, RaiderIO, Simulationcraft, TellMeWhen, TomTom,
TradeSkillMaster (`grep -rqI 'LibDataBroker-1.1'` per top-level folder, 2026-07-23;
counts folders that *mention* the string, which includes vendoring it as a library).
[unverified] The earlier claim here that "LibDBIcon-1.0 and LibSharedMedia-3.0
upstream is CurseForge SVN" was removed — I did not establish where either library
is canonically hosted. What is true is narrower: **we have no upstream clone of
either under `raw/addon-research/`, so every LibDBIcon line cited above is read from
the copy vendored inside BigWigs**, and may not match upstream.

---

## 10. Honest gaps

- **[gap] The SavedVariables writer is not in the shipped Lua source.** It is C
  code. Everything in §1.5 is inferred from output files. Number formatting
  precision, NaN/inf, table-cycle behaviour, key ordering, and depth limits are
  unverified at every tier.
- **[gap] `.bak` semantics are undocumented** at Tier 1 and Tier 2. Rename-vs-copy,
  and the ordering relative to the main write, are unknown. WoWUIBugs #241 is
  Tier-2 evidence it is not a reliable recovery mechanism.
- **[gap] "Secrets in SavedVariables become nil, with a comment"** is traceable
  only to a Discord blue post archived on the wiki. I could not produce the comment
  locally because no SavedVariable on this install held a secret. @verify-ingame
- **[gap] No Tier-1 statement of the 16-char prefix / 255-byte message limits.**
  The generated docs type them as bare `cstring`. Wiki (Tier 2) + AceComm's tested
  comment (Tier 3) agree, which is the strongest corroboration available.
- **[gap] The throttle numbers (10 allowance, 1/s regen) are Tier 2 only** and the
  same source says the server may change them at any time. Do not encode them.
- **[gap] No length or rate limits documented for `C_BattleNet.SendGameData`** at
  any tier.
- **[gap] `C_EncodingUtil` error semantics.** Six of ten functions are
  `MayReturnNothing`, but nothing says under what conditions.
- **[gap] LDB's attribute specification** lives on an external GitHub wiki I did not
  fetch.
- **[gap] Nothing here was executed in the client.** Every "Tier 1 by observation"
  claim is a read of files the client wrote; every API-behaviour claim is a read of
  Blizzard's own documentation tables.
- **[gap] `LibDBIcon-1.0` and `LibSharedMedia-3.0` have no upstream clone here.**
  Every LibDBIcon line cited in §9 is read from the copy vendored inside BigWigs and
  may differ from upstream. An earlier version of §9 asserted their upstream was
  "CurseForge SVN"; that was uncited and is removed.
- **Adversarial re-verification pass, 2026-07-23.** Every locator in this file was
  re-opened. Two classes of error were found and fixed: (a) all wikitext line numbers
  on `Patch 12.0.0/Planned API changes`, `Patch 12.0.0/API changes`,
  `Patch 12.0.5/API changes` and `TOC format` were uniformly **five lines high** — they
  now match the raw wikitext at the cited revid; (b) the `WeakAuras2` short commit was
  `38d4bf1e6099`, actually `38d4bf1e60b0`, and
  `INSTALL/WTF/SavedVariables/Blizzard_Console.lua`'s `["version"] = 3` is on line 3,
  not line 2. **No quoted text was found to be misquoted, and no revid or issue
  number was wrong.**
- Build skew to keep straight: `wow-ui-source` = 12.0.7.**68887**;
  `BlizzardInterfaceResources` (used only for GlobalStrings and CVars above) =
  12.0.7.**68256**. Same patch, different build.

---

## Rules we could audit against

Concrete, checkable statements. Each names the tier of the evidence behind it.
Rules marked **[derived]** are our recommendation, not a requirement any source
states — do not report them as violations of a documented rule.

1. **An addon that persists data declares it in the `.toc`, not in Lua.** A global
   assigned at runtime and never named by `## SavedVariables`,
   `## SavedVariablesPerCharacter` or `## SavedVariablesMachine` is not written to
   disk. [Tier 2: wiki `Saving variables between game sessions`, lastedit
   2023-12-11. Tier 1 by observation, stated precisely: over the 49 account-scope
   files in `INSTALL/WTF/Account/LLOYDCHRISTMAS/SavedVariables/`, 41 map to a
   top-level addon folder with a `.toc`; for all 41, **every top-level global
   assigned in the file is named by that addon's `## SavedVariables` line** — zero
   extras. The other 8 (`Bagnon`, `BagBrother`, `BetterCooldownManager`, and five
   `Blizzard_*` client addons) have no matching top-level `.toc` in
   `Interface/AddOns/` and were not checked. The converse direction — that every
   declared global appears in the file — is supported by the observation in §1.5
   that even a `nil`-valued declared global is written, but was not exhaustively
   audited.]

2. **A `SavedVariablesMachine` variable lands in `WTF/SavedVariables/<AddOn>.lua`,
   not under `WTF/Account/`.** [Tier 1 by observation: the three shipped addons
   declaring it — `Blizzard_Console.toc:3`, `Blizzard_GlueSavedVariables.toc:4`,
   `Blizzard_AddOnList.toc:6` — are exactly the three files present in
   `INSTALL/WTF/SavedVariables/`.]

3. **Without `## LoadSavedVariablesFirst: 1`, code running at *file scope* cannot
   see its own SavedVariable — it will read `nil`.** The earliest point the value is
   populated is the addon's own `ADDON_LOADED`. Auditable, precisely: flag reads of
   a declared SavedVariable global **in a statement that executes during file load**
   (top-level statements, and function bodies invoked from top level), in an addon
   whose `.toc` lacks the directive.
   ⚠ Do **not** flag every read outside an `ADDON_LOADED` handler — a read inside a
   function that is only *called* later (from `PLAYER_LOGIN`, a slash command, an
   `OnUpdate`) is perfectly correct and is the common case. An earlier phrasing of
   this rule said "outside an `ADDON_LOADED` handler", which would have produced
   false positives on most well-written addons.
   [Tier 2: wiki `AddOn loading process`:10-11, lastedit 2025-04-23. Tier 1 pattern:
   `Blizzard_Console.lua:102` reads it inside `ADDON_LOADED`; `Blizzard_DamageMeter`
   reads at file scope (`DamageMeter.lua:12`) *and* sets the directive at
   `Blizzard_DamageMeter.toc:3`.]

4. **A file-scope `MyDB = { …defaults… }` in an addon that sets
   `LoadSavedVariablesFirst: 1` destroys the user's saved data on every load.**
   The safe form is `MyDB = MyDB or nil` plus a lazy defaults merge. [Tier 1:
   `Blizzard_DamageMeter/DamageMeter.lua:12,16,20` does exactly the safe form under
   that directive; `BigWigs/Loader.lua:1233-1235` is the Tier-3 equivalent
   (`if type(BigWigsIconDB) ~= "table" then BigWigsIconDB = {} end`, under
   `BigWigs.toc:18`). Tier 2: WoWUIBugs #414 names this hazard as the reason the
   directive is opt-in — note #414 describes it hypothetically, as the reason *not*
   to change the default; it does not report an observed loss under the shipped
   directive.]

5. **A persisted table that can outlive an addon update carries a version field
   inside itself, and the load path branches on it.** [Tier 1:
   `Blizzard_Console.lua:8,102-109` — `SAVED_VARS_VERSION`, missing-version reset,
   ascending `< N` migrations, version stamped last. Tier 3 at scale: WeakAuras
   `internalVersion` = 90, `Modernize.lua:15-2502`.]

6. **Version comparison in only one direction is a defect.** A loader that handles
   `stored < current` but not `stored > current` will silently run new-format data
   through old code after a downgrade. [Tier 3: WeakAuras handles it explicitly at
   `WeakAuras/WeakAuras.lua:2427`; Blizzard's `Blizzard_Console.lua:102-109` does
   not — so this rule is a Tier-3 convention, not a Tier-1 requirement.]

7. **`C_ChatInfo.SendAddonMessage` and `SendAddonMessageLogged` must never be
   called with a secret value.** Both carry `SecretArguments = "NotAllowed"` —
   2 of only 84 such functions in 6144. [Tier 1:
   `ChatInfoDocumentation.lua:518, 537`.]

8. **A SavedVariable must never be assigned a value that could be secret.**
   [Tier 1 content via Tier 2 channel: Blizzard blue post, "Saved variables are no
   longer allowed to contain secrets… replaced with nil values",
   `Patch 12.0.0/Planned API changes:436-438`, lastedit 2026-06-17. Corroborating
   Tier 1 stance: `Blizzard_SharedXMLBase/SecureTypes.lua:35,114,234,262,287,328,357`
   assert against storing secrets.]

9. **[derived]** **Every `C_ChatInfo.SendAddonMessage` call site inspects the returned
   `Enum.SendAddonMessageResult`.** Discarding it discards
   `AddonMessageThrottle` (3), `ChannelThrottle` (8) and `AddOnMessageLockdown` (11).
   [Tier 1 establishes only that the information *is* in the return value: return
   type at `ChatInfoDocumentation.lua:531`; enum at
   `ChatConstantsDocumentation.lua:144`. **No Tier-1 or Tier-2 source requires
   callers to inspect it** — Blizzard's own wiki example
   (`API C_ChatInfo.SendAddonMessage` §Example) discards the result on all three of
   its `SendAddonMessage` calls. Treat a discarded result as a quality finding, not
   a violation.]

10a. **A prefix is re-registered on every load**, because registration does not
    survive `/reload`. [Tier 2: wiki `API C_ChatInfo.RegisterAddonMessagePrefix`
    §Details, lastedit 2026-06-04.]

10b. **No call site tests a send/register result for truthiness.** Since 10.2.7
    both calls return an enum, `Success` is `0`, and `0` is truthy in Lua — so
    `if C_ChatInfo.SendAddonMessage(...) then` and
    `if C_ChatInfo.RegisterAddonMessagePrefix(p) then` are true on *every* outcome
    and detect nothing. Auditable: grep for either call used directly as a
    condition or assigned into a boolean. The correct test is `== Enum.
    SendAddonMessageResult.Success` / `== Enum.RegisterAddonMessagePrefixResult.Success`.
    [Tier 1: enum values `Success = 0` at `ChatConstantsDocumentation.lua:130,144`;
    return types at `ChatInfoDocumentation.lua:516,469`. Tier 2: "Now returns a
    result code, rather than a boolean" — Patch 10.2.7 note on both wiki pages,
    lastedit 2026-06-04. The truthiness of `0` is Lua 5.1 semantics, not a WoW
    fact.]

11. **A payload longer than 255 bytes must be chunked, and a payload that may
    contain NUL must be encoded before it is sent.** [Tier 2: wiki
    `API C_ChatInfo.SendAddonMessage`, "at most 255 characters… all characters
    (decimal ID 1-255) are permissible except NULL", lastedit 2026-06-04.
    Tier 3 implementations: `AceComm-3.0.lua:95,105-137`;
    `LibDeflate.lua:3060-3079`.]

12. **Throttle constants are not hard-coded.** The Tier-2 source of the 10/1-per-
    second figures states the server may reconfigure them at any time; an addon
    that encodes them will mis-schedule when it does. [Tier 2: wiki
    `API C_ChatInfo.SendAddonMessage` §Message throttling, lastedit 2026-06-04.]

13. **`BNSendGameData`, `BNSendWhisper`, `BNSetCustomMessage` and `BNInviteFriend`
    are deprecation shims that exist only when the CVar `loadDeprecationFallbacks`
    is set; call `C_BattleNet.*` instead.** [Tier 1:
    `Blizzard_DeprecatedBattleNet/Deprecated_BattleNet.lua:4-23`;
    `C_BattleNet.SendGameData` at `BattleNetDocumentation.lua:144`.]

14. **Code that reacts to the Midnight comms lockdown re-checks it on
    `ADDON_RESTRICTION_STATE_CHANGED`, and does not call
    `C_RestrictedActions.IsAddOnRestrictionActive` from inside that handler** —
    Blizzard documents it as *always* returning false during dispatch of that event.
    [Tier 1: `RestrictedActionsDocumentation.lua:55, 97`.]

15. **An addon that reads chat lines while a keystone/PvP match/encounter is
    running must be secret-safe on `C_ChatInfo.GetChatLineText`,
    `GetChatLineSenderName` and `GetChatLineSenderGUID`** — those three are
    `SecretInChatMessagingLockdown`. [Tier 1: `ChatInfoDocumentation.lua:146`
    (`GetChatLineSenderGUID`, annotation at `:148`), `:162`
    (`GetChatLineSenderName`) and `:178` (`GetChatLineText`) — they are **not**
    contiguous; predicate prose at `SecretPredicatesDocumentation.lua:53-55`.]

16. **A `PLAYER_LOGOUT` handler must not depend on API calls that fail during a real
    logout.** A handler validated only by `/reload` is not validated. [Tier 2:
    WoWUIBugs #748, open, *Acknowledged by Blizzard*, with a concrete list of
    affected calls.]

17. **[derived]** **An addon large enough to risk `SAVED_VARIABLES_TOO_LARGE` should
    register for the event** so it can at least warn rather than silently lose the
    session's writes as well. Note what the sources do and do not say: the wiki says
    the event fires *after* `ADDON_LOADED`, may affect `SavedVariables` and/or
    `SavedVariablesPerCharacter`, and that "SavedVariables will not save on the next
    logout". **No source says handling the event prevents that loss**, and Blizzard's
    own reaction is only a static popup, so an addon handler is a diagnostic, not a
    remedy. [Tier 1: event entry at `AddOnsDocumentation.lua:410` (`LiteralName`
    `:412`); Blizzard's popup at `Blizzard_UIParent/Mainline/UIParent.lua:140,1772,1774`.
    Tier 2: wiki `SAVED_VARIABLES_TOO_LARGE` §Details, lastedit 2026-01-03.]

18. **A tool that reads an addon's SavedVariables off disk during a live session is
    reading the last flush, not current state.** The only client-side write points
    are logout, disconnect, quit and `/reload`; there is no addon-callable save.
    `C_AddOns.SaveAddOns()` is not one — it persists the addon enable list.
    [Tier 2: wiki `Saving variables between game sessions` §"Saving to disk",
    lastedit 2023-12-11. Tier 1: `C_AddOns.SaveAddOns` at
    `AddOnsDocumentation.lua:371`, called only from
    `Blizzard_AddOnList/AddonList.lua:665,813`.]

19. **A SavedVariables file is not a data-integrity guarantee.** Partial and empty
    writes after crashes are on record, and the `.lua.bak` sibling does not reliably
    recover them. **[derived]** The mitigation — periodic-reload or external-copy
    discipline for anything that must not be lost — is our recommendation; no source
    prescribes one. [Tier 2: WoWUIBugs #241 (closed, *Feature Request*, **no**
    Blizzard-acknowledgement label — this is a user report, not a Blizzard statement).
    Tier 1 by observation: `.bak` exists, holds the *previous* save, and is absent for
    first-ever writes.]

20. **`Settings.RegisterProxySetting` callers own their own default-initialisation
    and write-back; `Settings.RegisterAddOnSetting` callers do not need to do
    either** — the readme says "you **do not need to** default initialize", not that
    doing so is forbidden, so a redundant initialisation is noise, not a bug.
    [Tier 1: `Blizzard_ImplementationReadme.lua:60-61, 82-85`; signatures
    at `Blizzard_Settings.lua:173, 177`.]

21. **An AceDB-backed SavedVariable will not contain keys whose values equal the
    registered defaults** — auditing an AceDB file for "missing" settings is a false
    positive. [Tier 3: `Ace3/AceDB-3.0/AceDB-3.0.lua:355-399` strips defaults and
    empty sections on `PLAYER_LOGOUT`; registered at `:403-404`.]

22. **A `LibDBIcon-1.0` registration passes a table the addon has declared as a
    SavedVariable**, or the minimap button's position and hidden state do not
    persist. [Tier 3, **one adopter examined**: `INSTALL/…/BigWigs/Loader.lua:1236`
    passes `BigWigsIconDB`, declared at `INSTALL/…/BigWigs/BigWigs.toc:29`; the
    library writes `minimapPos`/`hide`/`lock`/`showInCompartment` into whatever
    table it is handed — `LibDBIcon-1.0.lua:203,287,304-312,375,386,642,669`, read
    from the copy vendored inside BigWigs. The `db` argument is optional in the
    signature (`:363`), so a registration that omits it is a persistence bug, not a
    load error.]

23. **Code that must distinguish "quitting the client" from "logging out or
    reloading" uses `ADDONS_UNLOADING`, not `PLAYER_LOGOUT`.** `PLAYER_LOGOUT`
    carries **no payload** at all, so it cannot tell them apart;
    `ADDONS_UNLOADING` carries `closingClient: bool`. Auditable: any handler that
    branches on "is the client closing" while registered only for `PLAYER_LOGOUT`
    is branching on something it cannot know. [Tier 1: payloads at
    `SystemDocumentation.lua:135` (none) and `AddOnsDocumentation.lua:400`
    (`closingClient`); Blizzard's own use of exactly this discriminator at
    `Blizzard_Console/Blizzard_Console.lua:124-128`.]

24. **A serialized payload that crosses a version boundary carries a version
    marker the reader validates.** Auditable: a deserializer with no version check
    accepts a future format and mis-reads it. [Tier 3, two independent
    implementations: `LibSerialize` writes a version byte (`:1120`) and asserts
    `version <= DESERIALIZATION_VERSION` (`:1176-1177`); WeakAuras prefixes its
    export strings with `"!WA:2!"` (`Transmission.lua:291`), parses the version
    back out with `inString:find("^(!WA:%d+!)(.+)$")` (`:306-308`, comment at
    `:304`) and switches deserializer on it (`:344-348`). No Tier 1 or Tier 2
    source requires this.]
