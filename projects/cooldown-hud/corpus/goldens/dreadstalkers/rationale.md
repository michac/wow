# dreadstalkers — rationale

**Situation:** combat, **outside** a Tyrant window; Summon Demonic Tyrant is cooling far away
(~35s, napkin); **Call Dreadstalkers is probably-up**; 3 soul shards; no Demonic Core; no Demonic
Art armed (Shadow Bolt / Hand of Gul'dan un-transformed); Grimoire: Imp Lord still on its long
(~2-min) cooldown; Implosion cooling.

**Oracle (rotation source → expected Guidance):**
- **Call Dreadstalkers is the #1 press.** The source treats the hard cooldowns as use-it-or-lose-it:
  *"Everything hard is on a clock: Tyrant 60s, Dreadstalkers 20s, Imp Lord 2min, Implosion 15s.
  Press on cooldown"* (`diabolist-sequences.md`, TL;DR + proc taxonomy). The steady-state loop
  closes with the explicit rule *"…and Call Dreadstalkers whenever it's up and Tyrant isn't
  imminent"* (loop, and `rotation.md` step 5). Here it **is** up and Tyrant **isn't** imminent
  (~35s away, well past the ~20s Dreadstalkers cooldown), so the "hold it to be the last cast
  before Tyrant" caveat does not apply — holding would waste the cooldown. **Press it now →
  single `ROTATION`.**
- **Hand of Gul'dan does NOT draw.** HoG is affordable (3 shards ≥ its cost of 3), but it is a
  *resource-gated* spender that is available on every GCD the shards allow, whereas Dreadstalkers
  is *time-gated* and lost if delayed. The shard bucket is at **3/5 — not near cap**, so there is
  no overcap pressure forcing a spend this GCD (contrast `incoming-overcap`, where a projected 5
  makes HoG the press). With no cap pressure, the always-available spender yields to the
  use-it-or-lose-it summon that feeds the next Tyrant. HoG stays `AVAILABLE` (unlisted).
- **Demonbolt** is reactive on a Demonic Core — Core is **down** (`buff.isActive:false` on 777,
  `glow:false` on 1979) — not a call. Unlisted.
- **Shadow Bolt** is the builder/filler (source: press only when nothing better is affordable).
  Dreadstalkers and HoG both outrank it; and shards aren't starved. Unlisted.
- **Summon Demonic Tyrant** is cooling ~35s out — not ready, and not close enough to raise `SOON`.
  Unlisted (see the contrast below).
- **Grimoire: Imp Lord** pairs with Tyrant (SEQUENCE 2) and is on its own long cooldown (~52s,
  cooling) — not up, not a competing press. Unlisted.
- **Implosion** — cooling, and this is single-target (`mode:"st"`); its real gate is ≥6 Wild Imps
  in AoE. Not a call. Unlisted.
- No `SEQUENCE` pane: no opener/burst plan is active (steady state, outside the Tyrant block).

**Readability (the crux):**
- Every `cd` read is `readable:false` in combat. Dreadstalkers' "probably-up" is the **napkin
  estimate elapsing**: `{ "state":"unknown", "readable":false, "source":"napkin" }` with **no
  `remaining`** — the sanctioned "hard-CD past due → probably ready" read. This is a **readable
  napkin signal**, distinct from `source:"none"` (an instant with no cd model, e.g. HoG/SB/DB),
  and it is what justifies the `ROTATION` call. Napkin honesty holds: it is `unknown`, never
  `ready` (a live read that never happens in combat).
- HoG's exclusion rests on the **readable shard value** (`power.SoulShards.value:3`, not capping),
  not on any secret cd.
- Core-down rests on **`buff.isActive` + `glow`** (both readable), never on `aura`
  (`readable:false` in combat).
- No `transient`: Dreadstalkers has been sitting available (steady-state), not a fresh `ready`
  edge, so — like `hand-of-guldan` — the steady `ROTATION` carries no transient.

**Contrast — why not `SOON`/stage (the sibling case):** Tyrant here reads `cooling`/remaining ~35.
If Tyrant were instead **near** (a short napkin countdown, ~2s out), the call would flip: you would
**hold** Dreadstalkers so its pair lands fresh *inside* the Tyrant window (SEQUENCE 2:
"Dreadstalkers is the last thing you press before Tyrant"), and Tyrant's frame would draw `SOON`
(anticipation, not a press) while Dreadstalkers dropped to `AVAILABLE`. At 35s, Tyrant is too far
to anticipate and nothing is worth staging — so Dreadstalkers presses on cooldown now.

**Invariants exercised:**
- **Single-top-press:** exactly one `ROTATION` (Dreadstalkers); every other ready/affordable
  ability (notably HoG at 3 shards) caps at `AVAILABLE` and is unlisted.
- **Cooldown-gated beats resource-gated when the resource isn't capping** — the ranking is a
  *winner*, not per-ability lights.
- **Napkin "probably-up" (`unknown`/`source:napkin`, no `remaining`)** as the readable stand-in
  for a secret cooldown — and its separation from `source:"none"`.
