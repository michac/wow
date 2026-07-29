# Observability map — the Destruction APL inputs vs. what the game lets us read

> **⚠ STATUS: reference / desk-derived.** For each field the priority list needs
> (`input-contract.md`), where the value comes from in the State pulse, how reliably it
> reads **out of combat vs. in combat**, and how it degrades. The list itself
> (`rotation.md`) is unchanged — this only says *how honestly each input can be fed*.
> Unlike the Demonology map, **none of this has been confirmed against a live
> Destruction capture**; the Secret-Value facts carry over from Demonology's probe, the
> Destruction-specific ones are marked **verify**.

## Sources of truth for this pass

- **What the client exposes** — the reduced-State pulse: per-cooldown `cd`
  (`state ∈ ready|on-cooldown|unknown`, `source ∈ live|napkin|none`, `remaining`),
  `glow` (the combat-readable spell-overlay proc signal), `aura`/`buff.isActive`
  (buff presence), `power.<PowerType>.{value,incoming,max}`, cast `history`, the spell
  `override`/`liveSpellID` (transforms), and `mode` (st/aoe).
- **What's provably secret** (from the Demonology probe, class-independent):
  **in-combat cooldown reads go secret** (readiness survives via an OOC baseline +
  observed alert edges); **buff *presence* is readable, buff counts/durations are
  not**. Destruction inherits both walls.

## The readiness model (unchanged from Demonology — read that first)

Cooldown readiness is **observed, not guessed**: an observed CDM alert edge, else the
OOC-readiness baseline carried across combat entry, else the napkin (base-cooldown
countdown from the last observed cast, which supplies *remaining* only and expires to
"probably-up, **unconfirmed**" — never a laundered `ready`). Full statement in
`specs/demonology/observability-map.md`; it is spec-agnostic and transfers verbatim.

**One Destruction-specific hole in it: charges.** Conflagrate and Shadowburn are
2-charge abilities and Demonology has none, so the `charge` half of the full-database
read is still `@verify-ingame` (`docs/status.md`). Until it is closed, a charged
ability's readiness is binary — "some charge available" vs "none" — and the napkin
cannot model recharge at all (it counts one cooldown, not a refilling pool).

## The map

| # | Field | Source in the pulse | OOC | In combat | Confidence | Degrades to |
|---|---|---|---|---|---|---|
| 1 | `shards` (whole) | `power.SoulShards.value + .incoming` | exact | **readable** (power survives combat) | **High** | value secret one pulse → unknown; don't force a shard gate |
| 1b | `shards` (fragments) | **not read today** — see *the fragment read* below | — | — | **Absent** | falls back to whole shards + the rounded gates |
| 2 | `ruination_up` | `override`/`liveSpellID` on the **Chaos Bolt** frame = the Ruination Art id | exact | **readable** (override event fires in combat, per Demo) | **Med–High — verify ID** | no override seen → false. ⚠ the Destruction Ruination ID is *not* Demo's (`notes.md`) |
| 3 | `soulfire_usable` | `cd` on Soul Fire (readiness model) | exact | edge/baseline observed, else napkin | **Med–High** | unknown → false |
| 4 | `art_armed` | Diabolic Ritual `428514` `buff.isActive`, and/or the CB override edge | exact | **readable (presence)** | **Med–High** | neither → false. Expect `428514` tracked **twice** (Demo finding) — key on cooldownID |
| 5 | `cb_usable` | `shards >= cost` (cost live via `ns.ShardCost`) + off GCD | exact | **readable** | **High** | cost unreadable → assume 2 |
| 6 | `conflagrate_usable` | `cd` + **charges** on Conflagrate | exact | edge/baseline/napkin, **no charge count** | **Med — charge gap** | binary off-cd; under-presses rather than dumping a banked charge |
| 7 | `backdraft_present` | Backdraft `117828` `buff.isActive` | exact | **readable (presence)** | **High (presence)** | not readable → false. **Count is secret — never inferred** |
| 8 | `infernal_castable` | `cd` on Summon Infernal (readiness model) | exact | edge/baseline observed, else napkin | **Med–High** | unknown → false. Base CD is **120 s (90 s w/ Inferno)** — talent-dependent, so read live, don't hardcode the napkin |
| 9 | `chaotic_inferno` | Chaotic Inferno `1244860` `buff.isActive` / glow on Incinerate | exact | **readable (presence)** | **Med — verify** | ⚠ if Incinerate is untracked there is no frame to glow; the aura read is the only route |
| 10 | `incinerate_usable` | no cd / no cost | true | true | **High** | only false if locked out |
| 11 | `shadowburn_usable` | `cd` + **charges** + `shards >= 1` | exact | edge/baseline/napkin, **no charge count** | **Med — charge gap** | as #6 |
| 12 | `fiendish_cruelty` | Fiendish Cruelty `1245664` `buff.isActive` | exact | **readable (presence)** | **Med — verify tracked** | not tracked → false, and L7 loses half its gate |
| 13 | `target_execute` | **not in the pulse** — no target channel exists | — | — | **Absent (not secret)** | false → the execute half of L7 never fires |
| 14 | `dot_refreshable` | **not in the pulse** — needs `abilities[base].uptime` off the tracked bar's duration | — | — | **Absent (blocked)** | false → **L8 never fires**; the DoT goes unmanaged |
| 15 | `cataclysm_usable` | `cd` on Cataclysm (readiness model) | exact | edge/baseline/napkin | **Med–High** | unknown → false |
| 16 | `aoe_mode` | `mode` (the manual `single`/`multi`/`aoe` toggle) | exact | exact | **High (as a toggle)** | it is a *player declaration*, not an observation — it is never wrong, only stale |
| 17 | `rof_usable` | `shards >= 3` + off GCD | exact | **readable** | **High** | cost unreadable → assume 3 |
| 18 | `ib_usable` | `override`/`liveSpellID` on the **Incinerate** frame = the Infernal Bolt Art id | exact | override event *should* fire | **Low — likely blind** | ⚠ if Incinerate is untracked there is no frame carrying the override → false. See below |

