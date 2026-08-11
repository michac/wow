---
id: ritual-sites
name: Ritual sites (Field Accolades + S2 crests)
goal: [gearing]
venue: world
group: solo
cadence: repeatable
time: standing
scope: character
status: active
gate: { type: always }
reward: { type: [power, currency], detail: "Field Accolades (uncapped, solo, → S2 Void-Touched Caches) + Season 2 crests at Delve-equivalent rates; 12.1 realigned T1-6 to S2 Delve tiers 1-6, so the T6 Myth-crest payout and the T6 Voidcore bonus roll are GONE — this is now an accolade engine, not a crest promotion" }
yields:
  currencies: { veteran_crest: 10, field_accolade: 100 }   # T6/run. 12.1: crests = S2 Delve-tier-equivalent, so T6 tops out at VETERAN Mistcrest — myth_crest/hero_crest removed. ⚠ per-run S2 crest AMOUNT is unpublished; 10 is a placeholder, not a sourced figure. Accolades unchanged.
time_blocks: 1
enjoyment: 1.2
urgency: 1
patch: 12.1
fetched: 2026-08-11
reviewed: 2026-08-11
sources:
  - https://worldofwarcraft.blizzard.com/en-us/news/24293281   # 12.1 "Curse of Ula'tek" content update notes, EVENTS → RITUAL SITES (Tier 1); verbatim in _meta/patch-notes/12.1.md
  - https://www.icy-veins.com/wow/midnight-patch-12-1-guide     # Tier 3 — corroborates the T4/T5/T6 ilvls and the vault realignment
  - knowledge/systems/ritual-sites.md
  - knowledge/endgame/delves/overview.md
  - knowledge/endgame/great-vault.md
confidence: medium
---
Farmable solo power engine — no weekly reset (`cadence: repeatable`), always available
(`gate: always`, U=1). Low urgency by design: it never expires, so it fills time after
the expiring weeklies are cleared. **Nothing here waits for Aug 18** — ritual sites are
unchanged by the pre-season split and run normally this week.

**⚠ 12.1 demoted this row — the Myth-crest promotion is dead.** Tier-1 notes: *"Ritual
Site tiers 1-6 vault rewards have been updated to match the Season 2 Delve tiers 1-6 vault
rewards"* and *"Ritual Sites now reward Season 2 crests equivalent to Delves at these
tiers."* Consequences, in order of how much they move the score:

1. **No more Myth crests.** The old **T6 = 5 Myth + 10 Hero Dawncrests/run** payout is
   gone. Crests are now Season 2 **Mistcrests** at the Delve-tier-equivalent rate, and
   S2 Delve tiers 1–6 top out at **Veteran Mistcrest** (`../../endgame/delves/overview.md`:
   T4 → Adventurer, T5–6 → Veteran). So this is **no longer the only repeatable solo
   Myth-crest source — it is not a Myth-crest source at all.** S2 Myth crests come from
   M+/raid and the T11 Gilded Stash at Delver's Journey rank 4. ⚠ The per-delve-tier crest
   mapping is Tier-3 and unverified, and the **per-run crest amount is unpublished** for S2
   — confirm both at the obelisk. @verify-ingame
2. **T6 Advanced Ritual Studies quests no longer grant a Nebulous Voidcore bonus roll**
   (the Weeks 3 & 6 bonus rolls). The quests remain completable for the achievement. Any
   scoring that leaned on those bonus rolls now has nothing behind it.
3. **Vault value drops with it.** T1–6 vault rewards match S2 Delve tiers 1–6, so a stack
   of ritual sites fills the world-row *counters* (2/4/8) at low slot quality while delve
   T7+ out-ranks it for what the row actually offers — and the first S2 vault caps the
   world row at Champion 3/6 anyway (`../../endgame/great-vault.md`). Run rituals for
   accolades/crests, delves for vault slot quality.

**New recommended ilvls: T4 259** (was 257) · **T5 268** (was 264) · **T6 275** (was 274).
T1–3 keep Season 1 recommended ilvls and tuning.

**What still justifies the row: Field Accolades.** Uncapped, solo, repeatable, ~100/run at
T5+, and 12.1 re-pointed the Void-Touched Cache vendor at Season 2 gear — **200 accolades**
= S2 Adventurer Warbound cache, **500** = S2 Veteran BoP (random slot), **750** = S2 Veteran
BoP (slot-specific), with the Season 1 caches removed. That makes accolade volume a live
gearing path again for a solo character early in S2. Coffer-key shards still drop, but
Blizzard calls the 12.1 shard retune "a work in progress" — don't plan a farm around a
shard number (`../../endgame/delves/overview.md`).

**Ranker note (tooling, not content):** `yields.currencies` now declares `veteran_crest`,
and `tools/wowkb/rewards.py` has **no `veteran_crest` entry in `CURRENCY_CONSUMERS`** — so
this row's crest yield currently values at 0 in the needs-first R override, which
under-rates it for a character still upgrading Veteran-track slots. Add the consumer (and
an `adventurer_crest` key) when the S2 crest rework lands in the scoring loop; see
`../../_meta/kb-inbox.md`. The pre-needs-first formula is unaffected — U=1, it never expires.
