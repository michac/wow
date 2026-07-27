# opener-midflight — rationale

**Situation:** combat ~4 s in (opener still running). History shows **Call Dreadstalkers**
(`104316`) and **Grimoire: Imp Lord** (`1276452`) already **succeeded**; **Summon Demonic Tyrant**
has *not* been cast yet. 3 soul shards. No Demonic Core, no Diabolic Ritual armed, no Wild Imps out
(no Hand of Gul'dan has landed). `mode:st`.

**Oracle (rotation source → expected Guidance):**
- `diabolist-sequences.md` **SEQUENCE 1 — Opener (FIXED, learnable)** is the authority here. Its
  burst skeleton (1a) is `… Call Dreadstalkers → Grimoire: Imp Lord → Summon Demonic Tyrant → Hand
  of Gul'dan → Hand of Gul'dan → (Implosion only if adds) …`, and SEQUENCE 2 confirms the fixed
  micro-order **"Dreadstalkers is the last thing before Tyrant; if Imp Lord is up press it next to
  Dreadstalkers; then Tyrant, then dump Hand of Gul'dan."** Because the opener is the single most
  **sequence-able** part of the spec ("the most sequence-able part of the spec"), the salient plan
  lives in the **panel**, not in a per-icon press light.
- **Panel state (readable evidence → stepState):**
  - `done` × 2 — Dreadstalkers + Imp Lord are in `history` as `succeeded` (readable history).
  - `active` — **Tyrant** is the cursor step: the two pre-Tyrant summons are down and Tyrant is not
    yet cast, so it is the current step (`cursor:2`). Per SEQUENCE 1a/2, Tyrant is pressed at
    t≈3–5 s with the board freshly summoned — exactly this moment.
  - `pending` — the first **Hand of Gul'dan** after Tyrant is affordable *when reached* (3 shards
    banked, HoG costs 3).
  - `blocked` — the **second** Hand of Gul'dan (SEQUENCE 3: `TYR → HoG HoG` opens the window) needs
    3 more shards, which we won't have after the first HoG zeroes the bar. Gate note **"Need 3
    shards"** — a readable-shard gate.
  - `skipped` — **Implosion** is the AoE drop-through (`rotation.md` step 7 / SEQUENCE-1 line 8:
    "Rotmire has adds — burst them; **pure ST: skip**"). `mode:st`, so the step passes without
    casting. Note **"AoE only"**.
- **The one drawn cue — Tyrant `2742` = `SEQUENCE`.** Per the contract, `SEQUENCE` is an
  **attention-redirect, not a press**: it points the player at the opener panel (which holds the
  plan) rather than lighting an icon to "press now". The active step is Tyrant, so the redirect
  reads correctly ("look at the panel — Tyrant is the step"). It is authored as `SEQUENCE`, **not**
  `ROTATION`, precisely because the opener panel is the salient carrier while it is active.

**Why nothing else draws (all demoted to `AVAILABLE`, unlisted):**
- **Hand of Gul'dan** (`34991`) is affordable (3 shards) and would normally be the `ROTATION` press
  in steady state (see `hand-of-guldan` golden) — but here the opener panel owns the plan and Tyrant
  comes **first** in the fixed sequence. Lighting HoG as `ROTATION` would fight the panel ("press
  Tyrant now"). Demoted to `AVAILABLE`.
- **Shadow Bolt** (`34990`) — filler only; not called while a spender/summon step is live. Unlisted.
- **Demonbolt** (`1979`) — reactive; no Demonic Core (`777` `buff.isActive:false`, no glow), so not
  a call. (Omitted from the subset — not decision-relevant.)
- **Implosion** (`149122`) — does **not** draw `JUDGE`: `mode:st` (Implosion is the AoE-only gate,
  `rotation.md` step 7) **and** no Wild Imps are out yet (`143038` `buff.isActive:false`), so the
  imp-count approximation isn't even close. It is the `skipped` panel step, nothing more.
- **Dreadstalkers / Imp Lord** (`671` / `135056`) — just cast, now cooling (napkin). Done steps, not
  presses. Unlisted.

**Readability & invariants:**
- Every drawn cue traces to **readable** signals: the SEQUENCE redirect rests on `history`
  (`succeeded` Dreadstalkers + Imp Lord → done steps), the **readable shard count** (pending vs
  blocked HoG gate, "Need 3 shards"), the combat flag + `combatStartedAt` (opener window), and
  `mode:st` (Implosion drop-through). No secret `cd` or `aura` is used to justify anything.
- Tyrant's own `cd` is `unknown / source:"none"` — at the opener it has never been on cooldown, so
  there is no napkin model; it reads as "available, no cd info". Honest: no false "ready" (a live
  read that never happens in combat).
- **Single-top-press:** **zero** `ROTATION`/`LATE` cues (allowed — "at most one"). `SEQUENCE`
  coexists with the resourceBar and would coexist with a `ROTATION`; here the panel deliberately
  holds the press, so no icon claims "press now".
- This is the **only** scenario exercising the **sequence pane** (`show:true`), the **`SEQUENCE`**
  emphasis, and **all five `stepState`s** (`done`, `active`, `pending`, `blocked`, `skipped`).
