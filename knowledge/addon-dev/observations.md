---
title: Observations while coding — the un-drained queue
patch: 12.0.7
fetched: 2026-08-05
reviewed: 2026-08-05
sources:
  - our own addon code, running in the client
confidence: low
---

# Observations while coding

**This is a QUEUE, not a claim.** Nothing here is asserted by the KB. Entries are facts
our own running code discovered, parked until they are drained into the topic file that
owns them.

**Why it exists.** A fact learned while writing addon code has nowhere else to go. The
three other queues are all scoped elsewhere: `_meta/kb-inbox.md` is the *game* KB's
parking lot, `_meta/verify-in-game.md` is **generated** from markers on claims the KB
already asserts, and `mined-pending-verification.md` is third-party-addon mining with
clone provenance. So the fact ends up in a source comment, where it dies with the file —
`State.lua:377` is the proof (see OBS-001).

## The rules

1. **No entry without a `Drains to:`.** Naming the destination is what forces the entry to
   be a claim. If you cannot name a file and section, say so in the body and cap it at
   `confidence: low`.
2. **Drain when you are already in the file.** If your session edits an entry's target,
   drain it. You are one keystroke away.
3. **A capture discharges its observations.** A session that reads a flight or decisionlog
   capture closes every `open` entry that capture settles, before the session ends. The
   capture is the evidence; there will not be a better moment.
4. **`wowkb.obs check` gates a release.** Warn on `--patch`, block on `--minor`/`--major`
   if anything is open past 14 days or more than 12 are open.

Draining means: edit the target file's claim, then set `Status: drained <date>` here.
Do not delete the entry — the record that the fact came from a measurement is the
provenance the target file cites.

---

## OBS-001 · 2026-08-05 · `ChargeGained` is not "+1 charge"

**Observed:** `CooldownViewerItemMixin:TriggerAlertEvent("ChargeGained")` fires on any
upward move of Blizzard's cached charge count, including cooldown-reset procs — not once
per charge restored.

**How:** live pull, 2026-07-31, Destruction. Conflagrate won 702 of 1272 decisions and was
cued while genuinely on cooldown. Recorded only in a `State.lua:377-378` comment until now.

**Confidence:** medium — one spec, one session, one ability.

**Drains to:** `cooldown-manager.md` §5.3 *(was `api-events-and-discovery.md` §2.8; that
material transferred to `cooldown-manager.md` in the 2026-08-05 cleanup)*

**Status:** drained 2026-08-05

---

## OBS-002 · 2026-08-05 · WoW has no clipboard API; copy-out is EditBox + `HighlightText`

**Observed:** there is no clipboard call. The only way to get text out of the client is a
multiline `EditBox`: `SetText(payload)` → `HighlightText()` → `SetFocus()`, leaving the
text selected for the user's own Ctrl+C.

**How:** source read, not a measurement. `SetMultiLine` / `SetMaxBytes` / `SetMaxLetters`
are documented at `SimpleEditBoxAPIDocumentation.lua:776, :756, :766` **[T1]**;
`HighlightText()` has 17 Blizzard call sites, e.g.
`Blizzard_SharedXML/Shared/InputBox/InputBoxTemplates.lua:113` **[T1]**; the shipping
copy-out idiom is WeakAuras' debug log, `WeakAurasOptions/OptionsFrames/DebugLogFrame.lua:36,
:52-53` — `OnTextChanged → SetText(text); HighlightText()`, read-only by reselection **[T3]**.

**Why it matters:** `knowledge/addon-dev/` documents none of this today. Greps for
`clipboard`, `HighlightText` and `SetMultiLine` across all 12 files return only incidental
hits. `AlertTape.lua:220-224` records the cost of not knowing it: an earlier capture printed
to chat only, "the one output that has to reach the analysis machine was the one output that
could not leave the client."

**Confidence:** high for the mechanism, low for the limits (see OBS-003).

**Drains to:** `frames-textures-animation.md` — needs a new EditBox section; the file
currently documents no EditBox behaviour at all.

**Status:** open

---

## OBS-003 · 2026-08-05 · The EditBox letter cap and the payload-size stall are both unmeasured

**Observed:** two limits govern how much text a copy-out box can carry, and neither is
established by anything readable:

- the **default** `SetMaxLetters` cap on an `EditBox` — unknown. Mitigated by calling
  `SetMaxLetters(0)` / `SetMaxBytes(0)` unconditionally, so it never applies.
  (`AceGUIWidget-WeakAurasMultiLineEditBox.lua:213` uses `SetMaxLetters(0)`, corroborating
  that 0 means unlimited **[T3]**.)
- the payload size at which `SetText` **stalls the client** — folk knowledge, no number.
  `DumpPanel.lua` pages at 30,000 characters, and **30,000 is a guess.**

**How:** not measured. Both are `@verify-ingame`.

**Confidence:** low — this entry records an absence, not a finding.

**Drains to:** `frames-textures-animation.md`, same new EditBox section as OBS-002.
Settle by pasting a known-size payload and bisecting.

**Status:** open

---

## OBS-004 · 2026-08-05 · `ns.OnLogin` is a hook nothing defines

**Observed:** `Core.lua:141` calls `if ns.OnLogin then ns.OnLogin() end` on `PLAYER_LOGIN`,
but no file in CDMProbe assigns `ns.OnLogin`. It is a dead extension point, and because it
is a single scalar rather than a list, the first module to claim it would silently exclude
every later one.

**How:** `grep -rn "ns.OnLogin\s*=" *.lua` → no matches.

**Confidence:** high — this is a source read of our own code, not a game fact.

**Drains to:** not a KB fact — it is a defect in our addon. Route to
`projects/cooldown-hud/docs/status.md` backlog: either delete the hook or make it a
list of callbacks. `DumpPanel.lua` avoided it by restoring lazily on first open.

**Status:** open

---

## OBS-005 · 2026-08-05 · Does the addon sandbox expose `require`, `os` or `io`

**Observed:** `sandbox-require-os-io` recorded **ok** — `{io={env=nil, g=nil}, os={env=nil, g=nil}, require={env=nil, g=nil}}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** All three nil. 2298 shipped .lua files contain zero uses of require/dofile/loadfile/module/os./io., which is corroboration by absence; this converts it to a measurement. A non-nil `os` would be a notable finding worth its own KB section.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `anatomy-and-runtime.md:677`

**Status:** drained 2026-08-05

---

## OBS-006 · 2026-08-05 · Is `string.rtgsub` — wiki-tagged `framexml`, i.e. flagged Blizzard-internal rather than 

**Observed:** `string-rtgsub-callable` recorded **ok** — `{calledOk=true, result=a-b-c, type=function}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Unknown; that is the point. If the `framexml` tag means anything enforceable, the lookup is nil or the call errors from an insecure frame. If it is merely documentation of intent, it is a normal function and works.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `anatomy-and-runtime.md:690`

**Status:** drained 2026-08-05

---

## OBS-007 · 2026-08-05 · Do `table.freeze`, `table.isfrozen`, `table.removemulti` and `strsplittable` exist at 12

**Observed:** `wow-lua-zero-use-fns` recorded **ok** — `{strsplittable=function, table.freeze=function, table.isfrozen=function, table.removemulti=function}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** All four present as functions. If any is nil, the wiki list is stale and §5's WoW-additions table needs a correction — which is exactly the failure mode a zero-use, Tier-2-only claim has.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `anatomy-and-runtime.md:697`

**Status:** drained 2026-08-05

---

## OBS-008 · 2026-08-05 · Is a nested-`.toc` library (LibStub) enumerated by the client as an addon in its own rig

