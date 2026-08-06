# Combat Assist Plus — notes

**What this file is for:** the running record of what we did — session logs,
decisions and why they went that way, things we tried that didn't work, in-game
observations. Append-only in spirit: this is the file you read to find out how the
project got where it is.

It is deliberately the *loose* one. `spec.md` says what the addon should do and
`backlog.md` says what's left; anything that doesn't fit either — a measurement, a
dead end, a rationale, a "next session, start here" — lands here rather than
getting lost or being forced into a spec line.

Newest session at the top. Date each entry.

⚠ **A fact about how the game or the API behaves does not stop here.** That goes to
`knowledge/addon-dev/` (see the wow-developer skill's "Improve the KB as you go") —
this file records *our* work, not the client's behaviour.

---

## 2026-08-05 — M2 and the catalog, built in parallel

Four tracks run concurrently — three subagents plus the integrator — after checking that
the backlog's apparent M2→M3→M4→M5 line is not the real dependency graph. It isn't: the
**catalog** blocks M3/M4/M5 and needs no addon code at all, and the **movable frame** has no
CDM dependency, so only the CDM binding was ever on the critical path.

**The constraint that shaped the split was the repo, not the work.** Two tracks write Lua
into `addon/`, a separate gitignored git repo, and they share two surfaces no matter how
cleanly the modules divide: the `.toc` file list and `ns.Commands`. So the shared surface
was landed first — `Core.lua` gained **`ns.RegisterCommand{...}`** (replacing the array
literal) and **`ns.RegisterStatus(order, fn)`** (replacing the hardcoded `cmdStatus` body),
after which each module registers its commands and its own `/cap status` line from its own
file and never touches Core. `Bind.lua` and `Frame.lua` were stubbed and `.toc`-listed by
the integrator. ⚠ Worktree isolation would have been **wrong** here — a worktree of the wow
repo does not carry the gitignored addon clone.

**⚠ Nothing built this session has run in the client.** cap **is** released and deployed —
but at **v0.1.1, the scaffold**: the game folder holds `.toc` + `Core.lua` only. `Bind.lua`
and `Frame.lua` exist solely in the working tree, and `ghaddons` installs from the latest
GitHub *release*, so a new cut is what puts them in the game. Every acceptance item below is
unflown, and the gate used was parse (luaparser) plus inspection against
`knowledge/addon-dev/`. *(The project `CLAUDE.md` said "no release has been cut" — stale
since v0.1.1; corrected the same day.)*

**Track A — the catalog gets a shape, and Demonology gets one.** `spec.md` §3.5 now defines
what a spec declares: applies-to, roster, windows, entries, silence, sequences — **data in a
closed vocabulary, not code**. Three devices do the load-bearing work, all aimed at §3.1's
third rule. **Entries cannot see each other** (a condition may name only its own ability,
resources/player buffs and windows — there is no syntax for another entry's tier or
readiness, so mutual exclusion, which is what a priority list is made of, is inexpressible).
**Band conditions are positive** — no negation; a held ability is *promoted* where pressing
it is right and demotes by falling through, forcing the author to name a fight situation
rather than an order. **Cross-ability reasoning happens only in a window**, capped at six and
named after situations. The vocabulary splits into **gates** (branchable) and **channels**
(display-only), which is how Secret Values became structural rather than a discipline:
`impCount >= 6` is not writable as a band condition because the only stack-count term is a
*cue* term. Two things are now checkable rather than hoped-for — **coverage** (every
CDM-tracked row must be an entry or a declared silence with a reason) and the **breadth
measure** (how many entries are HIGH at once).

`specs/demonology/catalog.md` is the first catalog: 9 entries, 5 windows, 4 bars, 11 declared
silences. The APL→tier-field translation is not mechanical and two places show it.
**Implosion can never be HIGH** — its true gate is the sealed Wild Imp count, so the tier says
"the button is up", a threshold cue says "the imps are there", and the player does the AND.
**Dreadstalkers' hold** is two positive windows (`tyrant_setup`, `tyrant_far`) with a
deliberate gap between them, so the hold zone is where neither is true and no band says "not".

**Track B — bound to the Cooldown Manager.** `Bind.lua` resolves the four CDM viewers into
rows keyed by `cooldownID`, each carrying the rule-15 spellID union (base ∪ `overrideSpellID`
∪ `overrideTooltipSpellID` ∪ resolved live id) with the linked pool kept separate, exposed on
`ns.Bind` (`Rows`, `Row`, `RowsForSpell`, `ItemFrame`, `Health`, `Generation`, `OnChanged`).
Rebinds fire on spec, talent, hero-tree, `SPELLS_CHANGED` and the three CDM events, coalesced
through a 0.2 s timer and **refused in combat** — a rebind under lockdown queues and drains on
`PLAYER_REGEN_ENABLED`. The decision that shaped everything else: **a read is three-way, not
two-way.** An *empty* item frame is a real "nothing here" (viewers pad to a minimum of two); a
*secret or throwing* read is "no answer", and a pass containing one is marked incomplete,
retaining the previous rows flagged `stale` rather than dropping them — so a CDM that goes
unreadable leaves cap holding a stale-but-correct binding instead of an empty one. Missing-CDM
states (`no-addon` / `unavailable` / `disabled` / `empty` / `hidden`) announce **once on
transition**, re-arm when the state clears, cap at three per session, and defer five seconds
past login so the async CDM data load cannot raise a false alarm.

**Track C — the movable panel.** `Frame.lua` builds `CombatAssistPlusPanel`, anchored to
UIParent and explicitly *not* to the CDM. `/cap move` toggles placement (out of combat only,
auto-locked on `PLAYER_REGEN_DISABLED` with an in-flight drag stopped and saved cleanly);
`/cap move reset` recentres. Unlocked it shows backdrop, border and label; locked and empty it
has no regions and no mouse, so it is invisible and inert while still present for M4's bars.
Position persists as the panel's centre offset from UIParent's centre **in UIParent units
normalised to scale 1.0** — Blizzard's own Edit Mode form (`EditModeManager.lua:295-320`,
restore at `EditModeSystemTemplates.lua:375`) — resolution-independent because the UI's root
space is a fixed 768 units tall, scale-independent because restore divides by current scale.
Every geometry read is guarded and **refuses to save rather than write an unmeasured number**
(OBS-049: a secret stored in SavedVariables comes back `nil` after `/reload`, so an unguarded
save would silently blank the position). **The frame is deliberately non-secure** — cap never
takes a protected action, protection is one-way and contagious to parents and anchor targets,
and staying unprotected is precisely what will let M4 relayout bars mid-pull. M4's seam is
`ns.Frame.Attach(region, height)` / `Detach` / `Relayout`, with the row height passed in as a
plain number so no bar's secret geometry can reach the container's own size.

