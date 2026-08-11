# Combat Assist Plus — open questions

**What this file is for:** product questions that still require an author decision. It holds
the smallest live options and what would decide between them. Approved behavior belongs in
`spec.md`; agreed work in `backlog.md`; completed reasoning in `notes.md`.

The simplification decisions are settled: one emphasis rather than HIGH / MEDIUM / LOW,
readable-only markers are first-class, catalogs name only enhanced abilities, automatic
current/next sequences are removed, the baseline is static, the only bar experiment is
Tyrant, and the pilot is Demonbolt plus Tyrant. Those choices are not reopened here.

## D18 — What static emphasis survives real icon art?

The baseline needs one treatment that is clearly more informative than Blizzard's stock proc
glow without turning every enhanced icon into an alarm.

Smallest candidates:

- a static ring outside the icon;
- a static border or underlay with a different silhouette;
- a restrained icon treatment combined with a separate context marker.

The first flight should compare brightness, contrast, size and stock-proc interaction on the
actual CDM surface. No alpha, blend mode or geometry is approved before that look.

**Baseline under test:** a static three-pixel gold border outside the icon. Its exact paint is
a disposable hypothesis until the Phase 5 flight.

## D19 — How should stock proc glow coexist with Demonbolt emphasis?

The first suppression attempt did not visibly dim Blizzard's proc glow. The product need is
only that Demonbolt's readable shard context not be drowned out.

Smallest options:

- reliably soften the stock glow while cap has a Demonbolt opinion;
- leave it intact and make cap's static treatment distinguishable by shape and position;
- stop adding icon emphasis and put shard context in a nearby marker instead.

First instrument whether the alert field resolves and whether the setter runs. Then choose by
looking; a successful setter call cannot decide the visual result.

**Baseline under test:** leave the stock glow intact and distinguish cap by the static outer
border. The draw capture says `stock:coexist`; it does not claim the two are visually distinct.

## D20 — What should the two Tyrant setup markers look like?

The facts are approved: separate readable markers for Dreadstalkers and Grimoire setup state,
with no combined press/don't-press verdict. The remaining choice is how the player tells the
facts apart without learning a miniature legend.

Smallest options:

- two fixed-position dots with distinct colors;
- simple glyphs tied to the source abilities;
- one compact two-cell marker whose positions are stable.

Choose the simplest form the player can identify during a real Tyrant setup.

**Baseline under test:** a blue left dot for Dreadstalkers committed and a purple right dot for
the transformed Grimoire row. These are commitment facts, not pet-active indicators.

## D21 — Does the Tyrant bar earn its surface?

The bar is deliberately independent of icon emphasis and markers. It succeeds only if the
next burst window becomes easier to read than it is from the CDM icon alone.

After one flight, keep it if the countdown is legible and useful without pulling attention
away from the icon. Otherwise remove the bar rather than generalizing it to more cooldowns.