**Observed:** `addon-exists-nested-lib` recorded **ok** — `{LibStub=false, RaiderIO=true}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** DoesAddOnExist("LibStub") == false and DoesAddOnExist("RaiderIO") == true. That combination confirms the §19b folder-name rule AND kills the draft's inference that absence from AddOns.txt proves never-enumerated. Either half coming back the other way rewrites §1.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `anatomy-and-runtime.md:127`, `anatomy-and-runtime.md:152`, `anatomy-and-runtime.md:1165`

**Status:** drained 2026-08-05

---

## OBS-009 · 2026-08-05 · Is `RegisterUnitEvent`'s documented four-unit cap real

**Observed:** `register-unit-event-cap` recorded **ok** — `{fiveUnitsCallOk=true}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Passing 5 units errors, or silently ignores units past the fourth. Distinguish the two: after registering with 5, the test records whether the call raised. If it neither errors nor is observably capped, the Tier-2 cap claim should be softened in §2.2.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `api-events-and-discovery.md:200`

**Status:** drained 2026-08-05

---

## OBS-010 · 2026-08-05 · Does `Frame:UnregisterEventCallback` exist, and what is its arity

**Observed:** `unregister-event-callback` recorded **ok** — `{methodType=nil}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Present as a function on a frame (FrameUtil calls it, so it must be, unless FrameUtil path is dead). Existence is the cheap half; arity needs a call and is recorded as whatever the error says.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `api-events-and-discovery.md:389`

**Status:** drained 2026-08-05

---

## OBS-011 · 2026-08-05 · Does `C_EventUtils.IsCallbackEvent` return true for exactly the 12 `CallbackEvent = true

**Observed:** `is-callback-event` recorded **ok** — `{MINIMAP_PING=true, PLAYER_LOGIN=false}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** true for a flagged event (e.g. MINIMAP_PING), false for an unflagged one (e.g. PLAYER_LOGIN). That would upgrade 'the 12 flagged events are exactly what RegisterEventCallback accepts' from a reasonable reading to a measurement. The function is called nowhere in the shipped Lua, so its behaviour is entirely unexercised.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `api-events-and-discovery.md:411`

**Status:** drained 2026-08-05

---

## OBS-012 · 2026-08-05 · Do the six `C_CombatLog.*` names that are documented only on `C_CombatLogSecure` (AddEve

**Observed:** `combatlog-secure-globals` recorded **ok** — `{C_CombatLog.AddEventFilter=nil, C_CombatLog.ClearEventFilters=nil, C_CombatLog.GetCurrentEntryInfo=nil, C_CombatLog.GetCurrentEventInfo=nil, C_CombatLog.GetEntryCount=nil, C_CombatLog.ShouldShowCurrentEntry=nil}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** All six nil on `C_CombatLog` for us — the `Environment = "SecureOnly"` reading. Any that is non-nil means SecureOnly is not enforced by nil-ing the binding, and §3's account of the combat-log surface changes.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `api-events-and-discovery.md:484`

**Status:** drained 2026-08-05

---

## OBS-013 · 2026-08-05 · Do `GetCurrentEventID()` and `GetEventTime(eventProfileIndex)` exist and return anything

**Observed:** `event-profiler-api` recorded **ok** — `{GetCurrentEventID=function, GetEventTime=function, currentEventID=nil, eventTime0=nil}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Both exist (they are in FrameScriptDocumentation). GetCurrentEventID called outside a handler probably returns nil or 0; GetEventTime with that value probably errors or returns nothing. Recording the error IS the answer — it is what tells a future reader the pair is unusable without a profiling CVar.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `api-events-and-discovery.md:893`

**Status:** drained 2026-08-05

---

## OBS-014 · 2026-08-05 · What does the `SecureHooksAllowed = false` annotation actually do

**Observed:** `secure-hooks-allowed-flag` recorded **ok** — `{err=hooksecurefunc(): CreateFromMixins is forbidden for hooking, hookInstalledOk=false}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Unknown and genuinely open. The annotation appears in 24 generated doc entries and in zero Lua logic anywhere in the shipped source, and it overlaps the wiki's empirically-derived unhookable list on only ONE name — which is a reason for caution, not confidence. If the hook installs without error, the natural reading ('hooking these raises') is wrong and both §2.4 and module-architecture rule 6 need rewriting.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `api-events-and-discovery.md:959`, `module-architecture.md:1089`

**Status:** drained 2026-08-05

---

## OBS-015 · 2026-08-05 · Does `CreateFromMixins(nil)` error, or silently produce an empty mixin

**Observed:** `create-from-mixins-nil` recorded **ok** — `{err=Usage: local object = CreateFromMixins(...)
Lua Taint: ClientLab, errored=true}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Errors. The Lua SecureMixin implementation does `for k, v in pairs(mixin)`, which raises on nil — but Mixin/CreateFromMixins are engine functions whose failure mode has never been observed, so the Lua reading may not describe the C one. A silent empty table would be a much nastier failure mode and worth calling out in §1.2.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `module-architecture.md:104`

**Status:** drained 2026-08-05

---

## OBS-016 · 2026-08-05 · Do the deprecated `UIDropDownMenu_*` globals still resolve for addon code at 12.0.7

**Observed:** `dropdown-menu-globals` recorded **ok** — `{ToggleDropDownMenu=_G=function env=function, UIDropDownMenu_AddButton=_G=function env=function, UIDropDownMenu_Initialize=_G=function env=function, UIDropDownMenu_SetWidth=_G=function env=function}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** This is the question `ns.GlobalType` exists for: a name may be absent from `_G` yet present in the addon environment, or vice versa. If `_G.UIDropDownMenu_Initialize` is nil, the file is scoped away from addons and LibUIDropDownMenu's continued use by WeakAurasOptions in 2026 gets a causal explanation the KB currently declines to assert.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `libraries-and-ecosystem.md:552`, `libraries-and-ecosystem.md:789`

**Status:** drained 2026-08-05

---

## OBS-017 · 2026-08-05 · Is the 16-character addon-message prefix limit real, and how is it enforced

**Observed:** `addon-message-prefix-limit` recorded **ok** — `{len16=0, len17=2}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** 16 succeeds, 17 returns false (or errors). The generated docs type the parameter as a bare `cstring` with no limit; wiki (Tier 2) + AceComm's tested comment (Tier 3) agree on 16, which is the strongest corroboration available and still not Tier 1. Harvested from a bare [gap] with no marker — see _meta.status.candidate — and promoted to built because it is pure call-and-record.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `state-persistence-and-communication.md:935`

**Status:** drained 2026-08-05

---

## OBS-018 · 2026-08-05 · Which of the security primitives are actually visible to an addon

**Observed:** `secret-api-surface` recorded **ok** — `{C_Secrets=table, canaccessvalue=function, forceinsecure=function, hooksecurefunc=function, issecrettable=function, issecretvalue=function, issecure=function, issecurevariable=function, scrub=function, secureexecuterange=function}`

**How:** ClientLab `/clab run`, run **2026-07-24 07:49:13** (v0.1.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** All present as functions (CDMProbe already calls issecretvalue/issecrettable/canaccessvalue successfully). `issecurevariable` is the one to watch: a single Tier-2 source with zero shipped call sites is exactly the shape of a claim that turns out to be stale. This test is also the PRECONDITION for the whole §4.2 table below — if issecretvalue is missing, Secret.lua cannot gate anything.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:1328`

**Status:** drained 2026-08-05

---

## OBS-019 · 2026-08-05 · ⭐ Is `item.auraDataCached` / `item:GetAuraDataCached()` on a Cooldown Manager item frame