**Track D — Cooldown HUD marked superseded.** Banners on `projects/cooldown-hud/CLAUDE.md`,
`docs/status.md` and `docs/multi-class-rollout.md`, and both root-`CLAUDE.md` side-project
entries rewritten. `status.md`'s routing rule ("plan the next cooldown-HUD thing starts
HERE") is **revoked** and its backlog is explicitly no longer a queue; the auto-deploy
exception is dead with the project. The root entry for cap no longer says "what it's for is
deliberately undefined", which was the stalest line in that file.

**Two corrections to our own spec, both found by building against it.**

1. **§3.1's own HIGH example was unimplementable.** "Implosion off cooldown **and** at 6+
   imps" requires branching on a sealed stack count — asserted two paragraphs above the
   section explaining why that cannot be done. Fixed in place, and §3.1 now states the
   tier/cue division explicitly.
2. **§4's Assisted-Combat rationale was factually wrong**, and so is the 2026-08-05 entry
   below that argued it. **Demonic Strength, Bilescourge Bombers and Guillotine are not on
   the Midnight Demonology tree at all** (no row in `all-talents.tsv` @ 12.0.7.67808 — for
   any spec), and **Doom is a PASSIVE** (talent 460551, applied by Demonbolt). So four of the
   five abilities we cited as damning omissions were *correctly* omitted; the list's only real
   omission is Implosion. **The decision to drop the assist stands unchanged** — the shape
   objection (one answer where cap is a field) was always the strong argument and is now the
   stated one. Verified independently by the integrator against `all-talents.tsv`; Implosion
   and Power Siphon are confirmed a CHOICE pair on node 101893, so exactly one exists per build.