## The five fields that need a decision or a check

- **The fragment read (#1b) — the one genuinely new capability question.**
  `State.lua`'s `readOnePower` calls `UnitPower("player", value)` with **no unmodified
  flag**, so it returns whole shards; Destruction's fractional generation is invisible.
  The documented route to fragments is the *unmodified* power read scaled by the
  power's display modifier — i.e. a second argument and a divisor, not a new event or a
  secret-value workaround. **Verify** that (a) the unmodified read is not itself secret
  in combat and (b) it is worth the fidelity: the payoff is restoring simc's `<= 4.2` /
  `<= 4.6` gates instead of the conservative rounding in `rotation.md`. Note this also
  forces a `resourceDisplay` member (`notes.md`), so it is a **contract-touching**
  change, not a spec-local one.

- **`dot_refreshable` (#14) blocks a whole line and is the spec's spine.** Immolate is
  tracked as the **DoT aura `157736`**, which is the encouraging part — a tracked bar
  item is where a duration would come from, and `abilities[base].uptime` is already on
  the backlog. **Do not** approximate it from `history`: a DoT refreshed by Soul Fire,
  spread by Cataclysm, or ticking on a target that has since died is not
  reconstructible from "I cast Immolate 14 s ago." Until the uptime read lands, L8 is
  honestly dead — and a Destruction HUD that cannot say "refresh your DoT" is missing
  the spec's most important call. **This is the gating item for the spec, not a
  polish item.**

- **`ib_usable` (#18) is probably a hard blind spot, and worse than Demo's.**
  Demonology's Shadow Bolt → Infernal Bolt half is blind because Shadow Bolt is not in
  the tracked set. Destruction's Incinerate → Infernal Bolt half looks blind **for the
  same reason** — Incinerate does not appear in the cooldown-set union at all
  (`notes.md`). The difference is that Incinerate is Destruction's *floor press*, so
  the missing frame costs more than the missing proc does. **First thing to check on a
  live capture**; if confirmed, it is the concrete need that un-parks the curated
  layout override in `docs/status.md`.

- **Charges (#6, #11).** Not a Destruction quirk so much as a project gap that
  Destruction is the first spec to hit. Capturing a Destruction `/cdmp probe`
  **closes** the `charge` open item in `docs/status.md` — worth doing early, since the
  answer changes how two rotation lines behave.

- **`target_execute` (#13) — decide whether the pulse gets a target channel.** It is
  cheap to *read* and not secret, but it is a new class of observed thing (target
  state, which changes on every target swap) and the pipeline currently has none. The
  honest options are: add a minimal target channel, or accept that Shadowburn's
  execute half never fires and let the player make that call. **This is a design
  decision, not a capability limit** — worth stating so it does not get filed under
  "Secret Values" and forgotten.

## What is simply not observable (and no field pretends to be)

- **Backdraft stack count** — the Conflagrate gate. Presence only; L4 is deliberately
  stricter than simc as a result.
- **Wither stack count** *(Hellcaller)* — the 8-stack Blackened Soul threshold.
  Maintenance only.
- **Target count** — Rain of Fire's real gate (~8+ Diabolist, 5+ Hellcaller). Replaced
  by the manual `mode` toggle, which is a declaration rather than an observation.
- **Havoc's target selection** — a roster with time-to-die. No roster, no TTD; Havoc
  can only be offered as availability with the reason stated, never as a press.

All four absences are load-bearing: they are why L4 holds Conflagrate early, why L10 is
mode-gated rather than count-gated, and why Havoc is not in the priority list at all.