**Observed:** `cdm-auradatacached-plain-in-combat` recorded **ok** — `{accessorClass=table, applications=secret, auraInstanceID=number, bound=1, duration=secret, expirationTime=secret, fieldClass=table, lastAccessorClass=nil, lastFieldClass=nil, rows=29, timeMod=secret, viewer=BuffIconCooldownViewer}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** UNKNOWN, and it is the highest-value open question in the subtree. If the record is plain in combat it carries `expirationTime`/`duration`, which makes the in-combat DoT-remaining read that `cooldown-manager.md` §5.1 and §7 BOTH declare unanswerable already available on the frame. Method: `ns.ClassOf` the record itself BEFORE indexing it (the container may be secret independently of its fields, per the 12.1.0 `UNIT_AURA` note), then class-check each field. Needs a real pull with a bound aura — out of combat proves nothing, since every sibling reads fine there too.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `cooldown-manager.md:748`, `mined-pending-verification.md:48`

**Status:** drained 2026-08-05

---

## OBS-020 · 2026-08-05 · Is `x == nil` genuinely PERMITTED on a Secret Value, while `x == <number>` throws

**Observed:** `secret-compare-to-nil-permitted` recorded **ok** — `{controlEqZero={err=Interface/AddOns/ClientLab/T_Security.lua:161: attempt to compare upvalue 'v' (a secret number value, while execution tainted by 'ClientLab'), errored=true}, eqNil={errored=false, result=false, resultSecret=false}, neNil={errored=false, result=true, resultSecret=false}, nilEq={errored=false, result=false, resultSecret=false}}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** The asymmetry is consistent with the model — comparing to nil leaks nothing not already knowable — but it is inferred from two data points and NO Tier-1 statement says so. Test both directions against a known secret inside `pcall`: `s == nil`, `nil == s`, `s ~= nil`, and a control `s == 0` that must throw. ⚠ A pass does NOT license comparing to nil in product code — house rule stands: class-check first, branch on the class. This question exists to make the KB's claim honest, not to change the practice.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:1514`

**Status:** drained 2026-08-05

---

## OBS-021 · 2026-08-05 · §4.2 row 1 — store a secret in a local / upvalue / table VALUE.

**Observed:** `secret-op-store-local` recorded **ok** — `{errored=false, result=true, resultSecret=false}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Allowed. If this errors, nothing else in the table is testable and the whole secret-handling chapter is wrong.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:722`

**Status:** drained 2026-08-05

---

## OBS-022 · 2026-08-05 · §4.2 row 2 — pass a secret to a Lua function.

**Observed:** `secret-op-pass-lua-fn` recorded **ok** — `{errored=false, result=<secret>, resultSecret=true}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Allowed. This is the premise of every 'launder it through a helper' pattern.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:723`

**Status:** drained 2026-08-05

---

## OBS-023 · 2026-08-05 · §4.2 row 3 — pass a secret to an unmarked C function (e.g. `strlen`-ish builtin / a C AP

**Observed:** `secret-op-pass-c-fn` recorded **ok** — `{err=attempt to perform numeric conversion on a secret number value (execution tainted by 'ClientLab'), errored=true}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Errors, unless the API is explicitly marked (§4.5). Which C function is chosen matters: the test uses one with no marking so a pass would be genuinely surprising.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:724`

**Status:** drained 2026-08-05

---

## OBS-024 · 2026-08-05 · §4.2 row 4 — concatenate a secret string/number with `..`.

**Observed:** `secret-op-concat` recorded **ok** — `{errored=false, result=<secret>, resultSecret=true}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Allowed, and the RESULT is itself secret. The table says allowed but says nothing about the result's secrecy — record `issecretvalue` on the result, which is the half the KB does not state.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:725`

**Status:** drained 2026-08-05

---

## OBS-025 · 2026-08-05 · §4.2 row 5 — `string.format` / `string.join` / `string.concat` with a secret argument.

**Observed:** `secret-op-string-format` recorded **ok** — `{errored=false, result=<secret>, resultSecret=true}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Allowed, result secret. Same as above: the secrecy of the OUTPUT is the interesting half, since it decides whether a formatted string can be printed.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:726`

**Status:** drained 2026-08-05

---

## OBS-026 · 2026-08-05 · §4.2 row 6 — arithmetic on a secret number.

**Observed:** `secret-op-arith` recorded **ok** — `{err=Interface/AddOns/ClientLab/T_Security.lua:82: attempt to perform arithmetic on upvalue 'v' (a secret number value, while execution tainted by 'ClientLab'), errored=true}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Errors. This is the row CDMProbe's HUD is designed around — no cooldown math on a secret.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:727`

**Status:** drained 2026-08-05

---

## OBS-027 · 2026-08-05 · §4.2 row 7 — compare a secret with `==` and with `<`.

**Observed:** `secret-op-compare` recorded **ok** — `{eq={err=Interface/AddOns/ClientLab/T_Security.lua:89: attempt to compare upvalue 'v' (a secret number value, while execution tainted by 'ClientLab'), errored=true}, lt={err=Interface/AddOns/ClientLab/T_Security.lua:90: attempt to compare upvalue 'v' (a secret number value, while execution tainted by 'ClientLab'), errored=true}}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Errors. Test BOTH operators separately: `==` on differing types is a plausible engine special case and the table does not distinguish them.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:728`

**Status:** drained 2026-08-05

---

## OBS-028 · 2026-08-05 · §4.2 row 9 — boolean test on a NON-boolean secret.

**Observed:** `secret-op-bool-test-nonboolean` recorded **ok** — `{errored=false, result=truthy, resultSecret=false}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Allowed — type isn't secret, so nil→false and everything else→true. The asymmetry with row 8 is the single subtlest rule in the chapter and the one most likely to be misremembered.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:730`

**Status:** drained 2026-08-05

---

## OBS-029 · 2026-08-05 · §4.2 row 10 — length operator `#` on a secret.

**Observed:** `secret-op-length` recorded **ok** — `{err=Interface/AddOns/ClientLab/T_Security.lua:117: attempt to get length of upvalue 'v' (a secret number value, while execution tainted by 'ClientLab'), errored=true}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Errors.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:731`

**Status:** drained 2026-08-05

---

## OBS-030 · 2026-08-05 · §4.2 row 11 — use a secret as a table KEY.

**Observed:** `secret-op-table-key` recorded **ok** — `{err=Interface/AddOns/ClientLab/T_Security.lua:123: attempted to perform indexed assignment on a table that cannot be indexed with secret keys, errored=true}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Errors. Contrast with row 1 (as a table VALUE, allowed) — the key/value asymmetry is the rule that bites caching code.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:732`

**Status:** drained 2026-08-05

---

## OBS-031 · 2026-08-05 · §4.2 row 12 — index and index-assign a secret (`secret.foo`, `secret["foo"] = 1`).

**Observed:** `secret-op-index` recorded **ok** — `{read={err=Interface/AddOns/ClientLab/T_Security.lua:130: attempt to index upvalue 'v' (a secret number value, while execution tainted by 'ClientLab'), errored=true}, write={err=Interface/AddOns/ClientLab/T_Security.lua:131: attempt to perform indexed assignment on upvalue 'v' (a secret number value, while execution tainted by 'ClientLab'), errored=true}}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Both error. Test read and write separately.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:733`

**Status:** drained 2026-08-05

---

## OBS-032 · 2026-08-05 · §4.2 row 13 — call a secret as a function.