⚠ **That correction rests on a claim the KB itself marks unresolved.**
`knowledge/classes/warlock/demonology/abilities.md:89-91` carries the same "not on the current
Midnight Demo spec tree" statement with an **`@verify-ingame`** marker still open. Two
independent sources agree (the DB2-derived talent table and that file), but by the workspace's
own rule a marked claim you are about to build on is a **STOP: ask**. The catalog's three
"not on the spec" silences inherit it.

**Decision, taken the same session and against the catalog as authored: a threshold cue
is drawn in the tier it stands for.** The catalog pass had Implosion's imp count as a
neutral marker beside a MEDIUM icon, with the player expected to AND "the button is up"
against "the imps are there". The author's call: **draw the number in the HIGH treatment**
— the same colour and styling as a HIGH icon — so Implosion simply *reads* HIGH.

This does not relax §5 and does not touch what cap may branch on. The composition is
`ready(this)` (cap's gate, band-legal) → `stacks(Wild Imp) ≥ 6` (the client's threshold,
never seen by us) → drawn HIGH. cap still never learns the count; what changed is that the
**presentation** carries the meaning cap is not allowed to compute, which is move 2 of §1
applied to the register that had been treated as second-class. §3.1 now states it as a
rule: *the two registers differ in resolution, never in vocabulary* — an emphasis that
means HIGH looks like HIGH, whoever did the arithmetic, and the player is never asked to
learn a second visual language.

