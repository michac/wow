# Cooldown HUD — notes archive (superseded / parked)

> **Nothing in this file is current.** It's the rabbit-hole record: work we did,
> decisions we reversed, and machinery we built understanding for and then chose
> not to ship. It exists so `notes.md` can be *only* what informs the current
> framing, without us losing the reasoning — or re-deriving a dead end twice.
>
> **Read `notes.md` for what's true now.** Every entry here says what it was, why
> it's parked, and what would revive it.
>
> Split out of `notes.md` on 2026-07-20.

---

## A. The green-phosphor era — icon tinting and the 4-letter labels

**Status: reversed 2026-07-19** (the M3 aesthetic revision, `milestones.md` §6).
The terminal/TUI *feel* survived; the icon treatment did not.

**What we believed.** v1 was "CRT / green-phosphor," and crucially a *treatment of
Blizzard's real icon columns*: keep `item.Icon`, `SetDesaturated(true)` +
`SetVertexColor` it to uniform green, and surround it with monospace **4-letter
labels** + keybinds, block-char meters and a scanline/vignette overlay. Identity
was to be encoded as `colour(group) × position × 4-letter label`. The M1 prototype
built exactly this and the feasibility questions all passed (`notes.md` §9 F1–F5).

**Why it's parked.** Looked at in anger, desaturating + green-tinting the icons
measurably **hurt cooldown legibility** — the native swipe and countdown both read
worse — which defeats the entire point of keeping the icons rather than drawing
abstract blocks. The 4-letter labels went with it: they obscured the swipe and only
paid off in a solid-colour skin where the icon art is gone. v1 now leaves icons
**native and untouched** and puts the value-add in the chrome around them.

**What survives in `notes.md`.** The leaf-method hook mechanism (§9) is **kept and
dormant** — it's the machinery any future tinting needs. The F1 verdict ("keep +
tint is feasible") remains true; we just don't exercise it.

**What would revive this.** An **optional solid-colour mode** — a skin variant that
hides the icon art entirely and draws abstract blocks, where the group hue *is* the
identity and 4-letter labels earn their place again. That's the future the dormant
hooks gate.

### The visual-style exploration (2026-07-17)

Two published artifacts drove the original decision; both are history now.

1. **"Demonology CDM — 5 design directions"** — layout exploration: (1) Priority
   Column, (2) Burst Lane, (3) Resource-Centric, (4) Compact Dashboard,
   (5) Clear-the-Board. Interactive, solid-colour, JS-animated, each animating only
   what the capability map allows (shard fills + cap glitter = ours; cooldown swipe
   drain = borrowed; proc glow = presence). In-repo:
   [`../prototype/cdm-designs.html`](../prototype/cdm-designs.html),
   [`../prototype/resource-centric.html`](../prototype/resource-centric.html).
2. **Visual-style exploration** — restyled the **real Blizzard icon columns**
   (addon-feasible ops only, each direction captioned with its "WoW mapping")
   across five aesthetics: (A) Gnomeregan powered-goggles, (B) **CRT /
   green-phosphor ← chosen**, (C) LCARS, (D) Bound Grimoire, (E) Neon District
   (cyberpunk). In-repo:
   [`../prototype/overlay-styles.html`](../prototype/overlay-styles.html);
   published: <https://claude.ai/code/artifact/939bac84-6701-4eab-ae7c-33f70d40a327>.

**Findings worth keeping:** LCARS elbow curves and grimoire ink-wobble need bespoke
texture art or are outright unbuildable; **CRT was the most natively feasible**,
which is why it won. The direction-B terminal chrome (`DEMONOLOGY.SYS`
header/footer, blinking `C:\>_` prompt) was brought into the addon in M1 and
**survives the revision** — it's the part of "CRT" that was never about the icons.
The **cyberpunk direction (E)** stays alive as the M7 stretch art pass.

**Dead question:** "icon-tint brightness — bright & readable vs dimmed 'text-first /
ghostly icons'." Moot; we don't tint.

---

## B. The layer-① curated-layout machinery

**Status: understood, proven writable, then deliberately not shipped** (M2 decision,
2026-07-18). Parked for **M7**.

**What we believed.** §0 pillar 1 made an *imported* Cooldown Layout string a hard
dependency — one blessed layout per spec, "not negotiable," with the overlay's
colour/priority/keybind map keyed to an exact known tracked set and order. We did
the full source dig to make that shippable.

**Why it's parked.** Binding per item by `GetCooldownID()` on the `RefreshLayout`
hook gets us the same determinism against **whatever layout is active**, and
reorder-safety plus missing-spell-skip fall out for free. Asking the user to import
anything became pure cost. Design baseline is now the real DB2-default filtered set
(`CooldownSet`/`CooldownSetSpell`, spec 266 = set 60).

**What would revive it.** Two triggers, both live: (a) the DB2 defaults proving
insufficient — the noisy 13-spell Utility default is the likely one; (b) **§0.5.8
#18, the predictive Diabolic Ritual tracker**, which *requires* the per-stage ritual
auras in the tracked set (only the `428514` container is tracked today). Either
re-opens this as M7 work, at which point everything below is the head start.