**Observed:** `secret-op-call` recorded **ok** — `{err=Interface/AddOns/ClientLab/T_Security.lua:138: attempt to call upvalue 'v' (a secret number value, while execution tainted by 'ClientLab'), errored=true}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Errors.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:734`

**Status:** drained 2026-08-05

---

## OBS-033 · 2026-08-05 · §4.2 row 14 — `type(secret)`.

**Observed:** `secret-op-type` recorded **ok** — `{errored=false, result=number, resultSecret=false}`

**How:** ClientLab run **2026-08-05 13:59:03** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Allowed and returns the REAL type. This is §4.3's Trap 1: type() passes, then the comparison blows up. Record the returned string — it also tells us what kind of secret the cooldown source hands out.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:735`

**Status:** drained 2026-08-05

---

## OBS-034 · 2026-08-05 · Does the CDM item frame's PLAIN `auraInstanceID` reach `C_UnitAuras.GetAuraDuration`, yi

**Observed:** `cdm-aura-duration-object-chain` recorded **ok** — `{bound=2, buff={baseSpellID=387109, call2=userdata, getRemaining=secret, hasExpired=secret, hasSecretValues=true, instClass=number, isActive=secret, unit=player, viewer=BuffIconCooldownViewer}, debuff={baseSpellID=348, call2=userdata, getRemaining=secret, hasExpired=secret, hasSecretValues=true, instClass=number, isActive=secret, unit=target, viewer=EssentialCooldownViewer}, rows=30}`

**How:** ClientLab run **2026-08-05 14:35:32** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** UNKNOWN, and it is the follow-on to `cdm-auradatacached-plain-in-combat`. That measurement killed the direct read (`expirationTime`/`duration`/`timeMod`/`applications` all secret) but left `auraInstanceID` PLAIN — and a secret can never be fed INTO a curve or a duration, since every sink is `AllowedWhenUntainted` and all four negative controls refused `[client 2026-08-04]`. The sanctioned route is the reverse: an API returns an object already carrying the secret internally. §4.8.1 measured `C_UnitAuras.GetAuraDuration` behaving identically to `GetSpellCooldownDuration`, so IF the plain instance id is the key it accepts, the CDM frame supplies a legal in-combat aura timer for display — which is a capability, not a footnote. ⚠ The SIGNATURE is unverified: both arities are tried and the error is recorded, because an argument-count complaint names the real shape. ⚠ `HasSecretValues()` is `ReturnsNeverSecret`, so its VALUE (not just its class) is the one real readback — expect true in combat. ⚠ `GetRemainingDuration` returning a PLAIN number in combat would be a hole in the seal, not a convenience; do not treat it as one. ⚠ The duration sinks are ASPECT-LESS, so this test can prove the object was obtained and carries secrets, and can NEVER prove a pixel moved — that half needs an eyeball.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `cooldown-manager.md:748`, `security-taint-and-restricted-data.md:1323`

**Status:** drained 2026-08-05

---

## OBS-035 · 2026-08-05 · Does a secret-bearing aura duration obtained via `C_UnitAuras.GetAuraDuration` actually 

**Observed:** `cdm-aura-duration-renders` — a **HUMAN VERDICT**: `{asked=Do the AURA bars move like the CONTROL bar does — filling or draining over time?, verdict=aura bars animate like the control}`

**How:** ClientLab showed a stimulus and a person answered, **2026-08-05 15:01:34** (v0.2.1, interface 120007), in combat, instance `none`. ⚠ **This is an eyeball verdict, not an instrument reading** — it is the only evidence class that can close this question, and it must never be cited as a measurement.

**Expected (questions.json):** UNKNOWN, and unknowable by instrument: all three duration sinks declare NO `SecretArgumentsAddAspect`, so there is no readback of any kind and 'the call was accepted' is not evidence a pixel moved. §4.8.1 states it outright — on an aspect-less channel the only oracle is an eyeball. `cdm-aura-duration-object-chain` already proved the object is obtained on both sides and that `HasSecretValues()` is true, so what is left is purely whether it renders. ⚠ A PLAIN CONTROL duration is shown in the same frame: without it 'the bar is empty' cannot be told from 'this widget never animates'. ⚠ `SetMinMaxValues(0,1)` is called BEFORE the timer on every bar — the known trap is a correctly installed duration drawing at 0 % width, which would read as the secret having been dropped. ⚠ 'control doesn't animate either' is a real option and indicts the STIMULUS, not the channel.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `cooldown-manager.md:748`, `security-taint-and-restricted-data.md:1323`

**Status:** drained 2026-08-05

---

## OBS-036 · 2026-08-05 · Is the XSD's listing order of the five draw layers actually the z-order, and does HIGHLI

**Observed:** `draw-layer-z-order` — a **HUMAN VERDICT**: `{asked=Which square is IN FRONT — the RED one (drawn on ARTWORK) or the BLUE one (drawn on OVERLAY)?, verdict=blue (OVERLAY) in front}`

**How:** ClientLab showed a stimulus and a person answered, **2026-08-05 15:01:34** (v0.2.1, interface 120007), in combat, instance `none`. ⚠ **This is an eyeball verdict, not an instrument reading** — it is the only evidence class that can close this question, and it must never be cited as a measurement.

**Expected (questions.json):** Universally believed, matches the names, and stated at Tier 1 nowhere. Needs two overlapping textures and a visual read — the one pass-1 bucket that a SavedVariables record cannot capture on its own.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `frames-textures-animation.md:606`

**Status:** drained 2026-08-05

---

## OBS-037 · 2026-08-05 · Does `issecure()` ever return true in an addon call frame — i.e. can an addon satisfy th

**Observed:** `issecure-in-addon-frame` recorded **ok** — `{AddLuaErrorHandler=function, issecure=function, issecureResult=false}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** false, from a plain addon call frame. Rule 23 currently states the consequence ('no addon may register a Lua error handler this way') as inference from the assert; this measures the premise. Also probe whether AddLuaErrorHandler is even visible to us.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `anatomy-and-runtime.md:768`, `anatomy-and-runtime.md:1212`

**Status:** drained 2026-08-05

---

## OBS-038 · 2026-08-05 · Can `RegisterAllEvents` be combined with `UnregisterEvent`

**Observed:** `register-all-then-unregister` recorded **ok** — `{control=SPELL_UPDATE_USABLE, controlSeen=25, distinctEvents=84, registeredAfterRegisterAll=false, registeredAfterUnregister=false, totalEvents=998, unregisterOk=true, unregisterReturn=false, unregistered=SPELL_UPDATE_COOLDOWN, unregisteredSeen=14, window=18s}`

**How:** ClientLab run **2026-08-05 14:32:09** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Needs a scratch frame plus observation over time — register all, unregister one, count arrivals of that one. Bucket 2.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `api-events-and-discovery.md:194`, `api-events-and-discovery.md:1029`

**Status:** drained 2026-08-05

---

## OBS-039 · 2026-08-05 · Is `OnUpdate` really blocked by hiding a frame or its parent

**Observed:** `onupdate-blocked-by-hidden` recorded **ok** — `{phaseSeconds=0.5, ticksParentHidden=0, ticksReshown=79, ticksSelfHidden=0, ticksShown=76, visibleWhenParentHidden=false, visibleWhenReshown=true, visibleWhenSelfHidden=false, visibleWhenShown=true}`

**How:** ClientLab run **2026-08-05 14:32:09** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Tier 2 and dated; oUF guards on `self:IsVisible()` independently, which is consistent but not proof. Scratch frame + tick counter across a Hide/Show cycle.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `api-events-and-discovery.md:556`

**Status:** drained 2026-08-05

---

## OBS-040 · 2026-08-05 · In what order do two frames registered for the same event receive it — registration orde

**Observed:** `event-dispatch-order-between-frames` recorded **ok** — `{creationOrder=ABCD, distinctOrders=3, firings=78, lastEvent=SPELL_UPDATE_USABLE, orders={ABDC=33, CABD=42, DCAB=3}, registrationOrder=ABDC, window=18s}`

**How:** ClientLab run **2026-08-05 14:32:09** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** No Tier-1 statement, and the wiki's account is explicitly disclaimed by the wiki itself. Two scratch frames plus a shared counter. Bucket 2.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `api-events-and-discovery.md:1025`

**Status:** drained 2026-08-05

---

## OBS-041 · 2026-08-05 · Does `CreateFontString` accept a fourth `subLevel` argument, or is it silently discarded

**Observed:** `fontstring-sublevel-arg` recorded **ok** — `{defaultLayer=ARTWORK, defaultSubLevel=0, fourArgCallOk=true, fourArgLayer=ARTWORK, fourArgSubLevel=0, setDrawLayerLayer=ARTWORK, setDrawLayerSubLevel=0, textureFourArgLayer=ARTWORK, textureFourArgSubLevel=3}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Create two FontStrings on the same frame and draw layer with different subLevel values and see whether stacking order differs. Bucket 2.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `frames-textures-animation.md:223`

