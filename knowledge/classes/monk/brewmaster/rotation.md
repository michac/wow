---
title: Brewmaster Monk — Rotation (Midnight S1)
patch: 12.0.7
fetched: 2026-07-11
reviewed: 2026-07-11
sources:
  - simc midnight branch profiles/MID1/MID1_Monk_Brewmaster.simc  # tier 1 APL, WoW 12.0.7, fetched 2026-07-11
  - https://raw.githubusercontent.com/simulationcraft/simc/midnight/profiles/MID1/MID1_Monk_Brewmaster.simc  # tier 1
  - https://www.icy-veins.com/wow/brewmaster-monk-pve-tank-rotation-cooldowns-abilities  # tier 3, 12.0.7, 2026-07-11
  - https://www.method.gg/guides/brewmaster-monk/playstyle-and-rotation  # tier 3, upd. 2026-06-17
  - https://www.wowhead.com/guide/classes/monk/brewmaster/rotation-cooldowns-pve-tank  # tier 4, corroboration
confidence: medium
---

# Brewmaster Monk — Rotation (Midnight S1)

Distilled from the **SimulationCraft MID1 default APL** (tier 1) for 12.0.7,
corroborated by the Icy Veins and Method 12.0.7 guides. Brewmaster is a tank,
so the "rotation" is really two interleaved jobs: a **threat/damage priority**
(Keg Smash-centric) that also builds mitigation, and a **defensive brew** layer
(Purifying Brew / Celestial Brew / Stagger) you weave on top reactively.

> **12.0.7 "Revelations" — Brewmaster went unchanged this patch** (Method:
> "no Brewmaster-specific changes in 12.0.7"; only new Sporefall raid items to
> chase). The priority below is the Midnight-simplified kit: **Rising Sun Kick
> and Weapons of Order are gone**; the loop now runs through the apex talent
> **Bring Me Another** (Brews → **Empty Barrel** → supercharged **Keg Smash**)
> and, for Master of Harmony, the **Aspect of Harmony** accumulator feeding a
> big Celestial Brew.

## Core principle

Two rules dominate everything:

1. **Never miss a Keg Smash.** It is the biggest damage source *and* the engine
   for Brew cooldown-reduction and **Shuffle** uptime. The APL and Icy Veins are
   emphatic: keep enough Energy banked to cast it on cooldown. With **Bring Me
   Another**, a held **Empty Barrel** resets Keg Smash and slashes its cost — so
   spend the barrel promptly to chain an extra Keg Smash.
2. **Purify with timing, not on cooldown.** Purifying Brew clears 50% of the
   *current* Stagger pool — using it right after a big hit (while the pool is
   fat) mitigates far more than reflexively dumping charges. Keep Shuffle up so
   more damage is staggered in the first place.

## Pre-combat / opener

1. (Optional) Pre-cast **Breath of Fire** ~3s before pull for Charred Passions.
2. **Rushing Jade Wind** in the last ~2s before combat (if talented over Special
   Delivery).
