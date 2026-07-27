# tyrant-ready — rationale

**Situation:** combat; **5 soul shards** (cap); the summon board is **freshly laid** — Call
Dreadstalkers and Grimoire: Imp Lord were both just cast (history `succeeded` at t≈998.5 / 997.0)
and Wild Imps are out (`143038` `buff.isActive:true`); no Demonic Core; no Demonic Art armed.
**Summon Demonic Tyrant reads probably-up** (napkin `unknown`).

**Oracle (rotation source → expected Guidance):**
- This is the **Tyrant entry** moment. `rotation.md` step 6: *"Summon Demonic Tyrant at 5 Soul
  Shards — the primary cooldown; enter it with a full board (Dreadstalkers + grimoire demons
  freshly out, imps banked)."* `diabolist-sequences.md` SEQUENCE 2 pins the exact micro-order:
  *"…→ Call Dreadstalkers → [Grimoire: Imp Lord] → Summon Demonic Tyrant → Hand of Gul'dan →
  Hand of Gul'dan…"*. The board is already set (Dreadstalkers + Imp Lord down, imps out) and
  shards are at cap → **Tyrant is the #1 ready ability → the single `ROTATION` press.**
- **Hand of Gul'dan does NOT draw** even though it is affordable (5 shards). In the entry block
  Tyrant **precedes** HoG (`Tyrant → HoG HoG`): you press Tyrant first so it empowers the fresh
  board, *then* flood HoG inside the window. Spending shards on HoG before Tyrant would delay the
  60 s cooldown and waste the full-board burst. HoG is `AVAILABLE` (unlisted), not the call.
- **Call Dreadstalkers (`671`) and Grimoire: Imp Lord (`135056`) do NOT draw** — both were just
  cast (history + napkin `cooling` with `remaining`), so they are on cooldown, not competitors.
  This is why Tyrant, not Dreadstalkers, is the press: for Tyrant to be the go, Dreadstalkers must
  **already be on the board** (SEQUENCE 2 makes Dreadstalkers the *last cast before* Tyrant). A
  Dreadstalkers that were still castable would itself be the `ROTATION` press and Tyrant would
  wait — so the board-is-fresh state is what licenses the Tyrant call.
- **Demonbolt (`1979`)** is reactive — needs a Demonic Core, which is down (`777`
  `buff.isActive:false`, Demonbolt `glow:false`). Unlisted.
- **Implosion (`149122`)** is cooling (napkin) and the mode is `st` — not a call. Unlisted.
- **Shadow Bolt (`34990`)** is filler, pressed only when nothing better is affordable; Tyrant (and
  HoG) are affordable. Unlisted.
- **No `SEQUENCE` pane.** This is a *recurring* ~60 s Tyrant entry mid-fight, not an opener — the
  single `ROTATION` press carries it. `sequence.show:false` (the burst/opener pane is reserved for
  opener-active scenarios).

**Readability (the crux):**
- Tyrant's cooldown is **secret in combat** (`readable:false`). Its readiness is supplied by the
  **napkin** as `state:"unknown", source:"napkin"` with **no `remaining`** — the honest "the
  estimate ran out, so it's probably up" reading. Per napkin honesty a napkin cd is **never**
  `"ready"` (that is a live read, which does not happen in combat). So the `ROTATION` call does
  **not** rest on a cd read.
- What the `ROTATION` press actually traces to: **`power.SoulShards.value = 5` (readable)** — the
  shard gate step 6 names — plus the **fresh-board** evidence, all readable: Dreadstalkers +
  Imp Lord in **history** (`succeeded`) and Wild Imps out via **`143038 buff.isActive:true`**. The
  napkin-probably-up is corroboration; the *gate* that makes it pressable now is the readable
  shard cap + board.
- `aura` fields are `readable:false` throughout (C_UnitAuras dark in combat) and are never the
  source. No Art is armed (`9426 buff.isActive:false`), so HoG and Shadow Bolt are **not**
  transformed — `liveSpellID == spellID` on both (identity-coherence holds; no Ruination / Infernal
  Bolt hat here).

**Contract invariants exercised:**
- **Single-top-press among competing ready abilities.** Both Tyrant (burst CD, probably-up) and HoG
  (spender, 5 shards) are castable, yet exactly **one** `ROTATION` draws (Tyrant). HoG is demoted
  to `AVAILABLE` by rotation priority, not by unavailability — the case that distinguishes a
  *ranked winner* from independent per-ability lights.
- **Napkin honesty.** A hard cooldown reads as "probably ready" via `state:"unknown"` /
  `source:"napkin"` / **no `remaining`**, and the press is justified from readable shards + board
  rather than the secret cd.
- **resourceBar at cap.** `value:5, incoming:0` (no builder in flight — the in-flight history is
  summons, which do not project a shard delta).
- **`sequence.show:false`** at a recurring cooldown entry (no opener pane).