**Status:** drained 2026-08-05

---

## OBS-042 · 2026-08-05 · What does frameStrata `PARENT` actually do

**Observed:** `frame-strata-parent` recorded **ok** — `{hostStrata=HIGH, hostStrataMoved=DIALOG, kidDefaultStrata=HIGH, kidSetParentErr=bad argument #2 to '?' (Usage: self:SetFrameStrata(strata)), kidSetParentOk=false, kidStrataAfterHostMoved=DIALOG, kidStrataAfterParent=HIGH, topSetParentErr=bad argument #2 to '?' (Usage: self:SetFrameStrata(strata)), topSetParentOk=false, topStrataAfterParent=MEDIUM, uiParentStrata=MEDIUM}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Tier 1 gives the value and the default and nothing more. The dropped gloss ('inherit from parent, not a z-band') was inference from the name.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `frames-textures-animation.md:485`

**Status:** drained 2026-08-05

---

## OBS-043 · 2026-08-05 · Do frame levels run 0–10000, does a child default to one level above its parent, and doe

**Observed:** `frame-level-arithmetic` recorded **ok** — `{childAfterParent0=10000, childAfterParent10=11, childAt2=2, childDefault=2, childMinusParent=1, parentAt0=0, parentAt10=10, parentAt10000=10000, parentAt10001=10000, parentAtNeg1=0, parentDefault=1, setChild2=ok, setParent0=ok, setParent10=ok, setParent10000=ok, setParent10001=ok, setParentNeg1=errored: bad argument #2 to '?' (outside of expected range 0 to 65535 - Usage: self:SetFrameLevel(frameLevel)), uiParentLevel=0}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** All three are Tier 2 only. Cheap once a scratch frame exists — create parent/child, read GetFrameLevel, then SetFrameLevel(0) on the parent and re-read.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `frames-textures-animation.md:513`

**Status:** drained 2026-08-05

---

## OBS-044 · 2026-08-05 · Are SetTexture / SetAtlas / SetColorTexture mutually exclusive — does exactly one 'win'

**Observed:** `texture-source-exclusivity` recorded **ok** — `{atlasFirst_atlas=bags-item-slot64, atlasFirst_texture=4701874, atlasThenColor_atlas=nil, atlasThenColor_texture=nil, atlasThenColor_vertex=1.00,1.00,1.00,1.00, atlasThenFile_atlas=nil, atlasThenFile_texture=130871, atlasUsed=bags-item-slot64, fileFirst_atlas=nil, fileFirst_texture=130871, fileThenAtlas_atlas=bags-item-slot64, fileThenAtlas_texture=4701874, whiteFile=Interface\Buttons\WHITE8X8}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** The near-universal mental model, consistent with GetTexture returning nil after SetAtlas, and cited at no tier.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `frames-textures-animation.md:644`

**Status:** drained 2026-08-05

---

## OBS-045 · 2026-08-05 · Do SetVertexColor and SetGradient write the same storage

**Observed:** `vertexcolor-vs-gradient` recorded **ok** — `{a_afterGradient=1.00,1.00,1.00,1.00, a_afterVertexRed=1.00,0.00,0.00,1.00, a_baseline=1.00,1.00,1.00,1.00, a_gradientCallOk=true, b_afterGradient=1.00,1.00,1.00,1.00, b_afterVertexRed=1.00,0.00,0.00,1.00, b_baseline=1.00,1.00,1.00,1.00, b_gradientCallOk=true}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** README §6 calls this the most consequential unresolved gap in the whole subtree, and the workspace has already observed it once — todo/addon-engineering.md records that SetGradient RESETS the vertex colour to white. That prior observation makes this a confirm-and-cite, not a discovery.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `frames-textures-animation.md:769`

**Status:** drained 2026-08-05

---

## OBS-046 · 2026-08-05 · Do FontString:SetTextColor and Region:GetVertexColor share storage

**Observed:** `settextcolor-vs-getvertexcolor` recorded **ok** — `{GetTextColor=function, GetVertexColor=function, SetTextColor=function, SetVertexColor=function, afterSetTextColor_text=1.00,0.00,0.00,1.00, afterSetTextColor_vertex=1.00,0.00,0.00,1.00, afterSetVertexColor_text=0.00,0.00,1.00,1.00, afterSetVertexColor_vertex=0.00,0.00,1.00,1.00, baseline_text=1.00,0.82,0.00,1.00, baseline_vertex=1.00,0.82,0.00,1.00, hasFontObject=true, setTextColorOk=true, setVertexColorOk=true}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** 'Identical annotations ⇒ identical storage' is inference. The two wiki pages say nothing about the relationship, and one of them was effectively abandoned in 2021.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `frames-textures-animation.md:811`

**Status:** drained 2026-08-05

---

## OBS-047 · 2026-08-05 · What does an alpha or vertex-colour animation do to the underlying value when it stops W

**Observed:** `anim-restore-without-final` recorded **ok** — `{finishMeasured=false, finishWhy=natural-finish arm starting now - re-run /clab run in a few seconds to read it, stop_alphaAfterStop=0.501960813999176, stop_alphaDuringPlay=1, stop_baseAlpha=0.501960813999176, stop_isSetToFinalAlpha=false, vertex_afterStop=0.00,1.00,0.00,1.00, vertex_base=1.00,0.00,0.00,1.00, vertex_duringPlay=0.00,1.00,0.00,1.00}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** The attribute's existence implies restoration, but that is inference and is stated at no tier. Needs an AnimationGroup and a read after OnFinished.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `frames-textures-animation.md:1111`

**Status:** drained 2026-08-05

---

## OBS-048 · 2026-08-05 · What is the real order of PLAYER_LEAVING_WORLD → PLAYER_LOGOUT → ADDONS_UNLOADING, and d

**Observed:** `logout-event-order` recorded **ok** — `{e1=1 PLAYER_LEAVING_WORLD arg1=nil t=191278.794, e2=2 ADDONS_UNLOADING arg1=true t=191278.794, e3=3 PLAYER_LOGOUT arg1=nil t=191278.794, measured=true, phase=read-back, stamp=2026-08-05 14:07:39, total=3}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** The wiki carries its own {{fact}} tags on both bullets, i.e. it does not vouch for the ordering. Needs the pass-3 journal (record each event with an incrementing sequence number, read it back next session). The crash half is not testable politely.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `state-persistence-and-communication.md:275`

**Status:** drained 2026-08-05

---

## OBS-049 · 2026-08-05 · Does a Secret Value stored in SavedVariables come back as nil after a /reload

**Observed:** `savedvars-secret-roundtrip` recorded **ok** — `{after=trailing, armedAt=2026-08-05 14:33:00, measured=true, phase=read-back, readSecret=false, readType=nil, rearmed=no — run again to re-arm; this payload is kept for one logout only, sentinel=written, slotSurvived=true, source=GetSpellCooldown(686).cooldown-field, wroteClass=secret, wroteErr=none, wroteOk=true}`

**How:** ClientLab run **2026-08-05 14:35:51** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Traceable only to a Discord blue post archived on the wiki; the KB could not produce it locally because no SavedVariable on this install held a secret. A two-session round trip settles it. PASS 3 — it is the first test that needs the journal (write in session N, assert in session N+1), so it validates that machinery.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `state-persistence-and-communication.md:934`

**Status:** drained 2026-08-05

---

## OBS-050 · 2026-08-05 · How does the SavedVariables writer format numbers — what precision, and what does it do 

**Observed:** `savedvars-number-precision` recorded **ok** — `{armedAt=2026-08-05 14:31:51, drifted=wide=1234567890.123457 want 1234567890.1234567, exact=pi,negative,large,twoPow53,int,tenth,twoPow53minus1,tiny,third, inf=nil nil, measured=true, missing=none, nan=nil nil, negzero=0, ninf=nil nil, phase=read-back, rearmed=no — run again to re-arm; this payload is kept for one logout only, sentinel=written, slotSurvived=true}`

**How:** ClientLab run **2026-08-05 14:35:51** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Unverified at every tier; the writer is C, not shipped Lua, so §1.5 is entirely inferred from output files. Write known values, /reload, read back.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `state-persistence-and-communication.md:925`

**Status:** drained 2026-08-05

---

## OBS-051 · 2026-08-05 · What does the SavedVariables writer do with a table cycle, and is there a depth limit

**Observed:** `savedvars-table-cycles` recorded **ok** — `{aliasA=shared, aliasIdentity=false, armedAt=2026-08-05 14:31:51, cycle=self field is nil, cycleTag=cycle, deepGot=64, deepWanted=64, measured=true, phase=read-back, rearmed=no — run again to re-arm; this payload is kept for one logout only, sentinel=written, slotSurvived=true}`

**How:** ClientLab run **2026-08-05 14:35:51** (v0.2.0, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Unverified at every tier. Risky to test — a hang or a corrupt file is a plausible outcome — so it wants its own throwaway SavedVariable, not ClientLabDB.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `state-persistence-and-communication.md:925`

**Status:** drained 2026-08-05

---

## OBS-052 · 2026-08-05 · Is SavedVariables key ordering stable across writes

**Observed:** `savedvars-key-ordering` recorded **ok** — `{armedAt=2026-08-05 14:04:47, keysRead=10, keysWritten=10, measured=true, phase=read-back, readOrder=foxtrot,delta,hotel,echo,india,alpha,golf,juliet,bravo,charlie, rearmed=written, slotSurvived=true, stable=false, wroteOrder=foxtrot,delta,hotel,echo,juliet,india,alpha,golf,bravo,charlie}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Unverified. Matters for anything diffing the file between sessions — which wowkb.cdmp and wowkb.lab both do.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `state-persistence-and-communication.md:925`

**Status:** drained 2026-08-05

---

## OBS-053 · 2026-08-05 · Under `## LoadSavedVariablesFirst`, when do ADDON_LOADED and SAVED_VARIABLES_TOO_LARGE f

**Observed:** `savedvariables-first-ordering` recorded **ok** — `{addonLoadedDBType=table, addonLoadedSawDisk=true, addonLoadedStep=2, armedAt=2026-08-05 14:04:47, fileTimeDBType=nil, fileTimeSawDisk=false, fileTimeStep=1, measured=true, phase=read-back, rearmed=written, slotSurvived=true, tocTagViaMetadata=nil, tooLargeStep=SAVED_VARIABLES_TOO_LARGE did not fire, witness=on disk}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** The only statement is a PROPOSAL in a feature request, not a shipped-behaviour statement. Needs the lab's own .toc to set the tag, which changes the lab's own load behaviour — so it belongs with the W1d container work rather than with the in-process tests.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `state-persistence-and-communication.md:147`

**Status:** drained 2026-08-05

---

## OBS-054 · 2026-08-05 · Is the 255-byte addon-message body limit real, and what happens on overflow — truncation

**Observed:** `addon-message-size-limit` recorded **ok** — `{at255=0 (Success), at256=0 (Success), delivered=nothing received yet — delivery is async, re-run to see it, prefix=CLABSZ, register=0 (Success), target=self WHISPER}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Same Tier-2/Tier-3-only footing as the prefix limit. Deferred past the prefix test because sending actually puts traffic on a channel, which the prefix registration does not.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `state-persistence-and-communication.md:935`

**Status:** drained 2026-08-05

---

## OBS-055 · 2026-08-05 · Under what conditions do the six `MayReturnNothing` functions of `C_EncodingUtil` return

**Observed:** `encoding-util-error-semantics` recorded **ok** — `{b64_decode_bad=n=1 string len=6, b64_decode_ok=n=1 string "hello", b64_encode=n=1 string "aGVsbG8=", b64_encode_badVariant=errored: bad argument #2 to '?' (Usage: local output = C_EncodingUtil.EncodeBase64(source [, variant])), compress_badMethod=errored: bad argument #2 to '?' (Usage: local output = C_EncodingUtil.CompressString(source [, method, level])), compress_empty=n=1 string len=2, compress_nilSource=errored: bad argument #1 to '?' (Usage: local output = C_EncodingUtil.CompressString(source [, method, level])), compress_ok=n=1 string len=17, decompress_empty=errored: DecompressString(): internal decompression error
Lua Taint: ClientLab, decompress_garbage=errored: DecompressString(): internal decompression error
Lua Taint: ClientLab, decompress_roundtrip=n=1 string len=35, enums=method=0 level=0 variant=0, hex_decode_nonhex=n=1 string len=2, hex_decode_odd=errored: DecodeHex(): attempted to decode a string that does not have an even number of bytes
Lua Taint: ClientLab, hex_decode_ok=n=1 string "hello", hex_encode=n=1 string "68656c6c6f", hex_encode_empty=n=1 string "", hex_encode_nil=errored: bad argument #1 to '?' (Usage: local output = C_EncodingUtil.EncodeHex(source))}`

**How:** ClientLab run **2026-08-05 14:31:51** (v0.2.0, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Nothing states the conditions. Pure call-and-record once someone enumerates plausible bad inputs — a good pass-2 addition, cheap and self-contained.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `state-persistence-and-communication.md:942`

**Status:** drained 2026-08-05

---

## OBS-056 · 2026-08-06 · Can `item.cooldownID` on a Cooldown Manager item frame read SECRET, and in which state

**Observed:** `cdm-cooldownid-secret-when` recorded **ok** — `{combat={disagreements=0, everFieldSecret=false, everMethodSecret=false, fieldErrored=0, fieldNil=0, fieldNumber=26, fieldOther=0, fieldSecret=0, frames=26, methodErrored=0, methodNil=0, methodNumber=26, methodOther=0, methodSecret=0, samples=1, viewers=4}, ooc={disagreements=0, everFieldSecret=false, everMethodSecret=false, fieldErrored=0, fieldNil=0, fieldNumber=26, fieldOther=0, fieldSecret=0, frames=26, methodErrored=0, methodNil=0, methodNumber=26, methodOther=0, methodSecret=0, samples=1, viewers=4}}`

**How:** ClientLab run **2026-08-06 09:38:47** (v0.2.2, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** UNKNOWN. It is the only untagged row in a §7 Tier 2 table whose twelve neighbours all carry `[client]`, and it is load-bearing: `resolve out of combat, never overwrite a known-good id with an unreadable one` is the whole merge-don't-replace design of anything binding to the CDM. A result showing it is never secret does not fail the milestone — it means that machinery is unreachable and should be simplified rather than kept because it was expensive to write. ⚠ This row deliberately does NOT declare needs="secret": that gate records `skipped` out of combat, `skipped` never drains, and the out-of-combat half IS half the claim — gating it would lose that half by construction.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `cooldown-manager.md:740`

**Status:** drained 2026-08-06

---

## OBS-057 · 2026-08-06 · Does `CooldownViewerMixin:GetItemFrames()` still return item frames when the viewer itse

**Observed:** `cdm-hidden-viewer-item-frames` recorded **ok** — `{hiddenAndPopulated=4, hiddenViewers=EssentialCooldownViewer, UtilityCooldownViewer, BuffIconCooldownViewer, BuffBarCooldownViewer, viewers={BuffBarCooldownViewer=IsShown=false IsVisible=false children=4 childrenShown=0 poolActive=3 itemFrames=3, BuffIconCooldownViewer=IsShown=false IsVisible=false children=9 childrenShown=1 poolActive=7 itemFrames=7, EssentialCooldownViewer=IsShown=false IsVisible=false children=10 childrenShown=9 poolActive=9 itemFrames=9, UtilityCooldownViewer=IsShown=false IsVisible=false children=8 childrenShown=7 poolActive=7 itemFrames=7}}`

**How:** ClientLab run **2026-08-06 09:41:27** (v0.2.2, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** Tier 1 PREDICTS the children survive, and that is the reason to measure it rather than to assume it. GetItemFrames is GetLayoutChildren (`CooldownViewer.lua:1490-1497`), whose filter tests each CHILD's own `IsShown()` plus a `layoutIndex` (`LayoutFrame.lua:38`) rather than the viewer's `IsVisible()`, and the viewer's `OnHide` unregisters events without releasing `itemFramePool` (`:1570-1580`). It decides whether a consumer's `hidden` and `empty` health verdicts can discriminate at all, or should collapse to one. ⚠ FIVE NUMBERS OR IT PRODUCES A FALSE ANSWER — an empty list has three incompatible causes (the IsShown filter dropped every child / the pool holds nothing / no child carries a layoutIndex), so each row records IsShown, IsVisible, the raw child count, the pool-active count, #GetItemFrames() and how many raw children individually pass IsShown().

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `cooldown-manager.md:857`

**Status:** drained 2026-08-06

---

## OBS-058 · 2026-08-06 · Is an ordinary addon frame parented and anchored to UIParent `IsProtected() == false`, d

**Observed:** `uiparent-child-frame-unprotected` recorded **ok** — `{inCombatOps=SetPoint=ok SetScale=ok Show=ok Hide=ok, plainUnderUIParent=isProtected=false explicit=false, reanchoredToProtected=target=ActionButton1 (isProtected=true explicit=true) -> our frame now isProtected=false explicit=false, uiparentItself=isProtected=true explicit=true}`

**How:** ClientLab run **2026-08-06 09:38:47** (v0.2.2, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** §1.1 asserts the frame is unprotected; §1.2 states that protection propagates to a protected frame's parents and anchor targets. But UIParent is itself `protected="true"`, so a child of UIParent anchored to UIParent sits beside both legs of that rule, and the resolution — that the spread runs upward/outward FROM the protected frame and leaves such a child alone — is stated nowhere. Everything an addon draws rests on it. The in-combat pcalls are the half the claim is actually cashed for: all four setters sit in the protected-widget 59, and a `UI_SCALE_CHANGED` handler that re-`SetPoint`s carries no combat guard. Free rider: `:183`'s `[unverified]` on IsProtected()'s SECOND return is settled by recording both returns.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:131`, `security-taint-and-restricted-data.md:183`

**Status:** drained 2026-08-06

---

## OBS-059 · 2026-08-06 · Does `SetClampedToScreen(true)` re-clamp a frame parked past a screen edge when its own 

**Observed:** `frame-clamp-reapplies-on-geometry-change` recorded **ok** — `{readings=DISPLAY_SIZE_CHANGED, inline -> no resolved rect | UI_SCALE_CHANGED, inline -> no resolved rect | DISPLAY_SIZE_CHANGED, inline -> no resolved rect | UI_SCALE_CHANGED, inline -> no resolved rect | DISPLAY_SIZE_CHANGED, after a settle -> no resolved rect | UI_SCALE_CHANGED, after a settle -> no resolved rect | DISPLAY_SIZE_CHANGED, after a settle -> no resolved rect | UI_SCALE_CHANGED, after a settle -> no resolved rect | at rest, before parking -> no resolved rect | parked 120 past the top-left corner, same frame -> left=-0.0 right=128.0 screen=[0.0,1365.3] scale=0.640 onScreen=true | parked, after a settle -> left=-0.0 right=128.0 screen=[0.0,1365.3] scale=0.640 onScreen=true | immediately after SetScale(2), a geometry change of its own -> left=-0.0 right=256.0 screen=[0.0,1365.3] scale=1.280 onScreen=true | SetScale(2), after a settle -> left=-0.0 right=256.0 screen=[0.0,1365.3] scale=1.280 onScreen=true, scaleEvents=4}`

**How:** ClientLab run **2026-08-06 09:38:18** (v0.2.2, interface 120007), out of combat, instance `none`. A direct measurement in the client.

⚠ **The run quoted above is the FIRST of the session and predates the UI-scale change**, so its eight `no resolved rect` readings are the login-time events, taken before the frame was anchored. The screen-side half — four post-park firings across two UI-scale changes, `left` pinned at `0.0` at scales 2.000 / 1.560 / 1.280 — is on **run 17 of the same session** (`2026-08-06 09:42:48`), which is what `frames-textures-animation.md` §3.6 tabulates. `drain` picks the earliest complete run; both are the same session and the same date.

**Expected (questions.json):** UNKNOWN — Tier 1 declares the setter and says nothing about when it applies. The case that matters is a movable panel parked at an edge and then met by a resolution or UI-scale change: a one-shot clamp walks the panel off screen with no recovery but a position reset. ⚠ Three ways to read a wrong number, all designed against: `GetLeft()` is in the frame's OWN coordinate space, so every reading is converted to screen units and compared against UIParent's equivalent (otherwise SetScale 'measures' a clamp failure that is arithmetic); the C layer plausibly applies the clamp off-frame, so each step is read inline AND after a settle; and `run` executes on every retry tick, so the frame is created once at load, kept shown but empty so a hidden frame is not a fourth confounder.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `frames-textures-animation.md:467`, `frames-textures-animation.md:1540`

**Status:** drained 2026-08-06

---

## OBS-060 · 2026-08-07 · §4.8 — does LuaDurationObject:HasExpired / IsActive / HasStarted / IsZero return a PLAIN

**Observed:** `duration-predicate-secret-in-combat` recorded **ok** — `{HasExpired=<secret boolean>, HasStarted=<secret boolean>, IsActive=<secret boolean>, IsZero=<secret boolean>, control_GetRemainingDuration=<secret>, holdsSecrets=true, spellID=686}`

**How:** ClientLab run **2026-08-06 21:38:37** (v0.2.2, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** UNKNOWN, and the annotation is not evidence either way. §4.8's roster lists these four predicates with no SecretWhen* and no ReturnsNeverSecret — exactly the annotation state of GetRemainingDuration, which finding 7 measured SECRET in combat. So absence of a marker is known NOT to be a guarantee on this object. Three outcomes, all useful to projects/combat-assist: a PLAIN boolean makes ready(this) one exact call and deletes the readiness latch that 6 of 9 Demonology catalog entries depend on; a SECRET boolean still drives emphasis leak-free through SetVertexColorFromBoolean / SetAlphaFromBoolean (both AllowedWhenTainted with SecretArgumentsAddAspect) but may never gate a band condition; a raise means the route does not exist. HasSecretValues() is ReturnsNeverSecret and is the GATE — a duration holding nothing secret proves nothing, so the test refuses to answer until it finds one that does, and GetRemainingDuration runs as the control.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:1264`

**Status:** drained 2026-08-07

---

## OBS-061 · 2026-08-07 · In COMBAT, can a consumer read a row's current DISPLAY identity — via item:GetSpellID() 

**Observed:** `cdm-identity-readable-in-combat` recorded **ok** — `{auraBoundRows=2, getSpellID_plain=19, getSpellID_secret=2, infoOverride_plain=21, infoOverride_secret=0, rows=E/671 base=104316 ovr=104316 get=104316 aura=n | E/2742 base=265187 ovr=265187 get=265187 aura=n | E/34991 base=105174 ovr=105174 get=105174 aura=n | E/135056 base=1276452 ovr=1276452 get=1276452 aura=n | E/149122 base=196277 ovr=196277 get=196277 aura=n | E/1979 base=264178 ovr=264178 get=264178 aura=n | E/34990 base=686 ovr=686 get=686 aura=n | U/135274 base=1271802 ovr=1271802 get=1271802 aura=n | U/2425 base=119898 ovr=119898 get=119898 aura=n | U/2561 base=48020 ovr=48020 get=48020 aura=n | U/2254 base=104773 ovr=104773 get=104773 aura=n | U/782 base=108416 ovr=108416 get=108416 aura=n | U/2402 base=30283 ovr=30283 get=30283 aura=n | U/2512 base=6789 ovr=6789 get=6789 aura=n | BI/143038 base=296553 ovr=296553 get=296553 aura=Y | BI/9472 base=428514 ovr=428514 get=secret aura=Y | BI/9426 base=428514 ovr=428514 get=428514 aura=n | BB/777 base=264173 ovr=264173 get=264173 aura=n | BB/169561 base=1276166 ovr=1276166 get=1276166 aura=n | BB/84183 base=104773 ovr=104773 get=104773 aura=n | BB/760 base=104316 ovr=104316 get=secret aura=n, rowsSeen=21, verdictInput=info.overrideSpellID READ PLAIN on every row — the struct is an in-combat identity route}`

**How:** ClientLab run **2026-08-06 21:38:37** (v0.2.2, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** UNKNOWN, and the two candidate routes carry opposite evidence. item:GetSpellID() was measured secret on 8 of 51 rows and those 8 were exactly the rows carrying a live bound aura — so a row with NO bound aura may survive, but that was never measured separately. GetCooldownViewerCooldownInfo is Tier-1 documented as structural config 'readable even when live state is not', yet every reading of it on record was taken out of combat, including cap's own 200-row v0.2.0 capture. Splitting each row by auraDataUnit is the measurement: if secrecy tracks aura-boundness, a non-aura row is a working in-combat identity route. This gates projects/combat-assist catalog entry E6 (Ruination), whose whole content is a mid-combat transform — Bind refuses to resolve in combat, so without an independent read E6 is dead code that would pass every unit test and never light once in play.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `cooldown-manager.md:817`

**Status:** drained 2026-08-07

---

## OBS-062 · 2026-08-07 · For a LuaCurveObject with points (0,10) and (20,20): what does Step snap to between them

**Observed:** `curve-step-and-clamp-semantics` recorded **ok** — `{emptyCurveAt5=0, linear=-5=10 0=10 5=12.5 9.9=14.949999809265 10=15 10.1=15.050000190735 15=17.5 19.9=19.950000762939 20=20 25=20 100=20, step=-5=10 0=10 5=10 9.9=10 10=10 10.1=10 15=10 19.9=10 20=20 25=20 100=20}`

**How:** ClientLab run **2026-08-07 14:30:54** (v0.2.2, interface 120007), out of combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** UNKNOWN on both cells, and NEITHER needs a secret — curve semantics are a property of the curve, so plain inputs settle them and this answers out of combat on the first run. STEP DIRECTION: the docs say 'performs no interpolation between points, instead snapping to values exactly' without saying WHICH point. Previous-point-hold and nearest-point are both consistent and put a threshold in different places — with points at 0 and 20, hold gives an edge at 20, nearest gives one at 10. Read y at x=9.9 / 10 / 10.1 to separate them. OUT-OF-RANGE: clamping is INFERRED and never documented — Blizzard's EncounterTimelineTrailAlphaCurve defines points only at x=0.0 and x=0.1 yet drives alpha across a full 0..1 progress, which only works if x>0.1 clamps to the last y. x=-5 and x=100 settle it. Nothing in the shipped UI uses Step at all, so there is no precedent to read either off. Gates whether projects/combat-assist may threshold a cooldown with a Step curve or must pad a Linear one.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:1464`

**Status:** drained 2026-08-07

---

## OBS-063 · 2026-08-07 · §4.8.4 — with a NON-secret curve, does LuaDurationObject:Evaluate*(curve, modifier) retu

**Observed:** `duration-curve-result-secret` recorded **ok** — `{EvaluateElapsedDuration=<secret number>, EvaluateElapsedPercent=<secret number>, EvaluateRemainingDuration=<secret number>, EvaluateRemainingPercent=<secret number>, EvaluateTotalDuration=<secret number>, control_GetRemainingDuration=<secret>, curveSecret=false, holdsSecrets=true, spellID=686}`

**How:** ClientLab run **2026-08-07 14:31:18** (v0.2.2, interface 120007), in combat, instance `none`. A direct measurement in the client.

**Expected (questions.json):** UNKNOWN, and the annotation is the whole problem. All five Evaluate* methods carry `SecretWhenCurveSecret` — secret WHEN THE CURVE IS — and ours is not. Read literally that returns a READABLE number derived from a duration measured SECRET on the same object (§4.8.4, GetRemainingDuration), which would let a caller binary-search the remaining time. Either the annotation is incomplete or it is a leak; §4.8.4 records the cell as unmeasured rather than guessing. The curve is an identity over 0..600 so a PLAIN result is legible as the remaining time itself rather than as an opaque number. `HasSecretValues()` on the DURATION is the gate — an unrestricted duration proves nothing — and GetRemainingDuration is the control; if the control reads plain the object is not restricted and every other cell is meaningless. A table result is checked at a MEMBER, since a colour result is a readable table with secret members (§4.8.1 finding 9). The answer decides what an addon may DO with the result, not whether the route works: SetDesaturation and SetVertexColor take a secret either way. PLAIN is the finding that matters — it means the graded emphasis route hands Lua a value the restriction exists to withhold, which is a legitimacy problem for projects/combat-assist §5 rather than a technical one.

**Confidence:** high — the client answered directly. Low only if the result contradicts `expect` in a way that suggests the test asked the wrong thing.

**Drains to:** `security-taint-and-restricted-data.md:1657`

**Status:** drained 2026-08-07
