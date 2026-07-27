# soon-anticipated — rationale

**Situation:** combat; **4 soul shards** banked (no cast in flight → `incoming:0`); **Summon
Demonic Tyrant ~2 s from ready**; **Call Dreadstalkers probably up**; Grimoire: Imp Lord still on
its 2-min cooldown (it was paired with the last Tyrant ~58 s ago); no Demonic Core; few Wild Imps
out. This is the **Tyrant-entry staging beat** — the moment right before the 60 s burst window.

**Oracle (rotation source → expected Guidance):**

- **Dreadstalkers is the single `ROTATION` press.** `diabolist-sequences.md` SEQUENCE 2 (the Tyrant
  entry block, "the single most repeatable pattern in the data") states the learnable rule verbatim:
  *"Dreadstalkers is the last thing you press before Tyrant… Then Tyrant, then immediately dump
  Hand of Gul'dan."* The cast *immediately* before Tyrant is Call Dreadstalkers in essentially
  every window across all six parses, because Tyrant extends the freshly-summoned pair. With Tyrant
  ~2 s out and Dreadstalkers available, the correct thing to press **now** is Dreadstalkers so the
  pair is on the board when Tyrant lands. → the one `ROTATION`.

- **Tyrant draws `SOON`, not a press.** Tyrant is ~2 s away (napkin `anticipated`, `remaining:2.0`).
  Per the contract, `SOON` = "anticipating — not yet pressable." It is **not** a press claim, so it
  legally coexists with the single `ROTATION`. The pass-through `note` ("~2s — stage demons first")
  is the countdown-ish hint the scenario calls for; it is opaque display text, not a token.

- **Hand of Gul'dan is HELD — the correction baked into this case.** 4 shards are affordable
  (`rotation.md` step 9: HoG at ≥3 shards), so a naïve per-ability light would green HoG. But the
  Tyrant-entry doctrine is explicit: you **bank shards pre-Tyrant** and flood `HoG HoG` *inside*
  the window (SEQUENCE 2 → SEQUENCE 3: "`HoG HoG` opens the window"; the single biggest DPS lever is
  how many HoG casts you fit **inside** the Tyrant window, per `rotation.md` Core idea). Spending
  shards on HoG now would waste the window's flood potential. So HoG is demoted to `AVAILABLE`
  (unlisted). This is the same shard-exclusion discipline as `demonbolt-proc`/`incoming-overcap`,
  applied to *timing* rather than *cost*.

- **Losers, all `AVAILABLE` (unlisted):**
  - **Shadow Bolt** (`34990`) — filler/builder; you would only build if starved, but you are at 4
    shards with the staging press available. Not the call.
  - **Demonbolt** (`1979`) — reactive on a Demonic Core; Core is down (`777` `buff.isActive:false`,
    `glow:false`). Not a call.
  - **Grimoire: Imp Lord** (`135056`) — SEQUENCE 2's other pre-Tyrant summon, but it is still
    cooling (napkin `anticipated`, ~62 s out — a 2-min CD that lines up with only ~every other
    Tyrant). Down this window, so it does not compete for the staging press; Dreadstalkers stands
    alone.
  - **Implosion / HoG** — HoG held (above); Implosion isn't in the subset (ST, imps not out).

**Readability (what's secret, what stands in):**

- Every `cd` is `readable:false` (combat secret). Dreadstalkers' readiness is supplied by the
  **napkin** as the *elapsed* shape — `{ state:"unknown", source:"napkin" }` with **no** `remaining`
  — the model's "hard-CD probably ready in combat." The `ROTATION` press therefore traces to a
  **readable napkin estimate**, exactly the signal the contract permits (shards / glow /
  `buff.isActive` / a napkin estimate).
- Tyrant's `SOON` traces to the **napkin `anticipated`** countdown (`remaining:2.0`, `source:napkin`).
  Napkin honesty holds: it is anticipated with `remaining>0`, never "ready" (ready is a live read
  that never happens in combat).
- The decision to **hold HoG** is driven by the readable Tyrant-imminent napkin — the Coach sees the
  window ~2 s out and stages instead of spending. No secret drove a drawn cue.
- `aura` is `readable:false` throughout (combat), and no cue rests on it. Wild Imp / Demonic Core
  **counts** are secret; here neither gates a drawn cue (imps-out `buff.isActive:false` only supports
  "summons not all out yet" narratively).

**Contract invariants exercised:**

- **Single-top-press:** exactly one `ROTATION`/`LATE` (Dreadstalkers). `SOON` on Tyrant is
  anticipation, not a press, and coexists — the case that proves `SOON` + `ROTATION` legally
  co-occur.
- **`SOON` semantics:** an anticipated napkin countdown surfaces as `SOON` with a pass-through note,
  never as a press.
- **Timing-based demotion:** an *affordable* spender (HoG, 4 shards) is correctly withheld because
  the rotation banks it for the Tyrant window — the oracle encodes rotational timing, not just cost.
- **Readable-only justification:** both drawn cues trace to napkin/power readables; no secret cd or
  aura is read.