### The mechanism (verified against `Gethe/wow-ui-source` @ build 68453 = 12.0.7)

Sources: `Blizzard_CooldownViewer/CooldownViewer.lua`,
`CooldownViewerSettingsDataStoreSerialization.lua`,
`Blizzard_APIDocumentationGenerated/EditModeManagerConstantsDocumentation.lua`.

**Layer ① — the Cooldown Layout string.** "Cooldown Settings" panel → *Copy to
Clipboard / Import*; backed by `C_CooldownViewer.GetLayoutData()` /
`SetLayoutData()`. Carries the **tracked set + per-cooldown category** (Essential /
Utility / Hidden, and buff **Icon** = `TrackedBuff` vs **Bar** = `TrackedBar`) +
**order** + **per-cooldown alert overrides**. Spec-aware (keyed by class+spec tag).
Carries **no** orientation/size/position.

**Exact serialized fields:** `COOLDOWN_ORDER`, `CATEGORY_OVERRIDES`,
`ALERT_OVERRIDES` — CBOR → Deflate → Base64, prefixed `<encodingVersion>|`. Two
consequences worth remembering:

- **Alerts ride inside the string.** A chunk of the §3 / M6 audio+visual alert set
  (`Available` / `OnCooldown` / `PandemicTime` / **`OnAuraApplied`** …) ships
  *inside* the import string — secure and combat-safe — rather than needing
  programmatic injection.
- **Icon-vs-bar for buffs is just a category** (`TrackedBuff` vs `TrackedBar`), so
  it travels in the string too; there's no separate setting to configure.

**Auto-apply is viable (probed 2026-07-17, `/cdmp layout write`, out of combat):**
the call is permitted from addon code, no blocked-action error. Two caveats for
*how*:

- `SetLayoutData(str)` replaces the **whole** data store — every spec's layouts.
  Don't clobber.
- The clean single-layout **merge** is
  `CooldownViewerSettings:GetLayoutManager():ImportLayout(str, info)` — the path the
  Import button itself calls. **Prefer the merge.** (Sub-probe never run: is
  `ImportLayout` addon-callable too? In-combat writability untested, expected
  blocked.)

So enforcement strength (auto-apply → import-and-verify → nag) was always a **UX
choice, not a capability question** — which is exactly how M7 inherits it.

---

## C. Superseded claims and assumptions

Kept so nobody re-derives them from an old draft.

**C1. "Post-hook `RefreshData` to persist the tint."** *Wrong* — corrected in M1
(v0.5.2). Blizzard re-colours the icon from paths **outside** `RefreshData`, so this
still flashed white on the usable/range paths (status showed 65 hook fires while
visibly flickering). The correct mechanism — per-item **leaf**-method hooks — is
current and lives in `notes.md` §9. *(Doubly moot now: we don't tint at all — see A.)*

**C2. "`RefreshLayout` is the single persist watchdog."** Same error, stated
architecturally. `RefreshLayout` handles **relayout and re-hooking newly-pooled
items** — real jobs it still does — but it does **not** fire on per-item recolour
paths, so it was never the tint watchdog.

**C3. The burst window = Tyrant + Dreadstalkers + Grimoire + Summon Doomguard.**
Wrong twice over. **Doomguard is neither tracked nor cast** in the modern build
(dropped per `diabolist-sequences.md`), and the go-gate must **not** include the
Grimoire summon: it's a ~2-min cooldown, absent from roughly half the windows (21
casts vs 48 Tyrant across the top parses), so gating on it suppresses the cue half
the time. Correct gate: **Tyrant + Dreadstalkers**, Grimoire brighten-if-up.
*(`guidance-model.md` §0.5.8.6 blocking error #2.)*

**C4. The old "what drives salience" list.** §2 once carried a four-bullet sketch
(shards / Core presence / imp presence / cooldown-ready). It was a reasonable first
pass and is now **wholly superseded** by `guidance-model.md` — §0.5.2 ranks ten
moments by tier, §0.5.4 maps each to a readable trigger and an own/borrow/can't
verdict, and §0.5.8.3 commits the 18-row v1 set. Use those; the sketch under-serves
AoE and has no mode model.

**C5. "v1 standardizes on one CDM profile — candidate Kalamazi 'Demonology CDM'."**
Superseded by B: v1 ships **no profile**. The candidate is recorded only in case M7
re-opens the curated-layout question and wants a starting point.

**C6. The `Core*` verify gate.** Rows #7/#8/#10/#11/#12 of §0.5.8.3 were committed
as `Core*` — real targets carrying a stated reactive/borrowed fallback in case the
in-combat cast-ID read proved secret. **Closed 2026-07-20** as a design assumption
(START and SUCCEEDED are taken to carry a readable spellID in all combat contexts);
asterisks retired. The fallback is no longer a planned degradation path, only a
recovery if the assumption is ever falsified in play.

**C7. "[X]/4" for the Wild Imp readout.** The imp and Core counts were once one
note sharing the Demonic Core cap of 4. The Wild Imp gate is **≥6 → Implosion**, so
that readout is **"/6"**; `/4` is only ever the Demonic Core cap. Shipping the old
note would have put the wrong denominator on the one v1 AoE assist.