3. **Chi Burst** as you run in.
4. **Keg Smash** → **Keg Smash** (Provoke if you're the pulling tank).
5. **Blackout Kick** → **Breath of Fire**.
6. **Tiger Palm** to consume Blackout Combo.
7. **Exploding Keg** / **Invoke Niuzao** (stagger the two across the opener).
8. **Keg Smash** → **Blackout Kick** → the other of Exploding Keg / Niuzao.
9. Fall into the single-target priority.

## Cooldown rules

- **Black Ox Brew** (off-GCD) when Celestial Brew charges are low / you need an
  immediate Purifying Brew refill + Energy dump. The APL fires it when
  `celestial_brew.charges_fractional < 1` (MoH) / `< 0.5` (Shado-Pan).
- **Invoke Niuzao** on cooldown as a coupled damage + mitigation window; for
  **Shado-Pan**, the APL prioritizes **Breath of Fire** and **Keg Smash while
  Niuzao is up** *if* Sal'salabim's Strength is talented.
- **Fortifying Brew** / **Zen Meditation** / **Diffuse Magic** are reactive
  panic buttons — hold for spike windows, not on cooldown.
- **Touch of Death** whenever available (execute/burst).
- **Potion & racials** are dumped early in the APL (no special sync window for a
  tank — use them in your damage window, typically with Niuzao).

## Single-target priority (Shado-Pan)

Order follows the MID1 `shado_pan` action list, simplified to buttons:

1. **Black Ox Brew** — off-GCD, when Celestial Brew charges are nearly empty.
2. **Breath of Fire → Keg Smash while Niuzao is up** — only if **Sal'salabim's
   Strength** is talented (elevates these during the Niuzao window).
3. **Blackout Kick** — to apply the **Blackout Combo** buff (if talented and the
   buff is down).
4. **Purifying Brew** — defensive; clear Stagger (respect the Empty Barrel guard).
5. **Fortifying Brew** — if a defensive window calls for it.
6. **Chi Burst**.
7. **Invoke Niuzao**.
8. **Tiger Palm** — to *consume* Blackout Combo when Blackout Kick is ~1.3s from
   coming back.
9. **Exploding Keg** — when Keg Smash has < 1 charge available.
10. **Empty the Cellar** — when its buff is about to fall off.
11. **Tiger Palm** — to consume any remaining Blackout Combo.
12. **Celestial Brew / Celestial Infusion** — spend the absorb.
13. **Keg Smash** — the core builder; cast on cooldown / when the Empty Barrel
    is up.
14. **Empty the Cellar** (secondary use).
15. **Breath of Fire**.
16. **Rushing Jade Wind** — refresh.
17. **Blackout Kick**.
18. **Tiger Palm** — Energy dump when `energy > 65 - regen` (don't cap Energy).
19. **Expel Harm** — filler / self-heal.

## Single-target priority (Master of Harmony)

Same skeleton, with the **Aspect of Harmony** layer elevated (MID1
`master_of_harmony` list):

- **Black Ox Brew** when a Celestial Brew charge is needed.
- **Celestial Brew when the Aspect of Harmony *spender* is up** (and no Empty
  Barrel to protect) — this is the big absorb/heal discharge; a top priority.
- **Keg Smash while the Aspect spender is up *and* an Empty Barrel is up** — pairs
  the barrel throw with the discharge.
- **Blackout Kick** to set Blackout Combo → **Tiger Palm** to consume it.
- **Celestial Brew** when the Aspect **accumulator** value exceeds ~30% of max HP
  and you have spare charges (or ~20% if the target is about to die).
- **Purifying Brew** (Empty Barrel guard) → **Fortifying Brew** → **Chi Burst**
  (pulled higher for MoH) → **Invoke Niuzao**.
- Then the shared filler chain: **Exploding Keg** (Keg Smash < 1 charge) →
  **Empty the Cellar** → **Breath of Fire** → **Keg Smash** → **Rushing Jade
  Wind** → **Blackout Kick** → **Tiger Palm** (energy dump `>50 - regen*2`) →
  **Expel Harm**.

## Cleave / AoE (2+)

The lists barely branch — Brewmaster's whole kit is already AoE (Keg Smash,
Breath of Fire, Spinning Crane Kick, Rushing Jade Wind, Exploding Keg, Niuzao
Stomp). Differences vs single target:

- **Breath of Fire** moves up (`active_enemies > 2` in the Shado-Pan APL) to keep
  the DoT / **Charred Passions** on the whole pack.
- **Empty Barrel Keg Smash ricochets** across multiple targets (Bring Me Another)
  — extra reason to spend the barrel in AoE.
- **Spinning Crane Kick** is used *situationally* to gather / for Charred-Passions
  cleave — **not** on the strict priority, because it gives no mitigation.
- **Exploding Keg** and **Rushing Jade Wind** carry more weight; keep RJW up.
- Otherwise: Keg Smash on cooldown → Breath of Fire → fillers, exactly as ST.

## Hero-tree branches

- **Shado-Pan** — M+/big-pull leaning. Physical burst via **Flurry Strikes** and
  a stronger **Invoke Niuzao** window; the APL specifically re-prioritizes
  Breath of Fire + Keg Smash *during Niuzao* when **Sal'salabim's Strength** is
  talented. Simpler, more "press Keg Smash and cleave."
- **Master of Harmony** — raid/single-target leaning. The **Aspect of Harmony**
  accumulator turns your damage/healing into a bankable Celestial Brew discharge,
  and MoH grants a second Celestial Brew/Infusion charge for smoother, more
  self-sufficient mitigation. **Chi Burst** is a real rotational button here, not
  a filler.

## TODO

- [ ] Re-distill against a top WCL Brewmaster log (`wowkb.wcl rankings` → `casts`)
      to confirm real-game Purifying/Celestial cadence vs the sim's absorb math.
- [ ] Confirm exact Bring Me Another apex-rank behavior (Empty Barrel proc %, Keg
      Smash cost reduction, Refreshing Drink) in-game — @verify-ingame.
- [ ] Pull precise Brew charge counts / recharge and Fortifying/Niuzao/ToD CDs
      from the Blizzard spell API for the abilities table.