It also fixes something the catalog had backwards. Implosion's entry justified having no
HIGH partly because a 15s cooldown would leave a HIGH band permanently lit — true of a
*band*, but not of the cue: the imp count crosses 6 in bursts, so a HIGH-styled number
arrives and leaves with the actual opportunity. The cue is the *better* signal here, not
the consolation prize. Two consequences elsewhere: §3.5 gained a **cue honesty** check (a
HIGH cue must carry a gate precondition, or it is permanently lit and reads as "always
press this"), and the breadth check now counts HIGH-declaring cues as HIGH-capable
entries, which takes the Demonology catalog from six to seven.

**Open, and escalated rather than decided:** the **dark field** (Demonology's filler is not
CDM-tracked, so LOW has nothing to draw on and a common state has nothing lit — teach "nothing
lit means go build", or have cap draw its own icons, which is a different addon from one that
rides the CDM); and **target count** (no vocabulary term supplies it, no KB fact establishes
whether it is readable, so every AoE opinion on Demonology is currently unsayable). Both are
now `spec.md` §6. The sequence work is the weakest part of the catalog — the opener was
**deliberately not authored**, because the sources describe it starting with Power Siphon,
which needs Wild Imps you do not have at a pull.

## 2026-08-05 — the tier model replaces the assist, on evidence

§3.1 was rewritten the same day it was written. The verbatim-Assisted-Combat design
lasted exactly as long as it took to read Blizzard's actual Demonology list.

**What killed it.** `raw/addon-research/simc/ActionPriorityLists/assisted_combat/warlock_demonology.simc`
— the in-client Assisted Combat priority list, from the `AssistedCombat*` DB2 tables:

```
summon_felguard (×2) · call_dreadstalkers · ruination · hand_of_guldan
infernal_bolt if buff · shadow_bolt if buff
# "for Blizzard automation, not included in the game's Assisted Combat system":
summon_demonic_tyrant · demonbolt if demonic_core · power_siphon · …
```

The author's worry was that the assist would recommend **Implosion** below 6 imps and
stick there. It cannot: **Implosion is not in the list at all.** Neither are Demonic
Strength, Bilescourge Bombers, Guillotine or Doom. And `hand_of_guldan` carries **no
shard condition**, so a hand-written "MEDIUM when you have the shards" rule is strictly
*more* informative than Blizzard's own line. Under the stricter reading of that comment
(which the destruction and fire files support, though retribution's placement of the
same comment at the top of its list muddies it) the assist also omits **Demonbolt-on-Core
and Tyrant** — which would have shipped a HUD that never highlights Demonbolt on proc,
while §3.2 is a feature entirely about Demonbolt procs. Incoherent either way.

So §3.1 had to change regardless of what replaced it. `[T1: DB2-derived]`

**What replaced it.** The author's own proposal: a **tier signal** — HIGH / MEDIUM /
LOW emphasis across the tracked set, with sequence hints layered on top. Adopted
wholesale, and the assist dropped **entirely** rather than kept as a fallback (the
offered middle option). §6's first open question is therefore answered at M1 instead of
M7, which is what it was written to allow.

The argument that made it more than a preference: **tiers unify §3.1, §3.2 and §3.4 into
one engine at three surfaces.** Smart procs stop being a feature and become an *input*
to the tier; the cooldown bars' urgency treatment is the same signal on a second
surface. That is a real simplification, not a rationalisation of a change already made.

⚠ **The risk it introduces, written into §3.1 as an enforceable rule and into §6 as the
thing to measure:** tiers are a priority list with extra steps *if in practice exactly
one thing is ever HIGH*. Hence the three rules — tiers describe value not order, cap
never ranks within a tier, and a tiering that collapses to one answer per GCD is
mis-designed rather than shippable. M3 carries an item to instrument this.

**The visual vocabulary, and why it has two registers.** Checking the tier inputs
against what the platform allows produced a sharper split than expected:

| Input | Continuous emphasis? | Threshold? |
|---|---|---|
| Soul Shards | ✅ readable *and branchable* — no indirection needed | ✅ |
| Cooldown remaining | ✅ duration object is itself a curve evaluator (§4.8.1 finding 4) | ✅ |
| Proc presence | ✅ presence is readable; only the stack *count* is sealed | ✅ |
| **Wild Imp count** | ❌ **no curve sink exists at all** | ⚠ text only |

So the imp count is the single odd input out. §4.8.2's shipped technique —
`GetAuraApplicationDisplayCount(unit, id, min, max)` quantising in C, empty string below
the threshold — is text-shaped and cannot reach alpha, colour or a bar. Offered
text-as-glyph / napkin-the-count-in-Lua / accept-binary, the author's call was
**glowing text, and "that's plenty signal"**. §3.1 now states both registers and
explicitly forbids contorting the design to make a stack count fade. The napkin-count
idea is parked in the backlog rather than discarded.

**A distinction worth not re-litigating:** `projects/cooldown-hud/specs/demonology/observability-map.md`
calls the imp count *"provably unreadable"* (`imp-side-channel-closed`). That is **not**
in conflict with §4.8.2. It is scoped to reading the count *into Lua to feed a priority
engine*, which remains true. Showing a threshold was never the same question, and the
distinction is the entire basis of this design.

## 2026-08-05 — the spec, and cap supersedes the Cooldown HUD

`spec.md` §1–§5 written from a design conversation. The shape of it, and why each
call went the way it did:

**The origin is a retreat, and that's the point.** CDMProbe started as "what can I
do with the CDM" and evolved into a next-action HUD — a decision engine. Two things
made that untenable rather than merely unfashionable: it runs against Blizzard's
stated position on combat addons, and the 12.0 restrictions had already started
capping what it could calculate. cap is the same premise re-aimed at what the
platform actually invites: **re-present, grade, contextualise** — narrow the
decision, don't make it. The restrictions stop being a wall to route around and
become the design brief.

**Decisions taken (all the author's):**

- **cap supersedes Cooldown HUD.** Not a sibling, not a handoff after the Havoc
  flight — a replacement. CDMProbe's *code* is not carried over; its measured
  client facts are already in `knowledge/addon-dev/` and stay authoritative, and
  its per-spec rotation research is worth harvesting into catalogs. ⚠ The
  cooldown-hud docs and the root `CLAUDE.md` still read as if it's the live CDM
  addon — backlogged, not yet done. **Its outstanding Havoc flight is now moot as a
  CDMProbe deliverable.**
- **Fully fresh code.** No pipeline port. The Coach/Binder/Renderer architecture was
  shaped around authoring a priority answer, which is the one thing cap doesn't do;
  inheriting it would smuggle the premise back in.
- **The assist line is deliberately provisional.** v1 surfaces
  `C_AssistedCombat`'s pick verbatim and cap authors no priority list of its own.
  The author's framing: *play it by ear — start with verbatim, re-approach if that
  plus the other three features still leave me information-starved.* Written into
  the spec as §6's first open question and M7, so it's a scheduled revisit rather
  than a boundary someone has to argue their way past later.
- **Demonology first**, one spec at a time, per-spec catalogs.
- **Procs: replace, don't annotate.** Blizzard's glow gets suppressed and redrawn
  graded, rather than overlaid with a veto mark. One signal, ours, with a fade
  rather than a flip wherever the deciding quantity is continuous.
- **Sequences: auto-detect only.** A manual arm was offered and declined — being
  asked to declare "I am now opening" at the moment you're opening defeats the
  purpose. The cost is accepted false positives, so the spec makes *losing the
  thread silently* a first-class requirement.
- **Cooldown bars: free-floating**, not anchored to the CDM. Place them where your
  eyes already are.
- **Audience: me first, public later.** No settings panel in v1; nothing hardcoded
  so hard that publishing becomes a rewrite.

**The technical ground was checked before writing, and it holds.** The author's
instinct that this would be built on "curves based on secret values" is exactly
right: `security-taint-and-restricted-data.md` §4.8/§4.8.1 records the measured
channels that carry a secret (alpha, vertex colour, desaturation, bar value,
rotation, duration objects), and §4.8.1 finding 3 has a **live in-combat cooldown
bar drawing off a secret duration** already proven on Demonology's Summon Demonic
Tyrant. So §3.4 rests on a measured mechanism, not a hope, and §3.2's graded
fade has a sanctioned route even when the deciding quantity is unreadable.
`C_AssistedCombat.GetNextCastSpell` is measured readable in combat
(`cooldown-manager.md` §7) — with the caveat that its *usefulness* was never
sampled, only its readability.

⚠ **Open risk carried into M3:** the one capture that sampled `GetNextCastSpell`
recorded a constant `691` at every sample and the recorder dedups by readability
class, so nothing yet shows the value tracks the rotation at all. §3.1 assumes it
does. **A value-sampling pass is the first thing M3 should do** — if the oracle
doesn't move, §3.1 has no content and §6's first question gets asked immediately
instead of at M7.

## 2026-08-05 — scaffold

Created the project and the addon repo `michac/cap` from scratch.

- `projects/combat-assist/addon/` — own git repo, gitignored by the wow repo, same
  arrangement as CDMProbe / BucketBinds / PlannerState. Pushed, public, MIT.
- `CombatAssistPlus/` — `.toc` (Interface 120007, v0.1.0,
  SavedVariables `CombatAssistPlusDB`) + `Core.lua`: namespace, a defaults merge on
  `ADDON_LOADED` that fills new keys without clobbering saved ones, and the `/cap`
  router built off an `ns.Commands` schema table with exact-match dispatch and a
  prefix-only "did you mean" (house rule 7 — no substring dispatch). `status`,
  `toggle`, `help`. No combat code, no frames.
- Registered as `cap` in `wowkb.addon` (→ `michac/cap` →
  `projects/combat-assist/addon`, confirm hint `/cap status`) and added to
  `addon-manager/config.json`. `release cap --dry-run` runs clean end to end.
- **No release cut**, so `ghaddons` has nothing to install — the addon is not in the
  game folder yet.

Decision: what the addon *does* was left undefined on purpose rather than guessed
at. `spec.md` §6 carries the open questions.
