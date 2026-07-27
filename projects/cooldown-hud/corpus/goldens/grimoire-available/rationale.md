# grimoire-available — rationale

**Situation:** combat, AoE (`mode:"aoe"`); 3 soul shards; no Demonic Core proc; no Wild Imps
flooded yet; **Grimoire: Imp Lord (135056) is off cooldown** (napkin says probably-up);
Tyrant / Dreadstalkers / Implosion all cooling (napkin). A normal build/spend press exists.

**Oracle (rotation source → expected Guidance):**
- **HoG is the readable `ROTATION` winner.** With 3 shards banked and no higher call up, Hand of
  Gul'dan is the primary spender the shard economy points at (`rotation.md` step 9: spend shards
  with HoG; `diabolist-sequences.md` steady-state loop: "Soul Shards ≥ 3 → Hand of Gul'dan").
  Its gate is **shards**, which are readable — so the press rests entirely on readable state.
- **Grimoire: Imp Lord is off cd but does NOT independently green.** It is **unlisted**
  (`draw:false` = `AVAILABLE` internal) — deliberately *not suppressed*, but *not a standalone
  press either*. The rotation source is explicit that Imp Lord's correct press is a **sequence
  position, not a lone light**: `diabolist-sequences.md` SEQUENCE 2 (Tyrant-entry block) — *"…→
  Call Dreadstalkers → [Grimoire: Imp Lord] → Summon Demonic Tyrant → Hand of Gul'dan"* — pairs
  Imp Lord **right beside Dreadstalkers, immediately before Tyrant** (it is a ~2-min CD that lines
  up with ~every other Tyrant). Firing it as a lone light in open filler, with Tyrant ~26 s away
  and Dreadstalkers still cooling (~9 s), would waste the Tyrant pairing that is its whole value.
  So off-cd-Grimoire is `AVAILABLE`, and the **readable build/spend winner (HoG) is the one
  `ROTATION`.**
- **No `SEQUENCE` cue.** `SEQUENCE` (attention-redirect to the panel) fires when the panel holds
  the salient plan — an opener or an imminent Tyrant-entry block. Here we are in **steady state**:
  Tyrant is ~26 s out (napkin), so the Tyrant-entry sequence is not yet active and no panel is
  driving. `sequence.show:false`, and no `SEQUENCE` emphasis is drawn. (When Tyrant becomes
  imminent and Dreadstalkers comes up, a paired scenario would surface SEQUENCE 2 as the pane —
  that is where Imp Lord's press actually lives.)
- **Demonbolt** is reactive — needs a Demonic Core, which is down (`777` `buff.isActive:false`,
  `glow:false`). Not a call. Unlisted.
- **Shadow Bolt** is the filler (`rotation.md` step 12) — the press only when nothing else is
  affordable. HoG is affordable, so Shadow Bolt does not draw. Unlisted.
- **Implosion** — even in AoE, its gate is ≥6 Wild Imps, and no imps are out yet
  (`143038` `buff.isActive:false`); it is also cooling (napkin). Not a call, not even `JUDGE`.
  Unlisted.
- **Tyrant / Dreadstalkers** are cooling (napkin) — not ready, not close enough for `SOON`. Unlisted.

**Readability:** every `cd` read is `readable:false` (combat secret). Grimoire's off-cd status is
**not** a live "ready" read — it is the **napkin's probably-up** estimate (`cd.state:"unknown"`,
`source:"napkin"`, **no** `remaining`, per the napkin-honesty rule: a napkin cd may never be
`"ready"`). Crucially, that probably-up signal is what lets the Coach *consider* Grimoire, but the
oracle still declines to green it as a lone press — the decision is a **rotation-shape** judgment
(sequence position), not a readability gap. HoG's `ROTATION` rests on readable shards; nothing
leans on a secret.

**Contract checks this exercises:**
- **Single-top-press holds** — exactly one cue is `ROTATION` (HoG); Grimoire, though off cd, is
  `AVAILABLE` (unlisted), not a second press. This is the case that proves *off-cooldown ≠
  automatically greened*: a hard-CD summon whose value is its Tyrant pairing stays internal until
  the sequence calls it.
- **AVAILABLE-is-unlisted convention** — the decision-relevant subset carries Grimoire (napkin
  probably-up) precisely so the validator can confirm the winner is justified *despite* a
  competing off-cd ability, and that the competitor is correctly demoted to no-cue.
- **Secrecy gate** — no drawn cue leans on a `readable:false` fact; the lone `ROTATION` traces to
  readable `power.SoulShards`.
